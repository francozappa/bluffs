"""
mkdf_tests.py

Check at the protocol-level that mkdf prevents the BLUFFS attacks.

"""
import logging

from mkdf import mkdf, mac
from constants import log

log.setLevel(logging.INFO)

if __name__ == "__main__":

    # Pairing Key (PK), unknown to Charlie
    LK = bytearray.fromhex("F80FA88FF3DC39F659F1155F0B4D249E")

    # NOTE: Charlie, attacker
    AU_RAND_C = bytearray.fromhex("00000000000000000000000000000000")
    EN_NONCE_C = bytearray.fromhex("00000000000000000000000000000000")
    ENTROPY_C = 7
    BTADDR_C = bytearray.fromhex("DCE55B277196")

    # NOTE: victim
    EN_NONCE_V = bytearray.fromhex("00000000000000000000000000000001")
    BTADDR_V = bytearray.fromhex("BABABABABABA")

    # NOTE: victim authenticates EN_NONCE_C
    MAC_C = mac(LK, EN_NONCE_C, BTADDR_V)

    # NOTE: attacker CANNOT authenticate EN_NONCE_V as she does not know LK
    MAC_V = mac(LK, EN_NONCE_V, BTADDR_V)

    # NOTE: attacker CANNOT force a SK as she does not control EN_NONCE_V
    SK = mkdf(LK, AU_RAND_C, EN_NONCE_C, EN_NONCE_V, BTADDR_V, ENTROPY_C)
