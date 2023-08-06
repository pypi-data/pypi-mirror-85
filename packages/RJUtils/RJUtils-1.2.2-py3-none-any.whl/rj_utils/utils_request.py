# -*- coding:utf-8 -*-
from urllib.error import HTTPError, URLError
from urllib.request import urlopen, Request


class Client(object):
    def __init__(self, url=None, ref=None, cookie=None):
        self._ref = ref
        self._cookie = cookie
        self._url = url
        self._setOpener()

    def _setOpener(self):
        request = Request(self._url)
        request.add_header("Accept-Language", "en-US,en;q=0.5")
        request.add_header("Connection", "keep-alive")
        #         request.add_header('Referer', self._ref)
        if self._cookie is not None:
            request.add_header("Cookie", self._cookie)
        request.add_header("User-Agent", 'Mozilla/5.0 (Windows NT 6.1; rv:37.0) Gecko/20100101 Firefox/37.0')
        self._request = request

    def gvalue(self):
        values = ""
        try:
            values = urlopen(self._request, timeout=10).read()
            # URLError是OSError的一个子类，HTTPError是URLError的一个子类
            # 如果想用HTTPError和URLError一起捕获异常，那么需要将HTTPError放在URLError的前面
        except HTTPError as e:
            print(e.code)
        except URLError as e:
            print(e.reason)
        return values


def proxyRequest(url, proxy):
    """
    使用代理
    :param url:
    :param proxy: 字典数据 代理地址 {'http': '106.46.136.112:808'}
    :return:
    """
    # 访问网址
    # url = 'http://www.whatismyip.com.tw/'
    # 这是代理IP
    # proxy = {'http': '106.46.136.112:808'}
    # 创建ProxyHandler
    from urllib import request
    proxy_support = request.ProxyHandler(proxy)
    # 创建Opener
    opener = request.build_opener(proxy_support)
    # 添加User Angent
    opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) \
                          AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36')]
    # 安装OPener
    request.install_opener(opener)
    # 使用自己安装好的Opener
    response = request.urlopen(url)
    return response


def downloadFile(url, filename):
    """
    下载文件
    :param url: "http://www.pythonscraping.com/"
    :param filename "logo.jpg"
    :return:
    """
    from urllib.request import urlretrieve
    urlretrieve(url, filename)
