# SPDX-License-Identifier: LGPL-2.1-or-later
# This file was generated by tools/generate-settings-dataclasses.py,
# if possible, please make changes by also updating the script.
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional
from .base import NetworkManagerSettingsMixin


@dataclass
class OvsPortSettings(NetworkManagerSettingsMixin):
    """OvsPort Link Settings"""

    bond_downdelay: Optional[int] = field(
        metadata={'dbus_name': 'bond-downdelay', 'dbus_type': 'u'},
        default=None,
    )
    bond_mode: Optional[str] = field(
        metadata={'dbus_name': 'bond-mode', 'dbus_type': 's'},
        default=None,
    )
    bond_updelay: Optional[int] = field(
        metadata={'dbus_name': 'bond-updelay', 'dbus_type': 'u'},
        default=None,
    )
    lacp: Optional[str] = field(
        metadata={'dbus_name': 'lacp', 'dbus_type': 's'},
        default=None,
    )
    tag: Optional[int] = field(
        metadata={'dbus_name': 'tag', 'dbus_type': 'u'},
        default=None,
    )
    vlan_mode: Optional[str] = field(
        metadata={'dbus_name': 'vlan-mode', 'dbus_type': 's'},
        default=None,
    )
    """The VLAN mode. One of "access", "native-tagged", "native-untagged", "trunk"
    or unset."""
