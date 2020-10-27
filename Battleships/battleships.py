# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
#
# a[i][j] - i = НОМЕР СТРОКИ, j = НОМЕР СТОЛБЦА
# «четрыехпалубные» авианосцы - Aerocarrier
# «трехпалубные» крейсера - Cruiser
# «двухпалубные» эсминцы - Destroyer
# «однопалубные» торпедные катера - Boat
#
# обозначение палубы ◙
import random

dict_size_name = {4: "Aerocarrier", 3: "Cruiser", 2: "Destroyer", 1: "Boat"}
letter_to_number = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7, 'I': 8, 'J': 9}
number_to_letter = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'H', 8: 'I', 9: 'J'}


class Ship(object):
    """Class for ships"""
    global letter_to_number, number_to_letter

    def __init__(self, name=None, size=0, position=(), close_water=()):
        self.name = name
        self.size = size
        self.position = position
        self.close_water = close_water

    def place(self):
        """Position ship in place"""
        temp_position = []
        temp_water = []
        cell = [a for a in input("Enter top/left cell: ").upper()[::-1]]
        cell[0] = int(cell[0]) - 1
        direction = input("Enter direction (R/D): ").upper()
        if direction == "R":
            pos = self.letter_to_number[cell[1]]
            for k in range(self.size):
                pos += 1
                shadow_field[cell[0]][pos - 1] = "+"
                for i in [-1, 0, 1]:
                    for j in [-1, 0, 1]:
                        try:
                            if shadow_field[cell[0] + i][pos - 1 + j] != "+" and (cell[0] + i and pos - 1 + j >= 0):
                                shadow_field[cell[0] + i][pos - 1 + j] = "-"
                        except IndexError:
                            pass
                temp_position.append([cell[0], self.number_to_letter[pos - 1]])
        elif direction == "D":
            pos = int(cell[0])
            for k in range(self.size):
                pos += 1
                shadow_field[pos - 1][self.letter_to_number[cell[1]]] = "+"
                for i in [-1, 0, 1]:
                    for j in [-1, 0, 1]:
                        try:
                            if shadow_field[pos - 1 + i][self.letter_to_number[cell[1]] + j] != "+" \
                                    and (pos - 1 + i and self.letter_to_number[cell[1]] + j >= 0):
                                shadow_field[pos - 1 + i][self.letter_to_number[cell[1]] + j] = "-"
                        except IndexError:
                            pass
                temp_position.append([pos - 1, cell[1]])
        self.position = tuple(temp_position)
        print(f"Ship {self.name} placed!")
        return

    def shot(self):
        """Register a shot"""
        return

    def _print_position(self):
        """Print current position of ship"""
        for digit, letter in self.position:
            print(letter, digit + 1)
        return


def show_field(choice="battlefield"):
    if choice == "battlefield":
        field = battle_field
    else:
        field = shadow_field
    i = 0
    print('   ABCDEFGHIJ')
    for line in field:
        i += 1
        print(i, " " * (3 - len(str(i))), end="", sep="")
        for letter in line:
            print(letter, end="")
        print()


def random_place_all():
    for ship_size, ship_name in dict_size_name.items():
        for l in range(5 - ship_size):
            check_done = False
            while not check_done:
                cell = []
                check_place = False
                while not check_place:
                    i, j = [random.randint(0, 9), random.randint(0, 9)]
                    if shadow_field[i][j] == " ":
                        check_place = True
                        cell += [i, j]
                    else:
                        continue
                    if ship_size != 1:
                        check_direction = False
                        arr = ["left", "up", "right", "down"]
                        while not check_direction:
                            if not arr:
                                break
                            direction = random.choice(arr)
                            if direction == "left":
                                for k in range(ship_size - 1):
                                    if j - (k + 1) < 0:
                                        print("Got through the border")
                                        arr.remove(direction)
                                        direction = ""
                                        break
                                    elif shadow_field[i][j - (k + 1)] != " ":
                                        print("Something in the cell")
                                        arr.remove(direction)
                                        direction = ""
                                        break
                                if direction != "":
                                    check_direction = True
                                    break
                                else:
                                    continue
                            elif direction == "up":
                                for k in range(ship_size - 1):
                                    if i - (k + 1) < 0:
                                        print("Got through the border")
                                        arr.remove(direction)
                                        direction = ""
                                        break
                                    elif shadow_field[i - (k + 1)][j] != " ":
                                        print("Something in the cell")
                                        arr.remove(direction)
                                        direction = ""
                                        break
                                if direction != "":
                                    check_direction = True
                                    break
                                else:
                                    continue
                            elif direction == "right":
                                for k in range(ship_size - 1):
                                    try:
                                        if shadow_field[i][j + (k + 1)] != " ":
                                            print("Something in the cell")
                                            arr.remove(direction)
                                            direction = ""
                                            break
                                    except IndexError:
                                        print("Got through the border")
                                        arr.remove(direction)
                                        direction = ""
                                        break
                                if direction != "":
                                    check_direction = True
                                    break
                                else:
                                    continue
                            elif direction == "down":
                                for k in range(ship_size - 1):
                                    try:
                                        if shadow_field[i + (k + 1)][j] != " ":
                                            print("Something in the cell")
                                            arr.remove(direction)
                                            direction = ""
                                            break
                                    except IndexError:
                                        print("Got through the border")
                                        arr.remove(direction)
                                        direction = ""
                                        break
                                if direction != "":
                                    check_direction = True
                                    break
                                else:
                                    continue
                    else:
                        check_direction = True
                    check_done = check_direction and check_place
            print(f"Cell is [{i}][{j}]. Direction is {direction}")
            print(f"SHIP PLACED! SHIP {ship_name} SIZE {ship_size}")
            place_ship(cell, direction, ship_size)


def place_ship(cell, direction, size):
    global shadow_field
    around = [-1, 0, 1]
    i, j = cell
    for m in range(size):
        if direction == "down":
            shadow_field[i + m][j] = "◙"
            try:
                for k in around:
                    for l in around:
                        if (i + m + k < 0) or (j + l < 0):
                            continue
                        elif shadow_field[i + m + k][j + l] != "◙":
                            shadow_field[i + m + k][j + l] = "+"
            except IndexError:
                continue
        elif direction == "right":
            shadow_field[i][j + m] = "◙"
            try:
                for k in around:
                    for l in around:
                        if (i + k < 0) or (j + m + l < 0):
                            continue
                        elif shadow_field[i + k][j + m + l] != "◙":
                            shadow_field[i + k][j + m + l] = "+"
            except IndexError:
                continue
        elif direction == "up":
            shadow_field[i - m][j] = "◙"
            try:
                for k in around:
                    for l in around:
                        if (i - m + k < 0) or (j + l < 0):
                            continue
                        elif shadow_field[i - m + k][j + l] != "◙":
                            shadow_field[i - m + k][j + l] = "+"
            except IndexError:
                continue
        elif direction == "left":
            shadow_field[i][j - m] = "◙"
            try:
                for k in around:
                    for l in around:
                        if (j - m + l < 0) or (i + k < 0):
                            continue
                        elif shadow_field[i + k][j - m + l] != "◙":
                            shadow_field[i + k][j - m + l] = "+"
            except IndexError:
                continue
    show_field("shadow_field")


shadow_field = [[" "] * 10 for i in range(10)]
battle_field = [[" "] * 10 for i in range(10)]

random_place_all()
'''
show_field(shadow_field)
print()
four_celled = Ship("Aerocarrier", 4)
four_celled.place()
show_field(shadow_field)
three_celled_1 = Ship("Cruiser 1", 3)
three_celled_1.place()
show_field(shadow_field)
'''
