"""
analyzer.py

"""

from parser import LmpNotAccepted, LmpAccepted, LmpAuRand, LmpSres, get_opcode
from parser import LmpEncryptionKeySizeReq, LmpStartEncryptionReq

import pyshark

from lmp import LMP_OPCODES
from kdf import kdf

PK_BYTES = 16
BTADD_BYTES = 6
BTADD_DEVBOARD = bytearray.fromhex("20819A093E41")

BA_16_ZEROS = bytearray.fromhex("00000000000000000000000000000000")


def check_pk(pair_key: str) -> bool:
    """Check if PK is in valid format

    e.g., 5B61D2D4E4341878441883BB2055F2C9
    """
    try:
        assert len(pair_key) == PK_BYTES * 2
        assert int(pair_key, 16)
        return True
    except (AssertionError, ValueError):
        print("check_pk ERROR")
        return False


def check_btadd(btadd: str) -> bool:
    """Check if PK is in valid format

    e.g., 5B61D2D4E4341878441883BB2055F2C9
    """
    try:
        assert len(btadd) == BTADD_BYTES * 2
        assert int(btadd, 16)
        return True
    except (AssertionError, ValueError):
        print("check_btadd ERROR")
        return False


def gen_sessions(pcap_path: str) -> list:
    """Parse pcap and generate a list of sessions"""

    # NOTE: test first btlmp DF and then btbrlmp
    pkts = pyshark.FileCapture(pcap_path, display_filter="btlmp")
    pkts.load_packets()
    if len(pkts) == 0:
        print("DEBUG: No LMP packets with btlmp df, trying btbrlmp.")
        pkts = pyshark.FileCapture(pcap_path, display_filter="btbrlmp")
        pkts.load_packets()
    if len(pkts) == 0:
        print("DEBUG: No LMP packets found with bt[br]lmp df.")

    ses = []
    ses_count = 0
    parse = False
    se = []
    # FIXME: ATM I'm not filtering out LMP pairing
    for pkt in pkts:
        opcode = get_opcode(pkt)
        # NOTE: new session  with LMP_host_connection_req
        if opcode == 51:
            ses_count += 1
            parse = True
            se = []
        # NOTE: end session  with LMP_detach
        elif opcode == 7:
            # NOTE: if LMP_detach is before LMP_host_connection_req
            try:
                ses.append(se)
            except UnboundLocalError:
                pass
            parse = False
        elif parse:
            if LMP_OPCODES[opcode] == "LMP_accepted":
                se.append(LmpAccepted(pkt))
            elif LMP_OPCODES[opcode] == "LMP_not_accepted":
                se.append(LmpNotAccepted(pkt))
            elif LMP_OPCODES[opcode] == "LMP_au_rand":
                se.append(LmpAuRand(pkt))
            elif LMP_OPCODES[opcode] == "LMP_sres":
                se.append(LmpSres(pkt))
            elif LMP_OPCODES[opcode] == "LMP_encryption_key_size_req":
                se.append(LmpEncryptionKeySizeReq(pkt))
            elif LMP_OPCODES[opcode] == "LMP_start_encryption_req":
                se.append(LmpStartEncryptionReq(pkt))
        else:
            continue

    pkts.close()
    return ses


def gen_report(session: list, pk: bytearray, btadd_p: bytearray) -> dict:
    """Generate a security report for an LSC session"""

    report = {}

    aurands = []
    found_keysize = False
    found_aurand = False
    found_enrand = False
    for pkt in session:
        if isinstance(pkt, LmpEncryptionKeySizeReq):
            if "keysize" not in report or report["keysize"] > pkt.keysize:
                report["keysize"] = pkt.keysize
                report["keysize_pnum"] = pkt.number
        elif isinstance(pkt, LmpAccepted) and pkt.in_resp_to == 16:
            report["keysize_accept_pnum"] = pkt.number
            assert report["keysize_pnum"] < report["keysize_accept_pnum"]
            found_keysize = True
        # NOTE: storing the last couple of AU_RAND-SRES
        elif isinstance(pkt, LmpAuRand):
            aurands.append(pkt.aurand_ba)
            found_aurand = True
        elif isinstance(pkt, LmpSres):
            report["sres"] = pkt.sres_ba
        elif isinstance(pkt, LmpStartEncryptionReq):
            report["enrand"] = pkt.enrand_ba
            found_enrand = True
        elif isinstance(pkt, LmpAccepted) and pkt.in_resp_to == 17:
            report["start_enc_accept_pnum"] = pkt.number
        # NOTE: remove last aurand if you get LMP_not_accepted 11
        elif isinstance(pkt, LmpNotAccepted) and pkt.in_resp_to == 11:
            aurands.pop(-1)

    # NOTE: manage multiple AURAND
    if found_aurand:
        report["aurand"] = aurands[-1]

    if found_aurand and found_enrand and found_keysize:
        report["sk"] = kdf(
            pk,
            report["aurand"],
            report["enrand"],
            btadd_p,
            report["keysize"],
        )

    return report


def gen_analysis(PCAP: str, LK: bytearray, EXP_SK: bytearray, BTADD_P: bytearray):
    """Generate list of sessions and reports"""

    sessions = gen_sessions(PCAP)

    reports = []
    for session in sessions:
        report = gen_report(session, LK, BTADD_P)
        reports.append(report)

    i = 1
    for report in reports:
        print(f"## Begin session: {i}")
        if "keysize" in report:
            print(f"keysize: {report['keysize']}")
        if "enrand" in report:
            print(f"enrand: {report['enrand'].hex()}")
        if "aurand" in report:
            print(f"aurand: {report['aurand'].hex()}")
        if "sk" in report:
            print(f"sk ses: {report['sk'].hex()}")
            # NOTE: check constant SK
            if report["aurand"] == BA_16_ZEROS and report["enrand"] == BA_16_ZEROS:
                print(f"sk exp: {EXP_SK.hex()}")
                assert report["sk"] == EXP_SK
        print(f"## End session: {i}\n")
        i += 1


def test_lsc_pixelbudsa():
    """test_lsc_pixelbudsa"""

    PCAP = "../pcap/lsc-pixelbuds-aseries.pcapng"
    LK = bytearray.fromhex("75fc7a5988b3529473858a10f947156a")
    BTADD_P = bytearray.fromhex("0CC413F76795")

    # NOTE: SK_C that we expect (see packet comment)
    EXP_SK = bytearray.fromhex("c61da2f42fefab75bb15b7927af0a631")

    print("# Pixel Buds A series, spoofed LSC victim")
    gen_analysis(PCAP, LK, EXP_SK, BTADD_P)
    print("")


def test_sc_pixelbudsa():
    """test_sc_pixelbudsa"""

    PCAP = "../pcap/sc-pixelbuds-aseries.pcapng"
    LK = bytearray.fromhex("07c508e25d92d9102ecddc0db62cb405")
    BTADD_P = bytearray.fromhex("0CC413F76795")

    # NOTE: SK_C that we expect (see packet comment)
    EXP_SK = bytearray.fromhex("3581f68eecc5d1f295894c6bc9262812")

    print("# Pixel Buds A series, spoofed SC victim")
    gen_analysis(PCAP, LK, EXP_SK, BTADD_P)
    print("")


if __name__ == "__main__":

    print("# NOTE")
    print("Ignore the first session as it is related to legitimate pairing")
    print("The attacker forces EXP_SK in all sessions")
    print("")
    test_lsc_pixelbudsa()
    test_sc_pixelbudsa()
