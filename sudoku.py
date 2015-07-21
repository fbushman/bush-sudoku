__author__ = 'bushman'

import threading

from v1 import tools
from v1.tools import Colors
from v1.field import Field


class SudokuList:
    def __init__(self):
        self.list = []
        self.lock = threading.Lock()
        self.get = self.get()

    def add(self, string, level):
        self.lock.acquire()
        self.list.append((string, level))

    def get(self):
        yield self.list.pop()


class Sudoku:
    changes = 0
    fields = dict()
    level = "Not set"
    error_line = str()
    line = ""
    loader = None

    def __init__(self, rand=None):
        self.rows = {i: [] for i in range(1, 10)}
        self.cols = {i: [] for i in range(1, 10)}
        self.areas = {i: [] for i in range(1, 10)}
        self.error_line = Colors.OKBLUE + "[-] {}" + Colors.ENDC
        if rand:
            rand = True
        i = 0
        for row in range(1, 10):
            for col in range(1, 10):
                i += 1
                self.fields[i] = Field(i, row, col, rand=rand)
                self.cols[col].append(i)
                self.rows[row].append(i)
                self.areas[tools.rc2a(row, col)].append(i)

    def __str__(self):
        # lines = ["[+] Sudoku Possibles"]
        lines = []
        line1 = "{} {} {}  {} {} {}  {} {} {}  | {} {} {}  {} {} {}  {} {} {}  | {} {} {}  {} {} {}  {} {} {}"
        line2 = "{} {} {}  {} {} {}  {} {} {}  | {} {} {}  {} {} {}  {} {} {}  | {} {} {}  {} {} {}  {} {} {}"
        line3 = "{} {} {}  {} {} {}  {} {} {}  | {} {} {}  {} {} {}  {} {} {}  | {} {} {}  {} {} {}  {} {} {}"
        i = 0
        for row in range(9):
            numbers1 = []
            numbers2 = []
            numbers3 = []
            for col in range(9):
                i += 1
                values = self.fields[i].val
                for num in range(1, 4):
                    if num in values:
                        numbers1.append(str(num))
                    else:
                        numbers1.append("`")
                for num in range(4, 7):
                    if num in values:
                        numbers2.append(str(num))
                    else:
                        numbers2.append("`")
                for num in range(7, 10):
                    if num in values:
                        numbers3.append(str(num))
                    else:
                        numbers3.append("`")
            lines.append(line1.format(*numbers1))
            lines.append(line2.format(*numbers2))
            lines.append(line3.format(*numbers3))
            if row in {2, 5}:
                lines.append("---------------------|----------------------|---------------------")
            elif row == 8:
                break
            else:
                lines.append("                     |                      |                     ")
        return "\n".join(lines)

    def print(self, level=None, numbers=None, possibles=None):
        if level:
            print("[+] Level: {}".format(self.level))
        if numbers:
            tools.print_field_numbers()
        if possibles:
            print(self)

    def load_string(self, sudoku_string):
        self.line = sudoku_string
        for index, value in enumerate(sudoku_string):
            if value in [".", "0"]:
                value = {1, 2, 3, 4, 5, 6, 7, 8, 9}
            else:
                try:
                    value = {int(value)}
                except ValueError:
                    print("[-} load_string: Bad Input!")
                    raise
            r, c = tools.i2rc(index + 1)
            self.fields[index + 1] = Field(index+1, r, c, value)
        # print("[+] Loaded sudoku string: {}".format(sudoku_string))

    def row(self, i=None, row=None):
        if i:
            r, c = tools.i2rc(i)
            retval = []
            for col in range(1, 10):
                retval.append(tools.rc2i(r, col))
        elif row:
            retval = []
            for col in range(1, 10):
                retval.append(tools.rc2i(row, col))
        else:
            print(self.error_line.format("No kwargs set!"))
            raise Exception
        return set(retval)

    def col(self, i=None, col=None):
        if i:
            r, c = tools.i2rc(i)
            retval = []
            for row in range(1, 10):
                retval.append(tools.rc2i(row, c))
        elif col:
            retval = []
            for row in range(1, 10):
                retval.append(tools.rc2i(row, col))
        else:
            print(self.error_line.format("No kwargs set!"))
            raise Exception
        return set(retval)
