import logging
from ..comm.mysql_helper import MysqlClient
from scrapy.utils.project import get_project_settings

settings = get_project_settings()
logger = logging.getLogger(__name__)


class UseSQL:

    def __init__(self, own_id):
        self.mc = MysqlClient()
        self.version = settings['VERSION']
        self.source_table = 'site_source'
        self.url_table = 'distributed_schedul_url'
        # 网站唯一识别ID
        self.own_id = own_id
        self.param = (int(own_id), settings['VERSION'],)
    # 判断此站点是否开始生产
    def get_product(self):
        try:
            result = None
            sql = 'select d.id as id,' \
                  'd.url as url,' \
                  's.source as source,' \
                  's.version as version ' \
                  'from {url_table} d ' \
                  'left join {source_table} s ' \
                  'on d.site_source_id=s.id ' \
                  'where s.source=%s ' \
                  'and s.version = %s ' \
                  'order by d.id limit 1;'.format(url_table=self.url_table, source_table=self.source_table)
            # print(sql)
            result = self.mc.select_one(sql, self.param)
        except Exception as e:
            logger.error('dao.get_product wrong:' + str(e))
        finally:
            return result

    # 成为生产者
    def tobe_product(self):
        try:
            count, table_id = None, None
            sql = "insert into {source_table}(source,version) VALUE (%s,%s)".format(source_table=self.source_table)
            count, table_id = self.mc.insert_one(sql, self.param)
            logger.info("insert success count:" + str(count))
        except Exception as e:
            logger.error('dao.tobe_product wrong:' + str(e))
        finally:
            return count, table_id

    # 插入url到消费队列
    def insert_url_by_id(self, table_id, url):
        try:
            result = None
            sql = "insert into {url_table}(site_source_id,url) VALUE (%s,%s)".format(url_table=self.url_table)
            param = (table_id, str(url),)
            count, table_id = self.mc.insert_one(sql, param)
            logger.info("insert success count:" + str(count))
        except Exception as e:
            logger.error('dao.insert_url_by_id wrong:' + str(e))
        finally:
            return result

    # 消费url
    def delete_url_by_id(self, id):
        try:
            result = None
            sql = "delete from {url_table} where id = %s".format(url_table=self.url_table)
            param = (id)
            result = self.mc.delete_one(sql, param)
            logger.info("delete success count:" + str(result))
        except Exception as e:
            logger.error('dao.delete_url_by_id wrong:' + str(e))
        finally:
            return result


if __name__ == '__main__':
    use = UseSQL(9)
    use.delete_url_by_id()
