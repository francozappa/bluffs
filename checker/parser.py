#!/usr/bin/env python
"""
parser.py

"""

import pyshark
from pathlib import Path

from hwdb import HWDB
from lmp import LMP_OPCODES, LMP_OPCODES_EXT, LMP_VERSIONS, LMP_ERROR_CODES
from lmp import LMP_AUTH_REQS, LMP_TRANS_FLOW, LMP_TRANS_INIT, LMP_IO_CAPS
from lmp import LMP_CRYPTO_MODES, LMP_KEYSIZES
from lmp import LMP_ENRAND_LEN, LMP_AURAND_LEN, LMP_SRES_LEN


def check_path(arg1: str) -> bool:
    """Check that arg1 is a valid pcap[ng] path.

    :arg1: str
    :returns: bool

    """
    path = Path(arg1)
    is_path = False
    if path is None:
        print(f"check_path: {arg1} is None")
        is_path = False
    elif path.is_dir():
        print(f"check_path: {arg1} is a path to a folder")
        is_path = False
    elif path.is_file() and path.suffix in (".pcap", ".pcapng"):
        is_path = True
    elif not path.exists():
        print(f"check_path: {arg1} does not exist")
        is_path = False
    else:
        is_path = False
    return is_path


def get_opcode(packet: pyshark.packet.packet.Packet) -> int:
    """Return the LMP opcode"""
    return int(packet.h4bcm.btbrlmp_op)


def get_opcode_ext(packet: pyshark.packet.packet.Packet) -> int:
    """Return the LMP opcode"""
    assert get_opcode(packet) == 127
    return int(packet.h4bcm.btbrlmp_eop)


# NOTE: Parent class
class LmpBase(object):
    """Base Class for LMP Parsing"""

    def __init__(self, packet: pyshark.packet.packet.Packet):
        # self.lenght = int(packet.length)
        self.number = int(packet.number)
        # self.sniff_time = packet.sniff_time  # datetime.datetime

        # h4bcm layer
        _tinit = int(packet.h4bcm.btbrlmp_tid)
        self.tinit = LMP_TRANS_INIT[_tinit]
        self.tflow = LMP_TRANS_FLOW[_tinit][int(packet.h4bcm.flow)]

        self.opcode = int(packet.h4bcm.btbrlmp_op)
        # NOTE: if the opcode is ex we use the ext LMP command string
        if self.opcode == 127:
            self.opcode_ext = int(packet.h4bcm.btbrlmp_eop)
            self.opcode_str = LMP_OPCODES_EXT[self.opcode_ext]
        else:
            self.opcode_str = LMP_OPCODES[self.opcode]

    def __repr__(self):
        return str(vars(self))


# NOTE: Specialized LMP classes
class LmpHostConnReq(LmpBase):
    """Parse LMP_host_connection_req"""

    def __init__(self, packet: pyshark.packet.packet.Packet):
        super().__init__(packet)


class LmpDetach(LmpBase):
    """Parse LMP_detach"""

    def __init__(self, packet: pyshark.packet.packet.Packet):
        super().__init__(packet)

        self.err = int(packet.h4bcm.btbrlmp_err, 16)
        self.err_str = LMP_ERROR_CODES[self.err]


class LmpAccepted(LmpBase):
    """Parse LMP_accepted"""

    def __init__(self, packet: pyshark.packet.packet.Packet):
        super().__init__(packet)

        self.in_resp_to = int(packet.h4bcm.btbrlmp_opinre)
        self.in_resp_to_str = LMP_OPCODES[self.in_resp_to]


class LmpNotAccepted(LmpBase):
    """Parse LMP_not_accepted"""

    def __init__(self, packet: pyshark.packet.packet.Packet):
        super().__init__(packet)

        self.in_resp_to = int(packet.h4bcm.btbrlmp_opinre)
        self.in_resp_to_str = LMP_OPCODES[self.in_resp_to]
        self.err = int(packet.h4bcm.btbrlmp_err, 16)
        self.err_str = LMP_ERROR_CODES[self.err]


class LmpAuRand(LmpBase):
    """Parse LMP_au_rand"""

    def __init__(self, packet: pyshark.packet.packet.Packet):
        super().__init__(packet)

        self.aurand = packet.h4bcm.btbrlmp_rand
        self.aurand_ba = bytearray.fromhex(self.aurand.replace(":", ""))
        assert len(self.aurand_ba) == LMP_AURAND_LEN


class LmpSres(LmpBase):
    """Parse LMP_sres"""

    def __init__(self, packet: pyshark.packet.packet.Packet):
        super().__init__(packet)

        self.sres = packet.h4bcm.btbrlmp_authres
        self.sres_ba = bytearray.fromhex(self.sres.replace(":", ""))
        assert len(self.sres_ba) == LMP_SRES_LEN


class LmpEncryptionKeySizeReq(LmpBase):
    """Parse LMP_encryption_key_size_req"""

    def __init__(self, packet: pyshark.packet.packet.Packet):
        super().__init__(packet)

        self.keysize = int(packet.h4bcm.btbrlmp_keysz)
        assert self.keysize in LMP_KEYSIZES


class LmpStartEncryptionReq(LmpBase):
    """Parse LMP_start_encryption_req"""

    def __init__(self, packet: pyshark.packet.packet.Packet):
        super().__init__(packet)

        # NOTE: enrand not used with SC
        self.enrand = packet.h4bcm.btbrlmp_rand
        self.enrand_ba = bytearray.fromhex(self.enrand.replace(":", ""))
        assert len(self.enrand_ba) == LMP_ENRAND_LEN
