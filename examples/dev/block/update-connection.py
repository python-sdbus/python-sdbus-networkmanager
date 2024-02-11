#!/usr/bin/env python
# SPDX-License-Identifier: LGPL-2.1-or-later
#
# Update a property of a connection profile, looked up by connection id
#
# The IPv4 settings of connections profiles are documented here:
# https://networkmanager.dev/docs/api/latest/settings-ipv4.html
#

import sdbus
from functools import partial
from sdbus_block.networkmanager import NetworkManagerSettings
from sdbus_block.networkmanager import NetworkConnectionSettings
from pprint import pprint
from typing import Any, Dict


def update_connection(args: Dict[str, Any]) -> None:
    """Update the settings for [key][entry] of the 1st matching connection"""
    con = NetworkManagerSettings().get_connections_by_id(args["connection_id"])
    settings_domain, setting = args["connection_setting"]
    if con:
        connection_settings = NetworkConnectionSettings(con[0])
        properties = connection_settings.get_settings()
        # For compatibility with old tools, NM adds and prefers them, delete:
        properties["ipv4"].pop("addresses")  # -> Use ["ipv4"]["address-data"]
        properties["ipv4"].pop("routes")  # ----> Use ["ipv4"]["route-data"]

        # Update the setting's value in the given configuration group:
        properties[settings_domain][setting] = args["value"]
        connection_settings.update(properties)

        print(f'Updated {properties["connection"]["uuid"]}.{settings_domain}:')
        partial(pprint, sort_dicts=False)(properties[settings_domain])
    else:
        print(f"No connection matching {id}")


if __name__ == "__main__":
    sdbus.set_default_bus(sdbus.sd_bus_open_system())
    args = {
        # Set MyConnectionExample.ipv4.dns-search to "domain1.com,domain2.com":
        "connection_id": "MyConnectionExample",
        "connection_setting": ("ipv4", "dns-search"),
        # "as" is the so-called DBus signature, it means "array of strings":
        "value": ("as", ["domain1.com", "domain2.com"]),
    }
    update_connection(args)
