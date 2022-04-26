# SPDX-License-Identifier: LGPL-2.1-or-later

# Copyright (C) 2022 igo95862

# This file is part of python-sdbus

# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301 USA
from __future__ import annotations

from dataclasses import dataclass, field, fields
from functools import lru_cache
from typing import Any, Dict, List, Optional, Type, cast

from .types import (
    NetworkManagerConnectionProperties,
    NetworkManagerSettingsDomain,
)

# See https://networkmanager.dev/docs/api/latest/nm-settings-dbus.html
# for list of all settings


class NetworkManagerSettingsMixin:
    def to_dict(self) -> Dict[str, Dict[str, Any]]:
        """Return a simple dict (without signatures) of this settings domain"""
        new_dict = {}
        for x in fields(self):
            value = getattr(self, x.name)
            if value in [x.default, {}, []]:
                continue
            if x.metadata['dbus_type'] == 'aa{sv}':
                value = [x.to_dict() for x in value]
            new_dict[x.metadata['dbus_name']] = value
        return new_dict

    def to_dbus(self) -> NetworkManagerSettingsDomain:
        """Return a dbus dict of this settings domain for NetworkManager"""
        new_dict: NetworkManagerSettingsDomain = {}

        for x in fields(self):
            value = getattr(self, x.name)
            # get_settings() doesn't return settings using the default and we
            if value in [x.default, {}, []]:  # also don't return empty fields
                continue
            if x.metadata['dbus_type'] == 'aa{sv}':
                packed_variant = ('aa{sv}', [x.to_dbus() for x in value])
            else:
                packed_variant = (x.metadata['dbus_type'], value)

            new_dict[x.metadata['dbus_name']] = packed_variant

        return new_dict

    @classmethod
    def _unpack_variant(cls, key: str, signature: str, value: Any) -> Any:
        if signature == 'aa{sv}':
            inner_class = cls.setting_name_to_inner_class(key)
            return [inner_class.from_dbus(x) for x in value]

        return value

    @classmethod
    def from_dbus(cls,
                  dbus_dict: NetworkManagerSettingsDomain,
                  ) -> NetworkManagerSettingsMixin:

        reverse_mapping = cls.setting_name_reverse_mapping()
        unvarianted_options = {
            reverse_mapping[k]: cls._unpack_variant(k, *v)
            for k, v in dbus_dict.items()}

        # Don't import {ipv4,ipv6}.{addresses,routes}, they are deprecated,
        # and for old clients, NM prefers them if they exist:
        for key in "addresses", "routes":  # TODO: Maybe use field metadata
            if key in unvarianted_options:
                unvarianted_options.pop(key)

        return cls(**unvarianted_options)

    @classmethod
    def from_dict(cls,
                  plain_dict: Dict[str, Any]
                  ) -> NetworkManagerSettingsMixin:
        options = {}
        for dataclass_field in fields(cls):
            dbus_name = dataclass_field.metadata["dbus_name"]
            if dbus_name in plain_dict:
                value = plain_dict[dbus_name]
                if dataclass_field.metadata["dbus_type"] == 'aa{sv}':
                    inner_class = cls.setting_name_to_inner_class(dbus_name)
                    value = [inner_class.from_dict(item) for item in value]
                options[dataclass_field.name] = value
        return cls(**options)

    @classmethod
    @lru_cache(maxsize=None)
    def setting_name_reverse_mapping(cls) -> Dict[str, str]:
        return {f.metadata['dbus_name']: f.name for f in fields(cls)}

    @classmethod
    @lru_cache(maxsize=None)
    def setting_name_to_inner_class(cls, setting_name: str) -> Type[Any]:
        for x in fields(cls):
            if setting_name != x.metadata['dbus_name']:
                continue

            return cast(Type[Any], x.metadata['dbus_inner_class'])

        raise ValueError('Inner class not found')


@dataclass
class ConnectionSettings(NetworkManagerSettingsMixin):
    """General Connection Profile Settings. For full information, see
    https://networkmanager.pages.freedesktop.org/NetworkManager/NetworkManager/settings-connection.html
    """
    uuid: str = field(
        metadata={'dbus_name': 'uuid', 'dbus_type': 's'},
    )
    connection_type: str = field(
        metadata={'dbus_name': 'type', 'dbus_type': 's'},
    )
    # Optional arguments:
    auth_retries: Optional[int] = field(
        metadata={'dbus_name': 'auth-retries', 'dbus_type': 'i'},
        default=None,
    )
    autoconnect: Optional[bool] = field(
        metadata={'dbus_name': 'autoconnect', 'dbus_type': 'b'},
        default=True,
    )
    autoconnect_priority: Optional[int] = field(
        metadata={'dbus_name': 'autoconnect-priority', 'dbus_type': 'i'},
        default=None,
    )
    autoconnect_retries: Optional[int] = field(
        metadata={'dbus_name': 'autoconnect-retries', 'dbus_type': 'i'},
        default=None,
    )
    autoconnect_slaves: Optional[int] = field(
        metadata={'dbus_name': 'autoconnect-slaves', 'dbus_type': 'i'},
        default=None,
    )
    dns_over_tls: Optional[int] = field(
        metadata={'dbus_name': 'dns-over-tls', 'dbus_type': 'i'},
        default=None,
    )
    gateway_ping_timeout: Optional[int] = field(
        metadata={'dbus_name': 'gateway-ping-timeout', 'dbus_type': 'u'},
        default=None,
    )
    connection_id: Optional[str] = field(
        metadata={'dbus_name': 'id', 'dbus_type': 's'},
        default=None,
    )
    interface_name: Optional[str] = field(
        metadata={'dbus_name': 'interface-name', 'dbus_type': 's'},
        default=None,
    )
    lldp: Optional[int] = field(
        metadata={'dbus_name': 'lldp', 'dbus_type': 'i'},
        default=None,
    )
    llmnr: Optional[int] = field(
        metadata={'dbus_name': 'llmnr', 'dbus_type': 'i'},
        default=None,
    )
    master: Optional[str] = field(
        metadata={'dbus_name': 'master', 'dbus_type': 's'},
        default=None,
    )
    mdns: Optional[int] = field(
        metadata={'dbus_name': 'mdns', 'dbus_type': 'i'},
        default=None,
    )
    metered: Optional[int] = field(
        metadata={'dbus_name': 'metered', 'dbus_type': 'i'},
        default=None,
    )
    mud_url: Optional[str] = field(
        metadata={'dbus_name': 'mud-url', 'dbus_type': 's'},
        default=None,
    )
    multi_connect: Optional[int] = field(
        metadata={'dbus_name': 'multi-connect', 'dbus_type': 'i'},
        default=None,
    )
    permissions: Optional[List[str]] = field(
        metadata={'dbus_name': 'permissions', 'dbus_type': 'as'},
        default=None,
    )
    read_only: Optional[bool] = field(
        metadata={'dbus_name': 'read-only', 'dbus_type': 'b'},
        default=None,
    )
    secondaries: Optional[List[str]] = field(
        metadata={'dbus_name': 'secondaries', 'dbus_type': 'as'},
        default=None,
    )
    slave_type: Optional[str] = field(
        metadata={'dbus_name': 'slave-type', 'dbus_type': 's'},
        default=None,
    )
    stable_id: Optional[str] = field(
        metadata={'dbus_name': 'stable-id', 'dbus_type': 's'},
        default=None,
    )
    timestamp: Optional[int] = field(
        metadata={'dbus_name': 'timestamp', 'dbus_type': 't'},
        default=None,
    )
    wait_device_timeout: Optional[int] = field(
        metadata={'dbus_name': 'wait-device-timeout', 'dbus_type': 'i'},
        default=None,
    )
    zone: Optional[str] = field(
        metadata={'dbus_name': 'zone', 'dbus_type': 's'},
        default=None,
    )


@dataclass
class AddressData(NetworkManagerSettingsMixin):
    address: str = field(
        metadata={'dbus_name': 'address', 'dbus_type': 's'},
    )
    prefix: int = field(
        metadata={'dbus_name': 'prefix', 'dbus_type': 'u'},
    )


@dataclass
class RouteData(NetworkManagerSettingsMixin):
    dest: str = field(
        metadata={'dbus_name': 'dest', 'dbus_type': 's'},
    )
    prefix: int = field(
        metadata={'dbus_name': 'prefix', 'dbus_type': 'u'},
    )
    next_hop: Optional[str] = field(
        metadata={'dbus_name': 'next-hop', 'dbus_type': 's'},
        default=None,
    )
    metric: Optional[int] = field(
        metadata={'dbus_name': 'metric', 'dbus_type': 'u'},
        default=None,
    )


# FIXME: Maybe different RouteData for IPv6:
NetworkManagerConnectionRoute6Data = RouteData


# FIXME: Implemented from NM's live response, not from the source. Maybe more:
@dataclass
class WireguardPeers(NetworkManagerSettingsMixin):
    public_key: str = field(
        metadata={'dbus_name': 'public-key', 'dbus_type': 's'},
    )
    endpoint: int = field(
        metadata={'dbus_name': 'endpoint', 'dbus_type': 's'},
    )
    allowed_ips: List[str] = field(
        metadata={'dbus_name': 'allowed-ips', 'dbus_type': 'as'},
    )


@dataclass
class Ipv4Settings(NetworkManagerSettingsMixin):
    """IPv4 Settings"""

    address_data: Optional[List[AddressData]] = field(
        metadata={'dbus_name': 'address-data',
                  'dbus_type': 'aa{sv}',
                  'dbus_inner_class': AddressData},
        default=None,
    )
    # Deprecated - Ignored on creation, use address-data instead:
    addresses: Optional[List[List[int]]] = field(
        metadata={'dbus_name': 'addresses', 'dbus_type': 'deprecated{aau}'},
        default=None,
    )
    dad_timeout: Optional[int] = field(
        metadata={'dbus_name': 'dad-timeout', 'dbus_type': 'i'},
        default=None,
    )
    dhcp_client_id: Optional[str] = field(
        metadata={'dbus_name': 'dhcp-client-id', 'dbus_type': 's'},
        default=None,
    )
    dhcp_fqdn: Optional[str] = field(
        metadata={'dbus_name': 'dhcp-fqdn', 'dbus_type': 's'},
        default=None,
    )
    dhcp_hostname: Optional[str] = field(
        metadata={'dbus_name': 'dhcp-hostname', 'dbus_type': 's'},
        default=None,
    )
    dhcp_hostname_flags: Optional[int] = field(
        metadata={'dbus_name': 'dhcp-hostname-flags', 'dbus_type': 'u'},
        default=None,
    )
    dhcp_iaid: Optional[str] = field(
        metadata={'dbus_name': 'dhcp-iaid', 'dbus_type': 's'},
        default=None,
    )
    dhcp_reject_servers: Optional[List[str]] = field(
        metadata={'dbus_name': 'dhcp-reject-servers', 'dbus_type': 'as'},
        default=None,
    )
    dhcp_send_hostname: Optional[bool] = field(
        metadata={'dbus_name': 'dhcp-send-hostname', 'dbus_type': 'b'},
        default=True,
    )
    dhcp_timeout: Optional[int] = field(
        metadata={'dbus_name': 'dhcp-timeout', 'dbus_type': 'i'},
        default=None,
    )
    dhcp_vendor_class_identifier: Optional[str] = field(
        metadata={'dbus_name': 'dhcp-vendor-class-identifier',
                  'dbus_type': 's'},
        default=None,
    )
    dns: Optional[List[int]] = field(
        metadata={'dbus_name': 'dns', 'dbus_type': 'au'},
        default=None,
    )
    dns_options: Optional[List[str]] = field(
        metadata={'dbus_name': 'dns-options', 'dbus_type': 'as'},
        default=None,
    )
    dns_priority: Optional[int] = field(
        metadata={'dbus_name': 'dns-priority', 'dbus_type': 'i'},
        default=None,
    )
    dns_search: Optional[List[str]] = field(
        metadata={'dbus_name': 'dns-search', 'dbus_type': 'as'},
        default=None,
    )
    gateway: Optional[str] = field(
        metadata={'dbus_name': 'gateway', 'dbus_type': 's'},
        default=None,
    )
    ignore_auto_dns: Optional[bool] = field(
        metadata={'dbus_name': 'ignore-auto-dns', 'dbus_type': 'b'},
        default=False,
    )
    ignore_auto_routes: Optional[bool] = field(
        metadata={'dbus_name': 'ignore-auto-routes', 'dbus_type': 'b'},
        default=False,
    )
    may_fail: Optional[bool] = field(
        metadata={'dbus_name': 'may-fail', 'dbus_type': 'b'},
        default=True,
    )
    method: Optional[str] = field(
        metadata={'dbus_name': 'method', 'dbus_type': 's'},
        default=None,
    )
    never_default: Optional[bool] = field(
        metadata={'dbus_name': 'never-default', 'dbus_type': 'b'},
        default=False,
    )
    required_timeout: Optional[int] = field(
        metadata={'dbus_name': 'required-timeout', 'dbus_type': 'i'},
        default=None,
    )
    route_data: Optional[List[RouteData]] = field(
        metadata={'dbus_name': 'route-data',
                  'dbus_type': 'aa{sv}',
                  'dbus_inner_class': RouteData},
        default=None,
    )
    route_metric: Optional[int] = field(
        metadata={'dbus_name': 'route-metric', 'dbus_type': 'x'},
        default=None,
    )
    route_table: Optional[int] = field(
        metadata={'dbus_name': 'route-table', 'dbus_type': 'u'},
        default=None,
    )
    # FIXME: Deprecated - Should be ignored instead, use route-data instead
    routes: Optional[List[List[int]]] = field(
        metadata={'dbus_name': 'routes', 'dbus_type': 'deprecated{aau}'},
        default=None,
    )


@dataclass
class Ipv6Settings(NetworkManagerSettingsMixin):
    """IPv6 Settings"""

    addr_gen_mode: Optional[int] = field(
        metadata={'dbus_name': 'addr-gen-mode', 'dbus_type': 'i'},
        default=1
    )
    # FIXME: Maybe different AddressData for IPv6:
    address_data: Optional[List[AddressData]] = field(
        metadata={'dbus_name': 'address-data',
                  'dbus_type': 'aa{sv}',
                  'dbus_inner_class': AddressData},
        default=None,
    )
    # Deprecated - Ignored on creation, use address-data instead:
    addresses: Optional[List[List[int]]] = field(
        metadata={'dbus_name': 'addresses', 'dbus_type': 'deprecated{ayuay}'},
        default=None,
    )
    dad_timeout: Optional[int] = field(
        metadata={'dbus_name': 'dad-timeout', 'dbus_type': 'i'},
        default=None,
    )
    dhcp_duid: Optional[str] = field(
        metadata={'dbus_name': 'dhcp-duid', 'dbus_type': 's'},
        default=None
    )
    dhcp_hostname: Optional[str] = field(
        metadata={'dbus_name': 'dhcp-hostname', 'dbus_type': 's'},
        default=None
    )
    dhcp_hostname_flags: Optional[int] = field(
        metadata={'dbus_name': 'dhcp-hostname-flags', 'dbus_type': 'u'},
        default=None,
    )
    dhcp_iaid: Optional[str] = field(
        metadata={'dbus_name': 'dhcp-iaid', 'dbus_type': 's'},
        default=None
    )
    dhcp_reject_servers: Optional[List[str]] = field(
        metadata={'dbus_name': 'dhcp-reject-servers', 'dbus_type': 'as'},
        default=None
    )
    dhcp_send_hostname: Optional[bool] = field(
        metadata={'dbus_name': 'dhcp-send-hostname', 'dbus_type': 'b'},
        default=True
    )
    dhcp_timeout: Optional[int] = field(
        metadata={'dbus_name': 'dhcp-timeout', 'dbus_type': 'i'},
        default=None,
    )
    dns: Optional[List[bytes]] = field(
        metadata={'dbus_name': 'dns', 'dbus_type': 'aay'},
        default=None
    )
    """Array of IP addresses of DNS servers (as network-byte-order integers)"""

    dns_options: Optional[List[str]] = field(
        metadata={'dbus_name': 'dns-options', 'dbus_type': 'as'},
        default=None
    )
    dns_priority: Optional[int] = field(
        metadata={'dbus_name': 'dns-priority', 'dbus_type': 'i'},
        default=None,
    )
    dns_search: Optional[List[str]] = field(
        metadata={'dbus_name': 'dns-search', 'dbus_type': 'as'},
        default=None
    )
    gateway: Optional[str] = field(
        metadata={'dbus_name': 'gateway', 'dbus_type': 's'},
        default=None
    )
    ignore_auto_dns: Optional[bool] = field(
        metadata={'dbus_name': 'ignore-auto-dns', 'dbus_type': 'b'},
        default=False
    )
    ignore_auto_routes: Optional[bool] = field(
        metadata={'dbus_name': 'ignore-auto-routes', 'dbus_type': 'b'},
        default=False
    )
    # enum NMSettingIP6ConfigPrivacy (int32):
    ip6_privacy: Optional[int] = field(
        metadata={'dbus_name': 'ip6-privacy', 'dbus_type': 'i'},
        default=True
    )
    may_fail: Optional[bool] = field(
        metadata={'dbus_name': 'may-fail', 'dbus_type': 'b'},
        default=True
    )
    method: Optional[str] = field(
        metadata={'dbus_name': 'method', 'dbus_type': 's'},
        default=None
    )
    never_default: Optional[bool] = field(
        metadata={'dbus_name': 'never-default', 'dbus_type': 'b'},
        default=False
    )
    ra_timeout: Optional[int] = field(
        metadata={'dbus_name': 'ra-timeout', 'dbus_type': 'i'},
        default=None,
    )
    required_timeout: Optional[int] = field(
        metadata={'dbus_name': 'required-timeout', 'dbus_type': 'i'},
        default=None,
    )
    route_data: Optional[List[NetworkManagerConnectionRoute6Data]] = field(
        metadata={'dbus_name': 'route-data',
                  'dbus_type': 'aa{sv}',
                  'dbus_inner_class': NetworkManagerConnectionRoute6Data},
        default=None,
    )
    route_metric: Optional[int] = field(
        metadata={'dbus_name': 'route-metric', 'dbus_type': 'x'},
        default=None,
    )
    route_table: Optional[int] = field(
        metadata={'dbus_name': 'route-table', 'dbus_type': 'u'},
        default=None,
    )
    # Deprecated - Ignored on creation, use route-data instead:
    routes: Optional[List[List[int]]] = field(
        metadata={'dbus_name': 'routes', 'dbus_type': 'deprecated{ayuay}'},
        default=None,
    )
    token: Optional[str] = field(
        metadata={'dbus_name': 'token', 'dbus_type': 's'},
        default=None
    )


@dataclass
class WifiSettings(NetworkManagerSettingsMixin):
    ap_isolation: Optional[int] = field(
        metadata={'dbus_name': 'ap-isolation', 'dbus_type': 'i'},
        default=None,
    )
    assigned_mac_address: Optional[str] = field(
        metadata={'dbus_name': 'assigned-mac-address', 'dbus_type': 's'},
        default=None,
    )
    band: Optional[str] = field(
        metadata={'dbus_name': 'band', 'dbus_type': 's'},
        default=None,
    )
    bssid: Optional[bytes] = field(
        metadata={'dbus_name': 'bssid', 'dbus_type': 'ay'},
        default=None,
    )
    channel: Optional[int] = field(
        metadata={'dbus_name': 'channel', 'dbus_type': 'u'},
        default=None,
    )
    cloned_mac_address: Optional[bytes] = field(
        metadata={'dbus_name': 'cloned-mac-address', 'dbus_type': 'ay'},
        default=None,
    )
    generate_mac_address_mask: Optional[str] = field(
        metadata={'dbus_name': 'generate-mac-address-mask',
                  'dbus_type': 's'},
        default=None,
    )
    hidden: Optional[bool] = field(
        metadata={'dbus_name': 'hidden', 'dbus_type': 'b'},
        default=None,
    )
    mac_address: Optional[bytes] = field(
        metadata={'dbus_name': 'mac-address', 'dbus_type': 'ay'},
        default=None,
    )
    mac_address_blacklist: Optional[List[str]] = field(
        metadata={'dbus_name': 'mac-address-blacklist',
                  'dbus_type': 'as'},
        default=None,
    )
    mac_address_randomization: Optional[int] = field(
        metadata={'dbus_name': 'mac-address-randomization',
                  'dbus_type': 'u'},
        default=None,
    )
    mode: Optional[str] = field(
        metadata={'dbus_name': 'mode', 'dbus_type': 's'},
        default=None,
    )
    mtu: Optional[int] = field(
        metadata={'dbus_name': 'mtu', 'dbus_type': 'u'},
        default=None,
    )
    powersave: Optional[int] = field(
        metadata={'dbus_name': 'powersave', 'dbus_type': 'u'},
        default=None,
    )
    rate: Optional[int] = field(
        metadata={'dbus_name': 'rate', 'dbus_type': 'u'},
        default=None,
    )
    security: Optional[str] = field(
        metadata={'dbus_name': 'security', 'dbus_type': 's'},
        default=None,
    )
    seen_bssids: Optional[List[str]] = field(
        metadata={'dbus_name': 'seen-bssids', 'dbus_type': 'as'},
        default=None,
    )
    ssid: Optional[bytes] = field(
        metadata={'dbus_name': 'ssid', 'dbus_type': 'ay'},
        default=None,
    )
    tx_power: Optional[int] = field(
        metadata={'dbus_name': 'tx-power', 'dbus_type': 'u'},
        default=None,
    )
    wake_on_wlan: Optional[int] = field(
        metadata={'dbus_name': 'wake-on-wlan', 'dbus_type': 'u'},
        default=None,
    )


@dataclass
class WifiSecuritySettings(NetworkManagerSettingsMixin):
    auth_alg: Optional[str] = field(
        metadata={'dbus_name': 'auth-alg', 'dbus_type': 's'},
        default=None,
    )
    fils: Optional[int] = field(
        metadata={'dbus_name': 'fils', 'dbus_type': 'i'},
        default=None,
    )
    group: Optional[List[str]] = field(
        metadata={'dbus_name': 'group', 'dbus_type': 'as'},
        default=None,
    )
    key_mgmt: Optional[str] = field(
        metadata={'dbus_name': 'key-mgmt', 'dbus_type': 's'},
        default=None,
    )
    leap_password: Optional[int] = field(
        metadata={'dbus_name': 'leap-password', 'dbus_type': 's'},
        default=None,
    )
    leap_password_flags: Optional[int] = field(
        metadata={'dbus_name': 'leap-password-flags', 'dbus_type': 'u'},
        default=None,
    )
    leap_username: Optional[str] = field(
        metadata={'dbus_name': 'leap-username', 'dbus_type': 's'},
        default=None,
    )
    pairwise: Optional[List[str]] = field(
        metadata={'dbus_name': 'pairwise', 'dbus_type': 'as'},
        default=None,
    )
    pmf: Optional[int] = field(
        metadata={'dbus_name': 'pmf', 'dbus_type': 'i'},
        default=None,
    )
    proto: Optional[List[str]] = field(
        metadata={'dbus_name': 'proto', 'dbus_type': 'as'},
        default=None,
    )
    psk: Optional[str] = field(
        metadata={'dbus_name': 'psk', 'dbus_type': 's'},
        default=None,
    )
    psk_flags: Optional[int] = field(
        metadata={'dbus_name': 'psk-flags', 'dbus_type': 'u'},
        default=None,
    )
    wep_key_flags: Optional[int] = field(
        metadata={'dbus_name': 'wep-key-flags', 'dbus_type': 'u'},
        default=None,
    )
    wep_key_type: Optional[int] = field(
        metadata={'dbus_name': 'wep-key-type', 'dbus_type': 'u'},
        default=None,
    )
    wep_key0: Optional[str] = field(
        metadata={'dbus_name': 'wep-key0', 'dbus_type': 's'},
        default=None,
    )
    wep_key1: Optional[str] = field(
        metadata={'dbus_name': 'wep-key1', 'dbus_type': 's'},
        default=None,
    )
    wep_key2: Optional[str] = field(
        metadata={'dbus_name': 'wep-key2', 'dbus_type': 's'},
        default=None,
    )
    wep_key3: Optional[str] = field(
        metadata={'dbus_name': 'wep-key3', 'dbus_type': 's'},
        default=None,
    )
    wep_tx_keyidx: Optional[int] = field(
        metadata={'dbus_name': 'wep-tx-keyidx', 'dbus_type': 'u'},
        default=None,
    )
    wps_method: Optional[int] = field(
        metadata={'dbus_name': 'wps-method', 'dbus_type': 'u'},
        default=None,
    )


@dataclass
class ProxySettings(NetworkManagerSettingsMixin):
    """WWW Proxy Settings"""

    browser_only: Optional[bool] = field(
        metadata={'dbus_name': 'browser-only', 'dbus_type': 'b'},
        default=False
    )
    """Whether the proxy configuration is for browser only."""

    method: Optional[int] = field(
        metadata={'dbus_name': 'method', 'dbus_type': 'i'},
        default=None,
    )
    """Method for proxy configuration, Default is
    NM_SETTING_PROXY_METHOD_NONE (0)
    """

    pac_script: Optional[str] = field(
        metadata={'dbus_name': 'pac-script', 'dbus_type': 's'},
        default=None
    )
    """PAC script for the connection."""

    pac_url: Optional[str] = field(
        metadata={'dbus_name': 'pac-url', 'dbus_type': 's'},
        default=None
    )
    """PAC URL for obtaining PAC file."""


@dataclass
class BridgeSettings(NetworkManagerSettingsMixin):
    """Bridging Settings"""

    ageing_time: Optional[int] = field(
        metadata={'dbus_name': 'ageing-time', 'dbus_type': 'u'},
        default=300
    )
    """The Ethernet MAC address aging time, in seconds."""

    forward_delay: Optional[int] = field(
        metadata={'dbus_name': 'forward-delay', 'dbus_type': 'u'},
        default=15
    )
    """The Spanning Tree Protocol (STP) forwarding delay, in seconds."""

    group_address: Optional[bytes] = field(
        metadata={'dbus_name': 'group-address', 'dbus_type': 'ay'},
        default=None
    )
    """If specified, The MAC address of the multicast group this bridge
    uses for STP. The address must be a link-local address in standard
    Ethernet MAC address format, ie an address of the form
    01:80:C2:00:00:0X, with X in [0, 4..F]. If not specified the default
    value is 01:80:C2:00:00:00.
    """

    group_forward_mask: Optional[int] = field(
        metadata={'dbus_name': 'group-forward-mask', 'dbus_type': 'u'},
        default=None,
    )
    """A mask of group addresses to forward. Usually, group addresses in
    the range from 01:80:C2:00:00:00 to 01:80:C2:00:00:0F are not
    forwarded according to standards. This property is a mask of 16 bits,
    each corresponding to a group address in that range that must be
    forwarded. The mask can't have bits 0, 1 or 2 set because they are
    used for STP, MAC pause frames and LACP.
    """

    hello_time: Optional[int] = field(
        metadata={'dbus_name': 'hello-time', 'dbus_type': 'u'},
        default=2
    )
    """The Spanning Tree Protocol (STP) hello time, in seconds."""

    interface_name: Optional[str] = field(
        metadata={'dbus_name': 'interface-name', 'dbus_type': 's'},
        default=None
    )
    """Deprecated in favor of connection.interface-name, but can be used
    for backward-compatibility with older daemons, to set the bridge's
    interface name.
    """

    mac_address: Optional[bytes] = field(
        metadata={'dbus_name': 'mac-address', 'dbus_type': 'ay'},
        default=None
    )
    """If specified, the MAC address of bridge. When creating a new
    bridge, this MAC address will be set. If this field is left
    unspecified, the "ethernet.cloned-mac-address" is referred instead to
    generate the initial MAC address. Note that setting "ethernet.cloned-
    mac-address" anyway overwrites the MAC address of the bridge later
    while activating the bridge. Hence, this property is deprecated.
    Deprecated: 1
    """

    max_age: Optional[int] = field(
        metadata={'dbus_name': 'max-age', 'dbus_type': 'u'},
        default=20
    )
    """The Spanning Tree Protocol (STP) maximum message age, in seconds."""

    multicast_hash_max: Optional[int] = field(
        metadata={'dbus_name': 'multicast-hash-max', 'dbus_type': 'u'},
        default=4096
    )
    """Set maximum size of multicast hash table (value must be a power of 2)"""

    multicast_last_member_count: Optional[int] = field(
        metadata={'dbus_name': 'multicast-last-member-count',
                  'dbus_type': 'u'},
        default=2
    )
    """Set the number of queries the bridge will send before stopping
    forwarding a multicast group after a "leave" message has been
    received.
    """

    multicast_last_member_interval: Optional[int] = field(
        metadata={'dbus_name': 'multicast-last-member-interval',
                  'dbus_type': 't'},
        default=100
    )
    """Set interval (in deciseconds) between queries to find remaining
    members of a group, after a "leave" message is received.
    """

    multicast_membership_interval: Optional[int] = field(
        metadata={'dbus_name': 'multicast-membership-interval',
                  'dbus_type': 't'},
        default=26000
    )
    """Set delay (in deciseconds) after which the bridge will leave a
    group, if no membership reports for this group are received.
    """

    multicast_querier: Optional[bool] = field(
        metadata={'dbus_name': 'multicast-querier', 'dbus_type': 'b'},
        default=False
    )
    """Enable or disable sending of multicast queries by the bridge. If
    not specified the option is disabled.
    """

    multicast_querier_interval: Optional[int] = field(
        metadata={'dbus_name': 'multicast-querier-interval', 'dbus_type': 't'},
        default=25500
    )
    """If no queries are seen after this delay (in deciseconds) has
    passed, the bridge will start to send its own queries.
    """

    multicast_query_interval: Optional[int] = field(
        metadata={'dbus_name': 'multicast-query-interval', 'dbus_type': 't'},
        default=12500
    )
    """Interval (in deciseconds) between queries sent by the bridge after
    the end of the startup phase.
    """

    multicast_query_response_interval: Optional[int] = field(
        metadata={'dbus_name': 'multicast-query-response-interval',
                  'dbus_type': 't'},
        default=1000
    )
    """Set the Max Response Time/Max Response Delay (in deciseconds) for
    IGMP/MLD queries sent by the bridge.
    """

    multicast_query_use_ifaddr: Optional[bool] = field(
        metadata={'dbus_name': 'multicast-query-use-ifaddr', 'dbus_type': 'b'},
        default=False
    )
    """If enabled the bridge's own IP address is used as the source
    address for IGMP queries otherwise the default of 0.0.0.0 is used.
    """

    multicast_router: Optional[str] = field(
        metadata={'dbus_name': 'multicast-router', 'dbus_type': 's'},
        default=None
    )
    """Sets bridge's multicast router. Multicast-snooping must be enabled
    for this option to work. Supported values are: 'auto', 'disabled',
    'enabled' to which kernel assigns the numbers 1, 0, and 2,
    respectively. If not specified the default value is 'auto' (1).
    """

    multicast_snooping: Optional[bool] = field(
        metadata={'dbus_name': 'multicast-snooping', 'dbus_type': 'b'},
        default=True
    )
    """Controls whether IGMP snooping is enabled for this bridge. Note
    that if snooping was automatically disabled due to hash collisions,
    the system may refuse to enable the feature until the collisions are
    resolved.
    """

    multicast_startup_query_count: Optional[int] = field(
        metadata={'dbus_name': 'multicast-startup-query-count',
                  'dbus_type': 'u'},
        default=2
    )
    """Set the number of IGMP queries to send during startup phase."""

    multicast_startup_query_interval: Optional[int] = field(
        metadata={'dbus_name': 'multicast-startup-query-interval',
                  'dbus_type': 't'},
        default=3125
    )
    """Sets the time (in deciseconds) between queries sent out at startup
    to determine membership information.
    """

    priority: Optional[int] = field(
        metadata={'dbus_name': 'priority', 'dbus_type': 'u'},
        default=32768
    )
    """Sets the Spanning Tree Protocol (STP) priority for this bridge.
    Lower values are "better"; the lowest priority bridge will be elected
    the root bridge.
    """

    stp: Optional[bool] = field(
        metadata={'dbus_name': 'stp', 'dbus_type': 'b'},
        default=True
    )
    """Controls whether Spanning Tree Protocol (STP) is enabled for this
    bridge.
    """

    vlan_default_pvid: Optional[int] = field(
        metadata={'dbus_name': 'vlan-default-pvid', 'dbus_type': 'u'},
        default=1
    )
    """The default PVID for the ports of the bridge, that is the VLAN id
    assigned to incoming untagged frames.
    """

    vlan_filtering: Optional[bool] = field(
        metadata={'dbus_name': 'vlan-filtering', 'dbus_type': 'b'},
        default=False
    )
    """Control whether VLAN filtering is enabled on the bridge."""

    vlan_protocol: Optional[str] = field(
        metadata={'dbus_name': 'vlan-protocol', 'dbus_type': 's'},
        default=None
    )
    """If specified, the protocol used for VLAN filtering. Supported
    values are: '802.1Q', '802.1ad'. If not specified the default value is
    '802.1Q'.
    """

    vlan_stats_enabled: Optional[bool] = field(
        metadata={'dbus_name': 'vlan-stats-enabled', 'dbus_type': 'b'},
        default=False
    )
    """Controls whether per-VLAN stats accounting is enabled."""

    # FIXME:
    vlans: Optional[List[AddressData]] = field(
        metadata={'dbus_name': 'vlans',
                  'dbus_type': 'aa{sv}',
                  'dbus_inner_class': AddressData},
        default=None,
    )
    """Array of bridge VLAN objects. In addition to the VLANs specified
    here, the bridge will also have the default-pvid VLAN configured  by
    the bridge.vlan-default-pvid property. In nmcli the VLAN list can be
    specified with the following syntax: $vid [pvid] [untagged] [, $vid
    [pvid] [untagged]]... where $vid is either a single id between 1 and
    4094 or a range, represented as a couple of ids separated by a dash.
    """


@dataclass
class WireguardSettings(NetworkManagerSettingsMixin):
    """WireGuard Settings"""

    fwmark: Optional[int] = field(
        metadata={'dbus_name': 'fwmark', 'dbus_type': 'u'},
        default=None,
    )
    """The use of fwmark is optional and is by default off. Setting it to
    0 disables it. Otherwise, it is a 32-bit fwmark for outgoing packets.
    Note that "ip4-auto-default-route" or "ip6-auto-default-route"
    enabled, implies to automatically choose a fwmark.
    """
    ip4_auto_default_route: Optional[int] = field(
        metadata={'dbus_name': 'ip4-auto-default-route', 'dbus_type': 'i'},
        default=None,
    )
    ip6_auto_default_route: Optional[int] = field(
        metadata={'dbus_name': 'ip6-auto-default-route', 'dbus_type': 'i'},
        default=None,
    )
    listen_port: Optional[int] = field(
        metadata={'dbus_name': 'listen-port', 'dbus_type': 'u'},
        default=None,
    )
    """The listen-port. If listen-port is not specified, the port will be
    chosen randomly when the interface comes up.
    """

    mtu: Optional[int] = field(
        metadata={'dbus_name': 'mtu', 'dbus_type': 'u'},
        default=None,
    )
    """If non-zero, only transmit packets of the specified size or
    smaller, breaking larger packets up into multiple fragments. If zero a
    default MTU is used. Note that contrary to wg-quick's MTU setting,
    this does not take into account the current routes at the time of
    activation.
    """

    peer_routes: Optional[bool] = field(
        metadata={'dbus_name': 'peer-routes', 'dbus_type': 'b'},
        default=True
    )
    """Whether to automatically add routes for the AllowedIPs ranges of
    the peers. If TRUE (the default), NetworkManager will automatically
    add routes in the routing tables according to ipv4.route-table and
    ipv6.route-table. Usually you want this automatism enabled. If FALSE,
    no such routes are added automatically. In this case, the user may
    want to configure static routes in ipv4.routes and ipv6.routes,
    respectively. Note that if the peer's AllowedIPs is "0.0.0.0/0" or
    "::/0" and the profile's ipv4.never-default or ipv6.never-default
    setting is enabled, the peer route for this peer won't be added
    automatically.
    """

    peers: Optional[List[WireguardPeers]] = field(
        metadata={'dbus_name': 'peers',
                  'dbus_type': 'aa{sv}',
                  'dbus_inner_class': WireguardPeers},
        default=None,
    )
    private_key: Optional[str] = field(
        metadata={'dbus_name': 'private-key', 'dbus_type': 's'},
        default=None
    )
    """The 256 bit private-key in base64 encoding."""

    # private-key-flags type NMSettingSecretFlags (uint32) not found


@dataclass
class VpnSettings(NetworkManagerSettingsMixin):
    """VPN Settings"""

    data: Optional[Dict[str, str]] = field(
        metadata={'dbus_name': 'data', 'dbus_type': 'a{ss}'},
        default=None
    )
    """Dictionary of key/value pairs of VPN plugin specific data.  Both
    keys and values must be strings.
    """

    persistent: Optional[bool] = field(
        metadata={'dbus_name': 'persistent', 'dbus_type': 'b'},
        default=False
    )
    """If the VPN service supports persistence, and this property is TRUE,
    the VPN will attempt to stay connected across link changes and
    outages, until explicitly disconnected.
    """

    secrets: Optional[Dict[str, str]] = field(
        metadata={'dbus_name': 'secrets', 'dbus_type': 'a{ss}'},
        default=None
    )
    """Dictionary of key/value pairs of VPN plugin specific secrets like
    passwords or private keys.  Both keys and values must be strings.
    """

    service_type: Optional[str] = field(
        metadata={'dbus_name': 'service-type', 'dbus_type': 's'},
        default=None
    )
    """D-Bus service name of the VPN plugin that this setting uses to
    connect to its network.  i.e. org.freedesktop.NetworkManager.vpnc for
    the vpnc plugin.
    """

    timeout: Optional[int] = field(
        metadata={'dbus_name': 'timeout', 'dbus_type': 'u'},
        default=None,
    )
    """Timeout for the VPN service to establish the connection. Some
    services may take quite a long time to connect. Value of 0 means a
    default timeout, which is 60 seconds (unless overridden by vpn.timeout
    in configuration file). Values greater than zero mean timeout in
    seconds.
    """

    user_name: Optional[str] = field(
        metadata={'dbus_name': 'user-name', 'dbus_type': 's'},
        default=None
    )
    """If the VPN connection requires a user name for authentication, that
    name should be provided here.  If the connection is available to more
    than one user, and the VPN requires each user to supply a different
    name, then leave this property empty.  If this property is empty,
    NetworkManager will automatically supply the username of the user
    which requested the VPN connection.
    """


@dataclass
class EthernetSettings(NetworkManagerSettingsMixin):
    """Wired Ethernet Settings"""

    # accept-all-mac-addresses type NMTernary (int32) not found
    assigned_mac_address: Optional[str] = field(
        metadata={'dbus_name': 'assigned-mac-address', 'dbus_type': 's'},
        default=None
    )
    """The new field for the cloned MAC address. It can be either a
    hardware address in ASCII representation, or one of the special values
    "preserve", "permanent", "random" or "stable". This field replaces the
    deprecated "cloned-mac-address" on D-Bus, which can only contain
    explicit hardware addresses. Note that this property only exists in
    D-Bus API. libnm and nmcli continue to call this property "cloned-mac-
    address".
    """

    auto_negotiate: Optional[bool] = field(
        metadata={'dbus_name': 'auto-negotiate', 'dbus_type': 'b'},
        default=False  # Note: auto-negotiate is always sent by nm
    )
    """When TRUE, enforce auto-negotiation of speed and duplex mode. If
    "speed" and "duplex" properties are both specified, only that single
    mode will be advertised and accepted during the link auto-negotiation
    process: this works only for BASE-T 802.3 specifications and is useful
    for enforcing gigabits modes, as in these cases link negotiation is
    mandatory. When FALSE, "speed" and "duplex" properties should be both
    set or link configuration will be skipped.
    """

    cloned_mac_address: Optional[bytes] = field(
        metadata={'dbus_name': 'cloned-mac-address', 'dbus_type': 'ay'},
        default=None
    )
    """This D-Bus field is deprecated in favor of "assigned-mac-address"
    which is more flexible and allows specifying special variants like
    "random". For libnm and nmcli, this field is called "cloned-mac-
    address".
    """

    duplex: Optional[str] = field(
        metadata={'dbus_name': 'duplex', 'dbus_type': 's'},
        default=None
    )
    """When a value is set, either "half" or "full", configures the device
    to use the specified duplex mode. If "auto-negotiate" is "yes" the
    specified duplex mode will be the only one advertised during link
    negotiation: this works only for BASE-T 802.3 specifications and is
    useful for enforcing gigabits modes, as in these cases link
    negotiation is mandatory. If the value is unset (the default), the
    link configuration will be either skipped (if "auto-negotiate" is
    "no", the default) or will be auto-negotiated (if "auto-negotiate" is
    "yes") and the local device will advertise all the supported duplex
    modes. Must be set together with the "speed" property if specified.
    Before specifying a duplex mode be sure your device supports it.
    """

    generate_mac_address_mask: Optional[str] = field(
        metadata={'dbus_name': 'generate-mac-address-mask', 'dbus_type': 's'},
        default=None
    )
    """With "cloned-mac-address" setting "random" or "stable", by default
    all bits of the MAC address are scrambled and a locally-administered,
    unicast MAC address is created. This property allows to specify that
    certain bits are fixed. Note that the least significant bit of the
    first MAC address will always be unset to create a unicast MAC
    address. If the property is NULL, it is eligible to be overwritten by
    a default connection setting. If the value is still NULL or an empty
    string, the default is to create a locally-administered, unicast MAC
    address. If the value contains one MAC address, this address is used
    as mask. The set bits of the mask are to be filled with the current
    MAC address of the device, while the unset bits are subject to
    randomization. Setting "FE:FF:FF:00:00:00" means to preserve the OUI
    of the current MAC address and only randomize the lower 3 bytes using
    the "random" or "stable" algorithm. If the value contains one
    additional MAC address after the mask, this address is used instead of
    the current MAC address to fill the bits that shall not be randomized.
    For example, a value of "FE:FF:FF:00:00:00 68:F7:28:00:00:00" will set
    the OUI of the MAC address to 68:F7:28, while the lower bits are
    randomized. A value of "02:00:00:00:00:00 00:00:00:00:00:00" will
    create a fully scrambled globally-administered, burned-in MAC address.
    If the value contains more than one additional MAC addresses, one of
    them is chosen randomly. For example, "02:00:00:00:00:00
    00:00:00:00:00:00 02:00:00:00:00:00" will create a fully scrambled MAC
    address, randomly locally or globally administered.
    """

    mac_address: Optional[bytes] = field(
        metadata={'dbus_name': 'mac-address', 'dbus_type': 'ay'},
        default=None
    )
    """If specified, this connection will only apply to the Ethernet
    device whose permanent MAC address matches. This property does not
    change the MAC address of the device (i.e. MAC spoofing).
    """

    mac_address_blacklist: Optional[List[str]] = field(
        metadata={'dbus_name': 'mac-address-blacklist', 'dbus_type': 'as'},
        default=None
    )
    """If specified, this connection will never apply to the Ethernet
    device whose permanent MAC address matches an address in the list.
    Each MAC address is in the standard hex-digits-and-colons notation
    (00:11:22:33:44:55).
    """

    mtu: Optional[int] = field(
        metadata={'dbus_name': 'mtu', 'dbus_type': 'u'},
        default=None,
    )
    """If non-zero, only transmit packets of the specified size or
    smaller, breaking larger packets up into multiple Ethernet frames.
    """

    port: Optional[str] = field(
        metadata={'dbus_name': 'port', 'dbus_type': 's'},
        default=None
    )
    """Specific port type to use if the device supports multiple
    attachment methods.  One of "tp" (Twisted Pair), "aui" (Attachment
    Unit Interface), "bnc" (Thin Ethernet) or "mii" (Media Independent
    Interface). If the device supports only one port type, this setting is
    ignored.
    """

    s390_nettype: Optional[str] = field(
        metadata={'dbus_name': 's390-nettype', 'dbus_type': 's'},
        default=None
    )
    """s390 network device type; one of "qeth", "lcs", or "ctc",
    representing the different types of virtual network devices available
    on s390 systems.
    """

    s390_options: Optional[Dict[str, str]] = field(
        metadata={'dbus_name': 's390-options', 'dbus_type': 'a{ss}'},
        default=None
    )
    """Dictionary of key/value pairs of s390-specific device options.
    Both keys and values must be strings.  Allowed keys include "portno",
    "layer2", "portname", "protocol", among others.  Key names must
    contain only alphanumeric characters (ie, [a-zA-Z0-9]). Currently,
    NetworkManager itself does nothing with this information. However,
    s390utils ships a udev rule which parses this information and applies
    it to the interface.
    """

    s390_subchannels: Optional[List[str]] = field(
        metadata={'dbus_name': 's390-subchannels', 'dbus_type': 'as'},
        default=None
    )
    """Identifies specific subchannels that this network device uses for
    communication with z/VM or s390 host.  Like the "mac-address" property
    for non-z/VM devices, this property can be used to ensure this
    connection only applies to the network device that uses these
    subchannels.  The list should contain exactly 3 strings, and each
    string may only be composed of hexadecimal characters and the period
    (.) character.
    """

    speed: Optional[int] = field(
        metadata={'dbus_name': 'speed', 'dbus_type': 'u'},
        default=None,
    )
    """When a value greater than 0 is set, configures the device to use
    the specified speed. If "auto-negotiate" is "yes" the specified speed
    will be the only one advertised during link negotiation: this works
    only for BASE-T 802.3 specifications and is useful for enforcing
    gigabit speeds, as in this case link negotiation is mandatory. If the
    value is unset (0, the default), the link configuration will be either
    skipped (if "auto-negotiate" is "no", the default) or will be auto-
    negotiated (if "auto-negotiate" is "yes") and the local device will
    advertise all the supported speeds. In Mbit/s, ie 100 == 100Mbit/s.
    Must be set together with the "duplex" property when non-zero. Before
    specifying a speed value be sure your device supports it.
    """

    wake_on_lan: Optional[int] = field(
        metadata={'dbus_name': 'wake-on-lan', 'dbus_type': 'u'},
        default=1
    )
    """The NMSettingWiredWakeOnLan options to enable. Not all devices
    support all options. May be any combination of
    NM_SETTING_WIRED_WAKE_ON_LAN_PHY (0x2),
    NM_SETTING_WIRED_WAKE_ON_LAN_UNICAST (0x4),
    NM_SETTING_WIRED_WAKE_ON_LAN_MULTICAST (0x8),
    NM_SETTING_WIRED_WAKE_ON_LAN_BROADCAST (0x10),
    NM_SETTING_WIRED_WAKE_ON_LAN_ARP (0x20),
    NM_SETTING_WIRED_WAKE_ON_LAN_MAGIC (0x40) or the special values
    NM_SETTING_WIRED_WAKE_ON_LAN_DEFAULT (0x1) (to use global settings)
    and NM_SETTING_WIRED_WAKE_ON_LAN_IGNORE (0x8000) (to disable
    management of Wake-on-LAN in NetworkManager).
    """

    wake_on_lan_password: Optional[str] = field(
        metadata={'dbus_name': 'wake-on-lan-password', 'dbus_type': 's'},
        default=None
    )
    """If specified, the password used with magic-packet-based Wake-on-
    LAN, represented as an Ethernet MAC address.  If NULL, no password
    will be required.
    """


@dataclass
class NetworkManngerSettings:
    """
    NetworkManager is based on a concept of connection profiles, most often
    referred to just as "connections". Connection profiles provide a network
    configuration. When NetworkManager activates a connection profile on a
    network device, the configuration will be applied and an active network
    connection will be established. Users are free to create as many
    connection profiles as they see fit. Thus they are flexible in having
    various network configurations for different networking needs:
    https://networkmanager.pages.freedesktop.org/NetworkManager/NetworkManager/nm-settings-dbus.html
    """
    connection: ConnectionSettings = field(
        metadata={'dbus_name': 'connection',
                  'settings_class': ConnectionSettings},
    )
    ipv4: Optional[Ipv4Settings] = field(
        metadata={'dbus_name': 'ipv4',
                  'settings_class': Ipv4Settings},
        default=None,
    )
    ipv6: Optional[Ipv6Settings] = field(
        metadata={'dbus_name': 'ipv6',
                  'settings_class': Ipv6Settings},
        default=None,
    )
    bridge: Optional[BridgeSettings] = field(
        metadata={'dbus_name': 'bridge',
                  'settings_class': BridgeSettings},
        default=None,
    )
    wireguard: Optional[WireguardSettings] = field(
        metadata={'dbus_name': 'wireguard',
                  'settings_class': WireguardSettings},
        default=None,
    )
    vpn: Optional[VpnSettings] = field(
        metadata={'dbus_name': 'vpn',
                  'settings_class': VpnSettings},
        default=None,
    )
    ethernet: Optional[EthernetSettings] = field(
        metadata={'dbus_name': '802-3-ethernet',
                  'settings_class': EthernetSettings},
        default=None,
    )
    wifi_settings: Optional[WifiSettings] = field(
        metadata={'dbus_name': '802-11-wireless',
                  'settings_class': WifiSettings},
        default=None,
    )
    wifi_security: Optional[WifiSecuritySettings] = field(
        metadata={'dbus_name': '802-11-wireless-security',
                  'settings_class': WifiSecuritySettings},
        default=None,
    )
    proxy: Optional[ProxySettings] = field(
        metadata={'dbus_name': 'proxy',
                  'settings_class': ProxySettings},
        default=None,
    )

    def to_dict(self) -> Dict[str, Dict[str, Any]]:
        new_dict = {}
        for x in fields(self):
            settingsdomain_dataclass = getattr(self, x.name)
            if settingsdomain_dataclass is None:
                continue
            settingsdomain_dict = settingsdomain_dataclass.to_dict()
            if settingsdomain_dict != {}:
                new_dict[x.metadata['dbus_name']] = settingsdomain_dict
        return new_dict

    def to_dbus(self) -> NetworkManagerConnectionProperties:
        new_dict: NetworkManagerConnectionProperties = {}

        for x in fields(self):
            value = getattr(self, x.name)
            if value is None:
                continue
            settingsdomain_dict = value.to_dbus()
            if settingsdomain_dict != {}:
                new_dict[x.metadata['dbus_name']] = settingsdomain_dict

        return new_dict

    @property
    def dbus_name_to_settings_class(self) -> Dict[str, str]:
        return {f.metadata['dbus_name']: f.name
                for f in fields(self)}

    @classmethod
    def from_dbus(cls, dbus_dict: NetworkManagerConnectionProperties
                  ) -> NetworkManngerSettings:
        unvarianted_options: Dict[str, Any] = {
            SETTING_DBUS_NAME_TO_NAME[k]: SETTING_NAME_TO_CLASS[k].from_dbus(v)
            for k, v in dbus_dict.items()}
        return cls(**unvarianted_options)

    @classmethod
    def from_dict(cls, plain_dict: Dict[str, Any]
                  ) -> NetworkManngerSettings:
        unvarianted_options: Dict[str, Any] = {
            SETTING_DBUS_NAME_TO_NAME[k]: SETTING_NAME_TO_CLASS[k].from_dict(v)
            for k, v in plain_dict.items()}
        return cls(**unvarianted_options)


SETTING_DBUS_NAME_TO_NAME: Dict[str, str] = {
    f.metadata['dbus_name']: f.name
    for f in fields(NetworkManngerSettings)
}

SETTING_NAME_TO_CLASS: Dict[str, NetworkManagerSettingsMixin] = {
    f.metadata['dbus_name']: f.metadata['settings_class']
    for f in fields(NetworkManngerSettings)
}
ConnectionProfile = NetworkManngerSettings


# TODO: remove
def test() -> NetworkManngerSettings:
    return NetworkManngerSettings(
        connection=ConnectionSettings(
            connection_type='802-11-wireless',
            uuid="b43278e9-3402-3e23-bb2a-7877505b98a6"
        ),
        ipv4=Ipv4Settings(
            address_data=[
                AddressData('192.168.7.7', 24)
            ]
        ),
    )


def test2() -> None:
    x = NetworkManngerSettings.from_dbus({
        "connection": {
            "id": ("s", 'test'),
            "uuid": ("s", 'test'),
            "type": ("s", "802-11-wireless"),
            "autoconnect": ('b', True),
        },
        'ipv4': {
            'address-data': ('aa{sv}', [
                    {
                        'address': ('s', '192.168.7.7'),
                        'prefix': ('u', 24)
                    }])
                }
        })
    if x.connection is not None:
        print(x.connection.connection_id)

    ipv4_settings = x.ipv4
    if ipv4_settings is not None:
        address_data = ipv4_settings.address_data
        if address_data is not None:
            for a in address_data:
                print(a)
