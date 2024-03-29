# SPDX-License-Identifier: LGPL-2.1-or-later
# This file was generated by tools/generate-settings-dataclasses-jinja.py,
# if possible, please make changes by also updating the script.
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, Optional
from .base import NetworkManagerSettingsMixin


@dataclass
class OvsExternalIdsSettings(NetworkManagerSettingsMixin):
    """OVS External IDs Settings"""

    data: Optional[Dict[str, str]] = field(
        metadata={
            'dbus_name': 'data',
            'dbus_type': 'a{ss}',
        },
        default=None,
    )
    """A dictionary of key/value pairs with exernal-ids for OVS."""
