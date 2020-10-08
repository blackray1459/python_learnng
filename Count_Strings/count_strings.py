from collections import defaultdict
from sortedcontainers import SortedDict

def sort_dict_by_value(d):
    for key, value in d.items():

    return d


counter = defaultdict(int)
max_key_length = 0
for i in range(15):
    key = str(input()).strip()
    counter[key] += 1
    if len(key) > max_key_length:
        max_key_length = len(key)
    #(lambda word, d: d[word]+=1)(word,d)
d = dict(SortedDict(counter))
max_val_length = 0
for word in counter.values():
    if len(str(word)) > max_val_length:
        max_val_length = len(str(word))

print("+" + "-" * (2 + max_key_length) + "+" + "-" * (2 + max_val_length) + "+")
for key, value in d.items():
    print("| " + (lambda a: str(a) + " " * (max_key_length - key.__str__().__len__()))(key) + " | " + (lambda a: " " *
                                                      (max_val_length - value.__str__().__len__()) +  str(a))(value) + " |")
print("+" + "-" * (2 + max_key_length) + "+" + "-" * (2 + max_val_length) + "+")
