# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
#
# «четрыехпалубные» авианосцы - Aerocarrier
# «трехпалубные» крейсера - Cruiser
# «двухпалубные» эсминцы - Destroyer
# «однопалубные» торпедные катера - Boats
#
# обозначение палубы ◙

class Ship(object):
    """Class for ships"""

    letter_to_number = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7, 'I': 8, 'J': 9}
    number_to_letter = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'H', 8: 'I', 9: 'J'}

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
        cell[0] = int(cell[0])-1
        direction = input("Enter direction (R/D): ").upper()
        if direction == "R":
            pos = self.letter_to_number[cell[1]]
            for k in range(self.size):
                pos += 1
                shadow_field[cell[0]][pos-1] = "+"
                for i in [-1, 0, 1]:
                    for j in [-1, 0, 1]:
                        try:
                            if shadow_field[cell[0] + i][pos - 1 + j] != "+" and (cell[0] + i and pos - 1 + j >= 0):
                                shadow_field[cell[0] + i][pos - 1 + j] = "-"
                        except IndexError:
                            pass
                temp_position.append([cell[0], self.number_to_letter[pos-1]])
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
                temp_position.append([pos-1, cell[1]])
        self.position = tuple(temp_position)
        print(f"Ship {self.name} placed!")
        return

    def shot(self):
        """Register a shot"""
        return

    def _print_position(self):
        """Print current position of ship"""
        for digit, letter in self.position:
            print(letter, digit+1)
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
        print(i, " "*(3 - len(str(i))), end="", sep="")
        for letter in line:
            print(letter, end="")
        print()


shadow_field = [[" "]*10 for i in range(10)]
battle_field = [[" "]*10 for i in range(10)]

show_field(shadow_field)
print()
four_celled = Ship("Aerocarrier", 4)
four_celled.place()
show_field(shadow_field)
three_celled_1 = Ship("Cruiser 1", 3)
three_celled_1.place()
show_field(shadow_field)



