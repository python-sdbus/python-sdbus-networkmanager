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
from .interfaces_devices import (
    NetworkManagerDeviceBluetoothInterfaceAsync,
    NetworkManagerDeviceBondInterfaceAsync,
    NetworkManagerDeviceBridgeInterfaceAsync,
    NetworkManagerDeviceGenericInterfaceAsync,
    NetworkManagerDeviceInterfaceAsync,
    NetworkManagerDeviceIPTunnelInterfaceAsync,
    NetworkManagerDeviceLowpanInterfaceAsync,
    NetworkManagerDeviceMacsecInterfaceAsync,
    NetworkManagerDeviceMacvlanInterfaceAsync,
    NetworkManagerDeviceModemInterfaceAsync,
    NetworkManagerDeviceOlpcMeshInterfaceAsync,
    NetworkManagerDeviceOvsBridgeInterfaceAsync,
    NetworkManagerDeviceOvsPortInterfaceAsync,
    NetworkManagerDeviceStatisticsInterfaceAsync,
    NetworkManagerDeviceTeamInterfaceAsync,
    NetworkManagerDeviceTunInterfaceAsync,
    NetworkManagerDeviceVethInterfaceAsync,
    NetworkManagerDeviceVlanInterfaceAsync,
    NetworkManagerDeviceVrfInterfaceAsync,
    NetworkManagerDeviceVxlanInterfaceAsync,
    NetworkManagerDeviceWifiP2PInterfaceAsync,
    NetworkManagerDeviceWiredInterfaceAsync,
    NetworkManagerDeviceWireGuardInterfaceAsync,
    NetworkManagerDeviceWirelessInterfaceAsync,
    NetworkManagerPPPInterfaceAsync,
)
from .interfaces_other import (
    NetworkManagerAccessPointInterfaceAsync,
    NetworkManagerCheckpointInterfaceAsync,
    NetworkManagerConnectionActiveInterfaceAsync,
    NetworkManagerDHCP4ConfigInterfaceAsync,
    NetworkManagerDHCP6ConfigInterfaceAsync,
    NetworkManagerDnsManagerInterfaceAsync,
    NetworkManagerInterfaceAsync,
    NetworkManagerIP4ConfigInterfaceAsync,
    NetworkManagerIP6ConfigInterfaceAsync,
    NetworkManagerSecretAgentInterfaceAsync,
    NetworkManagerSecretAgentManagerInterfaceAsync,
    NetworkManagerSettingsConnectionInterfaceAsync,
    NetworkManagerSettingsInterfaceAsync,
    NetworkManagerVPNConnectionInterfaceAsync,
    NetworkManagerVPNPluginInterfaceAsync,
    NetworkManagerWifiP2PPeerInterfaceAsync,
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
from .exceptions import (
    NetworkManagerBaseError,
    NmAgentManagerFailedError,
    NmAgentManagerPermissionDeniedError,
    NmAgentManagerInvalidIdentifierError,
    NmAgentManagerNotRegisteredError,
    NmAgentManagerNoSecretsError,
    NmAgentManagerUserCanceledError,
    NmConnectionFailedError,
    NmConnectionSettingNotFoundError,
    NmConnectionPropertyNotFoundError,
    NmConnectionPropertyNotSecretError,
    NmConnectionMissingSettingError,
    NmConnectionInvalidSettingError,
    NmConnectionMissingPropertyError,
    NmConnectionInvalidPropertyError,
    NmDeviceFailedError,
    NmDeviceCreationFailedError,
    NmDeviceInvalidConnectionError,
    NmDeviceIncompatibleConnectionError,
    NmDeviceNotActiveError,
    NmDeviceNotSoftwareError,
    NmDeviceNotAllowedError,
    NmDeviceSpecificObjectNotFoundError,
    NmDeviceVersionIdMismatchError,
    NmDeviceMissingDependenciesError,
    NmDeviceInvalidArgumentError,
    NetworkManagerFailedError,
    NetworkManagerPermissionDeniedError,
    NetworkManagerUnknownConnectionError,
    NetworkManagerUnknownDeviceError,
    NetworkManagerConnectionNotAvailableError,
    NetworkManagerConnectionNotActiveError,
    NetworkManagerConnectionAlreadyActiveError,
    NetworkManagerDependencyFailedError,
    NetworkManagerAlreadyAsleepOrAwakeError,
    NetworkManagerAlreadyEnabledOrDisabledError,
    NetworkManagerUnknownLogLevelError,
    NetworkManagerUnknownLogDomainError,
    NetworkManagerInvalidArgumentsError,
    NetworkManagerMissingPluginError,
    NmSecretManagerFailedError,
    NmSecretManagerPermissionDeniedError,
    NmSecretManagerInvalidConnectionError,
    NmSecretManagerUserCanceledError,
    NmSecretManagerAgentCanceledError,
    NmSecretManagerNoSecretsError,
    NmSettingsFailedError,
    NmSettingsPermissionDeniedError,
    NmSettingsNotSupportedError,
    NmSettingsInvalidConnectionError,
    NmSettingsReadOnlyConnectionError,
    NmSettingsUuidExistsError,
    NmSettingsInvalidHostnameError,
    NmSettingsInvalidArgumentsError,
    NmVpnPluginFailedError,
    NmVpnPluginStartingInProgressError,
    NmVpnPluginAlreadyStartedError,
    NmVpnPluginStoppingInProgressError,
    NmVpnPluginAlreadyStoppedError,
    NmVpnPluginWrongStateError,
    NmVpnPluginBadArgumentsError,
    NmVpnPluginLaunchFailedError,
    NmVpnPluginInvalidConnectionError,
    NmVpnPluginInteractiveNotSupportedError,
)
from .settings.connection import ConnectionSettings
from .settings.profile import ConnectionProfile
from .settings.ipv4 import Ipv4Settings
from .settings.ipv6 import Ipv6Settings
from .settings.adsl import AdslSettings
from .settings.bluetooth import BluetoothSettings
from .settings.bond import BondSettings
from .settings.bond_port import BondPortSettings
from .settings.bridge import BridgeSettings
from .settings.bridge_port import BridgePortSettings
from .settings.cdma import CdmaSettings
from .settings.dcb import DcbSettings
from .settings.ethernet import EthernetSettings
from .settings.gsm import GsmSettings
from .settings.hostname import HostnameSettings
from .settings.ieee802_1x import Ieee8021XSettings
from .settings.infiniband import InfinibandSettings
from .settings.ip_tunnel import IpTunnelSettings
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
from .settings.datatypes import (
    AddressData,
    RouteData,
    WireguardPeers,
)
from .types import (
    NetworkManagerSetting,
    NetworkManagerSettingsDomain,
    NetworkManagerConnectionProperties,
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
    'AccessPointCapabilities', 'BluetoothCapabilities',
    'ConnectionFlags', 'ConnectionState', 'ConnectionStateFlags',
    'ConnectionStateReason', 'ConnectivityState',
    'DeviceCapabilities', 'DeviceInterfaceFlags', 'DeviceMetered',
    'DeviceState', 'DeviceStateReason', 'DeviceType', 'IpTunnelMode',
    'ModemCapabilities', 'NetworkManagerConnectivityState',
    'NetworkManagerState', 'SecretAgentCapabilities', 'VpnFailure',
    'VpnState', 'WiFiOperationMode', 'WirelessCapabilities',
    'WpaSecurityFlags',

    'NetworkManagerDeviceBluetoothInterfaceAsync',
    'NetworkManagerDeviceBondInterfaceAsync',
    'NetworkManagerDeviceBridgeInterfaceAsync',
    'NetworkManagerDeviceGenericInterfaceAsync',
    'NetworkManagerDeviceInterfaceAsync',
    'NetworkManagerDeviceIPTunnelInterfaceAsync',
    'NetworkManagerDeviceLowpanInterfaceAsync',
    'NetworkManagerDeviceMacsecInterfaceAsync',
    'NetworkManagerDeviceMacvlanInterfaceAsync',
    'NetworkManagerDeviceModemInterfaceAsync',
    'NetworkManagerDeviceOlpcMeshInterfaceAsync',
    'NetworkManagerDeviceOvsBridgeInterfaceAsync',
    'NetworkManagerDeviceOvsPortInterfaceAsync',
    'NetworkManagerDeviceStatisticsInterfaceAsync',
    'NetworkManagerDeviceTeamInterfaceAsync',
    'NetworkManagerDeviceTunInterfaceAsync',
    'NetworkManagerDeviceVethInterfaceAsync',
    'NetworkManagerDeviceVlanInterfaceAsync',
    'NetworkManagerDeviceVrfInterfaceAsync',
    'NetworkManagerDeviceVxlanInterfaceAsync',
    'NetworkManagerDeviceWifiP2PInterfaceAsync',
    'NetworkManagerDeviceWiredInterfaceAsync',
    'NetworkManagerDeviceWireGuardInterfaceAsync',
    'NetworkManagerDeviceWirelessInterfaceAsync',
    'NetworkManagerPPPInterfaceAsync',

    'NetworkManagerAccessPointInterfaceAsync',
    'NetworkManagerCheckpointInterfaceAsync',
    'NetworkManagerConnectionActiveInterfaceAsync',
    'NetworkManagerDHCP4ConfigInterfaceAsync',
    'NetworkManagerDHCP6ConfigInterfaceAsync',
    'NetworkManagerDnsManagerInterfaceAsync',
    'NetworkManagerInterfaceAsync',
    'NetworkManagerIP4ConfigInterfaceAsync',
    'NetworkManagerIP6ConfigInterfaceAsync',
    'NetworkManagerSecretAgentInterfaceAsync',
    'NetworkManagerSecretAgentManagerInterfaceAsync',
    'NetworkManagerSettingsConnectionInterfaceAsync',
    'NetworkManagerSettingsInterfaceAsync',
    'NetworkManagerVPNConnectionInterfaceAsync',
    'NetworkManagerVPNPluginInterfaceAsync',
    'NetworkManagerWifiP2PPeerInterfaceAsync',

    'NetworkManager',
    'NetworkManagerAgentManager',
    'NetworkManagerDnsManager',
    'NetworkManagerSettings',
    'NetworkConnectionSettings',
    'NetworkDeviceGeneric',
    'NetworkDeviceWired',
    'NetworkDeviceWireless',
    'NetworkDeviceBluetooth',
    'NetworkDeviceBond',
    'NetworkDeviceBridge',
    'NetworkDeviceIpTunnel',
    'NetworkDeviceMacsec',
    'NetworkDeviceMacvlan',
    'NetworkDeviceModem',
    'NetworkDeviceOlpcMesh',
    'NetworkDeviceOpenVSwitchBridge',
    'NetworkDeviceOpenVSwitchPort',
    'NetworkDeviceTeam',
    'NetworkDeviceTun',
    'NetworkDeviceVeth',
    'NetworkDeviceVlan',
    'NetworkDeviceVrf',
    'NetworkDeviceVxlan',
    'NetworkDeviceWifiP2P',
    'NetworkDeviceWireGuard',
    'NetworkDevicePPP',
    'ActiveConnection',
    'ActiveVPNConnection',
    'IPv4Config',
    'IPv6Config',
    'DHCPv4Config',
    'DHCPv6Config',
    'AccessPoint',
    'WiFiP2PPeer',
    'ConfigCheckpoint',

    'ConnectionProfile',
    'ConnectionSettings',
    'AdslSettings',
    'BluetoothSettings',
    'BondPortSettings',
    'BondSettings',
    'BridgePortSettings',
    'BridgeSettings',
    'CdmaSettings',
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
    'ProxySettings',
    'SerialSettings',
    'TeamPortSettings',
    'TeamSettings',
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
    'WirelessSecuritySettings',
    'WirelessSettings',
    'WpanSettings',

    'AddressData',
    'RouteData',
    'WireguardPeers',

    'DEVICE_TYPE_TO_CLASS',

    'NetworkManagerBaseError',
    'NmAgentManagerFailedError',
    'NmAgentManagerPermissionDeniedError',
    'NmAgentManagerInvalidIdentifierError',
    'NmAgentManagerNotRegisteredError',
    'NmAgentManagerNoSecretsError',
    'NmAgentManagerUserCanceledError',
    'NmConnectionFailedError',
    'NmConnectionSettingNotFoundError',
    'NmConnectionPropertyNotFoundError',
    'NmConnectionPropertyNotSecretError',
    'NmConnectionMissingSettingError',
    'NmConnectionInvalidSettingError',
    'NmConnectionMissingPropertyError',
    'NmConnectionInvalidPropertyError',
    'NmDeviceFailedError',
    'NmDeviceCreationFailedError',
    'NmDeviceInvalidConnectionError',
    'NmDeviceIncompatibleConnectionError',
    'NmDeviceNotActiveError',
    'NmDeviceNotSoftwareError',
    'NmDeviceNotAllowedError',
    'NmDeviceSpecificObjectNotFoundError',
    'NmDeviceVersionIdMismatchError',
    'NmDeviceMissingDependenciesError',
    'NmDeviceInvalidArgumentError',
    'NetworkManagerFailedError',
    'NetworkManagerPermissionDeniedError',
    'NetworkManagerUnknownConnectionError',
    'NetworkManagerUnknownDeviceError',
    'NetworkManagerConnectionNotAvailableError',
    'NetworkManagerConnectionNotActiveError',
    'NetworkManagerConnectionAlreadyActiveError',
    'NetworkManagerDependencyFailedError',
    'NetworkManagerAlreadyAsleepOrAwakeError',
    'NetworkManagerAlreadyEnabledOrDisabledError',
    'NetworkManagerUnknownLogLevelError',
    'NetworkManagerUnknownLogDomainError',
    'NetworkManagerInvalidArgumentsError',
    'NetworkManagerMissingPluginError',
    'NmSecretManagerFailedError',
    'NmSecretManagerPermissionDeniedError',
    'NmSecretManagerInvalidConnectionError',
    'NmSecretManagerUserCanceledError',
    'NmSecretManagerAgentCanceledError',
    'NmSecretManagerNoSecretsError',
    'NmSettingsFailedError',
    'NmSettingsPermissionDeniedError',
    'NmSettingsNotSupportedError',
    'NmSettingsInvalidConnectionError',
    'NmSettingsReadOnlyConnectionError',
    'NmSettingsUuidExistsError',
    'NmSettingsInvalidHostnameError',
    'NmSettingsInvalidArgumentsError',
    'NmVpnPluginFailedError',
    'NmVpnPluginStartingInProgressError',
    'NmVpnPluginAlreadyStartedError',
    'NmVpnPluginStoppingInProgressError',
    'NmVpnPluginAlreadyStoppedError',
    'NmVpnPluginWrongStateError',
    'NmVpnPluginBadArgumentsError',
    'NmVpnPluginLaunchFailedError',
    'NmVpnPluginInvalidConnectionError',
    'NmVpnPluginInteractiveNotSupportedError',

    'NetworkManagerSetting',
    'NetworkManagerSettingsDomain',
    'NetworkManagerConnectionProperties',
    'SettingsDict',
)
