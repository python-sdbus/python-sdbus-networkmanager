#!/usr/bin/env python
# SPDX-License-Identifier: LGPL-2.1-or-later
import asyncio
import sdbus
from sdbus_async.networkmanager import (
    NetworkManagerSettings,
    NetworkConnectionSettings,
    NetworkManagerConnectionProperties,
)
from typing import List


def remove_empty_settings(profile: NetworkManagerConnectionProperties) -> None:
    """Remove empty arrays and dicts from which are not needed by NM"""
    for domainsettings in profile.values():
        todelete = [
            property
            for property, value in domainsettings.items()
            if value[1] in [[], {}]
        ]
        for delete in todelete:
            domainsettings.pop(delete)
    todelete = [
        domain
        for domain, domainsettings in profile.items()
        if domainsettings == {}
    ]
    for delete in todelete:
        profile.pop(delete)


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
            for property in ["addresses", "routes"]:
                settings[domain].pop(property)
        # 802-3-ethernet.auto-negotiate defaults to False but NM returns it:
        if ethernet := settings.get("802-3-ethernet"):
            if ethernet["auto-negotiate"][1] is False:
                ethernet.pop("auto-negotiate")
        remove_empty_settings(settings)

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
