from typing import Literal, TypedDict


class BanSettings(TypedDict, total=False):
    description: str
    networks: list[str]
    enable_ban: bool
    ban_for_pps: bool
    ban_for_bandwidth: bool
    ban_for_flows: bool
    threshold_pps: int
    threshold_mbps: int
    threshold_flows: int
    ban_for_tcp_bandwidth: bool
    ban_for_tcp_syn_bandwidth: bool
    ban_for_udp_bandwidth: bool
    ban_for_icmp_bandwidth: bool
    ban_for_tcp_pps: bool
    ban_for_tcp_syn_pps: bool
    ban_for_udp_pps: bool
    ban_for_icmp_pps: bool
    threshold_tcp_mbps: int
    threshold_tcp_syn_mbps: int
    threshold_udp_mbps: int
    threshold_icmp_mbps: int
    threshold_tcp_pps: int
    threshold_tcp_syn_pps: int
    threshold_udp_pps: int
    threshold_icmp_pps: int


class BanSettingsRequired(TypedDict):
    name: str
    description: str
    networks: list[str]
    enable_ban: bool
    ban_for_pps: bool
    ban_for_bandwidth: bool
    ban_for_flows: bool
    threshold_pps: int
    threshold_mbps: int
    threshold_flows: int
    ban_for_tcp_bandwidth: bool
    ban_for_tcp_syn_bandwidth: bool
    ban_for_udp_bandwidth: bool
    ban_for_icmp_bandwidth: bool
    ban_for_tcp_pps: bool
    ban_for_tcp_syn_pps: bool
    ban_for_udp_pps: bool
    ban_for_icmp_pps: bool
    threshold_tcp_mbps: int
    threshold_tcp_syn_mbps: int
    threshold_udp_mbps: int
    threshold_icmp_mbps: int
    threshold_tcp_pps: int
    threshold_tcp_syn_pps: int
    threshold_udp_pps: int
    threshold_icmp_pps: int


type HostGroupBoolOptions = Literal[
    "ban_for_pps",
    "ban_for_bandwidth",
    "ban_for_flows",
    "enable_ban",
    "ban_for_tcp_bandwidth",
    "ban_for_tcp_syn_bandwidth",
    "ban_for_udp_bandwidth",
    "ban_for_icmp_bandwidth",
    "ban_for_tcp_pps",
    "ban_for_tcp_syn_pps",
    "ban_for_udp_pps",
    "ban_for_icmp_pps",
]

type HostGroupIntOptions = Literal[
    "threshold_pps",
    "threshold_mbps",
    "threshold_flows",
    "threshold_tcp_mbps",
    "threshold_tcp_syn_mbps",
    "threshold_udp_mbps",
    "threshold_icmp_mbps",
    "threshold_tcp_pps",
    "threshold_tcp_syn_pps",
    "threshold_udp_pps",
    "threshold_icmp_pps",
]

type HostGroupStrOptions = Literal[
    "name",
    "description",
    "networks",
]

type GlobalStrOptions = Literal["networks_list",]

type GlobalIntOptions = Literal[
    "sflow_ports",
    "netflow_ports",
]


class BaseResponse(TypedDict):
    success: bool
    error_text: str


class ArrayResponse[T](BaseResponse):
    values: list[T]


class FlowSpecAction(TypedDict):
    rate: int


class FlowSpecRule(TypedDict, total=False):
    source_prefix: str
    destination_prefix: str
    destination_ports: list[int]
    source_ports: list[int]
    packet_lengths: list[int]
    protocols: list[str]
    fragmentation_flags: list[str]
    tcp_flags: list[str]
    ttls: list[int]
    vlans: list[int]
    action_type: str
    action: FlowSpecAction
    ipv4_nexthops: list[str]


class ThresholdStructure(TypedDict):
    flows: bool
    mbits: bool
    packets: bool


class FlexibleThresholdsDetails(TypedDict):
    incoming: bool
    outgoing: bool
    incoming_details: ThresholdStructure
    outgoing_details: ThresholdStructure


class CallbackAttackDetails(TypedDict):
    attack_uuid: str
    attack_severity: str
    host_group: str
    parent_host_group: str
    host_network: str
    protocol_version: str
    attack_detection_triggered_by_flexible_threshold: bool
    attack_detection_flexible_thresholds: list[str]
    attack_detection_flexible_thresholds_detailed: dict[str, FlexibleThresholdsDetails]
    attack_detection_threshold: str
    attack_detection_threshold_direction: str
    attack_detection_source: str

    total_incoming_traffic: int
    total_outgoing_traffic: int
    total_incoming_pps: int
    total_outgoing_pps: int
    total_incoming_flows: int
    total_outgoing_flows: int

    incoming_ip_fragmented_traffic: int
    outgoing_ip_fragmented_traffic: int
    incoming_ip_fragmented_pps: int
    outgoing_ip_fragmented_pps: int

    incoming_tcp_traffic: int
    outgoing_tcp_traffic: int
    incoming_tcp_pps: int
    outgoing_tcp_pps: int

    incoming_syn_tcp_traffic: int
    outgoing_syn_tcp_traffic: int
    incoming_syn_tcp_pps: int
    outgoing_syn_tcp_pps: int

    incoming_udp_traffic: int
    outgoing_udp_traffic: int
    incoming_udp_pps: int
    outgoing_udp_pps: int

    incoming_icmp_traffic: int
    outgoing_icmp_traffic: int
    incoming_icmp_pps: int
    outgoing_icmp_pps: int


class CallbackPacketDumpEntry(TypedDict):
    ip_version: str
    source_ip: str
    destination_ip: str
    source_port: int
    destination_port: int
    tcp_flags: str
    fragmentation: bool
    packets: int
    length: int
    ip_length: int
    ttl: int
    sample_ratio: int
    protocol: str
    agent_address: str


class CallbackDetails(TypedDict):
    ip: str
    action: Literal["ban", "unban", "attack_status", "partial_block", "partial_unblock"]
    attack_details: CallbackAttackDetails
    alert_scope: Literal["host", "hostgroup"]
    hostgroup_name: str
    parent_hostgroup_name: str
    hostgroup_networks: list[str]
    packet_dump: list[str]
    packet_dump_detailed: list[CallbackPacketDumpEntry]
    flow_spec_rules: list[FlowSpecRule]
