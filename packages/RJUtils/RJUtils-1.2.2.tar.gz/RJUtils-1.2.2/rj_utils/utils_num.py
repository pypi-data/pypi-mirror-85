def getRandom(n=13):
    """
    获取随机数
    :param n: 位数
    :return:
    """
    from random import randint
    start = 10 ** (n - 1)
    end = (10 ** n) - 1
    return str(randint(start, end))