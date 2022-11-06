from dataclasses import dataclass, field
from typing import List, Optional

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


@dataclass
class WireguardPeers(NetworkManagerSettingsMixin):
    public_key: str = field(
        metadata={'dbus_name': 'public-key', 'dbus_type': 's'},
    )
    endpoint: int = field(
        metadata={'dbus_name': 'endpoint', 'dbus_type': 's'},
    )
    allowed_ips: List[str] = field(
        metadata={'dbus_name': 'allowed-ips', 'dbus_type': 'as'},
    )


@dataclass
class RoutingRules(NetworkManagerSettingsMixin):
    action: Optional[int] = field(
        metadata={'dbus_name': 'action', 'dbus_type': 'y'},
    )
    dport_end: Optional[int] = field(
        metadata={'dbus_name': 'dport-end', 'dbus_type': 'q'},
    )
    dport_start: Optional[int] = field(
        metadata={'dbus_name': 'dport-start', 'dbus_type': 'q'},
    )
    family: Optional[int] = field(
        metadata={'dbus_name': 'family', 'dbus_type': 'i'},
    )
    from_prefix: Optional[str] = field(
        metadata={'dbus_name': 'from', 'dbus_type': 's'},
    )
    from_len: Optional[int] = field(
        metadata={'dbus_name': 'from-len', 'dbus_type': 'y'},
    )
    fwmark: Optional[int] = field(
        metadata={'dbus_name': 'fwmark', 'dbus_type': 'u'},
    )
    fwmask: Optional[int] = field(
        metadata={'dbus_name': 'fwmask', 'dbus_type': 'u'},
    )
    iifname: Optional[str] = field(
        metadata={'dbus_name': 'iifname', 'dbus_type': 's'},
    )
    invert: Optional[bool] = field(
        metadata={'dbus_name': 'invert', 'dbus_type': 'b'},
    )
    ipproto: Optional[str] = field(
        metadata={'dbus_name': 'ipproto', 'dbus_type': 's'},
    )
    oifname: Optional[str] = field(
        metadata={'dbus_name': 'oifname', 'dbus_type': 's'},
    )
    priority: Optional[int] = field(
        metadata={'dbus_name': 'priority', 'dbus_type': 'u'},
    )
    sport_end: Optional[int] = field(
        metadata={'dbus_name': 'sport-end', 'dbus_type': 'q'},
    )
    sport_start: Optional[int] = field(
        metadata={'dbus_name': 'sport-start', 'dbus_type': 'q'},
    )
    supress_prefixlength: Optional[int] = field(
        metadata={'dbus_name': 'supress-prefixlength', 'dbus_type': 'i'},
    )
    table: Optional[int] = field(
        metadata={'dbus_name': 'table', 'dbus_type': 'u'},
    )
    to: Optional[str] = field(
        metadata={'dbus_name': 'to', 'dbus_type': 's'},
    )
    tos: Optional[int] = field(
        metadata={'dbus_name': 'tos', 'dbus_type': 'y'},
    )
    to_len: Optional[int] = field(
        metadata={'dbus_name': 'to-len', 'dbus_type': 'y'},
    )
    range_end: Optional[int] = field(
        metadata={'dbus_name': 'range-end', 'dbus_type': 'u'},
    )
    range_start: Optional[int] = field(
        metadata={'dbus_name': 'range-start', 'dbus_type': 'u'},
    )


@dataclass
class Vfs(NetworkManagerSettingsMixin):
    index: str = field(
        metadata={'dbus_name': 'index', 'dbus_type': 's'},
    )
    mac: Optional[str] = field(
        metadata={'dbus_name': 'mac', 'dbus_type': 's'},
    )
    spoof_check: Optional[str] = field(
        metadata={'dbus_name': 'spoof-check', 'dbus_type': 's'},
    )
    trust: Optional[str] = field(
        metadata={'dbus_name': 'trust', 'dbus_type': 's'},
    )
    min_tx_rate: Optional[str] = field(
        metadata={'dbus_name': 'min-tx-rate', 'dbus_type': 's'},
    )
    max_tx_rate: Optional[str] = field(
        metadata={'dbus_name': 'max-tx-rate', 'dbus_type': 's'},
    )
    vlans: Optional[str] = field(
        metadata={'dbus_name': 'vlans', 'dbus_type': 's'},
    )


@dataclass
class Qdiscs(NetworkManagerSettingsMixin):
    ...


@dataclass
class Tfilters(NetworkManagerSettingsMixin):
    ...
