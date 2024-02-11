#!/usr/bin/env python
# SPDX-License-Identifier: LGPL-2.1-or-later
#
# Create and delete a connection profile using the unique connection uuid
#
import logging
import sdbus
from uuid import uuid4
from argparse import Namespace
from sdbus_block.networkmanager import NetworkManagerSettings
from sdbus_block.networkmanager import NmSettingsInvalidConnectionError


def delete_connection_by_uuid(uuid: str) -> bool:
    """Find and delete the connection identified by the given UUID"""
    try:
        NetworkManagerSettings().delete_connection_by_uuid(uuid)
    except NmSettingsInvalidConnectionError:
        logging.getLogger().fatal(f"Connection {uuid} for deletion not found")
        return False
    return True


def create_and_delete_wifi_psk_connection_async(args: Namespace) -> bool:
    """Add a temporary (not yet saved) network connection profile
    :param Namespace args: autoconnect, conn_id, psk, save, ssid, uuid
    :return: dbus connection path of the created connection profile
    """
    add_wifi_psk_connection = __import__("add-wifi-psk-connection")
    if not add_wifi_psk_connection.add_wifi_psk_connection(args):
        return False
    return delete_connection_by_uuid(str(args.uuid))


if __name__ == "__main__":
    logging.basicConfig(format="%(message)s", level=logging.WARNING)
    sdbus.set_default_bus(sdbus.sd_bus_open_system())
    args = Namespace(conn_id="Example", uuid=uuid4(), ssid="S", psk="Password")
    if create_and_delete_wifi_psk_connection_async(args):
        print(f"Succeeded in creating and deleting connection {args.uuid}")
