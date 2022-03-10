"""
----------------------------------------------------
@Time  :  2022/2/21 19:57
@Author  :  shina
@File  :  db_utils01.PY
----------------------------------------------------
"""
import pymysql
from comms.public_api import get_ini_data


class DBUtils(object):
    count = -1

    # 封装连接对象和游标对象
    def __init__(self):
        try:
            self.conn = pymysql.connect(host=get_ini_data('mysql', 'host'),
                                        port=int(get_ini_data('mysql', 'port')),
                                        user=get_ini_data('mysql', 'user'),
                                        password=get_ini_data('mysql', 'password'),
                                        db=get_ini_data('mysql', 'db'))
            self.cursor = self.conn.cursor()
        except Exception as e:
            print("数据库工具类连接出现异常，请检查DBUtils中的__init__方法")
            print(e)

    # 封装关闭游标对象和连接对象
    def close(self):
        self.cursor.close()
        self.conn.close()

    # 封装查询结果集有多少条数据
    # 如果execute()括号里面只有1个参数，我们需要运行count = cursor.execute(sql)
    # 如果execute()括号里面有2个参数，我们需要运行count = cursor.execute(sql，展位符数据（元组）)---params
    def find_count(self, sql, params=None):
        self.conn.commit()  # 防止连接池溢出
        try:
            if params is None:
                self.count = self.cursor.execute(sql)
                return self.count
            elif params is not None:
                self.count = self.cursor.execute(sql, params)
                return self.count
        except Exception as e:
            print("查询数据库条目失败", e)

    # 封装增删改
    # 如果execute()括号里只传一个参数,我们需要运行: count = cursor.execute(sql)
    # 如果execute()括号里传2个参数,我们需要运行: count = cursor.execute(sql,占位符数据(元组))
    def cud(self, sql, params=None):
        self.conn.commit()
        try:
            if params is None:
                self.count = self.cursor.execute(sql)
            if isinstance(params, tuple):
                self.count = self.cursor.execute(sql, params)
            if isinstance(params, list):
                self.count = self.cursor.executemany(sql, params)
            self.conn.commit()
            return self.count
        except Exception as e:
            print("增删改执行失败!", e)

    # 封装查询并获取一条数据: execute(sql)   execute(sql,params)
    def find_one(self, sql, params=None):
        self.conn.commit()
        try:
            if params is None:
                self.cursor.execute(sql)  # 执行sql语句并且把结果放在cursor当中
            elif params is not None:
                self.cursor.execute(sql, params)
            return self.cursor.fetchone()  # 从结果集中获取一条数据
        except Exception as e:
            print("查询单条数据失败!", e)

    def find_all(self, sql, params=None):
        self.conn.commit()
        try:
            if params is None:
                self.cursor.execute(sql)  # 执行sql语句并且把结果存在cursor
            if params is not None:
                self.cursor.execute(sql, params)
            return self.cursor.fetchall()  # 从结果集中获取所有数据
        except Exception as e:
            print("查询所有数据失败!", e)


if __name__ == '__main__':
    db = DBUtils()
    data = db.find_one('select * from tb_user order by rand() limit 1;')
    print(data)
    db.close()
