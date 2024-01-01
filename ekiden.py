import pandas as pd
import re
import sys
import argparse

def skelton(url, edit):
    df = pd.read_html(url)
    schools = edit(df)
    for r in sorted(set([(s, len([i for i in schools if i == s])) for s in schools]),
                    key=lambda x: -x[1]):
        print(r)

def kyoto():
    def _kyoto(df):
        data = [d.values.tolist() for d in df[0:]][0][1:]
        return [re.sub('..地区/', '', s[3]) for s in data]

    skelton('https://mainichi.jp/koukouekiden/articles/20200205/hrc/00m/050/008000d', _kyoto)

def hakone():
    def _hakone(df):
        data = [d.values.tolist() for d in df[0:]][0]
        return [d[2] for d in data]

    skelton('https://www.hakone-ekiden.jp/record/', _hakone)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--hakone",action='store_true')
    group.add_argument("--kyoto",action='store_true')
    args = parser.parse_args(sys.argv[1:])
    if args.hakone:
        hakone()
    if args.kyoto:
        kyoto()
