"""
e1_tests.py

"""
import logging

from constants import log
from e1 import e1
from h import H

log.setLevel(logging.DEBUG)


def test_e1_1():
    """First test vector from the spec."""

    rand = bytearray.fromhex("00000000000000000000000000000000")
    addr = bytearray.fromhex("000000000000")
    key = bytearray.fromhex("00000000000000000000000000000000")

    Keys = [i for i in range(18)]
    ComputedKeys, Ar, ComputedKeysPrime, ArPrime, ComputedKc = H(key, rand, addr, 6)
    print("test_e1_1 BEGIN ComputedKeys, Ar")
    round1 = bytearray.fromhex("00000000000000000000000000000000")
    assert Ar[1] == round1
    Keys[1] = bytearray.fromhex("00000000000000000000000000000000")
    assert ComputedKeys[1] == Keys[1]
    Keys[2] = bytearray.fromhex("4697b1baa3b7100ac537b3c95a28ac64")
    assert ComputedKeys[2] == Keys[2]
    # NOTE: this should be input to round2
    round2 = bytearray.fromhex("78d19f9307d2476a523ec7a8a026042a")
    assert Ar[2] == round2
    Keys[3] = bytearray.fromhex("ecabaac66795580df89af66e66dc053d")
    assert ComputedKeys[3] == Keys[3]
    Keys[4] = bytearray.fromhex("8ac3d8896ae9364943bfebd4969b68a0")
    assert ComputedKeys[4] == Keys[4]
    round3 = bytearray.fromhex("600265247668dda0e81c07bbb30ed503")
    assert Ar[3] == round3
    Keys[5] = bytearray.fromhex("5d57921fd5715cbb22c1be7bbc996394")
    assert ComputedKeys[5] == Keys[5]
    Keys[6] = bytearray.fromhex("2a61b8343219fdfb1740e6511d41448f")
    assert ComputedKeys[6] == Keys[6]
    round4 = bytearray.fromhex("d7552ef7cc9dbde568d80c2215bc4277")
    assert Ar[4] == round4
    Keys[7] = bytearray.fromhex("dd0480dee731d67f01a2f739da6f23ca")
    assert ComputedKeys[7] == Keys[7]
    Keys[8] = bytearray.fromhex("3ad01cd1303e12a1cd0fe0a8af82592c")
    assert ComputedKeys[8] == Keys[8]
    round5 = bytearray.fromhex("fb06bef32b52ab8f2a4f2b6ef7f6d0cd")
    assert Ar[5] == round5
    Keys[9] = bytearray.fromhex("7dadb2efc287ce75061302904f2e7233")
    assert ComputedKeys[9] == Keys[9]
    Keys[10] = bytearray.fromhex("c08dcfa981e2c4272f6c7a9f52e11538")
    assert ComputedKeys[10] == Keys[10]
    round6 = bytearray.fromhex("b46b711ebb3cf69e847a75f0ab884bdd")
    assert Ar[6] == round6
    Keys[11] = bytearray.fromhex("fc2042c708e409555e8c147660ffdfd7")
    assert ComputedKeys[11] == Keys[11]
    Keys[12] = bytearray.fromhex("fa0b21001af9a6b9e89e624cd99150d2")
    assert ComputedKeys[12] == Keys[12]
    round7 = bytearray.fromhex("c585f308ff19404294f06b292e978994")
    assert Ar[7] == round7
    Keys[13] = bytearray.fromhex("18b40784ea5ba4c80ecb48694b4e9c35")
    assert ComputedKeys[13] == Keys[13]
    Keys[14] = bytearray.fromhex("454d54e5253c0c4a8b3fcca7db6baef4")
    assert ComputedKeys[14] == Keys[14]
    # NOTE: round8 does not include last add_one
    round8 = bytearray.fromhex("2665fadb13acf952bf74b4ab12264b9f")
    assert Ar[8] == round8
    Keys[15] = bytearray.fromhex("2df37c6d9db52674f29353b0f011ed83")
    assert ComputedKeys[15] == Keys[15]
    Keys[16] = bytearray.fromhex("b60316733b1e8e70bd861b477e2456f1")
    assert ComputedKeys[16] == Keys[16]
    Keys[17] = bytearray.fromhex("884697b1baa3b7100ac537b3c95a28ac")
    assert ComputedKeys[17] == Keys[17]
    print("test_e1_1 END ComputedKeys, Ar")

    print("test_e1_1 BEGIN ComputedKeysPrime, ArPrime")
    round1 = bytearray.fromhex("158ffe43352085e8a5ec7a88e1ff2ba8")
    log.debug("test_e1_1 Ar[9]     : {}".format(repr(Ar[9])))
    log.debug("test_e1_1 ArPrime[1]: {}".format(repr(ArPrime[1])))
    log.debug("test_e1_1 round1    : {}".format(repr(round1)))
    assert ArPrime[1] == round1
    Keys[1] = bytearray.fromhex("e9e5dfc1b3a79583e9e5dfc1b3a79583")
    assert ComputedKeysPrime[1] == Keys[1]
    Keys[2] = bytearray.fromhex("7595bf57e0632c59f435c16697d4c864")
    assert ComputedKeysPrime[2] == Keys[2]
    round2 = bytearray.fromhex("0b5cc75febcdf7827ca29ec0901b6b5b")
    assert ArPrime[2] == round2
    Keys[3] = bytearray.fromhex("e31b96afcc75d286ef0ae257cbbc05b7")
    assert ComputedKeysPrime[3] == Keys[3]
    Keys[4] = bytearray.fromhex("0d2a27b471bc0108c6263aff9d9b3b6b")
    assert ComputedKeysPrime[4] == Keys[4]
    round3 = bytearray.fromhex("e4278526c8429211f7f2f0016220aef4")
    # NOTE: inp_1 + inp_3, currently not asserted
    assert ArPrime[3] == round3
    added = bytearray.fromhex("f1b68365fd6217f952de6a89831fd95c")
    Keys[5] = bytearray.fromhex("98d1eb5773cf59d75d3b17b3bc37c191")
    assert ComputedKeysPrime[5] == Keys[5]
    Keys[6] = bytearray.fromhex("fd2b79282408ddd4ea0aa7511133336f")
    assert ComputedKeysPrime[6] == Keys[6]
    round4 = bytearray.fromhex("d0304ad18337f86040145d27aa5c8153")
    assert ArPrime[4] == round4
    Keys[7] = bytearray.fromhex("331227756638a41d57b0f7e071ee2a98")
    assert ComputedKeysPrime[7] == Keys[7]
    Keys[8] = bytearray.fromhex("aa0dd8cc68b406533d0f1d64aabacf20")
    assert ComputedKeysPrime[8] == Keys[8]
    round5 = bytearray.fromhex("84db909d213bb0172b8b6aaf71bf1472")
    assert ArPrime[5] == round5
    Keys[9] = bytearray.fromhex("669291b0752e63f806fce76f10e119c8")
    assert ComputedKeysPrime[9] == Keys[9]
    Keys[10] = bytearray.fromhex("ef8bdd46be8ee0277e9b78adef1ec154")
    assert ComputedKeysPrime[10] == Keys[10]
    round6 = bytearray.fromhex("f835f52921e903dfa762f1df5abd7f95")
    assert ArPrime[6] == round6
    Keys[11] = bytearray.fromhex("f3902eb06dc409cfd78384624964bf51")
    assert ComputedKeysPrime[11] == Keys[11]
    Keys[12] = bytearray.fromhex("7d72702b21f97984a721c99b0498239d")
    assert ComputedKeysPrime[12] == Keys[12]
    round7 = bytearray.fromhex("ae6c0b4bb09f25c6a5d9788a31b605d1")
    assert ArPrime[7] == round7
    Keys[13] = bytearray.fromhex("532e60bceaf902c52a06c2c283ecfa32")
    assert ComputedKeysPrime[13] == Keys[13]
    Keys[14] = bytearray.fromhex("181715e5192efb2a64129668cf5d9dd4")
    assert ComputedKeysPrime[14] == Keys[14]
    # NOTE: round8 does not include last add_one
    round8 = bytearray.fromhex("744a6235b86cc0b853cc9f74f6b65311")
    assert ArPrime[8] == round8
    Keys[15] = bytearray.fromhex("83017c1434342d4290e961578790f451")
    assert ComputedKeysPrime[15] == Keys[15]
    Keys[16] = bytearray.fromhex("2603532f365604646ff65803795ccce5")
    assert ComputedKeysPrime[16] == Keys[16]
    Keys[17] = bytearray.fromhex("882f7c907b565ea58dae1c928a0dcf41")
    assert ComputedKeysPrime[17] == Keys[17]
    SRES = bytearray.fromhex("056c0fe6")
    ACO = bytearray.fromhex("48afcdd4bd40fef76693b113")
    Out = bytearray.fromhex("056c0fe648afcdd4bd40fef76693b113")
    log.debug("test_e1_1 Out        : {}".format(repr(Out)))
    log.debug("test_e1_1 ArPrime[9] : {}".format(repr(ArPrime[9])))
    assert ArPrime[10] == Out
    assert ArPrime[10][:4] == SRES
    assert ArPrime[10][4:] == ACO
    # NOTE: test high level API call
    ComputedSRES, ComputedACO = e1(key, rand, addr)
    assert ComputedSRES == SRES
    assert ComputedACO == ACO
    print("test_e1_1 END ComputedKeysPrime, ArPrime")


def test_e1_2():
    rand = bytearray.fromhex("bc3f30689647c8d7c5a03ca80a91eceb")
    addr = bytearray.fromhex("7ca89b233c2d")
    key = bytearray.fromhex("159dd9f43fc3d328efba0cd8a861fa57")
    SRES = bytearray.fromhex("8d5205c5")
    ACO = bytearray.fromhex("3ed75df4abd9af638d144e94")
    ComputedSRES, ComputedACO = e1(key, rand, addr)
    assert ComputedSRES == SRES
    assert ComputedACO == ACO


def test_e1_3():
    rand = bytearray.fromhex("0891caee063f5da1809577ff94ccdcfb")
    addr = bytearray.fromhex("c62f19f6ce98")
    key = bytearray.fromhex("45298d06e46bac21421ddfbed94c032b")
    SRES = bytearray.fromhex("00507e5f")
    ACO = bytearray.fromhex("2a5f19fbf60907e69f39ca9f")
    ComputedSRES, ComputedACO = e1(key, rand, addr)
    assert ComputedSRES == SRES
    assert ComputedACO == ACO


def test_e1_4():
    rand = bytearray.fromhex("0ecd61782b4128480c05dc45542b1b8c")
    addr = bytearray.fromhex("f428f0e624b3")
    key = bytearray.fromhex("35949a914225fabad91995d226de1d92")
    SRES = bytearray.fromhex("80e5629c")
    ACO = bytearray.fromhex("a6fe4dcde3924611d3cc6ba1")
    ComputedSRES, ComputedACO = e1(key, rand, addr)
    assert ComputedSRES == SRES
    assert ComputedACO == ACO


if __name__ == "__main__":

    print("")
    test_e1_1()
    test_e1_2()
    test_e1_3()
