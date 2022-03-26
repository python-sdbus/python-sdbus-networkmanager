#!/usr/bin/env python
# SPDX-License-Identifier: LGPL-2.1-or-later
#
# Example to list the active IPv4 protocol configuration of network devices
# and the current status of WiFi adapters
#
# For IPv4 and org.freedesktop.NetworkManager.Device.Wireless see:
# https://networkmanager.dev/docs/api/latest/settings-ipv4.html
# https://networkmanager.dev/docs/api/latest/ref-dbus-devices.html
import sdbus
from sdbus_block.networkmanager import (
    NetworkManager,
    NetworkDeviceGeneric,
    IPv4Config,
    DeviceType,
    NetworkDeviceWireless,
    WiFiOperationMode,
    AccessPoint,
)


def list_networkdevice_details_blocking() -> None:
    nm = NetworkManager()
    devices_paths = nm.get_devices()

    for device_path in devices_paths:
        generic_device = NetworkDeviceGeneric(device_path)
        device_ip4_conf_path = generic_device.ip4_config
        if device_ip4_conf_path == "/":
            continue

        ip4_conf = IPv4Config(device_ip4_conf_path)

        print("Device: ", generic_device.interface)
        if ip4_conf.gateway:
            print("Gateway:", ip4_conf.gateway)

        for ip4addr in ip4_conf.address_data:
            print(f'Address: {ip4addr["address"][1]}/{ip4addr["prefix"][1]}')

        for dns in ip4_conf.nameserver_data:
            print("DNS:    ", dns["address"][1])

        if generic_device.device_type == DeviceType.WIFI:
            wifidevice = NetworkDeviceWireless(device_path)
            print("Wifi:   ", WiFiOperationMode(wifidevice.mode).name.title())
            ap = AccessPoint(wifidevice.active_access_point)
            if ap.ssid:
                print("SSID:   ", ap.ssid.decode("utf-8", "ignore"))
            if ap.strength:
                print("Signal: ", ap.strength)

        print("")


if __name__ == "__main__":
    sdbus.set_default_bus(sdbus.sd_bus_open_system())
    list_networkdevice_details_blocking()
