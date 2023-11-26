#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
constants.py

"""
import logging

log = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s %(name)-4s %(levelname)-4s %(message)s")
handler.setFormatter(formatter)
log.addHandler(handler)
# log.setLevel(logging.DEBUG)

Ar_ROUNDS = 8
Ar_KEY_LEN = 16  # Bytes, 128 biis
EN_RAND_LEN = 16  # Bytes, 96 bits
KEYS_LEN = 16  # Bytes, Kl, Kc, Kc_prime

COF_LEN = 12  # Bytes, 96 bits
ACO_LEN = 12  # Bytes, 96 bits

BTADD_LEN = 6  # Bytes, 48 bits

CRC_LEN = 2  # Bytes, pag 1598
MIC_LEN = 4  # Bytes, pag 1704

# NOTE: NEX is the master
NEX_BTADD = "ccfa0070dcb6"
MOTO_BTADD = "829f669bda24"

SRES_LEN = 4  # Bytes, 32 bits
CLK26_1_LEN = 4  # Bytes, 32 bits

# NOTE: path to the E0 binary
E0_IMPL_PATH = "/home/mel/knob/e0/e0"

PATTERNS = {
    "L2CAP1": b"\x08\x00\x01\x00",
    "L2CAP1_R": b"\x00\x01\x00\x08",
    "L2CAP2": b"\x0c\x00\x01\x00",
    "L2CAP2_R": b"\x00\x01\x00\x0c",
    "L2CAP3": b"\x0a\x00\x01\x00",
    "L2CAP3_R": b"\x00\x01\x00\x0a",
    "L2CAP1_T": b"\x03\x00\x49\x00",
    "L2CAP1_TR": b"\x00\x49\x00\x03",
    "aaaa": b"\x61\x61\x61\x61",
    "bbbb": b"\x62\x62\x62\x62",
    "cccc": b"\x63\x63\x63\x63",
    "dddd": b"\x64\x64\x64\x64",
    "image": b"\x69\x6d\x61\x67\x65",
    "jpeg": b"\x6a\x70\x65\x67",
    "f_i_l_e": b"\x66\x00\x69\x00\x6c\x00\x65",
    "j_p_e_g": b"\6a\x00\x70\x00\x65\x00\x67",
    # NOTE: compute and add CRCs
}

G1 = [
    0x00,  # not used
    0x0000011D,  # L=1
    0x0001003F,  # L=2
    0x010000DB,
    0x01000000AF,
    0x010000000039,
    0x01000000000291,
    0x0100000000000095,
    0x01000000000000001B,
    0x01000000000000000609,
    0x0100000000000000000215,
    0x01000000000000000000013B,
    0x010000000000000000000000DD,
    0x010000000000000000000000049D,
    0x01000000000000000000000000014F,
    0x010000000000000000000000000000E7,
    0x0000000100000000000000000000000000000000,  # L = 16
]

G2 = [
    0x00,  # not used
    0xE275A0ABD218D4CF928B9BBF6CB08F,  # L=1
    0x01E3F63D7659B37F18C258CFF6EFEF,  # L=2
    0x000001BEF66C6C3AB1030A5A1919808B,
    0x016AB89969DE17467FD3736AD9,
    0x0163063291DA50EC55715247,
    0x2C9352AA6CC054468311,
    0xB3F7FFFCE279F3A073,
    0xA1AB815BC7EC8025,
    0x02C98011D8B04D,
    0x058E24F9A4BB,
    0x0CA76024D7,
    0x1C9C26B9,
    0x26D9E3,
    0x4377,
    0x89,
    0x01,  # L = 16
]

# NOTE: used for nonlin_subs
EXP_45 = []
for i in range(0, 256):
    EXP_45.append(int(((45**i) % 257) % 256))
