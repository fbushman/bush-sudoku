__author__ = 'bushman'

import math

from v1 import tools


class Field:
    row = 0
    col = 0
    area = 0
    val = {1, 2, 3, 4, 5, 6, 7, 8, 9}

    def __init__(self, i, row, column, value=None, rand=None):
        if value:
            self.val = value
        elif rand:
            self.val = tools.random_value()
        self.i = i
        self.row = row
        self.col = column
        self.area = (math.ceil(row/3) * 3 - 2) + (math.ceil(column/3) - 1)

    def __str__(self):
        if len(self.val) > 1:
            return " "
        else:
            return set(self.val).pop()

    def __len__(self):
        return len(self.val)

    def remove(self, value):
        try:
            value = set(value)
            self.val = set(self.val - value)
        except TypeError:
            self.val = set(self.val - {value})