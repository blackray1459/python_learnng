# ВВОД И СОРТИРОВКА СЛОВАРЯ С ПОДСЧЕТОМ ВВЕДЕННОЙ СТРОКИ

from collections import defaultdict
from sys import stdin

counter = defaultdict(int)
max_key_length = 0
max_val_length = 0
for key in stdin:
    if key == '\n' or key == '':
        break
    key = str(key).strip()
    counter[key] += 1
    if len(key) > max_key_length:
        max_key_length = len(key)
    if len(str(counter[key])) > max_val_length:
        max_val_length = len(str(counter[key]))

print("+" + "-" * (2 + max_key_length) + "+" + "-" * (2 + max_val_length) + "+")
for key, value in sorted(counter.items(), key=lambda x: x[1]):
    print("| " + key + " " * (max_key_length - len(key)) + " | " + " " * (max_val_length - len(str(value))) +
          str(value) + " |")
print("+" + "-" * (2 + max_key_length) + "+" + "-" * (2 + max_val_length) + "+")
