#!/usr/bin/env python
# SPDX-License-Identifier: LGPL-2.1-or-later
from __future__ import print_function
import collections
from typing import Any, Dict, List, OrderedDict, Optional, Tuple
import xml.etree.ElementTree as ElementTree
import textwrap


def dbg(msg: Any) -> None:
    # pass
    print(f"{msg}")


dbus_type_name_map = {
    "b": "bool",
    "s": "str",
    "i": "int",
    "u": "int",
    "t": "int",
    "x": "int",
    "y": "Byte",
    "as": "List[str]",
    "au": "List[int]",
    "ay": "bytes",
    "a{ss}": "Dict[str, str]",
    "a{sv}": "vardict",
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
    'boolean': 'b',
    'byte': 'y',
    'byte array': 'ay',
    'dict of string to string': 'a{ss}',
    'int32': 'i',
    'int64': 'x',
    'string': 's',
    'uint32': 'u',
    'uint64': 't',
    'vardict': 'a{sv}',
}

###############################################################################

_setting_name_order = [
    "connection",
    "ipv4",
    "ipv6",
    "generic",
    "802-3-ethernet",
    "802-11-wireless",
    "802-11-wireless-security",
    "gsm",
    "ethtool",
    "6lowpan",
    "802-1x",
    "adsl",
    "bluetooth",
    "bond",
    "bridge",
    "bridge-port",
    "cdma",
    "dcb",
    "dummy",
    "infiniband",
    "ip-tunnel",
    "macsec",
    "macvlan",
    "match",
    "802-11-olpc-mesh",
    "ovs-bridge",
    "ovs-dpdk",
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
    "vlan",
    "vpn",
    "vrf",
    "vxlan",
    "wifi-p2p",
    "wimax",
    "wireguard",
    "wpan",
]


def _setting_name_order_idx(name: str) -> int:
    try:
        return _setting_name_order.index(name)
    except ValueError:
        return len(_setting_name_order)


def key_fcn_setting_name(n1: str) -> Tuple[int, str]:
    return (_setting_name_order_idx(n1), n1)


def iter_keys_of_dicts(
    dicts: List[Dict[str, Any]], key: Optional[Any] = None
) -> List[str]:
    keys = {k for d in dicts for k in d.keys()}
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


###############################################################################

gl_only_from_first = False
gl_output_xml_file = "out/o"
# gl_input_files = list(argv[1:])

###############################################################################
# gl_input_files = ["src/nmcli/generate-docs-nm-settings-nmcli.xml"]
gl_input_files = ["src/libnm-client-impl/nm-property-infos-dbus.xml"]
# gl_input_files = ["man/nm-settings-docs-nmcli.xml"]
gl_input_files = ["man/nm-settings-docs-dbus.xml"]
for f in gl_input_files:
    dbg(f"# input file {f}")

xml_roots = [ElementTree.parse(f).getroot() for f in gl_input_files]
assert all(root.tag == "nm-setting-docs" for root in xml_roots)
settings_roots = [node_to_dict(root, "setting", "name") for root in xml_roots]

root_node = ElementTree.Element("nm-setting-docs")
print("from typing import Dict, List, Optional")
print("from .settings import NetworkManagerSettingsMixin")
print("")
print("")
for setting_name in iter_keys_of_dicts(settings_roots, key_fcn_setting_name):
    # print(setting_name)
    # if setting_name != "ipv4":
    #     continue

    settings = [d.get(setting_name) for d in settings_roots]
    properties = [node_to_dict(s, "property", "name") for s in settings]
    if properties == [OrderedDict()]:
        continue
    setting_node = ElementTree.SubElement(root_node, "setting")
    c = setting_name.replace('-', '_').title() + "Settings"
    if setting_name == "802-3-ethernet":
        c = "Ethernet"
    print(f"    {setting_name.replace('802-3-', '')}: Optional[{c}] = field(")
    print(f"        metadata={{'dbus_name': '{setting_name}',")
    print(f"                  'settings_class': {c}}},")
    print("        default=None,")
    print("    )")
    print("")
    dbg("@dataclass")
    dbg(f"class {c}(NetworkManagerSettingsMixin):")
    setting_node.set("name", setting_name)
    desc = node_get_attr(settings, "description")
    print('    """' + desc + '"""')
    print("")
    # node_set_attr(setting_node, "alias", settings)
    for property_name in iter_keys_of_dicts(properties):
        properties_attrs = [p.get(property_name) for p in properties]
        property_node = ElementTree.SubElement(setting_node, "property")
        property_node.set("name", property_name)
        t = node_get_attr(properties_attrs, "type")
        attribute = property_name.replace('-', '_')
        print(f"t: '{t}'")

        if not t:
            t = "string"
        if t.startswith("array of legacy"):
            print("    # Deprecated - TODO: ignore")
            continue
        if t not in dbus_name_type_map:
            print(f"    # {setting_name}.{property_name} type [{t}] not found")
            ty = t.replace(")", "")[-5:]
            if ty in dbus_name_type_map:
                t = ty
        if t in ["{sv}'"]:
            t = "{sv}"
        if t in ["array of 'a{sv}'"]:
            if f"{setting_name}.{property_name}" == "wireguard.peers":
                print("# Has special class in settings.py")
            continue
        dbustype = dbus_name_type_map[t]
        if t == "array of vardict":
            default = node_get_attr(properties_attrs, "default")
            inner_class = (
                property_name.title().replace("-", "").replace("data", "Data")
            )
            print(f"    {attribute}: Optional[List[{inner_class}]] = field(")
            print(f"        metadata={{'dbus_name': '{property_name}',")
            print(f"                  'dbus_type': '{dbustype}',")
            print(f"                  'dbus_inner_class': {inner_class}}},")
            print(f"        default={str(default).title()},")
            print("    )")
        else:
            attribute_type = dbus_type_name_map[dbustype]
            print(f"    {attribute}: Optional[{attribute_type}] = field(")
            meta = f"'dbus_name': '{property_name}', 'dbus_type':@'{dbustype}'"
            line = "metadata={" + meta + "},"
            wrapper = textwrap.TextWrapper(
                width=80,
                initial_indent="        ",
                subsequent_indent="                  ",
            )
            word_list = wrapper.wrap(text=line)
            for element in word_list:
                print(element.replace(":@", ": "))
            default = node_get_attr(properties_attrs, "default")
            if default in ["{}", "0", "-1"]:
                default = "None"
            print(f"        default={str(default).title()},")
            print("    )")
            if setting_name != "ipv4":
                desc = node_get_attr(properties_attrs, "description")
                wrapper = textwrap.TextWrapper(
                    width=74, initial_indent="    ", subsequent_indent="    "
                )
                word_list = wrapper.wrap(text=f'"""{desc}')
                if len(word_list) == 1:
                    print(word_list[0] + '"""')
                else:
                    for element in word_list:
                        print(element)
                    print('    """')
                print("")
        # node_set_attr(property_node, "alias", properties_attrs)
    print("")

# ElementTree.ElementTree(root_node).write(gl_output_xml_file)
