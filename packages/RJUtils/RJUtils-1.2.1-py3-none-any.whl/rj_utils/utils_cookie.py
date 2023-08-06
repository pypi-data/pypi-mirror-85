"""
在HTTP包中，提供了cookiejar模块，用于提供对Cookie的支持。
该模块主要的对象有CookieJar、FileCookieJar、MozillaCookieJar、LWPCookieJar

CookieJar–派生–>FileCookieJar–派生–>MozillaCookieJar和LWPCookieJar

"""


def cookieRequest(url):
    """
    将Cookie保存到变量中
    :return:response,cookie
    """
    # 声明一个CookieJar对象实例来保存cookie
    from http import cookiejar
    from urllib import request
    cookie = cookiejar.CookieJar()
    # 利用urllib.request库的HTTPCookieProcessor对象来创建cookie处理器,也就CookieHandler
    handler = request.HTTPCookieProcessor(cookie)
    # 通过CookieHandler创建opener
    opener = request.build_opener(handler)
    # 此处的open方法打开网页
    response = opener.open(url)
    # 打印cookie信息
    for item in cookie:
        print('Name = %s' % item.name)
        print('Value = %s' % item.value)
    return response, cookie


def cookieToFileRequest(url, filepath):
    """
    保存Cookie到文件
    :param url:
    :param filepath: 保存的文件路径 'c:/cookie.txt'
    :return:
    """
    from http import cookiejar
    from urllib import request
    # 设置保存cookie的文件，同级目录下的cookie.txt
    # 声明一个MozillaCookieJar对象实例来保存cookie，之后写入文件
    cookie = cookiejar.MozillaCookieJar(filepath)
    # 利用urllib.request库的HTTPCookieProcessor对象来创建cookie处理器,也就CookieHandler
    handler = request.HTTPCookieProcessor(cookie)
    # 通过CookieHandler创建opener
    opener = request.build_opener(handler)
    # 此处的open方法打开网页
    response = opener.open(url)
    # 保存cookie到文件
    cookie.save(ignore_discard=True, ignore_expires=True)


def loadCookieFromFileRequest(url, filepath):
    """
    从文件中获取Cookie并访问
    :param url:
    :param filepath:文件路径 'c:/cookie.txt'
    :return:
    """
    from http import cookiejar
    from urllib import request
    # 设置保存cookie的文件的文件名,相对路径,也就是同级目录下
    # 创建MozillaCookieJar实例对象
    cookie = cookiejar.MozillaCookieJar()
    # 从文件中读取cookie内容到变量
    cookie.load(filepath, ignore_discard=True, ignore_expires=True)
    # 利用urllib.request库的HTTPCookieProcessor对象来创建cookie处理器,也就CookieHandler
    handler = request.HTTPCookieProcessor(cookie)
    # 通过CookieHandler创建opener
    opener = request.build_opener(handler)
    # 此用opener的open方法打开网页
    response = opener.open(url)
    # 打印信息
    print(response.read().decode('utf-8'))
