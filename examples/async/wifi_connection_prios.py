#!/usr/bin/env python
# SPDX-License-Identifier: LGPL-2.1-or-later
import asyncio
import sdbus
from metadict import MetaDict  # type: ignore
from sdbus_async.networkmanager import (
    NetworkManager,
    NetworkDeviceGeneric,
    DeviceType,
)

# from nmsettings_namespace import nmsettings
from sdbus_async.networkmanager import (
    NetworkManagerSettings,
    NetworkConnectionSettings,
)
from typing import Any, Dict, List, Optional, Tuple


class NmMetaDict(MetaDict[str, Any]):  # type: ignore
    def __init__(
        self, *args: Any, nested_assignment: bool = True, **kwargs: Any
    ) -> None:
        """Override to make the default of "nested_assignment" to be True"""
        super().__init__(*args, nested_assignment=nested_assignment, **kwargs)

    def item_name_for_attr(self, attr: str) -> str:
        """Maps _ to - and removes leading _ for items with starting digits"""
        if attr.startswith("__"):
            return attr
        if attr[0] == "_":
            attr = attr[1:]
        return attr.replace("_", "-")

    @staticmethod
    def uint(integer: int) -> Tuple[str, int]:
        """Method for assigning an unsigned integer to a field"""
        return ("u", integer)

    def __setattr__(self, attr: str, val: Any) -> None:
        """Override to create tuples for standard types(string, int, ...) """
        item_name = self.item_name_for_attr(attr)
        if type(val) == str:
            val = ("s", val)
        elif type(val) == int:
            val = ("i", val)
        # TODO: List (for ipv4.addressdata), ...
        super().__setattr__(item_name, val)

    def __getattr__(self, attr: str) -> Any:
        """Override to extract the 2nd value of tuples (1st is a signature)"""
        item_name = self.item_name_for_attr(attr)
        value = super().__getattr__(item_name)
        if type(value) == tuple:
            return value[1]
        return value


async def last_connection_by_ifname(ifname: str, type: str) -> Optional[str]:
    """Return the last autoconnect connection for the given ifname and type"""
    connection_settings_manager = NetworkManagerSettings()
    connection_paths: List[str] = await connection_settings_manager.connections
    conns = {}
    prios: Dict[int, Dict[int, NmMetaDict]] = {}
    for connection_path in connection_paths:
        connection_service = NetworkConnectionSettings(connection_path)
        settings = NmMetaDict(await connection_service.get_settings())
        connection = settings.connection

        # Only connections with matching type and where autoconnect isn't False
        if connection.type != type or connection.autoconnect is False:
            continue

        # Only connections without interface-name or where it matches:
        if connection.interface_name and connection.interface_name != ifname:
            continue

        # Update the dict of timestamps from the last use of the connection
        conns[connection.timestamp] = connection.id

        # Update the dict of autoconnect-priorities and last-use timestamps
        if connection.autoconnect_priority not in prios:
            prios[connection.autoconnect_priority] = {}
        prios[connection.autoconnect_priority][connection.timestamp] = settings

    # This table is just for visual information for now
    print("Table of connections by autoconnect-priority and timestamp")
    print("columns: autoconnect-priority, timestamp, ID")
    print("---------------------")
    # reconnection_prio: List[Tuple[int, str]] = []
    # From each sorted autoconnect-priorty, extend sorted by the timestamp
    for prio in sorted(prios.items(), reverse=True):
        for key, item in prio[1].items():
            print(prio[0], key, item.connection.id)
        # reconnection_prio.extend(iter(sorted(prio[1].items(), reverse=True)))

    # Return just the current or most-recently used connection
    return conns.get(max(conns.keys()))


async def wifi_interface() -> Optional[str]:
    """Print the list of activated network devices similar to nmcli device"""
    nm = NetworkManager()
    devices_paths = await nm.get_devices()

    for device_path in devices_paths:
        generic = NetworkDeviceGeneric(device_path)
        if DeviceType(await generic.device_type) == DeviceType.WIFI:
            return await generic.interface
    return None


async def analyze_wifi_connections() -> None:
    ifname = await wifi_interface()
    if not ifname:
        print("No WiFi interface found")
    else:
        ret = await last_connection_by_ifname(ifname, "802-11-wireless")
        print("Current or most recently used WiFi connection:", ret)


if __name__ == "__main__":
    sdbus.set_default_bus(sdbus.sd_bus_open_system())
    asyncio.run(analyze_wifi_connections())
