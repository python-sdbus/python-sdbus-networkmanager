#!/usr/bin/env python
# SPDX-License-Identifier: LGPL-2.1-or-later
from sdbus_async.networkmanager import (
    ConnectionProfile,
)


def test_connection_profile_ipv4_from_dbus() -> None:
    """Parse connection and ipv4 settings from dbus using ConnectionProfile"""
    profile = ConnectionProfile.from_dbus(
        {
            "connection": {
                "id": ("s", 'Test for the connection id'),
                "uuid": ("s", '1ba25035-970b-4c4a-bf3c-8c6cdf8ab5d0'),
                "type": ("s", "802-3-ethernet"),
                "autoconnect": ('b', True),
            },
            'ipv4': {
                'address-data': (
                    'aa{sv}',
                    [{'address': ('s', '192.0.2.1'), 'prefix': ('u', 24)}],
                )
            },
        }
    )
    assert profile.connection.connection_id == "Test for the connection id"
    assert profile.connection.uuid == "1ba25035-970b-4c4a-bf3c-8c6cdf8ab5d0"
    assert profile.connection.connection_type == "802-3-ethernet"
    assert profile.connection.autoconnect is True
    assert profile.ipv4
    assert profile.ipv4.address_data
    assert profile.ipv4.address_data[0].address == "192.0.2.1"
    assert profile.ipv4.address_data[0].prefix == 24


if __name__ == "__main__":
    """The tests can be run by pytest (and from IDEs by running this module)"""
    test_connection_profile_ipv4_from_dbus()
