## 3.0.0

### Breaking changes

All enums were revisisted and updated in accordance to NetworkManager documentation.

Some enums and their fields were renamed:

* `AccessPointCapabilities` -> `WifiAccessPointCapabilities`
* `WirelessCapabilities` -> `WifiCapabilities`
* `WpaSecurityFlags` -> `WifiAccessPointSecurityFlags`
  * `P2P_*` -> `PAIR_*`
  * `BROADCAST_*` -> `GROUP_*`
  * `AUTH_*` -> `KEY_MGMT_*`
* `ConnectionState` -> `ActiveConnectionState`
* `ConnectionStateReason` -> `ActiveConnectionStateReason`
* `ConnectionFlags` -> `SettingsConnectionFlags`
* `ConnectionStateFlags` -> `ActivationStateFlags`
* `DeviceCapabilities` -> `DeviceCapabilitiesFlags`
* `BluetoothCapabilities` -> `BluetoothCapabilitiesFlags`
* `ModemCapabilities` -> `ModemCapabilitiesFlags`
* `SecretAgentCapabilities` -> `SecretAgentCapabilitiesFlags`
* `VpnState` -> `VpnServiceState`
* `VpnFailure`
  * `LOGIN_FAILURE` -> `LOGIN_FAILED`

New enums:

* `NetworkManagerCapabilities`
* `WimaxNSPNetworkType`
* `SecretAgentGetSecretsFlags`
* `CheckpointCreateFlags`
* `CheckpointRollbackResult`
* `SettingsAddConnection2Flags`
* `SettingsUpdate2Flags`
* `DeviceReapplyFlags`
* `NetworkManagerReloadFlags`
* `RadioFlags`
* `MptcpFlags`
* `VpnConnectionState`
* `VpnConnectionStateReason`

## 2.0.0

### Warning if you used pre-release version

`connection_profile` of `NetworkConnectionSettings` object has been replaced with
equivalent `get_profile` method which can also fetch the secrets fields. (you can
use `mypy` to check)

### Breaking changes

* Renamed certain elements of `ConnectionType` enum to match `DeviceType` enum.

  * `WIRED` -> `ETHERNET`
  * `GSM` -> `MODEM`

### Features

* Added connection settings dataclasses.
  Those dataclasses are found under `networkmanager.settings` sub-package.
  They allow for easy and typed reading, modifying and writing connection settings
  without dealing with D-Bus variants.

  Thank you @bernhardkaindl for spearheading this feature.

  New methods have been added to existing interfaces that utilize the new dataclasses:

  * `NetworkManagerSettingsConnectionInterface`

    * `get_profile`
    * `update_profile`

  * `NetworkManagerSettingsInterface`

    * `add_connection_profile`

  * `NetworkManagerInterfaceAsync`

    * `add_and_activate_connection_profile`

* Added support for loopback devices from NetworkManager 1.42

## 1.1.0

### Features

* Added NetworkManager errors as named exceptions.

## 1.0.0

Initial release.
