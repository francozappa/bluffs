# BLUFFS

## Introduction

This repository contains code related to
[BLUFFS: Bluetooth Forward and Future Secrecy Attacks and Defenses](https://dl.acm.org/doi/pdf/10.1145/3576915.3623066).



### Paper abstract

Bluetooth is a pervasive technology for wireless communication. Billions of
devices use it in sensitive applications and to exchange private data. The
security of Bluetooth depends on the Bluetooth standard and its two security
mechanisms: pairing and session establishment. No prior work, including
the standard itself, analyzed the future and forward secrecy guarantees
of these mechanisms, e.g., if Bluetooth pairing and session establishment
defend past and future sessions when the adversary compromises the current.
To address this gap, we present six novel attacks, defined as the BLUFFS
attacks, breaking Bluetooth sessions’ forward and future secrecy. Our attacks
enable device impersonation and machine-in-the-middle across sessions by only
compromising one session key. The attacks exploit two novel vulnerabilities
that we uncover in the Bluetooth standard related to unilateral and repeatable
session key derivation. As the attacks affect Bluetooth at the architectural
level, they are effective regardless of the victim’s hardware and software
details (e.g., chip, stack, version, and security mode).

We also release BLUFFS, a low-cost toolkit to perform and automatically check
the effectiveness of our attacks. The toolkit employs seven original patches
to manipulate and monitor Bluetooth session key derivation by dynamically
patching a closed-source Bluetooth firmware that we reverse-engineered. We
show that our attacks have a critical and large-scale impact on the Bluetooth
ecosystem, by evaluating them on seventeen diverse Bluetooth chips (eighteen
devices) from popular hardware and software vendors and supporting the most
popular Bluetooth versions. Motivated by our empirical findings, we develop
and successfully test an enhanced key derivation function for Bluetooth that
stops by-design our six attacks and their four root causes. We show how
to effectively integrate our fix into the Bluetooth standard and discuss
alternative implementation-level mitigations. We responsibly disclosed our
contributions to the Bluetooth SIG.

### BibTex entry

```bash
@inproceedings{antonioli23bluffs,
    title={{BLUFFS: Bluetooth Forward and Future Secrecy Attacks and Defenses}},
    author={Antonioli, Daniele},
    booktitle={ACM conference on Computer and Communications Security (CCS)},
    month={November},
    year={2023}
}
```

### More resources

[CVE 2023-24023](https://nvd.nist.gov/vuln/detail/CVE-2023-24023),
[ACM CCS'23 slides](https://francozappa.github.io/publication/2023/bluffs/slides.pdf).

## Usage

### pcap

Navigate to the pcap directory.
Use the following command to analyze pcap samples:

```arduino
wireshark file.pcap
```

### checker

The checker folder contains the parser.
To use the parser, run:

```bash
python checker/parser.py [arguments]
```

### device


To test if a victim device is vulnerable to the BLUFFS attacks read Section
6.1 of the paper and patch the attack device using:

```bash
python device/bluffs.py
```

The individual patches are also provided in dedicated `*.s` files.

## pwnlib

Contains the patched `asm.py` adding the `--no-warn-rwx-segment` flag to `ldflags` to
avoid an `ld` error with recent versions of arm binutils. On Linux, the file
should be copied to: `/usr/lib/python2.7/site-packages/pwnlib`.
