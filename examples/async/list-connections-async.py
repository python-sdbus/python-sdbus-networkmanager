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
import pprint
from sdbus_async.networkmanager import (
    NetworkManagerSettings,
    NetworkConnectionSettings,
)
from typing import List


async def list_connection_profiles_async() -> None:
    settings_service = NetworkManagerSettings()
    dbus_connections_paths: List[str] = await settings_service.connections
    for dbus_connection_path in dbus_connections_paths:
        await print_connection_profile(dbus_connection_path)


async def print_connection_profile(connection_path: str) -> None:
    connectionsettings_service = NetworkConnectionSettings(connection_path)
    profile = await connectionsettings_service.connection_profile()
    connection = profile.connection
    # Skip connection profiles for bridges and wireless networks
    if connection.connection_type in ("bridge", "802-11-wireless"):
        return
    print("-------------------------------------------------------------")
    print("name:", connection.connection_id)
    print("uuid:", connection.uuid)
    print("type:", connection.connection_type)
    if connection.interface_name:
        print("      interface-name:", connection.interface_name)
    if profile.ipv4:
        print("ipv4: method:", profile.ipv4.method)
        if profile.ipv4.address_data:
            for address in profile.ipv4.address_data:
                print(f'      ipaddr: {address.address}/{address.prefix}')
        if profile.ipv4.route_metric:
            print(f'      route-metric: {profile.ipv4.route_metric}')
    if profile.ipv6:
        print("ipv6: method:", profile.ipv6.method)
    pprint.pprint(profile.to_dict())


if __name__ == "__main__":
    sdbus.set_default_bus(sdbus.sd_bus_open_system())
    asyncio.run(list_connection_profiles_async())
