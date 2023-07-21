#!/usr/bin/env python
# SPDX-License-Identifier: LGPL-2.1-or-later
#
# Example to create a new VPN network connection profile. Currently supported only with tls-auth
#
# $ examples/async/add-openvpn-connection-async.py --help
# usage: add-openvpn-connection.py [-h] [-c CONN_ID] [-d DEV] [--remote REMOTE] [--remote-cert-tls] [-a] [--save]
#                                  [--ca, CA_PATH] [--cert, CERT_PATH] [--key, KEY_path] [--ta, TA_PATH]
#
# Optional arguments have example values:
#
# optional arguments:
#   -h, --help         show this help message and exit
#   -c CONN_ID         Connection Id
#   -u UUID            Connection UUID
#   -f OVPN            .ovpn connection file
#   -a                 autoconnect
#   --save             Save
#   --ca               Path to CA file
#   --cert             Path to cert file
#   --key              Path to key file
#   --ta               Path to tls-auth file
#
# $ add-vpn-connection.py
# New unsaved connection profile created, show it with:
# nmcli connection show "MyConnectionExample"|grep -v -e -- -e default
#
# Connection Profile settings are described at:
# https://networkmanager.dev/docs/api/latest/ref-settings.html
#
# Note: By default, it uses add_connection_unsaved() to add a temporary
# memory-only connection which is not saved to the system-connections folder:
# For reference, see: https://networkmanager.dev/docs/api/latest/spec.html
# -> org.freedesktop.NetworkManager.Settings (Settings Profile Manager)

import asyncio
import functools
import logging
import sdbus
from uuid import uuid4
from argparse import ArgumentParser
from pprint import pformat
from sdbus_async.networkmanager import (
    NetworkManagerSettings as SettingsManager,
    ConnectionType,
)
from sdbus_async.networkmanager.settings import (
    ConnectionProfile,
    ConnectionSettings,
    Ipv4Settings,
    Ipv6Settings,
    VpnSettings
)


async def add_vpn_connection_async(conn_id: str,
                                   dev: str,
                                   remote: str,
                                   remote_cert_tls: str,
                                   uuid,
                                   auto: bool,
                                   save: bool,
                                   ca: str,
                                   cert: str,
                                   key: str,
                                   ta: str) -> str:
    # Add a temporary (not yet saved) network connection profile
    # param Namespace args: dev, remote, remote_cert_tls, ca_path, cert_path, key_path, ta_path
    # return: dbus connection path of the created connection profile

    info = logging.getLogger().info

    # If we add many connections passing the same id, things get messy. Check:
    if await SettingsManager().get_connections_by_id(conn_id):
        print(f'Connection "{conn_id}" exists, remove it first')
        print(f'Run: nmcli connection delete "{conn_id}"')
        return ""

    profile = ConnectionProfile(
        connection=ConnectionSettings(
            connection_id=conn_id,
            uuid=str(uuid),
            connection_type=ConnectionType.VPN.value,
            autoconnect=bool(auto),
        ),
        ipv4=Ipv4Settings(method="auto"),
        ipv6=Ipv6Settings(method="auto"),
        vpn=VpnSettings(data={
            'ca': ca,
            'cert': cert,
            'cert-pass-flags': '0',
            'connection-type': 'tls',
            'dev': dev,
            'key': key,
            'remote': remote,
            'remote-cert-tls': remote_cert_tls,
            'ta': ta,
            'ta-dir': '1'
        }, service_type='org.freedesktop.NetworkManager.openvpn')
    )

    s = SettingsManager()
    save = bool(save)
    addconnection = s.add_connection if save else s.add_connection_unsaved
    connection_settings_dbus_path = await addconnection(profile.to_dbus())
    created = "created and saved" if save else "created"
    info(f"New unsaved connection profile {created}, show it with:")
    info(f'nmcli connection show "{conn_id}"|grep -v -e -- -e default')
    info("Settings used:")
    info(functools.partial(pformat, sort_dicts=False)(profile.to_settings_dict()))
    return connection_settings_dbus_path


if __name__ == "__main__":
    logging.basicConfig(format="%(message)s", level=logging.INFO)
    p = ArgumentParser(description="Optional arguments have example values:")
    conn_id = "MyConnectionExample"
    p.add_argument("-c", dest="conn_id", default=conn_id, help="Connection Id")
    p.add_argument("-u", dest="uuid", default=uuid4(), help="Connection UUID")
    p.add_argument("--dev", dest="dev", default="tun", help="VPN Dev")
    p.add_argument("--remote", dest="remote", default="example.com:443:tcp", help="VPN Remote")
    p.add_argument("--remote-cert-tls", dest="remote_cert_tls", default="server", help="VPN Remote cert tls")
    p.add_argument("--ca", dest="ca", required=True, help="VPN CA file path")
    p.add_argument("--cert", dest="cert", required=True, help="VPN cert file path")
    p.add_argument("--key", dest="key", required=True, help="VPN key file path")
    p.add_argument("--ta", dest="ta", required=True, help="VPN TA file path")
    p.add_argument("-a", dest="auto", action="store_true", help="autoconnect")
    p.add_argument("--save", dest="save", action="store_true", help="Save")
    args = p.parse_args()
    sdbus.set_default_bus(sdbus.sd_bus_open_system())
    if connection_dpath := asyncio.run(add_vpn_connection_async(**vars(args))):
        print(f"Path of the new connection: {connection_dpath}")
        print(f"UUID of the new connection: {args.uuid}")
    else:
        print("Error: No new connection created.")
