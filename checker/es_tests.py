"""
es_tests.py

"""
import logging
import pprint

from es import Kc_to_Kc_prime
from BitVector import BitVector
from constants import log, G1, G2


def test_Kc(name, g1, g2, Kc, Kc_mod_g1, Kc_prime):
    """Test from test vector the reverse computation of Kc."""

    quotient, remainder = Kc_prime.gf_divide_by_modulus(g2, 128)
    assert int(quotient) == int(Kc_mod_g1)
    log.debug("int(quotient): {}".format(int(quotient)))
    log.debug("int(remainder): {}".format(int(remainder)))

    mi = quotient.gf_MI(g1, 128)
    quotient2, remainder2 = quotient.gf_divide_by_modulus(g1, 128)
    mi2 = quotient.multiplicative_inverse(g1)
    log.debug("int(Kc): {}".format(int(Kc)))
    try:
        assert int(mi2) == int(Kc)
    except Exception:
        if mi2 is not None:
            log.debug("int(mi2): {}".format(int(mi2)))
        else:
            log.debug("mi2 is None")
        log.debug("Fail mi2")
    try:
        assert int(mi) == int(Kc)
    except Exception:
        log.debug("int(mi): {}".format(int(mi)))
        log.debug("Fail mi")
    try:
        assert int(remainder2) == int(Kc)
    except Exception:
        log.debug("int(remainder2): {}".format(int(remainder2)))
        log.debug("Fail remainder2")
    try:
        assert int(quotient2) == int(Kc)
    except Exception:
        log.debug("int(quotient2): {}".format(int(quotient2)))
        log.debug("Fail quotient2")

    # one = BitVector(intVal=0x01, size=128)
    # r = Kc_prime.gf_MI(kkj, 128)
    # quotient, remainder = r.gf_divide_by_modulus(g1, 128)
    # r = Kc.gf_multiply_modular(one, g1, 128)
    # emsg = "{} Kc mod g1: {} is not equal to {}".format(name, int(r), int(Kc_mod_g1))
    # assert int(r) == int(Kc_mod_g1), emsg

    # r = g2.gf_multiply(Kc_mod_g1)
    # emsg = "{} g2 * Kc_mod_g1: {} is not equal to {}".format(name, int(r), int(Kc_prime))
    # assert int(r) == int(Kc_prime), emsg


def test_g1_g2():
    # NOTE: L=1
    g1 = BitVector(intVal=0x011D, size=128)
    g1_t = BitVector(intVal=G1[1], size=128)
    assert int(g1) == int(g1_t)
    g2 = BitVector(intVal=0x00E275A0ABD218D4CF928B9BBF6CB08F, size=128)
    g2_t = BitVector(intVal=G2[1], size=128)
    assert int(g2) == int(g2_t)

    # NOTE: L=2
    g1 = BitVector(intVal=0x0001003F, size=128)
    g1_t = BitVector(intVal=G1[2], size=128)
    assert int(g1) == int(g1_t)
    g2 = BitVector(intVal=0x01E3F63D7659B37F18C258CFF6EFEF, size=128)
    g2_t = BitVector(intVal=G2[2], size=128)
    assert int(g2) == int(g2_t)


def test_Kc_prime_bit_vec():

    log.debug("Kc_prime(x) = g2(x) (Kc(x) mod g1(x))")
    one = BitVector(intVal=0x01, size=128)

    # NOTE: L=1
    g1 = BitVector(intVal=G1[1], size=128)
    g2 = BitVector(intVal=G2[1], size=128)
    Kc = BitVector(intVal=0xA2B230A493F281BB61A85B82A9D4A30E, size=128)
    Kc_prime = BitVector(intVal=0x7AA16F3959836BA322049A7B87F1D8A5, size=128)
    Kc_mod_g1 = BitVector(intVal=0x9F, size=128)

    Kc_mod_g1_t = Kc.gf_multiply_modular(one, g1, 128)
    assert Kc_mod_g1_t == Kc_mod_g1
    # NOTE: mutiplication increase the size of the vector
    Kc_prime_t = g2.gf_multiply(Kc_mod_g1)[128:]
    assert Kc_prime_t == Kc_prime

    # NOTE: L=2
    g1 = BitVector(intVal=G1[2], size=128)
    g2 = BitVector(intVal=G2[2], size=128)
    Kc = BitVector(intVal=0x64E7DF78BB7CCAA4614331235B3222AD, size=128)
    Kc_mod_g1 = BitVector(intVal=0x00001FF0, size=128)
    Kc_prime = BitVector(intVal=0x142057BB0BCEAC4C58BD142E1E710A50, size=128)

    Kc_mod_g1_t = Kc.gf_multiply_modular(one, g1, 128)
    assert Kc_mod_g1_t == Kc_mod_g1
    # NOTE: mutiplication increase the size of the vector
    Kc_prime_t = g2.gf_multiply(Kc_mod_g1)[128:]
    assert Kc_prime_t == Kc_prime


def test_Kc_prime():
    """pag 1511 L1 means that Kc negotiation ended up with L=1"""

    Kc = bytearray.fromhex("a2b230a493f281bb61a85b82a9d4a30e")
    Kc_prime = bytearray.fromhex("7aa16f3959836ba322049a7b87f1d8a5")
    rv = Kc_to_Kc_prime(Kc, 1)
    log.debug("test_Kc_prime L=1 rv      : {}".format(repr(rv)))
    log.debug("test_Kc_prime L=1 Kc_prime: {}".format(repr(Kc_prime)))
    assert rv == Kc_prime

    Kc = bytearray.fromhex("64e7df78bb7ccaa4614331235b3222ad")
    Kc_prime = bytearray.fromhex("142057bb0bceac4c58bd142e1e710a50")
    rv = Kc_to_Kc_prime(Kc, 2)
    log.debug("test_Kc_prime L=2 rv      : {}".format(repr(rv)))
    log.debug("test_Kc_prime L=2 Kc_prime: {}".format(repr(Kc_prime)))
    assert rv == Kc_prime

    Kc = bytearray.fromhex("575e5156ba685dc6112124acedb2c179")
    Kc_prime = bytearray.fromhex("d56d0adb8216cb397fe3c5911ff95618")
    rv = Kc_to_Kc_prime(Kc, 3)
    log.debug("test_Kc_prime L=3 rv      : {}".format(repr(rv)))
    log.debug("test_Kc_prime L=3 Kc_prime: {}".format(repr(Kc_prime)))
    assert rv == Kc_prime

    Kc = bytearray.fromhex("8917b4fc403b6db21596b86d1cb8adab")
    Kc_prime = bytearray.fromhex("91910128b0e2f5eda132a03eaf3d8cda")
    rv = Kc_to_Kc_prime(Kc, 4)
    log.debug("test_Kc_prime L=4 rv      : {}".format(repr(rv)))
    log.debug("test_Kc_prime L=4 Kc_prime: {}".format(repr(Kc_prime)))
    assert rv == Kc_prime

    Kc = bytearray.fromhex("785c915bdd25b9c60102ab00b6cd2a68")
    Kc_prime = bytearray.fromhex("6fb5651ccb80c8d7ea1ee56df1ec5d02")
    rv = Kc_to_Kc_prime(Kc, 5)
    log.debug("test_Kc_prime L=5 rv      : {}".format(repr(rv)))
    log.debug("test_Kc_prime L=5 Kc_prime: {}".format(repr(Kc_prime)))
    assert rv == Kc_prime

    Kc = bytearray.fromhex("5e77d19f55ccd7d5798f9a323b83e5d8")
    Kc_prime = bytearray.fromhex("16096bcbafcf8def1d226a1b4d3f9a3d")
    rv = Kc_to_Kc_prime(Kc, 6)
    log.debug("test_Kc_prime L=6 rv      : {}".format(repr(rv)))
    log.debug("test_Kc_prime L=6 Kc_prime: {}".format(repr(Kc_prime)))
    assert rv == Kc_prime

    Kc = bytearray.fromhex("05454e038ddcfbe3ed024b2d92b7f54c")
    Kc_prime = bytearray.fromhex("50f9c0d4e3178da94a09fe0d34f67b0e")
    rv = Kc_to_Kc_prime(Kc, 7)
    log.debug("test_Kc_prime L=7 rv      : {}".format(repr(rv)))
    log.debug("test_Kc_prime L=7 Kc_prime: {}".format(repr(Kc_prime)))
    assert rv == Kc_prime

    Kc = bytearray.fromhex("7ce149fcf4b38ad72a5d8a41eb15ba31")
    Kc_prime = bytearray.fromhex("532c36d45d0954e0922989b6826f78dc")
    rv = Kc_to_Kc_prime(Kc, 8)
    log.debug("test_Kc_prime L=8 rv      : {}".format(repr(rv)))
    log.debug("test_Kc_prime L=8 Kc_prime: {}".format(repr(Kc_prime)))
    assert rv == Kc_prime

    Kc = bytearray.fromhex("5eeff7ca84fc27829c0517263df6f36e")
    Kc_prime = bytearray.fromhex("016313f60d3771cf7f8e4bb94aa6827d")
    rv = Kc_to_Kc_prime(Kc, 9)
    log.debug("test_Kc_prime L=9 rv      : {}".format(repr(rv)))
    log.debug("test_Kc_prime L=9 Kc_prime: {}".format(repr(Kc_prime)))
    assert rv == Kc_prime

    Kc = bytearray.fromhex("7b13846e88beb4de34e7160afd44dc65")
    Kc_prime = bytearray.fromhex("023bc1ec34a0029ef798dcfb618ba58d")
    rv = Kc_to_Kc_prime(Kc, 10)
    log.debug("test_Kc_prime L=10 rv      : {}".format(repr(rv)))
    log.debug("test_Kc_prime L=10 Kc_prime: {}".format(repr(Kc_prime)))
    assert rv == Kc_prime

    Kc = bytearray.fromhex("bda6de6c6e7d757e8dfe2d499a181193")
    Kc_prime = bytearray.fromhex("022e08a93aa51d8d2f93fa7885cc1f87")
    rv = Kc_to_Kc_prime(Kc, 11)
    log.debug("test_Kc_prime L=11 rv      : {}".format(repr(rv)))
    log.debug("test_Kc_prime L=11 Kc_prime: {}".format(repr(Kc_prime)))
    assert rv == Kc_prime

    Kc = bytearray.fromhex("e6483b1c2cdb10409a658f97c4efd90d")
    Kc_prime = bytearray.fromhex("030d752b216fe29bb880275cd7e6f6f9")
    rv = Kc_to_Kc_prime(Kc, 12)
    log.debug("test_Kc_prime L=12 rv      : {}".format(repr(rv)))
    log.debug("test_Kc_prime L=12 Kc_prime: {}".format(repr(Kc_prime)))
    assert rv == Kc_prime

    Kc = bytearray.fromhex("d79d281da22668476b223c46dc0ab9ee")
    Kc_prime = bytearray.fromhex("03f111389cebf91900b938084ac158aa")
    rv = Kc_to_Kc_prime(Kc, 13)
    log.debug("test_Kc_prime L=13 rv      : {}".format(repr(rv)))
    log.debug("test_Kc_prime L=13 Kc_prime: {}".format(repr(Kc_prime)))
    assert rv == Kc_prime

    Kc = bytearray.fromhex("cad9a65b9fca1c1da2320fcf7c4ae48e")
    Kc_prime = bytearray.fromhex("284840fdf1305f3c529f570376adf7cf")
    rv = Kc_to_Kc_prime(Kc, 14)
    log.debug("test_Kc_prime L=14 rv      : {}".format(repr(rv)))
    log.debug("test_Kc_prime L=14 Kc_prime: {}".format(repr(Kc_prime)))
    assert rv == Kc_prime

    Kc = bytearray.fromhex("21f0cc31049b7163d375e9e106029809")
    Kc_prime = bytearray.fromhex("7f10b53b6df84b94f22e566a3754a37e")
    rv = Kc_to_Kc_prime(Kc, 15)
    log.debug("test_Kc_prime L=15 rv      : {}".format(repr(rv)))
    log.debug("test_Kc_prime L=15 Kc_prime: {}".format(repr(Kc_prime)))
    assert rv == Kc_prime

    log.debug("e0_tests If L=16 then Kc_prime equals Kc")
    Kc = bytearray.fromhex("35ec8fc3d50ccd325f2fd907bde206de")
    Kc_prime = bytearray.fromhex("35ec8fc3d50ccd325f2fd907bde206de")
    rv = Kc_to_Kc_prime(Kc, 16)
    log.debug("test_Kc_prime L=16 rv      : {}".format(repr(rv)))
    log.debug("test_Kc_prime L=16 Kc_prime: {}".format(repr(Kc_prime)))
    assert Kc == Kc_prime
    assert rv == Kc_prime


def test_Kc_prime_entropy1():
    """Fix Kc vary L"""

    Kc = bytearray.fromhex("aaaabbbbccccddddeeee000011112222")
    rv = [i for i in range(18)]
    for i in range(1, 17):
        rv[i] = Kc_to_Kc_prime(Kc, i)
    log.info("test_Kc_prime_entropy1 Kc       : {}".format(repr(Kc)))
    log.info("test_Kc_prime_entropy1 L=1      : {}".format(repr(rv[1])))
    log.info("test_Kc_prime_entropy1 L=2      : {}".format(repr(rv[2])))
    log.info("test_Kc_prime_entropy1 L=3      : {}".format(repr(rv[3])))
    log.info("test_Kc_prime_entropy1 L=4      : {}".format(repr(rv[4])))
    log.info("test_Kc_prime_entropy1 L=5      : {}".format(repr(rv[5])))
    log.info("test_Kc_prime_entropy1 L=6      : {}".format(repr(rv[6])))
    log.info("test_Kc_prime_entropy1 L=7      : {}".format(repr(rv[7])))
    log.info("test_Kc_prime_entropy1 L=8      : {}".format(repr(rv[8])))
    log.info("test_Kc_prime_entropy1 L=9      : {}".format(repr(rv[9])))
    log.info("test_Kc_prime_entropy1 L=10     : {}".format(repr(rv[10])))
    log.info("test_Kc_prime_entropy1 L=11     : {}".format(repr(rv[11])))
    log.info("test_Kc_prime_entropy1 L=12     : {}".format(repr(rv[12])))
    log.info("test_Kc_prime_entropy1 L=13     : {}".format(repr(rv[13])))
    log.info("test_Kc_prime_entropy1 L=14     : {}".format(repr(rv[14])))
    log.info("test_Kc_prime_entropy1 L=15     : {}".format(repr(rv[15])))
    log.info("test_Kc_prime_entropy1 L=16     : {}".format(repr(rv[16])))


def test_Kc_prime_entropy2():
    """Fix L vary Kc Byte by Byte"""

    zero = bytearray.fromhex("00000000000000000000000000000000")
    almost_one = bytearray(
        "\x7f\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff"
    )
    Kc = bytearray.fromhex("00001111222233334444555566667777")
    # log.info('test_Kc_prime_entropy2 Kc    : {}'.format(repr(Kc)))

    L = 1
    for l in range(2, 17):
        L = l
        filename = "kcs/L{}-00001111222233334444555566667777.txt".format(L)
        with open(filename, mode="w") as fp:
            fp.write(
                "test_Kc_prime_entropy2 Kc                  :{}\n".format(repr(Kc))
            )
            for j in range(16):  # 0--15
                rv = {}
                zeros = []
                almost_ones = []
                BYTE_INDEX = j
                for i in range(256):  # 0..256
                    Kc[BYTE_INDEX] = i
                    # log.info('test_Kc_prime_entropy2 Kc[{}]: {}'.format(BYTE_INDEX, i))
                    rv[i] = Kc_to_Kc_prime(Kc, L)
                    if rv[i] == zero:
                        zeros.append(i)
                    elif rv[i] == almost_one:
                        almost_ones.append(i)

                fp.write(
                    "test_Kc_prime_entropy2 BEGIN BYTE_INDEX: {}\n".format(BYTE_INDEX)
                )
                # log.info('test_Kc_prime_entropy2 zeros : {}'.format(repr(zeros)))
                fp.write(
                    "test_Kc_prime_entropy2 zeros           : {}\n".format(repr(zeros))
                )
                # log.info('test_Kc_prime_entropy2 almost_ones : {}'.format(repr(almost_ones)))
                fp.write(
                    "test_Kc_prime_entropy2 almost_ones     : {}\n".format(
                        repr(almost_ones)
                    )
                )
                rvp = pprint.pformat(rv, 4)
                # log.info('test_Kc_prime_entropy2 Kc        : {}'.format(rvp))
                fp.write("test_Kc_prime_entropy2 Kc_prime        : {}\n".format(rvp))
                fp.write(
                    "test_Kc_prime_entropy2 END BYTE_INDEX  : {}\n\n".format(BYTE_INDEX)
                )
                print(
                    "{} BYTE_INDEX {} zeros: {}, almost_ones: {}".format(
                        filename, j, zeros, almost_ones
                    )
                )
        # print('Output of: cat {}'.format(filename))
        # call(["cat", filename])


if __name__ == "__main__":

    test_g1_g2()
    test_Kc_prime_bit_vec()
    test_Kc_prime()
    log.setLevel(logging.INFO)

    # test_Kc_prime_entropy1()
    # test_Kc_prime_entropy2()
