# bluffs

Bluetooth Forward and Future Secrecy Attacks and Defenses (BLUFFS) [CVE 2023-24023]

## pcap

Contains pcap samples captured while testing the attacks.

## checker

Contains the parser.

## device

Contains the ARM patches (`*.s`) and the `bluffs.py` script to test the attacks.

## pwnlib

Contains the patched `asm.py` adding the `--no-warn-rwx-segment` flag to `ldflags` to
avoid an `ld` error with recent versions of arm binutils. On Linux, the file
should be copied to: `/usr/lib/python2.7/site-packages/pwnlib`
