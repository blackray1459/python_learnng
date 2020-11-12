# РЕАЛИЗАЦИЯ ИГРЫ "МОРСКОЙ БОЙ"

import random
from enum import Enum


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


def to_letter(number):
    return chr(number + 65)


def to_number(letter):
    return ord(letter) - 65


def init_field(field):
    field = [[Marks.EMPTY] * 10 for i in range(10)]
    return


def print_field(admin=False):
    print('   ABCDEFGHIJ')
    for i, line in enumerate(field):
        print(i + 1, " " * (3 - len(str(i + 1))), end="", sep="")
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
    for ship_size in range(4):
        ship_size += 1
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
                    delta_row_column = [[0, -1], [-1, 0], [0, 1], [1, 0]]  # "left","up","right","down"
                    while not check_direction:
                        if not delta_row_column:
                            break
                        row_delta, column_delta = random.choice(delta_row_column)
                        temp_row = row
                        temp_column = column
                        for counter in range(ship_size - 1):
                            temp_row += row_delta
                            temp_column += column_delta
                            if (temp_row not in range(10) or temp_column not in range(10)) or field[temp_row][\
                                    temp_column] != \
                                    Marks.EMPTY:
                                delta_row_column.remove([row_delta, column_delta])
                                row_delta = None
                                break
                        if row_delta is not None:
                            check_direction = True
                            break
                        else:
                            continue
                else:
                    check_direction = True
                    row_delta, column_delta = 0, 0
                check_done = check_place and check_direction
            place_ship(cell, row_delta, column_delta, ship_size)
    print("Корабли размещены. К бою!")


def place_ship(cell, row_delta, column_delta, size):
    around = [-1, 0, 1]
    row, column = cell
    for counter in range(size):
        field[row][column] = Marks.BOARD
        for k in around:
            for n in around:
                if row + k not in range(10) or column + n not in range(10):
                    continue
                elif field[row + k][column + n] != (Marks.BOARD or Marks.NEARBY):
                    field[row + k][column + n] = Marks.NEARBY
        row += row_delta
        column += column_delta


def shot(row, column):  # РЕГИСТРАЦИЯ ВЫСТРЕЛА И ПРОВЕРКА НА УБИЙСТВО
    around = [-1, 0, 1]
    direction_delta = [[-1, 0], [1, 0], [0, -1], [0, 1]]  # ВВЕРХ, ВНИЗ, ВЛЕВО, ВПРАВО
    if field[row][column] == Marks.EMPTY or field[row][column] == Marks.NEARBY:
        field[row][column] = Marks.WATER
        print("МИМО!")
        return
    elif field[row][column] == Marks.WATER:
        print("Ты сюда стрелял. Тут ●")
        return
    elif field[row][column] == Marks.SHOT:
        print("Ты сюда стрелял. Тут Х")
        return
    elif field[row][column] == Marks.BOARD:
        field[row][column] = Marks.SHOT
        check_dead = False
        count_directions = 0
        while True:
            for vertical_delta, horizontal_delta in direction_delta:
                temp_row = row
                temp_column = column
                while True:
                    if 0 <= temp_row <= 9 and 0 <= temp_column <= 9:
                        if field[temp_row][temp_column] == Marks.BOARD:
                            print("РАНИЛ!")
                            return
                        elif check_dead and field[temp_row][temp_column] == Marks.SHOT:
                            for p in around:
                                for r in around:
                                    if (temp_row + p and temp_column + r < 0) or (temp_row + p and temp_column + r > 9):
                                        continue
                                    elif field[temp_row + p][temp_column + r] == Marks.NEARBY:
                                        field[temp_row + p][temp_column + r] = Marks.WATER
                            temp_row += vertical_delta
                            temp_column += horizontal_delta
                        elif field[temp_row][temp_column] == (Marks.NEARBY or Marks.WATER):
                            break
                        else:
                            temp_row += vertical_delta
                            temp_column += horizontal_delta
                    else:
                        break
                if check_dead:
                    count_directions += 1
            if count_directions == 4:
                print("ПОТОПИЛ!")
                return
            check_dead = True


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
        print_field(admin=True)
    elif (len(turn) == 2 or len(turn) == 3) and turn[0].isalpha() and turn[1:].isdigit():
        if to_number(turn[0].upper()) not in range(0, 10):
            print("Введи нормальную букву! A B C D E F G H I J. Выбирай!")
            continue
        if not 0 < int(turn[1:]) < 11:
            print("Цифры от 1 до 10! Без запятых!")
            continue
        row = int(turn[1:]) - 1
        column = to_number(turn[0].upper())
        shot(row, column)
        print_field()
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
