__author__ = 'bushman'


from functools import wraps
from time import time


def time_me(f):
    @wraps(f)
    def wrap(*args, **kw):
        ts = time()
        result = f(*args, **kw)
        te = time()
        print("func:{} args:[{}, {}] took: {:2.4f} sec".format(f.__name__, args, kw, te - ts))
        return result
    return wrap


def combine_files(origins, target):
    lines = []
    for origin in origins:
        with open(origin) as orig:
            lines.extend(orig.readlines())
    len1 = len(lines)
    lines = sorted(set(lines))
    len2 = len(lines)
    print("[*] Before:{}  After:{}".format(len1, len2))
    cleaned_lines = []
    for line in lines:
        cleaned_lines.append(line.split(",")[0].replace("\"", "").rstrip())
    with open(target, mode="w") as t:
        for line in cleaned_lines:
            if line != "\n" and line != "":
                t.write(line + "\n")


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
    def green(msg, end="42"):
        if end != "42":
            print(Colors._green(msg), end=end)
        else:
            print(Colors._green(msg))

    @staticmethod
    def blue(msg, end="42"):
        if end != "42":
            print(Colors._blue(msg), end=end)
        else:
            print(Colors._blue(msg))

    @staticmethod
    def red(msg, end="42"):
        if end != "42":
            print(Colors._red(msg), end=end)
        else:
            print(Colors._red(msg))

    @staticmethod
    def yellow(msg, end="42"):
        if end != "42":
            print(Colors._yellow(msg), end=end)
        else:
            print(Colors._yellow(msg))

    @staticmethod
    def _green(msg):
        return "{}{}{}".format(Colors.OKGREEN, msg, Colors.ENDC)

    @staticmethod
    def _blue(msg):
        return "{}{}{}".format(Colors.OKBLUE, msg, Colors.ENDC)

    @staticmethod
    def _red(msg):
        return "{}{}{}".format(Colors.FAIL, msg, Colors.ENDC)

    @staticmethod
    def _yellow(msg):
        return "{}{}{}".format(Colors.WARNING, msg, Colors.ENDC)
