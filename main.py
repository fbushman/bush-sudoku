#!/usr/bin/env python


__author__ = 'bushman'

from queue import Queue
import threading
import time

from v1.solver import Solver
from v1.tools import Colors
from v1 import tools
from v1.tools import prnt

thread_count = 2
nameList = [i for i in range(1, 10)]
countLock = threading.Lock()
printLock = threading.Lock()

workers = []
total_i = 0
solved_i = 0
time_start = 0
archive_loader = tools.archive_loader("puzzles\puzzles.csv")
loadLock = threading.Lock()
archive_eof = False


def load():
    global archive_loader, archive_eof
    try:
        string, level = next(archive_loader)
        return string, level
    except StopIteration or TypeError:
        archive_eof = True
        return False, False


def load_locked():
    global archive_loader, archive_eof
    try:
        loadLock.acquire()
        string, level = next(archive_loader)
        loadLock.release()
        return string, level
    except StopIteration or TypeError:
        archive_eof = True
        return False, False


def count(success):
    global countLock, solved_i, total_i, print_i
    countLock.acquire()
    if success:
        solved_i += 1
    total_i += 1
    # if total_i in tools.fibonacci:
    #     timer = time.clock() - time_start
    if total_i % 50 == 0:
        print(Colors.blue("[+] Solved {:5} of {:5}"
              .format(solved_i, total_i)), end="\r")
    countLock.release()


# TODO: Clone Solver class and turn it threaded.
class Worker(threading.Thread):
    def __init__(self, thread_id, queue):
        threading.Thread.__init__(self)
        self.id = thread_id
        self.queue = queue
        self.keep_going = True
        self.solved = 0
        self.total = 0
        self.sudoku = None

    def run(self):
        print("[T{}][+] Started.".format(self.id))
        solver = Solver()
        while True and self.keep_going:
            string, level = load()
            if not string:
                print("[T{}]    No more jobs.".format(self.id))
                break
            # print("[T{}][+] Processing...".format(self.id), end="\r")
            solver.load_string(string)
            result = solver.run(verbose=0, msg="T{}".format(self.id))
            if result:
                self.solved += 1
                # print(Colors.green("[T{}][+] Done: {}".format(self.id, string)))
            else:
                # print(Colors.red("[T{}][-] Done: {}".format(self.id, string)))
                pass
            self.total += 1

            # if self.total in tools.fibonacci:
            #     timer = time.clock() - time_start
            #     print(Colors.blue("[{}] Solved {:5} of {:5}  Queue: ~{:4}  Time: {:7.2f}s"
            #           .format(self.id, self.solved, self.total, self.queue.qsize(), timer)))

            count(result)
            # self.queue.task_done()
        print("[T{}][+] Ended... Solved {}/{} total.".format(self.id, self.solved, self.total))


def run_threaded():
    global time_start, archive_eof
    print("[+] Starting main thread")
    time_start = time.clock()
    workqueue = Queue(1500)

    # Create workers
    worker_id = 1
    for i in range(1, thread_count + 1):
        worker = Worker(worker_id, workqueue)
        worker.setDaemon(True)
        worker.keep_going = True
        workers.append(worker)
        worker_id += 1
    # Start the threads
    time.sleep(0.1)
    for worker in workers:
        worker.start()
    # Fill the queue
    # sudoku_archive = tools.archive_loader("puzzles\all.csv")
    # while True:
    #     sudoku_line = next(sudoku_archive)
    #     if not sudoku_line:
    #         break
    #     workqueue.put(sudoku_line[0], block=True)
    # # Wait for queue to empty
    # workqueue.join()
    while not archive_eof:
        pass
    # Wait for all threads to complete
    for t in workers:
        t.keep_going = False
    for t in workers:
        t.join()
    time_end = time.clock()
    timer = round(time_end - time_start, 1)
    # print(Colors.OKBLUE + "[+] All archived Sudoku checked." + Colors.ENDC)
    print(Colors.blue("[+] Done! Solved {:5} of {:5}  Q ~{:4}  Time: {:7.2f}s"
          .format(solved_i, total_i, workqueue.qsize(), timer)))


def run():
    def solve(archive, total, solved):
        solver = Solver()
        try:
            for string_line in archive:
                solver.load_string(string_line[0])
                result = solver.run(verbose=verbose)
                if result:
                    solved += 1
                    if verbose >= 2:
                        prnt("Done: {}".format(string_line[0]), level=1)
                else:
                    if verbose >= 2:
                        prnt("Done: {}".format(string_line[0]), level=4)
                    pass
                total += 1
                if verbose >= 1:
                    if verbose >= 2:
                        if total in [1000, 2000, 3000, 5000, 8000, 13000]:
                            timer = time.clock() - timer_start
                            prnt("Solved {:5} of {:5}  Time: {:7.2f}s".format(solved, total, timer), level=2)
                print(prnt("Solved {:5} of {:5}".format(solved, total), level=2, ret=True), end="\r")
        except StopIteration:
            raise
        prnt("Ending...", level=3)
        return total, solved
    global total_i, solved_i
    verbose = 0
    total_i = 0
    solved_i = 0
    prnt("Starting...", level=3)
    # path = "C:\\Users\\bushman\\PycharmProjects\\SudokuGrabber\\sudoku.csv"
    path = "C:\\Users\\bushman\\PycharmProjects\\SudokuGrabber\\output2.csv"
    # path = "puzzles\\shorter.csv"
    # path = "puzzles\\short.csv"
    # path = "puzzles\\long.csv"
    # path = "puzzles\\all.csv"
    sudoku_archive = tools.total_archive_loader(path)
    timer_start = time.clock()
    total_i, solved_i = solve(sudoku_archive, total_i, solved_i)
    timer = round(time.clock() - timer_start, 1)
    prnt("Done! Solved {:5} of {:5}  Time: {:7.2f}s".format(solved_i, total_i, timer), level=1)
    prnt("Ending...", level=3)
    return total_i, solved_i, timer


def non_threaded():
    tools.print_field_numbers()
    number_of_runs = 1
    totals = []
    solves = []
    timers = []
    for i in range(1, number_of_runs+1):
        prnt("START RUN {}".format(i), level=3)
        stats = run()
        totals.append(stats[0])
        solves.append(stats[1])
        timers.append(stats[2])
        avg_total = sum(totals)
        avg_solve = sum(solves)
        avg_timer = sum(timers)
        prnt("TOTALS: Solved {:5} of {:5}  Time: {:7.0f}ms".format(avg_solve, avg_total, avg_timer*1000), level=3)
        prnt("END RUN {}".format(i), level=3)


def threaded():
    run_threaded()


if __name__ == "__main__":
    # pr = cProfile.Profile()
    # pr.enable()
    non_threaded()
    #
    # pr.disable()
    # s = io.StringIO()
    # sortby = 'cumulative'
    # ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    # ps.print_stats()
    # print(s.getvalue())


# TEST RESULTS
# made 1000 sudoku shorter.csv benchmark
# [x] TOTALS: Solved   623 of  1000  Time:   18.60s
# [x] TOTALS: Solved   623 of  1000  Time: 27.30000s
# added pointing pairs
# [x] TOTALS: Solved   690 of  1000  Time:   24100ms


# [x] TOTALS: Solved 10246 of 17445  Time:  444300ms
# [x] TOTALS: Solved 11606 of 17445  Time:  481700ms


# [x] TOTALS: Solved   660 of 49595  Time:  112900ms
# [x] TOTALS: Solved 13125 of 49595  Time:  655400ms
