#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
es.py

"""
import logging

from BitVector import BitVector
from constants import log, Ar_KEY_LEN, G1, G2

log.setLevel(logging.DEBUG)


def Kc_to_Kc_prime(Kc, L, red=False):
    """Compute Kc_prime from Kc.
    Kc is the encryption key computed from e3

    L is the key byte size negotiated via LMP

    If red is True returns also Kc_mod_g1
    """
    assert len(Kc) == Ar_KEY_LEN and type(Kc) == bytearray
    assert type(L) == int and (L > 0 or L < 17)

    if L == 16:
        log.debug("Kc_to_Kc_prime If L=16 then Kc_prime equals Kc")
        if red:
            return Kc, Kc
        else:
            return Kc

    else:
        g1 = BitVector(intVal=G1[L], size=128)
        g2 = BitVector(intVal=G2[L], size=128)
        one = BitVector(intVal=0x01, size=128)

        Kc_hexstring = bytearray_to_hexstring(Kc)
        Kc_bv = hexstring_to_BitVector(Kc_hexstring)

        Kc_mod_g1 = Kc_bv.gf_multiply_modular(one, g1, 128)
        Kc_mod_g1_ba = BitVector_to_bytearray(Kc_mod_g1)
        for i in range(16 - L):
            # NOTE the first 16-L Bytes should be 0
            assert Kc_mod_g1_ba[i] == 0

        Kc_prime_bv = g2.gf_multiply(Kc_mod_g1)[128:]
        log.debug(
            "Kc_to_Kc_prime: bits: {}, {}".format(
                len(Kc_prime_bv), Kc_prime_bv.count_bits()
            )
        )
        Kc_prime = BitVector_to_bytearray(Kc_prime_bv)
        assert len(Kc_prime) == Ar_KEY_LEN and type(Kc_prime) == bytearray

        if red:
            return Kc_prime, Kc_mod_g1_ba
        else:
            return Kc_prime


def bytearray_to_hexstring(ba):
    """Bytearray to hexstring."""

    ba_hex_str = ""
    for b in ba:
        hex_digit = hex(b)[2:]  # 0x0 ... 0xff
        if len(hex_digit) == 1:
            hex_digit = "0" + hex_digit
        # log.debug('bytearray_to_hexstring: {}, {}'.format(b, hex_digit))
        ba_hex_str += hex_digit  # 0x0 ... 0xff
    # log.debug('bytearray_to_hexstring: {}'.format(ba_hex_str))
    return ba_hex_str


def hexstring_to_BitVector(hexstring):
    """Ugly workaround to create BitVector."""
    assert type(hexstring) == str

    bv = BitVector(hexstring=hexstring)

    return bv


def BitVector_to_bytearray(bv):
    assert type(bv) == BitVector

    bv_hexstring = bv.get_bitvector_in_hex()
    log.debug("BitVector_to_bytearray bv_hexstring: {}".format(bv_hexstring))
    ba = bytearray.fromhex(bv.getHexStringFromBitVector())

    assert len(ba) == Ar_KEY_LEN
    return ba


if __name__ == "__main__":

    pass
