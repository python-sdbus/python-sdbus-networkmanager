#!/usr/bin/env python
# SPDX-License-Identifier: LGPL-2.1-or-later
#
# Example which lists the details of NetworkManager's connection profiles.
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
import sdbus
from sdbus_block.networkmanager import (
    ConnectionType,
    NetworkManagerSettings,
    NetworkConnectionSettings,
)


def list_connection_profiles_blocking() -> None:
    """Call print_connection_profile_blocking() for all connection profiles"""
    networkmanager_settings = NetworkManagerSettings()
    for dbus_connection_path in networkmanager_settings.connections:
        print_connection_profile_blocking(dbus_connection_path)


def print_connection_profile_blocking(connection_path: str) -> None:
    """Show the use of NetworkConnectionSettings(path).get_profile()"""
    profile = NetworkConnectionSettings(connection_path).get_profile()
    print("-------------------------------------------------------------")
    print("name:", profile.connection.connection_id)
    print("uuid:", profile.connection.uuid)
    print("type:", profile.connection.connection_type)
    if profile.connection.interface_name:
        print("      interface-name:", profile.connection.interface_name)
    if profile.ipv4:
        print("ipv4: method:", profile.ipv4.method)
        if profile.ipv4.address_data:
            for address in profile.ipv4.address_data:
                print(f'      ipaddr: {address.address}/{address.prefix}')
        if profile.ipv4.route_metric:
            print(f'      route-metric: {profile.ipv4.route_metric}')
    if profile.ipv6:
        print("ipv6: method:", profile.ipv6.method)
    if profile.connection.connection_type == ConnectionType.WIFI:
        assert profile.wireless
        assert profile.wireless.ssid
        print("ssid:", profile.wireless.ssid.decode())


if __name__ == "__main__":
    sdbus.set_default_bus(sdbus.sd_bus_open_system())
    list_connection_profiles_blocking()
