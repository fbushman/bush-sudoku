__author__ = 'bushman'


from sudoku.tools import Colors
from sudoku import Sudoku


REMOVE = " - NakedSingle {} removes {} from {}:{}"


def run(s, verbose=0):
    changes = 0
    if verbose >= 2:
        Colors.blue("[*] Technique: NakedSingles".format(changes))
    if verbose >= 4:
        s.print()
    for loc, poss in s.fields.items():
        if len(poss) == 1:
            changes += _eliminate_from_regions(s, loc, poss, verbose)
    if changes:
        if verbose >= 2:
            Colors.green("[+] NakedSingles > Changes: {}".format(changes))
        if verbose >= 4:
            s.print()
        return changes
    if verbose >= 2:
        Colors.red("[-] NakedSingles > No change".format(changes))
    if verbose >= 4:
        s.print()
    return changes


def _eliminate_from_regions(s, source_loc, poss, verbose=0):
    """
    :type s: Sudoku
    :type source_loc: int
    :type poss: set
    :type verbose: int
    :return:
    """
    changes = 0
    target_locs = s.matching_regions_single(s, source_loc)
    for loc in target_locs:
        if poss.issubset(s.fields[loc]):
            changes += 1
            if verbose >= 3:
                Colors.yellow(REMOVE.format(source_loc, poss, loc, s.fields[loc]))
            s.fields[loc] = s.fields[loc] - poss
    return changes


# def run(s, verbose=0):
#     changes = 0
#     if verbose >= 2:
#         Colors.blue("[*] Technique: NakedSingles".format(changes))
#     if verbose >= 4:
#         s.print()
#     for loc in range(1, 82):
#         changes += _naked_singles(s, loc, verbose)
#     if changes:
#         if verbose >= 2:
#             Colors.yellow("[+] NakedSingles > Changes: {}".format(changes))
#         if verbose >= 4:
#             s.print()
#         return changes
#     if verbose >= 2:
#         Colors.red("[-] NakedSingles > No change".format(changes))
#     if verbose >= 4:
#         s.print()
#     return changes
#
#
# def _naked_singles(s, loc, verbose=0):
#     changes = 0
#     if len(s.fields[loc]) > 1:
#         return changes
#     value = s.fields[loc]
#     r, c = s.i2rc(loc)
#     a = s.i2a(loc)
#
#     target_locs = s.areas[a] | s.rows[r] | s.cols[c]
#     target_locs = target_locs - {loc}
#
#     for target_loc in target_locs:
#         changes += _eliminate_from_loc(s, value, loc, target_loc, verbose)
#     return changes
#
#
# def _eliminate_from_loc(s, value, by_loc, target_loc, verbose=0):
#     changes = 0
#     possibles = s.fields[target_loc]
#     if len(value & possibles):
#         changes = 1
#         s.fields[target_loc] = possibles - value
#         if verbose >= 3:
#             Colors.yellow(REMOVE.format(by_loc, value, target_loc, possibles))
#         if len(possibles) <= 1:
#             s.print()
#             raise ArithmeticError
#     return changes
