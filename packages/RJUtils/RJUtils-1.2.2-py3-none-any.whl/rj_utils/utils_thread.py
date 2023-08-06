import threading

threads = []


def createThrreadPool(fun, tupge):
    """
    创建线程池
    :param fun: 调用方法
    :param tupge: 参数组成的元组 (url, i)
    :return:
    """
    thread = threading.Thread(target=fun, args=tupge)
    thread.start()
    threads.append(thread)


def waitForThreadFinish():
    """
    等待线程池线程关闭
    :return:
    """
    for i in threads:
        i.join()
