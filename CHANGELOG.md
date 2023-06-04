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
