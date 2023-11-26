"""
kdf_tests.py

For LSC, the BTADDR is the Bluetooth address of the last device sending SRES,
typically the slave.

"""
import logging

from kdf import kdf
from constants import log
from es import bytearray_to_hexstring

log.setLevel(logging.INFO)


def test_kdf_1():
    """Test vector from the experiments.

    Master: devboard, Slave: Nexus XL

    LK copy pasted from Linux folder

    BTADD of the slave (victim) copied from hciconfig

    KcPrime copied from InternalBlue memory dump

    Do *NOT* remove const init code


    """

    # NOTE: 1 bytes of entropy
    LK = bytearray.fromhex("97773CA35380352AEBB317027C360BEE")
    AU_RAND = bytearray.fromhex("00000000000000000000000000000000")
    EN_RAND = bytearray.fromhex("00000000000000000000000000000000")
    BTADDR = bytearray.fromhex("404E3604F1F9")
    ComputedKcPrime = kdf(LK, AU_RAND, EN_RAND, BTADDR, 1)
    KcPrime = bytearray.fromhex("61d97e3717259fa931a45741ebc4010f")
    log.info("01 Comp: {}".format(bytearray_to_hexstring(ComputedKcPrime)))
    log.info("01 Expe: {}".format(bytearray_to_hexstring(KcPrime)))
    assert KcPrime == ComputedKcPrime

    # NOTE: 2 bytes of entropy
    LK = bytearray.fromhex("97773CA35380352AEBB317027C360BEE")
    AU_RAND = bytearray.fromhex("00000000000000000000000000000000")
    EN_RAND = bytearray.fromhex("00000000000000000000000000000000")
    BTADDR = bytearray.fromhex("404E3604F1F9")
    ComputedKcPrime = kdf(LK, AU_RAND, EN_RAND, BTADDR, 2)
    KcPrime = bytearray.fromhex("f899f6f9f2fd3c7580712e971bb65946")
    log.info("02 Comp: {}".format(bytearray_to_hexstring(ComputedKcPrime)))
    log.info("02 Expe: {}".format(bytearray_to_hexstring(KcPrime)))
    assert KcPrime == ComputedKcPrime

    # NOTE: 3 bytes of entropy
    LK = bytearray.fromhex("97773CA35380352AEBB317027C360BEE")
    AU_RAND = bytearray.fromhex("00000000000000000000000000000000")
    EN_RAND = bytearray.fromhex("00000000000000000000000000000000")
    BTADDR = bytearray.fromhex("404E3604F1F9")
    ComputedKcPrime = kdf(LK, AU_RAND, EN_RAND, BTADDR, 3)
    KcPrime = bytearray.fromhex("6a516d6cf3b0c1e2d7fa516e49a185fb")
    log.info("03 Comp: {}".format(bytearray_to_hexstring(ComputedKcPrime)))
    log.info("03 Expe: {}".format(bytearray_to_hexstring(KcPrime)))
    assert KcPrime == ComputedKcPrime

    # NOTE: 4 bytes of entropy
    LK = bytearray.fromhex("97773CA35380352AEBB317027C360BEE")
    AU_RAND = bytearray.fromhex("00000000000000000000000000000000")
    EN_RAND = bytearray.fromhex("00000000000000000000000000000000")
    BTADDR = bytearray.fromhex("404E3604F1F9")
    ComputedKcPrime = kdf(LK, AU_RAND, EN_RAND, BTADDR, 4)
    KcPrime = bytearray.fromhex("92a7d1695f9fa949a58093f07cb5cfd2")
    log.info("04 Comp: {}".format(bytearray_to_hexstring(ComputedKcPrime)))
    log.info("04 Expe: {}".format(bytearray_to_hexstring(KcPrime)))
    assert KcPrime == ComputedKcPrime

    # NOTE: 5 byte of entropy
    LK = bytearray.fromhex("97773CA35380352AEBB317027C360BEE")
    AU_RAND = bytearray.fromhex("00000000000000000000000000000000")
    EN_RAND = bytearray.fromhex("00000000000000000000000000000000")
    BTADDR = bytearray.fromhex("404E3604F1F9")
    ComputedKcPrime = kdf(LK, AU_RAND, EN_RAND, BTADDR, 5)
    KcPrime = bytearray.fromhex("e704580fea5d97b06ca67a0a7fd232b5")
    log.info("05 Comp: {}".format(bytearray_to_hexstring(ComputedKcPrime)))
    log.info("05 Expe: {}".format(bytearray_to_hexstring(KcPrime)))
    assert KcPrime == ComputedKcPrime

    # NOTE: 6 bytes of entropy
    LK = bytearray.fromhex("97773CA35380352AEBB317027C360BEE")
    AU_RAND = bytearray.fromhex("00000000000000000000000000000000")
    EN_RAND = bytearray.fromhex("00000000000000000000000000000000")
    BTADDR = bytearray.fromhex("404E3604F1F9")
    ComputedKcPrime = kdf(LK, AU_RAND, EN_RAND, BTADDR, 6)
    KcPrime = bytearray.fromhex("89af8d19e226c9abc164c371e11fe90e")
    log.info("06 Comp: {}".format(bytearray_to_hexstring(ComputedKcPrime)))
    log.info("06 Expe: {}".format(bytearray_to_hexstring(KcPrime)))
    assert KcPrime == ComputedKcPrime

    # NOTE: 7 bytes of entropy
    LK = bytearray.fromhex("97773CA35380352AEBB317027C360BEE")
    AU_RAND = bytearray.fromhex("00000000000000000000000000000000")
    EN_RAND = bytearray.fromhex("00000000000000000000000000000000")
    BTADDR = bytearray.fromhex("404E3604F1F9")
    ComputedKcPrime = kdf(LK, AU_RAND, EN_RAND, BTADDR, 7)
    KcPrime = bytearray.fromhex("cc2de64988a54ec6fcd1edeb4fa08521")
    log.info("07 Comp: {}".format(bytearray_to_hexstring(ComputedKcPrime)))
    log.info("07 Expe: {}".format(bytearray_to_hexstring(KcPrime)))
    assert KcPrime == ComputedKcPrime

    # NOTE: 8 bytes of entropy
    LK = bytearray.fromhex("97773CA35380352AEBB317027C360BEE")
    AU_RAND = bytearray.fromhex("00000000000000000000000000000000")
    EN_RAND = bytearray.fromhex("00000000000000000000000000000000")
    BTADDR = bytearray.fromhex("404E3604F1F9")
    ComputedKcPrime = kdf(LK, AU_RAND, EN_RAND, BTADDR, 8)
    KcPrime = bytearray.fromhex("fde6d783b5d97f430c3464966f05e400")
    log.info("08 Comp: {}".format(bytearray_to_hexstring(ComputedKcPrime)))
    log.info("08 Expe: {}".format(bytearray_to_hexstring(KcPrime)))
    assert KcPrime == ComputedKcPrime

    # NOTE: 9 bytes of entropy
    LK = bytearray.fromhex("97773CA35380352AEBB317027C360BEE")
    AU_RAND = bytearray.fromhex("00000000000000000000000000000000")
    EN_RAND = bytearray.fromhex("00000000000000000000000000000000")
    BTADDR = bytearray.fromhex("404E3604F1F9")
    ComputedKcPrime = kdf(LK, AU_RAND, EN_RAND, BTADDR, 9)
    KcPrime = bytearray.fromhex("f3c64abe37c115680496a319e8743700")
    log.info("09 Comp: {}".format(bytearray_to_hexstring(ComputedKcPrime)))
    log.info("09 Expe: {}".format(bytearray_to_hexstring(KcPrime)))
    assert KcPrime == ComputedKcPrime

    # NOTE: 10 bytes of entropy
    LK = bytearray.fromhex("97773CA35380352AEBB317027C360BEE")
    AU_RAND = bytearray.fromhex("00000000000000000000000000000000")
    EN_RAND = bytearray.fromhex("00000000000000000000000000000000")
    BTADDR = bytearray.fromhex("404E3604F1F9")
    ComputedKcPrime = kdf(LK, AU_RAND, EN_RAND, BTADDR, 10)
    KcPrime = bytearray.fromhex("98dc7701d413fc8ccdf9f0879f4ce900")
    log.info("10 Comp: {}".format(bytearray_to_hexstring(ComputedKcPrime)))
    log.info("10 Expe: {}".format(bytearray_to_hexstring(KcPrime)))
    assert KcPrime == ComputedKcPrime

    # NOTE: 11 bytes of entropy
    LK = bytearray.fromhex("97773CA35380352AEBB317027C360BEE")
    AU_RAND = bytearray.fromhex("00000000000000000000000000000000")
    EN_RAND = bytearray.fromhex("00000000000000000000000000000000")
    BTADDR = bytearray.fromhex("404E3604F1F9")
    ComputedKcPrime = kdf(LK, AU_RAND, EN_RAND, BTADDR, 11)
    KcPrime = bytearray.fromhex("d7e37ea76572f10fe00e4c5da2a9a405")
    log.info("11 Comp: {}".format(bytearray_to_hexstring(ComputedKcPrime)))
    log.info("11 Expe: {}".format(bytearray_to_hexstring(KcPrime)))
    assert KcPrime == ComputedKcPrime

    # NOTE: 12 bytes of entropy
    LK = bytearray.fromhex("97773CA35380352AEBB317027C360BEE")
    AU_RAND = bytearray.fromhex("00000000000000000000000000000000")
    EN_RAND = bytearray.fromhex("00000000000000000000000000000000")
    BTADDR = bytearray.fromhex("404E3604F1F9")
    ComputedKcPrime = kdf(LK, AU_RAND, EN_RAND, BTADDR, 12)
    KcPrime = bytearray.fromhex("4031012b857b8b9e193efc5878f04c05")
    log.info("12 Comp: {}".format(bytearray_to_hexstring(ComputedKcPrime)))
    log.info("12 Expe: {}".format(bytearray_to_hexstring(KcPrime)))
    assert KcPrime == ComputedKcPrime

    # NOTE: 13 bytes of entropy
    LK = bytearray.fromhex("97773CA35380352AEBB317027C360BEE")
    AU_RAND = bytearray.fromhex("00000000000000000000000000000000")
    EN_RAND = bytearray.fromhex("00000000000000000000000000000000")
    BTADDR = bytearray.fromhex("404E3604F1F9")
    ComputedKcPrime = kdf(LK, AU_RAND, EN_RAND, BTADDR, 13)
    KcPrime = bytearray.fromhex("664e0a617f03f1e88751629e5647d209")
    log.info("13 Comp: {}".format(bytearray_to_hexstring(ComputedKcPrime)))
    log.info("13 Expe: {}".format(bytearray_to_hexstring(KcPrime)))
    assert KcPrime == ComputedKcPrime

    # NOTE: 14 bytes of entropy
    LK = bytearray.fromhex("97773CA35380352AEBB317027C360BEE")
    AU_RAND = bytearray.fromhex("00000000000000000000000000000000")
    EN_RAND = bytearray.fromhex("00000000000000000000000000000000")
    BTADDR = bytearray.fromhex("404E3604F1F9")
    ComputedKcPrime = kdf(LK, AU_RAND, EN_RAND, BTADDR, 14)
    KcPrime = bytearray.fromhex("0c3880e2b92d6f6fc402f7266e5b110e")
    log.info("14 Comp: {}".format(bytearray_to_hexstring(ComputedKcPrime)))
    log.info("14 Expe: {}".format(bytearray_to_hexstring(KcPrime)))
    assert KcPrime == ComputedKcPrime

    # NOTE: 15 bytes of entropy
    LK = bytearray.fromhex("97773CA35380352AEBB317027C360BEE")
    AU_RAND = bytearray.fromhex("00000000000000000000000000000000")
    EN_RAND = bytearray.fromhex("00000000000000000000000000000000")
    BTADDR = bytearray.fromhex("404E3604F1F9")
    ComputedKcPrime = kdf(LK, AU_RAND, EN_RAND, BTADDR, 15)
    KcPrime = bytearray.fromhex("a85b53e7da0c8b8780bfd28de1529013")
    log.info("15 Comp: {}".format(bytearray_to_hexstring(ComputedKcPrime)))
    log.info("15 Expe: {}".format(bytearray_to_hexstring(KcPrime)))
    assert KcPrime == ComputedKcPrime

    # NOTE: 16 bytes of entropy
    LK = bytearray.fromhex("97773CA35380352AEBB317027C360BEE")
    AU_RAND = bytearray.fromhex("00000000000000000000000000000000")
    EN_RAND = bytearray.fromhex("00000000000000000000000000000000")
    BTADDR = bytearray.fromhex("404E3604F1F9")
    ComputedKcPrime = kdf(LK, AU_RAND, EN_RAND, BTADDR, 16)
    KcPrime = bytearray.fromhex("674444bf8008b7d11e30d37243392579")
    log.info("16 Comp: {}".format(bytearray_to_hexstring(ComputedKcPrime)))
    log.info("16 Expe: {}".format(bytearray_to_hexstring(KcPrime)))
    assert KcPrime == ComputedKcPrime


def test_kdf_2():
    """
    Looks like when entropy is 9 last byte is 0x00 with high probability
    """

    LK = bytearray.fromhex("97773CA35380352AEBB317027C360BAA")
    AU_RAND = bytearray.fromhex("00000000000000000000000000000000")
    EN_RAND = bytearray.fromhex("00000000000000000000000000000000")
    BTADDR = bytearray.fromhex("404E3604F1F9")
    ComputedKcPrime = kdf(LK, AU_RAND, EN_RAND, BTADDR, 9)
    log.info("09 Comp: {}".format(bytearray_to_hexstring(ComputedKcPrime)))

    LK = bytearray.fromhex("AA773CA35380352AEBB317027C360BAA")
    AU_RAND = bytearray.fromhex("00000000000000000000000000000000")
    EN_RAND = bytearray.fromhex("00000000000000000000000000000000")
    BTADDR = bytearray.fromhex("404E3604F1F9")
    ComputedKcPrime = kdf(LK, AU_RAND, EN_RAND, BTADDR, 9)
    log.info("09 Comp: {}".format(bytearray_to_hexstring(ComputedKcPrime)))

    LK = bytearray.fromhex("AA7735A353803523EBB317027C360fAA")
    AU_RAND = bytearray.fromhex("00000000000000000000000000000000")
    EN_RAND = bytearray.fromhex("00000000000000000000000000000000")
    BTADDR = bytearray.fromhex("404E3604F1F9")
    ComputedKcPrime = kdf(LK, AU_RAND, EN_RAND, BTADDR, 9)
    log.info("09 Comp: {}".format(bytearray_to_hexstring(ComputedKcPrime)))


def test_kdf_3():
    """
    From experiments
        Master: Pixel XL, Slave: Devboard
    """

    LK = bytearray.fromhex("97773CA35380352AEBB317027C360BEE")
    AU_RAND = bytearray.fromhex("459a3212d1452c6a1b793789fda175f6")
    EN_RAND = bytearray.fromhex("00000000000000000000000000000000")
    BTADDR = bytearray.fromhex("20819A093E41")
    ComputedKcPrime = kdf(LK, AU_RAND, EN_RAND, BTADDR, 9)
    KcPrime = bytearray.fromhex("dd4a4b89503d20a9bc4a6a8887abf801")
    log.info("09 Comp: {}".format(bytearray_to_hexstring(ComputedKcPrime)))
    log.info("09 Expe: {}".format(bytearray_to_hexstring(KcPrime)))
    assert KcPrime == ComputedKcPrime


def test_kdf_4():
    """
    From experiments
        Victim Pixel 6
    """

    LK = bytearray.fromhex("F80FA88FF3DC39F659F1155F0B4D249E")
    AU_RAND = bytearray.fromhex("00000000000000000000000000000000")
    EN_RAND = bytearray.fromhex("00000000000000000000000000000000")
    BTADDR = bytearray.fromhex("DCE55B277196")

    ComputedKcPrime = kdf(LK, AU_RAND, EN_RAND, BTADDR, 7)
    KcPrime = bytearray.fromhex("455ef0869087fe7a5a5683ef24f7387c")
    log.info("07 Comp: {}".format(bytearray_to_hexstring(ComputedKcPrime)))
    log.info("07 Expe: {}".format(bytearray_to_hexstring(KcPrime)))
    assert KcPrime == ComputedKcPrime


if __name__ == "__main__":

    print("")
    test_kdf_1()
    print("")
    test_kdf_2()
    print("")
    test_kdf_3()

    print("")
    test_kdf_4()
