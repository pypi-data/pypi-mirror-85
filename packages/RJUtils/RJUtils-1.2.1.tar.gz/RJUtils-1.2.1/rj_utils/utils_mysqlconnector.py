from pathlib import Path
import mysql.connector

"""
pip install mysql-connector-python
"""

def is_exist_db(connect, db_name):
    """数据库是否已存在"""
    cur = connect.cursor()
    cur.execute("SELECT 1 FROM information_schema.SCHEMATA where SCHEMA_NAME={db_name}".format(db_name=db_name))
    a = cur.fetchone()
    cur.close()
    return True if a else False


def get_db_version(connect, db_name):
    try:
        cur = connect.cursor()
        cur.execute("select \`version\` from {}.\`version\`".format(db_name))
        a = cur.fetchone()
        cur.close()
        return a[0] if a else 0
    except:
        return 0


def create_database_from_file(connect, sqlDir, filename, dbname):
    """
    从sql文件创建数据库
    :param connect:
    :param sqlDir: 文件夹路径 C:/mysql_upgrade/
    :param filename: 文件名 createdb.sql
    :param dbname: 数据库名
    :return:
    """
    """创建数据库"""
    cur = connect.cursor()
    if not is_exist_db(connect,dbname):
        filename = sqlDir + filename
        with open(filename, 'r', encoding='utf8') as f:
            sql = f.read()
        for x in cur.execute(sql, multi=True):
            # print(x.statement)
            pass

    db_version = get_db_version(connect, dbname)
    files = [x for x in Path(sqlDir).iterdir() \
             if x.is_file() \
             and x.name != filename \
             and x.name != '__init__.py' \
             and int(x.stem) > db_version and not x.is_dir()]
    files.sort()
    for file in files:
        sql = file.read_text(encoding='utf8')
        for x in cur.execute(sql, multi=True):
            # print(x.statement)
            pass

    connect.commit()
    cur.close()


if __name__ == '__main__':
    host = '127.0.0.1'
    port = 3306
    usr = 'root'
    pwd = 'root'

    cnx = mysql.connector.connect(user=usr, password=pwd, host=host, port=port)
    create_database_from_file(cnx, 'c:/sqldir/', 'test.sql', 'test')

    cnx.commit()
