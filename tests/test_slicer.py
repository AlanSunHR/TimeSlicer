from logging import root
import sys, os
from timeit import repeat
root_dir = os.path.dirname(os.path.dirname(__file__))
pkg_dir = os.path.join(root_dir, "src/time_slicer")
sys.path.append(pkg_dir)

from random import randint
from time_slicer import TimeSlicer, TargetOverdueError
import time

class Task(object):
    def __init__(self, msg, time_start) -> None:
        self.msg = msg
        self.time_start = time_start

    def task(self):
        time_start = round(time.time()*1000, 1)
        print("***")
        repeated_times = randint(1,10)
        print("The task will be repeated {} times".format(repeated_times))
        for i in range(repeated_times):
            time_elasped = round((time.time()-self.time_start)*1000.0)
            print("[{}] ".format(time_elasped) + self.msg)
            time.sleep(0.03)
        time_end = round(time.time()*1000, 1)
        print("Time elasped (ms): ", time_end - time_start)

if __name__ == "__main__":
    time_start = time.time()
    task = Task("A Message", time_start)
    ts = TimeSlicer()
    ts.setTimeInterval(30)
    ts.setTargetFunc(task.task)

    try:
        ts.start()
    except TargetOverdueError as e:
        ts.start()
        print(e)

    time.sleep(3)
    ts.stop()