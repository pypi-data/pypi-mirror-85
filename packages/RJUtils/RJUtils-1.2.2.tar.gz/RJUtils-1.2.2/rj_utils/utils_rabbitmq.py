# coding:utf-8
import traceback

import pika

"""
rabbitmq 工具类
pip install pika
"""


class RabbitmqTools:
    def __init__(self, username, password, host, port):
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self._connection = None
        self._channel = None
        self.queue_name = ''

    def connect(self, queue_name):
        try:
            credentials = pika.PlainCredentials(self.username, self.password)
            parameters = pika.ConnectionParameters(self.host, self.port, '/', credentials)
            self._connection = pika.BlockingConnection(parameters)
            # channel是进行消息读写的通道
            self._channel = self._connection.channel()
            # 2 创建名为queue的队列
            self.queue_name = queue_name
            self._channel.queue_declare(queue=queue_name)
            return True
        except Exception as e:
            print(e.args)
        return False

    def publish(self, exchange_name='', exchange_routing_key='', data: str = ''):
        try:
            if self._channel is not None:
                if len(exchange_routing_key) == 0:
                    exchange_routing_key = self.queue_name
                self._channel.basic_publish(exchange=exchange_name,
                                            routing_key=exchange_routing_key,
                                            body=data)
                return True
        except Exception as e:
            print(e.args)
        return False

    def consume(self, queue_name: str, callback_fun):
        # def callback(ch, method, properties, body):
        #     print(" [x] Received %r")
        try:
            self._channel.basic_consume(on_message_callback=callback_fun, #回调函数。执行结束后立即执行另外一个函数返回给发送端是否执行完毕。
                                        queue=queue_name,
                                        auto_ack=True) #不会告知服务端我是否收到消息。一般注释。
            self._channel.start_consuming()
        except Exception as e:
            print(e.args)
            print(traceback.print_exc())

    def close(self):
        try:
            if self._connection is not None:
                self._connection.close()
                self._connection = None
        except Exception as e:
            print(e.args)


def backcall(ch, method, properties, body):#参数body是发送过来的消息。
    print(ch, method, properties)
    print('[x] Received %r' % body)


if __name__ == '__main__':
    rb = RabbitmqTools(username='jian', password='xinfu978', host='127.0.0.1', port='5672')
    rb.connect(queue_name='test')
    rb.publish(data='Hello World!')
    rb.consume(queue_name='test', callback_fun=backcall)
    rb.close()
