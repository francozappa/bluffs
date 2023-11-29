# BLUFFS (Bluetooth Forward and Future Secrecy Attacks and Defenses)

## Introduction

BLUFFS (CVE 2023-24023) is a software suite designed to analyze and mitigate security vulnerabilities in Bluetooth technology. It aims to provide tools for testing and strengthening the forward and future secrecy properties of Bluetooth connections.

## Requirements

    Compatible ARM hardware
    Python 3.x
    Required Python libraries: [List of libraries]
    Bluetooth testing equipment (if applicable)

## Installation Instructions

```bash
# Clone the repository:
$ git clone https://github.com/francozappa/bluffs

# Navigate to the cloned directory:
cd bluffs

# Install required Python libraries:
pip install -r requirements.txt
```

## Usage

### `pcap`

Navigate to the pcap directory.
Use the following command to analyze pcap samples:

```arduino
[Command to run pcap analysis]
```

### `checker`

The checker folder contains the parser.
To use the parser, run:

```bash
python checker/parser.py [arguments]
```

### `device`

Contains the ARM patches (`*.s`) and the `bluffs.py` script to test the attacks.
Apply ARM patches using:

```
[Instructions for applying patches]
```

To run bluffs.py, use:

```bash
python device/bluffs.py [arguments]
```

## `pwnlib`

Contains the patched `asm.py` adding the `--no-warn-rwx-segment` flag to `ldflags` to
avoid an `ld` error with recent versions of arm binutils. On Linux, the file
should be copied to: `/usr/lib/python2.7/site-packages/pwnlib`

## Examples

Example 1: Running a basic check with bluffs.py

```bash
python device/bluffs.py --option
```

## Troubleshooting

- Issue 1: If you encounter [common problem], try [solution].
- Issue 2: For issues with installation, ensure all dependencies are correctly installed.

## Contributing

Contributions to BLUFFS are welcome! Please follow these steps to contribute:

    Fork the repository.
    Make your changes.
    Submit a pull request with a clear description of your improvements.

## License

See [License File](.LICENCE.md)

## Changelog

- **v1.0**: Initial release.
- **v1.1**: Add pwnlib folder
- **v1.2**: Complete README
