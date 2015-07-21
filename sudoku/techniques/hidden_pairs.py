__author__ = 'bushman'


import itertools
import collections
from sudoku import Sudoku
from sudoku.tools import Colors
import pprint


PAIR_FOUND = "[+] HiddenPairs > Pair {} at {}:"
REMOVE = " - HiddenPair {} removes {} from {}:{}."


def run(sudoku, verbose=0):
    changes = 0
    if verbose >= 2:
        Colors.blue("[*] Technique: HiddenPairs".format(changes))
        # s.print()
    for tag, row in sudoku.rows.items():
        changes = _find_hidden_pairs(sudoku, row, verbose=verbose)
    for tag, col in sudoku.cols.items():
        changes = _find_hidden_pairs(sudoku, col, verbose=verbose)
    for tag, area in sudoku.areas.items():
        changes = _find_hidden_pairs(sudoku, area, verbose=verbose)
    if changes:
        if verbose >= 2:
            Colors.green("[+] HiddenPairs > Changes: {}".format(changes))
        if verbose >= 4:
            sudoku.print()
    return changes


def _find_hidden_pairs(s, region, verbose=0):
    changes = 0
    freq = collections.defaultdict(set)
    already_set = 0
    for loc in region:
        length = len(s.fields[loc])
        if length == 1:
            already_set += 1
            continue
        for poss in s.fields[loc]:
            freq[poss].add(loc)
    pairs = []
    taken_poss = set()
    max_length = 9 - already_set
    for length in reversed(range(2, max_length + 1)):
        try:
            for candidates in itertools.combinations(freq, length):
                all_locs = set()
                all_poss = set()
                for p in candidates:
                    all_locs = all_locs | freq[p]
                    all_poss = all_poss | {p}
                if len(all_locs) == max_length:
                    raise StopIteration
                for (poss, locs) in pairs:
                    if all_poss.issubset(poss):
                        raise StopIteration
                if len(all_poss) == len(all_locs):
                    # Leaves a pair that is not a pair
                    # So...
                    # There are false hits, or freq should be redone for each iteration (meaning, return changes)
                    changes += _remove_pairs(s, all_poss, all_locs, verbose)
                    pairs.append((all_poss, all_locs))
                    taken_poss = taken_poss | all_poss
        except StopIteration:
            continue
    if len(pairs) == 0:
        return changes
    for poss, locs in pairs:
        for loc in region:
            old_possibles = s.fields[loc]
            if loc in locs:
                new_possibles = old_possibles & poss
                change = len(old_possibles - new_possibles)
                if change:
                    if verbose >= 3:
                        Colors.yellow(REMOVE.format(locs, old_possibles - poss, loc, old_possibles))
                    s.fields[loc] = new_possibles
                    changes += change
            else:
                new_possibles = old_possibles - poss
                change = len(old_possibles - new_possibles)
                if change:
                    if verbose >= 3:
                        Colors.yellow(REMOVE.format(locs, poss, loc, old_possibles))
                    s.fields[loc] = new_possibles
                    changes += change
            # change = len(old_possibles - new_possibles)
            # if change:
            #     if verbose >= 3:
            #         Colors.yellow(REMOVE.format(locs, poss, loc, old_possibles))
            #     s.fields[loc] = new_possibles
            #     changes += change
    # if changes:
    #     print("Boo!")
    return changes


def _remove_pairs(s, poss, locs, verbose):
    changes = 0

    return changes


# def _find_hidden_pairs(s, region, verbose=0):
#     changes = 0
#     freq = collections.defaultdict(set)
#     already_set = 0
#     for loc in region:
#         length = len(s.fields[loc])
#         if length == 1:
#             already_set += 1
#             continue
#         for poss in s.fields[loc]:
#             freq[poss].add(loc)
#     pairs = []
#     taken_poss = set()
#     max_length = 9 - already_set
#     for length in reversed(range(2, max_length + 1)):
#         try:
#             for candidates in itertools.combinations(freq, length):
#                 all_locs = set()
#                 all_poss = set()
#                 for p in candidates:
#                     all_locs = all_locs | freq[p]
#                     all_poss = all_poss | {p}
#                 if len(all_locs) == max_length:
#                     raise StopIteration
#                 for (poss, locs) in pairs:
#                     if all_poss.issubset(poss):
#                         raise StopIteration
#                 if len(all_poss) == len(all_locs):
#                     pairs.append((all_poss, all_locs))
#                     taken_poss = taken_poss | all_poss
#         except StopIteration:
#             continue
#     if len(pairs) == 0:
#         return changes
#     for poss, locs in pairs:
#         for loc in region:
#             old_possibles = s.fields[loc]
#             if loc in locs:
#                 new_possibles = old_possibles & poss
#             else:
#                 new_possibles = old_possibles - poss
#             change = len(old_possibles - new_possibles)
#             if change:
#                 if verbose >= 3:
#                     Colors.yellow(REMOVE.format(locs, poss, loc, old_possibles))
#                 s.fields[loc] = new_possibles
#                 changes += change
#     # if changes:
#     #     print("Boo!")
#     return changes
#






















