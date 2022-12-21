# SPDX-License-Identifier: LGPL-2.1-or-later

# Copyright (C) 2022 igo95862

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

from unittest import TestCase
from sdbus_async.networkmanager.settings import ConnectionProfile

connection_dict = {
    'connection': {'id': 'mlvd-wg',
                   'interface-name': 'mlvd-wg',
                   'timestamp': 150000,
                   'type': 'wireguard',
                   'uuid': 'uuid'},
    'ipv4': {'address-data': [{'address': '10.0.0.1', 'prefix': 32}],
             'dns': [150000],
             'dns-search': ['~'],
             'method': 'manual'},
    'ipv6': {'addr-gen-mode': 1,
             'address-data': [{'address': 'fc00:1',
                               'prefix': 128}],
             'method': 'manual'},
    'wireguard': {
        'peers': [
            {'allowed-ips': ['::/0', '0.0.0.0/0'],
             'endpoint': '1.1.1.1:51820',
             'public-key': 'public_key'}]}}

secret_dict = {
    'connection': {},
    'ipv4': {},
    'ipv6': {},
    'proxy': {},
    'wireguard': {
        'peers': [
            {'public-key': 'public_key'}
        ],
        'private-key': 'secret_key'}}


class TestSettingsProfile(TestCase):
    def test_update(self) -> None:
        connection = ConnectionProfile.from_settings_dict(connection_dict)
        secrets = ConnectionProfile.from_settings_dict(secret_dict)

        connection.update(secrets)

        self.assertEqual(connection.wireguard.private_key, 'secret_key')

    def test_update_secrets(self) -> None:
        connection = ConnectionProfile.from_settings_dict(connection_dict)
        secrets = ConnectionProfile.from_settings_dict(secret_dict)

        connection_secret_update_generator = (
            connection.update_secrets_generator()
        )

        setting_name = next(connection_secret_update_generator)
        self.assertEqual(setting_name, 'wireguard')

        with self.assertRaises(StopIteration):
            connection_secret_update_generator.send(secrets)

        self.assertEqual(connection.wireguard.private_key, 'secret_key')
