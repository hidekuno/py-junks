import pandas as pd
import re

url = 'https://mainichi.jp/koukouekiden/articles/20200205/hrc/00m/050/008000d'

df = pd.read_html(url)
data = [d.values.tolist() for d in df[0:]][0][1:]
school = [re.sub('..地区/', '', s[3]) for s in data]
for r in sorted(set([(s, len([i for i in school if i == s])) for s in school]), key=lambda x: -x[1]):
    print(r)
