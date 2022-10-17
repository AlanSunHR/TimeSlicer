from random import randint
from time_slicer import TimeSlicer
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
            time.sleep(0.001)
        time_end = round(time.time()*1000, 1)
        print("Time elasped (ms): ", time_end - time_start)

if __name__ == "__main__":
    time_start = time.time()
    task = Task("A Message", time_start)
    ts = TimeSlicer()
    ts.setTimeInterval(30)
    ts.setTargetFunc(task.task)

    ts.start()

    time.sleep(3)
    ts.stop()