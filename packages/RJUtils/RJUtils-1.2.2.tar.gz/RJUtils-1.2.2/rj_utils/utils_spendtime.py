import sys
import time
import timeit

"""
兼容不同系统计算时间精度
"""

if sys.platform == "win32":
    # On Windows, the best timer is time.clock()
    default_timer = time.clock
else:
    # On most other platforms the best timer is time.time()
    default_timer = time.time

start_time = 0


def start_spend():
    global start_time
    start_time = 0
    start_time = timeit.default_timer()


def stop_spend():
    global start_time
    elapsed = (timeit.default_timer() - start_time)
    print("Time used:", elapsed)
