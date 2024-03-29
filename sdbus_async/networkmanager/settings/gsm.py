# SPDX-License-Identifier: LGPL-2.1-or-later
# This file was generated by tools/generate-settings-dataclasses-jinja.py,
# if possible, please make changes by also updating the script.
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional
from .base import NetworkManagerSettingsMixin


@dataclass
class GsmSettings(NetworkManagerSettingsMixin):
    """GSM-based Mobile Broadband Settings"""
    secret_fields_names = ['password', 'pin']
    secret_name = 'gsm'

    apn: Optional[str] = field(
        metadata={
            'dbus_name': 'apn',
            'dbus_type': 's',
        },
        default=None,
    )
    """The GPRS Access Point Name specifying the APN used when establishing a
    data session with the GSM-based network.  The APN often determines
    how the user will be billed for their network usage and whether the
    user has access to the Internet or just a provider-specific walled-
    garden, so it is important to use the correct APN for the user's
    mobile broadband plan. The APN may only be composed of the
    characters a-z, 0-9, ., and - per GSM 03.60 Section 14.9."""
    auto_config: Optional[bool] = field(
        metadata={
            'dbus_name': 'auto-config',
            'dbus_type': 'b',
        },
        default=None,
    )
    """When TRUE, the settings such as APN, username, or password will default
    to values that match the network the modem will register to in the
    Mobile Broadband Provider database."""
    device_id: Optional[str] = field(
        metadata={
            'dbus_name': 'device-id',
            'dbus_type': 's',
        },
        default=None,
    )
    """The device unique identifier (as given by the WWAN management service)
    which this connection applies to.  If given, the connection will
    only apply to the specified device."""
    home_only: Optional[bool] = field(
        metadata={
            'dbus_name': 'home-only',
            'dbus_type': 'b',
        },
        default=None,
    )
    """When TRUE, only connections to the home network will be allowed.
    Connections to roaming networks will not be made."""
    mtu: Optional[int] = field(
        metadata={
            'dbus_name': 'mtu',
            'dbus_type': 'u',
        },
        default=None,
    )
    """If non-zero, only transmit packets of the specified size or smaller,
    breaking larger packets up into multiple frames."""
    network_id: Optional[str] = field(
        metadata={
            'dbus_name': 'network-id',
            'dbus_type': 's',
        },
        default=None,
    )
    """The Network ID (GSM LAI format, ie MCC-MNC) to force specific network
    registration.  If the Network ID is specified, NetworkManager will
    attempt to force the device to register only on the specified
    network. This can be used to ensure that the device does not roam
    when direct roaming control of the device is not otherwise possible."""
    number: Optional[str] = field(
        metadata={
            'dbus_name': 'number',
            'dbus_type': 's',
        },
        default=None,
    )
    """Legacy setting that used to help establishing PPP data sessions for GSM-
    based modems."""
    password: Optional[str] = field(
        metadata={
            'dbus_name': 'password',
            'dbus_type': 's',
        },
        default=None,
    )
    """The password used to authenticate with the network, if required.  Many
    providers do not require a password, or accept any password.  But if
    a password is required, it is specified here."""
    password_flags: Optional[int] = field(
        metadata={
            'dbus_name': 'password-flags',
            'dbus_type': 'u',
        },
        default=None,
    )
    """Flags indicating how to handle the "password" property."""
    pin: Optional[str] = field(
        metadata={
            'dbus_name': 'pin',
            'dbus_type': 's',
        },
        default=None,
    )
    """If the SIM is locked with a PIN it must be unlocked before any other
    operations are requested.  Specify the PIN here to allow operation
    of the device."""
    pin_flags: Optional[int] = field(
        metadata={
            'dbus_name': 'pin-flags',
            'dbus_type': 'u',
        },
        default=None,
    )
    """Flags indicating how to handle the "pin" property."""
    sim_id: Optional[str] = field(
        metadata={
            'dbus_name': 'sim-id',
            'dbus_type': 's',
        },
        default=None,
    )
    """The SIM card unique identifier (as given by the WWAN management service)
    which this connection applies to.  If given, the connection will
    apply to any device also allowed by "device-id" which contains a SIM
    card matching the given identifier."""
    sim_operator_id: Optional[str] = field(
        metadata={
            'dbus_name': 'sim-operator-id',
            'dbus_type': 's',
        },
        default=None,
    )
    """A MCC/MNC string like "310260" or "21601" identifying the specific
    mobile network operator which this connection applies to.  If given,
    the connection will apply to any device also allowed by "device-id"
    and "sim-id" which contains a SIM card provisioned by the given
    operator."""
    username: Optional[str] = field(
        metadata={
            'dbus_name': 'username',
            'dbus_type': 's',
        },
        default=None,
    )
    """The username used to authenticate with the network, if required.  Many
    providers do not require a username, or accept any username.  But if
    a username is required, it is specified here."""
