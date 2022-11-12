#!/usr/bin/env python
# SPDX-License-Identifier: LGPL-2.1-or-later

# Gerating nm-settings-docs-dbus.xml from NetworkManager source code
# 1. meson setup \
#       -Dselinux=false \
#       -Dqt=false \
#       -Dintrospection=true \
#       -Ddocs=true \
#       build
# 2. cd build
# 3. ninja man/nm-settings-docs-dbus.xml
from __future__ import annotations

import builtins
import keyword
from argparse import ArgumentParser
from functools import cached_property
from itertools import dropwhile
from pathlib import Path
from re import Pattern
from re import compile as regex_compile
from textwrap import fill
from typing import List, Optional
from xml.etree.ElementTree import Element, parse

from jinja2 import Environment, FileSystemLoader

dbus_to_python_extra_typing_imports = {
    "as": ("List", ),
    "au": ("List", ),
    "a{ss}": ("Dict", ),
    "aa{sv}": ("List", "Tuple", "Any"),
    "aau": ("List", ),
    "aay": ("List", )
}

dbus_to_python_type_map = {
    "b": "bool",
    "s": "str",
    "i": "int",
    "u": "int",
    "t": "int",
    "x": "int",
    "y": "int",
    "as": "List[str]",
    "au": "List[int]",
    "ay": "bytes",
    "a{ss}": "Dict[str, str]",
    "aa{sv}": "List[Tuple[str, Any]]",
    "aau": "List[List[int]]",
    "aay": "List[bytes]",
}

dbus_name_type_map = {
    'array of array of uint32': 'aau',
    'array of byte array': 'aay',
    'array of legacy IPv6 address struct': 'a(ayuay)',
    'array of legacy IPv6 address struct (a(ayuay))': 'a(ayuay)',
    'array of legacy IPv6 route struct': 'a(ayuayu)',
    'array of legacy IPv6 route struct (a(ayuayu))': 'a(ayuayu)',
    'array of string': 'as',
    'array of strings': 'as',
    'array of uint32': 'au',
    'array of vardict': 'aa{sv}',
    "array of 'a{sv}'": 'aa{sv}',  # wireguard.peers uses this, fix NM upstream
    'boolean': 'b',
    'byte': 'y',
    'byte array': 'ay',
    'dict of string to string': 'a{ss}',
    'int32': 'i',
    'int64': 'x',
    'string': 's',
    'uint32': 'u',
    'uint64': 't',
}

python_name_replacements = {
    'type': 'connection_type',
    'id': 'pretty_id',
}


array_of_vardicts_python_classes: dict[str, str] = {
    'peers': 'WireguardPeers',
    'vlans': 'Vlans',
    'address-data': 'AddressData',
    'route-data': 'RouteData',
    'routing-rules': 'RoutingRules',
    'vfs': 'Vfs',
    'qdiscs': 'Qdiscs',
    'tfilters': 'Tfilters',
    'link-watchers': 'LinkWatchers',
}

setting_name_replacement: dict[str, str] = {
    'x': 'eapol',
}


def must_replace_name(name: str) -> bool:
    return (keyword.iskeyword(name)
            or keyword.issoftkeyword(name)
            or hasattr(builtins, name))


class NmSettingPropertyIntrospection:
    def __init__(self, name: str,
                 description: str,
                 name_upper: str,
                 dbus_type: str,
                 parent: NmSettingsIntrospection,
                 default: Optional[str] = None,
                 ) -> None:
        self.name = name
        self.description = description
        self.name_upper = name_upper
        self.python_name = name_upper.lower()
        self.dbus_type = dbus_type
        self.default = default

        if must_replace_name(self.python_name):
            self.python_name = (f"{parent.name_upper.lower()}"
                                f"_{self.python_name}")

        extra_typing = dbus_to_python_extra_typing_imports.get(dbus_type)
        if extra_typing is not None:
            parent.typing_imports.update(extra_typing)

    @cached_property
    def python_type(self) -> str:
        if self.dbus_type == 'aa{sv}':
            return f"List[{array_of_vardicts_python_classes[self.name]}]"

        return dbus_to_python_type_map[self.dbus_type]

    @cached_property
    def python_inner_class(self) -> Optional[str]:
        return array_of_vardicts_python_classes.get(self.name)


class NmSettingsIntrospection:
    def __init__(self, name: str, description: str, name_upper: str,
                 ) -> None:
        self.name = name
        self.description = description
        self.name_upper = name_upper

        self.typing_imports = {'Optional'}

        self.properties: List[NmSettingPropertyIntrospection] = []

    @cached_property
    def python_class_name(self) -> str:

        camel_case = ''.join(
            map(str.title, self.snake_name.split('_'))
        )

        return camel_case + 'Settings'

    @cached_property
    def snake_name(self) -> str:
        underscore_name = self.name.replace('-', '_')

        no_first_digits_name = ''.join(
            dropwhile(
                lambda s: not str.isalpha(s), underscore_name))

        return setting_name_replacement.get(
            no_first_digits_name,
            no_first_digits_name,
        )

    @cached_property
    def datatypes_imports(self) -> list[str]:
        datatypes_found: list[str] = []
        for x in self.properties:
            if (datatype := x.python_inner_class) is not None:
                datatypes_found.append(datatype)

        return datatypes_found


def extract_docbook_paragraphs(docbook_node: Element) -> List[str]:
    return [x.text for x in docbook_node]


def extract_description_paragraph(description_node: Element) -> str:
    return description_node.text


def extract_and_format_option_description(node: Element) -> str:
    formatted_paragraphs: list[str] = []
    paragraphs: list[str] = []
    description = 'Not documented'

    for doc_node in node:
        if doc_node.tag == 'description-docbook':
            paragraphs.extend(extract_docbook_paragraphs(doc_node))
        elif doc_node.tag == 'description':
            description = extract_description_paragraph(doc_node)
        elif doc_node.tag == 'deprecated':
            ...
        elif doc_node.tag == 'deprecated-docbook':
            ...
        else:
            raise ValueError("Unknown doc node", doc_node.tag)

    if paragraphs:
        first_para = paragraphs.pop(0)
    else:
        first_para = description

    formatted_paragraphs.append(
        fill(
            first_para,
            width=72,
            subsequent_indent='    ',
        )
    )
    for para in paragraphs:
        formatted_paragraphs.append(
            fill(
                para,
                width=72,
                initial_indent='    ',
                subsequent_indent='    ',
            )
        )

    return '\n\n'.join(formatted_paragraphs)


def convert_property(node: Element,
                     parent: NmSettingsIntrospection
                     ) -> Optional[NmSettingPropertyIntrospection]:
    options = node.attrib.copy()

    try:
        unconverted_type = options.pop('type')
    except KeyError:
        return None

    try:
        dbus_type = dbus_name_type_map[unconverted_type]
    except KeyError:
        dbus_type = dbus_name_type_map[unconverted_type.split('(')[1][:-1]]

    options['dbus_type'] = dbus_type
    options['description'] = extract_and_format_option_description(node)

    new_property = NmSettingPropertyIntrospection(**options, parent=parent)

    try:
        new_property.python_type
    except KeyError:
        return None

    return new_property


def generate_introspection(root: Element) -> List[NmSettingsIntrospection]:
    settings_introspection: List[NmSettingsIntrospection] = []
    for setting_node in root:
        setting = NmSettingsIntrospection(**setting_node.attrib)

        for x in setting_node:
            new_property = convert_property(x, setting)
            if new_property is not None:
                setting.properties.append(new_property)

        settings_introspection.append(setting)

    return settings_introspection


def main(
        settings_xml_path: Path,
        settings_regex_filter: Optional[Pattern] = None,
) -> None:
    jinja_env = Environment(
        loader=FileSystemLoader(Path('./tools/jinja_templates/')),
    )
    settings_template = jinja_env.get_template('setting.py.jinja2')

    tree = parse(settings_xml_path)
    all_settings = sorted(
        generate_introspection(tree.getroot()),
        key=lambda x: x.snake_name,
    )

    settings_dir = Path('./sdbus_async/networkmanager/settings/')
    for setting in all_settings:

        if settings_regex_filter is not None:
            if not settings_regex_filter.match(setting.snake_name):
                continue

        setting_py_file = settings_dir / (setting.snake_name + '.py')
        with open(setting_py_file, mode='w') as f:
            f.write(settings_template.render(setting=setting))

    profile_template = jinja_env.get_template('profile.py.jinja2')
    with open(settings_dir / 'profile.py', mode='w') as f:
        f.write(profile_template.render(all_settings=all_settings))

    init_template = jinja_env.get_template('__init__.py.jinja2')
    with open(settings_dir / '__init__.py', mode='w') as f:
        f.write(init_template.render(all_settings=all_settings))


if __name__ == '__main__':
    arg_parser = ArgumentParser()
    arg_parser.add_argument(
        'settings_xml_path',
        type=Path,
        default=Path('./nm-settings-docs-dbus.xml'),
    )
    arg_parser.add_argument(
        '--settings-regex-filter',
        type=regex_compile,
    )

    args = arg_parser.parse_args()

    main(**vars(args))
