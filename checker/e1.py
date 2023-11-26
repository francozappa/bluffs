#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
e1.py

"""
import logging

from constants import log, SRES_LEN, ACO_LEN
from h import H

log.setLevel(logging.DEBUG)


def e1(K, RAND, BTADD_S):
    """Generate SRES and ACO, EQ 12, pag 1675.

    BTADD_S slave address (leftmost byte is MSB)

    h = Hash (K , RAND, address, 6 )

    SRES = h[:4], 4 Bytes

    ACO  = h[4:], 12 Bytes


    """

    Keys, Ar, KeysPrime, ArPrime, Out = H(K, RAND, BTADD_S, 6)

    SRES = Out[0:4]
    assert len(SRES) == SRES_LEN

    ACO = Out[4:]
    assert len(ACO) == ACO_LEN

    return SRES, ACO
