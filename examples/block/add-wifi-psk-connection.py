#!/usr/bin/env python
# SPDX-License-Identifier: LGPL-2.1-or-later
#
# Example to create a new WiFi-PSK network connection profile:
#
# $ add-wifi-psk-connection.py --help
# usage: add-wifi-psk-connection.py [-h] [-c CONN_ID] [-s SSID] [-p PSK]
#                                   [-i INTERFACE_NAME] [-a] [--save]
#
# Optional arguments have example values:
#
# optional arguments:
#   -h, --help         show this help message and exit
#   -c CONN_ID         Connection Id
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

import functools
import pprint
import sdbus
import uuid
from argparse import ArgumentParser, Namespace
from sdbus_block.networkmanager import NetworkManagerSettings
from sdbus_block.networkmanager import NetworkManagerConnectionProperties


def add_wifi_psk_connection_profile(args: Namespace) -> None:
    """Add a temporary (not yet saved) network connection profile"""

    # If we add many connections passing the same id, things get messy. Check:
    if NetworkManagerSettings().get_connections_by_id(args.conn_id):
        print(f'Connection "{args.conn_id}" exists, remove it first')
        print(f'Run: nmcli connection delete "{args.conn_id}"')
        return

    properties: NetworkManagerConnectionProperties = {
        "connection": {
            "id": ("s", args.conn_id),
            "uuid": ("s", str(uuid.uuid4())),
            "type": ("s", "802-11-wireless"),
            "autoconnect": ("b", args.auto),
        },
        "802-11-wireless": {
            "mode": ("s", "infrastructure"),
            "security": ("s", "802-11-wireless-security"),
            "ssid": ("ay", args.ssid.encode("utf-8")),
        },
        "802-11-wireless-security": {
            "key-mgmt": ("s", "wpa-psk"),
            "auth-alg": ("s", "open"),
            "psk": ("s", args.psk),
        },
        "ipv4": {"method": ("s", "auto")},
        "ipv6": {"method": ("s", "auto")},
    }

    # To bind the new connection to a specific interface, use this:
    if args.interface_name:
        properties["connection"]["interface-name"] = ("s", args.interface_name)

    if args.save:
        NetworkManagerSettings().add_connection(properties)
        print("New connection profile created and saved, show it with:")
    else:
        NetworkManagerSettings().add_connection_unsaved(properties)
        print("New unsaved connection profile created, show it with:")

    print(f'nmcli connection show "{args.conn_id}"|grep -v -e -- -e default')
    print("Settings used:")
    functools.partial(pprint.pprint, sort_dicts=False)(properties)


if __name__ == "__main__":
    p = ArgumentParser(description="Optional arguments have example values:")
    conn_id = "MyConnectionExample"
    p.add_argument("-c", dest="conn_id", default=conn_id, help="Connection Id")
    p.add_argument("-s", dest="ssid", default="CafeSSID", help="WiFi SSID")
    p.add_argument("-p", dest="psk", default="Coffee!!", help="WiFi PSK")
    p.add_argument("-i", dest="interface_name", default="", help="WiFi device")
    p.add_argument("-a", dest="auto", action="store_true", help="autoconnect")
    p.add_argument("--save", dest="save", action="store_true", help="Save")
    args = p.parse_args()
    sdbus.set_default_bus(sdbus.sd_bus_open_system())
    add_wifi_psk_connection_profile(args)
