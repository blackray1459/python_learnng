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
from enum import Enum

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
                field[cell[0]][pos - 1] = "+"
                for i in [-1, 0, 1]:
                    for j in [-1, 0, 1]:
                        try:
                            if field[cell[0] + i][pos - 1 + j] != "+" and (cell[0] + i and pos - 1 + j >= 0):
                                field[cell[0] + i][pos - 1 + j] = "-"
                        except IndexError:
                            pass
                temp_position.append([cell[0], self.number_to_letter[pos - 1]])
        elif direction == "D":
            pos = int(cell[0])
            for k in range(self.size):
                pos += 1
                field[pos - 1][self.letter_to_number[cell[1]]] = "+"
                for i in [-1, 0, 1]:
                    for j in [-1, 0, 1]:
                        try:
                            if field[pos - 1 + i][self.letter_to_number[cell[1]] + j] != "+" \
                                    and (pos - 1 + i and self.letter_to_number[cell[1]] + j >= 0):
                                field[pos - 1 + i][self.letter_to_number[cell[1]] + j] = "-"
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


class Marks(Enum):
    EMPTY = 1
    NEARBY = 2
    BOARD = 3
    WATER = 4
    SHOT = 5


def print_field(admin=False):
    i = 0
    print('   ABCDEFGHIJ')
    for line in field:
        i += 1
        print(i, " " * (3 - len(str(i))), end="", sep="")
        for cell in line:
            if cell == Marks.NEARBY and admin:
                print("+", end="")
            elif cell == Marks.BOARD and admin:
                print("◙", end="")
            elif cell == Marks.WATER:
                print("●", end="")
            elif cell == Marks.SHOT:
                print("X", end="")
            else:
                print(" ", end="")
        print()


def generate_ships():
    for ship_size, ship_name in dict_size_name.items():
        for i in range(5 - ship_size):
            check_done = False
            while not check_done:
                cell = []
                check_place = False
                while not check_place:
                    row, column = [random.randint(0, 9), random.randint(0, 9)]
                    if field[row][column] == Marks.EMPTY:
                        check_place = True
                        cell += [row, column]
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
                                for delta in range(ship_size - 1):
                                    if column - (delta + 1) < 0 or field[row][column - (delta + 1)] != Marks.EMPTY:
                                        arr.remove(direction)
                                        direction = ""
                                        break
                                if direction != "":
                                    check_direction = True
                            elif direction == "up":
                                for delta in range(ship_size - 1):
                                    if row - (delta + 1) < 0 or field[row - (delta + 1)][column] != Marks.EMPTY:
                                        arr.remove(direction)
                                        direction = ""
                                        break
                                if direction != "":
                                    check_direction = True
                            elif direction == "right":
                                for delta in range(ship_size - 1):
                                    if column + (delta + 1) > 9 or field[row][column + (delta + 1)] != Marks.EMPTY:
                                        arr.remove(direction)
                                        direction = ""
                                        break
                                if direction != "":
                                    check_direction = True
                            elif direction == "down":
                                for delta in range(ship_size - 1):
                                    if row + (delta + 1) > 9 or field[row + (delta + 1)][column] != Marks.EMPTY:
                                        arr.remove(direction)
                                        direction = ""
                                        break
                                if direction != "":
                                    check_direction = True
                    else:
                        check_direction = True
                check_done = check_direction and check_place
            place_ship(cell, direction, ship_size)
    print("All ships are in position!")


def place_ship(cell, direction, size):
    around = [-1, 0, 1]
    row, column = cell
    for m in range(size):
        if direction == "down":
            field[row + m][column] = Marks.BOARD
            for k in around:
                for n in around:
                    if (row + m + k < 0) or (column + n < 0) or (row + m + k > 9) or (column + n > 9):
                        continue
                    elif field[row + m + k][column + n] != Marks.BOARD:
                        field[row + m + k][column + n] = Marks.NEARBY
        elif direction == "right":
            field[row][column + m] = Marks.BOARD
            for k in around:
                for n in around:
                    if (row + k < 0) or (column + m + n < 0) or (row + k > 9) or (column + m + n > 9):
                        continue
                    elif field[row + k][column + m + n] != Marks.BOARD:
                        field[row + k][column + m + n] = Marks.NEARBY
        elif direction == "up":
            field[row - m][column] = Marks.BOARD
            for k in around:
                for n in around:
                    if (row - m + k < 0) or (column + n < 0) or (row - m + k > 9) or (column + n > 9):
                        continue
                    elif field[row - m + k][column + n] != Marks.BOARD:
                        field[row - m + k][column + n] = Marks.NEARBY
        elif direction == "left":
            field[row][column - m] = Marks.BOARD
            for k in around:
                for n in around:
                    if (column - m + n < 0) or (row + k < 0) or (column - m + n > 9) or (row + k > 9):
                        continue
                    elif field[row + k][column - m + n] != Marks.BOARD:
                        field[row + k][column - m + n] = Marks.NEARBY


def shot(row, column):  # РЕГИСТРАЦИЯ ВЫСТРЕЛА И ПРОВЕРКА НА УБИЙСТВО
    around = [-1, 0, 1]
    direction_delta = [[-1, 0], [1, 0], [0, -1], [0, 1]]  # ВВЕРХ, ВНИЗ, ВЛЕВО, ВПРАВО
    if field[row][column] == Marks.EMPTY or field[row][column] == Marks.NEARBY:
        field[row][column] = Marks.WATER
        print("МИМО!")
        print_field()
        return
    elif field[row][column] == Marks.WATER:
        print("Ты сюда стрелял. Тут ●")
        return
    elif field[row][column] == Marks.SHOT:
        print("Ты сюда стрелял. Тут Х")
        return
    elif field[row][column] == Marks.BOARD:
        field[row][column] = Marks.SHOT
        for vertical_delta, horizontal_delta in direction_delta:
            temp_row = row + vertical_delta
            temp_column = column + horizontal_delta
            while True:
                if 0 <= (temp_row) <= 9 and 0 <= (temp_column) <= 9:
                    if field[temp_row][temp_column] == Marks.BOARD:
                        print("РАНИЛ!")
                        print_field()
                        return
                    elif field[temp_row][temp_column] == Marks.NEARBY or field[temp_row][temp_column] == Marks.WATER:
                        break
                    else:
                        temp_row += vertical_delta
                        temp_column += horizontal_delta
                else:
                    break
        #  ЕСЛИ НЕ НАШЛОСЬ ЗДОРОВОЙ ПАЛУБЫ
        for vertical_delta, horizontal_delta in direction_delta:
            temp_row = row
            temp_column = column
            while True:
                if temp_row < 0 or temp_column < 0 or temp_row > 9 or temp_column > 9:
                    break
                elif field[temp_row][temp_column] == Marks.SHOT:
                    for p in around:
                        for r in around:
                            if (temp_row + p < 0) or (temp_column + r < 0) or (temp_row + p > 9) or (temp_column + r > 9):
                                continue
                            elif field[temp_row + p][temp_column + r] == Marks.NEARBY:
                                field[temp_row + p][temp_column + r] = Marks.WATER
                    temp_row += vertical_delta
                    temp_column += horizontal_delta
                elif field[temp_row][temp_column] == Marks.NEARBY or field[temp_row][temp_column] == Marks.WATER:
                    break
        print("ПОТОПИЛ!")
        print_field()


field = [[Marks.EMPTY] * 10 for i in range(10)]
generate_ships()
turn = ""

while turn != "stop":
    win = True
    turn = input("\nВведи клетку, по которой будешь стрелять: ")
    print()
    if turn == "":
        print("Клетка не выбрана.")
        continue
    elif turn == "show":
        print_field()
        print_field(admin=True)
    elif (type(turn) is str) and (len(turn) == 2 or len(turn) == 3) and turn[0].isalpha() and turn[1:].isdigit():
        if turn[0].upper() not in letter_to_number.keys():
            print("Введи нормальную букву! A B C D E F G H I J. Выбирай!")
            continue
        if not 0 < int(turn[1:]) < 11:
            print("Цифры от 1 до 10! Без запятых!")
            continue
        row = int(turn[1:]) - 1
        column = letter_to_number[turn[0].upper()]
        shot(row, column)
    else:
        print("Ничего не понял. Примеры ввода: A4, B7. Буква и цифра. Давай по новой, Миша!")
        continue
    for line in field:
        if Marks.BOARD in line:
            win = False
            break
    if win:
        print("Победа! Весь флот уничтожен!")
        break
    else:
        continue
