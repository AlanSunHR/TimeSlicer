from pyclbr import Function
from threading import Timer, Thread
import time
from types import MethodType
from typing import Any
from copy import deepcopy

class TimeSlicer(object):
    def __init__(self, time_interval_ms=30, target_func=None, args=(), kwargs=None, wait_target=True):
        self._time_interval_ms = time_interval_ms
        self._target_func = None
        self._args = None
        self._kwargs = None
        self.setTargetFunc(target_func, args, kwargs)

        self.__current_time = 0.0
        self.__last_exec_time = 0.0
        self.__running = True
        self.__timer_thread = None
        self.__target_func_thread = None
        self.__timer_sleep_time = 0.0001

    @property
    def _time_interval_seconds(self):
        return self._time_interval_ms/1000.0

    def setTimeInterval(self, milliseconds):
        '''
            Set time interval in milliseconds.

            @params:
            milliseconds: interval in ms; must be an integer (semi-millisecond 
            accuracy should not be expected)
        '''
        assert isinstance(milliseconds, int), \
            "The argument should be of type int. "
        self._time_interval_ms = milliseconds

    def setTargetFunc(self, target_func, args=(), kwargs=None):
        '''
            Set the target function to be called at a fixed frequency according
            to self.time_interval_ms. (freqency = 1000/self.time_interval_ms)

            @params
            target_func: the function to be repeatly called
            args: target_func arguments
            kwargs: target_func keyword arguments
        '''
        self._target_func = target_func
        self._args = args
        if kwargs is None:
            kwargs = {}
        self._kwargs = kwargs

    # def __timerTask(self):
    #     while self.__running:
    #         self.__current_time = round(time.time()*10e3, 1)
    #         time.sleep(self.__timer_sleep_time)

    def __updateTime(self):
        self.__current_time = round(time.time()*1000, 1)

    def __targetTask(self):
        while self.__running:
            if self.__current_time - self.__last_exec_time >= self._time_interval_ms:
                self.__updateTime()
                self.__last_exec_time = deepcopy(self.__current_time)
                self._target_func(*self._args, **self._kwargs) # Execute the target function
                self.__updateTime() # Update the current time
                time_elasped = self.__current_time - self.__last_exec_time
                # If the execution time took longer than expected, raise the error
                if time_elasped > self._time_interval_ms:
                    raise TargetOverdueError(self._time_interval_ms, time_elasped)
            else:
                self.__updateTime()
                time.sleep(self.__timer_sleep_time)

    def start(self):
        '''
            Start executing target function repeatly
        '''
        assert self._target_func is not None, \
            "No target function is specified. "
        # self.__current_time = round(time.time()*10e3, 1)
        # self.__timer_thread = Thread(target=self.__timerTask)
        # self.__timer_thread.start()
        self.__updateTime()
        self.__target_func_thread = Thread(target=self.__targetTask)
        self.__target_func_thread.start()
    
    def stop(self):
        '''
            Stop executing the target function
        '''
        self.__running = False
        
class TargetOverdueError(Exception):
    def __init__(self, expected_interval, actual_exec_ms):
        error_msg = "Target function execution time ({} ms) exceeding the expected interval {} ms. ".format(actual_exec_ms, expected_interval)
        super().__init__(error_msg)