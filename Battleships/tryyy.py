import random


def show_field():
    global shadow_field
    i = 0
    print('   ABCDEFGHIJ')
    for line in shadow_field:
        i += 1
        print(i, " " * (3 - len(str(i))), end="", sep="")
        for letter in line:
            print(letter, end="")
        print()


shadow_field = [[" "]*10 for i in range(10)]

for k in range(26):
    i, j = [random.randint(0, 9), random.randint(0, 9)]
    shadow_field[i][j] = "+"
l = 0
for k in range(50):
    check_place = False
    while not check_place:
        l += 1
        i, j = [random.randint(0, 9), random.randint(0, 9)]
        if shadow_field[i][j] == " ":
            check_place = True
            shadow_field[i][j] == "0"
            print(f"Found a free place at [{i}, {j}]")
        else:
            print(f"Found a busy place at [{i}, {j}] with char {shadow_field[i][j]}")
            continue
show_field()
print()
print(l)