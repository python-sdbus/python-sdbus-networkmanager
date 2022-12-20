# SPDX-License-Identifier: LGPL-2.1-or-later
# This file was generated by tools/generate-settings-dataclasses-jinja.py,
# if possible, please make changes by also updating the script.
from __future__ import annotations
from dataclasses import dataclass, field
from typing import ClassVar, List, Optional
from .base import NetworkManagerSettingsMixin


@dataclass
class DcbSettings(NetworkManagerSettingsMixin):
    """Data Center Bridging Settings"""
    secret_fields_names: ClassVar[List[str]] = ['priority_flow_control']
    secret_name = 'dcb'

    app_fcoe_flags: Optional[int] = field(
        metadata={
            'dbus_name': 'app-fcoe-flags',
            'dbus_type': 'u',
        },
        default=None,
    )
    """Specifies the NMSettingDcbFlags for the DCB FCoE application.  Flags may
    be any combination of NM_SETTING_DCB_FLAG_ENABLE (0x1),
    NM_SETTING_DCB_FLAG_ADVERTISE (0x2), and NM_SETTING_DCB_FLAG_WILLING
    (0x4)."""
    app_fcoe_mode: Optional[str] = field(
        metadata={
            'dbus_name': 'app-fcoe-mode',
            'dbus_type': 's',
        },
        default=None,
    )
    """The FCoE controller mode; either "fabric" or "vn2vn".

    Since 1.34, NULL is the default and means "fabric". Before 1.34,
    NULL was rejected as invalid and the default was "fabric"."""
    app_fcoe_priority: Optional[int] = field(
        metadata={
            'dbus_name': 'app-fcoe-priority',
            'dbus_type': 'i',
        },
        default=None,
    )
    """The highest User Priority (0 - 7) which FCoE frames should use, or -1
    for default priority.  Only used when the "app-fcoe-flags" property
    includes the NM_SETTING_DCB_FLAG_ENABLE (0x1) flag."""
    app_fip_flags: Optional[int] = field(
        metadata={
            'dbus_name': 'app-fip-flags',
            'dbus_type': 'u',
        },
        default=None,
    )
    """Specifies the NMSettingDcbFlags for the DCB FIP application.  Flags may
    be any combination of NM_SETTING_DCB_FLAG_ENABLE (0x1),
    NM_SETTING_DCB_FLAG_ADVERTISE (0x2), and NM_SETTING_DCB_FLAG_WILLING
    (0x4)."""
    app_fip_priority: Optional[int] = field(
        metadata={
            'dbus_name': 'app-fip-priority',
            'dbus_type': 'i',
        },
        default=None,
    )
    """The highest User Priority (0 - 7) which FIP frames should use, or -1 for
    default priority.  Only used when the "app-fip-flags" property
    includes the NM_SETTING_DCB_FLAG_ENABLE (0x1) flag."""
    app_iscsi_flags: Optional[int] = field(
        metadata={
            'dbus_name': 'app-iscsi-flags',
            'dbus_type': 'u',
        },
        default=None,
    )
    """Specifies the NMSettingDcbFlags for the DCB iSCSI application.  Flags
    may be any combination of NM_SETTING_DCB_FLAG_ENABLE (0x1),
    NM_SETTING_DCB_FLAG_ADVERTISE (0x2), and NM_SETTING_DCB_FLAG_WILLING
    (0x4)."""
    app_iscsi_priority: Optional[int] = field(
        metadata={
            'dbus_name': 'app-iscsi-priority',
            'dbus_type': 'i',
        },
        default=None,
    )
    """The highest User Priority (0 - 7) which iSCSI frames should use, or -1
    for default priority. Only used when the "app-iscsi-flags" property
    includes the NM_SETTING_DCB_FLAG_ENABLE (0x1) flag."""
    priority_bandwidth: Optional[List[int]] = field(
        metadata={
            'dbus_name': 'priority-bandwidth',
            'dbus_type': 'au',
        },
        default=None,
    )
    """An array of 8 uint values, where the array index corresponds to the User
    Priority (0 - 7) and the value indicates the percentage of bandwidth
    of the priority's assigned group that the priority may use.  The sum
    of all percentages for priorities which belong to the same group
    must total 100 percents."""
    priority_flow_control: Optional[List[int]] = field(
        metadata={
            'dbus_name': 'priority-flow-control',
            'dbus_type': 'au',
        },
        default=None,
    )
    """An array of 8 boolean values, where the array index corresponds to the
    User Priority (0 - 7) and the value indicates whether or not the
    corresponding priority should transmit priority pause."""
    priority_flow_control_flags: Optional[int] = field(
        metadata={
            'dbus_name': 'priority-flow-control-flags',
            'dbus_type': 'u',
        },
        default=None,
    )
    """Specifies the NMSettingDcbFlags for DCB Priority Flow Control (PFC).
    Flags may be any combination of NM_SETTING_DCB_FLAG_ENABLE (0x1),
    NM_SETTING_DCB_FLAG_ADVERTISE (0x2), and NM_SETTING_DCB_FLAG_WILLING
    (0x4)."""
    priority_group_bandwidth: Optional[List[int]] = field(
        metadata={
            'dbus_name': 'priority-group-bandwidth',
            'dbus_type': 'au',
        },
        default=None,
    )
    """An array of 8 uint values, where the array index corresponds to the
    Priority Group ID (0 - 7) and the value indicates the percentage of
    link bandwidth allocated to that group.  Allowed values are 0 - 100,
    and the sum of all values must total 100 percents."""
    priority_group_flags: Optional[int] = field(
        metadata={
            'dbus_name': 'priority-group-flags',
            'dbus_type': 'u',
        },
        default=None,
    )
    """Specifies the NMSettingDcbFlags for DCB Priority Groups.  Flags may be
    any combination of NM_SETTING_DCB_FLAG_ENABLE (0x1),
    NM_SETTING_DCB_FLAG_ADVERTISE (0x2), and NM_SETTING_DCB_FLAG_WILLING
    (0x4)."""
    priority_group_id: Optional[List[int]] = field(
        metadata={
            'dbus_name': 'priority-group-id',
            'dbus_type': 'au',
        },
        default=None,
    )
    """An array of 8 uint values, where the array index corresponds to the User
    Priority (0 - 7) and the value indicates the Priority Group ID.
    Allowed Priority Group ID values are 0 - 7 or 15 for the
    unrestricted group."""
    priority_strict_bandwidth: Optional[List[int]] = field(
        metadata={
            'dbus_name': 'priority-strict-bandwidth',
            'dbus_type': 'au',
        },
        default=None,
    )
    """An array of 8 boolean values, where the array index corresponds to the
    User Priority (0 - 7) and the value indicates whether or not the
    priority may use all of the bandwidth allocated to its assigned
    group."""
    priority_traffic_class: Optional[List[int]] = field(
        metadata={
            'dbus_name': 'priority-traffic-class',
            'dbus_type': 'au',
        },
        default=None,
    )
    """An array of 8 uint values, where the array index corresponds to the User
    Priority (0 - 7) and the value indicates the traffic class (0 - 7)
    to which the priority is mapped."""
