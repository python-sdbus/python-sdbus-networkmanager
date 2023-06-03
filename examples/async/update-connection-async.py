#!/usr/bin/env python
# SPDX-License-Identifier: LGPL-2.1-or-later
#
# Update a property of a connection profile, looked up by connection id
#
# This version uses connection_manager.get_profile().to_settings_dict()
# to retrieve the connection profile from NetworkManager as a settings dict.
#
# It then updates it dynamically using the given arguments:
# The default is to set ipv4.dns-search to ["domain1.com", "domain2.com"].
#
# The dynamically updated dict is then used to update connection profile of NM.
#
# The IPv4 settings of connections profiles are documented here:
# https://networkmanager.dev/docs/api/latest/settings-ipv4.html
#
import asyncio
import sdbus
from functools import partial
from sdbus_async.networkmanager import NetworkManagerSettings
from sdbus_async.networkmanager import NetworkConnectionSettings
from sdbus_async.networkmanager.settings import ConnectionProfile
from pprint import pprint
from typing import Any, Dict


async def update_connection_async(args: Dict[str, Any]) -> None:
    """Update the settings for [key][entry] of the 1st matching connection"""

    # Get the connection path of the connection(s) with the recieved id
    fn = NetworkManagerSettings().get_connections_by_id(args["connection_id"])
    connection_paths = await fn
    if not connection_paths:
        print(f"No connection {id}, create with add-wifi-psk-connection-async")
        return

    # Get the profile settings of the first connection with given id
    connection_manager = NetworkConnectionSettings(connection_paths[0])
    existing_connection_profile = await connection_manager.get_profile()
    settings = existing_connection_profile.to_settings_dict()

    # Update the given setting's property using the given value
    setting, property = args["connection_setting"]
    settings[setting][property] = args["value"]

    # Get a new ConnectionProfile with the change incorporated
    new_connection_profile = ConnectionProfile.from_settings_dict(settings)

    # Update the new ConnectionProfile in NetworkManager's configuration
    await connection_manager.update(new_connection_profile.to_dbus())

    print(f'Updated {new_connection_profile.connection.uuid}.{setting}:')
    partial(pprint, sort_dicts=False)(settings)

    # Restore the previous connection profile:
    await connection_manager.update(existing_connection_profile.to_dbus())


if __name__ == "__main__":
    sdbus.set_default_bus(sdbus.sd_bus_open_system())
    args = {
        # Set MyConnectionExample.ipv4.dns-search to "domain1.com,domain2.com":
        "connection_id": "MyConnectionExample",
        "connection_setting": ("ipv4", "dns-search"),
        "value": ["domain1.com", "domain2.com"],
    }
    asyncio.run(update_connection_async(args))
