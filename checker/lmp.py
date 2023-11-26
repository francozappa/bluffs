"""
lmp.py

"""

# NOTE: https://github.com/pauloborges/bluez/blob/master/monitor/lmp.c
LMP_OPCODES = {
    1: "LMP_name_req",
    2: "LMP_name_res",
    3: "LMP_accepted",
    4: "LMP_not_accepted",
    5: "LMP_clkoffset_req",
    6: "LMP_clkoffset_res",
    7: "LMP_detach",
    8: "LMP_in_rand",
    9: "LMP_comb_key",
    10: "LMP_unit_key",
    11: "LMP_au_rand",
    12: "LMP_sres",
    13: "LMP_temp_rand",
    14: "LMP_temp_key",
    15: "LMP_encryption_mode_req",
    16: "LMP_encryption_key_size_req",
    17: "LMP_start_encryption_req",
    18: "LMP_stop_encryption_req",
    19: "LMP_switch_req",
    20: "LMP_hold",
    21: "LMP_hold_req",
    22: "LMP_sniff",
    23: "LMP_sniff_req",
    24: "LMP_unsniff_req",
    25: "LMP_park_req",
    26: "LMP_park",
    27: "LMP_set_broadcast_scan_window",
    28: "LMP_modify_beacon",
    29: "LMP_unpark_BD_ADDR_req",
    30: "LMP_unpark_PM_ADDR_req",
    31: "LMP_incr_power_req",
    32: "LMP_decr_power_req",
    33: "LMP_max_power",
    34: "LMP_min_power",
    35: "LMP_auto_rate",
    36: "LMP_preferred_rate",
    37: "LMP_version_req",
    38: "LMP_version_res",
    39: "LMP_features_req",
    40: "LMP_features_res",
    41: "LMP_quality_of_service",
    42: "LMP_quality_of_service_req",
    43: "LMP_SCO_link_req",
    44: "LMP_remove_SCO_link_req",
    45: "LMP_max_slot",
    46: "LMP_max_slot_req",
    47: "LMP_timing_accuracy_req",
    48: "LMP_timing_accuracy_res",
    49: "LMP_setup_complete",
    50: "LMP_use_semi_permanent_key",
    51: "LMP_host_connection_req",
    52: "LMP_slot_offset",
    53: "LMP_page_mode_req",
    54: "LMP_Page_scan_mode_req",
    55: "LMP_supervision_timeout",
    56: "LMP_test_activate",
    57: "LMP_test_control",
    58: "LMP_encryption_key_size_mask_req",
    59: "LMP_encryption_key_size_mask_res",
    60: "LMP_set_AFH",
    61: "LMP_encapsulated_header",
    62: "LMP_encapsulated_payload",
    63: "LMP_simple_pairing_confirm",
    64: "LMP_simple_pairing_number",
    65: "LMP_DHkey_check",
    66: "LMP_pause_encryption_aes_req",
    # XXX: added to handle extended opcodes
    127: "LMP_extended_opcode",
}

# NOTE: https://github.com/pauloborges/bluez/blob/master/monitor/lmp.c
# NOTE: used when opcode is 127 = 0xfe
LMP_OPCODES_EXT = {
    1: "LMP_accepted_ext",
    2: "LMP_not_accepted_ext",
    3: "LMP_features_req_ext",
    4: "LMP_features_res_ext",
    5: "LMP_clk_adj",
    6: "LMP_clk_adj_ack",
    7: "LMP_clk_adj_req",
    11: "LMP_packet_type_table",
    12: "LMP_eSCO_link_req",
    13: "LMP_remove_eSCO_link_req",
    16: "LMP_channel_classification_req",
    17: "LMP_channel_classification",
    21: "LMP_sniff_subrating_req",
    22: "LMP_sniff_subrating_res",
    23: "LMP_pause_encryption_req",
    24: "LMP_resume_encryption_req",
    25: "LMP_IO_capability_req",
    26: "LMP_IO_capability_res",
    27: "LMP_numeric_comparision_failed",
    28: "LMP_passkey_failed",
    29: "LMP_oob_failed",
    30: "LMP_keypress_notification",
    31: "LMP_power_control_req",
    32: "LMP_power_control_res",
    33: "LMP_ping_req",
    34: "LMP_ping_res",
}

# NOTE: from Bluetooth assigned LMP
LMP_VERSIONS = {
    "0": "1.0b",
    "1": "1.1",
    "2": "1.2",
    "3": "2.0",
    "4": "2.1",
    "5": "3.0",
    "6": "4.0",
    "7": "4.1",
    "8": "4.2",
    "9": "5.0",
    "10": "5.1",
    "11": "5.2",
    "12": "5.3",
}

LMP_TRANS_INIT = {
    0: "C",
    1: "P",
}

LMP_TRANS_FLOW = {
    # NOTE: transaction initiated by Central
    0: {
        # NOTE: Flow False/True
        0: "C -> P",
        1: "P -> C",
    },
    # NOTE: transaction initiated by Peripheral
    1: {
        # NOTE: Flow False/True
        0: "P -> C",
        1: "C -> P",
    },
}

LMP_IO_CAPS = {
    0: "Display",
    1: "Display with Yes/No",
    2: "Keyboard",
    3: "No Input No Output",
}

LMP_AUTH_REQS = {
    0: "No MitM, No Bond",
    1: "MitM Prot,  No Bond",
    2: "No MitM, Dedicated Bond",
    3: "MitM Prot, Dedicated Bond",
    4: "No MitM, General Bond",
    5: "MitM Prot, General Bond",
}

# NOTE: LMP/LL codes from bt53 page 370
LMP_ERROR_CODES = {
    0x00: "Success",
    0x01: "Unknown HCI Command",
    0x02: "Unknown Connection Identifier",
    0x03: "Hardware Failure",
    0x04: "Page Timeout",
    0x05: "Authentication Failure",
    0x06: "PIN or Key Missing",
    0x07: "Memory Capacity Exceeded",
    0x08: "Connection Timeout",
    0x09: "Connection Limit Exceeded",
    0x0A: "Synchronous Connection Limit To A Device Exceeded",
    0x0B: "Connection Already Exists",
    0x0C: "Command Disallowed",
    0x0D: "Connection Rejected due to Limited Resources",
    0x0E: "Connection Rejected Due To Security Reasons",
    0x0F: "Connection Rejected due to Unacceptable BD_ADDR",
    0x10: "Connection Accept Timeout Exceeded",
    0x11: "Unsupported Feature or Parameter Value",
    0x12: "Invalid HCI Command Parameters",
    0x13: "Remote User Terminated Connection",
    0x14: "Remote Device Terminated Connection due to Low Resources",
    0x15: "Remote Device Terminated Connection due to Power Off",
    0x16: "Connection Terminated By Local Host",
    0x17: "Repeated Attempts",
    0x18: "Pairing Not Allowed",
    0x19: "Unknown LMP PDU",
    0x1A: "Unsupported Remote Feature",
    0x1B: "SCO Offset Rejected",
    0x1C: "SCO Interval Rejected",
    0x1D: "SCO Air Mode Rejected",
    0x1E: "Invalid LMP Parameters / Invalid LL Parameters",
    0x1F: "Unspecified Error",
    0x20: "Unsupported LMP Parameter Value / Unsupported LL Parameter Value",
    0x21: "Role Change Not Allowed",
    0x22: "LMP Response Timeout / LL Response Timeout",
    0x23: "LMP Error Transaction Collision / LL Procedure Collision",
    0x24: "LMP PDU Not Allowed",
    0x25: "Encryption Mode Not Acceptable",
    0x26: "Link Key cannot be Changed",
    0x27: "Requested QoS Not Supported",
    0x28: "Instant Passed",
    0x29: "Pairing With Unit Key Not Supported",
    0x2A: "Different Transaction Collision",
    0x2B: "Reserved for future use",
    0x2C: "QoS Unacceptable Parameter",
    0x2D: "QoS Rejected",
    0x2E: "Channel Classification Not Supported",
    0x2F: "Insufficient Security",
    0x30: "Parameter Out Of Mandatory Range",
    0x31: "Reserved for future use",
    0x32: "Role Switch Pending",
    0x33: "Reserved for future use",
    0x34: "Reserved Slot Violation",
    0x35: "Role Switch Failed",
    0x36: "Extended Inquiry Response Too Large",
    0x37: "Secure Simple Pairing Not Supported By Host",
    0x38: "Host Busy - Pairing",
    0x39: "Connection Rejected due to No Suitable Channel Found",
    0x3A: "Controller Busy",
    0x3B: "Unacceptable Connection Parameters",
    0x3C: "Advertising Timeout",
    0x3D: "Connection Terminated due to MIC Failure",
    0x3E: "Connection Failed to be Established / Synchronization Timeout",
    0x3F: "Previously used",
    0x40: "Coarse Clock Adjustment Rejected but Will Try to Adjust Using Clock Dragging",
    0x41: "Type0 Submap Not Defined",
    0x42: "Unknown Advertising Identifier",
    0x43: "Limit Reached",
    0x44: "Operation Cancelled by Host",
    0x45: "Packet Too Long",
}

# NOTE: bt53 page 699
LMP_CRYPTO_MODES = {
    0: "No encryption",
    1: "Encryption ON",
    2: "Previously used",
}

LMP_KEYSIZES = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]

LMP_AURAND_LEN = 16
LMP_SRES_LEN = 4
LMP_ENRAND_LEN = 16
