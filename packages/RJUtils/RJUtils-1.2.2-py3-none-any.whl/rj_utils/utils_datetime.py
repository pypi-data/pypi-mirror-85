import time
from datetime import datetime, timedelta

"""
时间工具类
"""


def getMisSecond():
    """
    秒级时间戳
    :return:
    """
    return time.time()  # float


def getMisSecond2():
    """
    秒级时间戳
    :return:
    """
    return int(time.time())


def getMisSecond3():
    """
    毫秒级时间戳
    :return:
    """
    return int(round(time.time() * 1000))


def getMisSecond4():
    """
    微秒级时间戳
    :return:
    """
    return int(round(time.time() * 1000000))


def getDateTimeStr(format='%Y-%m-%d %H:%M:%S'):
    """
    获取当前日期时间
    :param format:
    :return:
    """
    import datetime
    # 2018-09-06 21:54:46
    return datetime.datetime.now().strftime(format)


def getDateTimeStrWithMis(format='%Y-%m-%d %H:%M:%S.%f'):
    """
    获取当前日期时间，带微秒
    :param format:
    :return:
    """
    import datetime
    # 2018-09-06 21:54:46.205213
    return datetime.datetime.now().strftime(format)  # 含微秒的日期时间，来源 比特量化


def timestampToDateStr(timestamp, format='%Y-%m-%d %H:%M:%S'):
    """
    1515774430 -> 2018-01-13 00:27:10
    :param timestamp:
    :param format:格式化的字符串
    :return:
    """
    return time.strftime(format, time.localtime(timestamp))


def reformatDatetimeStr(dateStr, oldFormat='%m/%d/%Y %H:%M', newFormat='%Y-%m-%d %H:%M:%S'):
    """
    '08/02/2019 01:00' -> 2019-08-02 01:00:00
    :param dt:
    :return:
    """
    import datetime
    return datetime.datetime.strptime(dateStr, oldFormat).strftime(newFormat)


def compare_time(time1, time2, format_time='%Y-%m-%d', dis_type='d'):
    """
    比较日期字符串间隔的天数，毫秒，秒
    :param time1: '2015-03-05 17:41:20'
    :param time2: '2015-03-02 17:41:20'
    :param dis_type:d 天，s 秒，ms 毫秒
    :return:返回日期间隔 d 天，s 秒，ms 毫秒
    """
    import datetime
    d1 = datetime.datetime.strptime(time1, format_time)
    d2 = datetime.datetime.strptime(time2, format_time)
    delta = d1 - d2
    if dis_type == 's':
        return delta.seconds
    elif dis_type == 'd':
        return delta.days
    elif dis_type == 'ms':
        return delta.microseconds
    else:
        return delta.days


def datetimeStr2struct(datetime_str: str):
    """
    :param datetime_str:"2018-09-06 21:54:46"
    :return:time.struct_time(tm_year=2018, tm_mon=9, tm_mday=6, tm_hour=21, tm_min=54, tm_sec=46, tm_wday=3, tm_yday=249, tm_isdst=-1)
    """
    return time.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')  # 日期时间转结构体


def timestamp2struct(timestamp):
    """
    :param timestamp: 1486188476
    :return: time.struct_time(tm_year=2017, tm_mon=2, tm_mday=4, tm_hour=14, tm_min=7, tm_sec=56, tm_wday=5, tm_yday=35, tm_isdst=0)
    """
    return time.localtime(timestamp)  # 时间戳转结构体，注意时间戳要求为int，来源 比特量化


def get_today_str():
    """
    获取日
    :return:2020-08-03
    """
    return str(datetime.today().date())


def getNowTimeStr():
    """
    获取当前时间字符串
    :return: %Y-%m-%d %H:%M:%S
    """
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def getDateBeforeToday(beforeOfDay):
    """
    获取前1天或N天的日期，beforeOfDay=1：前1天；beforeOfDay=N：前N天
    :param self:
    :param beforeOfDay:整数，例如：20,30...
    :return:
    """
    today = datetime.now()
    # 计算偏移量
    offset = timedelta(days=-beforeOfDay)
    # 获取想要的日期的时间
    re_date = (today + offset).strftime('%Y-%m-%d')
    return re_date


def getYearStr():
    """
    当前年份
    :return:
    """
    return datetime.today().year


def getMonthStr():
    """
    当前月份
    :return:
    """
    return datetime.today().month


def getHourStr():
    """
    当前小时
    :return:
    """
    return datetime.today().hour


def getTodayLastYear():
    """
    上年对应的时间
    :return:
    """
    return str(datetime.today().date() + timedelta(-365))


def getWeek_N_Day(days=-7):
    """
    前几天对应的星期
    :param days:
    :return:例如：
    """
    return str(datetime.today().date() + timedelta(days))


def compare_time2(time1, time2, format_time='%Y-%m-%d', dis_type='d'):
    """
    比较日期字符串间隔的天数
    :param time1: '2015-03-05 17:41:20'
    :param time2: '2015-03-02 17:41:20'
    :param dis_type:d 天，s 秒，ms 毫秒
    :return:返回日期间隔的天数，毫秒，秒
    """
    import datetime
    d1 = datetime.datetime.strptime(time1, format_time)
    d2 = datetime.datetime.strptime(time2, format_time)
    delta = d1 - d2
    if dis_type == 's':
        return delta.seconds
    elif dis_type == 'd':
        return delta.days
    elif dis_type == 'ms':
        return delta.microseconds
    else:
        return delta.days


def compare_time(time1, time2, format_time='%Y-%m-%d'):
    """
    比较日期字符串间隔的天数
    :param time1:
    :param time2:
    :return:
    """
    import time
    s_time = time.mktime(time.strptime(time1, format_time))
    e_time = time.mktime(time.strptime(time2, format_time))
    return int(s_time) - int(e_time)


def calpreMinu():
    """
    计算距离下一分钟还有多少秒
    :return:
    """
    date_1 = datetime.now()
    date_2 = date_1 + timedelta(minutes=1)  # 同理，后一秒钟设置：seconds=1
    print(date_1, date_2)
    dis = date_2-date_1
    return dis.seconds


def isTradeTime() -> bool:
    """
    判断是否股票交易时间
    :return:
    """
    now_time = datetime.strptime(datetime.strftime(datetime.now(), '%H:%M:%S'), '%H:%M:%S')
    # now_time为记录当前时间，由于从Tushare取回的实时分笔数据只有时间，
    # 没有日期，所以用上面的操作把现在的时间的日期换成1900:1:1日，方便计算时间差
    rest_time = now_time - datetime.strptime('11:30:00', '%H:%M:%S')
    # 用来计算当前时间和中午11:30休市时间的差值
    if rest_time.days == 0 and rest_time.seconds > 0 and rest_time.seconds < 5400:
        # 中午11:30~13:00为中午休市时间，时长5400 seconds
        print(f'中午休市时间 {datetime.now()}')
        return False
    if rest_time.days == 0 and rest_time.seconds > 12600:
        # 下午15:00结束交易，与11:30的时间差为12600 seconds，关闭程序
        print(f'交易时间已结束!{datetime.now()}')
        return False
    return True


if __name__ == '__main__':
    print(calpreMinu())
