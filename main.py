__author__ = 'bushman'


from sudoku import Colors
from sudoku import Manager
from time import time
from sudoku import tools


VERBOSE = 3
CHUNKSIZE = 42
PUZZLE_FILES = [
    # 'puzzles\\test_nakedsingles.txt',
    # 'puzzles\\combined.txt',
    # 'puzzles\\all.txt',
    # 'puzzles\\shortlist.csv',
    # 'puzzles\\single.csv',
    # 'puzzles\\test.csv',
    # 'puzzles\\top91.txt',
    # 'puzzles\\top95.txt',
    # 'puzzles\\top99.txt',
    # 'puzzles\\top100.txt',
    # 'puzzles\\top870.txt',
    # 'puzzles\\top2365.txt',
    # 'puzzles\\subig20.txt',
    # 'puzzles\\msk_009.txt',
    'puzzles\\learning-curve.txt',
]


def main():
    start = time()
    manager = Manager()
    total_changes = 0
    total_count = 0
    total_solved = 0
    messages = []
    for puzzles in PUZZLE_FILES:
        manager.load_puzzles(puzzles)
        changes, solved, count, message = manager.solve_current_puzzle_file(verbose=VERBOSE, chucksize=CHUNKSIZE)
        total_changes += changes
        total_solved += solved
        total_count += count
        messages.append(message)
    end = time()
    total_time = end - start
    for message in messages:
        print(message)
    Colors.green("[*] Totals:")
    print(" Total Changes: {}".format(total_changes))
    print(" Solved: {} of {} ({:.1f}%)".format(total_solved, total_count, (total_solved / total_count) * 100))
    print(" Time: {:.2f}s".format(total_time))
    print(" Speed: {:.2f}/s".format(total_count / total_time))


def test():
    puzzle_files = [
        'puzzles\\all.csv',
        'puzzles\\all.txt',
        'puzzles\\msk_009.txt',
        'puzzles\\shortlist.csv',
        'puzzles\\single.csv',
        'puzzles\\subig20.txt',
        'puzzles\\test.csv',
        'puzzles\\top91.txt',
        'puzzles\\top95.txt',
        'puzzles\\top99.txt',
        'puzzles\\top100.txt',
        'puzzles\\top870.txt',
        'puzzles\\top2365.txt',
    ]
    target = "puzzles\\combined.txt"
    tools.combine_files(puzzle_files, target)


if __name__ == "__main__":
    main()
