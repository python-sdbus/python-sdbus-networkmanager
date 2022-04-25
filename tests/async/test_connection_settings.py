#!/usr/bin/env python
# SPDX-License-Identifier: LGPL-2.1-or-later
import asyncio
import sdbus
from sdbus_async.networkmanager import (
    NetworkManagerSettings,
    NetworkConnectionSettings,
)
from typing import List


async def list_connection_profiles_async() -> None:
    settings_service = NetworkManagerSettings()
    connections_paths: List[str] = await settings_service.connections
    for con_path in connections_paths:
        connectionsettings_service = NetworkConnectionSettings(con_path)
        profile = await connectionsettings_service.connection_profile()
        connection = profile.connection
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

        # Expect that the deprecated fields addresses and routes are removed:
        settings = await connectionsettings_service.get_settings()
        for domain in ["ipv4", "ipv6"]:
            for setting in ["addresses", "routes"]:
                settings[domain].pop(setting)
        assert profile.to_dbus() == settings


def test_settings_not_changed_by_dataclasses() -> None:
    """Test the from_dbus() and to_dbus() functions of the dataclasses and
    that the type of Field(metadata.dbus_type) of the dataclass is correct.

    Note: The test data used by this test comes from the NetworkManager running
    on the system. It is good to test with real data and good for diagnosing
    issues, but it not alway be present and it cannot check all fields."""

    # TODO: Generate several tests with different fixed connection profiles.
    # Tip: They can use real connection profiles, saved in .json data files.

    sdbus.set_default_bus(sdbus.sd_bus_open_system())
    asyncio.run(list_connection_profiles_async())


if __name__ == "__main__":
    test_settings_not_changed_by_dataclasses()
