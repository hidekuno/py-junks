#!/usr/bin/env python
#
# this is toy tool
#
# hidekuno@gmail.com
#
import ctypes
import os
import sys

sofile = os.path.join(os.environ['HOME'], "rust-elisp","ffilisp","target","release","libffilisp.so")
if not os.path.isfile(sofile):
    sys.exit(1)

rust = ctypes.cdll.LoadLibrary(sofile)

def do_scheme(ex):
    p = ctypes.create_string_buffer(ex.encode('utf-8'))
    r = rust.do_scheme(p)
    return ctypes.c_char_p(r).value.decode('utf-8')

def repl():
    print("######## This is a mini lisp like Scheme. #######\n")

    while True:
        try:
            exp = input("<rust-elisp> ")
            if exp == "(quit)":
                break
            if exp == "":
                continue
            value = do_scheme(exp)
            print(value)
        except KeyboardInterrupt:
            print("")
            continue
        except EOFError:
            break

repl()
