# ВВОД И СОРТИРОВКА СЛОВАРЯ С ПОДСЧЕТОМ ВВЕДЕННОЙ СТРОКИ

from collections import defaultdict
from sys import stdin


def file_to_dict_print_table(f):  # РАСПЕЧАТКА ТАБЛИЦЫ С ПОДСЧЕТОМ СТРОК ИЗ ФАЙЛА
    counter = defaultdict(int)
    max_key_length = 0
    max_val_length = 0
    for val in f:
        if val == '\n' or val == '':
            break
        val = str(val).strip()
        counter[val] += 1
        if len(val) > max_key_length:
            max_key_length = len(val)
        if len(str(counter[val])) > max_val_length:
            max_val_length = len(str(counter[val]))
    print("+" + "-" * (2 + max_key_length) + "+" + "-" * (2 + max_val_length) + "+")
    for val, count in sorted(counter.items(), key=lambda x: x[1]):
        print("| " + val + " " * (max_key_length - len(val)) + " | " + " " * (max_val_length - len(str(count))) +
              str(count) + " |")
    print("+" + "-" * (2 + max_key_length) + "+" + "-" * (2 + max_val_length) + "+")
    return dict(counter)


with open('text.txt', 'r') as f:
    file_to_dict_print_table(f)

