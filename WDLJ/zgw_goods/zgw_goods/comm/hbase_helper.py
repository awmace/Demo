import happybase
import hashlib

class HbaseClient(object):
    """
     :param str name:table name
     :param str row: the row key
     :param list_or_tuple columns: list of columns (optional)
    """
    def __init__(self,host,port):
        self.conn = happybase.Connection(host, port=port)
        self.conn.open()

    def close(self):
        self.conn.close()

    #显示hbase中的列表
    def list_tables(self):
        tabels = self.conn.tables()
        self.conn.close()
        return tabels

    #返回具体列表名
    def table(self, name):
        table = self.conn.table(name)
        return table

    #创建数据表
    def creat(self, name, kw):
        """
        :param name: str
        :param kw: dict
        exp:
            kw = {"":dict()}
        :return: None
        """
        self.conn.create_table(name, kw)

    #删除数据表
    def delete(self, name, row):
        table = self.table(name)
        table.delete(row)

    #删除某表某行某列的数据
    def delete_column(self, name, row, columns):
        self.table(name).delete(row, columns=columns)

    #删除数据表
    def drop(self, name):
        self.conn.disable_table(name)
        self.conn.delete_table(name)

    #获取具体表的具体某项数据 return: list
    def cell(self, name, row, column):
        return self.table(name).cells(row, column)

    #查看某表属于哪个列族return: dict
    def families(self, name):
        return self.conn.table(name).families()

    #向某个表增加某条数据
    # def put(self, name, row, kw):
    #     self.table(name).put(row, kw)
    def put(self, name, rowkey, contents):
        self.table(name).put(rowkey, contents)

    #获取某表某行数据 return: dict
    def get(self, name, row):
        return self.table(name).row(row)

    # 获取某表某行某列具体数据 return: dict
    def get_column(self, name, row, columns):
        return self.table(name).row(row, columns)


