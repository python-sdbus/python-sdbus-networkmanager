from __future__ import annotations
from dataclasses import fields
from functools import lru_cache
from typing import Any, Dict, Type, cast

from ..types import (
    NetworkManagerSettingsDomain,
)


class NetworkManagerSettingsMixin:
    def to_dbus(self) -> NetworkManagerSettingsDomain:
        """TODO: Add proper docstring"""
        new_dict: NetworkManagerSettingsDomain = {}

        for x in fields(self):
            value = getattr(self, x.name)
            if value is None:
                continue

            if x.metadata['dbus_type'] == 'aa{sv}':
                packed_variant = ('aa{sv}', [x.to_dbus() for x in value])
            else:
                packed_variant = (x.metadata['dbus_type'], value)

            new_dict[x.metadata['dbus_name']] = packed_variant

        return new_dict

    @classmethod
    def _unpack_variant(cls, key: str, signature: str, value: Any) -> Any:
        if signature == 'aa{sv}':
            inner_class = cls.setting_name_to_inner_class(key)
            return [inner_class.from_dbus(x) for x in value]

        return value

    @classmethod
    def from_dbus(
        cls,
        dbus_dict: NetworkManagerSettingsDomain,
    ) -> NetworkManagerSettingsMixin:
        """TODO: Add proper docstring"""
        reverse_mapping = cls.setting_name_reverse_mapping()
        unvarianted_options = {
            reverse_mapping[k]: cls._unpack_variant(k, *v)
            for k, v in dbus_dict.items()
        }
        return cls(**unvarianted_options)

    @classmethod
    def from_dict(cls,
                  plain_dict: Dict[str, Any]
                  ) -> NetworkManagerSettingsMixin:
        options = {}
        for dataclass_field in fields(cls):
            dbus_name = dataclass_field.metadata["dbus_name"]
            if dbus_name in plain_dict:
                value = plain_dict[dbus_name]
                if dataclass_field.metadata["dbus_type"] == 'aa{sv}':
                    inner_class = cls.setting_name_to_inner_class(dbus_name)
                    value = [inner_class.from_dict(item) for item in value]
                options[dataclass_field.name] = value
        return cls(**options)

    @classmethod
    @lru_cache(maxsize=None)
    def setting_name_reverse_mapping(cls) -> Dict[str, str]:
        return {f.metadata['dbus_name']: f.name for f in fields(cls)}

    @classmethod
    @lru_cache(maxsize=None)
    def setting_name_to_inner_class(cls, setting_name: str) -> Type[Any]:
        for x in fields(cls):
            if setting_name != x.metadata['dbus_name']:
                continue
            return cast(Type[Any], x.metadata['dbus_inner_class'])

        raise ValueError('Inner class not found')
