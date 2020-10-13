# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

class Ship(object):
    """Class for ships"""

    letter_to_number = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7, 'I': 8, 'J': 9}
    number_to_letter = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'H', 8: 'I', 9: 'J'}

    def __init__(self, name=None, size=0, position=[]):
        """Constructor"""
        self.name = name
        self.size = size
        self.position = position

    def place(self):
        """Position ship in place"""
        cell = [a for a in input("Enter top/left cell: ")[-1: -2]]
        direction = input("Enter direction (R/D): ")
        print(cell, cell[0], cell[1], direction)
        #cell = list(cell)
        #cell.reverse()
        cell[1] = self.letter_to_number[cell[1]]
        cell[0] = int(cell[1])
        if direction == "R":
            pos = cell[1]
            for i in range(self.size):
                pos += i
                self.position.append([self.number_to_letter[pos], cell[0]])
        elif direction == "D":
            pos = cell[0]
            for i in range(self.size):
                pos += i
                self.position.append(reversed([self.number_to_letter[pos], cell[1]]))
        print(f"Ship {self.name} placed!")

    def shot(self):
        """Register a shot"""
        return


four_celled = Ship("Aerocarrier", 4)
four_celled.place()
print(str(four_celled.position[1]))
three_celled_1 = Ship("Cruiser 1", 3)
three_celled_1.place()
print(three_celled_1.position)
