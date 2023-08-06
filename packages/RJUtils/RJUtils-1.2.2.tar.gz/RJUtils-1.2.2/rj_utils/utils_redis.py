# coding: utf-8
import redis
from rj_utils.utils_file import file2dict


class RedisUtils(object):
    """
    Redis操作类
    配置文件格式：
        {
            "redisip": "127.0.0.1",
            "redisport": "6379",
            "passwd": "redis123",
            "db": 0
        }
    """

    def __init__(self, conf_path):
        """
        :param conf_path: 配置文件路径 ../redis.conf
        """
        self.config = file2dict(conf_path)
        if self.config['redisip'] is None or self.config['redisport'] is None:
            print("配置文件参数错误！！")
            return

        try:
            if self.config['passwd'] is None:
                self.selfpool = redis.ConnectionPool(host=self.config['redisip'],
                                                     port=self.config['redisport'],
                                                     decode_responses=True)

            else:
                self.selfpool = redis.ConnectionPool(host=self.config['redisip'],
                                                     port=self.config['redisport'],
                                                     password=self.config['passwd'],
                                                     decode_responses=True)
            self.r = redis.Redis(connection_pool=self.selfpool)
        except Exception as e:
            print(e.args)

    def cleanup(self):
        """
        清理Redis当前数据库
        :return:
        """
        self.r.flushdb()

    def lookup_redist_info(self):
        """
        查询Redis配置
        :return:
        """
        info = self.r.info()
        return info

    def set_key_value(self, key, value):
        """
        设置键值对key<-->value
        :param key:
        :param value:
        :return:
        """
        self.r.expire(key, 20)
        return self.r.set(key, value)

    def set_key_value_with_timeout(self, key, value, time):
        """
        设置键值对key<-->value
        带超时
        :param key:
        :param value:
        :param time: 超时时间（秒）
        :return:
        """
        self.r.set(key, value)
        self.r.expire(key, time)

    def get_key_value(self, key):
        """
        查询键值对
        :param key:
        :return:
        """
        return self.r.get(key)

    def set_hkey_value(self, name, key, value):
        """
        设置哈希键值对key<-->value
        :param name:
        :param key:
        :param value:
        :return:
        """
        return self.r.hset(name, key, value)

    def get_hkey_value(self, name, key):
        """
        设置哈希键值对key<-->value
        :param name:
        :param key:
        :return:
        """
        return self.r.hget(name, key)

    def save(self):
        """
        强行保存数据到硬盘
        :return:
        """
        return self.r.save()

    def get_keys(self):
        """
        获取当前数据库里面所有键值
        :return:
        """
        return self.r.keys()

    def delete_key(self, key):
        """
        删除某个键
        :param key:
        :return:
        """
        return self.r.delete(key)

    def push_list_value(self, listname, value):
        """
        推入到队列
        :param listname:
        :param value:
        :return:
        """
        return self.r.lpush(listname, value)

    def pull_list_range(self, listname, starpos=0, endpos=-1):
        """
        获取队列某个连续片段
        :param listname:
        :param starpos:
        :param endpos:
        :return:
        """
        return self.r.lrange(listname, starpos, endpos)

    def get_list_len(self, listname):
        """
        获取队列长度
        :param listname:
        :return:
        """
        return self.r.llen(listname)


def main():
    ri = RedisUtils('../conf/redis.conf')
    ri.lookup_redist_info()
    # ri.set_key_value('test1', 1)
    ri.set_key_value_with_timeout("timeout", "ded", 30)
    # ri.push_list_value('test2', 1)
    # ri.push_list_value('test2', 2)


if __name__ == '__main__':
    main()
