import random
import time

import requests

"""
requests 网络请求工具
"""
user_agents = [
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
    'Opera/9.25 (Windows NT 5.1; U; en)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
    'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
    'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
    'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9',
    "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Ubuntu/11.04 Chromium/16.0.912.77 Chrome/16.0.912.77 Safari/535.7",
    "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0 ",
    "Mozilla/5.0 (Windows NT 10.0; WOW64)",
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)Chrome/51.0.2704.63 Safari/537.36'
]


def get_html_text(url):
    request = None
    while True:
        try:
            # 在短時間使用多次requests会Failed to establish a new connection這樣一個錯誤，设置'Connection': 'close'
            headers = {'User-Agent': random.choice(user_agents), 'Connection': 'close'}
            request = requests.get(url, headers=headers, timeout=None)

            if request is not None:
                request.raise_for_status()
                request.encoding = request.apparent_encoding
                # print(r.url)
                if request.status_code == 200:
                    rst = request.text
                    request.close()
                    return rst
                request.close()
            return ""
        except Exception as e:
            request.close()
            print(f'请求发生错误：{e}')
            time.sleep(2)


def get_page_json(url):
    headers = {'cookie': '',
               'User-Agent': random.choice(user_agents),
               'Connection': 'close'}
    # url = 'https://www.csdn.net/api/articles?type=more&category=home&shown_offset=0'
    try:
        r = requests.get(url, headers=headers, timeout=30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        if r.status_code == 200:
            return r.json()
        return ""
    except ConnectionError as e:
        print(e)
        return ""


def get_page_detail(url):
    headers = {
        'user-agent': random.choice(user_agents),
        'Connection': 'close'}
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except ConnectionError:
        print('Error occurred')
        return None


def download_image(url):
    print('Downloading', url)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            save_image(response.content)
        return None
    except ConnectionError:
        return None


def save_image(content):
    import os
    file_path = '{0}'.format(os.getcwd() + '\images')
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    from _md5 import md5
    image_path = '{0}/{1}.{2}'.format(os.getcwd() + '\images', md5(content).hexdigest(), 'jpg')
    if not os.path.exists(image_path):
        with open(image_path, 'wb') as f:
            f.write(content)
            f.close()
