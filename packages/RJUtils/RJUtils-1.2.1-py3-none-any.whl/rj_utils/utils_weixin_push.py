# -*- coding: utf-8 -*-
import json
import requests

'''
https://work.weixin.qq.com/api/doc/90000/90135/90236

企业微信消息推送
'''


class WeixinPushTools:
    _weixin_token = ''

    def __init__(self, corpid: str, corpsecret: str):
        self.corpid = corpid
        self.corpsecret = corpsecret

    def get_wxtoken(self):
        """获取access_token
        corpid：企业ID
        corpsecret：应用Secret
        """
        url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken'
        values = {'corpid': self.corpid,
                  'corpsecret': self.corpsecret,
                  }
        req = requests.post(url, params=values)
        data = json.loads(req.text)
        # print(data)
        '''
        {'errcode': 0, 'errmsg': 'ok', 'access_token': 'Ne-hg11xn3eTYkLfumfHrzCeNc9vDLL2dPcjPSHsSHwJOG6dhWyods4Unu__tkTieArpLd4UHSp4KTvXH8jDCTkjTSWIyQ654D309ss1Rq-hE0VWEVFP0nc6QMcJBCtQY3C_kS_tEvIfFxGuiOYF-I6-DlUuKy5XZP5-dMbyEIuJDJlZFT83CkOJLA2XcqIMfueSt9cV8HSrzbckRGNhrQ', 'expires_in': 7200}
        '''
        if data is not None and data['errcode'] == 0:
            return data["access_token"]
        else:
            return ''

    def send_msg(self, msg):
        """发送消息
        touser：账号，发送给谁，填写账号，多个人以“|”分隔
        toparty：部门ID
        agentid：应用AgentId
        content：发送的具体内容
        """
        retry_count = 2
        while retry_count >= 0:
            retry_count = retry_count - 1
            if self._weixin_token == '':
                self._weixin_token = self.get_wxtoken()
                if self._weixin_token == '':
                    print("获取不到微信access_token")
                    return

            url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=" + self._weixin_token
            values = """{"touser" : "ZhaoRuJian",
                     "toparty":"BaoStock",
                     "msgtype":"text",
                     "agentid":"1000002",
                     "text":{
                     "content": "%s"
                     },
                     "safe":"0"
                     }""" % (str(msg))
            req = requests.post(url, values.encode("utf-8").decode("latin1"))
            data = json.loads(req.text)
            if data is not None and data['errcode'] != 0:
                self._weixin_token = ''  # 重新获取token


if __name__ == '__main__':
    wx = WeixinPushTools('12123213', '2e1jij312ijiji123')
    wx.send_msg('123213')
