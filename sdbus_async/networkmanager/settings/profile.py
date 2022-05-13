from __future__ import annotations

from dataclasses import dataclass, field, fields
from typing import Any, Dict, Optional

from .base import NetworkManagerSettingsMixin
from .bridge import BridgeSettings
from .ethernet import EthernetSettings
from .connection import ConnectionSettings
from .ipv4 import Ipv4Settings
from .ipv6 import Ipv6Settings
from .proxy import ProxySettings
from .vpn import VpnSettings
from .wireless import WirelessSettings
from .wireless_security import WirelessSecuritySettings
from .wireguard import WireguardSettings
from ..types import NetworkManagerConnectionProperties


@dataclass
class ConnectionProfile:
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
    bridge: Optional[BridgeSettings] = field(
        metadata={'dbus_name': 'bridge',
                  'settings_class': BridgeSettings},
        default=None,
    )
    ethernet: Optional[EthernetSettings] = field(
        metadata={'dbus_name': '802-3-ethernet',
                  'settings_class': EthernetSettings},
        default=None,
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
    proxy: Optional[ProxySettings] = field(
        metadata={'dbus_name': 'proxy',
                  'settings_class': ProxySettings},
        default=None,
    )
    vpn: Optional[VpnSettings] = field(
        metadata={'dbus_name': 'vpn',
                  'settings_class': VpnSettings},
        default=None,
    )
    wifi: Optional[WirelessSettings] = field(
        metadata={'dbus_name': '802-11-wireless',
                  'settings_class': WirelessSettings},
        default=None,
    )
    wifi_security: Optional[WirelessSecuritySettings] = field(
        metadata={'dbus_name': '802-11-wireless-security',
                  'settings_class': WirelessSecuritySettings},
        default=None,
    )
    wireguard: Optional[WireguardSettings] = field(
        metadata={'dbus_name': 'wireguard',
                  'settings_class': WireguardSettings},
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
                  ) -> ConnectionProfile:
        for domain in ("ipv4", "ipv6"):
            group = dbus_dict.get(domain, None)
            if group:
                for key in ("addresses", "routes"):
                    group.pop(key, None)
        try:
            unvarianted_options: Dict[str, Any] = {
                SETTING_DBUS_NAME_TO_NAME[k]: SETTING_TO_CLASS[k].from_dbus(v)
                for k, v in dbus_dict.items()}
        except KeyError as e:
            print(dbus_dict)
            raise e
        return cls(**unvarianted_options)


SETTING_DBUS_NAME_TO_NAME: Dict[str, str] = {
    f.metadata['dbus_name']: f.name
    for f in fields(ConnectionProfile)
}

SETTING_TO_CLASS: Dict[str, NetworkManagerSettingsMixin] = {
    f.metadata['dbus_name']: f.metadata['settings_class']
    for f in fields(ConnectionProfile)
}
