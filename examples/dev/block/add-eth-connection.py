#!/usr/bin/env python
# SPDX-License-Identifier: LGPL-2.1-or-later
#
# Example to create a new Ethernet network connection profile:
#
# examples/block/add-eth-connection.py --help
# usage: add-eth-connection.py [-h] [-c CONN_ID] [-u UUID] [-i INTERFACE_NAME]
#                              [-4 IP4] [-g GW] [-a] [--save]
#
# Optional arguments have example values:
#
# optional arguments:
#   -h, --help         show this help message and exit
#   -c CONN_ID         Connection Id
#   -u UUID            Connection UUID
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
import logging
import pprint
import sys
from uuid import uuid4
from argparse import ArgumentParser, Namespace
from sdbus_block.networkmanager import NetworkManagerSettings
from sdbus_block.networkmanager import NetworkManagerConnectionProperties


def add_ethernet_connection(args: Namespace) -> str:
    """Add a (by default) temporary (not yet saved) network connection profile
    :param Namespace args: autoconnect, conn_id, psk, save, ssid, uuid
    :return: dbus connection path of the created connection profile
    """
    info = logging.getLogger().info

    # If we add many connections using the same id, things get messy. Check:
    if NetworkManagerSettings().get_connections_by_id(args.conn_id):
        info(f'Connections using ID "{args.conn_id}" exist, remove them:')
        info(f'Run: nmcli connection delete "{args.conn_id}"')
        return ""

    ipaddr, prefix = args.ip4.split("/")
    properties: NetworkManagerConnectionProperties = {
        "connection": {
            "id": ("s", args.conn_id),
            "uuid": ("s", str(args.uuid)),
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
        properties["connection"]["interface-name"] = ("s", args.interface_name)
    if len(sys.argv) == 1 or args.gw != "192.0.2.1/4000":
        default_gateway, route_metric = args.gw.split("/")
        properties["ipv4"]["gateway"] = ("s", default_gateway)
        properties["ipv4"]["route-metric"] = ("u", int(route_metric))

    s = NetworkManagerSettings()
    addconnection = s.add_connection if args.save else s.add_connection_unsaved
    connection_settings_dbus_path = addconnection(properties)
    created = "created and saved" if args.save else "created"

    info(f"New unsaved connection profile {created}, show it with:")
    info(f'nmcli connection show "{args.conn_id}"|grep -v -e -- -e default')
    info("Settings used:")
    info(functools.partial(pprint.pformat, sort_dicts=False)(properties))
    return connection_settings_dbus_path


if __name__ == "__main__":
    logging.basicConfig(format="%(message)s", level=logging.INFO)
    p = ArgumentParser(description="Optional arguments have example values:")
    conn_id = "MyConnectionExample"
    p.add_argument("-c", dest="conn_id", default=conn_id, help="Connection Id")
    p.add_argument("-u", dest="uuid", default=uuid4(), help="Connection UUID")
    p.add_argument("-i", dest="interface_name", default="", help="ethX device")
    p.add_argument("-4", dest="ip4", default="192.0.2.8/24", help="IP4/prefix")
    p.add_argument("-g", dest="gw", default="192.0.2.1/4000", help="gw/metric")
    p.add_argument("-a", dest="auto", action="store_true", help="autoconnect")
    p.add_argument("--save", dest="save", action="store_true", help="Save")
    args = p.parse_args()
    sdbus.set_default_bus(sdbus.sd_bus_open_system())
    if connection_dpath := add_ethernet_connection(args):
        print(f"Path of the new connection: {connection_dpath}")
        print(f"UUID of the new connection: {args.uuid}")
    else:
        print("Error: No new connection created.")
