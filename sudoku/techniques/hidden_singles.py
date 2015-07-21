__author__ = 'bushman'


from sudoku.tools import Colors
import collections


REMOVE = " - HiddenSingle {}:{} -> {}"


def run(sudoku, verbose=0):
    changes = 0
    if verbose >= 2:
        Colors.blue("[*] Technique: Hidden Singles".format(changes))
        # sudoku.print()
    for _, region in sudoku.regions.items():
        changes += _hidden_singles_test(sudoku, region, verbose)
        if changes:
            if verbose >= 2:
                Colors.green("[+] Hidden Singles > Changes: {}".format(changes))
                # sudoku.print()
            return changes
    if verbose >= 2:
        Colors.red("[-] Hidden Singles > No change".format(changes))
        # sudoku.print()
    return changes


def _hidden_singles_test(s, region, verbose=0):
    changes = 0
    freq = collections.defaultdict(list)
    for loc in region:
        for poss in s.fields[loc]:
            freq[poss].append(loc)
    for poss, locs in freq.items():
        if len(locs) > 1:
            continue
        for loc in region:
            if loc in locs:
                continue
            old_possibles = s.fields[loc]
            new_possibles = old_possibles - {poss}
            change = len(old_possibles - new_possibles)
            if change:
                changes += change
                if verbose >= 3:
                    Colors.yellow(REMOVE.format(loc, s.fields[loc], poss))
                s.fields[loc] = new_possibles
    return changes


def _hidden_singles(s, region, verbose=0):
    changes = 0
    freq = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    locations = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for loc in region:
        for poss in s.fields[loc]:
            freq[poss] += 1
            locations[poss] = loc
    for poss in range(1, 10):
        if freq[poss] == 1:
            loc = locations[poss]
            changes += len(s.fields[loc]) - 1
            if verbose >= 3:
                Colors.yellow(REMOVE.format(loc, s.fields[loc], poss))
            s.fields[loc] = {poss}
    return changes
