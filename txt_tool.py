#!/usr/bin/env python
#
# This is a personal tool what I need for my working.
#
# hidekuno@gmail.com
#
import sys
import os
import argparse

def check_words_length(s):
    dq_mode = False
    sp_mode = False
    pc = None
    words = ""

    is_whitespace = lambda c: c == ' ' or c == "\n"
    def print_result():
        nonlocal words
        print(f'"{words}"', ":", len(words))
        words = ""

    for c in s:
        if dq_mode:
            if c == '"' and pc != '\\':
                print_result()
                dq_mode = False
            elif is_whitespace(c)  and pc == '"':
                words = words[0:-1]
                print_result()
                dq_mode = False
            else:
                words += c
        elif sp_mode:
            if is_whitespace(c):
                if pc == '\\':
                    words += c
                else:
                    print_result()
                    sp_mode = False
            else:
                words += c
        else:
            if c == '"' and pc != '\\':
                dq_mode = True
            elif (is_whitespace(pc) or not pc) and c != ' ':
                sp_mode = True
                words += c
        pc = c

    if sp_mode:
        print_result()

# test code
#check_words_length('"abc \\" def"  hoge     foo  "ghi jkl" "\\""')
#check_words_length('12345 "abc def"    67890')
#check_words_length('\\ 12345    \\     67890')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--filename", type=str, dest="filename", required=True)
    args = parser.parse_args(sys.argv[1:])

    if not os.path.exists(args.filename):
        sys.exit("No such filename")

    with open(args.filename) as fd:
        check_words_length(fd.read())
