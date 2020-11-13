"""
CLI implementation of a popular game Battleship.
https://en.wikipedia.org/wiki/Battleship_(game)
"""

import re
import random
import enum


class Marks:
    EMPTY = "mark_empty"
    BOARD = "mark_board"
    DAMAGED = "mark_damaged"
    DESTROYED = "mark_destroyed"
    MISSED = "mark_missed"


class Battleship(object):
    def __init__(self, field_size=10, ships_number=4):
        if not isinstance(field_size, int):
            raise ValueError("field_size must be an integer number from 10 to 99.")
        if field_size > 99:
            raise ValueError("field_size can not be bigger that 99.")
        self.field_size = field_size

        if not isinstance(ships_number, int):
            raise ValueError(
                "ship_number must be an integer number from 4 to field_size/2."
            )
        if ships_number > field_size / 2:
            raise ValueError("ship_number can not be bigger that half of a field size.")
        self.ships_number = ships_number

        self.generate_field()

    def print_help(self):
        print("Welcome to Battleship game!")
        print("Please check out the rules if you are unfamiliar with the game.")
        print("https://en.wikipedia.org/wiki/Battleship_(game)")
        print()
        print("Possible actions:")
        print("\texit - finish the game")
        print("\t[0-9][A-J] - shot")
        print("Good luck!")

    def print_field(self):
        print(f"   {' '.join(str(i) for i in range(10))}")
        for row_index, row in enumerate(self.field):
            formatted_row = f" {chr(row_index + 65)} {' '.join(str(i) for i in row)}"
            formatted_row = formatted_row.replace(str(Marks.EMPTY), " ")
            formatted_row = formatted_row.replace(str(Marks.BOARD), " ")
            formatted_row = formatted_row.replace(str(Marks.DAMAGED), "*")
            formatted_row = formatted_row.replace(str(Marks.DESTROYED), "X")
            formatted_row = formatted_row.replace(str(Marks.MISSED), ".")
            print(formatted_row)

    def run(self):
        game_continues = True
        turns_number = 0
        while game_continues:
            self.print_field()
            print("> ", end="")
            turn = input()
            if turn == "exit":
                print("Bye.")
                game_continues = False
            elif not re.match("^[A-Ja-j][0-9]$", turn):
                print("Wrong input, try again.")
            else:
                turns_number += 1
                shot_row = ord(turn[0].lower()) - 97
                shot_column = int(turn[1])
                if self.field[shot_row][shot_column] not in [Marks.EMPTY, Marks.BOARD]:
                    print("You already shoted this cell. Try again.")
                    continue
                hit = self.shot(shot_row, shot_column)
                if hit and all(cell != Marks.BOARD for cell in sum(self.field, [])):
                    self.print_field()
                    print("Victory!")
                    print(f"You won in {turns_number} turns")
                    game_continues = False

    def restart(self):
        self.generate_field()

    def generate_field(self):
        self.field = [[Marks.EMPTY] * self.field_size for _ in range(self.field_size)]
        for ship_size in range(self.ships_number, 0, -1):
            for ship_counter in range(self.ships_number - ship_size + 1):
                space_found = False
                while not space_found:
                    position_row = random.randint(0, self.field_size - 1)
                    position_column = random.randint(0, self.field_size - 1)
                    ship_direction = random.randint(0, 1)
                    if self.space_is_free(
                            ship_size, position_row, position_column, ship_direction
                    ):
                        space_found = True
                for row_index in range(
                        position_row, position_row + max(1, ship_size * ship_direction)
                ):
                    for column_index in range(
                            position_column,
                            position_column + max(1, ship_size * (1 - ship_direction)),
                    ):
                        self.field[row_index][column_index] = Marks.BOARD
                ship_placed = True

    def space_is_free(self, ship_size, position_row, position_column, ship_direction):
        for row_index in range(
                position_row, position_row + max(1, ship_size * ship_direction)
        ):
            for column_index in range(
                    position_column,
                    position_column + max(1, ship_size * (1 - ship_direction)),
            ):
                if not self.cell_in_range(row_index, column_index):
                    return False
                if self.field[row_index][column_index] != Marks.EMPTY:
                    return False
                for row_offset in [-1, 0, 1]:
                    for column_offset in [-1, 0, 1]:
                        if (
                                self.cell_in_range(
                                    row_index + row_offset, column_index + column_offset
                                )
                                and self.field[row_index + row_offset][
                            column_index + column_offset
                        ]
                                != Marks.EMPTY
                        ):
                            return False
        return True

    def shot(self, row_index, column_index):
        hit = False
        if self.field[row_index][column_index] == Marks.EMPTY:
            self.field[row_index][column_index] = Marks.MISSED
        else:
            self.field[row_index][column_index] = Marks.DAMAGED
            hit = True
            if self.is_destroyed(row_index, column_index):
                self.mark_destroyed(row_index, column_index)
        return hit

    def is_destroyed(self, row_index, column_index):
        for row_offset_step, column_offset_step in [[-1, 0], [0, -1], [1, 0], [0, 1]]:
            row_offset = 0
            column_offset = 0
            while True:
                row_offset += row_offset_step
                column_offset += column_offset_step
                if not self.cell_in_range(
                        row_index + row_offset, column_index + column_offset
                ):
                    break
                if (
                        self.field[row_index + row_offset][column_index + column_offset]
                        == Marks.BOARD
                ):
                    return False
                elif (
                        self.field[row_index + row_offset][column_index + column_offset]
                        == Marks.DAMAGED
                ):
                    continue
                else:
                    break
        return True

    def mark_destroyed(
            self, row_index, column_index, row_offset_step=0, column_offset_step=0
    ):
        if not self.cell_in_range(row_index, column_index):
            return

        if self.field[row_index][column_index] in [Marks.EMPTY, Marks.MISSED]:
            return

        if self.field[row_index][column_index] in [Marks.DAMAGED, Marks.DESTROYED]:
            self.field[row_index][column_index] = Marks.DESTROYED
            for row_offset in [-1, 0, 1]:
                for column_offset in [-1, 0, 1]:
                    if (
                            self.cell_in_range(
                                row_index + row_offset, column_index + column_offset
                            )
                            and self.field[row_index + row_offset][
                        column_index + column_offset
                    ]
                            == Marks.EMPTY
                    ):
                        self.field[row_index + row_offset][
                            column_index + column_offset
                            ] = Marks.MISSED

            if row_offset_step or column_offset_step:
                self.mark_destroyed(
                    row_index + row_offset_step,
                    column_index + column_offset_step,
                    row_offset_step,
                    column_offset_step,
                )
            else:
                for row_offset, column_offset in [[-1, 0], [0, -1], [1, 0], [0, 1]]:
                    self.mark_destroyed(
                        row_index + row_offset,
                        column_index + column_offset,
                        row_offset,
                        column_offset,
                    )

    def cell_in_range(self, row_index, column_index):
        return 0 <= row_index < self.field_size and 0 <= column_index < self.field_size


if __name__ == "__main__":
    game = Battleship()
    game.run()