# !/usr/bin/env python
# -*- coding: UTF-8 -*-

import logging
import queue
import threading

# 异步任务队列
_task_queue = queue.Queue()


def async_call(function, callback, *args, **kwargs):
    _task_queue.put({
        'function': function,
        'callback': callback,
        'args': args,
        'kwargs': kwargs
    })


def _task_queue_consumer():
    """
    异步任务队列消费者
    """
    while True:
        try:
            task = _task_queue.get()
            function = task.get('function')
            callback = task.get('callback')
            args = task.get('args')
            kwargs = task.get('kwargs')
            try:
                if callback:
                    callback(function(*args, **kwargs))
            except Exception as ex:
                if callback:
                    callback(ex)
            finally:
                _task_queue.task_done()
        except Exception as ex:
            logging.warning(ex)


# 自定义执行函数
def func_a(a, b):
    return a + b


def func_b():
    pass


def func_c(a, b, c):
    return a, b, c


# 结果处理
def handle_result(result):
    print(type(result), result)


def startQueueTask():
    """
    开启任务队列
    阻塞当前线程
    :return:
    """
    t = threading.Thread(target=_task_queue_consumer)
    t.daemon = True
    t.start()
    _task_queue.join()


if __name__ == '__main__':
    # 使用方式：
    # 添加任务入队列
    async_call(func_a, handle_result, 1, 2)
    async_call(func_b, handle_result)
    async_call(func_c, handle_result, 1, 2, 3)
    async_call(func_c, handle_result, 1, 2, 3, 4)
    startQueueTask()
