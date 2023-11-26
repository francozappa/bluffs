#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
mkdf.py

Exhanced KDF for LSC (see paper's Section 7)
"""
import logging

from e1 import e1
from es import Kc_to_Kc_prime
from e3 import e3

from constants import log

log.setLevel(logging.INFO)


def mac(LK, EN_NONCE, BTADDR):
    """Generate a 16 Byte diversifier message authentication code (MAC)."""
    assert type(LK) == bytearray and len(LK) == 16
    assert type(EN_NONCE) == bytearray and len(EN_NONCE) == 16
    assert type(BTADDR) == bytearray and len(BTADDR) == 6

    a, b = e1(LK, EN_NONCE, BTADDR)
    en_nonce_mac = a + b
    log.debug(f"{en_nonce_mac.hex()}")

    return en_nonce_mac


def mkdf(LK, AU_RAND, EN_NONCE_C, EN_NONCE_P, BTADDR, ENTROPY):
    """Generate KcPrime

    LK link key, 16 Bytes

    AU_RAND, 16 Bytes

    EN_NONCE_C, 16 Bytes diversification nonce from the Central

    EN_NONCE_P, 16 Bytes diversification nonce from the Peripheral

    BTADD address (leftmost byte is MSB)

    ENTROPY  = [1, ..., 16]


    """
    assert type(LK) == bytearray and len(LK) == 16
    assert type(AU_RAND) == bytearray and len(AU_RAND) == 16
    assert type(EN_NONCE_C) == bytearray and len(EN_NONCE_C) == 16
    assert type(EN_NONCE_P) == bytearray and len(EN_NONCE_P) == 16
    assert type(BTADDR) == bytearray and len(BTADDR) == 6
    assert type(ENTROPY) == int and ENTROPY <= 16 and ENTROPY > 0

    BTADDR.reverse()
    _, COF = e1(LK, AU_RAND, BTADDR)
    log.debug("COF: {}".format(repr(COF)))
    # NOTE: redo reverse as it is passed by reference
    BTADDR.reverse()

    # NOTE: e3 used two times with EN_NONCE_C and EN_NONCE_P
    Kc = e3(LK, EN_NONCE_C, COF)
    log.debug("Kc: {}".format(repr(Kc)))
    Kc2 = e3(Kc, EN_NONCE_P, COF)
    log.debug("Kc2: {}".format(repr(Kc2)))
    Kc2.reverse()

    KcPrime = Kc_to_Kc_prime(Kc2, ENTROPY)
    KcPrime.reverse()

    return KcPrime
