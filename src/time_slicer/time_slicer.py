from pyclbr import Function
from threading import Timer, Thread
import time
from types import MethodType
from typing import Any

class TimeSlicer(object):
    def __init__(self, time_interval_ms=30, target_func=None, args=(), kwargs=None, wait_target=True):
        self._time_interval_ms = time_interval_ms
        self._target_func = target_func
        self._args = args
        self._kwargs = kwargs

        self.__running_thread = None
        self.__running = True
        self.__timer = None
        self.__target_func_thread = None

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
        self._kwargs = kwargs

    def __timerTask(self):
        self.__target_func_thread = Thread(target=self._target_func, 
                              args=self._args,
                              kwargs=self._kwargs)
        self.__target_func_thread.start()
        self.__runTimer()
        
    def __runTimer(self):
        if self.__running:
            self.__timer = Timer(self._time_interval_seconds, 
                                self.__timerTask)
            self.__timer.start()
        
    def start(self):
        '''
            Start executing target function repeatly
        '''
        assert self._target_func is not None, \
            "No target function is specified. "
        self.__running_thread = Thread(target=self.__runTimer)
        self.__running_thread.start()
    
    def stop(self):
        '''
            Stop executing the target function
        '''
        self.__running = False
        
# class TargetOverdueError(Exception):
#     def __init__(self, expected_interval, actual_exec_seconds):
#         error_msg = "Target function execution time ({} ms) exceeding the expected interval {} ms. ".format(actual_exec_seconds*1000.0, expected_interval)
#         super().__init__(error_msg)