from typing import Optional
from pandas import DataFrame
from sqlalchemy import create_engine
import pandas as pd
from sqlalchemy.exc import ProgrammingError

"""
DateFrame 保存到mysql
"""


class Pd2Sql:
    engine = None

    def initConnect(self, name: str, pwd: str, dbname: str, host='127.0.0.1', port='3306') -> bool:
        """
        初始化连接数据库
        :param name: 用户名
        :param pwd: 密码
        :param dbname: 数据库名
        :param host: 地址
        :return:
        """
        if len(name) == 0 or len(pwd) == 0 or len(dbname) == 0:
            print('参数错误')
            return False
        self.engine = create_engine(f'mysql+pymysql://{name}:{pwd}@{host}:{port}/{dbname}?charset=utf8')
        # 用DBAPI构建数据库链接engine
        # con = pymysql.connect(host=localhost, user=username, password=password, database=dbname, charset='utf8',
        #                       use_unicode=True)

        if self.engine is None:
            return False
        else:
            return True

    def sql2df(self, table_name: str, sql_cmd='') -> Optional[DataFrame]:
        """
        从mysql中读取数据转DataFrame
        :param sql_cmd:数据库执行语句，例如：SELECT * FROM tablename;
        :param table_name:表名
        :return:
        """
        if self.engine is None:
            print("请先调用initConnect初始化")
            return None

        if sql_cmd == '':
            sql_cmd = 'SELECT * FROM {}'.format(table_name)
        return pd.read_sql(sql=sql_cmd, con=self.engine)

    def sqlcmd2df(self, sql_cmd='') -> Optional[DataFrame]:
        """
        从mysql中读取数据转DataFrame
        :param sql_cmd:数据库执行语句，例如：SELECT * FROM tablename;
        :return:
        """
        df = None
        if self.engine is None:
            print("请先调用initConnect初始化")
            return None

        if sql_cmd == '':
            print("sql 语句为空")
            return None
        try:
            df = pd.read_sql(sql=sql_cmd, con=self.engine)
        except ProgrammingError as e:
            print(f'数据库查询出错:{e.code}')
            return None
        return df

    def df2sql(self, df: DataFrame, table_name: str, dtype=None, replace_if_exists=False):
        """
        DataFrame 存到mysql
        :param replace_if_exists:
        :param df:
        :param table_name:
        :param dtype:
        例如：
        dtype={'EMP_ID': sqlalchemy.types.BigInteger(),
              'GENDER': sqlalchemy.types.String(length=20)
              }
        :return:
        """
        if self.engine is None:
            print("请先调用initConnect初始化")
            return
        if df is None:
            print("df 为空")
            return

        if replace_if_exists:
            df.to_sql(table_name, self.engine, index=False, if_exists='replace', dtype=dtype)
        else:
            df.to_sql(table_name, self.engine, index=False, if_exists='append', dtype=dtype)
