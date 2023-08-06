import pymysql
from pymysql.cursors import DictCursor

"""
pymysql
"""


class DBUtils:
    conn = None
    cur = None
    dowork = False
    host = ""
    port = ""
    user = ""
    passwd = ""
    db = ""

    def initConnect(self, host="127.0.0.1", port=3306, user="root", passwd="root", db="bigdata"):
        self.dowork = False
        try:
            # 创建数据库连接  localhost等效于127.0.0.1
            self.conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db, charset="utf8")
            # 建立游标，指定游标类型，返回字典
            self.cur = self.conn.cursor(DictCursor)
        except Exception as e:
            print(f"连接数据库异常:{e.args}")

    def exec_select(self, sqlStr):
        try:
            # 操作语句，只查询前两行 'select * from students limit 2;'
            self.cur.execute(sqlStr)
            # 获取查询的所有结果
            res = self.cur.fetchall()
            # 打印结果
            # print(res)
            return res
        except Exception as e:
            print(f"执行异常:{e.args}")
            return None

    # 开启事务
    def setDoWork(self):
        print('DBMySQL.setDoWork')
        self.dowork = True

    def commitWork(self):
        print('DBMySQL.commitWork')
        self.conn.commit()
        self.dowork = False

    def backWork(self):
        print('DBMySQL.backWork')
        self.conn.rollback()
        self.dowork = False

    def exec(self, sql_str, sql_par=()):
        try:
            self.cur.execute(sql_str, sql_par)
            if self.dowork is False:
                print('exec.commit')
                self.conn.commit()

            # 返回影响数
            return self.cur.rowcount
        except Exception as e:
            if self.dowork is False:
                self.conn.rollback()
            print('DBMySQL.exec:', e)
            raise e

    def query_all(self, sql_str, sql_par=()):
        cur = self.cur.execute(sql_str=sql_str, sql_par=sql_par)
        que = cur.fetchall()
        cols = cur.description
        tmp = []
        for v in que:
            row = {}
            for v2 in range(0, len(cols)):
                row[cols[v2][0]] = v[v2]
            tmp.append(row)
        return tmp

    def query_one(self, sql_str, sql_par=()):
        cur = self.cur.execute(sql_str=sql_str, sql_par=sql_par)
        que = cur.fetchone()
        if que is None:
            return None
        cols = cur.description
        row = {}
        for v2 in range(0, len(cols)):
            row[cols[v2][0]] = que[v2]
        return row

    def add(self, obj, tableName):
            sql = "INSERT INTO `"+ tableName +"` "
            par = []
            bval = '('
            eval = '('
            for key in obj:
                bval = bval + str(key) + ','
                eval = eval + '%s,'
                par.append(obj[key])

            bval = bval[0:-1] + ')'
            eval = eval[0:-1] + ') '
            sql = sql + bval + ' VALUES ' + eval
            bak = self.exec(sql_str=sql, sql_par=par)
            return bak

    def delById(self, id,tableName):
        if id <= 0:
            raise Exception("id < 0")
        sql = 'DELETE FROM `' + tableName + '` WHERE id = %s'
        par = [id]

        bak = self.exec(sql_str=sql, sql_par=par)
        return bak

    def findById(self, id,tableName):
        if id <= 0:
            raise Exception("id < 0")
        sql = 'SELECT * FROM `' + tableName + '` where id = %s'
        par = [id]

        bak = self.query(sql_str=sql, sql_par=par).fetchone()
        return bak

    def closeConnect(self):
        try:
            if self.cur is not None:
                self.cur.close()
            if self.conn is not None:
                self.conn.close()
        except Exception as e:
            print(f"执行异常:{e.args}")


if __name__ == '__main__':
    db = DBUtils()
    db.initConnect()
    db.exec('select * from strategies;')
