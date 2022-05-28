#!/usr/bin/env python
# SPDX-License-Identifier: LGPL-2.1-or-later
import asyncio
import contextlib
import sdbus
import pytest
from sdbus_async.networkmanager import (
    ConnectionProfile,
    NetworkConnectionSettings,
    NetworkManagerSettings as SettingsManager,
    NmSettingsInvalidConnectionError,
)

# All test coroutines will be treated as marked.


def test_wifi_wpa_psk_simple_from_dict() -> ConnectionProfile:
    """Parse connection and ipv4 settings from dbus using ConnectionProfile"""
    profile = ConnectionProfile.from_settings_dict(
        {
            "connection": {
                "id": "WirelessWpaPskConnection",
                "type": "802-11-wireless",
                "uuid": "16ea7af1-0e35-4036-831e-ced975f48510",
                "autoconnect": False,
            },
            "ipv4": {"method": "auto"},
            "ipv6": {"method": "disabled"},
            "802-11-wireless": {
                "security": "802-11-wireless-security",
                "ssid": b"CafeSSID",
            },
            "802-11-wireless-security": {"key-mgmt": "wpa-psk"},
        }
    )
    assert profile.connection.connection_id == "WirelessWpaPskConnection"
    assert profile.connection.uuid == "16ea7af1-0e35-4036-831e-ced975f48510"
    assert profile.connection.connection_type == "802-11-wireless"
    assert profile.connection.autoconnect is False
    assert profile.ipv4
    assert profile.ipv4.method == "auto"
    assert profile.ipv4.address_data is None
    assert profile.ipv6
    assert profile.ipv6.method == "disabled"
    return profile


async def delete_connection_by_uuid(nmset: SettingsManager, uuid: str) -> None:
    dpath = await nmset.get_connection_by_uuid(uuid)
    connection_settings = NetworkConnectionSettings(dpath)
    await connection_settings.delete()


# @pytest_asyncio.fixture
@pytest.mark.asyncio
async def test_add_wifi_wpa_psk_simple_from_dict() -> None:
    """Test adding a wireless WPA PSK connection profile(unsaved) from dict"""
    profile = test_wifi_wpa_psk_simple_from_dict()

    # If we add many connections passing the same id, things get messy. Check:
    sdbus.set_default_bus(sdbus.sd_bus_open_system())
    settings = SettingsManager()
    assert profile.connection.uuid
    with contextlib.suppress(NmSettingsInvalidConnectionError):
        await settings.get_connection_by_uuid(profile.connection.uuid)
        print(f"Deleting existing connection with {profile.connection.uuid}")
        await delete_connection_by_uuid(settings, profile.connection.uuid)
    await settings.add_connection_unsaved(profile.to_dbus())
    await delete_connection_by_uuid(settings, profile.connection.uuid)


if __name__ == "__main__":
    """The tests can be run by pytest (and from IDEs by running this module)"""
    test_wifi_wpa_psk_simple_from_dict()

    # Test using ConnectionProfile.from_dict() to create a ConnectionProfile
    # which can be used to add Wireless WPA PSK connection profile from dict
    # to a running NetworkManager. Requires access and permissions to access
    # a running NetworkManager. The added connection is not saved and deleted
    # immediately (and does not have autoconnect enabled):
    asyncio.run(test_add_wifi_wpa_psk_simple_from_dict())
