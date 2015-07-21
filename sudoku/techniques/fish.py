__author__ = 'bushman'


from sudoku import Sudoku
import collections
import itertools
from sudoku.tools import Colors


def run(sudoku, verbose=0):
    """
    :type sudoku: Sudoku
    :type verbose: int
    :rtype: int
    """
    changes = 0
    if verbose >= 2:
        Colors.blue("[*] Technique: Fish".format(changes))
        # sudoku.print()
    sets = _find_sets(sudoku, sudoku.rows, verbose)
    for poss, parts in sets.items():
        changes += _process(sudoku, poss, parts["doubles"], parts["triples"], parts["quads"], verbose)
    sets = _find_sets(sudoku, sudoku.cols, verbose)
    for poss, parts in sets.items():
        changes += _process(sudoku, poss, parts["doubles"], parts["triples"], parts["quads"], verbose)
    if changes:
        if verbose >= 2:
            Colors.yellow("[+] Fish > Changes: {}".format(changes))
            # sudoku.print()
    else:
        if verbose >= 2:
            Colors.red("[-] Fish > No changes")
            # sudoku.print()
    return changes


def _find_sets(s, regions, verbose=0):
    """
    :type s: Sudoku
    :type regions: dict
    :type verbose: int
    :rtype: dict
    """
    sets = {poss: {"doubles": [], "triples": [], "quads": []} for poss in range(1, 10)}
    for _, locs in regions.items():
        freq = collections.defaultdict(list)
        for loc in locs:
            for poss in s.fields[loc]:
                freq[poss].append(loc)
        for poss, pair_locs in freq.items():
            if len(pair_locs) == 2:
                sets[poss]["doubles"].append(pair_locs)
            elif len(pair_locs) in (2, 3):
                sets[poss]["triples"].append(pair_locs)
            elif len(pair_locs) in (2, 3, 4):
                sets[poss]["quads"].append(pair_locs)
    return sets


def _process(s, poss, doubles, triples, quads, verbose=0):
    """
    :type s: Sudoku
    :type poss: int
    :type doubles: list
    :type triples: list
    :type quads: list
    :type verbose: int
    :rtype: int
    """
    changes = 0
    for dpair in itertools.combinations(doubles, 2):
        is_fish, rows, cols, locs = _is_fish(dpair, 2)
        if not is_fish:
            continue
        for dpart in dpair:
            try:
                triples.remove(dpart)
            except ValueError:
                pass
            try:
                quads.remove(dpart)
            except ValueError:
                pass
        # Colors.blue("Fish:{}  Rows:{}  Cols:{}  Locs:{}  Poss:{}".format(is_fish, rows, cols, locs, poss))
        changes += _eliminate(s, poss, rows, cols, locs)
    for tpair in itertools.combinations(triples, 3):
        is_fish, rows, cols, locs = _is_fish(tpair, 3)
        if not is_fish:
            continue
        # Colors.blue("Fish:{}  Rows:{}  Cols:{}  Locs:{}  Poss:{}".format(is_fish, rows, cols, locs, poss))
        for tpart in tpair:
            try:
                quads.remove(tpart)
            except ValueError:
                pass
        changes += _eliminate(s, poss, rows, cols, locs)
    for qpair in itertools.combinations(quads, 4):
        is_fish, rows, cols, locs = _is_fish(qpair, 4)
        if not is_fish:
            continue
        # Colors.blue("Fish:{}  Rows:{}  Cols:{}  Locs:{}  Poss:{}".format(is_fish, rows, cols, locs, poss))
        changes += _eliminate(s, poss, rows, cols, locs)
    return changes


def _is_fish(possible_fish, size):
    fish_rows = set()
    fish_cols = set()
    fish_locs = set()
    for locs in possible_fish:
        for loc in locs:
            r, c = Sudoku.i2rc(loc)
            fish_rows.add(r)
            if len(fish_rows) > size:
                return False, fish_rows, fish_cols, fish_locs
            fish_cols.add(c)
            if len(fish_cols) > size:
                return False, fish_rows, fish_cols, fish_locs
            fish_locs.add(loc)
    if len(fish_rows) != size or len(fish_cols) != size:
        return False, fish_rows, fish_cols, fish_locs
    return True, fish_rows, fish_cols, fish_locs


def _eliminate(s, poss, rows, cols, not_locs):
    changes = 0
    for row_nr in rows:
        for loc in (loc for loc in s.rows[row_nr] if loc not in not_locs):
            possibles = s.fields[loc]
            if poss not in possibles:
                continue
            s.fields[loc] = possibles - {poss}
            changes += 1
    for col_nr in cols:
        for loc in (loc for loc in s.cols[col_nr] if loc not in not_locs):
            possibles = s.fields[loc]
            if poss not in possibles:
                continue
            s.fields[loc] = possibles - {poss}
            changes += 1
    return changes






















