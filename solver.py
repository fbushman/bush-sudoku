__author__ = 'bushman'

import itertools

from v1 import tools
from v1.tools import prnt
from v2.sudoku import Sudoku


class Solver(object):
    def __init__(self):
        self.sudoku = Sudoku()
        self.complete_fields = []
        self.changes = 0
        self.update_line = "{} I{:2} -> I{:2}: {:27} => {:27}"
        self.freq_area = {i: [] for i in range(1, 10)}
        self.freq_col = {i: [] for i in range(1, 10)}
        self.freq_row = {i: [] for i in range(1, 10)}

    def load_string(self, sudoku_string):
        self.changes = 0
        self.sudoku.load_string(sudoku_string)
        self.find_complete_fields()

    def find_complete_fields(self):
        self.complete_fields = []
        for field in self.sudoku.fields:
            if len(self.sudoku.fields[field].val) > 1:
                continue
            self.complete_fields.append(field)

    def run(self, verbose=0, msg=""):
        # TODO: use list of technique_methods to loop over and call this method
        # def technique(method, name):
        #     if verbose >= 2:
        #         prnt("{}{}".format(msg, name), level=2)
        #     if method():
        #         if verbose >= 1:
        #             if verbose >= 3:
        #                 self.sudoku.print(possibles=True)
        #             prnt("{}{}: {}".format(msg, name, self.changes), level=1)
        #         return True
        #     elif verbose >= 3:
        #         self.sudoku.print(possibles=True)
        #         prnt("{}{}: {}".format(msg, name, self.changes), level=4)

        if verbose >= 1:
            if msg != "":
                msg = "[{}]".format(msg)
            prnt("{}Running loaded sudoku: {:50}".format(msg, self.sudoku.line), level=2)
        while True:
            self.find_complete_fields()
            if len(self.complete_fields) == 81:
                if verbose >= 1:
                    if verbose >= 3:
                        self.sudoku.print(possibles=True)
                    prnt("{}Sudoku is Solved!".format(msg), level=1)
                return True
            # if verbose >= 2:
            #     prnt("{}Naked Singles".format(msg), level=2)
            if self.naked_singles():
                if verbose >= 1:
                    if verbose >= 3:
                        self.sudoku.print(possibles=True)
                    prnt("{}Naked: {}".format(msg, self.changes), level=1)
                continue
            elif verbose >= 3:
                self.sudoku.print(possibles=True)
                prnt("{}Naked: {}".format(msg, self.changes), level=4)
            self.frequency_dicts()
            # if verbose >= 2:
            #     prnt("{}Hidden Singles".format(msg), level=2)
            if self.hidden(verbose=verbose):
                if verbose >= 1:
                    if verbose >= 3:
                        self.sudoku.print(possibles=True)
                    prnt("{}Hidden: {}".format(msg, self.changes), level=1)
                continue
            elif verbose >= 3:
                self.sudoku.print(possibles=True)
                prnt("{}Hidden: {}".format(msg, self.changes), level=4)
            # if verbose >= 2:
            #     prnt("{}Poiting Pairs".format(msg), level=2)
            if self.pointing_pairs():  # (verbose=verbose):
                if verbose >= 1:
                    if verbose >= 3:
                        self.sudoku.print(possibles=True)
                    prnt("{}Pointing Pairs: {}".format(msg, self.changes), level=1)
                continue
            elif verbose >= 3:
                self.sudoku.print(possibles=True)
                prnt("{}Pointing Pairs: {}".format(msg, self.changes), level=4)
            break

        if verbose:
            # self.sudoku.print(possibles=True)
            prnt("{}No more techniques to try. {}/81 found.".format(msg, len(self.complete_fields)), level=4)
        return False

    def naked_singles_field(self, row, col):
        def run(fields):
            if current_i not in fields:
                return
            for ix in fields:
                if current_i == ix:
                    continue
                ix_value = self.sudoku.fields[ix].val
                if len(current_value & ix_value) > 0:
                    new_value = set(ix_value - current_value)
                    self.sudoku.fields[ix].val = new_value
                    self.changes += 1
        field = self.sudoku.fields[tools.rc2i(row, col)]
        current_value = field.val
        current_i = tools.rc2i(row, col)
        if len(current_value) > 1:
            return
        for a in self.sudoku.areas:
            run(self.sudoku.areas[a])
        for c in self.sudoku.cols:
            run(self.sudoku.cols[c])
        for r in self.sudoku.rows:
            run(self.sudoku.rows[r])

    def naked_singles(self):
        self.changes = 0
        i = 0
        for row in range(1, 10):
            for col in range(1, 10):
                i += 1
                if len(self.sudoku.fields[i].val) > 1:
                    continue
                self.naked_singles_field(row, col)
        return self.changes

    def frequency_dicts(self):
        self.freq_area = {i: [] for i in range(1, 10)}
        self.freq_col = {i: [] for i in range(1, 10)}
        self.freq_row = {i: [] for i in range(1, 10)}
        section_i = 0
        for area in self.sudoku.areas:
            section_i += 1
            frequency = {1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: []}
            for field_i in self.sudoku.areas[area]:
                # if len(self.sudoku.fields[field_i].val) == 1:
                #     continue
                for val in self.sudoku.fields[field_i].val:
                    frequency[val].append(field_i)
            self.freq_area[section_i] = frequency
        section_i = 0
        for row in self.sudoku.rows:
            section_i += 1
            frequency = {1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: []}
            for field_i in self.sudoku.rows[row]:
                # if len(self.sudoku.fields[field_i].val) == 1:
                #     continue
                for val in self.sudoku.fields[field_i].val:
                    frequency[val].append(field_i)
            self.freq_row[section_i] = frequency
        section_i = 0
        for col in self.sudoku.cols:
            section_i += 1
            frequency = {1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: []}
            for field_i in self.sudoku.cols[col]:
                # if len(self.sudoku.fields[field_i].val) == 1:
                #     continue
                for val in self.sudoku.fields[field_i].val:
                    frequency[val].append(field_i)
            self.freq_col[section_i] = frequency

    def hidden(self, verbose=None):
        def single(values, section_i, section_type=" "):
            f = -1
            for f in values:
                break
            _old_value = self.sudoku.fields[f].val
            if len(_old_value) == 1:
                return
            if verbose >= 3:
                prnt("", level=2)
                self.sudoku.print(possibles=True)
            self.sudoku.fields[f].val = {number}
            if verbose >= 2:
                _new_value = self.sudoku.fields[f].val
                if len(_new_value) == 0:
                    return
                prnt(self.update_line.format("[S] {}{}".format(section_type, str(section_i).zfill(2)),
                                             str(f).zfill(2),
                                             str(f).zfill(2),
                                             str(_old_value),
                                             str(_new_value)), level=0)
                r, c = tools.i2rc(f)
                self.naked_singles_field(r, c)
                if verbose >= 3:
                    self.sudoku.print(possibles=True)
                # prnt("", level=3)
            self.changes += 1

        def double():
            # TODO
            self.changes += 0

        self.changes = 0
        for area in self.freq_area:
            for number in self.freq_area[area]:
                val = self.freq_area[area][number]
                if len(val) == 1:
                    single(val, area, section_type="A")
                    continue
                elif len(val) == 2:
                    for n in self.freq_area[area]:
                        if n == number:
                            continue
                        match = self.freq_area[area][n]
                        if set(match) == set(val):
                            double()
                            continue
        if self.changes > 0:
            return self.changes
        for row in self.freq_row:
            for number in self.freq_row[row]:
                val = self.freq_row[row][number]
                if len(val) == 1:
                    single(val, row, section_type="R")
                    continue
                elif len(val) == 2:
                    for n in self.freq_row[row]:
                        if n == number:
                            continue
                        match = self.freq_row[row][n]
                        if set(match) == set(val):
                            double()
                            continue
        if self.changes > 0:
            return self.changes
        for col in self.freq_col:
            for number in self.freq_col[col]:
                val = self.freq_col[col][number]
                if len(val) == 1:
                    single(val, col, section_type="C")
                    continue
                elif len(val) == 2:
                    for n in self.freq_col[col]:
                        if n == number:
                            continue
                        match = self.freq_col[col][n]
                        if set(match) == set(val):
                            double()
                            continue
        return self.changes

    def pointing_pairs(self):
        for area in self.freq_area:
            for value in self.freq_area[area]:
                if len(self.freq_area[area][value]) == 2:
                    # TODO: Find value with matching locations
                    for value2 in self.freq_area[area]:
                        if value == value2:
                            continue
                        i1 = self.freq_area[area][value]
                        i2 = self.freq_area[area][value2]
                        if set(i1) == set(i2):
                            for rw in self.sudoku.rows:
                                rw_x = self.sudoku.rows[rw]
                                if len(set(i1) & set(rw_x)) == len(i1):
                                    # Remove value from row except from a_i and b_i
                                    for i in rw_x:
                                        old_length = len(self.sudoku.fields[i])
                                        if i in i1 or old_length == 1:
                                            continue
                                        self.sudoku.fields[i].remove(value)
                                        new_length = len(self.sudoku.fields[i])
                                        if old_length != new_length:
                                            self.changes += 1
                                            pass
                                    break
                            for cl in self.sudoku.cols:
                                cl_x = self.sudoku.cols[cl]
                                if len(set(i1) & set(cl_x)) == len(i1):
                                    # Remove value from col except from a_i and b_i
                                    for i in cl_x:
                                        old_length = len(self.sudoku.fields[i])
                                        if i in i1 or old_length == 1:
                                            continue
                                        self.sudoku.fields[i].remove(value)
                                        new_length = len(self.sudoku.fields[i])
                                        if old_length != new_length:
                                            self.changes += 1
                                            pass
                                    break
        for row in self.freq_row:
            for value in self.freq_row[row]:
                if len(self.freq_row[row][value]) == 2:
                    # TODO: Find value with matching locations
                    for value2 in self.freq_row[row]:
                        if value == value2:
                            continue
                        i1 = self.freq_row[row][value]
                        i2 = self.freq_row[row][value2]
                        if set(i1) == set(i2):
                            for cl in self.sudoku.cols:
                                cl_x = self.sudoku.cols[cl]
                                if len(set(i1) & set(cl_x)) == len(i1):
                                    # Remove value from col except from a_i and b_i
                                    for i in cl_x:
                                        old_length = len(self.sudoku.fields[i])
                                        if i in i1 or old_length == 1:
                                            continue
                                        self.sudoku.fields[i].remove(value)
                                        new_length = len(self.sudoku.fields[i])
                                        if old_length != new_length:
                                            self.changes += 1
                                            pass
                                    break
                            for ar in self.sudoku.areas:
                                ar_x = self.sudoku.areas[ar]
                                if len(set(i1) & set(ar_x)) == len(i1):
                                    # Remove value from col except from a_i and b_i
                                    for i in ar_x:
                                        old_length = len(self.sudoku.fields[i])
                                        if i in i1 or old_length == 1:
                                            continue
                                        self.sudoku.fields[i].remove(value)
                                        new_length = len(self.sudoku.fields[i])
                                        if old_length != new_length:
                                            self.changes += 1
                                            pass
                                    break
        for col in self.freq_col:
            for value in self.freq_col[col]:
                if len(self.freq_col[col][value]) == 2:
                    # TODO: Find value with matching locations
                    for value2 in self.freq_col[col]:
                        if value == value2:
                            continue
                        i1 = self.freq_col[col][value]
                        i2 = self.freq_col[col][value2]
                        if set(i1) == set(i2):
                            for rw in self.sudoku.rows:
                                rw_x = self.sudoku.rows[rw]
                                if len(set(i1) & set(rw_x)) == len(i1):
                                    # Remove value from row except from a_i and b_i
                                    for i in rw_x:
                                        old_length = len(self.sudoku.fields[i])
                                        if i in i1 or old_length == 1:
                                            continue
                                        self.sudoku.fields[i].remove(value)
                                        new_length = len(self.sudoku.fields[i])
                                        if old_length != new_length:
                                            self.changes += 1
                                            pass
                                    break
                            for ar in self.sudoku.areas:
                                ar_x = self.sudoku.areas[ar]
                                if len(set(i1) & set(ar_x)) == len(i1):
                                    # Remove value from col except from a_i and b_i
                                    for i in ar_x:
                                        old_length = len(self.sudoku.fields[i])
                                        if i in i1 or old_length == 1:
                                            continue
                                        self.sudoku.fields[i].remove(value)
                                        new_length = len(self.sudoku.fields[i])
                                        if old_length != new_length:
                                            self.changes += 1
                                            pass
                                    break
        return self.changes

    def pointing_triples(self):
        for area in self.freq_area:
            for a, b, c in itertools.combinations([j for j in self.freq_area[area] if 2 >= len(j) <= 3], 3):
                if len(a | b | c) == 3:
                    for rw in self.freq_row:
                        if a in self.freq_row[rw] and b in self.freq_row[rw]:
                            # TODO: Remove set(a) from row
                            pass
                    for cl in self.freq_col:
                        if a in self.freq_col[cl] and b in self.freq_col[cl]:
                            # TODO: Remove set(a) from col
                            pass
        for row in self.freq_row:
            for a, b in itertools.combinations([j for j in self.freq_row[row] if 2 >= len(j) <= 3], 3):
                if a == b:
                    for cl in self.freq_col:
                        if a in self.freq_col[cl] and b in self.freq_col[cl]:
                            # TODO: Remove set(a) from col
                            pass
                    for ar in self.freq_area:
                        if a in self.freq_area[ar] and b in self.freq_area[ar]:
                            # TODO: Remove set(a) from area
                            pass
        for col in self.freq_col:
            for a, b in itertools.combinations([j for j in self.freq_col[col] if 2 >= len(j) <= 3], 3):
                if a == b:
                    for rw in self.freq_row:
                        if a in self.freq_row[rw] and b in self.freq_row[rw]:
                            # TODO: Remove set(a) from row
                            pass
                    for ar in self.freq_area:
                        if a in self.freq_area[ar] and b in self.freq_area[ar]:
                            # TODO: Remove set(a) from area
                            pass
        self.changes += 0