#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
h.py

Ar and Ar_prime uses SAFER+

SAFER+ is an enhanced
version of an existing 64-bit block cipher SAFER-SK128

bitstring.BitArray API:

    s = BitArray()
    s.append('0x000001b3')  # the sequence_header_code
    s.append('uint:12=352') # 12 bit unsigned integer
    s.append('uint:12=288')
    # s[0] contains the MOST SIGNIFICANT BIT

Tested by e3_tests.py

"""

from bitstring import BitArray
from constants import Ar_KEY_LEN, BTADD_LEN, COF_LEN, log, EXP_45


def H(K, I_one, I_two, L):
    """Hash function used in e1 and e3.

    e1 computes SRES and ACO

    e3 computes Kc

    Returns Keys, Ar, KeysPrime, ArPrime, Out

    """
    assert len(K) == Ar_KEY_LEN and type(K) == bytearray
    assert len(I_one) == Ar_KEY_LEN and type(I_one) == bytearray
    assert (len(I_two) == COF_LEN or len(I_two) == BTADD_LEN) and type(
        I_two
    ) == bytearray

    log.debug("H(K, I_one, I_two, {})".format(L))

    Keys = key_sched(K)
    K_tilda = K_to_K_tilda(K)
    KeysPrime = key_sched(K_tilda)

    I_two_ext = E(I_two, L)
    log.debug("H I_two    : {}".format(repr(I_two)))
    log.debug("H I_two_ext: {}".format(repr(I_two_ext)))

    Ar = Ar_rounds(Keys, I_one, is_prime=False)

    pre_ar_prime_inp = xor_bytes(Ar[10], I_one)
    log.debug("H pre_ar_prime_inp: {}".format(repr(pre_ar_prime_inp)))
    ar_prime_inp = add_bytes_mod256(I_two_ext, pre_ar_prime_inp)
    log.debug("H ar_prime_inp: {}".format(repr(ar_prime_inp)))
    ArPrime = Ar_rounds(KeysPrime, ar_prime_inp, is_prime=True)

    # NOTE: either Kc or SRES || ACO
    Out = ArPrime[10]

    return Keys, Ar, KeysPrime, ArPrime, Out


def Ar_rounds(Keys, inp, is_prime):
    """
    Ar[0] = None, not used
    Ar[1] = inp = round1
    Ar[2..9] = round1..8
    Ar[10] = extra add_one after last round
    """
    assert len(Keys) == 18 and type(Keys[1]) == bytearray
    assert len(inp) == Ar_KEY_LEN and type(inp) == bytearray

    # NOTE: Ar[0..9]
    Ar = [i for i in range(11)]
    Ar[0] = None

    # NOTE: deep copy here
    Ar[1] = bytearray(inp[i] for i in range(16))
    log.debug("Ar_rounds is_prime: {}, Ar[1]: {}".format(is_prime, repr(Ar[1])))

    # NOTE: temp holds the current input value
    temp = bytearray(inp[i] for i in range(16))

    for r in range(1, 9):  # 1..7
        # NOTE: input of round1 is add_one to input of round3
        if is_prime and r == 3:
            temp = add_one(temp, Ar[1])
            # log.debug('Ar_rounds is_prime: {}, added: {}'.format(is_prime, repr(temp)))

        rv1 = add_one(temp, Keys[2 * r - 1])  # odd keys use add_one
        rv2 = nonlin_subs(rv1)
        rv3 = add_two(rv2, Keys[2 * r])  # even keys use add_two

        rv4 = PHTs(rv3)
        rv5 = PERMUTE(rv4)

        rv6 = PHTs(rv5)
        rv7 = PERMUTE(rv6)

        rv8 = PHTs(rv7)
        rv9 = PERMUTE(rv8)

        rv10 = PHTs(rv9)

        temp = rv10
        Ar[r + 1] = rv10
        # log.debug('Ar_rounds is_prime: {}, Ar[{}]: {}'.format(is_prime, r+1, repr(Ar[r+1])))

    Ar[10] = add_one(Ar[9], Keys[17])
    # log.debug('Ar_rounds is_prime: {}, Ar[10]: {}'.format(is_prime, repr(Ar[9])))
    emsg = "Ar_rounds len(Ar) is {}, it should be {}".format(len(Ar), 10)
    assert len(Ar) == 11, emsg

    return Ar


def add_one(l, r):
    """Applied when subkey index is odd, including K[17]."""

    assert type(l) == bytearray and len(l) == Ar_KEY_LEN
    assert type(r) == bytearray and len(r) == Ar_KEY_LEN

    rv = bytearray(16)
    for i in range(16):
        if i in [0, 3, 4, 7, 8, 11, 12, 15]:
            rv[i] = l[i] ^ r[i]
        else:
            rv[i] = (l[i] + r[i]) % 256

    assert len(rv) == Ar_KEY_LEN
    return rv


def add_two(l, r):
    """Applied when subkey index is even."""

    assert type(l) == bytearray and len(l) == Ar_KEY_LEN
    assert type(r) == bytearray and len(r) == Ar_KEY_LEN

    rv = bytearray(16)
    for i in range(16):
        if i in [0, 3, 4, 7, 8, 11, 12, 15]:
            rv[i] = (l[i] + r[i]) % 256
        else:
            rv[i] = l[i] ^ r[i]

    assert len(rv) == Ar_KEY_LEN
    return rv


def nonlin_subs(inp):
    """e(xponential) and l(og) non linear subs."""
    assert type(inp) == bytearray and len(inp) == Ar_KEY_LEN

    rv = bytearray(16)
    for i in range(16):
        if i in [0, 3, 4, 7, 8, 11, 12, 15]:
            rv[i] = EXP_45[inp[i]]
        else:
            rv[i] = EXP_45.index(inp[i])

    assert len(rv) == Ar_KEY_LEN
    return rv


def PHT(x, y):
    """Pseudo-Hadamard transform"""

    assert type(x) == int
    assert type(y) == int

    rv_x = (2 * x + y) % 256
    rv_y = (x + y) % 256

    return rv_x, rv_y


def PHTs(inp):
    assert type(inp) == bytearray and len(inp) == Ar_KEY_LEN

    rv = bytearray(16)
    for i in [0, 2, 4, 6, 8, 10, 12, 14]:
        rv[i], rv[i + 1] = PHT(inp[i], inp[i + 1])

    assert len(rv) == Ar_KEY_LEN
    return rv


def PERMUTE(inp):
    """Armenian permutation."""

    assert type(inp) == bytearray
    assert len(inp) == Ar_KEY_LEN

    permuted_inp = bytearray()

    permuted_inp.append(inp[8])
    permuted_inp.append(inp[11])
    permuted_inp.append(inp[12])
    permuted_inp.append(inp[15])
    permuted_inp.append(inp[2])
    permuted_inp.append(inp[1])
    permuted_inp.append(inp[6])
    permuted_inp.append(inp[5])
    permuted_inp.append(inp[10])
    permuted_inp.append(inp[9])
    permuted_inp.append(inp[14])
    permuted_inp.append(inp[13])
    permuted_inp.append(inp[0])
    permuted_inp.append(inp[7])
    permuted_inp.append(inp[4])
    permuted_inp.append(inp[3])

    assert len(permuted_inp) == Ar_KEY_LEN
    return permuted_inp


def key_sched(key):
    emsg = "key_sched key len is {}, it should be {}".format(len(key), Ar_KEY_LEN)
    assert len(key) == Ar_KEY_LEN, emsg

    Keys = [i for i in range(18)]
    Keys[0] = None  # Keys[0] is not used

    B = biases()

    # NOTE: XOR of all Bytes
    byte_16 = 0
    for i in range(16):
        byte_16 ^= key[i]
    # log.debug('key_sched byte_16: {}'.format(byte_16))
    # NOTE: deep copy here
    presel_k1 = bytearray(key[i] for i in range(16))
    presel_k1.append(byte_16)
    # log.debug('key_sched presel_k1: {}'.format(repr(presel_k1)))
    emsg = "key_sched presel_k1 len is {}, it should be {}".format(
        len(presel_k1), Ar_KEY_LEN + 1
    )
    assert len(presel_k1) == Ar_KEY_LEN + 1, emsg
    k1 = select(1, presel_k1)
    emsg = "key_sched k1 len is {}, it should be {}".format(len(k1), Ar_KEY_LEN)
    assert len(k1) == Ar_KEY_LEN, emsg
    Keys[1] = k1
    # log.debug('key_sched k1: {}'.format(repr(k1)))
    # presel_k2 = rotate(presel_k1)
    # pre_k2 = select('k2', presel_k2)
    # Keys[2] = add_bytes_mod256(pre_k2, B[2])
    # presel_k3 = rotate(presel_k2)
    # pre_k3 = select('k3', presel_k3)
    # Keys[3] = add_bytes_mod256(pre_k3, B[3])
    presel_old = presel_k1
    for N in range(2, 18):
        presel = rotate(presel_old)
        pre_k = select(N, presel)
        Keys[N] = add_bytes_mod256(pre_k, B[N])
        presel_old = presel

    return Keys


def select(what, key):

    if what == 1:
        selected_key = key[0:16]
    elif what == 2:
        selected_key = key[1:]
    elif what == 3:
        selected_key = key[2:]
        selected_key.append(key[0])
    elif what == 4:
        selected_key = key[3:]
        selected_key.extend(key[:2])
    elif what == 5:
        selected_key = key[4:]
        selected_key.extend(key[:3])
    elif what == 6:
        selected_key = key[5:]
        selected_key.extend(key[:4])
    elif what == 7:
        selected_key = key[6:]
        selected_key.extend(key[:5])
    elif what == 8:
        selected_key = key[7:]
        selected_key.extend(key[:6])
    elif what == 9:
        selected_key = key[8:]
        selected_key.extend(key[:7])
    elif what == 10:
        selected_key = key[9:]
        selected_key.extend(key[:8])
    elif what == 11:
        selected_key = key[10:]
        selected_key.extend(key[:9])
    elif what == 12:
        selected_key = key[11:]
        selected_key.extend(key[:10])
    elif what == 13:
        selected_key = key[12:]
        selected_key.extend(key[:11])
    elif what == 14:
        selected_key = key[13:]
        selected_key.extend(key[:12])
    elif what == 15:
        selected_key = key[14:]
        selected_key.extend(key[:13])
    elif what == 16:
        selected_key = key[15:]
        selected_key.extend(key[:14])
    elif what == 17:
        selected_key = key[16:]
        selected_key.extend(key[:15])
    else:
        log.error("select what: {} is not supported".format(what))
        return None
    emsg = "select selected_key len is {}, it should be {}".format(
        len(selected_key), Ar_KEY_LEN
    )

    assert len(selected_key) == Ar_KEY_LEN, emsg
    return selected_key


def biases():
    """Returns a list of bytearrays biases.

    These are constants and can be pre-computed:

    biases B[2]:  bytearray(b'F\x97\xb1\xba\xa3\xb7\x10\n\xc57\xb3\xc9Z(\xacd')
    biases B[3]:  bytearray(b'\xec\xab\xaa\xc6g\x95X\r\xf8\x9a\xf6nf\xdc\x05=')
    biases B[4]:  bytearray(b'\x8a\xc3\xd8\x89j\xe96IC\xbf\xeb\xd4\x96\x9bh\xa0')
    biases B[5]:  bytearray(b']W\x92\x1f\xd5q\\\xbb"\xc1\xbe{\xbc\x99c\x94')
    biases B[6]:  bytearray(b'*a\xb842\x19\xfd\xfb\x17@\xe6Q\x1dAD\x8f')
    biases B[7]:  bytearray(b'\xdd\x04\x80\xde\xe71\xd6\x7f\x01\xa2\xf79\xdao#\xca')
    biases B[8]:  bytearray(b':\xd0\x1c\xd10>\x12\xa1\xcd\x0f\xe0\xa8\xaf\x82Y,')
    biases B[9]:  bytearray(b'}\xad\xb2\xef\xc2\x87\xceu\x06\x13\x02\x90O.r3')
    biases B[10]: bytearray(b"\xc0\x8d\xcf\xa9\x81\xe2\xc4\'/lz\x9fR\xe1\x158")
    biases B[11]: bytearray(b'\xfcB\xc7\x08\xe4\tU^\x8c\x14v`\xff\xdf\xd7')
    biases B[12]: bytearray(b'\xfa\x0b!\x00\x1a\xf9\xa6\xb9\xe8\x9ebL\xd9\x91P\xd2')
    biases B[13]: bytearray(b'\x18\xb4\x07\x84\xea[\xa4\xc8\x0e\xcbHiKN\x9c5')
    biases B[14]: bytearray(b'EMT\xe5%<\x0cJ\x8b?\xcc\xa7\xdbk\xae\xf4')
    biases B[15]: bytearray(b'-\xf3|m\x9d\xb5&t\xf2\x93S\xb0\xf0\x11\xed\x83')
    biases B[16]: bytearray(b'\xb6\x03\x16s;\x1e\x8ep\xbd\x86\x1bG~$V\xf1')
    biases B[17]: bytearray(b'\x88F\x97\xb1\xba\xa3\xb7\x10\n\xc57\xb3\xc9Z(\xac')

    """

    B = [i for i in range(18)]
    B[0] = None  # not used
    B[1] = None  # not used

    # B[2] = bytearray()
    # N = 2
    # for i in range(16):
    #     int_val = ((45**(45**(17*N+i+1) % 257)) % 257) % 256
    #     B[2].append(int_val)
    # log.debug('biases B[2]: {}'.format(repr(B[2])))
    # assert len(B[2]) == Ar_KEY_LEN

    # B[3] = bytearray()
    # N=3
    # for i in range(16):
    #     int_val = ((45**(45**(17*N+i+1) % 257)) % 257) % 256
    #     B[3].append(int_val)
    # log.debug('biases B[3]: {}'.format(repr(B[3])))
    # assert len(B[3]) == Ar_KEY_LEN

    for N in range(2, 18):
        B[N] = bytearray()
        for i in range(16):
            int_val = ((45 ** (45 ** (17 * N + i + 1) % 257)) % 257) % 256
            B[N].append(int_val)
        # log.debug('biases B[{}]: {}'.format(N, repr(B[N])))
        assert len(B[N]) == Ar_KEY_LEN

    return B


def rotate(key):
    """ "Each Byte is rotated 3 positions on the left (not shifted)."""
    assert len(key) == Ar_KEY_LEN + 1 and type(key) == bytearray

    rotated_key = bytearray()
    for i in range(0, 17):
        byte = BitArray(key[i : i + 1])
        assert len(byte.bin) == 8
        # log.debug('rotate {} byte: {}, {}'.format(i, byte.bin, byte.uint))
        # rotated_byte = byte << 3
        rotated_byte = byte
        rotated_byte.rol(3)
        assert len(rotated_byte.bin) == 8
        # log.debug('rotate {} rotated_byte: {}, {}'.format(i, rotated_byte.bin, rotated_byte.uint))
        # NOTE: byte.uint is unsigned, byte.int is signed
        rotated_key.append(rotated_byte.uint)

    # log.debug('rotate rotated_key: {}'.format(repr(rotated_key)))
    assert len(rotated_key) == Ar_KEY_LEN + 1
    return rotated_key


def add_bytes_mod256(l, r):
    """Sixteen bytewise additions mod 256 .

    Used to produce input to for ArPrime
    """
    assert type(l) == bytearray
    assert len(l) == Ar_KEY_LEN
    assert type(r) == bytearray
    assert len(r) == Ar_KEY_LEN

    rv = bytearray()
    for i in range(16):
        rv.append((l[i] + r[i]) % 256)

    assert len(rv) == Ar_KEY_LEN
    return rv


def xor_bytes(l, r):
    """Sixteen bytewise XOR.

    Used to produce input to for ArPrime
    """
    assert type(l) == bytearray
    assert len(l) == Ar_KEY_LEN
    assert type(r) == bytearray
    assert len(r) == Ar_KEY_LEN

    rv = bytearray()
    for i in range(16):
        rv.append(l[i] ^ r[i])

    assert len(rv) == Ar_KEY_LEN
    return rv


def K_to_K_tilda(K):
    """(EQ 15) p 1676 Accepts and returns a bytearray"""
    emsg1 = "K_to_K_tilda K len is {}, it should be {}".format(len(K), Ar_KEY_LEN)
    assert len(K) == Ar_KEY_LEN, emsg1
    emsg2 = "K_to_K_tilda K type is {}, it should be a bytearray".format(type(K))
    assert type(K) == bytearray, emsg2

    K_tilda = bytearray()
    K_tilda.append((K[0] + 233) % 256)
    K_tilda.append(K[1] ^ 229)
    K_tilda.append((K[2] + 223) % 256)
    K_tilda.append(K[3] ^ 193)
    K_tilda.append((K[4] + 179) % 256)
    K_tilda.append(K[5] ^ 167)
    K_tilda.append((K[6] + 149) % 256)
    K_tilda.append(K[7] ^ 131)
    K_tilda.append(K[8] ^ 233)
    K_tilda.append((K[9] + 229) % 256)
    K_tilda.append(K[10] ^ 223)
    K_tilda.append((K[11] + 193) % 256)
    K_tilda.append(K[12] ^ 179)
    K_tilda.append((K[13] + 167) % 256)
    K_tilda.append(K[14] ^ 149)
    K_tilda.append((K[15] + 131) % 256)
    log.debug("K_to_K_tilda K_tilda: {}".format(repr(K_tilda)))

    assert len(K_tilda) == Ar_KEY_LEN
    return K_tilda


def K_to_K_tilda_str(K):
    """(EQ 15) p 1676 Accepts and returns a str"""
    emsg1 = "K_to_K_tilda K len is {}. it should be {}".format(len(K), Ar_KEY_LEN)
    assert len(K) == Ar_KEY_LEN, emsg1
    emsg2 = "K_to_K_tilda K type is {}. it should be {}".format(type(K), str)
    assert type(K) == str, emsg2

    K_tilda = ""
    K_tilda += chr((ord(K[0]) + 233) % 256)
    K_tilda += chr((ord(K[1]) ^ 229))
    K_tilda += chr((ord(K[2]) + 223) % 256)
    K_tilda += chr((ord(K[3]) ^ 193))
    K_tilda += chr((ord(K[4]) + 179) % 256)
    K_tilda += chr((ord(K[5]) ^ 167))
    K_tilda += chr((ord(K[6]) + 149) % 256)
    K_tilda += chr((ord(K[7]) ^ 131))
    K_tilda += chr((ord(K[8]) ^ 233))
    K_tilda += chr((ord(K[9]) + 229) % 256)
    K_tilda += chr((ord(K[10]) ^ 223))
    K_tilda += chr((ord(K[11]) + 193) % 256)
    K_tilda += chr((ord(K[12]) ^ 179))
    K_tilda += chr((ord(K[13]) + 167) % 256)
    K_tilda += chr((ord(K[14]) ^ 149))
    K_tilda += chr((ord(K[15]) + 131) % 256)
    log.debug("K_to_K_tilda_str: {}".format(K_tilda.encode("hex")))

    return K_tilda


def E(inp, L):
    """(EQ 14) pag 1675 Expansion of a L Bytes inp to a 16 Byte output.

    X[i % L] for i = 0...15

    """
    emsg1 = "E L is {}, it should be {}".format(type(L), "int")
    assert type(L) == int, emsg1
    emsg2 = "E inp is {}, it should be bytearray".format(type(inp))
    assert type(inp) == bytearray, emsg2
    emsg3 = "E inp len is {}, it should be {}".format(len(inp), L)
    assert len(inp) == L, emsg3

    ext_inp = bytearray()
    for i in range(16):
        index = i % L
        ext_inp.append(inp[index])
    # log.debug('E     inp: {}'.format(repr(inp)))
    # log.debug('E ext_inp: {}'.format(repr(ext_inp)))

    assert len(ext_inp) == Ar_KEY_LEN
    return ext_inp


def E_str(inp, L):
    """Expansion of a L Bytes inp to a 16 Byte output.

    Our inp should always be 12 Bytes long.
    """

    emsg1 = "E L is {}, it should be {}".format(type(L), "int")
    assert type(L) == int, emsg1
    emsg2 = "E inp is {}, it should be {}".format(type(inp), "str")
    assert type(inp) == str, emsg2
    emsg3 = "E inp len is {}, it should be {}".format(len(inp), L)
    assert len(inp) == L, emsg3

    ext_inp = ""
    for i in range(16):
        index = i % L
        ext_inp += inp[index]
    # log.debug('E     inp: {}'.format(inp))
    # log.debug('E ext_inp: {}'.format(ext_inp))
    log.debug("E     inp: {}".format(inp.encode("hex")))
    log.debug("E ext_inp: {}".format(ext_inp.encode("hex")))

    return ext_inp
