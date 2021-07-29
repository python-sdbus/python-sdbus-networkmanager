NetworkManager errors and exceptions
====================================

Agent Manager errors
--------------------

.. autoexception:: sdbus_async.networkmanager.NmAgentManagerFailedError

.. autoexception:: sdbus_async.networkmanager.NmAgentManagerPermissionDeniedError

.. autoexception:: sdbus_async.networkmanager.NmAgentManagerInvalidIdentifierError

.. autoexception:: sdbus_async.networkmanager.NmAgentManagerNotRegisteredError

.. autoexception:: sdbus_async.networkmanager.NmAgentManagerNoSecretsError

.. autoexception:: sdbus_async.networkmanager.NmAgentManagerUserCanceledError

Connection errors
-----------------

.. autoexception:: sdbus_async.networkmanager.NmConnectionFailedError

.. autoexception:: sdbus_async.networkmanager.NmConnectionSettingNotFoundError

.. autoexception:: sdbus_async.networkmanager.NmConnectionPropertyNotFoundError

.. autoexception:: sdbus_async.networkmanager.NmConnectionPropertyNotSecretError

.. autoexception:: sdbus_async.networkmanager.NmConnectionMissingSettingError

.. autoexception:: sdbus_async.networkmanager.NmConnectionInvalidSettingError

.. autoexception:: sdbus_async.networkmanager.NmConnectionMissingPropertyError

.. autoexception:: sdbus_async.networkmanager.NmConnectionInvalidPropertyError

Device errors
-------------

.. autoexception:: sdbus_async.networkmanager.NmDeviceFailedError

.. autoexception:: sdbus_async.networkmanager.NmDeviceCreationFailedError

.. autoexception:: sdbus_async.networkmanager.NmDeviceInvalidConnectionError

.. autoexception:: sdbus_async.networkmanager.NmDeviceIncompatibleConnectionError

.. autoexception:: sdbus_async.networkmanager.NmDeviceNotActiveError

.. autoexception:: sdbus_async.networkmanager.NmDeviceNotSoftwareError

.. autoexception:: sdbus_async.networkmanager.NmDeviceNotAllowedError

.. autoexception:: sdbus_async.networkmanager.NmDeviceSpecificObjectNotFoundError

.. autoexception:: sdbus_async.networkmanager.NmDeviceVersionIdMismatchError

.. autoexception:: sdbus_async.networkmanager.NmDeviceMissingDependenciesError

.. autoexception:: sdbus_async.networkmanager.NmDeviceInvalidArgumentError

NetworkManager main errors
--------------------------

Errors raised by main NetworkManager objects.


.. autoexception:: sdbus_async.networkmanager.NetworkManagerFailedError

.. autoexception:: sdbus_async.networkmanager.NetworkManagerPermissionDeniedError

.. autoexception:: sdbus_async.networkmanager.NetworkManagerUnknownConnectionError

.. autoexception:: sdbus_async.networkmanager.NetworkManagerUnknownDeviceError

.. autoexception:: sdbus_async.networkmanager.NetworkManagerConnectionNotAvailableError

.. autoexception:: sdbus_async.networkmanager.NetworkManagerConnectionNotActiveError

.. autoexception:: sdbus_async.networkmanager.NetworkManagerConnectionAlreadyActiveError

.. autoexception:: sdbus_async.networkmanager.NetworkManagerDependencyFailedError

.. autoexception:: sdbus_async.networkmanager.NetworkManagerAlreadyAsleepOrAwakeError

.. autoexception:: sdbus_async.networkmanager.NetworkManagerAlreadyEnabledOrDisabledError

.. autoexception:: sdbus_async.networkmanager.NetworkManagerUnknownLogLevelError

.. autoexception:: sdbus_async.networkmanager.NetworkManagerUnknownLogDomainError

.. autoexception:: sdbus_async.networkmanager.NetworkManagerInvalidArgumentsError

.. autoexception:: sdbus_async.networkmanager.NetworkManagerMissingPluginError

Secret Manager errors
---------------------

Errors that secret managers pass to NetworkManager.

.. autoexception:: sdbus_async.networkmanager.NmSecretManagerFailedError

.. autoexception:: sdbus_async.networkmanager.NmSecretManagerPermissionDeniedError

.. autoexception:: sdbus_async.networkmanager.NmSecretManagerInvalidConnectionError

.. autoexception:: sdbus_async.networkmanager.NmSecretManagerUserCanceledError

.. autoexception:: sdbus_async.networkmanager.NmSecretManagerAgentCanceledError

.. autoexception:: sdbus_async.networkmanager.NmSecretManagerNoSecretsError

NetworkManager settings errors
------------------------------

.. autoexception:: sdbus_async.networkmanager.NmSettingsFailedError

.. autoexception:: sdbus_async.networkmanager.NmSettingsPermissionDeniedError

.. autoexception:: sdbus_async.networkmanager.NmSettingsNotSupportedError

.. autoexception:: sdbus_async.networkmanager.NmSettingsInvalidConnectionError

.. autoexception:: sdbus_async.networkmanager.NmSettingsReadOnlyConnectionError

.. autoexception:: sdbus_async.networkmanager.NmSettingsUuidExistsError

.. autoexception:: sdbus_async.networkmanager.NmSettingsInvalidHostnameError

.. autoexception:: sdbus_async.networkmanager.NmSettingsInvalidArgumentsError

VPN plugins errors
------------------


.. autoexception:: sdbus_async.networkmanager.NmVpnPluginFailedError

.. autoexception:: sdbus_async.networkmanager.NmVpnPluginStartingInProgressError

.. autoexception:: sdbus_async.networkmanager.NmVpnPluginAlreadyStartedError

.. autoexception:: sdbus_async.networkmanager.NmVpnPluginStoppingInProgressError

.. autoexception:: sdbus_async.networkmanager.NmVpnPluginAlreadyStoppedError

.. autoexception:: sdbus_async.networkmanager.NmVpnPluginWrongStateError

.. autoexception:: sdbus_async.networkmanager.NmVpnPluginBadArgumentsError

.. autoexception:: sdbus_async.networkmanager.NmVpnPluginLaunchFailedError

.. autoexception:: sdbus_async.networkmanager.NmVpnPluginInvalidConnectionError

.. autoexception:: sdbus_async.networkmanager.NmVpnPluginInteractiveNotSupportedError
