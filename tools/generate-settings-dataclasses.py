#!/usr/bin/env python
# Based on NetworkManager-1.39.2/tools/generate-docs-nm-settings-docs-merge.py
# SPDX-License-Identifier: LGPL-2.1-or-later
import collections
import textwrap
import xml.etree.ElementTree as ElementTree
from argparse import ArgumentParser
from pathlib import Path
from typing import Any, Dict, List, Optional, OrderedDict, Tuple


def dbg(msg: Any) -> None:
    print(f"{msg}")


def write(msg: Any) -> None:
    print(f"{msg}")


dbus_type_name_map = {
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
    # Legacy types:
    "a(ayuay)": "array of legacy IPv6 address struct",
    "a(ayuayu)": "array of legacy IPv6 route struct",
}
dbus_name_type_map = {
    'array of array of uint32': 'aau',
    'array of byte array': 'aay',
    'array of legacy IPv6 address struct': 'a(ayuay)',
    'array of legacy IPv6 route struct': 'a(ayuayu)',
    'array of string': 'as',
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

###############################################################################

# Order of the connection types(settings_classes) in the profile dataclass:
_setting_name_order = [
    "connection",
    "ipv4",
    "ipv6",
    "generic",
    "ethtool",
    "adsl",
    "bluetooth",
    "bond",
    "bond-port",
    "bridge",
    "bridge-port",
    "cdma",
    "dcb",
    "dummy",
    "802-3-ethernet",
    "gsm",
    "hostname",
    "802-1x",
    "infiniband",
    "ip-tunnel",
    "6lowpan",
    "macsec",
    "macvlan",
    "match",
    "802-11-olpc-mesh",
    "ovs-bridge",
    "ovs-dpdk",
    "ovs-external-ids",
    "ovs-interface",
    "ovs-patch",
    "ovs-port",
    "ppp",
    "pppoe",
    "proxy",
    "serial",
    "sriov",
    "tc",
    "team",
    "team-port",
    "tun",
    "user",
    "veth",
    "vlan",
    "vpn",
    "vrf",
    "vxlan",
    "wifi-p2p",
    "wimax",
    "wireguard",
    "802-11-wireless",
    "802-11-wireless-security",
    "wpan",
]

# List of modules for which we must generate an import of typing.List
list_modules = [
    "bridge",
    "bridge_port",
    "dcb",
    "connection",
    "ethernet",
    "ieee802_1x",
    "ipv4",
    "ipv6",
    "match",
    "sriov",
    "tc",
    "team",
    "team_port",
    "user",
    "vlan",
    "vpn",
    "wireguard",
    "wireless",
    "wireless_security",
]

# Order of special properties which must be first because they are not optional
_property_name_order = [
    "connection.id",
    "connection.type",
    "connection.uuid",
]

def _property_name_order_idx(name: str) -> int:
    """Return the sort index for the given connection setting property"""
    try:
        return _property_name_order.index(name)
    except ValueError:
        # Properties not in _property_name_order are sorted last and then by their name
        return len(_property_name_order)


def key_fcn_property_name(n1: str) -> Tuple[int, str]:
    """key function for sorted(), used to sort connection properties"""
    return (_property_name_order_idx(n1), n1)


def _setting_name_order_idx(name: str) -> int:
    """Return the sort index for the given connection type(settings_class)"""
    try:
        return _setting_name_order.index(name)
    except ValueError:
        return len(_setting_name_order)


def key_fcn_setting_name(n1: str) -> Tuple[int, str]:
    """key function for sorted(), used to sort the settings_classes(connection types)"""
    return (_setting_name_order_idx(n1), n1)


def iter_keys_of_dicts(
    dicts: List[Dict[str, Any]], key: Optional[Any] = None, prefix: Optional[str] = ""
) -> List[str]:
    """Return a sorted list of settings_classes or connection properties

    To support sorting the required properites of settings_classes first,
    the settingsname can be passed ad prefix argument to let the key function
    return the correct sort index for the given settingsname property.
    """
    keys = {f'{prefix}{k}' for d in dicts for k in d.keys()}
    return sorted(keys, key=key)


def node_to_dict(node: Any, tag: str, key_attr: str) -> Dict[str, Any]:
    dictionary = collections.OrderedDict()
    if node is not None:
        for n in node.iter(tag):
            k = n.get(key_attr)
            assert k is not None
            dictionary[k] = n
    return dictionary


def node_get_attr(nodes: List[Optional[Any]], name: str) -> Any:
    for n in nodes:
        if n is None:
            continue
        x = n.get(name, None)
        if x:
            return x
    return None


def node_set_attr(
    dst_node: Any, name: str, nodes: List[Optional[Any]]
) -> None:
    x = node_get_attr(nodes, name)
    if x:
        dst_node.set(name, x)


def find_first_not_none(itr: List[Any]) -> Optional[Any]:
    return next((i for i in itr if i is not None), None)


# The code quality of this function is poor(Sourcery says 5%), needs refactoring,
# also see the rework in tools/generate-settings-dataclasses-jinja.py
def main(settings_xml_path: Path) -> None:
    gl_input_files = [settings_xml_path]

    xml_roots = [ElementTree.parse(f).getroot() for f in gl_input_files]
    assert all(root.tag == "nm-setting-docs" for root in xml_roots)
    settings_roots = [node_to_dict(root, "setting", "name")
                      for root in xml_roots]

    root_node = ElementTree.Element("nm-setting-docs")

    # Generate the file header
    license = "SPDX-License-Identifier: LGPL-2.1-or-later"
    script = ("This file was generated by "
              "tools/generate-settings-dataclasses.py")
    header = f"""# {license}\n# {script},
# if possible, please make changes by also updating the script.\n"""
    i = open("sdbus_async/networkmanager/settings/__init__.py", mode="w")
    p = open("sdbus_async/networkmanager/settings/profile.py", mode="r")
    profile_py = open("sdbus_async/networkmanager/settings/profile.py").read()

    # define start and end markers for generating part of settings/profile.py:
    start_string = "# start of the generated list of settings classes\n"
    start_index = profile_py.index(start_string) + len(start_string)
    end_string = "    # end of the generated list of settings classes\n"
    end_index = profile_py.index(end_string)
    p = open("sdbus_async/networkmanager/settings/profile.py", mode="w")

    # write the file headers
    i.write(header)
    p.write(profile_py[:start_index])
    classes = []

    # generate the connection type settings classes:
    for settingname in iter_keys_of_dicts(settings_roots,
                                          key_fcn_setting_name):
        settings = [d.get(settingname) for d in settings_roots]
        properties = [node_to_dict(s, "property", "name") for s in settings]
        if properties == [OrderedDict()]:
            continue
        if settingname in ["tc", "sriov"]:
            continue  # Not supported by this codegen yet(needs Qdiscs and vfs)
        module = settingname.replace('-', '_')
        for prefix in ["6", "802_11_", "802_3_"]:
            if module.startswith(prefix):
                module = module.replace(prefix, "")
                break
        if settingname.startswith("802-1x"):
            module = f"ieee{module}"
        temp = module.split('_') + ["Settings"]
        classname = temp[0].title() + ''.join(ele.title() for ele in temp[1:])
        if classname.startswith("Ieee"):
            classname.replace("Ieee", "IEEE")
        i.write(f"from .{module} import {classname}\n")
        classes.append(classname)
        f = open(f"sdbus_async/networkmanager/settings/{module}.py", mode="w")

        # Generate module type headers with the needed import statements
        f.write(header)
        f.write("from __future__ import annotations\n")
        f.write("from dataclasses import dataclass, field\n")
        f.write("from typing import")
        if module in ["bond", "ethernet", "ovs_external_ids", "vpn", "user"]:
            f.write(" Dict,")
        if module in list_modules:
            f.write(" List,")
        f.write(" Optional\n")
        f.write("from .base import NetworkManagerSettingsMixin\n")
        if settingname.startswith("ipv"):
            f.write("from .datatypes import AddressData, RouteData\n")
        if settingname.startswith("bridge"):
            f.write("from .datatypes import Vlans\n")
        if settingname.startswith("team"):
            f.write("from .datatypes import LinkWatchers\n")
        if settingname == "wireguard":
            f.write("from .datatypes import WireguardPeers as Peers\n")
        f.write("\n\n")

        # Generate the settings_class and it's entry in profile.py:
        setting_node = ElementTree.SubElement(root_node, "setting")
        if module != "connection":
            p.write(f"    {module}: Optional[{classname}] = field(\n")
            p.write(f"        metadata={{'dbus_name': '{settingname}',\n")
            p.write(f"                  'settings_class': {classname}}},\n")
            p.write("        default=None,\n")
            p.write("    )\n")
        f.write("@dataclass\n")
        f.write(f"class {classname}(NetworkManagerSettingsMixin):\n")
        setting_node.set("name", settingname)

        # generate the docstring of the new settings_class
        desc = node_get_attr(settings, "description")
        f.write('    """' + desc + '"""\n\n')

        # Generate the attributes of the settings_class for this profile type:

        for property in iter_keys_of_dicts(properties, key_fcn_property_name, f'{settingname}.'):
            property_name = property[len(settingname)+1:]
            properties_attrs = [p.get(property_name) for p in properties]
            property_node = ElementTree.SubElement(setting_node, "property")
            property_node.set("name", property_name)
            t = node_get_attr(properties_attrs, "type")
            attribute = property_name.replace('-', '_')
            for builtin in ["id", "type"]:
                if attribute == builtin:
                    attribute = f"{module}_{attribute}"

            if not t:
                t = "string"
            if t.startswith("array of legacy"):
                continue
            if t not in dbus_name_type_map:
                print(f"{settingname}.{property_name}: type '{t}' not found")
                ty = t.replace(")", "")[-5:]
                if ty in dbus_name_type_map:
                    t = ty
            if t in ["{sv}'"]:
                t = "{sv}"
            dbustype = dbus_name_type_map[t]
            if dbustype == "aa{sv}":
                default = node_get_attr(properties_attrs, "default")
                inner_cls = (
                    property_name.title(
                    ).replace("-", "").replace("data", "Data")
                )
                f.write(
                    f"    {attribute}: Optional[List[{inner_cls}]] = field(\n")
                f.write(
                    f"        metadata={{'dbus_name': '{property_name}',\n")
                f.write(f"                  'dbus_type': '{dbustype}',\n")
                f.write(
                    f"                  'dbus_inner_class': {inner_cls}}},\n")
                f.write(f"        default={str(default).title()},\n    )\n")
            else:
                attribute_type = dbus_type_name_map[dbustype]
                optional = property not in _property_name_order
                if optional:
                    f.write(f"    {attribute}: Optional[{attribute_type}]")
                else:
                    f.write(f"    {attribute}: {attribute_type}")
                f.write(" = field(\n")
                meta = (f"'dbus_name': '{property_name}', "
                        f"'dbus_type':@'{dbustype}'")
                line = "metadata={" + meta + "},"
                wrapper = textwrap.TextWrapper(
                    width=80,
                    initial_indent="        ",
                    subsequent_indent="                  ",
                )
                lines = wrapper.wrap(text=line)
                for line in lines:
                    f.write(line.replace(":@", ": ") + '\n')
                default = node_get_attr(properties_attrs, "default")
                if default in ["{}", "0", "-1"]:
                    default = "None"
                if optional:
                    f.write(f"        default={str(default).title()},\n")
                f.write("    )\n")

                # Generate docstrings for attributes: Not stored by python,
                # but is parsed for generating documentation and be red by
                # developers when they lookup the attribute declaration:
                generate_descriptions_for_attributes = False
                if generate_descriptions_for_attributes:
                    desc = node_get_attr(properties_attrs, "description")
                    wrapper = textwrap.TextWrapper(
                        width=82,
                        initial_indent="    ",
                        subsequent_indent="    ",
                    )
                    lines = wrapper.wrap(text=f'"""{desc}"""')
                    if len(lines) == 1:
                        print(lines[0] + '"""')
                    else:
                        for line in lines:
                            f.write(f'{line}\n')
                        # If the closing """ shall be on a new line, use:
                        # f.write('    """\n')
                    f.write("")
    i.write('\n__all__ = (\n')
    for cls in classes:
        i.write(f"    '{cls}',\n")
    i.write(")\n")
    p.write(profile_py[end_index:])


if __name__ == '__main__':
    arg_parser = ArgumentParser()
    arg_parser.add_argument(
        'nm_settings_xml',
        type=Path,
        default=Path('man/nm-settings-docs-dbus.xml'),
    )
    args = arg_parser.parse_args()

    main(args.nm_settings_xml)
