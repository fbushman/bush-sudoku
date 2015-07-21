__author__ = 'bushman'


from sudoku import Sudoku
from sudoku.tools import Colors
import sudoku.techniques as technique
import csv
from time import time


class Manager:
    def __init__(self):
        self.loader = Manager._dummy_loader()
        self.current_puzzles = "No puzzles loaded!"
        self.puzzles = []
        self.current_sudoku = Sudoku()
        self.update = "[{:d}] Changes: {:<,} ^ Solved:{:5.1f}% ^ Time: {:.1f}s ^ Speed: {:.2f}/s"
        self.status = "\033[94m[*] Stats for '{}':\033[0m\n" \
                      " Total Changes: {}\n" \
                      " Solved: {} of {} ({:.1f}%)\n" \
                      " Time: {:.2f}s\n" \
                      " Speed: {:.2f}/s"

    @staticmethod
    def _dummy_loader():
        print("[*] Error: No puzzle file loaded!")
        yield StopIteration

    @staticmethod
    def _puzzle_loader(path):
        with open(path) as reader:
            sudoku_reader = csv.reader(reader, delimiter=",", quotechar="\"")
            try:
                while True:
                    puzzle_string = next(sudoku_reader)[0]
                    yield puzzle_string
            except IOError:
                print("Error while loading from: '{}'".format(path))
                raise

    def load_puzzles(self, path):
        self.loader = Manager._puzzle_loader(path)

    def next_sudoku(self):
        """
        :rtype: Sudoku
        """
        sudoku_string = next(self.loader)
        # print("[*] Loaded next puzzle.")
        self.current_sudoku = Sudoku(sudoku_string)
        return self.current_sudoku

    def solve_current_puzzle_file(self, verbose=0, chucksize=42):
        changes = 0
        count = 0
        solved = 0
        start = time()
        middle_time = time()
        try:
            Colors.yellow(self.update.format(0, 0, 0, 0, 0), end="\r")
            while True:
                su = self.next_sudoku()
                count += 1
                if verbose >= 2:
                    Colors.blue("[*] Puzzle #{}".format(count))
                if verbose >= 4:
                    su.print()
                changes += self.solve_current_sudoku(verbose)
                if verbose >= 4:
                    su.print()
                if self.check_sudoku(su, verbose):
                    solved += 1
                if verbose == 1 and count % chucksize == 0:
                    total_duration = time() - start
                    duration = time() - middle_time
                    middle_time = time()
                    Colors.yellow(self.update.format(count,
                                                     changes,
                                                     (solved / count) * 100,
                                                     total_duration,
                                                     chucksize / duration),
                                  end="\r")
                # input("Press Enter to continue...")
        except StopIteration:
            if verbose >= 2:
                Colors.blue("[*] End of puzzle file.")
            pass
        end = time()
        total_time = end - start
        status_message = self.status.format(self.current_puzzles,
                                            changes,
                                            solved,
                                            count,
                                            (solved / count) * 100,
                                            total_time,
                                            count / total_time)
        if verbose >= 2:
            print(status_message)
        return changes, solved, count, status_message

    @staticmethod
    def repeat_technique(sudoku, tech, verbose=0):
        changes = 0
        while True:
            tech_changes = tech(sudoku, verbose)
            if tech_changes:
                changes += tech_changes
            else:
                return changes
        return changes

    def solve_sudoku(self, sudoku, verbose=0):
        """
        :type sudoku: Sudoku
        """
        total_changes = 0
        changes = 0
        while True:
            total_changes += changes
            changes = 0
            if self.check_sudoku(sudoku):
                if verbose >= 2:
                    Colors.green("[+] Solved: {}".format(sudoku.line))
                break
            sudoku.print()
            changes += technique.naked_singles(sudoku, verbose)
            if changes:
                continue
            sudoku.print()
            changes += technique.hidden_singles(sudoku, verbose)
            if changes:
                continue
            sudoku.print()
            changes += technique.hidden_pairs(sudoku, verbose)
            if changes:
                continue
            sudoku.print()
            changes += technique.pointing_pairs(sudoku, verbose)
            if changes:
                continue
            # changes += technique.fish(sudoku, verbose)
            # if changes:
            #     continue
            # changes += technique.simple_colouring(sudoku, verbose)
            if verbose >= 2:
                Colors.red("[-] Not solved: {}".format(sudoku.line))
            if verbose >= 4:
                sudoku.print()
            break
        # if total_changes:
        #     print("Aaahh!")
        return total_changes

    @staticmethod
    def check_sudoku(sudoku, verbose=0):
        """
        :type sudoku: Sudoku
        """
        # verbose = True
        solved_fields = len([None for _, poss in sudoku.fields.items() if len(poss) == 1])
        if solved_fields == 81:
            if verbose >= 2:
                Colors.green("[+] Sudoku solved!".format())
            return True
        if verbose >= 2:
            Colors.red("[-] Solved fields: {}".format(solved_fields))
        return False

    def solve_current_sudoku(self, verbose=0):
        return self.solve_sudoku(self.current_sudoku, verbose)

    def check_current_sudoku(self, verbose=0):
        return self.check_sudoku(self.current_sudoku, verbose)
