from dataclasses import dataclass, field
from typing import Optional

from .base import NetworkManagerSettingsMixin


@dataclass
class AddressData(NetworkManagerSettingsMixin):
    address: str = field(
        metadata={'dbus_name': 'address', 'dbus_type': 's'},
    )
    prefix: int = field(
        metadata={'dbus_name': 'prefix', 'dbus_type': 'u'},
    )


@dataclass
class RouteData(NetworkManagerSettingsMixin):
    dest: str = field(
        metadata={'dbus_name': 'dest', 'dbus_type': 's'},
    )
    prefix: int = field(
        metadata={'dbus_name': 'prefix', 'dbus_type': 'u'},
    )
    next_hop: Optional[str] = field(
        metadata={'dbus_name': 'next-hop', 'dbus_type': 's'},
        default=None,
    )
    metric: Optional[int] = field(
        metadata={'dbus_name': 'metric', 'dbus_type': 'u'},
        default=None,
    )


@dataclass
class LinkWatchers(NetworkManagerSettingsMixin):
    """
    Link watchers configuration for the connection: each link watcher is
    defined by a dictionary, whose keys depend upon the selected link watcher.
    Available link watchers are 'ethtool', 'nsna_ping' and 'arp_ping' and it
    is specified in the dictionary with the key 'name'.
    Available keys are: ethtool: 'delay-up', 'delay-down', 'init-wait';
    nsna_ping: 'init-wait', 'interval', 'missed-max', 'target-host';
    arp_ping: all the ones in nsna_ping and 'source-host', 'validate-active',
    'validate-inactive', 'send-always'. See teamd.conf man for more details
    """
    name: str = field(
        metadata={'dbus_name': 'name', 'dbus_type': 's'},
    )
    delay_up: Optional[int] = field(
        metadata={'dbus_delay-up': 'delay-up', 'dbus_type': 'u'},
        default=None
    )
    delay_down: Optional[int] = field(
        metadata={'dbus_name': 'delay-down', 'dbus_type': 'u'},
        default=None
    )
    init_wait: Optional[int] = field(
        metadata={'dbus_name': 'init-wait', 'dbus_type': 'u'},
        default=None
    )
    interval: Optional[int] = field(
        metadata={'dbus_name': 'interval', 'dbus_type': 'u'},
        default=None
    )
    missed_max: Optional[int] = field(
        metadata={'dbus_name': 'missed-max', 'dbus_type': 'u'},
        default=None
    )
    source_host: Optional[str] = field(
        metadata={'dbus_name': 'source-host', 'dbus_type': 's'},
        default=None
    )
    target_host: Optional[str] = field(
        metadata={'dbus_name': 'target-host', 'dbus_type': 's'},
        default=None
    )
    validate_active: Optional[bool] = field(
        metadata={'dbus_name': 'validate-active', 'dbus_type': 'b'},
        default=None
    )
    validate_inactive: Optional[bool] = field(
        metadata={'dbus_name': 'validate-inactive', 'dbus_type': 'b'},
        default=None
    )
    send_alway: Optional[bool] = field(
        metadata={'dbus_name': 'send-alway', 'dbus_type': 'b'},
        default=None
    )


@dataclass
class Vlans(NetworkManagerSettingsMixin):
    """
    VLAN filtering in linux bridge connection attributes
    For background info, see the development of the merge:
    https://bugzilla.redhat.com/show_bug.cgi?id=1652910
    """
    vid_start: int = field(
        metadata={'dbus_name': 'vid-start', 'dbus_type': 'u'},
    )
    vid_end: int = field(
        metadata={'dbus_name': 'vid-end', 'dbus_type': 'u'},
    )
    pvid: bool = field(
        metadata={'dbus_name': 'pvid', 'dbus_type': 'b'},
    )
    untagged: bool = field(
        metadata={'dbus_name': 'untagged', 'dbus_type': 'b'},
    )
