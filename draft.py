#!/usr/bin/env python
#
# this is toy tool
#
# hidekuno@gmail.com
#
import pandas as pd
from functools import reduce
import unicodedata


def check_pro(s):
    def _check(s):
        return s in [
            "阪神",
            "広島",
            "ＤｅＮＡ",
            "巨人",
            "ヤクルト",
            "中日",
            "オリックス",
            "ロッテ",
            "ソフトバンク",
            "楽天",
            "西武",
            "日本ハム",
        ] or s in ["阪急", "近鉄", "南海", "大洋横浜", "横浜", "横浜ＤｅＮＡ", "阪急オリックス"]

    if not type(s) is str:
        return False
    for p in s.split("→"):
        if _check(unicodedata.normalize("NFKC", p)):
            return True
    return False


def _count_pro_excel():
    df = pd.read_excel("Book1.xlsx", index_col=None, header=0)
    len([n[1] for n in df.values.tolist() if check_pro(n[5])])


if __name__ == "__main__":
    url = "http://koushien.s100.xrea.com/homerun/tsuusan.htm"
    df = pd.read_html(url, encoding="shift-jis")
    player = reduce(lambda x, y: x + y, [d.values.tolist() for d in df[1:]])
    for n in [(n[1], n[5]) for n in player if check_pro(n[5])]:
        print(n)
