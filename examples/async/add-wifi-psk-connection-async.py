#!/usr/bin/env python
# SPDX-License-Identifier: LGPL-2.1-or-later
#
# Example to create a new WiFi-PSK network connection profile:
#
# $ examples/async/add-wifi-psk-connection-async.py --help
# usage: add-wifi-psk-connection.py [-h] [-c CONN_ID] [-s SSID] [-p PSK]
#                                   [-i INTERFACE_NAME] [-a] [--save]
#
# Optional arguments have example values:
#
# optional arguments:
#   -h, --help         show this help message and exit
#   -c CONN_ID         Connection Id
#   -u UUID            Connection UUID
#   -s SSID            WiFi SSID
#   -p PSK             WiFi PSK
#   -i INTERFACE_NAME  WiFi device
#   -a                 autoconnect
#   --save             Save
#
# $ add-wifi-psk-connection.py
# New unsaved connection profile created, show it with:
# nmcli connection show "MyConnectionExample"|grep -v -e -- -e default
# Settings used:
# {'connection': {'id': ('s', 'MyConnectionExample'),
#                 'uuid': ('s', '90e3bcc8-d3a5-4725-a363-abb788fd47bf'),
#                 'type': ('s', '802-11-wireless'),
#                 'autoconnect': ('b', False)},
#  '802-11-wireless': {'mode': ('s', 'infrastructure'),
#                      'security': ('s', '802-11-wireless-security'),
#                      'ssid': ('ay', b'CafeSSID')},
#  '802-11-wireless-security': {'key-mgmt': ('s', 'wpa-psk'),
#                               'auth-alg': ('s', 'open'),
#                               'psk': ('s', 'Coffee!!')},
#  'ipv4': {'method': ('s', 'auto')},
#  'ipv6': {'method': ('s', 'auto')}}
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
import pprint
import sdbus
from uuid import uuid4
from argparse import ArgumentParser, Namespace
from sdbus_async.networkmanager import NetworkManagerSettings
from sdbus_async.networkmanager import ConnectionProfile, SettingsDict


async def add_wifi_psk_connection_async(args: Namespace) -> str:
    """Add a temporary (not yet saved) network connection profile
    :param Namespace args: autoconnect, conn_id, psk, save, ssid, uuid
    :return: dbus connection path of the created connection profile
    """
    info = logging.getLogger().info

    # If we add many connections passing the same id, things get messy. Check:
    if await NetworkManagerSettings().get_connections_by_id(args.conn_id):
        print(f'Connection "{args.conn_id}" exists, remove it first')
        print(f'Run: nmcli connection delete "{args.conn_id}"')
        return ""

    settings_dict: SettingsDict = {
        "connection": {
            "id": args.conn_id,
            "uuid": str(args.uuid),
            "type": "802-11-wireless",
            "autoconnect": bool(hasattr(args, "auto") and args.auto),
        },
        "802-11-wireless": {
            "security": "802-11-wireless-security",
            "ssid": args.ssid,  # str is automatically encoded to utf-8 bytes
        },
        "802-11-wireless-security": {"key-mgmt": "wpa-psk", "psk": args.psk},
        "ipv4": {"method": "auto"},
        "ipv6": {"method": "auto"},
    }
    profile = ConnectionProfile.from_settings_dict(settings_dict)

    # To bind the new connection to a specific interface, use this:
    if hasattr(args, "interface_name") and args.interface_name:
        profile.connection.interface_name = args.interface_name

    s = NetworkManagerSettings()
    addconnection = s.add_connection if args.save else s.add_connection_unsaved
    connection_settings_dbus_path = await addconnection(profile.to_dbus())
    created = "created and saved" if args.save else "created"
    info(f"New unsaved connection profile {created}, show it with:")
    info(f'nmcli connection show "{args.conn_id}"|grep -v -e -- -e default')
    info("Settings used:")
    info(functools.partial(pprint.pformat, sort_dicts=False)(settings_dict))
    return connection_settings_dbus_path


if __name__ == "__main__":
    logging.basicConfig(format="%(message)s", level=logging.INFO)
    p = ArgumentParser(description="Optional arguments have example values:")
    conn_id = "MyConnectionExample"
    p.add_argument("-c", dest="conn_id", default=conn_id, help="Connection Id")
    p.add_argument("-u", dest="uuid", default=uuid4(), help="Connection UUID")
    p.add_argument("-s", dest="ssid", default="CafeSSID", help="WiFi SSID")
    p.add_argument("-k", dest="key_mgmt", default="wpa-psk", help="key-mgmt")
    p.add_argument("-p", dest="psk", default="Coffee!!", help="WiFi PSK")
    p.add_argument("-i", dest="interface_name", default="", help="WiFi device")
    p.add_argument("-a", dest="auto", action="store_true", help="autoconnect")
    p.add_argument("--save", dest="save", action="store_true", help="Save")
    args = p.parse_args()
    sdbus.set_default_bus(sdbus.sd_bus_open_system())
    if connection_dpath := asyncio.run(add_wifi_psk_connection_async(args)):
        print(f"Path of the new connection: {connection_dpath}")
        print(f"UUID of the new connection: {args.uuid}")
    else:
        print("Error: No new connection created.")
