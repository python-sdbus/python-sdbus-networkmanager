# SPDX-License-Identifier: LGPL-2.1-or-later
# This file was generated by tools/generate-settings-dataclasses-jinja.py,
# if possible, please make changes by also updating the script.
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional
from .base import NetworkManagerSettingsMixin


@dataclass
class HostnameSettings(NetworkManagerSettingsMixin):
    """Hostname settings"""

    from_dhcp: Optional[int] = field(
        metadata={
            'dbus_name': 'from-dhcp',
            'dbus_type': 'i',
        },
        default=None,
    )
    """Whether the system hostname can be determined from DHCP on this
    connection.

    When set to NM_TERNARY_DEFAULT (-1), the value from global
    configuration is used. If the property doesn't have a value in the
    global configuration, NetworkManager assumes the value to be
    NM_TERNARY_TRUE (1)."""
    from_dns_lookup: Optional[int] = field(
        metadata={
            'dbus_name': 'from-dns-lookup',
            'dbus_type': 'i',
        },
        default=None,
    )
    """Whether the system hostname can be determined from reverse DNS lookup of
    addresses on this device.

    When set to NM_TERNARY_DEFAULT (-1), the value from global
    configuration is used. If the property doesn't have a value in the
    global configuration, NetworkManager assumes the value to be
    NM_TERNARY_TRUE (1)."""
    only_from_default: Optional[int] = field(
        metadata={
            'dbus_name': 'only-from-default',
            'dbus_type': 'i',
        },
        default=None,
    )
    """If set to NM_TERNARY_TRUE (1), NetworkManager attempts to get the
    hostname via DHCPv4/DHCPv6 or reverse DNS lookup on this device only
    when the device has the default route for the given address family
    (IPv4/IPv6).

    If set to NM_TERNARY_FALSE (0), the hostname can be set from this
    device even if it doesn't have the default route.

    When set to NM_TERNARY_DEFAULT (-1), the value from global
    configuration is used. If the property doesn't have a value in the
    global configuration, NetworkManager assumes the value to be
    NM_TERNARY_FALSE (0)."""
    priority: Optional[int] = field(
        metadata={
            'dbus_name': 'priority',
            'dbus_type': 'i',
        },
        default=None,
    )
    """The relative priority of this connection to determine the system
    hostname. A lower numerical value is better (higher priority).  A
    connection with higher priority is considered before connections
    with lower priority.

    If the value is zero, it can be overridden by a global value from
    NetworkManager configuration. If the property doesn't have a value
    in the global configuration, the value is assumed to be 100.

    Negative values have the special effect of excluding other
    connections with a greater numerical priority value; so in presence
    of at least one negative priority, only connections with the lowest
    priority value will be used to determine the hostname."""
