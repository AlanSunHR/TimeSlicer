from logging import root
import sys, os
root_dir = os.path.dirname(os.path.dirname(__file__))
pkg_dir = os.path.join(root_dir, "src/time_slicer")
sys.path.append(pkg_dir)

from random import randint
from time_slicer import TimeSlicer
import time

class Task(object):
    def __init__(self, msg, time_start) -> None:
        self.msg = msg
        self.time_start = time_start

    def task(self):
        print("***")
        for i in range(randint(1,10)):
            time_elasped = round((time.time()-self.time_start)*1000.0)
            print("[{}] ".format(time_elasped) + self.msg)
            time.sleep(0.03)

if __name__ == "__main__":
    time_start = time.time()
    task = Task("A Message", time_start)
    ts = TimeSlicer()
    ts.setTimeInterval(30)
    ts.setTargetFunc(task.task)

    ts.start()
    time.sleep(3)
    ts.stop()