# coding=utf-8
"""
使用DBUtils数据库连接池中的连接，操作数据库 OperationalError: (2006, ‘MySQL server has gone away’)
"""
import json
import datetime
from dbutils.pooled_db import PooledDB
# from DBUtils.PooledDB import PooledDB
import pymysql


class MysqlClient(object):
    __pool = None;

    def __init__(self, mincached=10, maxcached=20, maxshared=10, maxconnections=200, blocking=True,
                 maxusage=100, setsession=None, reset=True,
                 host='47.113.200.109', port=33063, db='hx_sales',  # 192.168.5.70
                 user='aiit', passwd='aiit9876', charset='utf8mb4'):  # 123456    aqz111
        """

        :param mincached:连接池中空闲连接的初始数量
        :param maxcached:连接池中空闲连接的最大数量
        :param maxshared:共享连接的最大数量
        :param maxconnections:创建连接池的最大数量
        :param blocking:超过最大连接数量时候的表现，为True等待连接数量下降，为false直接报错处理
        :param maxusage:单个连接的最大重复使用次数
        :param setsession:optional list of SQL commands that may serve to prepare
            the session, e.g. ["set datestyle to ...", "set time zone ..."]
        :param reset:how connections should be reset when returned to the pool
            (False or None to rollback transcations started with begin(),
            True to always issue a rollback for safety's sake)
        :param host:数据库ip地址
        :param port:数据库端口
        :param db:库名
        :param user:用户名
        :param passwd:密码
        :param charset:字符编码
        """

        if not self.__pool:
            self.__class__.__pool = PooledDB(pymysql,
                                             mincached, maxcached,
                                             maxshared, maxconnections, blocking,
                                             maxusage, setsession, reset,
                                             host=host, port=port, db=db,
                                             user=user, passwd=passwd,
                                             charset=charset,
                                             cursorclass=pymysql.cursors.DictCursor
                                             )
        self._conn = None
        self._cursor = None
        self.__get_conn()

    def __get_conn(self):
        self._conn = self.__pool.connection();
        self._cursor = self._conn.cursor();

    def close(self):
        try:
            self._cursor.close()
            self._conn.close()
        except Exception as e:
            print(e)

    def __execute(self, sql, param=()):
        count = self._cursor.execute(sql, param)
        return count

    def execute(self, sql, param=()):
        count = self.__execute(sql, param)
        return count

    def begin(self):
        self._conn.autocommit(0)

    def end(self, option='commit'):
        if option == 'commit':
            self._conn.autocommit()
        else:
            self._conn.rollback()

    @staticmethod
    def __dict_datetime_obj_to_str(result_dict):
        """把字典里面的datatime对象转成字符串，使json转换不出错"""
        if result_dict:
            result_replace = {k: v.__str__() for k, v in result_dict.items() if isinstance(v, datetime.datetime)}
            result_dict.update(result_replace)
        return result_dict

    def select_one(self, sql, param=()):
        count = self.__execute(sql, param)
        result = self._cursor.fetchone()
        """:type result:dict"""
        result = self.__dict_datetime_obj_to_str(result)
        return count, result

    def select_many(self, sql, param=()):
        count = self.__execute(sql, param)
        result = self._cursor.fetchall()
        """:type result:list"""
        [self.__dict_datetime_obj_to_str(row_dict) for row_dict in result]
        return count, result

    def insert_one(self, sql, param):
        count = self.__execute(sql, param)
        id = self._cursor.lastrowid  # 最后插入行的主键id
        self._conn.commit()
        return count, id

    def delete_one(self, sql, param):
        count = self.__execute(sql, param)
        self._conn.commit()
        return count


if __name__ == "__main__":
    mc = MysqlClient()

    # 查询一条数据
    # sql1 = 'select d.url as url,s.source as source,s.version as version from distributed_schedul_url d left join  site_source  s on d.site_source_id=s.id where s.source=%s and s.version = %s order by d.id limit 1;'
    # param = (1, 20201027)
    # result = mc.select_one(sql1,param)
    # print("Total:",result[0]) # 返回总条数
    # print("res.url:", result[1].get("url"))
    # print("res:", result[1])

    # 查询一条记录后通过id删除该条数据，删除成功进行消费，删除失败再换一次查询一次操作
    # sql4 = "delete from distributed_schedul_url where id = %s"
    # param = (1)
    # result = mc.delete_one(sql4, param)
    # print("delete success count:", result)

    # 增加一条数据
    sql3 = "insert into distributed_schedul_url(site_source_id,url) VALUE (%s,%s)"
    param = (1, "www.baidu.com/id=8")
    count, id = mc.insert_one(sql3, param)
    print("insert success count:", count, ', id:', id)

    # 查询多条数据
    # sql2 = 'SELECT * FROM distributed_schedul_url  WHERE  id IN (%s,%s,%s)'
    # param = (1, 2, 3)
    # print(json.dumps(mc.select_many(sql2, param)[1], ensure_ascii=False))
