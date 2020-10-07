from collections import defaultdict
from sortedcontainers import SortedDict


d = defaultdict(int)
length_key = 0
for i in range(11):
    key = str(input()).strip()
    d[key] += 1
    if len(key) > length_key:
        length_key = len(key)
    #(lambda word, d: d[word]+=1)(word,d)
d = dict(SortedDict(d))
length_val = 0
for word in d.values():
    if len(str(word)) > length_val:
        length_val = len(str(word))
