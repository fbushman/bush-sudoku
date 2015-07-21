__author__ = 'bushman'


from sudoku.tools import Colors
from sudoku import Sudoku
import collections


REMOVE = " - PointingPairs {} removes {} from {}."


def run(sudoku, verbose=0):
    """
    :type sudoku: Sudoku
    :type verbose: int
    """
    changes = 0
    if verbose:
        Colors.blue("[*] Technique: PointingPairs".format(changes))
        sudoku.print()
    for _, row in sudoku.rows.items():
        changes += _pointing_pairs_test(sudoku, row, verbose)
        if changes:
            if verbose:
                Colors.green("[+] PointingPairs (Row) > Changes: {}".format(changes))
                # sudoku.print()
            return changes
    for _, col in sudoku.cols.items():
        changes += _pointing_pairs_test(sudoku, col, verbose)
        if changes:
            if verbose:
                Colors.green("[+] PointingPairs (Col) > Changes: {}".format(changes))
                # sudoku.print()
            return changes
    if verbose:
        Colors.red("[+] PointingPairs > No changes".format(changes))
        # sudoku.print()
    return changes


def _pointing_pairs_test(s, region, verbose=0):
    """
    :type s: Sudoku
    :type region: set
    :type verbose: int
    """
    changes = 0
    freq = collections.defaultdict(set)
    taken_poss = set()
    for loc in region:
        for poss in s.fields[loc]:
            if len(s.fields[loc]) == 1:
                taken_poss = taken_poss | s.fields[loc]
                continue
            freq[poss].add(loc)
    for poss in taken_poss:
        try:
            freq.pop(poss)
        except KeyError:
            pass
    for poss, locs in freq.items():
        for _, area in s.areas.items():
            if not locs.issubset(area):
                continue
            for loc in region - locs:
                old_possibles = s.fields[loc]
                new_possibles = old_possibles - {poss}
                change = len(old_possibles - new_possibles)
                assert len(new_possibles) != 0
                if change:
                    changes += change
                    if verbose:
                        Colors.yellow(REMOVE.format(old_possibles, poss, loc))
                    s.fields[loc] = new_possibles
    return changes


def _pointing_pairs(s, locs, verbose=0):
    """
    :type s: Sudoku
    :type locs: set
    :type verbose: int
    """
    changes = 0
    freq = collections.defaultdict(list)
    for loc in locs:
        for poss in s.fields[loc]:
            freq[poss].append(loc)
    for poss, pair_locs in {p: set(ls) for p, ls in freq.items() if len(ls) in (2, 3)}.items():
        target_locs = s.matching_regions(s, pair_locs)
        for loc in target_locs:
            if poss in s.fields[loc]:
                changes += 1
                s.fields[loc].remove(poss)
                if verbose:
                    Colors.yellow(REMOVE.format(pair_locs, poss, loc))
                assert len(s.fields[loc]) > 0
    return changes
