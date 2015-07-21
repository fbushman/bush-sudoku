__author__ = 'bushman'


from pprint import pprint


class Sudoku:
    def __init__(self, line=""):
        self.line = ""

        # Generate field possibles
        self.fields = {i: set([v for v in range(1, 10)]) for i in range(1, 82)}

        # Generate Rows:
        self.rows = {i: set([j for j in range(i * 9 - 8, i * 9 + 1)]) for i in range(1, 10)}

        # Generate Cols:
        self.cols = {i: set([j for j in range(i, i + 81, 9)]) for i in range(1, 10)}

        # Generate Areas:
        self.areas = {i: [] for i in range(1, 10)}
        d = 0
        for a in self.areas:
            vals = []
            for i in [1, 10, 19]:
                for j in range(3):
                    vals.append(i + j + d)
            self.areas[a] = set(vals)
            d += 3
            if a in [3, 6, 9]:
                d += 18

        # Aggregate Rows & Cols:
        self.rows_d_cols = {}
        self.rows_d_cols.update({"R{}".format(i): self.rows[i] for i in range(1, 10)})
        self.rows_d_cols.update({"C{}".format(i): self.cols[i] for i in range(1, 10)})

        # Aggregate Regions:
        self.regions = {}
        self.regions.update({"R{}".format(i): self.rows[i] for i in range(1, 10)})
        self.regions.update({"C{}".format(i): self.cols[i] for i in range(1, 10)})
        self.regions.update({"A{}".format(i): self.areas[i] for i in range(1, 10)})

        # Generate Field Coords
        self.coords = {i: self.i2rc(i) for i in range(1, 82)}

        # Initialize Sudoku
        if line != "":
            self.load_string(line)

    def __call__(self, row, col=None):
        """
        Return the field number and its possible values.
        Calling this object takes either a row and column, or just a field number.

        :type row: int
        :param row: Row or Field number
        :type col: int
        :param col: Row number
        :rtype: tuple
        :return: (Field number, Possibles)
        """
        if col:
            field = (self.rows[row] & self.cols[col]).pop()
        else:
            field = row
        return field, self.fields[field]

    def row(self, field, col=None):
        if col:
            field = self(field, col)[0]
        for row in self.rows:
            if len({field} & self.rows[row]):
                return field, self.rows[row]

    def col(self, field, col=None):
        if col:
            field = self(field, col)[0]
        for col in self.cols:
            if len({field} & self.cols[col]):
                return field, self.cols[col]

    def __str__(self):
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
                _, values = self(i)
                for num in range(1, 4):
                    char = str(num) if num in values else "`"
                    numbers1.append(char)
                for num in range(4, 7):
                    char = str(num) if num in values else "`"
                    numbers2.append(char)
                for num in range(7, 10):
                    char = str(num) if num in values else "`"
                    numbers3.append(char)
            lines.append(line1.format(*numbers1))
            lines.append(line2.format(*numbers2))
            lines.append(line3.format(*numbers3))
            if row in {2, 5}:
                lines.append("---------------------|----------------------|---------------------")
            elif row == 8:
                break
            else:
                lines.append("                     |                      |                     ")
        return "\n".join(lines) + "\n##################################################################"

    def print(self):
        print(self)

    def area(self, field, col=None):
        if col:
            field = self(field, col)[0]
        for area in self.areas:
            if len({field} & self.areas[area]):
                return area, self.areas[area]

    def load_string(self, sudoku_string):
        self.line = sudoku_string
        for index, value in enumerate(sudoku_string):
            if value in [".", "0"]:
                value = {1, 2, 3, 4, 5, 6, 7, 8, 9}
            else:
                try:
                    value = {int(value)}
                except ValueError:
                    print("[-] Load String: Bad Input in '{}'".format(sudoku_string))
                    raise
            self.fields[index + 1] = value
        # print("[+] Loaded sudoku string: {}".format(sudoku_string))

    def print_stats(self):
        print("\n[*] Rows")
        pprint(self.rows)
        print("\n[*] Cols")
        pprint(self.cols)
        print("\n[*] Areas")
        pprint(self.areas)
        # print("\n[*] Fields & Possibles")
        # pprint(self.fields)
        print("\n[*] Print Object")
        print(self)

    def print_test(self):
        print("\n[*] Tests")
        print("s(3,4): {}, {}".format(*self(3, 4)))
        print("s(22): {}, {}".format(*self(22)))
        print("s.row(3,4): {}, {}".format(*self.row(3, 4)))
        print("s.row(22): {}, {}".format(*self.row(22)))
        print("s.col(3,4): {}, {}".format(*self.col(3, 4)))
        print("s.col(22): {}, {}".format(*self.col(22)))
        print("s.area(3,4): {}, {}".format(*self.area(3, 4)))
        print("s.area(22): {}, {}".format(*self.area(22)))

    @staticmethod
    def matching_regions_single(s, loc):
        """
        :type s: Sudoku
        :type loc: int
        :rtype: set
        """
        locs = set()
        for _, region in s.regions.items():
            if loc in region:
                locs = locs | region - {loc}
        return locs

    @staticmethod
    def matching_regions(s, locs):
        """
        :type s: Sudoku
        :type locs: set
        :rtype: set
        """
        matching_locs = []
        for _, region in s.regions.items():
            if locs.issubset(region):
                for loc in region:
                    if loc in locs:
                        continue
                    matching_locs.append(loc)
        return set(matching_locs)

    @staticmethod
    def i2rc(i):
        r = (i - 1) // 9 + 1
        c = (i - 1) % 9 + 1
        return r, c

    @staticmethod
    def i2a(i):
        r = (i - 1) // 9 + 1
        c = (i - 1) % 9 + 1
        a = ((r + 2) // 3 - 1) * 3 + ((c + 2) // 3)
        return a

    @staticmethod
    def rc2a(row, col):
        a = ((row + 2) // 3 - 1) * 3 + ((col + 2) // 3)
        return a

    @staticmethod
    def rc2i(row, col):
        i = (9 * row) - 9 + col
        return i


def test():
    s = Sudoku()
    s.print_stats()
    s.print_test()


if __name__ == "__main__":
    test()
