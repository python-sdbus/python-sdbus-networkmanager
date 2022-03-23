#!/usr/bin/env python
# SPDX-License-Identifier: LGPL-2.1-or-later
#
# Example to list the network devices including type, state, internet
# connectivitycheck state and the identifier of the active connection.
#
# NetworkDeviceGeneric/org.freedesktop.NetworkManager.Device is described at
# https://networkmanager.dev/docs/api/latest/ref-dbus-devices.html
#
# The output resembles the output of the NM CLI command "nmcli device":
#
# Interface         Type     State        Internet Connection
# lo                Generic  Unmanaged    Unknown
# wlp0s20f3         Wifi     Activated    Full     Wolke7 [primary connection]
# docker0           Bridge   Activated    None     docker0
# enx0c3796090408   Ethernet Activated    Full     enx0c3796090408
# p2p-dev-wlp0s20f3 Wifi_P2P Disconnected None

import argparse
import asyncio
import sdbus
from sdbus_async.networkmanager import (
    NetworkManager,
    NetworkDeviceGeneric,
    DeviceState,
    DeviceType,
    DeviceCapabilities as Capabilities,
    ActiveConnection,
    ConnectivityState,
)
from enum import Enum


def title(enum: Enum) -> str:
    """Get the name of an enum: 1st character is uppercase, rest lowercase"""
    return enum.name.title()


async def list_active_hardware_networkdevice_states(only_hw: bool) -> None:
    """Print the list of activated network devices similar to nmcli device"""
    nm = NetworkManager()
    devices_paths = await nm.get_devices()

    print("Interface         Type     State        Internet Connection")
    for device_path in devices_paths:
        generic = NetworkDeviceGeneric(device_path)

        # Demonstrates an enum to match devices using capabilities:
        if only_hw and await generic.capabilities & Capabilities.IS_SOFTWARE:
            continue

        # Create the strings for the columns using the names of the enums:
        dev: str = await generic.interface
        type = title(DeviceType(await generic.device_type))
        state = title(DeviceState(await generic.state))
        connectivity = title(ConnectivityState(await generic.ip4_connectivity))

        if await generic.active_connection == "/":  # No active connection
            id = ""
        else:
            # ActiveConnection() gets propertites from active connection path:
            active_conn = ActiveConnection(await generic.active_connection)
            id: str = await active_conn.id
            if await active_conn.default:
                id += " [primary connection]"

        print(f"{dev:<17} {type:<8} {state:<12} {connectivity:<8} {id:<14}")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--hw", action="store_true", dest="only_hw", help="Only HW")
    args = p.parse_args()
    sdbus.set_default_bus(sdbus.sd_bus_open_system())
    asyncio.run(list_active_hardware_networkdevice_states(args.only_hw))
