# !/usr/bin/env python
# -*- coding: UTF-8 -*-

import logging
import queue
import threading
from datetime import datetime

from rj_utils.utils_dingding_push import DingdingManager

"""
消息发送队列
如果子线程中使用，使用queue.Queue

用于限制消息发送频率
multiprocessing.Queue 用在多进程里
queue.Queue 用在多线程中，作为多线程中target的参数
"""


class DingDingMsg:
    isRunning = False

    def __init__(self, dingding_token: str):
        self.actionFilter = {}
        # 异步任务队列
        self._task_queue = queue.Queue()
        self.dm = DingdingManager(dingding_token)

    def registMsgFilter(self, msgType: str, second: int, lastActionTime='1990-01-01 00:00:00'):
        """
        添加消息过滤器
        :param msgType: 消息类型
        :param second: 秒，n秒之内只触发一次动作
        :param lastActionTime: 上次触发时间
        """
        self.actionFilter[msgType] = {
            'second': second,
            'lastActionTime': lastActionTime
        }

    def addMsg(self, msgType: str, msg: str):
        """
        发送消息
        """
        self._task_queue.put({
            'msgType': msgType,
            'msg': msg
        })

    def _compare_time(self, time1, time2, format_time='%Y-%m-%d %H:%M:%S', dis_type='d'):
        """
        比较日期字符串间隔的天数，毫秒，秒
        :param time1: '2015-03-05 17:41:20'
        :param time2: '2015-03-02 17:41:20'
        :param dis_type:d 天，s 秒，ms 毫秒
        :return:返回日期间隔 d 天，s 秒，ms 毫秒
        """
        d1 = datetime.strptime(time1, format_time)
        d2 = datetime.strptime(time2, format_time)
        delta = d1 - d2
        if dis_type == 's':
            return delta.seconds
        elif dis_type == 'd':
            return delta.days
        elif dis_type == 'ms':
            return delta.microseconds
        else:
            return delta.days

    def _task_queue_consumer(self):
        """
        异步任务队列消费者
        """
        while self._task_queue:
            try:
                task = self._task_queue.get()
                if not task:
                    print("空数据，退出线程")
                    break
                msgType = task.get('msgType')
                msg = task.get('msg')
                filter = self.actionFilter.get(msgType)
                if filter is None:
                    self.dm.sendText(f'{msgType}:{msg}')
                else:
                    second = filter['second']
                    lastActionTime = filter['lastActionTime']
                    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    dis = self._compare_time(now, lastActionTime, dis_type='s')
                    if dis > second:
                        self.actionFilter[msgType]['lastActionTime'] = now
                        print(f'发出通知 {msgType} {now} : {msg}')
                        self.dm.sendText(f'{msgType}:{msg}')
                    else:
                        print(f'发送太频繁 {msgType} {now} : {msg}')
                self._task_queue.task_done()
            except Exception as ex:
                logging.warning(ex)

    def startQueueTask(self):
        """
        开启任务队列
        阻塞当前线程
        :return:
        """
        self._queueThread = threading.Thread(target=self._task_queue_consumer)
        self._queueThread.daemon = True

        self.isRunning = True
        self._queueThread.start()

    def join(self):
        self._queueThread.join()

    def stop(self):
        self._task_queue.put({})


if __name__ == '__main__':
    # 使用方式：
    dd = DingDingMsg(dingding_token='2x2s1s')
    dd.registMsgFilter('zhuli', 5)
    dd.registMsgFilter('dapan', 10)
    dd.startQueueTask()

    index = 0
    while True:
        index += 1
        dd.addMsg('zhuli', str(index))
        dd.addMsg('dapan', str(index))

        if index > 3:
            dd.stop()
            break
    dd.join()
    print('end')
