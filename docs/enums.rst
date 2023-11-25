Enums
================

Python's Enum quick intro
-------------------------

There are two types of enums. ``IntEnum`` is used for a discrete values
and ``IntFlag`` is used for bit flags. For example, :py:class:`DeviceType <sdbus_async.networkmanager.enums.DeviceType>`
identifies a single device type as a device cannot be of multiple types.
:py:class:`WifiCapabilitiesFlags <sdbus_async.networkmanager.enums.WifiCapabilitiesFlags>`
shows a particular Wifi device capabilities which it can have multiple, for example, supporting
both 5GHz and 2.4GHz radio bands.

Usually ``IntEnum`` is implied unless the enum's name ends with ``Flag``.

Example code using enums:

.. code-block:: python

   from sdbus_async.networkmanager.enums import DeviceType, WifiCapabilitiesFlags

   # Get particular device type from an integer
   DeviceType(2) == DeviceType.WIFI
   # Returns: True

   # Check if a specific flag is enabled
   WifiCapabilitiesFlags.FREQ_2GHZ in WifiCapabilitiesFlags(0x00000400 | 0x00000200)
   # Returns: True

   # Iterate over all enabled flags
   list(WifiCapabilitiesFlags(0x00000400 | 0x00000200))
   # Returns: [<WifiCapabilitiesFlags.FREQ_2GHZ: 512>, <WifiCapabilitiesFlags.FREQ_5GHZ: 1024>]

`See Python's standard library documentation for more detailed
tutorial and API reference. <https://docs.python.org/3/library/enum.html>`_

NetworkManager's enums
-------------------------

.. automodule:: sdbus_async.networkmanager.enums
   :members:

Helper classes
-----------------------

.. py:data:: DEVICE_TYPE_TO_CLASS
    :type: Dict[int, class]

    Mapping of NetworkManager device type int to the class.
