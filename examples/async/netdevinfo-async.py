#!/usr/bin/env python
# SPDX-License-Identifier: LGPL-2.1-or-later
#
# Example to list the active IPv4 protocol configuration of network devices
# and the current status of WiFi adapters
#
# For IPv4 and org.freedesktop.NetworkManager.Device.Wireless see:
# https://networkmanager.dev/docs/api/latest/settings-ipv4.html
# https://networkmanager.dev/docs/api/latest/ref-dbus-devices.html
import asyncio
import sdbus
from sdbus_async.networkmanager import (
    NetworkManager,
    NetworkDeviceGeneric,
    IPv4Config,
    DeviceType,
    NetworkDeviceWireless,
    WiFiOperationMode,
    AccessPoint,
)
from typing import Any, Dict, List, Tuple
NetworkManagerAddressData = List[Dict[str, Tuple[str, Any]]]


async def list_networkdevice_details_async() -> None:
    nm = NetworkManager()
    devices_paths = await nm.get_devices()

    for device_path in devices_paths:
        generic_device = NetworkDeviceGeneric(device_path)
        device_ip4_conf_path: str = await generic_device.ip4_config
        if device_ip4_conf_path == "/":
            continue

        ip4_conf = IPv4Config(device_ip4_conf_path)
        gateway: str = await ip4_conf.gateway

        print("Device: ", await generic_device.interface)
        if gateway:
            print("Gateway:", gateway)

        address_data: NetworkManagerAddressData = await ip4_conf.address_data
        for inetaddr in address_data:
            print(f'Address: {inetaddr["address"][1]}/{inetaddr["prefix"][1]}')

        nameservers: NetworkManagerAddressData = await ip4_conf.nameserver_data
        for dns in nameservers:
            print("DNS:    ", dns["address"][1])

        if await generic_device.device_type == DeviceType.WIFI:
            wifi = NetworkDeviceWireless(device_path)
            print("Wifi:   ", WiFiOperationMode(await wifi.mode).name.title())
            ap = AccessPoint(await wifi.active_access_point)
            ssid: bytes = await ap.ssid
            if ssid:
                print("SSID:   ", ssid.decode("utf-8", "ignore"))
            if await ap.strength:
                print("Signal: ", await ap.strength)

        print("")


if __name__ == "__main__":
    sdbus.set_default_bus(sdbus.sd_bus_open_system())
    asyncio.run(list_networkdevice_details_async())
