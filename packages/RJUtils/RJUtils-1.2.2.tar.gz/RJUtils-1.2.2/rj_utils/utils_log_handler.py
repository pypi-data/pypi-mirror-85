import logging
import os
from logging.handlers import TimedRotatingFileHandler
import logbook

logbook.set_datetime_format('local')


class LogHandler(object):
    """默认的 Log 类"""

    def __init__(self, filename='default.log', consolelevel=logging.DEBUG, filelevel=logging.ERROR):
        """Log对象
        :param :filename: log 文件名
        :param :loglevel: 设定log等级 ['CRITICAL', 'ERROR', 'WARNING', 'NOTICE', 'INFO', 'DEBUG', 'TRACE', 'NOTSET']
        """
        os.makedirs("./logs", exist_ok=True)
        self.log = self._logging(consolelevel=consolelevel, filelevel=filelevel, filename="./logs/" + filename)

    def __getattr__(self, item, *args, **kwargs):
        return self.log.__getattribute__(item, *args, **kwargs)

    def _logging(self, **kwargs):
        consolelevel = kwargs.pop('consolelevel', None)
        filelevel = kwargs.pop('filelevel', None)
        filename = kwargs.pop('filename', None)
        datefmt = kwargs.pop('datefmt', None)
        format = kwargs.pop('format', None)
        if filename is None:
            filename = 'default.log'
        if datefmt is None:
            datefmt = '%Y-%m-%d %H:%M:%S'
        if format is None:
            # [%(asctime)s] [%(levelname)s] [%(module)s] [%(lineno)d] %(message)s
            format = '[%(asctime)s] [%(levelname)s] [%(module)s] [%(lineno)d] %(message)s'

        log = logging.getLogger(filename)
        format_str = logging.Formatter(format, datefmt)
        # backupCount 保存日志的数量，过期自动删除
        # when 按什么日期格式切分(这里方便测试使用的秒)

        # file_handler = FileHandler(filepath, level=loglevel)
        # log.addHandler(file_handler)

        th = TimedRotatingFileHandler(filename=filename, when='D', backupCount=5, encoding='utf-8')
        th.setFormatter(format_str)
        th.setLevel(filelevel)
        log.addHandler(th)

        # 为了看的更视觉效果，可以显示在控制台答应
        cmd = logging.StreamHandler()
        cmd.setFormatter(format_str)
        cmd.setLevel(consolelevel)
        log.addHandler(cmd)
        log.setLevel(consolelevel)
        return log
