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
"""Enums used by the NetworkManager.

`Copied from NetworkManager documentation.
<https://www.networkmanager.dev/docs/api/latest/nm-dbus-types.html>`_
"""
from __future__ import annotations

from enum import Enum, IntEnum, IntFlag


class NetworkManagerVersionInfoCapability(IntEnum):
    """The numeric values represent the bit index of the capability.

    These capabilities can be queried in the ``version_info`` D-Bus property.

    Since NetworkManager 1.42.
    """

    SYNC_ROUTE_WITH_TABLE = 0
    """Contains the fix to a bug that caused that routes in table other
    than main were not removed on reapply nor on connection down.
    """
    IP4_FORWARDING = 1
    """Indicates that NetworkManager supports configuring per-device IPv4
    sysctl forwarding setting.

    Since NetworkManager 1.54.
    """
    SRIOV_PRESERVE_ON_DOWN = 2
    """NetworkManager supports the "sriov.preserve-on-down" property.

    Since NetworkManager 1.54.
    """


class NetworkManagerCapabilitiesFlags(IntFlag):
    """NetworkManager loaded plugins.

    Capabilities are positive numbers. They are part of stable API and
    a certain capability number is guaranteed not to change.

    The range 0x7000 - 0x7FFF of capabilities is guaranteed not to be
    used by upstream NetworkManager. It could thus be used for
    downstream extensions.

    Since NetworkManager 1.6.
    """

    TEAM = 0x1
    """Teams can be managed. This means the team device plugin is loaded."""
    OVS = 0x2
    """OpenVSwitch can be managed. This means the OVS device plugin is loaded.

    Since NetworkManager 1.24.
    """


class NetworkManagerState(IntEnum):
    """Indicates the current overall networking state."""

    UNKNOWN = 0
    """Networking state is unknown.

    This indicates a daemon error that makes it unable to reasonably assess
    the state. In such event the applications are expected to assume Internet
    connectivity might be present and not disable controls that require
    network access. The graphical shells may hide the network accessibility
    indicator altogether since no meaningful status indication can be provided.
    """
    ASLEEP = 10
    """Networking is not enabled, the system is being suspended or resumed
    from suspend."""
    DISCONNECTED = 20
    """There is no active network connection.

    The graphical shell should indicate no network connectivity and
    the applications should not attempt to access the network.
    """
    DISCONNECTING = 30
    """Network connections are being cleaned up.

    The applications should tear down their network sessions.
    """
    CONNECTING = 40
    """A network connection is being started.

    The graphical shell should indicate the network is being connected
    while the applications should still make no attempts to connect
    the network.
    """
    CONNECTED_LOCAL = 50
    """There is only local IPv4 and/or IPv6 connectivity, but no default route
    to access the Internet.

    The graphical shell should indicate no network connectivity.
    """
    CONNECTED_SITE = 60
    """There is only site-wide IPv4 and/or IPv6 connectivity.

    This means a default route is available, but the Internet
    connectivity check (see "Connectivity" property) did not succeed.
    The graphical shell should indicate limited network connectivity.
    """
    GLOBAL = 70
    """There is global IPv4 and/or IPv6 Internet connectivity.

    This means the Internet connectivity check succeeded, the graphical shell
    should indicate full network connectivity.
    """


class ConnectivityState(IntEnum):
    """System connectivity state."""

    UNKNOWN = 0
    """Network connectivity is unknown.

    This means the connectivity checks are disabled (e.g. on server
    installations) or has not run yet. The graphical shell should assume
    the Internet connection might be available and not present a captive
    portal window."""
    NONE = 1
    """The host is not connected to any network.

    There's no active connection that contains a default route to the internet
    and thus it makes no sense to even attempt a connectivity check.
    The graphical shell should use this state to indicate the network
    connection is unavailable."""
    PORTAL = 2
    """The Internet connection is hijacked by a captive portal gateway.

    The graphical shell may open a sandboxed web browser window (because
    the captive portals typically attempt a man-in-the-middle attacks against
    the https connections) for the purpose of authenticating to a gateway and
    retrigger the connectivity check with CheckConnectivity() when the browser
    window is dismissed."""
    LIMITED = 3
    """The host is connected to a network, does not appear to be able to reach
    the full Internet, but a captive portal has not been detected."""
    FULL = 4
    """The host is connected to a network, and appears to be able to reach the
    full Internet."""


class DeviceType(IntEnum):
    """Indicate the type of hardware represented by a device object."""

    UNKNOWN = 0
    """Unknown device."""
    ETHERNET = 1
    """A wired ethernet device."""
    WIFI = 2
    """An 802.11 Wi-Fi device."""
    UNUSED1 = 3
    """Not used."""
    UNUSED2 = 4
    """Not used."""
    BLUETOOTH = 5
    """A Bluetooth device supporting PAN or DUN access protocols."""
    OLPC_MESH = 6
    """An OLPC XO mesh networking device."""
    WIMAX = 7
    """An 802.16e Mobile WiMAX broadband device."""
    MODEM = 8
    """A modem supporting analog telephone, CDMA/EVDO, GSM/UMTS, or
    LTE network access protocols."""
    INFINIBAND = 9
    """An IP-over-InfiniBand device."""
    BOND = 10
    """A bond master interface."""
    VLAN = 11
    """An 802.1Q VLAN interface."""
    ADSL = 12
    """ADSL modem."""
    BRIDGE = 13
    """A bridge master interface."""
    GENERIC = 14
    """Generic support for unrecognized device types."""
    TEAM = 15
    """A team master interface."""
    TUN = 16
    """A TUN or TAP interface."""
    IP_TUNNEL = 17
    """A IP tunnel interface."""
    MACVLAN = 18
    """A MACVLAN interface."""
    VXLAN = 19
    """A VXLAN interface."""
    VETH = 20
    """A VETH interface."""
    MACSEC = 21
    """A MACsec interface."""
    DUMMY = 22
    """A dummy interface."""
    PPP = 23
    """A PPP interface."""
    OVS_INTERFACE = 24
    """A Open vSwitch interface."""
    OVS_PORT = 25
    """A Open vSwitch port."""
    OVS_BRIDGE = 26
    """A Open vSwitch bridge."""
    WPAN = 27
    """A IEEE 802.15.4 (WPAN) MAC Layer Device."""
    SIXLOWPAN = 28
    """6LoWPAN interface."""
    WIREGUARD = 29
    """A WireGuard interface."""
    WIFI_P2P = 30
    """An 802.11 Wi-Fi P2P device.

    Since NetworkManager 1.16.
    """
    VRF = 31
    """A VRF (Virtual Routing and Forwarding) interface.

    Since NetworkManager 1.24.
    """
    LOOPBACK = 32
    """A loopback interface.

    Since NetworkManager 1.42.
    """
    HSR = 33
    """A HSR/PRP device.

    Since NetworkManager 1.46.
    """
    IPVLAN = 34
    """A IPVLAN device.

    Since NetworkManager 1.52.
    """


class DeviceCapabilitiesFlags(IntFlag):
    """General device capability flags."""

    NONE = 0x00000000
    """Device has no special capabilities."""
    SUPPORTED = 0x00000001
    """NetworkManager supports this device."""
    CARRIER_DETECTABLE = 0x00000002
    """This device can indicate carrier status."""
    IS_SOFTWARE = 0x00000004
    """This device is a software device."""
    CAN_SRIOV = 0x00000008
    """This device supports single-root I/O virtualization."""


class WifiCapabilitiesFlags(IntFlag):
    """802.11 specific device encryption and authentication flags."""

    NONE = 0x00000000
    """Device has no encryption/authentication capabilities."""
    CIPHER_WEP40 = 0x00000001
    """Device supports 40/64-bit WEP encryption."""
    CIPHER_WEP104 = 0x00000002
    """Device supports 104/128-bit WEP encryption."""
    CIPHER_TKIP = 0x00000004
    """Device supports TKIP encryption."""
    CIPHER_CCMP = 0x00000008
    """Device supports AES/CCMP encryption."""
    WPA = 0x00000010
    """Device supports WPA1 authentication."""
    WPA2 = 0x00000020
    """Device supports WPA2/RSN authentication."""
    AP = 0x00000040
    """Device supports Access Point mode."""
    ADHOC = 0x00000080
    """Device supports Ad-Hoc mode."""
    FREQ_VALID = 0x00000100
    """Device reports frequency capabilities."""
    FREQ_2GHZ = 0x00000200
    """Device supports 2.4GHz frequencies."""
    FREQ_5GHZ = 0x00000400
    """Device supports 5GHz frequencies."""
    MESH = 0x00001000
    """Device supports acting as a mesh point.

    Since NetworkManager 1.20.
    """
    IBSS_WPA2 = 0x2000
    """Device supports WPA2/RSN in an IBSS network.

    Since NetworkManager 1.22.
    """


class WifiAccessPointCapabilitiesFlags(IntFlag):
    """802.11 access point flags."""

    NONE = 0x00000000
    """Access point has no special capabilities."""
    PRIVACY = 0x00000001
    """Access point requires authentication and encryption.

    Usually means WEP.
    """
    WPS = 0x00000002
    """Access point supports some WPS method."""
    WPS_BUTTON = 0x00000004
    """Access point supports push-button WPS."""
    WPS_PIN = 0x00000008
    """Access point supports PIN-based WPS."""


class WifiAccessPointSecurityFlags(IntFlag):
    """802.11 access point security and authentication flags.

    These flags describe the current security requirements of an access point
    as determined from the access point's beacon.
    """

    NONE = 0x00000000
    """The access point has no special security requirements."""
    PAIR_WEP40 = 0x00000001
    """40/64-bit WEP is supported for pairwise/unicast encryption."""
    PAIR_WEP104 = 0x00000002
    """104/128-bit WEP is supported for pairwise/unicast encryption."""
    PAIR_TKIP = 0x00000004
    """TKIP is supported for pairwise/unicast encryption."""
    PAIR_CCMP = 0x00000008
    """AES/CCMP is supported for pairwise/unicast encryption."""
    GROUP_WEP40 = 0x00000010
    """40/64-bit WEP is supported for group/broadcast encryption."""
    GROUP_WEP104 = 0x00000020
    """104/128-bit WEP is supported for group/broadcast encryption."""
    GROUP_TKIP = 0x00000040
    """TKIP is supported for group/broadcast encryption."""
    GROUP_CCMP = 0x00000080
    """AES/CCMP is supported for group/broadcast encryption."""
    KEY_MGMT_PSK = 0x00000100
    """WPA/RSN Pre-Shared Key encryption is supported."""
    KEY_MGMT_802_1X = 0x00000200
    """802.1x authentication and key management is supported."""
    KEY_MGMT_SAE = 0x00000400
    """WPA/RSN Simultaneous Authentication of Equals is supported."""
    KEY_MGMT_OWE = 0x00000800
    """WPA/RSN Opportunistic Wireless Encryption is supported."""
    KEY_MGMT_OWE_TM = 0x00001000
    """WPA/RSN Opportunistic Wireless Encryption transition mode is supported.

    Since NetworkManager 1.26.
    """
    KEY_MGMT_EAP_SUITE_B_192 = 0x00002000
    """WPA3 Enterprise Suite-B 192 bit mode is supported.

    Since NetworkManager 1.30.
    """


class WiFiOperationMode(IntEnum):
    """Indicates the 802.11 mode an access point or device is currently in."""

    UNKNOWN = 0
    """The device or access point mode is unknown."""
    ADHOC = 1
    """For both devices and access point objects, indicates the object is part
    of an Ad-Hoc 802.11 network without a central coordinating access point."""
    INFRA = 2
    """The device or access point is in infrastructure mode.

    For devices, this indicates the device is an 802.11 client/station. For
    access point objects, this indicates the object is an access point that
    provides connectivity to clients.
    """
    AP = 3
    """The device is an access point/hotspot.

    Not valid for access point objects; used only for hotspot mode on the
    local machine.
    """
    MESH = 4
    """The device is a 802.11s mesh point.

    Since NetworkManager 1.20.
    """


class BluetoothCapabilitiesFlags(IntFlag):
    """Bluetooth device capabilities."""

    NONE = 0x00000000
    """Device has no usable capabilities."""
    DUN = 0x00000001
    """Device provides Dial-Up Networking capability."""
    NAP = 0x00000002
    """Device provides Network Access Point capability."""


class ModemCapabilitiesFlags(IntFlag):
    """Modem device capabilities.

    Indicates the generic radio access technology families a modem device
    supports. For more information on the specific access technologies
    the device supports use the ModemManager D-Bus API.
    """

    NONE = 0x00000000
    """Modem has no usable capabilities."""
    POTS = 0x00000001
    """Modem uses the analog wired telephone network and is not a
    wireless/cellular device."""
    CDMA_EVDO = 0x00000002
    """Modem supports at least one of CDMA 1xRTT, EVDO revision 0, EVDO
    revision A, or EVDO revision B."""
    GSM_UMTS = 0x00000004
    """Modem supports at least one of GSM, GPRS, EDGE, UMTS, HSDPA, HSUPA
    or HSPA+ packet switched data capability."""
    LTE = 0x00000008
    """Modem has LTE data capability."""
    SGNR = 0x00000040
    """Modem has 5GNR data capability.

    Since NetworkManager 1.36.
    """


class WimaxNSPNetworkType(IntEnum):
    """WiMAX network type."""

    UNKNOWN = 0
    """Unknown network type."""
    HOME = 1
    """Home network."""
    PARTNER = 2
    """Partner network."""
    ROAMING_PARTNER = 3
    """Roaming partner network."""


class DeviceState(IntEnum):
    """Device's state."""

    UNKNOWN = 0
    """The device's state is unknown."""
    UNMANAGED = 10
    """The device is recognized, but not managed by NetworkManager."""
    UNAVAILABLE = 20
    """The device is managed by NetworkManager, but is not available for use.

    Reasons may include the wireless switched off, missing firmware, no
    ethernet carrier, missing supplicant or modem manager, etc.
    """
    DISCONNECTED = 30
    """The device can be activated, but is currently idle and not connected
    to a network."""
    PREPARE = 40
    """The device is preparing the connection to the network.

    This may include operations like changing the MAC address, setting physical
    link properties, and anything else required to connect to the requested
    network.
    """
    CONFIG = 50
    """The device is connecting to the requested network.

    This may include operations like associating with the Wi-Fi AP, dialing
    the modem, connecting to the remote Bluetooth device, etc.
    """
    NEED_AUTH = 60
    """The device requires more information to continue connecting to
    the requested network.

    This includes secrets like WiFi passphrases, login passwords, PIN
    codes, etc.
    """
    IP_CONFIG = 70
    """The device is requesting IPv4 and/or IPv6 addresses and routing
    information from the network."""
    IP_CHECK = 80
    """The device is checking whether further action is required for the
    requested network connection.

    This may include checking whether only local network access is available,
    whether a captive portal is blocking access to the Internet, etc.
    """
    SECONDARIES = 90
    """The device is waiting for a secondary connection (like a VPN) which
    must activated before the device can be activated"""
    ACTIVATED = 100
    """The device has a network connection, either local or global."""
    DEACTIVATING = 110
    """A disconnection from the current network connection was requested,
    and the device is cleaning up resources used for that connection.

    The network connection may still be valid.
    """
    FAILED = 120
    """The device failed to connect to the requested network and
    is cleaning up the connection request"""


class DeviceStateReason(IntEnum):
    """Device state change reason codes."""

    NONE = 0
    """No reason given."""
    UNKNOWN = 1
    """Unknown error."""
    NOW_MANAGED = 2
    """Device is now managed."""
    NOW_UNMANAGED = 3
    """Device is now unmanaged."""
    CONFIG_FAILED = 4
    """The device could not be readied for configuration."""
    IP_CONFIG_UNAVAILABLE = 5
    """IP configuration could not be reserved.

    No available address, timeout, etc...
    """
    IP_CONFIG_EXPIRED = 6
    """The IP config is no longer valid."""
    NO_SECRETS = 7
    """Secrets were required, but not provided."""
    SUPPLICANT_DISCONNECT = 8
    """802.1x supplicant disconnected."""
    SUPPLICANT_CONFIG_FAILED = 9
    """802.1x supplicant configuration failed."""
    SUPPLICANT_FAILED = 10
    """802.1x supplicant failed."""
    SUPPLICANT_TIMEOUT = 11
    """802.1x supplicant took too long to authenticate."""
    PPP_START_FAILED = 12
    """PPP service failed to start."""
    PPP_DISCONNECT = 13
    """PPP service disconnected."""
    PPP_FAILED = 14
    """PPP failed."""
    DHCP_START_FAILED = 15
    """DHCP client failed to start."""
    DHCP_ERROR = 16
    """DHCP client error."""
    DHCP_FAILED = 17
    """DHCP client failed."""
    SHARED_START_FAILED = 18
    """Shared connection service failed to start."""
    SHARED_FAILED = 19
    """Shared connection service failed."""
    AUTOIP_START_FAILED = 20
    """AutoIP service failed to start."""
    AUTOIP_ERROR = 21
    """AutoIP service error."""
    AUTOIP_FAILED = 22
    """AutoIP service failed."""
    MODEM_BUSY = 23
    """The line is busy."""
    MODEM_NO_DIAL_TONE = 24
    """No dial tone."""
    MODEM_NO_CARRIER = 25
    """No carrier could be established."""
    MODEM_DIAL_TIMEOUT = 26
    """The dialing request timed out."""
    MODEM_DIAL_FAILED = 27
    """The dialing attempt failed."""
    MODEM_INIT_FAILED = 28
    """Modem initialization failed."""
    GSM_APN_FAILED = 29
    """Failed to select the specified APN."""
    GSM_REGISTRATION_NOT_SEARCHING = 30
    """Not searching for networks."""
    GSM_REGISTRATION_DENIED = 31
    """Network registration denied."""
    GSM_REGISTRATION_TIMEOUT = 32
    """Network registration timed out."""
    GSM_REGISTRATION_FAILED = 33
    """Failed to register with the requested network."""
    GSM_PIN_CHECK_FAILED = 34
    """PIN check failed."""
    FIRMWARE_MISSING = 35
    """Necessary firmware for the device may be missing."""
    REMOVED = 36
    """The device was removed."""
    SLEEPING = 37
    """NetworkManager went to sleep."""
    CONNECTION_REMOVED = 38
    """The device's active connection disappeared."""
    USER_REQUESTED = 39
    """Device disconnected by user or client."""
    CARRIER = 40
    """Carrier/link changed."""
    CONNECTION_ASSUMED = 41
    """The device's existing connection was assumed."""
    SUPPLICANT_AVAILABLE = 42
    """The supplicant is now available."""
    MODEM_NOT_FOUND = 43
    """The modem could not be found."""
    BT_FAILED = 44
    """The Bluetooth connection failed or timed out."""
    GSM_SIM_NOT_INSERTED = 45
    """GSM Modem's SIM Card not inserted."""
    GSM_SIM_PIN_REQUIRED = 46
    """GSM Modem's SIM Pin required."""
    GSM_SIM_PUK_REQUIRED = 47
    """GSM Modem's SIM Puk required."""
    GSM_SIM_WRONG = 48
    """GSM Modem's SIM wrong."""
    INFINIBAND_MODE = 49
    """InfiniBand device does not support connected mode."""
    DEPENDENCY_FAILED = 50
    """A dependency of the connection failed."""
    BR2684_FAILED = 51
    """Problem with the RFC 2684 Ethernet over ADSL bridge."""
    MODEM_MANAGER_UNAVAILABLE = 52
    """ModemManager not running."""
    SSID_NOT_FOUND = 53
    """The Wi-Fi network could not be found."""
    SECONDARY_CONNECTION_FAILED = 54
    """A secondary connection of the base connection failed."""
    DCB_FCOE_FAILED = 55
    """DCB or FCoE setup failed."""
    TEAMD_CONTROL_FAILED = 56
    """teamd control failed."""
    MODEM_FAILED = 57
    """Modem failed or no longer available."""
    MODEM_AVAILABLE = 58
    """Modem now ready and available."""
    SIM_PIN_INCORRECT = 59
    """SIM PIN was incorrect."""
    NEW_ACTIVATION = 60
    """New connection activation was enqueued."""
    PARENT_CHANGED = 61
    """The device's parent changed."""
    PARENT_MANAGED_CHANGED = 62
    """The device parent's management changed."""
    OVSDB_FAILED = 63
    """Problem communicating with Open vSwitch database."""
    IP_ADDRESS_DUPLICATE = 64
    """A duplicate IP address was detected."""
    IP_METHOD_UNSUPPORTED = 65
    """The selected IP method is not supported."""
    SRIOV_CONFIGURATION_FAILED = 66
    """Configuration of SR-IOV parameters failed."""
    PEER_NOT_FOUND = 67
    """The Wi-Fi P2P peer could not be found."""
    DEVICE_HANDLER_FAILED = 68
    """The device handler dispatcher returned an error.

    Since NetworkManager 1.46.
    """
    UNMANAGED_BY_DEFAULT = 69
    """The device is unmanaged because the device type is unmanaged by default.

    Since NetworkManager 1.48.
    """
    UNMANAGED_EXTERNAL_DOWN = 70
    """The device is unmanaged because it is an external device and is
    unconfigured (down or without addresses).

    Since NetworkManager 1.48.
    """
    UNMANAGED_LINK_NOT_INIT = 71
    """The device is unmanaged because the link is not initialized by udev.

    Since NetworkManager 1.48.
    """
    UNMANAGED_QUITTING = 72
    """The device is unmanaged because NetworkManager is quitting.

    Since NetworkManager 1.48.
    """
    UNMANAGED_SLEEPING = 73
    """The device is unmanaged because networking is disabled or the system
    is suspended.

    Since NetworkManager 1.48.
    """
    UNMANAGED_USER_CONF = 74
    """The device is unmanaged by user decision in NetworkManager.conf.

    Since NetworkManager 1.48.
    """
    UNMANAGED_USER_EXPLICIT = 75
    """The device is unmanaged by explicit user decision.

    Since NetworkManager 1.48.
    """
    UNMANAGED_USER_SETTINGS = 76
    """The device is unmanaged by user decision via settings plugin.

    Since NetworkManager 1.48.
    """
    UNMANAGED_USER_UDEV = 77
    """The device is unmanaged via udev rule.

    Since NetworkManager 1.48.
    """


class DeviceMetered(IntEnum):
    """Device metered state.

    The NMMetered enum has two different purposes: one is to configure
    "connection.metered" setting of a ConnectionSettings, and
    the other is to express the actual metered state of the Device at a given
    moment.

    For the connection profile only UNKNOWN, NO and YES are allowed.

    The device's metered state at runtime is determined by the profile which
    is currently active. If the profile explicitly specifies NO or YES, then
    the device's metered state is as such. If the connection profile leaves it
    undecided at UNKNOWN (the default), then NetworkManager tries to guess
    the metered state, for example based on the device type or on DHCP options
    (like Android devices exposing a "ANDROID_METERED" DHCP vendor option).
    This then leads to either GUESS_NO or GUESS_YES.

    Most applications probably should treat the runtime state
    GUESS_YES like YES, and all other states as not metered.

    Note that the per-device metered states are then combined to a global
    metered state. This is basically the metered state of the device with the
    best default route. However, that generalization of a global metered state
    may not be correct if the default routes for IPv4 and IPv6 are on different
    devices, or if policy routing is configured. In general, the global metered
    state tries to express whether the traffic is likely metered, but since
    that depends on the traffic itself, there is not one answer in all cases.
    Hence, an application may want to consider the per-device's metered states.
    """

    UNKNOWN = 0
    """The metered status is unknown."""
    YES = 1
    """Metered, the value was explicitly configured."""
    NO = 2
    """Not metered, the value was explicitly configured."""
    GUESS_YES = 3
    """Metered, the value was guessed."""
    GUESS_NO = 4
    """Not metered, the value was guessed."""


class ConnectionMultiConnect(IntEnum):
    """Ability of a connection to be active on multiple devices.

    Since NetworkManager 1.14.
    """

    DEFAULT = 0
    """Indicates that the per-connection setting is unspecified.

    In this case, it will fallback to the default value of SINGLE.
    """
    SINGLE = 1
    """The connection profile can only be active once at each moment.

    Activating a profile that is already active, will first deactivate it.
    """
    MANUAL_MULTIPLE = 2
    """The profile can be manually activated multiple times
    on different devices.

    However, regarding autoconnect, the profile will autoconnect only if it
    is currently not connected otherwise.
    """
    MULTIPLE = 3
    """The profile can autoactivate and be manually activated multiple
    times together."""


class ActiveConnectionState(IntEnum):
    """Indicates the state of an active connection to a specific network."""

    UNKNOWN = 0
    """The state of the connection is unknown."""
    ACTIVATING = 1
    """A network connection is being prepared."""
    ACTIVATED = 2
    """There is a connection to the network."""
    DEACTIVATING = 3
    """The network connection is being torn down and cleaned up."""
    DEACTIVATED = 4
    """The network connection is disconnected and will be removed."""


class ActiveConnectionStateReason(IntEnum):
    """Active connection state reasons.

    Since NetworkManager 1.8.
    """

    UNKNOWN = 0
    """The reason for the active connection state change is unknown."""
    NONE = 1
    """No reason was given for the active connection state change."""
    USER_DISCONNECTED = 2
    """The active connection changed state because the user disconnected it."""
    DEVICE_DISCONNECTED = 3
    """The active connection changed state because the device it was using was
    disconnected."""
    SERVICE_STOPPED = 4
    """The service providing the VPN connection was stopped."""
    IP_CONFIG_INVALID = 5
    """The IP config of the active connection was invalid."""
    CONNECT_TIMEOUT = 6
    """The connection attempt to the VPN service timed out."""
    SERVICE_START_TIMEOUT = 7
    """A timeout occurred while starting the service providing the
    VPN connection."""
    SERVICE_START_FAILED = 8
    """Starting the service providing the VPN connection failed."""
    NO_SECRETS = 9
    """Necessary secrets for the connection were not provided."""
    LOGIN_FAILED = 10
    """Authentication to the server failed."""
    CONNECTION_REMOVED = 11
    """The connection was deleted from settings."""
    DEPENDENCY_FAILED = 12
    """Master connection of this connection failed to activate."""
    DEVICE_REALIZE_FAILED = 13
    """Could not create the software device link."""
    DEVICE_REMOVED = 14
    """The device this connection depended on disappeared."""


class SecretAgentGetSecretsFlags(IntFlag):
    """Flags to modify the behavior of a get_secrets request."""

    NONE = 0x0
    """No special behavior.

    By default no user interaction is allowed and requests for secrets
    are fulfilled from persistent storage, or if no secrets are available
    an error is returned.
    """
    ALLOW_INTERACTION = 0x1
    """Allows the request to interact with the user.

    Possibly prompting via UI for secrets if any are required, or if none
    are found in persistent storage.
    """
    REQUEST_NEW = 0x2
    """Explicitly prompt for new secrets from the user.

    This flag signals that NetworkManager thinks any existing secrets
    are invalid or wrong. This flag implies that interaction is allowed.
    """
    FLAG_USER_REQUESTED = 0x4
    """Set if the request was initiated by user-requested action via the D-Bus
    interface, as opposed to automatically initiated by NetworkManager
    in response to (for example) scan results or carrier changes."""
    WPS_PBC_ACTIVE = 0x8
    """Indicates that WPS enrollment is active with PBC method.

    The agent may suggest that the user pushes a button on the router
    instead of supplying a PSK.
    """


class SecretAgentCapabilitiesFlags(IntFlag):
    """Secret agent capabilities."""

    NONE = 0x0
    """The agent supports no special capabilities."""
    VPN_HINTS = 0x1
    """The agent supports passing hints to VPN plugin
    authentication dialogs."""


class IpTunnelMode(IntEnum):
    """Mode of IP tunnel.

    Since NetworkManager 1.2.
    """

    UNKNOWN = 0
    """Unknown/unset tunnel mode."""
    IP_IP = 1
    """IP in IP tunnel."""
    GRE = 2
    """GRE tunnel."""
    SIT = 3
    """SIT tunnel."""
    ISATAP = 4
    """ISATAP tunnel."""
    VTI = 5
    """VTI tunnel."""
    IP6_IP6 = 6
    """IPv6 in IPv6 tunnel."""
    IP_IP6 = 7
    """IPv4 in IPv6 tunnel."""
    IP6_GRE = 8
    """IPv6 GRE tunnel."""
    VTI6 = 9
    """IPv6 VTI tunnel."""
    GRE_TAP = 10
    """GRETAP tunnel."""
    IP6_GRE_TAP = 11
    """IPv6 GRETAP tunnel."""


class CheckpointCreateFlags(IntFlag):
    """Flags for checkpoint_create call.

    Since NetworkManager 1.4.
    """

    NONE = 0
    """No flags."""
    DESTROY_ALL = 0x01
    """When creating a new checkpoint, destroy all existing ones."""
    DELETE_NEW_CONNECTIONS = 0x02
    """Upon rollback, delete any new connection added after the checkpoint.

    Since NetworkManager 1.6.
    """
    NEW_DEVICES = 0x04
    """Upon rollback, disconnect any new device appeared after the checkpoint.

    Since NetworkManager 1.6.
    """
    ALLOW_OVERLAPPING = 0x08
    """By default, creating a checkpoint fails if there are already existing
    checkpoints that reference the same devices. With this flag, creation of
    such checkpoints is allowed, however, if an older checkpoint that
    references overlapping devices gets rolled back, it will automatically
    destroy this checkpoint during rollback. This allows to create several
    overlapping checkpoints in parallel, and rollback to them at will. With
    the special case that rolling back to an older checkpoint will invalidate
    all overlapping younger checkpoints. This opts-in that the checkpoint can
    be automatically destroyed by the rollback of an older checkpoint.

    Since NetworkManager 1.12.
    """
    NO_PRESERVE_EXTERNAL_PORTS = 0x10
    """During rollback, by default externally added ports attached to
    bridge devices are preserved. With this flag, the rollback detaches all
    external ports. This only has an effect for bridge ports. Before
    NetworkManager 1.38, this was the default behavior.

    Since NetworkManager 1.38.
    """
    TRACK_INTERNAL_GLOBAL_DNS = 0x20
    """during rollback, by default changes to global DNS via D-BUS interface
    are preserved. With this flag, the rollback reverts the global DNS changes
    made via D-Bus interface. Global DNS defined in [global-dns] section of
    NetworkManager.conf is not impacted by this flag.

    Since NetworkManager 1.48.
    """


class CheckpointRollbackResult(IntEnum):
    """The result of a checkpoint rollback for a specific device."""

    OK = 0
    """The rollback succeeded."""
    ERR_NO_DEVICE = 1
    """The device no longer exists."""
    ERR_DEVICE_UNMANAGED = 2
    """The device is now unmanaged."""
    ERR_FAILED = 3
    """Other errors during rollback."""


class SettingsConnectionFlags(IntFlag):
    """Settings Connection flags."""

    NONE = 0
    """An alias for numeric zero, no flags set."""
    UNSAVED = 0x01
    """The connection is not saved to disk.

    That either means, that the connection is in-memory only
    and currently is not backed by a file. Or, that the connection is
    backed by a file, but has modifications in-memory that were not
    persisted to disk.
    """
    NM_GENERATED = 0x02
    """A connection is "nm-generated" if it was generated by NetworkManger.

    If the connection gets modified or saved by the user, the flag
    gets cleared. A nm-generated is also unsaved and has no backing
    file as it is in-memory only.
    """
    VOLATILE = 0x04
    """The connection will be deleted when it disconnects.

    That is for in-memory connections (unsaved), which are currently active
    but deleted on disconnect. Volatile connections are always unsaved, but
    they are also no backing file on disk and are entirely in-memory only.
    """
    EXTERNAL = 0x08
    """The profile was generated to represent
    an external configuration of a networking device.

    Since NetworkManager 1.26.
    """


class ActivationStateFlags(IntFlag):
    """Flags describing the current activation state.

    Since NetworkManager 1.10.
    """

    NONE = 0
    """An alias for numeric zero, no flags set."""
    IS_MASTER = 0x1
    """The device is a master."""
    IS_SLAVE = 0x2
    """The device is a slave."""
    LAYER2_READY = 0x4
    """Layer2 is activated and ready."""
    IP4_READY = 0x8
    """IPv4 setting is completed."""
    IP6_READY = 0x10
    """IPv6 setting is completed."""
    MASTER_HAS_SLAVES = 0x20
    """The master has any slave devices attached.

    This only makes sense if the device is a master.
    """
    LIFE_TIME_BOUND_TO_PROFILE_VISIBILITY = 0x40
    """The lifetime of the activation is bound to the visibility of
    the connection profile, which in turn depends on "connection.permissions"
    and whether a session for the user exists.

    Since NetworkManager 1.16.
    """
    EXTERNAL = 0x80
    """The active connection was generated to represent an external
    configuration of a networking device.

    Since NetworkManager 1.26.
    """


class SettingsAddConnection2Flags(IntFlag):
    """Flags for the add_connection2() method."""

    NONE = 0
    """An alias for numeric zero, no flags set."""
    TO_DISK = 0x1
    """To persist the connection to disk."""
    IN_MEMORY = 0x2
    """To make the connection in-memory only."""
    BLOCK_AUTOCONNECT = 0x20
    """Usually, when the connection has autoconnect enabled and gets added,
    it becomes eligible to autoconnect right away. Setting this flag, disables
    autoconnect until the connection is manually activated."""


class SettingsUpdate2Flags(IntFlag):
    """Flags for the update2() method."""

    NONE = 0
    """An alias for numeric zero, no flags set."""
    TO_DISK = 0x1
    """To persist the connection to disk."""
    IN_MEMORY = 0x2
    """Makes the profile in-memory.

    Note that such profiles are stored in keyfile format under /run.
    If the file is already in-memory, the file in /run is updated in-place.
    Otherwise, the previous storage for the profile is left unchanged on disk,
    and the in-memory copy shadows it. Note that the original filename of the
    previous persistent storage (if any) is remembered. That means, when later
    persisting the profile again to disk, the file on disk will be overwritten
    again. Likewise, when finally deleting the profile, both the storage from
    /run and persistent storage are deleted (or if the persistent storage does
    not allow deletion, and nmmeta file is written to mark the UUID
    as deleted).
    """
    IN_MEMORY_DETACHED = 0x4
    """This is almost the same as IN_MEMORY, with one difference:
    when later deleting the profile, the original profile will not
    be deleted. Instead a nmmeta file is written to /run to indicate
    that the profile is gone. Note that if such a nmmeta tombstone
    file exists and hides a file in persistent storage, then when
    re-adding the profile with the same UUID, then the original storage
    is taken over again."""
    IN_MEMORY_ONLY = 0x8
    """This is like IN_MEMORY, but if the connection has a corresponding
    file on persistent storage, the file will be deleted right away.
    If the profile is later again persisted to disk, a new, unused
    filename will be chosen."""
    VOLATILE = 0x10
    """This can be specified with either IN_MEMORY, IN_MEMORY_DETACHED or
    IN_MEMORY_ONLY. After making the connection in-memory only, the connection
    is marked as volatile. That means, if the connection is currently not
    active it will be deleted right away. Otherwise, it is marked to for
    deletion once the connection deactivates. A volatile connection cannot
    autoactivate again (because it's about to be deleted), but a manual
    activation will clear the volatile flag."""
    BLOCK_AUTOCONNECT = 0x20
    """Usually, when the connection has autoconnect enabled and is modified,
    it becomes eligible to autoconnect right away. Setting this flag, disables
    autoconnect until the connection is manually activated."""
    NO_REAPPLY = 0x40
    """When a profile gets modified that is currently active, then
    these changes don't take effect for the active device unless the
    profile gets reactivated or the configuration reapplied. There are two
    exceptions: by default "connection.zone" and "connection.metered"
    properties take effect immediately. Specify this flag to prevent these
    properties to take effect, so that the change is restricted to modify
    the profile.

    Since NetworkManager 1.20.
    """


class DeviceReapplyFlags(IntFlag):
    """Flags for the reapply() methodof a device.

    Since NetworkManager 1.42.
    """

    NONE = 0
    """No flag set."""
    PRESERVE_EXTERNAL_IP = 0x1
    """During reapply, preserve external IP addresses and routes."""


class NetworkManagerReloadFlags(IntFlag):
    """Flags for the NetworkManager reload() call."""

    NONE = 0
    """An alias for numeric zero, no flags set. This reloads everything
    that is supported and is identical to a SIGHUP."""
    CONF = 0x1
    """Reload the NetworkManager.conf configuration from disk.

    Note that this does not include connections, which can be reloaded
    via Setting's reload_connections().
    """
    DNS_RC = 0x2
    """Update DNS configuration, which usually involves
    writing /etc/resolv.conf anew."""
    DNS_FULL = 0x4
    """Means to restart the DNS plugin.

    This is for example useful when using dnsmasq plugin, which uses additional
    configuration in /etc/NetworkManager/dnsmasq.d. If you edit those files,
    you can restart the DNS plugin. This action shortly interrupts name
    resolution.
    """
    ALL = 0x7
    """All flags."""


class DeviceInterfaceFlags(IntFlag):
    """Flags for a network interface.

    Since NetworkManager 1.22.
    """

    NONE = 0
    """An alias for numeric zero, no flags set."""
    UP = 0x1
    """The interface is enabled from the administrative point of view.

    Corresponds to kernel IFF_UP.
    """
    LOWER_UP = 0x2
    """The physical link is up.

    Corresponds to kernel IFF_LOWER_UP.
    """
    PROMISC = 0x4
    """Receive all packets.

    Corresponds to kernel IFF_PROMISC.

    Since NetworkManager 1.32.
    """
    CARRIER = 0x10000
    """The interface has carrier.

    In most cases this is equal to the value of LOWER_UP.
    However some devices have a non-standard carrier detection mechanism.
    """
    LLDP_CLIENT_ENABLED = 0x20000
    """The flag to indicate device LLDP status.

    Since NetworkManager 1.32.
    """


class ClientPermission(IntEnum):
    """Permissions that NetworkManager clients can obtain."""

    NONE = 0
    """Unknown or no permission."""
    ENABLE_DISABLE_NETWORK = 1
    """Controls whether networking can be globally enabled or disabled."""
    DISABLE_WIFI = 2
    """Controls whether Wi-Fi can be globally enabled or disabled."""
    DISABLE_WWAN = 3
    """Controls whether WWAN (3G) can be globally enabled or disabled."""
    DISABLE_WIMAX = 4
    """Controls whether WiMAX can be globally enabled or disabled."""
    SLEEP_WAKE = 5
    """Controls whether the client can ask NetworkManager to sleep and wake."""
    NETWORK_CONTROL = 6
    """Controls whether networking connections can be started, stopped, and
    changed.
    """
    WIFI_SHARE_PROTECTED = 7
    """Controls whether a password protected Wi-Fi hotspot can be created."""
    WIFI_SHARE_OPEN = 8
    """Controls whether an open Wi-Fi hotspot can be created."""
    SETTINGS_MODIFY_SYSTEM = 9
    """Controls whether connections that are available to all users
    can be modified.
    """
    MODIFY_OWN = 10
    """Controls whether connections owned by the current user
    can be modified.
    """
    MODIFY_HOSTNAME = 11
    """Controls whether the persistent hostname can be changed."""
    MODIFY_GLOBAL_DNS = 12
    """Modify persistent global DNS configuration."""
    RELOAD = 13
    """Controls access to reload."""
    CHECKPOINT_ROLLBACK = 14
    """Permission to create checkpoints."""
    ENABLE_DISABLE_STATISTICS = 15
    """Controls whether device statistics can be globally enabled
    or disabled.
    """
    ENABLE_DISABLE_CONNECTIVITY_CHECK = 16
    """Controls whether connectivity check can be enabled or disabled."""
    WIFI_SCAN = 17
    """Controls whether wifi scans can be performed."""


class ClientPermissionResult(IntEnum):
    """Indicate what authorizations and permissions required for permission."""

    UNKNOWN = 0
    """Unknown or no authorization."""
    YES = 1
    """Permission is available."""
    AUTH = 2
    """Authorization is necessary before the permission is available."""
    NO = 3
    """Permission to perform the operation is denied by system policy."""


class RadioFlags(IntFlag):
    """Flags related to radio interfaces.

    Since NetworkManager 1.38.
    """

    NONE = 0
    """An alias for numeric zero, no flags set."""
    WLAN_AVAILABLE = 0x1
    """A Wireless LAN device or rfkill switch is detected in the system."""
    WWAN_AVAILABLE = 0x2
    """A Wireless WAN device or rfkill switch is detected in the system."""


class MptcpFlags(IntFlag):
    """Flags related to Multi-path TCP.

    Since NetworkManager 1.40.
    """

    NONE = 0
    """The default, meaning that no MPTCP flags are set."""
    DISABLED = 0x1
    """Don't configure MPTCP endpoints on the device."""
    ENABLED = 0x2
    """MPTCP is enabled and endpoints will be configured.

    This flag is implied if any of the other flags indicate that MPTCP is
    enabled and therefore in most cases unnecessary. Note that
    if "/proc/sys/net/mptcp/enabled" sysctl is disabled, MPTCP handling is
    disabled despite this flag. This can be overruled with the
    "also-without-sysctl" flag. Note that by default interfaces that don't
    have a default route are excluded from having MPTCP endpoints configured.
    This can be overruled with the "also-without-default-route" and
    this affects endpoints per address family.
    """
    ALSO_WITHOUT_SYSCTL = 0x4
    """Even if MPTCP handling is enabled via the "enabled" flag,
    it is ignored unless "/proc/sys/net/mptcp/enabled" is on.
    With this flag, MPTCP endpoints will be configured regardless
    of the sysctl setting."""
    ALSO_WITHOUT_DEFAULT_ROUTE = 0x8
    """Even if MPTCP handling is enabled via the "enabled" flag,
    it is ignored per-address family unless NetworkManager
    configures a default route. With this flag, NetworkManager will
    also configure MPTCP endpoints if there is no default route.
    This takes effect per-address family."""
    SIGNAL = 0x10
    """Flag for the MPTCP endpoint.

    The endpoint will be announced/signaled to each peer via an MPTCP
    ADD_ADDR sub-option.
    """
    SUBFLOW = 0x20
    """Flag for the MPTCP endpoint.

    If additional subflow creation is allowed by the MPTCP limits, the MPTCP
    path manager will try to create an additional subflow using this endpoint
    as the source address after the MPTCP connection is established.
    """
    BACKUP = 0x40
    """Flag for the MPTCP endpoint.

    If this is a subflow endpoint, the subflows created using this endpoint
    will have the backup flag set during the connection process. This flag
    instructs the peer to only send data on a given subflow when all non-backup
    subflows are unavailable. This does not affect outgoing data, where subflow
    priority is determined by the backup/non-backup flag received from
    the peer.
    """
    FULLMESH = 0x80
    """Flag for the MPTCP endpoint.

    If this is a subflow endpoint and additional subflow creation is
    allowed by the MPTCP limits, the MPTCP path manager will try to create
    an additional subflow for each known peer address, using this endpoint as
    the source address. This will occur after the MPTCP connection is
    established. If the peer did not announce any additional addresses using
    the MPTCP ADD_ADDR sub-option, this will behave the same as a plain
    subflow endpoint. When the peer does announce addresses, each received
    ADD_ADDR sub-option will trigger creation of an additional subflow
    to generate a full mesh topology.
    """


# From VPN plugin

class VpnServiceState(IntEnum):
    """VPN daemon states."""

    UNKNOWN = 0
    """The state of the VPN plugin is unknown."""
    INIT = 1
    """The VPN plugin is initialized."""
    SHUTDOWN = 2
    """Not used."""
    STARTING = 3
    """The plugin is attempting to connect to a VPN server."""
    STARTED = 4
    """The plugin has connected to a VPN server."""
    STOPPING = 5
    """The plugin is disconnecting from the VPN server."""
    STOPPED = 6
    """The plugin has disconnected from the VPN server."""


class VpnConnectionState(IntEnum):
    """VPN connection states."""

    UNKNOWN = 0
    """The state of the VPN connection is unknown."""
    PREPARE = 1
    """The VPN connection is preparing to connect."""
    NEED_AUTH = 2
    """The VPN connection needs authorization credentials."""
    CONNECT = 3
    """The VPN connection is being established."""
    IP_CONFIG_GET = 4
    """The VPN connection is getting an IP address."""
    ACTIVATED = 5
    """The VPN connection is active."""
    FAILED = 6
    """The VPN connection failed."""
    DISCONNECTED = 7
    """The VPN connection is disconnected."""


class VpnConnectionStateReason(IntEnum):
    """VPN connection state reasons."""

    UNKNOWN = 0
    """The reason for the VPN connection state change is unknown."""
    NONE = 1
    """No reason was given for the VPN connection state change."""
    USER_DISCONNECTED = 2
    """The VPN connection changed state because the user disconnected it."""
    DEVICE_DISCONNECTED = 3
    """The VPN connection changed state because the device it was using
    was disconnected."""
    STOPPED = 4
    """The service providing the VPN connection was stopped."""
    IP_CONFIG_INVALID = 5
    """The IP config of the VPN connection was invalid."""
    CONNECT_TIMEOUT = 6
    """The connection attempt to the VPN service timed out."""
    SERVICE_START_TIMEOUT = 7
    """A timeout occurred while starting the service providing
    the VPN connection."""
    SERVICE_START_FAILED = 8
    """Starting the service starting the service providing the VPN connection
    failed."""
    NO_SECRETS = 9
    """Necessary secrets for the VPN connection were not provided."""
    LOGIN_FAILED = 10
    """Authentication to the VPN server failed."""
    CONNECTION_REMOVED = 11
    """The connection was deleted from settings."""


class VpnFailure(IntEnum):
    """VPN plugin failure reasons."""

    LOGIN_FAILED = 0
    """Login failed."""
    CONNECT_FAILED = 1
    """Connect failed."""
    BAD_IP_CONFIG = 2
    """Invalid IP configuration returned from the VPN plugin."""

# Connection Types, e.g. from connecion_profile.connection.type:
#
# There is no central list of all connection types in NM.
# The best bet is to look for nm_connection_is_type() checks which use
# NM_SETTING_(TYPE)_SETTING_NAME #defines (which are fined used for
# settings for this connection-type. One connection_type can have several
# of such settings groups, so we have to filter those to get the strings:
#
# Generated from NetworkManager source using:
# grep -r nm_connection_is_type src/|
#     sed -n 's/.*NM_SETTING_/NM_SETTING_/;s/_SETTING_NAME.*/=/p' |
#     sort -u >.connection_is_type
# grep -hr define.*_SETTING_NAME src/|
#     sed 's/#define //;s/_SETTING_NAME//;s/ /=/' >.setting_defines
# grep -f .connection_is_type .setting_defines |
#     sed 's/NM_SETTING_/    /;s/6L/SIXL/;/GENERIC/d;s/=/ = /'
# Manual edit: This resulted in WIRED instead of ETHERNET, but
# ETHERNET is the name used for DeviceType, so use ETHERNET instead to
# be able to lookup connection profiles for Ethernet using DeviceType.
#
# One src/core/nm-device-*.c can support more than one ConnectionType,
# thus there are more ConnectionTypes than DeviceTypes:


# From NetworkManager-1.35:
class ConnectionType(str, Enum):
    """Connection Types.

    * ADSL
    * BLUETOOTH
    * BOND
    * BRIDGE
    * CDMA
    * DUMMY
    * ETHERNET
    * MODEM
    * INFINIBAND
    * IP_TUNNEL
    * MACSEC
    * MACVLAN
    * OLPC_MESH
    * OVS_BRIDGE
    * OVS_INTERFACE
    * OVS_INTERFACE
    * PPPOE
    * SIXLOWPAN
    * TEAM
    * TUN
    * VETH
    * VLAN
    * VPN
    * VRF
    * VXLAN
    * WIFI_P2P
    * WIREGUARD
    * WIFI
    * WPAN
    * LOOPBACK
    """

    ADSL = "adsl"
    BLUETOOTH = "bluetooth"
    BOND = "bond"
    BRIDGE = "bridge"
    CDMA = "cdma"
    DUMMY = "dummy"
    ETHERNET = "802-3-ethernet"
    MODEM = "gsm"
    INFINIBAND = "infiniband"
    IP_TUNNEL = "ip-tunnel"
    MACSEC = "macsec"
    MACVLAN = "macvlan"
    OLPC_MESH = "802-11-olpc-mesh"
    OVS_BRIDGE = "ovs-bridge"
    OVS_INTERFACE = "ovs-interface"
    OVS_PORT = "ovs-port"
    PPPOE = "pppoe"
    SIXLOWPAN = "6lowpan"
    TEAM = "team"
    TUN = "tun"
    VETH = "veth"
    VLAN = "vlan"
    VPN = "vpn"
    VRF = "vrf"
    VXLAN = "vxlan"
    WIFI_P2P = "wifi-p2p"
    WIREGUARD = "wireguard"
    WIFI = "802-11-wireless"
    WPAN = "wpan"
    LOOPBACK = "loopback"
