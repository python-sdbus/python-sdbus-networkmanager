Examples
==================

Listing interfaces
------------------

List interface and their IPv4 adress using
blocking API:

.. code-block:: python

    from sdbus_block.networkmanager import (
        NetworkManager,
        NetworkDeviceGeneric,
        IPv4Config,
    )
    from sdbus import sd_bus_open_system

    system_bus = sd_bus_open_system()  # We need system bus

    nm = NetworkManager(system_bus)

    devices_paths = nm.get_devices()

    for device_path in devices_paths:
        generic_device = NetworkDeviceGeneric(device_path, system_bus)
        print('Device: ', generic_device.interface)
        device_ip4_conf_path = generic_device.ip4_config
        if device_ip4_conf_path == '/':
            # This is how NetworkManager indicates there is no ip config
            # for the interface
            continue
        else:
            ip4_conf = IPv4Config(device_ip4_conf_path, system_bus)
            for address_data in ip4_conf.address_data:
                print('     Ip Adress:', address_data['address'][1])

Same but using async API:

.. code-block:: python

    from sdbus_async.networkmanager import (
        NetworkManager,
        NetworkDeviceGeneric,
        IPv4Config,
    )
    from sdbus import sd_bus_open_system
    from asyncio import run as async_run

    system_bus = sd_bus_open_system()  # We need system bus

    nm = NetworkManager(system_bus)


    async def test() -> None:
        devices_paths = await nm.get_devices()
        for device_path in devices_paths:
            generic_device = NetworkDeviceGeneric(device_path, system_bus)
            print('Device: ', await generic_device.interface)
            device_ip4_conf_path = await generic_device.ip4_config
            if device_ip4_conf_path == '/':
                # This is how NetworkManager indicates there is no ip config
                # for the interface
                continue
            else:
                ip4_conf = IPv4Config(device_ip4_conf_path, system_bus)
                for address_data in await ip4_conf.address_data:
                    print('     Ip Adress:', address_data['address'][1])

    async_run(test())
