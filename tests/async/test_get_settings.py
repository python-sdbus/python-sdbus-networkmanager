#!/usr/bin/env python
# SPDX-License-Identifier: LGPL-2.1-or-later
import asyncio
import unittest
import pytest
import sdbus
from sdbus_async.networkmanager import (
    ConnectionProfile,
    NetworkManagerSettings as SettingsManager,
    NetworkManagerConnectionProperties as ConnectionProfileDict,
)


def profile_with_autoconnect_set_to(autoconnect: bool) -> ConnectionProfile:
    dummy_profile: ConnectionProfileDict = {
        "connection": {
            "id": ("s", 'DummyConnection'),
            "uuid": ("s", '16ea7af1-0e35-4036-831e-ced975f48510'),
            "type": ("s", "dummy"),
            "autoconnect": ("b", autoconnect),
            "interface-name": ("s", "dummy-notused0"),
        },
    }
    profile_from_dbus_dict = ConnectionProfile.from_dbus(dummy_profile)
    # Assert that ConnectionProfile.from_dbus parsed autoconnect correctly:
    assert profile_from_dbus_dict.connection.autoconnect is autoconnect
    return profile_from_dbus_dict


def set_sdbus_default_bus() -> None:
    sdbus.set_default_bus(sdbus.sd_bus_open_system())


async def get_settings_by_networkmanager(
    profile: ConnectionProfileDict,
) -> ConnectionProfileDict:
    """Add a connection and return the settings of NetworkManager
    Uses the helper method get_gettings_by_uuid() which uses get_settings()

    Requires access and permissions to access a running NetworkManager.
    The added (dummy) connection is not saved and deleted immediately"""
    manager = SettingsManager()

    # Temporarily add the new Wifi connection to NetworkManager:
    await manager.add_connection_unsaved(profile)

    # Get the settings of the temporary connection from NetworkManager:
    uuid = profile["connection"]["uuid"][1]
    connection_profile_dict = await manager.get_settings_by_uuid(uuid)

    # Remove the temporay connection (now that we have read its settings):
    await manager.delete_connection_by_uuid(uuid)
    return connection_profile_dict


@pytest.mark.asyncio
async def test_autoconnect_false_returned_by_networkmanager() -> None:
    """Test get_settings_by_uuid() and check that autoconnect = False is set"""
    set_sdbus_default_bus()

    # Set autoconnect = ("b", False) and expect it to be returned by NM:
    profile_test = profile_with_autoconnect_set_to(autoconnect=False).to_dbus()
    profile_from_manager = await get_settings_by_networkmanager(profile_test)
    # Assert that NetworkManager did return autoconnect=False (default is True)
    unittest.TestCase().assertTupleEqual(
        profile_from_manager["connection"]["autoconnect"], ("b", False)
    )


@pytest.mark.asyncio
async def test_autoconnect_true_not_returned_by_networkmanager() -> None:
    """Check autoconnect=True (is default) is not returned by get_settings()"""
    set_sdbus_default_bus()

    # Set autoconnect = ("b", True) and expect to not be returned by NM:
    # (NetworkManager does not return a property if it has the default value)
    profile_test = profile_with_autoconnect_set_to(autoconnect=True).to_dbus()
    unittest.TestCase().assertTupleEqual(
        profile_test["connection"]["autoconnect"], ("b", True)
    )
    # Assert that NetworkManager did not return autoconnect (default is True)
    profile_from_manager = await get_settings_by_networkmanager(profile_test)
    assert "autoconnect" not in profile_from_manager["connection"]


def test_autoconnect_true_returned_by_settings_dict_when_requested() -> None:
    """to_settings_dict(defaults=True) returns autoconnect=True (is default)"""
    profile_from_dbus_dict = profile_with_autoconnect_set_to(True)
    settings_dict = profile_from_dbus_dict.to_settings_dict(defaults=True)
    assert settings_dict["connection"]["autoconnect"] is True


def test_autoconnect_true_not_returned_by_to_settings_dict() -> None:
    """to_settings_dict(defaults=False) does not return autoconnect=True"""

    # Like checked by test_autoconnect_true_not_returned_by_networkmanager()
    # above (which checks that get_settings) does not return autoconnect=True
    # (because it is the default), test the same for .to_settings_dict():
    profile_from_dbus_dict = profile_with_autoconnect_set_to(True)
    settings_dict = profile_from_dbus_dict.to_settings_dict(defaults=False)

    # Assert that networkmanager did not return autoconnect (default is True)
    assert "autoconnect" not in settings_dict["connection"]


async def check_to_settings_dict_profile_eqal_to_from_settings_dict() -> None:
    """Async main function to run all tests when not run by pytest"""
    """The tests can be run by pytest (and from IDEs by running this module)"""
    set_sdbus_default_bus()
    await test_autoconnect_false_returned_by_networkmanager()
    await test_autoconnect_true_not_returned_by_networkmanager()
    test_autoconnect_true_returned_by_settings_dict_when_requested()
    test_autoconnect_true_not_returned_by_to_settings_dict()


if __name__ == "__main__":
    """Main function to run all tests when not run by pytest"""
    asyncio.run(check_to_settings_dict_profile_eqal_to_from_settings_dict())
