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
    ConnectionType,
    NetworkConnectionSettings,
    NetworkManager,
    NetworkManagerSettings,
    NetworkDeviceGeneric,
    IPv4Config,
    DeviceType,
    NetworkDeviceWireless,
    WiFiOperationMode,
    AccessPoint,
)
from typing import Any, Dict, List, Optional, Tuple
NetworkManagerAddressData = List[Dict[str, Tuple[str, Any]]]


def get_most_recent_connection_id(ifname: str, dev_type: str) -> Optional[str]:
    """Return the most-recently used connection_id for this device

    Besides getting the currently active connection, this will succeed
    in getting the most recent connection when a device is not connected
    at the moment this function is executed.

    It uses getattr(ConnectionType, dev_type) to get the connection_type
    used for connection_profiles for this DeviceType.

    With a slight modification, this could return the most recent connections
    of the given device, ordered by the time of the last use of them.
    """
    settings_service = NetworkManagerSettings()
    connection_paths: List[str] = settings_service.connections
    conns = {}
    for connection_path in connection_paths:
        connection_manager = NetworkConnectionSettings(connection_path)
        connection = connection_manager.get_profile().connection
        # Filter connection profiles matching the connection type for the device:
        if connection.connection_type != getattr(ConnectionType, dev_type):
            continue
        # If the interface_name of a connection profiles is set, it must match:
        if connection.interface_name and connection.interface_name != ifname:
            continue
        # If connection.timestamp is not set, it was never active. Set it to 0:
        if not connection.timestamp:
            connection.timestamp = 0
        # Record the connection_ids of the matches, and timestamp is the key:
        conns[connection.timestamp] = connection.connection_id
    if not len(conns):
        return None
    # Returns the connection_id of the highest timestamp which was found:
    return conns.get(max(conns.keys()))


def list_networkdevice_details_blocking() -> None:

    for device_path in NetworkManager().get_devices():
        generic_device = NetworkDeviceGeneric(device_path)
        device_ip4_conf_path: str = generic_device.ip4_config
        if device_ip4_conf_path == "/":
            continue
        if not generic_device.managed:
            continue
        dev_type = DeviceType(generic_device.device_type).name
        if dev_type == DeviceType.BRIDGE.name:
            continue

        dev_name = generic_device.interface
        ip4_conf = IPv4Config(device_ip4_conf_path)
        gateway: str = ip4_conf.gateway

        print("Type:   ", dev_type.title())
        print("Name:   ", dev_name)

        if gateway:
            print("Gateway:", gateway)

        address_data: NetworkManagerAddressData = ip4_conf.address_data
        for inetaddr in address_data:
            print(f'Address: {inetaddr["address"][1]}/{inetaddr["prefix"][1]}')

        nameservers: NetworkManagerAddressData = ip4_conf.nameserver_data
        for dns in nameservers:
            print("DNS:    ", dns["address"][1])

        if dev_type == DeviceType.WIFI.name:
            wifi = NetworkDeviceWireless(device_path)
            print("Wifi:   ", WiFiOperationMode(wifi.mode).name.title())
            ap = AccessPoint(wifi.active_access_point)
            ssid: bytes = ap.ssid
            if ssid:
                print("SSID:   ", ssid.decode("utf-8", "ignore"))
            if ap.strength:
                print("Signal: ", ap.strength)
        connection_id = get_most_recent_connection_id(dev_name, dev_type)
        if connection_id:
            print("Profile:", connection_id)

        print("")


if __name__ == "__main__":
    sdbus.set_default_bus(sdbus.sd_bus_open_system())
    list_networkdevice_details_blocking()
