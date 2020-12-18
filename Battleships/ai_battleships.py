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


def init_field(field_size=10):
    return [[Marks.EMPTY] * field_size for _ in range(field_size)]


def print_field(field):
    print(f'   {" ".join((chr(65 + i) for i in range(len(field[0]))))}')
    for row_index, row in enumerate(field):
        formatted_row = f'{row_index + 1:2} {" ".join(str(i) for i in row)}'
        formatted_row = formatted_row.replace(str(Marks.EMPTY), " ")
        formatted_row = formatted_row.replace(str(Marks.NEARBY), "+")
        formatted_row = formatted_row.replace(str(Marks.BOARD), "◙")
        formatted_row = formatted_row.replace(str(Marks.SHOT), "X")
        formatted_row = formatted_row.replace(str(Marks.WATER), "●")
        print(formatted_row)


def generate_ships(field, seed=0):
    if seed != 0:
        random.seed(seed)
    for ship_size in range(4):
        ship_size += 1
        for i in range(5 - ship_size):
            check_done = False
            while not check_done:
                check_place = False
                while not check_place:
                    row_index, column_index = [random.randint(0, field_size - 1), random.randint(0, field_size - 1)]
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
                            if (temp_row not in range(field_size - 1) or temp_column not in range(field_size - 1)) or \
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
            place_ship(field, row_index, column_index, row_delta, column_delta, ship_size)
    print("\nКорабли размещены. К бою!")
    return field


def surround(field, row_index, column_index, mark):
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


def place_ship(field, row_index, column_index, row_delta, column_delta, size, *direction):
    for _ in range(size):
        field[row_index][column_index] = Marks.BOARD
        surround(field, row_index, column_index, field[row_index][column_index])
        row_index += row_delta
        column_index += column_delta


def is_destroyed(field, row_index, column_index, check_dead=False):
    while True:
        for vertical_delta, horizontal_delta in direction_delta:
            temp_row_index = row_index
            temp_column_index = column_index
            while True:
                if temp_row_index not in range(field_size) or temp_column_index not in range(field_size):
                    break

                if field[temp_row_index][temp_column_index] in [Marks.NEARBY, Marks.WATER]:
                    break

                if field[temp_row_index][temp_column_index] == Marks.BOARD:
                    return False  # РАНИЛ!

                temp_row_index += vertical_delta
                temp_column_index += horizontal_delta
        break
    return True  # ПОТОПИЛ!


def destroyed(field, row_index, column_index):
    count_directions = 0
    while True:
        for vertical_delta, horizontal_delta in direction_delta:
            temp_row_index = row_index
            temp_column_index = column_index
            while True:
                if temp_row_index not in range(field_size) or temp_column_index not in range(field_size):
                    break

                if field[temp_row_index][temp_column_index] == Marks.SHOT:
                    surround(field, temp_row_index, temp_column_index, Marks.SHOT)
                else:
                    break

                temp_row_index += vertical_delta
                temp_column_index += horizontal_delta
            count_directions += 1
        if count_directions == 4:
            return


def put_mark(field, row_index, column_index, response):
    if response == Marks.BOARD:
        field[row_index][column_index] = Marks.SHOT
    elif response == Marks.SHOT:
        field[row_index][column_index] = Marks.SHOT
        destroyed(field, row_index, column_index)
    else:
        field[row_index][column_index] = Marks.WATER


def shot(field, row_index, column_index):  # РЕГИСТРАЦИЯ ВЫСТРЕЛА И ПРОВЕРКА НА УБИЙСТВО
    if field[row_index][column_index] in [Marks.EMPTY, Marks.NEARBY]:
        put_mark(field, row_index, column_index, Marks.WATER)
        print("МИМО!")
        return Marks.WATER

    if field[row_index][column_index] in [Marks.WATER, Marks.SHOT]:
        line = f"Ты сюда стрелял. Тут {str(field[row_index][column_index])}"
        line = line.replace(str(Marks.WATER), "●").replace(str(Marks.SHOT), "X")
        # print(line)
        return

    if field[row_index][column_index] == Marks.BOARD:
        put_mark(field, row_index, column_index, Marks.BOARD)
        return Marks.BOARD


def my_choice(
        field, field_size,
        first_shot_cell, destroying_cell, vert_or_horiz, direction_number,
        response
):
    if response == Marks.WATER:
        if first_shot_cell[0] != -1:
            print("Shot cell YES")
            if vert_or_horiz == 2:
                print("Choose random direction")
                while True:
                    vert_or_horiz = random.randint(0, 1)
                    direction_number = random.randint(0, 1)
                    destroying_cell = [x + y for x, y in
                                       zip(first_shot_cell, numerated_directions[vert_or_horiz][direction_number])]
                    if 0 <= destroying_cell[0] < field_size + 1 or 0 < destroying_cell[0] < field_size + 1:
                        break
                return to_letter(destroying_cell[1]), destroying_cell[0] + 1, destroying_cell, vert_or_horiz,\
                       direction_number
            else:
                direction_number -= 1
                destroying_cell = [x + y for x, y in
                                   zip(first_shot_cell, numerated_directions[vert_or_horiz][direction_number])]
                if direction_number == -2 or field[destroying_cell[0]][destroying_cell[1]] != Marks.EMPTYY:
                    print("Change vert/horiz")
                    vert_or_horiz -= 1
                    direction_number = random.randint(0, 1)
                destroying_cell = [x + y for x, y in
                                   zip(first_shot_cell, numerated_directions[vert_or_horiz][direction_number])]
                if not 0 < destroying_cell[0] < field_size + 1 or not 0 < destroying_cell[1] < field_size + 1:
                    direction_number -= 1
                    destroying_cell = [x + y for x, y in
                                       zip(first_shot_cell, numerated_directions[vert_or_horiz][direction_number])]
                return to_letter(destroying_cell[1]), destroying_cell[0] + 1, destroying_cell, vert_or_horiz, \
                       direction_number
        else:
            print("Shot cell NO")
            while True:
                temp_row = random.randint(0, field_size - 1)
                temp_column = random.randint(0, field_size - 1)
                if field[temp_row][temp_column] == Marks.EMPTY:
                    break
            return to_letter(temp_column), temp_row + 1, destroying_cell, vert_or_horiz, direction_number
    elif response == Marks.BOARD:
        if vert_or_horiz == 2:
            print("Choice random direction")
            while True:
                vert_or_horiz = random.randint(0, 1)
                direction_number = random.randint(0, 1)
                destroying_cell = [x+y for x, y in zip(first_shot_cell, numerated_directions[vert_or_horiz][direction_number])]
                if 0 <= destroying_cell[0] < field_size + 1 or 0 < destroying_cell[0] < field_size + 1:
                    break
        else:
            destroying_cell = [x + y for x, y in
                               zip(destroying_cell, numerated_directions[vert_or_horiz][direction_number])]
            if not 0 < destroying_cell[0] < field_size + 1 or not 0 < destroying_cell[1] < field_size + 1:
                direction_number -= 1
                destroying_cell = [x + y for x, y in
                                   zip(first_shot_cell, numerated_directions[vert_or_horiz][direction_number])]
        print(f"shot_cell is {first_shot_cell}, vert_or_horiz is {vert_or_horiz}, direction_number is {direction_number}")
        print(f"destroying_row is {destroying_cell[0]}, destroying_col is {destroying_cell[1]}")
        return to_letter(destroying_cell[1]), destroying_cell[0] + 1, destroying_cell, vert_or_horiz, direction_number
    else:
        if response == Marks.SHOT:
            destroying_cell = [-1, -1]
            vert_or_horiz = 2
            direction_number = 2
            destroyed(enemy_field, first_shot_cell[0], first_shot_cell[1])
        while True:
            temp_row = random.randint(0, field_size - 1)
            temp_column = random.randint(0, field_size - 1)
            if field[temp_row][temp_column] == Marks.EMPTY:
                break
        return to_letter(temp_column), temp_row + 1, destroying_cell, vert_or_horiz, direction_number


print("\nДобро пожаловать в игру \"Морской бой\"!")
print("Ввод осуществляется по шаблону Буква + Цифра. Например \"А4\",\"J10\".")
print("Для вызова помощи введи \"help\".")
print("Изпользуй латинские буквы для ввода. Приятной игры!")


direction_delta = [[-1, 0], [1, 0], [0, -1], [0, 1]]  # ВВЕРХ, ВНИЗ, ВЛЕВО, ВПРАВО
numerated_directions = [[[1, 0], [-1, 0]], [[0, 1], [0, -1]]]

field_size = 10
my_field = init_field(field_size)
enemy_field = init_field(field_size)
generate_ships(my_field, 1)
empty_enemy_cells = 0

first_shot_cell = [-1, -1]
destroying_cell = [-1, -1]
vert_or_horiz = 2
direction_number = 2
response = False
line_reading = 0

file_using = True
win = False
lose = True
my_turn = input("Я начинаю первым? Y/N\n> ").upper()
if my_turn == "N":
    my_turn = False
else:
    my_turn = True
if file_using:
    f1 = open("move_list.txt", "r")
while True:
    if my_turn:
        print(f"vert_or_horiz is {vert_or_horiz}")
        print(f"first_shot_cell is {first_shot_cell}")
        column_index, row_index, destroying_cell, vert_or_horiz, direction_number = my_choice(
            enemy_field, field_size,
            first_shot_cell, destroying_cell, vert_or_horiz, direction_number,
            response
        )
        print()
        print(f"Мой ход: {column_index}, {row_index}")
        column_index = to_number(column_index)
        row_index -= 1
        response = input("Какой результат выстрела?\n> ").upper()
        if response == "МИМО!":
            response = Marks.WATER
            my_turn = not my_turn
        elif response == "РАНИЛ!":
            response = Marks.BOARD
            if first_shot_cell[0] == -1:
                first_shot_cell = [row_index, column_index]
        elif response == "ПОТОПИЛ!":
            response = Marks.SHOT
            first_shot_cell = [-1, -1]
        put_mark(enemy_field, row_index, column_index, response)
        print_field(enemy_field)
        print()
        continue
    else:
        turn = input("\nВведи клетку, по которой был выстрел.\n> ").upper()
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
            if input("Размер чьего поля изменяется?: ").upper() == "MY":
                my_field = init_field(field_size)
                generate_ships(my_field)
            else:
                enemy_field = init_field(field_size)
            break
        continue

    if turn == "HELP":
        print_help()
        continue

    if turn == "":
        print("Клетка не выбрана.")
        continue

    if turn == "MY":
        print_field(my_field)
        continue

    if turn == "ENEMY":
        print_field(enemy_field)
        continue

    if re.match(r"^\w[1-99]", turn):
        if to_number(turn[0]) not in range(0, field_size + 1):
            print("Введи нормальную букву! A B C D E F G H I J. Выбирай!")
            continue
        if int(turn[1:]) not in range(1, field_size + 1):
            print("Цифры от 1 до 10! Без запятых!")
            continue
        row_index = int(turn[1:]) - 1
        column_index = to_number(turn[0])
        put_mark(my_field, row_index, column_index, shot(my_field, row_index, column_index))
        if my_field[row_index][column_index] == Marks.WATER:
            my_turn = not my_turn
            print_field(my_field)
            continue
        elif is_destroyed(my_field, row_index, column_index):
            destroyed(my_field, row_index, column_index)
            print("ПОТОПИЛ!")
        else:
            print("РАНИЛ!")
        print_field(my_field)
    else:
        print("Ничего не понял. Примеры ввода: A4, B7. Буква и цифра. Давай по новой, Миша!")
        continue

    for row in my_field:
        if Marks.BOARD in row:
            lose = False
            break

    destroyed_boards = 0
    empty_enemy_cells = 0
    for row in enemy_field:
        destroyed_boards += row.count(Marks.SHOT)
        empty_enemy_cells += row.count(Marks.EMPTY)

    if destroyed_boards == 20:
        print("Победа! Флот врага уничтожен!")
        break
    elif empty_enemy_cells == 0:
        print("Победа! Поле врага зачищено!")
        break

    if lose:
        print("Проигрыш! Дружественный флот уничтожен!")
        break

if file_using:
    f1.close()
