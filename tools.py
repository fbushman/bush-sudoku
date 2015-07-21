__author__ = 'bushman'


import random
import csv
import threading


fibonacci = [1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597,
             2584, 4181, 6765, 10946, 17711, 28657, 46368, 75025, 121393, 196418, 317811, 514229,
             832040, 1346269, 2178309, 3524578, 5702887, 9227465, 14930352, 24157817, 39088169,
             63245986, 102334155, 165580141, 267914296, 433494437, 701408733, 1134903170, 1836311903]
print_lock = threading.Lock()
loader_lock = threading.Lock()


class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    @staticmethod
    def green(msg):
        return "{}{}{}".format(Colors.OKGREEN, msg, Colors.ENDC)

    @staticmethod
    def blue(msg):
        return "{}{}{}".format(Colors.OKBLUE, msg, Colors.ENDC)

    @staticmethod
    def red(msg):
        return "{}{}{}".format(Colors.FAIL, msg, Colors.ENDC)

    @staticmethod
    def yellow(msg):
        return "{}{}{}".format(Colors.WARNING, msg, Colors.ENDC)


def random_value():
    choice = random.choice([1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    return {choice}


def print_field_numbers():
    prnt("[+] Field Numbers")
    longline = "{}. {}. {}. | {}. {}. {}. | {}. {}. {}."
    i = 0
    for row in range(9):
        numbers = []
        for col in range(9):
            i += 1
            numbers.append(str(i).zfill(2))
        prnt(longline.format(*numbers))
        if row in {2, 5}:
            prnt("------------|-------------|------------")
        elif row == 8:
            break
        else:
            prnt("            |             |            ")


def rc2a(row, col):
    a = ((row + 2) // 3 - 1) * 3 + ((col + 2) // 3)
    return a


def rc2i(row, col):
    i = (9 * row) - 9 + col
    return i


def i2rc(i):
    r = (i - 1) // 9 + 1
    c = (i - 1) % 9 + 1
    return r, c


def grab(_set):
    return (_set & _set).pop()


def archive_loader(path):
    global loader_lock
    with open(path) as reader:
        sudoku_reader = csv.reader(reader, delimiter=",", quotechar="\"")
        try:
            while True:
                try:
                    loader_lock.acquire()
                    sudoku_line = next(sudoku_reader)
                    loader_lock.release()
                    sudoku = sudoku_line[0]
                    level = sudoku_line[1]
                    yield sudoku, level
                except StopIteration:
                    yield False
        except Exception:
            prnt("Error while loading from archives.")
            raise


def total_archive_loader(path):
    archive = []
    with open(path) as reader:
        sudoku_reader = csv.reader(reader, delimiter=",", quotechar="\"")
        try:
            while True:
                try:
                    sudoku_line = next(sudoku_reader)
                    sudoku = sudoku_line[0]
                    level = sudoku_line[1]
                    archive.append((sudoku, level))
                except StopIteration:
                    break
        except Exception:
            prnt("Error while loading from archives.")
            raise
    return archive


def prnt(message, level=0, tag="", ret=False, end=None):
    if not end:
        end = "\r\n"
    global print_lock
    if level == 0:
        line = "{}    {}".format(tag, message)
    elif level == 1:
        line = Colors.green("{}[+] {}".format(tag, message))
    elif level == 2:
        line = Colors.blue("{}[^] {}".format(tag, message))
    elif level == 3:
        line = Colors.yellow("{}[x] {}".format(tag, message))
    elif level == 4:
        line = Colors.red("{}[-] {}".format(tag, message))
    elif level == 5:
        line = "{}{}".format(tag, message)
    else:
        line = Colors.red("{}[-] prnt: Bad level parameter!")
    line = tag + line
    if ret:
        return line
    # print_lock.acquire()
    if end:
        print(line, end=end)
    else:
        print(line)
    # print_lock.release()