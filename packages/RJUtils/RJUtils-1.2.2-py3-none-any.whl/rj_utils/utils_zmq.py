import zmq

"""
ZeroMq 工具类
"""


class ZMQClientUtils:
    _quote_ctx = None
    _client = None
    _finished = False

    def stop(self):
        """
        关闭连接
        :return:
        """
        self._finished = True
        if self._quote_ctx is not None:
            # 停止异步数据接收
            self._quote_ctx.stop()
            # 关闭对象
            self._quote_ctx.close()

    def _connect_zmq(self, ip_addr, theme):
        try:
            quote_ctx = zmq.Context()
            self._client = quote_ctx.socket(zmq.SUB)
            self._client.connect(ip_addr)
            # client.setsockopt(zmq.ZMQ_RECONNECT_IVL, 500)
            # client.setsockopt(zmq.ZMQ_RECONNECT_IVL_MAX, 5000)
            if type(theme) == list:
                for item in theme:
                    self._client.setsockopt_string(zmq.SUBSCRIBE, item)
            else:
                self._client.setsockopt_string(zmq.SUBSCRIBE, theme)

            self._client.setsockopt(zmq.RCVTIMEO, 10000)
            return self._client
        except zmq.error.ZMQError as e:
            print("zmq 连接出错:%s" % e)
            return None

    def createClient(self, ip_addr="tcp://localhost:10011", theme=None, callback=None):
        """
        创建连接
        :param ip_addr: tcp://localhost:10011
        :param theme: 主题
        :param 回调函数
        :return:
        """
        self._connect_zmq(ip_addr, theme)

        self._finished = False
        while not self._finished:
            try:
                if self._client is not None:
                    response = self._client.recv()
                else:
                    print(f'zmq尝试重连......')
                    client = self._connect_zmq(ip_addr, theme)
                    continue
            except zmq.ZMQError as e:
                print(f'zmq {e.args}')
                self._client.close()
                print(f'zmq尝试重连......')
                client = self._connect_zmq(ip_addr, theme)
                continue

            temp = str(response, encoding='GB2312')
            print("response: %s" % temp)
            if callback is not None:
                callback(temp)


class ZMQServerUtils:
    _zmq_content = None
    _zmq_socket = None

    @classmethod
    def init(self, ip_addr="tcp://*:10011"):
        try:
            self._zmq_content = zmq.Context()
            self._zmq_socket = self._zmq_content.socket(zmq.PUB)
            self._zmq_socket.bind(ip_addr)
        except zmq.error.ZMQError as e:
            print("zmq_socket 异常:%s" % e)
            return False
        return True

    @classmethod
    def sendMsg(self, theme='', data=''):
        if self._zmq_socket is not None:
            self._zmq_socket.send_string(theme, zmq.NOBLOCK | zmq.SNDMORE)
            self._zmq_socket.send_string(data)

    @classmethod
    def close(self):
        if self._zmq_socket is not None:
            self._zmq_socket.close()


if __name__ == '__main__':
    server = ZMQServerUtils()
    server.init()
    server.sendMsg('ee', '1212312')
    server.close()
