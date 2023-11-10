#!/usr/bin/env python
#
# This is a personal tool what I need for my working.
#
# hidekuno@gmail.com
#
import ssl
import socket

"""
test_host="www.yahoo.co.jp"
check_cipher(test_host, "RC4-MD5:AES256-SHA")
check_cipher(test_host, "RC4-MD5:AES128-SHA")
"""


def check_cipher(host, cipher):
    try:
        ssl_sock = ssl.wrap_socket(socket.socket(), ciphers=cipher)
        ssl_sock.connect((host, 443))
        print(host, ssl_sock.cipher())
        ssl_sock.close()

    except ssl.SSLError as e:
        print(e)
