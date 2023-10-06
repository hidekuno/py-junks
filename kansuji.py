#!/usr/bin/env python
#
# This is a personal tool what I need for my working.
#
# hidekuno@gmail.com
#
import sys
import argparse
from functools import reduce

class Cn(object):
    def __init__(self,unit,num):
        self.unit = unit
        self.value = num[::-1]

    def __str__(self):
        if int(self.value) == 0:
            return ""
        else:
            return "%s%s" % (self._to_kansuji(), self.unit,)

    def _to_kansuji(self):
        kansuji = [ "","", "二", "三", "四", "五", "六", "七", "八", "九"]
        unit = ["", "十","百","千"]

        ret = []
        for i, c in enumerate(self.value[::-1]):
            if (i == 0 and int(c) == 1):
                ret.append("一")
            elif int(c) == 0:
                pass
            else:
                ret.append(f"{kansuji[int(c)]}{unit[i]}")
        return "".join(ret[::-1])

def to_kansuji(num):
    unit = (
        "",
        "万",
        "億",
        "兆",
        "京",
        "垓",
        "𥝱",
        "穣",
        "溝",
        "澗",
        "正",
        "載",
        "極",
        "恒河沙",
        "阿僧祇",
        "那由他",
        "不可思議",
        "無量大数",)

    s = str(num)[::-1]
    if len(s) > 72:
        raise Exception("Too long")

    values = []
    buf = ""
    idx = 0
    for i, c in enumerate(str(num)[::-1]):
        if i % 4 == 0 and i > 0:
            values.append(Cn(unit[idx],buf))
            idx += 1
            buf = ""
        buf += c

    values.append(Cn(unit[idx],buf))
    s = reduce(lambda s, cur: s + str(cur), values[::-1], "")
    return s if s else "零"

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('num', type=int)
    args = parser.parse_args(sys.argv[1:])

    try:
        s = to_kansuji(args.num)
        print(s)
    except Exception as e:
        print(e)
