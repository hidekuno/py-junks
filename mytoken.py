#!/usr/bin/python3
#
# This is a personal tool what I need for my working.
#
# hidekuno@gmail.com
#
import datetime
import random
import string
import hashlib

SECRET= "d48a055ac6d44a06" # please replace.
def _generate_token(r):
    d = hex(int(datetime.datetime.now().strftime('%Y%m%d')))[2:]
    token = d + hashlib.sha256((d + SECRET + r).encode('utf-8')).hexdigest() + r
    return token

def create_token():
    return _generate_token(''.join(random.choices(string.ascii_lowercase + string.digits, k=16)))

def validate_token(token):
    return token == _generate_token(token[-16:])
