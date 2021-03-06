# SPDX-License-Identifier: LGPL-2.1-or-later

# Copyright (C) 2020, 2021 igo95862

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

from .enums import (
    AccessPointCapabilities,
    BluetoothCapabilities,
    ConnectionFlags,
    ConnectionState,
    ConnectionStateFlags,
    ConnectionStateReason,
    ConnectionType,
    ConnectivityState,
    DeviceCapabilities,
    DeviceInterfaceFlags,
    DeviceMetered,
    DeviceState,
    DeviceStateReason,
    DeviceType,
    IpTunnelMode,
    ModemCapabilities,
    NetworkManagerConnectivityState,
    NetworkManagerState,
    SecretAgentCapabilities,
    VpnFailure,
    VpnState,
    WiFiOperationMode,
    WirelessCapabilities,
    WpaSecurityFlags,
)
from .exceptions import (
    NetworkManagerAlreadyAsleepOrAwakeError,
    NetworkManagerAlreadyEnabledOrDisabledError,
    NetworkManagerBaseError,
    NetworkManagerConnectionAlreadyActiveError,
    NetworkManagerConnectionNotActiveError,
    NetworkManagerConnectionNotAvailableError,
    NetworkManagerDependencyFailedError,
    NetworkManagerFailedError,
    NetworkManagerInvalidArgumentsError,
    NetworkManagerMissingPluginError,
    NetworkManagerPermissionDeniedError,
    NetworkManagerUnknownConnectionError,
    NetworkManagerUnknownDeviceError,
    NetworkManagerUnknownLogDomainError,
    NetworkManagerUnknownLogLevelError,
    NmAgentManagerFailedError,
    NmAgentManagerInvalidIdentifierError,
    NmAgentManagerNoSecretsError,
    NmAgentManagerNotRegisteredError,
    NmAgentManagerPermissionDeniedError,
    NmAgentManagerUserCanceledError,
    NmConnectionFailedError,
    NmConnectionInvalidPropertyError,
    NmConnectionInvalidSettingError,
    NmConnectionMissingPropertyError,
    NmConnectionMissingSettingError,
    NmConnectionPropertyNotFoundError,
    NmConnectionPropertyNotSecretError,
    NmConnectionSettingNotFoundError,
    NmDeviceCreationFailedError,
    NmDeviceFailedError,
    NmDeviceIncompatibleConnectionError,
    NmDeviceInvalidArgumentError,
    NmDeviceInvalidConnectionError,
    NmDeviceMissingDependenciesError,
    NmDeviceNotActiveError,
    NmDeviceNotAllowedError,
    NmDeviceNotSoftwareError,
    NmDeviceSpecificObjectNotFoundError,
    NmDeviceVersionIdMismatchError,
    NmSecretManagerAgentCanceledError,
    NmSecretManagerFailedError,
    NmSecretManagerInvalidConnectionError,
    NmSecretManagerNoSecretsError,
    NmSecretManagerPermissionDeniedError,
    NmSecretManagerUserCanceledError,
    NmSettingsFailedError,
    NmSettingsInvalidArgumentsError,
    NmSettingsInvalidConnectionError,
    NmSettingsInvalidHostnameError,
    NmSettingsNotSupportedError,
    NmSettingsPermissionDeniedError,
    NmSettingsReadOnlyConnectionError,
    NmSettingsUuidExistsError,
    NmVpnPluginAlreadyStartedError,
    NmVpnPluginAlreadyStoppedError,
    NmVpnPluginBadArgumentsError,
    NmVpnPluginFailedError,
    NmVpnPluginInteractiveNotSupportedError,
    NmVpnPluginInvalidConnectionError,
    NmVpnPluginLaunchFailedError,
    NmVpnPluginStartingInProgressError,
    NmVpnPluginStoppingInProgressError,
    NmVpnPluginWrongStateError,
)
from .interfaces_devices import (
    NetworkManagerDeviceBluetoothInterface,
    NetworkManagerDeviceBondInterface,
    NetworkManagerDeviceBridgeInterface,
    NetworkManagerDeviceGenericInterface,
    NetworkManagerDeviceInterface,
    NetworkManagerDeviceIPTunnelInterface,
    NetworkManagerDeviceLowpanInterface,
    NetworkManagerDeviceMacsecInterface,
    NetworkManagerDeviceMacvlanInterface,
    NetworkManagerDeviceModemInterface,
    NetworkManagerDeviceOlpcMeshInterface,
    NetworkManagerDeviceOvsBridgeInterface,
    NetworkManagerDeviceOvsPortInterface,
    NetworkManagerDeviceStatisticsInterface,
    NetworkManagerDeviceTeamInterface,
    NetworkManagerDeviceTunInterface,
    NetworkManagerDeviceVethInterface,
    NetworkManagerDeviceVlanInterface,
    NetworkManagerDeviceVrfInterface,
    NetworkManagerDeviceVxlanInterface,
    NetworkManagerDeviceWifiP2PInterface,
    NetworkManagerDeviceWiredInterface,
    NetworkManagerDeviceWireGuardInterface,
    NetworkManagerDeviceWirelessInterface,
    NetworkManagerPPPInterface,
)
from .interfaces_other import (
    NetworkManagerAccessPointInterface,
    NetworkManagerCheckpointInterface,
    NetworkManagerConnectionActiveInterface,
    NetworkManagerDHCP4ConfigInterface,
    NetworkManagerDHCP6ConfigInterface,
    NetworkManagerDnsManagerInterface,
    NetworkManagerInterface,
    NetworkManagerIP4ConfigInterface,
    NetworkManagerIP6ConfigInterface,
    NetworkManagerSecretAgentInterface,
    NetworkManagerSecretAgentManagerInterface,
    NetworkManagerSettingsConnectionInterface,
    NetworkManagerSettingsInterface,
    NetworkManagerVPNConnectionInterface,
    NetworkManagerVPNPluginInterface,
    NetworkManagerWifiP2PPeerInterface,
)
from .objects import (
    AccessPoint,
    ActiveConnection,
    ActiveVPNConnection,
    ConfigCheckpoint,
    DHCPv4Config,
    DHCPv6Config,
    IPv4Config,
    IPv6Config,
    NetworkConnectionSettings,
    NetworkDeviceBluetooth,
    NetworkDeviceBond,
    NetworkDeviceBridge,
    NetworkDeviceGeneric,
    NetworkDeviceIpTunnel,
    NetworkDeviceMacsec,
    NetworkDeviceMacvlan,
    NetworkDeviceModem,
    NetworkDeviceOlpcMesh,
    NetworkDeviceOpenVSwitchBridge,
    NetworkDeviceOpenVSwitchPort,
    NetworkDevicePPP,
    NetworkDeviceTeam,
    NetworkDeviceTun,
    NetworkDeviceVeth,
    NetworkDeviceVlan,
    NetworkDeviceVrf,
    NetworkDeviceVxlan,
    NetworkDeviceWifiP2P,
    NetworkDeviceWired,
    NetworkDeviceWireGuard,
    NetworkDeviceWireless,
    NetworkManager,
    NetworkManagerAgentManager,
    NetworkManagerDnsManager,
    NetworkManagerSettings,
    WiFiP2PPeer,
)
from .settings.adsl import AdslSettings
from .settings.bluetooth import BluetoothSettings
from .settings.bond import BondSettings
from .settings.bond_port import BondPortSettings
from .settings.bridge import BridgeSettings
from .settings.bridge_port import BridgePortSettings
from .settings.cdma import CdmaSettings
from .settings.connection import ConnectionSettings
from .settings.datatypes import AddressData, RouteData, WireguardPeers
from .settings.dcb import DcbSettings
from .settings.ethernet import EthernetSettings
from .settings.gsm import GsmSettings
from .settings.hostname import HostnameSettings
from .settings.ieee802_1x import Ieee8021XSettings
from .settings.infiniband import InfinibandSettings
from .settings.ip_tunnel import IpTunnelSettings
from .settings.ipv4 import Ipv4Settings
from .settings.ipv6 import Ipv6Settings
from .settings.lowpan import LowpanSettings
from .settings.macsec import MacsecSettings
from .settings.macvlan import MacvlanSettings
from .settings.match import MatchSettings
from .settings.olpc_mesh import OlpcMeshSettings
from .settings.ovs_bridge import OvsBridgeSettings
from .settings.ovs_dpdk import OvsDpdkSettings
from .settings.ovs_external_ids import OvsExternalIdsSettings
from .settings.ovs_interface import OvsInterfaceSettings
from .settings.ovs_patch import OvsPatchSettings
from .settings.ovs_port import OvsPortSettings
from .settings.ppp import PppSettings
from .settings.pppoe import PppoeSettings
from .settings.profile import ConnectionProfile
from .settings.proxy import ProxySettings
from .settings.serial import SerialSettings
from .settings.team import TeamSettings
from .settings.team_port import TeamPortSettings
from .settings.tun import TunSettings
from .settings.user import UserSettings
from .settings.veth import VethSettings
from .settings.vlan import VlanSettings
from .settings.vpn import VpnSettings
from .settings.vrf import VrfSettings
from .settings.vxlan import VxlanSettings
from .settings.wifi_p2p import WifiP2PSettings
from .settings.wimax import WimaxSettings
from .settings.wireguard import WireguardSettings
from .settings.wireless import WirelessSettings
from .settings.wireless_security import WirelessSecuritySettings
from .settings.wpan import WpanSettings
from .types import (
    NetworkManagerConnectionProperties,
    NetworkManagerSetting,
    NetworkManagerSettingsDomain,
    SettingsDict,
)

DEVICE_TYPE_TO_CLASS = {
    DeviceType.ETHERNET: NetworkDeviceWired,
    DeviceType.WIFI: NetworkDeviceWireless,
    DeviceType.BLUETOOTH: NetworkDeviceBluetooth,
    DeviceType.OLPC_MESH: NetworkDeviceOlpcMesh,
    DeviceType.VETH: NetworkDeviceVeth,
    DeviceType.WIREGUARD: NetworkDeviceWireGuard,
    DeviceType.PPP: NetworkDevicePPP,
    DeviceType.BRIDGE: NetworkDeviceBridge,
    DeviceType.MODEM: NetworkDeviceModem,
}


__all__ = (
    # .enums
    'AccessPointCapabilities',
    'BluetoothCapabilities',
    'ConnectionFlags',
    'ConnectionState',
    'ConnectionStateFlags',
    'ConnectionStateReason',
    'ConnectionType',
    'ConnectivityState',
    'DeviceCapabilities',
    'DeviceInterfaceFlags',
    'DeviceMetered',
    'DeviceState',
    'DeviceStateReason',
    'DeviceType',
    'IpTunnelMode',
    'ModemCapabilities',
    'NetworkManagerConnectivityState',
    'NetworkManagerState',
    'SecretAgentCapabilities',
    'VpnFailure',
    'VpnState',
    'WiFiOperationMode',
    'WirelessCapabilities',
    'WpaSecurityFlags',
    # .exceptions
    'NetworkManagerAlreadyAsleepOrAwakeError',
    'NetworkManagerAlreadyEnabledOrDisabledError',
    'NetworkManagerBaseError',
    'NetworkManagerConnectionAlreadyActiveError',
    'NetworkManagerConnectionNotActiveError',
    'NetworkManagerConnectionNotAvailableError',
    'NetworkManagerDependencyFailedError',
    'NetworkManagerFailedError',
    'NetworkManagerInvalidArgumentsError',
    'NetworkManagerMissingPluginError',
    'NetworkManagerPermissionDeniedError',
    'NetworkManagerUnknownConnectionError',
    'NetworkManagerUnknownDeviceError',
    'NetworkManagerUnknownLogDomainError',
    'NetworkManagerUnknownLogLevelError',
    'NmAgentManagerFailedError',
    'NmAgentManagerInvalidIdentifierError',
    'NmAgentManagerNoSecretsError',
    'NmAgentManagerNotRegisteredError',
    'NmAgentManagerPermissionDeniedError',
    'NmAgentManagerUserCanceledError',
    'NmConnectionFailedError',
    'NmConnectionInvalidPropertyError',
    'NmConnectionInvalidSettingError',
    'NmConnectionMissingPropertyError',
    'NmConnectionMissingSettingError',
    'NmConnectionPropertyNotFoundError',
    'NmConnectionPropertyNotSecretError',
    'NmConnectionSettingNotFoundError',
    'NmDeviceCreationFailedError',
    'NmDeviceFailedError',
    'NmDeviceIncompatibleConnectionError',
    'NmDeviceInvalidArgumentError',
    'NmDeviceInvalidConnectionError',
    'NmDeviceMissingDependenciesError',
    'NmDeviceNotActiveError',
    'NmDeviceNotAllowedError',
    'NmDeviceNotSoftwareError',
    'NmDeviceSpecificObjectNotFoundError',
    'NmDeviceVersionIdMismatchError',
    'NmSecretManagerAgentCanceledError',
    'NmSecretManagerFailedError',
    'NmSecretManagerInvalidConnectionError',
    'NmSecretManagerNoSecretsError',
    'NmSecretManagerPermissionDeniedError',
    'NmSecretManagerUserCanceledError',
    'NmSettingsFailedError',
    'NmSettingsInvalidArgumentsError',
    'NmSettingsInvalidConnectionError',
    'NmSettingsInvalidHostnameError',
    'NmSettingsNotSupportedError',
    'NmSettingsPermissionDeniedError',
    'NmSettingsReadOnlyConnectionError',
    'NmSettingsUuidExistsError',
    'NmVpnPluginAlreadyStartedError',
    'NmVpnPluginAlreadyStoppedError',
    'NmVpnPluginBadArgumentsError',
    'NmVpnPluginFailedError',
    'NmVpnPluginInteractiveNotSupportedError',
    'NmVpnPluginInvalidConnectionError',
    'NmVpnPluginLaunchFailedError',
    'NmVpnPluginStartingInProgressError',
    'NmVpnPluginStoppingInProgressError',
    'NmVpnPluginWrongStateError',
    # .interfaces_devices
    'NetworkManagerDeviceBluetoothInterface',
    'NetworkManagerDeviceBondInterface',
    'NetworkManagerDeviceBridgeInterface',
    'NetworkManagerDeviceGenericInterface',
    'NetworkManagerDeviceInterface',
    'NetworkManagerDeviceIPTunnelInterface',
    'NetworkManagerDeviceLowpanInterface',
    'NetworkManagerDeviceMacsecInterface',
    'NetworkManagerDeviceMacvlanInterface',
    'NetworkManagerDeviceModemInterface',
    'NetworkManagerDeviceOlpcMeshInterface',
    'NetworkManagerDeviceOvsBridgeInterface',
    'NetworkManagerDeviceOvsPortInterface',
    'NetworkManagerDeviceStatisticsInterface',
    'NetworkManagerDeviceTeamInterface',
    'NetworkManagerDeviceTunInterface',
    'NetworkManagerDeviceVethInterface',
    'NetworkManagerDeviceVlanInterface',
    'NetworkManagerDeviceVrfInterface',
    'NetworkManagerDeviceVxlanInterface',
    'NetworkManagerDeviceWifiP2PInterface',
    'NetworkManagerDeviceWiredInterface',
    'NetworkManagerDeviceWireGuardInterface',
    'NetworkManagerDeviceWirelessInterface',
    'NetworkManagerPPPInterface',
    # .interfaces_other
    'NetworkManagerAccessPointInterface',
    'NetworkManagerCheckpointInterface',
    'NetworkManagerConnectionActiveInterface',
    'NetworkManagerDHCP4ConfigInterface',
    'NetworkManagerDHCP6ConfigInterface',
    'NetworkManagerDnsManagerInterface',
    'NetworkManagerInterface',
    'NetworkManagerIP4ConfigInterface',
    'NetworkManagerIP6ConfigInterface',
    'NetworkManagerSecretAgentInterface',
    'NetworkManagerSecretAgentManagerInterface',
    'NetworkManagerSettingsConnectionInterface',
    'NetworkManagerSettingsInterface',
    'NetworkManagerVPNConnectionInterface',
    'NetworkManagerVPNPluginInterface',
    'NetworkManagerWifiP2PPeerInterface',
    # .objects
    'AccessPoint',
    'ActiveConnection',
    'ActiveVPNConnection',
    'ConfigCheckpoint',
    'DHCPv4Config',
    'DHCPv6Config',
    'IPv4Config',
    'IPv6Config',
    'NetworkConnectionSettings',
    'NetworkDeviceBluetooth',
    'NetworkDeviceBond',
    'NetworkDeviceBridge',
    'NetworkDeviceGeneric',
    'NetworkDeviceIpTunnel',
    'NetworkDeviceMacsec',
    'NetworkDeviceMacvlan',
    'NetworkDeviceModem',
    'NetworkDeviceOlpcMesh',
    'NetworkDeviceOpenVSwitchBridge',
    'NetworkDeviceOpenVSwitchPort',
    'NetworkDevicePPP',
    'NetworkDeviceTeam',
    'NetworkDeviceTun',
    'NetworkDeviceVeth',
    'NetworkDeviceVlan',
    'NetworkDeviceVrf',
    'NetworkDeviceVxlan',
    'NetworkDeviceWifiP2P',
    'NetworkDeviceWired',
    'NetworkDeviceWireGuard',
    'NetworkDeviceWireless',
    'NetworkManager',
    'NetworkManagerAgentManager',
    'NetworkManagerDnsManager',
    'NetworkManagerSettings',
    'WiFiP2PPeer',
    # .settings
    'AdslSettings',
    'BluetoothSettings',
    'BondSettings',
    'BondPortSettings',
    'BridgeSettings',
    'BridgePortSettings',
    'CdmaSettings',
    'ConnectionSettings',
    'AddressData', 'RouteData', 'WireguardPeers',
    'DcbSettings',
    'EthernetSettings',
    'GsmSettings',
    'HostnameSettings',
    'Ieee8021XSettings',
    'InfinibandSettings',
    'IpTunnelSettings',
    'Ipv4Settings',
    'Ipv6Settings',
    'LowpanSettings',
    'MacsecSettings',
    'MacvlanSettings',
    'MatchSettings',
    'OlpcMeshSettings',
    'OvsBridgeSettings',
    'OvsDpdkSettings',
    'OvsExternalIdsSettings',
    'OvsInterfaceSettings',
    'OvsPatchSettings',
    'OvsPortSettings',
    'PppSettings',
    'PppoeSettings',
    'ConnectionProfile',
    'ProxySettings',
    'SerialSettings',
    'TeamSettings',
    'TeamPortSettings',
    'TunSettings',
    'UserSettings',
    'VethSettings',
    'VlanSettings',
    'VpnSettings',
    'VrfSettings',
    'VxlanSettings',
    'WifiP2PSettings',
    'WimaxSettings',
    'WireguardSettings',
    'WirelessSettings',
    'WirelessSecuritySettings',
    'WpanSettings',
    # .types
    'NetworkManagerConnectionProperties',
    'NetworkManagerSetting',
    'NetworkManagerSettingsDomain',
    'SettingsDict',

    'DEVICE_TYPE_TO_CLASS',
)
