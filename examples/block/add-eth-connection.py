#!/usr/bin/env python
# SPDX-License-Identifier: LGPL-2.1-or-later
#
# Example to create a new Ethernet network connection profile:
#
# add-eth-connection.py --help
# usage: add-eth-connection.py [-h] [-c CONN_ID] [-i INTERFACE_NAME] [-4 IP4]
#                              [-g GW] [-a] [--save]
#
# Optional arguments have example values:
#
# optional arguments:
#   -h, --help         show this help message and exit
#   -c CONN_ID         Connection Id
#   -i INTERFACE_NAME  ethX device
#   -4 IP4             IP4/prefix
#   -g GW              gw/metric
#   -a                 autoconnect
#   --save             Save
#
# Connection Profile settings are described at:
# https://networkmanager.dev/docs/api/latest/ref-settings.html

import sdbus
import functools
import pprint
import sys
import uuid
from argparse import ArgumentParser, Namespace
from sdbus_block.networkmanager import NetworkManagerSettings
from sdbus_block.networkmanager import NetworkManagerConnectionProperties


def add_ethernet_connection_profile(args: Namespace) -> None:
    """Add a temporary (not yet saved) network connection profile"""

    # If we add many connections using the same id, things get messy. Check:
    if NetworkManagerSettings().get_connections_by_id(args.conn_id):
        print(f'Connections using ID "{args.conn_id}" exist, remove them:')
        print(f'Run: nmcli connection delete "{args.conn_id}"')
        return

    ipaddr, prefix = args.ip4.split("/")
    profile: NetworkManagerConnectionProperties = {
        "connection": {
            "id": ("s", args.conn_id),
            "uuid": ("s", str(uuid.uuid4())),
            "type": ("s", "802-3-ethernet"),
            "autoconnect": ("b", args.auto),
        },
        "ipv4": {
            "method": ("s", "manual"),
            "address-data": (
                "aa{sv}",
                [
                    {
                        "address": ("s", ipaddr),
                        "prefix": ("u", int(prefix)),
                    },
                ],
            ),
        },
        "ipv6": {"method": ("s", "disabled")},
    }
    if args.interface_name:
        profile["connection"]["interface-name"] = ("s", args.interface_name)
    if len(sys.argv) == 1 or args.gw != "192.0.2.1/4000":
        default_gateway, route_metric = args.gw.split("/")
        profile["ipv4"]["gateway"] = ("s", default_gateway)
        profile["ipv4"]["route-metric"] = ("u", int(route_metric))

    if args.save:
        NetworkManagerSettings().add_connection(profile)
        print("New connection profile created and saved, show it with:")
    else:
        NetworkManagerSettings().add_connection_unsaved(profile)
        print("New unsaved connection profile created, show it with:")

    print(f'nmcli connection show "{args.conn_id}"|grep -v -e -- -e default')
    print("Settings used:")
    functools.partial(pprint.pprint, sort_dicts=False)(profile)


if __name__ == "__main__":
    p = ArgumentParser(description="Optional arguments have example values:")
    conn_id = "MyConnectionExample"
    p.add_argument("-c", dest="conn_id", default=conn_id, help="Connection Id")
    p.add_argument("-i", dest="interface_name", default="", help="ethX device")
    p.add_argument("-4", dest="ip4", default="192.0.2.8/24", help="IP4/prefix")
    p.add_argument("-g", dest="gw", default="192.0.2.1/4000", help="gw/metric")
    p.add_argument("-a", dest="auto", action="store_true", help="autoconnect")
    p.add_argument("--save", dest="save", action="store_true", help="Save")
    args = p.parse_args()
    sdbus.set_default_bus(sdbus.sd_bus_open_system())
    add_ethernet_connection_profile(args)
