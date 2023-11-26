#!/usr/bin/env python
"""
enable_diag.py

Send Cypress proprietary HCI command to enable LMP logging via H4
"""
import socket

HCI0 = 0
HCI1 = 1
HCI2 = 2

if __name__ == "__main__":
    s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_RAW, socket.BTPROTO_HCI)

    # NOTE: usually devboard is assigned to HCI1
    s.bind((HCI1,))

    # NOTE: enables LMP
    s.send(b"\x07\xf0\x01")

    s.close()
