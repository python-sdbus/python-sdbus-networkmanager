#!/usr/bin/env python3
# SPDX-License-Identifier: LGPL-2.1-or-later
# Copyright (C) 2025 igo95862
#
# Example of listening to device state change signals.
# Also shows the use of enums.
from __future__ import annotations

import asyncio
from argparse import ArgumentParser

import sdbus

from sdbus_async.networkmanager import NetworkDeviceGeneric, NetworkManager
from sdbus_async.networkmanager.enums import DeviceState, DeviceStateReason


async def listen_device(device_path: str, device_name: str) -> None:
    generic_device = NetworkDeviceGeneric(device_path)
    print(f"Listening state changes for device {device_name!r}")

    async for (
        new_state,
        old_state,
        reason,
    ) in generic_device.state_changed.catch():
        print(
            f"Now {DeviceState(new_state).name}, "
            f"was {DeviceState(old_state).name}, "
            f"reason {DeviceStateReason(reason).name}"
        )


async def main() -> None:
    arg_parser = ArgumentParser()
    arg_parser.add_argument("device_name")

    args = arg_parser.parse_args()

    network_manager = NetworkManager()

    device_name = args.device_name
    device_path = await network_manager.get_device_by_ip_iface(device_name)

    # If you use create_task() make sure to keep a reference to the
    # task or it will get garbage collected.
    await listen_device(device_path, device_name)


if __name__ == "__main__":
    sdbus.set_default_bus(sdbus.sd_bus_open_system())
    asyncio.run(main())
