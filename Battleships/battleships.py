# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
#
# a[i][j] - i = НОМЕР СТРОКИ, j = НОМЕР СТОЛБЦА
# «четрыехпалубные» авианосцы - Aerocarrier
# «трехпалубные» крейсера - Cruiser
# «двухпалубные» эсминцы - Destroyer
# «однопалубные» торпедные катера - Boat
#
# обозначение палубы ◙, воды рядом +, попадания ●
import random

dict_size_name = {4: "Aerocarrier", 3: "Cruiser", 2: "Destroyer", 1: "Boat"}
letter_to_number = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7, 'I': 8, 'J': 9}
number_to_letter = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'H', 8: 'I', 9: 'J'}
count = 0


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
                                        # print("Got through the border")
                                        arr.remove(direction)
                                        direction = ""
                                        break
                                    elif shadow_field[i][j - (k + 1)] != " ":
                                        # print("Something in the cell")
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
                                        # print("Got through the border")
                                        arr.remove(direction)
                                        direction = ""
                                        break
                                    elif shadow_field[i - (k + 1)][j] != " ":
                                        # print("Something in the cell")
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
                                            # print("Something in the cell")
                                            arr.remove(direction)
                                            direction = ""
                                            break
                                    except IndexError:
                                        # print("Got through the border")
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
                                            # print("Something in the cell")
                                            arr.remove(direction)
                                            direction = ""
                                            break
                                    except IndexError:
                                        # print("Got through the border")
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
            place_ship(cell, direction, ship_size)
    print("All ships are in position!")


def place_ship(cell, direction, size):
    global shadow_field
    around = [-1, 0, 1]
    i, j = cell
    for m in range(size):
        if direction == "down":
            shadow_field[i + m][j] = "◙"
            try:
                for k in around:
                    for n in around:
                        if (i + m + k < 0) or (j + n < 0):
                            continue
                        elif shadow_field[i + m + k][j + n] != "◙":
                            shadow_field[i + m + k][j + n] = "+"
            except IndexError:
                continue
        elif direction == "right":
            shadow_field[i][j + m] = "◙"
            try:
                for k in around:
                    for n in around:
                        if (i + k < 0) or (j + m + n < 0):
                            continue
                        elif shadow_field[i + k][j + m + n] != "◙":
                            shadow_field[i + k][j + m + n] = "+"
            except IndexError:
                continue
        elif direction == "up":
            shadow_field[i - m][j] = "◙"
            try:
                for k in around:
                    for n in around:
                        if (i - m + k < 0) or (j + n < 0):
                            continue
                        elif shadow_field[i - m + k][j + n] != "◙":
                            shadow_field[i - m + k][j + n] = "+"
            except IndexError:
                continue
        elif direction == "left":
            shadow_field[i][j - m] = "◙"
            try:
                for k in around:
                    for n in around:
                        if (j - m + n < 0) or (i + k < 0):
                            continue
                        elif shadow_field[i + k][j - m + n] != "◙":
                            shadow_field[i + k][j - m + n] = "+"
            except IndexError:
                continue
    # show_field("shadow_field")


def shot(i, j):  # РЕГИСТРАЦИЯ ВЫСТРЕЛА И ПРОВЕРКА НА УБИЙСТВО
    global shadow_field, battle_field, count
    around = [-1, 0, 1]
    counters = [[-1, 0], [1, 0], [0, -1], [0, 1]]  # ВВЕРХ, ВНИЗ, ВЛЕВО, ВПРАВО
    if shadow_field[i][j] == " " or shadow_field[i][j] == "+":
        battle_field[i][j] = "●"
        shadow_field[i][j] = "●"
        print("MIMO!")
        show_field()
        return
    elif shadow_field[i][j] == "●" or shadow_field[i][j] == "X":
        print(f"Uzhe strelyal suda. Tut {shadow_field[i][j]}")
        return
    elif shadow_field[i][j] == "◙":
        battle_field[i][j] = "X"
        shadow_field[i][j] = "X"
        for vertical_count, horizontal_count in counters:
            m = vertical_count
            n = horizontal_count
            while True:
                if 0 <= (i + m) <= 9 and 0 <= (j + n) <= 9:
                    if shadow_field[i + m][j + n] == "◙":
                        print("RANIL!")
                        show_field()
                        return
                    elif shadow_field[i + m][j + n] == "+" or shadow_field[i + m][j + n] == "●":
                        break
                    else:
                        m += vertical_count
                        n += horizontal_count
                else:
                    break
        #  ЕСЛИ НЕ НАШЛОСЬ ЗДОРОВОЙ ПАЛУБЫ
        for vertical_count, horizontal_count in counters:
            m = 0
            n = 0
            while True:
                if (i + m) >= 0 and (j + n) >= 0 or (i + m) <= 9 and (j + n) <= 9:
                    if shadow_field[i + m][j + n] == "X":
                        for p in around:
                            for r in around:
                                try:
                                    if (i + m + p < 0) or (j + n + r < 0):
                                        continue
                                    elif shadow_field[i + m + p][j + n + r] == "+":
                                        shadow_field[i + m + p][j + n + r] = "●"
                                        battle_field[i + m + p][j + n + r] = "●"
                                except IndexError:
                                    continue
                        m += vertical_count
                        n += horizontal_count
                    elif shadow_field[i + m][j + n] == "+" or shadow_field[i + m][j + n] == "●":
                        break
                else:
                    break
        print("POTOPIL!")
        show_field()
        count += 1


shadow_field = [[" "] * 10 for i in range(10)]
battle_field = [[" "] * 10 for i in range(10)]

random_place_all()
turn = ""
while turn != "stop":
    turn = input("\nEnter the cell you want to shoot: ")
    print()
    try:
        if turn == "":
            print("Cell is not chosen.")
            continue
        elif turn == "show":
            show_field()
            show_field("shadowfield")
        elif (type(turn) is str) and len(turn) == 2 and turn[0].isalpha() and turn[1].isdigit():
            if turn[0].upper() not in letter_to_number.keys():
                print("Vvedi normalnuiy bukvu! A B C D E F G H I J. Vybirai!")
                continue
            if int(turn[1]) not in number_to_letter.keys():
                print("Cifry ot 0 do 9, blin! I bez zapyatyh!")
                continue
            i = int(turn[1])-1
            j = letter_to_number[turn[0].upper()]
            shot(i, j)
            continue
        else:
            print("Nichego ne ponyal. Vvod takoi: A4, B7. Bukva i cifra. Davai po novoi, Misha!")
            continue
    except TypeError:
        print("Wrong input. Vvodi kak nado.")
        continue
    if count == 10:
        print("Eto pobeda! Ty ih nashel!")
        break

