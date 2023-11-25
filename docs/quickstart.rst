NetworkManager D-Bus API quickstart
===================================

This is a tutorial to understand the structure of the NetworkManager
D-Bus API and how to use it.

.. note::

  NetworkManager usually uses the system D-Bus, however, sdbus uses the session
  D-Bus by default. It is recommend to call ``sdbus.set_default_bus(sdbus.sd_bus_open_system())``
  to set the system bus as default bus.

NetworkManager main object
--------------------------

This is a static object that contains information about
entire state of NetworkManager. The Python class
:py:class:`NetworkManager <sdbus_async.networkmanager.NetworkManager>`
has a predefined service name and object path.

.. code-block:: python

  import sdbus
  from sdbus_block.networkmanager import NetworkManager

  sdbus.set_default_bus(sdbus.sd_bus_open_system())
  network_manager = NetworkManager()

Devices
-------

Every device object represents a network device. Device object has a generic
methods and properties that are universal across all device types and
a type specific methods. The :py:class:`NetworkDeviceGeneric
<sdbus_async.networkmanager.NetworkDeviceGeneric>` implements generic methods
and, for example, :py:class:`NetworkDeviceWireless <sdbus_async.networkmanager.NetworkDeviceWireless>`
adds Wi-Fi specific methods.

The :py:attr:`device_type <sdbus_async.networkmanager.NetworkManagerDeviceInterfaceAsync.device_type>`
property and enum :py:class:`DeviceType <sdbus_async.networkmanager.enums.DeviceType>`
can be used to determine particular type of a device.

.. code-block:: python

  from sdbus_block.networkmanager import NetworkDeviceGeneric, NetworkDeviceWireless
  from sdbus_block.networkmanager.enums import DeviceType

  all_devices = {path: NetworkDeviceGeneric(path) for path in network_manager.devices}

  wifi_devices = [
      NetworkDeviceWireless(path)
      for path, device in all_devices.items()
      if device.device_type == DeviceType.WIFI
  ]

Connection
----------

Connection represents a configuration containing an IP address, Wifi password,
proxy settings and etc... The main object to access connections is the
:py:class:`NetworkManagerSettings <sdbus_async.networkmanager.NetworkManagerSettings>`
which has predefined object path.

Each individual connection has a separate path which can be accessed with
:py:class:`NetworkConnectionSettings <sdbus_async.networkmanager.NetworkConnectionSettings>`
class.

.. code-block:: python

  from sdbus_block.networkmanager import NetworkManagerSettings

  networwork_manager_settings = NetworkManagerSettings()

  all_connections = [NetworkConnectionSettings(x) for x in networwork_manager_settings.connections]

The actual connection settings are represented by a complex double nested dictionary
of D-Bus variants. For convenience a `dataclass <https://docs.python.org/3/library/dataclasses.html>`_
based helper is provided.

The :py:meth:`get_profile <sdbus_async.networkmanager.NetworkManagerSettingsConnectionInterfaceAsync.get_profile>`
and :py:meth:`update_profile <sdbus_async.networkmanager.NetworkManagerSettingsConnectionInterfaceAsync.update_profile>`
are two main methods to interact with connection settings helper.

.. code-block:: python

  connection = all_connections[0]
  setting_dataclass = connection.get_profile()
  print("uuid:", profile.connection.uuid)

Active Connection
-----------------

:py:class:`ActiveConnection <sdbus_async.networkmanager.ActiveConnection>`
is a product of a Connection being applied to a Device.

For example, :py:meth:`activate_connection <sdbus_async.networkmanager.NetworkManagerInterfaceAsync.activate_connection>`
of the main NetworkManager object will create new Active Connection
(therefore configuring network on a device) and return its path.
The :py:meth:`deactivate_connection <sdbus_async.networkmanager.NetworkManagerInterfaceAsync.deactivate_connection>`
will remove the active connection and remove the device's network configuration.
