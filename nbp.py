#!/usr/bin/env python
#
# this is toy tool
#
# hidekuno@gmail.com
#
import pandas as pd
import json

url = 'https://npb.jp/bis/2023/stats/bat_c.html'
df = pd.read_html(url)

data = json.dumps([d.values.tolist() for d in df[0:]][0][1:], ensure_ascii=False)
print(data)
