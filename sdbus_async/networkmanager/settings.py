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

    def to_dbus(self) -> NetworkManagerSettingsDomain:
        new_dict: NetworkManagerSettingsDomain = {}

        for x in fields(self):
            value = getattr(self, x.name)
            if value is None:
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

        return cls(**unvarianted_options)

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
    auth_retries: Optional[int] = field(
        metadata={'dbus_name': 'auth-retries', 'dbus_type': 'i'},
        default=None,
    )
    autoconnect: Optional[bool] = field(
        metadata={'dbus_name': 'autoconnect', 'dbus_type': 'b'},
        default=None,
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
    pretty_id: Optional[str] = field(
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
        metadata={'dbus_name': 'timestamp', 'dbus_type': 'q'},
        default=None,
    )
    connection_type: Optional[str] = field(
        metadata={'dbus_name': 'type', 'dbus_type': 's'},
        default=None,
    )
    uuid: Optional[str] = field(
        metadata={'dbus_name': 'uuid', 'dbus_type': 's'},
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


@dataclass
class Ipv4Settings(NetworkManagerSettingsMixin):
    address_data: Optional[List[AddressData]] = field(
        metadata={'dbus_name': 'address-data',
                  'dbus_type': 'aa{sv}',
                  'dbus_inner_class': AddressData},
        default=None,
    )
    addresses: Optional[List[List[int]]] = field(
        metadata={'dbus_name': 'addresses', 'dbus_type': 'aau'},
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
        default=None,
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
        default=None,
    )
    ignore_auto_routes: Optional[bool] = field(
        metadata={'dbus_name': 'ignore-auto-routes', 'dbus_type': 'b'},
        default=None,
    )
    may_fail: Optional[bool] = field(
        metadata={'dbus_name': 'may-fail', 'dbus_type': 'b'},
        default=None,
    )
    method: Optional[str] = field(
        metadata={'dbus_name': 'method', 'dbus_type': 's'},
        default=None,
    )
    never_default: Optional[bool] = field(
        metadata={'dbus_name': 'never-default', 'dbus_type': 'b'},
        default=None,
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
    routes: Optional[List[List[str]]] = field(
        metadata={'dbus_name': 'routes', 'dbus_type': 'aau'},
        default=None,
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
class NetworkManngerSettings:
    connection_settings: Optional[ConnectionSettings] = field(
        metadata={'dbus_name': 'connection',
                  'settings_class': ConnectionSettings},
        default=None,
    )
    ipv4_settings: Optional[Ipv4Settings] = field(
        metadata={'dbus_name': 'ipv4',
                  'settings_class': Ipv4Settings},
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

    def to_dbus(self) -> NetworkManagerConnectionProperties:
        new_dict: NetworkManagerConnectionProperties = {}

        for x in fields(self):
            value = getattr(self, x.name)
            if value is None:
                continue

            new_dict[x.metadata['dbus_name']] = value.to_dbus()

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


SETTING_DBUS_NAME_TO_NAME: Dict[str, str] = {
    f.metadata['dbus_name']: f.name
    for f in fields(NetworkManngerSettings)
}

SETTING_NAME_TO_CLASS: Dict[str, NetworkManagerSettingsMixin] = {
    f.metadata['dbus_name']: f.metadata['settings_class']
    for f in fields(NetworkManngerSettings)
}


# TODO: remove
def test() -> NetworkManngerSettings:
    x = NetworkManngerSettings(
        connection_settings=ConnectionSettings(
            connection_type='802-11-wireless',
        ),
        ipv4_settings=Ipv4Settings(
            address_data=[
                AddressData('192.168.7.7', 24)
            ]
        ),
    )
    return x


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
    if x.connection_settings is not None:
        print(x.connection_settings.pretty_id)

    ipv4_settings = x.ipv4_settings
    if ipv4_settings is not None:
        address_data = ipv4_settings.address_data
        if address_data is not None:
            for a in address_data:
                print(a)
