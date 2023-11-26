"""
patch.py

Function used to ease the development of our attack device's patches.
"""

from pwn import *
from internalblue.hcicore import HCICore


def patch(name: str, trigger_addr: int, code_bstr: str, patch_addr: int):
    """
    Patch firmware at trigger_addr using code_bstr stored in
    RAM at patch_addr.

    Returns the length of the patch and the address that can be used for the
    next patch in RAM.
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
