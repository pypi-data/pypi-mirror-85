import random


# random.random()
# random.uniform(1, 10)
#
# random.randint(0, 99)
# random.randrange(0, 101, 2)
#
# # 随机字符：
# random.choice('abcdefg&#%^*f')
#
# # 多个字符中选取特定数量的字符
# random.sample('abcdefghij', 3)
#
# random.sample(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j'], 3)
#
# random.choice(['apple', 'pear', 'peach', 'orange', 'lemon'])

def randomValue():
    """
    获取一个随机数，浮点类型
    :return:
    """
    return random.random()


def shuffle(list_data) -> list:
    """
    打乱列表子项顺序
    :param list_data:
    :return:
    """
    # list_data = [1, 2, 3, 4, 5, 6]
    random.shuffle(list_data)
    return list_data
