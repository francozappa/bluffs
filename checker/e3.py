#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
e3.py

e3 is used to generate Kc. The test cases assumes that COF = ACO and ACO aro
provided.

"""
import logging

from h import H
from constants import log

log.setLevel(logging.DEBUG)


def e3(K, RAND, COF):
    """Generate Kc EQ 23, pag 1681.

    K is Kl aka the link key (combination type most of the time)
    RAND is EN_RAND aka N_pub
    COF is either ACO or BTADD_master || BTADD_master

    Returns: Kc
    """

    Keys, Ar, KeysPrime, ArPrime, Kc = H(K, RAND, COF, 12)

    return Kc
