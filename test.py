__author__ = 'bushman'

# System modules
from queue import Queue
from threading import Thread
import time
import random

from v1.tools import prnt


# Set up some global variables
num_fetch_threads = 8
job_queue = Queue(1500)


def solve_sudoku_string(thread_id, queue):
    """
    This is the worker thread function.
    It processes items in the queue one after
    another.  These daemon threads go into an
    infinite loop, and only exit when
    the main thread ends.
    """
    while True:
        prnt("T{} is waiting...".format(thread_id))
        string, level = queue.get()
        prnt("T{} got a {} sudoku: {}".format(thread_id, level, string))
        time.sleep(10 * random.random())
        prnt("T{} solved a {} sudoku!!".format(thread_id, level))
        queue.task_done()


# Set up some threads to fetch the enclosures
for i in range(num_fetch_threads):
    worker = Thread(target=solve_sudoku_string, args=(i, job_queue,))
    worker.setDaemon(True)
    worker.start()

# Download the feed(s) and put the enclosure URLs into
# the queue.
from v1 import tools

generator = tools.archive_loader("short.csv")
if not generator:
    prnt("Empty file or failure...")
else:
    for sudoku_string in generator:
        prnt("Queu({}): '{}'".format(job_queue.qsize(), sudoku_string))
        job_queue.put(sudoku_string)

# Now wait for the queue to be empty, indicating that we have
# processed all of the downloads.
print("*** Main thread waiting")
job_queue.join()
print("*** Done")