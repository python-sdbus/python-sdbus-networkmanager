# SPDX-License-Identifier: LGPL-2.1-or-later
# This file was generated by tools/generate-settings-dataclasses-jinja.py,
# if possible, please make changes by also updating the script.
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional
from .base import NetworkManagerSettingsMixin


@dataclass
class OvsBridgeSettings(NetworkManagerSettingsMixin):
    """OvsBridge Link Settings"""

    datapath_type: Optional[str] = field(
        metadata={
            'dbus_name': 'datapath-type',
            'dbus_type': 's',
        },
        default=None,
    )
    """The data path type. One of "system", "netdev" or empty."""
    fail_mode: Optional[str] = field(
        metadata={
            'dbus_name': 'fail-mode',
            'dbus_type': 's',
        },
        default=None,
    )
    """The bridge failure mode. One of "secure", "standalone" or empty."""
    mcast_snooping_enable: Optional[bool] = field(
        metadata={
            'dbus_name': 'mcast-snooping-enable',
            'dbus_type': 'b',
        },
        default=None,
    )
    """Enable or disable multicast snooping."""
    rstp_enable: Optional[bool] = field(
        metadata={
            'dbus_name': 'rstp-enable',
            'dbus_type': 'b',
        },
        default=None,
    )
    """Enable or disable RSTP."""
    stp_enable: Optional[bool] = field(
        metadata={
            'dbus_name': 'stp-enable',
            'dbus_type': 'b',
        },
        default=None,
    )
    """Enable or disable STP."""
