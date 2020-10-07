from collections import defaultdict
from sortedcontainers import SortedDict


d = defaultdict(int)
length_key = 0
for i in range(15):
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

print("+" + "-" * (2 + length_key) + "+" + "-" * (2 + length_val) + "+")
for key, value in d.items():
    print("| " + (lambda a: str(a) + " " * (length_key - key.__str__().__len__()))(key) + " | " + (lambda a: " " *
                                                      (length_val - value.__str__().__len__()) +  str(a))(value) + " |")
print("+" + "-" * (2 + length_key) + "+" + "-" * (2 + length_val) + "+")
