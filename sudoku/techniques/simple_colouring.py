__author__ = 'bushman'


import collections
from sudoku import Sudoku
from sudoku.tools import Colors


def run(sudoku, verbose=0):
    changes = 0
    if verbose:
        Colors.blue("[*] Technique: SimpleColouring".format(changes))
        # sudoku.print()
    all_doubles = _get_doubles(sudoku, verbose)
    for poss, doubles in all_doubles.items():
        changes += _colouring(sudoku, poss, doubles, verbose)
    return changes


def _get_doubles(s, verbose=0):
    all_freq = collections.defaultdict(list)
    for _, region in s.regions.items():
        freq = collections.defaultdict(list)
        for loc in region:
            for poss in s.fields[loc]:
                freq[poss].append(loc)
        for poss, locs in freq.items():
            if len(locs) == 2:
                all_freq[poss].append(locs)
    return all_freq


def _colouring(s, poss, doubles, verbose=0):
    changes = 0
    group_a = []
    group_b = []
    for [d1, d2] in doubles:
        if d1 in group_a:
            group_b.append(d1)
            group_a.append(d2)
        elif d1 in group_b:
            group_a.append(d1)
            group_b.append(d2)
    # for loc in set(group_a) & set(group_b):
    #     if poss in s.fields[loc]:
    #         changes += 1
    #         s.fields[loc].remove(poss)
    # if changes:
    #     return changes
    for group in (group_a, group_b):
        rows = []
        cols = []
        for loc in group:
            r, c = Sudoku.i2rc(loc)
            if r in rows or c in cols:
                changes += _eliminate_group(s, poss, group, verbose)
                break
            rows.append(r)
            cols.append(c)
    return changes


def _eliminate_group(s, poss, group, verbose=0):
    changes = 0
    for loc in group:
        if poss in s.fields[loc]:
            if len(s.fields[loc]) == 1:
                print(loc)
                print(s.fields[loc])
                s.print()
                raise ArithmeticError
            changes += 1
            s.fields[loc].remove(poss)
    return changes
