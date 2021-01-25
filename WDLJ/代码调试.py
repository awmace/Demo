# import os, time, MySQLdb
#
# conn = MySQLdb.connect(
#     host='47.113.200.109',
#     # mysql所在主机的ip
#     port=33063,  # mysql的端口号
#     user="aiit",  # mysql 用户名
#     password="aiit9876",  # mysql 的密码
#     db="hx_sales",  # 要使用的库名
#     charset="utf8"  # 连接中使用的字符集
# )
# p_crate_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
# cursor = conn.cursor()
# sql = 'select *from goods limit 10;'
# cursor.execute(sql)
# data = cursor.fetchone()
# print(data)
# -*- coding: utf-8 -*-

# Define your item.get pipelines here
#
# Don't forget to add your pipeline to the ITEM.get_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item.get-pipeline.html
import json, time

import MySQLdb
import requests
from itemadapter import ItemAdapter

conn = MySQLdb.connect(
    host='47.113.200.109',
    # mysql所在主机的ip
    port=33063,  # mysql的端口号
    user="aiit",  # mysql 用户名
    password="aiit9876",  # mysql 的密码
    db="hx_sales",  # 要使用的库名
    charset="utf8"  # 连接中使用的字符集
)
# url = 'http://47.113.195.31:3012/digital-oc/subject/34/object/list/'
# header = {'Content-Type': 'application/json'}  # 请求头
# table_id1 = 27
# table_id2 = 28
# old_time = int(time.time()) - 86400*15
# version = time.strftime('%Y%m%d', time.localtime(old_time))
# old_create_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(old_time))
# product_item = {
#     'ROW': str(table_id2) + '_' + version,  # 对象ID str
#     'amount': '',  # 数据量 int
#     'incremental': '',  # 增量 int
#     'caeate_time': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(old_time)),  # 创建时间 data
#     'table_id': table_id2,  # 主题id int  27,28
#     'weeks_logo': None,  # 周标识 int
#     'introduce': None  # 周介绍 str '2021-01-04至2021-01-08'
# }
# data1 = json.dumps([product_item], indent=2, ensure_ascii=False)  # 已经处理的数据
# res1 = requests.post(url, data=data1.encode('utf-8'), headers=header)
# print(res1.status_code)

# # 传入hbase
# li = [{'ROW': '1', 'site_id': 1, 'site_name': '采材宝'}, {'ROW': '2', 'site_id': 2, 'site_name': '找钢网'},
#       {'ROW': '3', 'site_id': 3, 'site_name': '慧聪网'}, {'ROW': '4', 'site_id': 4, 'site_name': '云筑优选'},
#       {'ROW': '5', 'site_id': 5, 'site_name': '1688'}, {'ROW': '6', 'site_id': 6, 'site_name': '建材在线'},
#       {'ROW': '7', 'site_id': 7, 'site_name': '五阿哥'}, {'ROW': '8', 'site_id': 8, 'site_name': '特乐意'},
#       {'ROW': '9', 'site_id': 9, 'site_name': '河姆渡'}, {'ROW': '10', 'site_id': 10, 'site_name': '材料网'}]
# li = []
# for i in range(10):
#     d = dict()
#     d['ROW'] = input('请输入ROW:')
#     d['site_id'] = int(input('请输入网站id:'))
#     d['site_name'] = input('请输入网站名称:')
#     li.append(d)
# url = 'http://47.113.195.31:3012/digital-oc/subject/36/object/list/'
# header = {'Content-Type': 'application/json'}  # 请求头
# data1 = json.dumps(li, ensure_ascii=False)  # 已经处理的数据
# res1 = requests.post(url, data=data1.encode('utf-8'), headers=header)
# print(res1.status_code)
