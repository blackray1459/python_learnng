# РЕАЛИЗАЦИЯ ИГРЫ "МОРСКОЙ БОЙ"

import random
import re
from enum import Enum


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


def print_help():
    print("Ознакомься с правилами, если игра тебе не знакома.")
    print("https://en.wikipedia.org/wiki/Battleship_(game)")
    print()
    print("Возможные действия:")
    print("\tstop - закончить игру")
    print("\t[0-9][A-J] - выстрел")


def init_field(field_size):
    return [[Marks.EMPTY]*field_size for _ in range(field_size)]


def surround(row_index, column_index, mark):
    if mark == Marks.SHOT:
        mark_around = Marks.WATER
    elif mark == Marks.BOARD:
        mark_around = Marks.NEARBY
    for horiz_offset in [-1, 0, 1]:
        for vert_offset in [-1, 0, 1]:
            if (row_index + horiz_offset not in range(field_size)) or \
                    (column_index + vert_offset not in range(field_size)):
                continue
            elif field[row_index + horiz_offset][column_index + vert_offset] in [Marks.NEARBY, Marks.EMPTY]:
                field[row_index + horiz_offset][column_index + vert_offset] = mark_around
    return


def print_field(admin=False):
    print(f'   {" ".join((chr(65 + i) for i in range(len(field[0]))))}')
    for row_index, row in enumerate(field):
        formatted_row = f'{row_index + 1:2} {" ".join(str(i) for i in row)}'
        formatted_row = formatted_row.replace(str(Marks.EMPTY), " ")
        if admin:
            formatted_row = formatted_row.replace(str(Marks.NEARBY), "+")
            formatted_row = formatted_row.replace(str(Marks.BOARD), "◙")
        else:
            formatted_row = formatted_row.replace(str(Marks.NEARBY), " ")
            formatted_row = formatted_row.replace(str(Marks.BOARD), " ")
        formatted_row = formatted_row.replace(str(Marks.SHOT), "X")
        formatted_row = formatted_row.replace(str(Marks.WATER), "●")
        print(formatted_row)


def generate_ships():
    for ship_size in range(4):
        ship_size += 1
        for i in range(5 - ship_size):
            check_done = False
            while not check_done:
                check_place = False
                while not check_place:
                    row_index, column_index = [random.randint(0, field_size-1), random.randint(0, field_size-1)]
                    if field[row_index][column_index] == Marks.EMPTY:
                        check_place = True
                    else:
                        continue
                if ship_size != 1:
                    check_direction = False
                    delta_row_column = [[0, -1], [-1, 0], [0, 1], [1, 0]]  # "left","up","right","down"
                    while not check_direction:
                        if not delta_row_column:
                            break
                        row_delta, column_delta = random.choice(delta_row_column)
                        temp_row = row_index
                        temp_column = column_index
                        for counter in range(ship_size - 1):
                            temp_row += row_delta
                            temp_column += column_delta
                            if (temp_row not in range(field_size-1) or temp_column not in range(field_size-1)) or \
                                    field[temp_row][temp_column] != Marks.EMPTY:
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
            place_ship(row_index, column_index, row_delta, column_delta, ship_size)
    print("\nКорабли размещены. К бою!")
    return


def place_ship(row_index, column_index, row_delta, column_delta, size, *direction):
    for counter in range(size):
        field[row_index][column_index] = Marks.BOARD
        surround(row_index, column_index, field[row_index][column_index])
        row_index += row_delta
        column_index += column_delta


def shot(row_index, column_index):  # РЕГИСТРАЦИЯ ВЫСТРЕЛА И ПРОВЕРКА НА УБИЙСТВО
    direction_delta = [[-1, 0], [1, 0], [0, -1], [0, 1]]  # ВВЕРХ, ВНИЗ, ВЛЕВО, ВПРАВО
    if field[row_index][column_index] in [Marks.EMPTY, Marks.NEARBY]:
        field[row_index][column_index] = Marks.WATER
        print("МИМО!")
        return

    if field[row_index][column_index] in [Marks.WATER, Marks.SHOT]:
        line = f"Ты сюда стрелял. Тут {str(field[row_index][column_index])}"
        line = line.replace(str(Marks.WATER), "●").replace(str(Marks.SHOT), "X")
        print(line)
        return

    if field[row_index][column_index] == Marks.BOARD:
        field[row_index][column_index] = Marks.SHOT
        check_dead = False
        count_directions = 0
        while True:
            for vertical_delta, horizontal_delta in direction_delta:
                temp_row_index = row_index
                temp_column_index = column_index
                while True:
                    if temp_row_index not in range(field_size) or temp_column_index not in range(field_size):
                        break

                    if field[temp_row_index][temp_column_index] == Marks.BOARD:
                        print("РАНИЛ!")
                        return

                    if field[temp_row_index][temp_column_index] in [Marks.NEARBY, Marks.WATER]:
                        break

                    if check_dead and field[temp_row_index][temp_column_index] == Marks.SHOT:
                        surround(temp_row_index, temp_column_index, field[temp_row_index][temp_column_index])

                    temp_row_index += vertical_delta
                    temp_column_index += horizontal_delta

                if check_dead:
                    count_directions += 1
            if count_directions == 4:
                print("ПОТОПИЛ!")
                return
            check_dead = True



print("\nДобро пожаловать в игру \"Морской бой\"!")
print("Ввод осуществляется по шаблону Буква + Цифра. Например \"А4\",\"J10\".")
print("Для вызова помощи введи \"help\".")
print("Изпользуй латинские буквы для ввода. Приятной игры!")

field_size = 10
field = init_field(field_size)
generate_ships()
win = False

while True:
    turn = input("\nВведи клетку, по которой будешь стрелять: ").upper()
    print()

    if turn == "STOP":
        print("Выход. До скорой встречи!")
        break

    if turn == "SIZE":
        while True:
            field_size = input("Введи размер нового поля: ")
            if not re.match(r"^[10-99]", field_size):
                print("Введи число от 10 до 99")
                continue
            field_size = int(field_size)
            field = init_field(field_size)
            generate_ships()
            break
        continue

    if turn == "HELP":
        print_help()
        continue

    if turn == "":
        print("Клетка не выбрана.")
        continue

    if turn == "SHOW":
        print_field(admin=True)
        continue

    if re.match(r"\w\d", turn) or re.match(r"\w\d\d", turn):
        if to_number(turn[0]) not in range(0, field_size+1):
            print("Введи нормальную букву! A B C D E F G H I J. Выбирай!")
            continue
        if int(turn[1:]) not in range(1, field_size+1):
            print("Цифры от 1 до 10! Без запятых!")
            continue
        row = int(turn[1:]) - 1
        column = to_number(turn[0])
        shot(row, column)
        print_field()
    else:
        print("Ничего не понял. Примеры ввода: A4, B7. Буква и цифра. Давай по новой, Миша!")
        continue

    for row in field:
        if Marks.BOARD in row:
            win = False
            break

    if win:
        print("Победа! Весь флот уничтожен!")
        break
    else:
        continue
