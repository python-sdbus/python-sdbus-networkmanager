#!/usr/bin/env python
# SPDX-License-Identifier: LGPL-2.1-or-later
#
# Example which lists the details of NetworkManager's connection profiles.
# This is the asyncio variant of this example using sdbus_async.networkmanager.
# The blocking variant of this example is examples/block/list-connections.py
#
# Configuration settings are described at
# https://networkmanager.dev/docs/api/latest/ref-settings.html
#
# Example output:
# | name: Wired connection 1
# | uuid: b2caabdc-98bb-3f88-8d28-d10369d6ded9
# | type: 802-3-ethernet
# |       interface-name: enx001e101f0000
# | ipv4: method: manual
# |       ipaddr: 192.168.178.34/24
# |       route-metric: 200
# | ipv6: method: disabled
import asyncio
import sdbus
from sdbus_async.networkmanager import (
    NetworkManagerSettings,
    NetworkConnectionSettings,
)
from typing import List


async def list_connection_profiles_async() -> None:
    networkmanager_settings = NetworkManagerSettings()
    connections_paths: List[str] = await networkmanager_settings.connections
    for connection_path in connections_paths:
        connection_settings = NetworkConnectionSettings(connection_path)
        settings = await connection_settings.get_settings()
        connection = settings["connection"]

        # Skip connection profiles for bridges and wireless networks
        if connection["type"][1] in ("bridge", "802-11-wireless"):
            continue

        print("-------------------------------------------------------------")
        print("name:", connection["id"][1])
        print("uuid:", connection["uuid"][1])
        print("type:", connection["type"][1])
        if "interface-name" in connection:
            print("      interface-name:", connection["interface-name"][1])

        if "ipv4" in settings:
            ipv4 = settings["ipv4"]
            print("ipv4: method:", ipv4["method"][1])
            if "address-data" in ipv4:
                for a in ipv4["address-data"][1]:
                    print(f'      ipaddr: {a["address"][1]}/{a["prefix"][1]}')
            if "route-metric" in ipv4:
                print(f'      route-metric: {ipv4["route-metric"][1]}')

        if "ipv6" in settings:
            print("ipv6: method:", settings["ipv6"]["method"][1])


if __name__ == "__main__":
    sdbus.set_default_bus(sdbus.sd_bus_open_system())
    asyncio.run(list_connection_profiles_async())
