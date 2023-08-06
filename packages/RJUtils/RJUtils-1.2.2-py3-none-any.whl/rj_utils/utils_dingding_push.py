import requests
import json


# 开发文档https://ding-doc.dingtalk.com/doc#/serverapi2/qf2nxq
class DingdingManager:
    # 构建请求头部
    _header = {
        "Content-Type": "application/json",
        "Charset": "UTF-8"
    }

    # 构建请求数据
    _keyword = "股哥预警："

    def __init__(self, token):
        self._webhook = f'https://oapi.dingtalk.com/robot/send?access_token={token}'

    def sendText(self, msg):
        """
        发送文本
        :param msg:
        :return:
        """
        message = {
            "msgtype": "text",
            "text": {
                "content": self._keyword + "\n" + msg
            },
            "at": {
                "atMobiles": [],
                "isAtAll": True
            }
        }
        self._request_url(message)

    def sendLinkText(self, msg: str, link: str):
        """
        发送链接消息
        :param msg: 消息内容,字符串类型
        :param link: 链接，如："http://baidu.com"
        :return:
        """
        message = {
            "msgtype": "link",
            "link": {
                "text": msg,
                "title": self._keyword,
                "picUrl": "",
                "messageUrl": link
            }
        }
        self._request_url(message)

    def sendMarkdownText(self, msg: str):
        """
        发送markdown数据
        :param msg:
        :return:
        """
        message = {
            "msgtype": "markdown",
            "markdown": {
                "title": self._keyword,
                "text": msg
            },
            "at": {
                "atMobiles": [],
                "isAtAll": False
            }
        }
        self._request_url(message)

    def sendActionCardText(self, msg: str, url: str):
        message = {
            "actionCard": {
                "title": self._keyword,
                "text": msg,
                "hideAvatar": "0",
                "btnOrientation": "0",
                "singleTitle": "阅读全文",
                "singleURL": url
            },
            "msgtype": "actionCard"

        }
        self._request_url(message)

    def sendFeedCardText(self, msg: str, url: str = '', picurl: str = ''):
        message = {
            "feedCard": {
                "links": [
                    {
                        "title": self._keyword + msg,
                        "messageURL": url,
                        "picURL": picurl
                    }
                ]
            },
            "msgtype": "feedCard"
        }
        self._request_url(message)

    def _request_url(self, message):
        # 对请求的数据进行json封装
        message_json = json.dumps(message)
        # 发送请求
        info = requests.post(url=self._webhook, data=message_json, headers=self._header)
        # 打印返回的结果
        print(info.text)


if __name__ == "__main__":
    dd = DingdingManager('xxx')
    dd.sendText("上班注意安全，不要迟到")
    # sendLinkText("")
    # sendMarkdownText("")
    # sendActionCardText("")
    # sendFeedCardText("")
