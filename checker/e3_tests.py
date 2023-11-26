#!/usr/bin/python
"""
e3_tests.py

e3 is used to generate Kc. The test cases assumes that COF = ACO and ACO aro
provided.

Ar and Ar_prime uses SAFER+
"""
import logging

from h import K_to_K_tilda, E, add_bytes_mod256, H
from e3 import e3
from constants import log

log.setLevel(logging.DEBUG)


def test_E(inp, L, ext_inp):

    rv = E(inp, L)
    assert rv == ext_inp


def test_Ar(key, inp, out):
    """Target out passed as hexstring.

    Eg: 'e9e5dfc1b3a79583e9e5dfc1b3a79583'
    """

    ct = Ar(key, inp, mode="enc")
    # pt = Ar(key, ct, mode='dec')
    # assert inp == pt
    log.debug("test_Ar ct : {}".format(ct.encode("hex")))
    log.debug("test_Ar out: {}".format(out))
    assert ct.encode("hex") == out


def test_e3(key, rand, cof, Kc):
    """Test from test vector the reverse computation of Kc."""

    rv = e3(key, rand, cof)
    assert rv == Kc


def test_e3_1():
    """First test vector from the spec."""

    rand = bytearray.fromhex("00000000000000000000000000000000")
    aco = bytearray.fromhex("48afcdd4bd40fef76693b113")
    key = bytearray.fromhex("00000000000000000000000000000000")

    Keys = [i for i in range(18)]
    ComputedKeys, Ar, ComputedKeysPrime, ArPrime, ComputedKc = H(key, rand, aco, 12)
    print("test_e3_1 BEGIN ComputedKeys, Ar")
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
    print("test_e3_1 END ComputedKeys, Ar")

    print("test_e3_1 BEGIN ComputedKeysPrime, ArPrime")
    round1 = bytearray.fromhex("5d3ecb17f26083df0b7f2b9b29aef87c")
    # log.debug('test_e3_1 Ar[9]     : {}'.format(repr(Ar[9])))
    # log.debug('test_e3_1 ArPrime[1]: {}'.format(repr(ArPrime[1])))
    # log.debug('test_e3_1 round1    : {}'.format(repr(round1)))
    assert ArPrime[1] == round1
    Keys[1] = bytearray.fromhex("e9e5dfc1b3a79583e9e5dfc1b3a79583")
    assert ComputedKeysPrime[1] == Keys[1]
    Keys[2] = bytearray.fromhex("7595bf57e0632c59f435c16697d4c864")
    assert ComputedKeysPrime[2] == Keys[2]
    round2 = bytearray.fromhex("de6fe85c5827233fe22514a16f321bd8")
    assert ArPrime[2] == round2
    Keys[3] = bytearray.fromhex("e31b96afcc75d286ef0ae257cbbc05b7")
    assert ComputedKeysPrime[3] == Keys[3]
    Keys[4] = bytearray.fromhex("0d2a27b471bc0108c6263aff9d9b3b6b")
    assert ComputedKeysPrime[4] == Keys[4]
    round3 = bytearray.fromhex("7cd335b50d09d139ea6702623af85edb")
    # NOTE: inp_1 + inp_3, currently not asserted
    added = bytearray.fromhex("211100a2ff6954e6e1e62df913a656a7")
    assert ArPrime[3] == round3
    Keys[5] = bytearray.fromhex("98d1eb5773cf59d75d3b17b3bc37c191")
    assert ComputedKeysPrime[5] == Keys[5]
    Keys[6] = bytearray.fromhex("fd2b79282408ddd4ea0aa7511133336f")
    assert ComputedKeysPrime[6] == Keys[6]
    round4 = bytearray.fromhex("991dccb3201b5b1c4ceff65a3711e1e9")
    assert ArPrime[4] == round4
    Keys[7] = bytearray.fromhex("331227756638a41d57b0f7e071ee2a98")
    assert ComputedKeysPrime[7] == Keys[7]
    Keys[8] = bytearray.fromhex("aa0dd8cc68b406533d0f1d64aabacf20")
    assert ComputedKeysPrime[8] == Keys[8]
    round5 = bytearray.fromhex("18768c7964818805fe4c6ecae8a38599")
    assert ArPrime[5] == round5
    Keys[9] = bytearray.fromhex("669291b0752e63f806fce76f10e119c8")
    assert ComputedKeysPrime[9] == Keys[9]
    Keys[10] = bytearray.fromhex("ef8bdd46be8ee0277e9b78adef1ec154")
    assert ComputedKeysPrime[10] == Keys[10]
    round6 = bytearray.fromhex("82f9aa127a72632af43d1a17e7bd3a09")
    assert ArPrime[6] == round6
    Keys[11] = bytearray.fromhex("f3902eb06dc409cfd78384624964bf51")
    assert ComputedKeysPrime[11] == Keys[11]
    Keys[12] = bytearray.fromhex("7d72702b21f97984a721c99b0498239d")
    assert ComputedKeysPrime[12] == Keys[12]
    round7 = bytearray.fromhex("1543d7870bf2d6d6efab3cbf62dca97d")
    assert ArPrime[7] == round7
    Keys[13] = bytearray.fromhex("532e60bceaf902c52a06c2c283ecfa32")
    assert ComputedKeysPrime[13] == Keys[13]
    Keys[14] = bytearray.fromhex("181715e5192efb2a64129668cf5d9dd4")
    assert ComputedKeysPrime[14] == Keys[14]
    # NOTE: round8 does not include last add_one
    round8 = bytearray.fromhex("eee3e8744a5f8896de95831ed837ffd5")
    assert ArPrime[8] == round8
    Keys[15] = bytearray.fromhex("83017c1434342d4290e961578790f451")
    assert ComputedKeysPrime[15] == Keys[15]
    Keys[16] = bytearray.fromhex("2603532f365604646ff65803795ccce5")
    assert ComputedKeysPrime[16] == Keys[16]
    Keys[17] = bytearray.fromhex("882f7c907b565ea58dae1c928a0dcf41")
    assert ComputedKeysPrime[17] == Keys[17]
    Kc = bytearray.fromhex("cc802aecc7312285912e90af6a1e1154")
    assert ComputedKc == Kc
    assert e3(key, rand, aco) == Kc
    print("test_e3_1 END ComputedKeysPrime, ArPrime")


def test_e3_2():
    """Second test vector from the spec."""

    rand = bytearray.fromhex("950e604e655ea3800fe3eb4a28918087")
    aco = bytearray.fromhex("68f4f472b5586ac5850f5f74")
    key = bytearray.fromhex("34e86915d20c485090a6977931f96df5")

    Keys = [i for i in range(18)]
    ComputedKeys, Ar, ComputedKeysPrime, ArPrime, ComputedKc = H(key, rand, aco, 12)
    print("test_e3_2 BEGIN ComputedKeys, Ar")
    round1 = bytearray.fromhex("950e604e655ea3800fe3eb4a28918087")
    assert Ar[1] == round1
    Keys[1] = bytearray.fromhex("34e86915d20c485090a6977931f96df5")
    assert ComputedKeys[1] == Keys[1]
    Keys[2] = bytearray.fromhex("8de2595003f9928efaf37e5229935bdb")
    # log.debug('test_e3_2         Keys[2]: {}'.format(repr(Keys[2])))
    # log.debug('test_e3_2 ComputedKeys[2]: {}'.format(repr(ComputedKeys[2])))
    assert ComputedKeys[2] == Keys[2]
    # NOTE: this should be input to round2
    round2 = bytearray.fromhex("d46f5a04c967f55840f83d1cdb5f9afc")
    assert Ar[2] == round2
    Keys[3] = bytearray.fromhex("46f05ec979a97cb6ddf842ecc159c04a")
    assert ComputedKeys[3] == Keys[3]
    Keys[4] = bytearray.fromhex("b468f0190a0a83783521deae8178d071")
    assert ComputedKeys[4] == Keys[4]
    round3 = bytearray.fromhex("e16edede9cb6297f32e1203e442ac73a")
    assert Ar[3] == round3
    Keys[5] = bytearray.fromhex("8a171624dedbd552356094daaadcf12a")
    assert ComputedKeys[5] == Keys[5]
    Keys[6] = bytearray.fromhex("3085e07c85e4b99313f6e0c837b5f819")
    assert ComputedKeys[6] == Keys[6]
    round4 = bytearray.fromhex("805144e55e1ece96683d23366fc7d24b")
    assert Ar[4] == round4
    Keys[7] = bytearray.fromhex("fe45c27845169a66b679b2097d147715")
    assert ComputedKeys[7] == Keys[7]
    Keys[8] = bytearray.fromhex("44e2f0c35f64514e8bec66c5dc24b3ad")
    assert ComputedKeys[8] == Keys[8]
    round5 = bytearray.fromhex("edbaf77af070bd22e9304398471042f1")
    assert Ar[5] == round5
    Keys[9] = bytearray.fromhex("0d534968f3803b6af447eaf964007e7b")
    assert ComputedKeys[9] == Keys[9]
    Keys[10] = bytearray.fromhex("f5499a32504d739ed0b3c547e84157ba")
    assert ComputedKeys[10] == Keys[10]
    round6 = bytearray.fromhex("0dab1a4c846aef0b65b1498812a73b50")
    assert Ar[6] == round6
    Keys[11] = bytearray.fromhex("e17e8e456361c46298e6592a6311f3fb")
    assert ComputedKeys[11] == Keys[11]
    Keys[12] = bytearray.fromhex("ec6d14da05d60e8abac807646931711f")
    assert ComputedKeys[12] == Keys[12]
    round7 = bytearray.fromhex("1e7793cac7f55a8ab48bd33bc9c649e0")
    assert Ar[7] == round7
    Keys[13] = bytearray.fromhex("2b53dde3d89e325e5ff808ed505706ae")
    assert ComputedKeys[13] == Keys[13]
    Keys[14] = bytearray.fromhex("41034e5c3fb0c0d4f445f0cf23be79b0")
    assert ComputedKeys[14] == Keys[14]
    round8 = bytearray.fromhex("3723768baa78b6a23ade095d995404da")
    assert Ar[8] == round8
    Keys[15] = bytearray.fromhex("e2ca373d405a7abf22b494f28a6fd247")
    assert ComputedKeys[15] == Keys[15]
    Keys[16] = bytearray.fromhex("74e09c9068c0e8f1c6902d1b70537c30")
    assert ComputedKeys[16] == Keys[16]
    Keys[17] = bytearray.fromhex("767a7f1acf75c3585a55dd4a428b2119")
    assert ComputedKeys[17] == Keys[17]
    print("test_e3_2 END ComputedKeys, Ar")

    print("test_e3_2 BEGIN ComputedKeysPrime, ArPrime")
    round1 = bytearray.fromhex("39809afb773efd1b7510cd4cb7c49f34")
    assert ArPrime[1] == round1
    Keys[1] = bytearray.fromhex("1d0d48d485abddd3798b483a82a0f878")
    assert ComputedKeysPrime[1] == Keys[1]
    Keys[2] = bytearray.fromhex("aed957e600a5aed5217984dd5fef6fd8")
    assert ComputedKeysPrime[2] == Keys[2]
    # NOTE: this should be input to round2
    round2 = bytearray.fromhex("6436ddbabe92655c87a7d0c12ae5e5f6")
    assert ArPrime[2] == round2
    Keys[3] = bytearray.fromhex("fee00bb0de89b6ef0a289696a4faa884")
    assert ComputedKeysPrime[3] == Keys[3]
    Keys[4] = bytearray.fromhex("33ce2f4411db4dd9b7c42cc586b8a2ba")
    assert ComputedKeysPrime[4] == Keys[4]
    round3 = bytearray.fromhex("cec690f7e0aa5f063062301e049a5cc5")
    # NOTE: inp_1 + inp_3, currently not asserted
    added = bytearray.fromhex("f7462a0c97e85c1d4572fd52b35efbf1")
    assert ArPrime[3] == round3
    Keys[5] = bytearray.fromhex("b5116f5c6c29e05e4acb4d02a46a3318")
    assert ComputedKeysPrime[5] == Keys[5]
    Keys[6] = bytearray.fromhex("ff4fa1f0f73d1a3c67bc2298abc768f9")
    assert ComputedKeysPrime[6] == Keys[6]
    round4 = bytearray.fromhex("dcdfe942e9f0163fc24a4718844b417d")
    assert ArPrime[4] == round4
    Keys[7] = bytearray.fromhex("5453650c0819e001e48331ad0e9076e0")
    assert ComputedKeysPrime[7] == Keys[7]
    Keys[8] = bytearray.fromhex("b4ff8dda778e26c0dce08349b81c09a1")
    assert ComputedKeysPrime[8] == Keys[8]
    round5 = bytearray.fromhex("265a16b2f766afae396e7a98c189fda9")
    assert ArPrime[5] == round5
    Keys[9] = bytearray.fromhex("f638fa294427c6ed94300fd823b31d10")
    assert ComputedKeysPrime[9] == Keys[9]
    Keys[10] = bytearray.fromhex("1ccfa0bd86a9879b17d4bc457e3e03d6")
    assert ComputedKeysPrime[10] == Keys[10]
    round6 = bytearray.fromhex("628576b5291d53d1eb8611c8624e863e")
    assert ArPrime[6] == round6
    Keys[11] = bytearray.fromhex("0eaee2ef4602ac9ca19e49d74a76d335")
    assert ComputedKeysPrime[11] == Keys[11]
    Keys[12] = bytearray.fromhex("6e1062f10a16e0d378476da3943842e9")
    assert ComputedKeysPrime[12] == Keys[12]
    round7 = bytearray.fromhex("d7b9c2e9b2d5ea5c27019324cae882b3")
    assert ArPrime[7] == round7
    Keys[13] = bytearray.fromhex("40be960bd22c744c5b23024688e554b9")
    assert ComputedKeysPrime[13] == Keys[13]
    Keys[14] = bytearray.fromhex("95c9902cb3c230b44d14ba909730d211")
    assert ComputedKeysPrime[14] == Keys[14]
    round8 = bytearray.fromhex("97fb6065498385e47eb3df6e2ca439dd")
    assert ArPrime[8] == round8
    Keys[15] = bytearray.fromhex("10d4b6e1d1d6798aa00aa2951e32d58d")
    assert ComputedKeysPrime[15] == Keys[15]
    Keys[16] = bytearray.fromhex("c5d4b91444b83ee578004ab8876ba605")
    assert ComputedKeysPrime[16] == Keys[16]
    Keys[17] = bytearray.fromhex("1663a4f98e2862eddd3ec2fb03dcc8a4")
    assert ComputedKeysPrime[17] == Keys[17]
    Kc = bytearray.fromhex("c1beafea6e747e304cf0bd7734b0a9e2")
    assert ComputedKc == Kc
    assert e3(key, rand, aco) == Kc
    print("test_e3_2 END ComputedKeysPrime, ArPrime")


def test_e3_3():
    """Third test vector from the spec."""

    rand = bytearray.fromhex("6a8ebcf5e6e471505be68d5eb8a3200c")
    aco = bytearray.fromhex("658d791a9554b77c0b2f7b9f")
    key = bytearray.fromhex("35cf77b333c294671d426fa79993a133")
    Kc = bytearray.fromhex("a3032b4df1cceba8adc1a04427224299")
    assert e3(key, rand, aco) == Kc


def test_e3_4():
    """Fourth test vector from the spec."""

    rand = bytearray.fromhex("5ecd6d75db322c75b6afbd799cb18668")
    aco = bytearray.fromhex("63f701c7013238bbf88714ee")
    key = bytearray.fromhex("b9f90c53206792b1826838b435b87d4d")
    Kc = bytearray.fromhex("ea520cfc546b00eb7c3a6cea3ecb39ed")
    assert e3(key, rand, aco) == Kc


def test_e3_5():
    """Test vector from attack."""

    rand = bytearray.fromhex("d72fb4217dcdc3145056ba488bea9076")
    aco = bytearray(b"\x1c\xe4\xf9Bm\xc2\xbc\x11\x04r\xd6\x8e")
    key = bytearray.fromhex("d5f20744c05d08601d28fa1dd79cdc27")
    Kc = bytearray(b"\xa3\xfc\xce\xf2*\xd2#,z\xcb\x01\xe9\xb9\xedg'")
    assert e3(key, rand, aco) == Kc


if __name__ == "__main__":

    print("")
    log.info("BEGIN test_K_to_K_tilda")
    K = bytearray.fromhex("00000000000000000000000000000000")
    K_tilda = bytearray.fromhex("e9e5dfc1b3a79583e9e5dfc1b3a79583")
    assert K_tilda == K_to_K_tilda(K)
    K = bytearray.fromhex("34e86915d20c485090a6977931f96df5")
    K_tilda = bytearray.fromhex("1d0d48d485abddd3798b483a82a0f878")
    assert K_tilda == K_to_K_tilda(K)
    log.info("END test_K_to_K_tilda")

    print("")
    log.info("BEGIN test_E_str")
    log.warning("test_E no test vectors available")
    aco = bytearray.fromhex("48afcdd4bd40fef76693b113")
    aco_ext = bytearray.fromhex("48afcdd4bd40fef76693b11348afcdd4")
    assert aco_ext == E(aco, 12)
    log.info("END test_E")

    print("")
    log.info("BEGIN test_add_bytes_mod256")
    inp = bytearray.fromhex("00000000000000000000000000000001")
    out = bytearray.fromhex("00000000000000000000000000000002")
    assert add_bytes_mod256(inp, inp) == out
    log.info("END test_add_bytes_mod256")

    print("")
    test_e3_1()
    print("")
    test_e3_2()
    print("")
    test_e3_3()
    print("")
    test_e3_4()

    print("")
    test_e3_5()
