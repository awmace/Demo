# -*- coding: utf-8 -*-

# Define your item.get pipelines here
#
# Don't forget to add your pipeline to the ITEM.get_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item.get-pipeline.html
import json

import MySQLdb
import requests
from itemadapter import ItemAdapter

conn1 = MySQLdb.connect(
    host='47.113.200.109',
    # mysql所在主机的ip
    port=33063,  # mysql的端口号
    user="aiit",  # mysql 用户名
    password="aiit9876",  # mysql 的密码
    db="hx_sales",  # 要使用的库名
    charset="utf8"  # 连接中使用的字符集
)
conn2 = MySQLdb.connect(
    host='101.68.94.251',
    # mysql所在主机的ip
    port=3308,  # mysql的端口号
    user="beixin",  # mysql 用户名
    password="SXki89_23@4$3i8s",  # mysql 的密码
    db="b2b_product_house",  # 要使用的库名
    charset="utf8"  # 连接中使用的字符集
)
cursor = conn1.cursor()
cursor_wj = conn2.cursor()

p_url = 'http://47.113.195.31:3012/digital-oc/subject/27/object/list/'
c_url = 'http://47.113.195.31:3012/digital-oc/subject/28/object/list/'
header = {'Content-Type': 'application/json'}  # 请求头


class ZgwGoodsPipeline(object):
    def __init__(self):
        self.count = 0
        self.products = []
        self.customers = []

    def process_item(self, item, spider):
        sql_data = {
            'pid': item.get('p_id'),  # 商品唯一id
            'shop_info': item.get('p_customer_name'),  # 店铺名称
            'category_full_name': item.get('category'),  # 全类目名称
            'p_source': item.get('p_source'),  # 网站id
            'deleted': item.get('p_deleted'),  # 删除标识:0代表未删除，1代表删除
            'version': item.get('p_version'),  # 数据版本号
            'product_info': json.dumps({
                'spu_id': item.get('spu_id'),  # spu_id
                'sku_id': item.get('sku_id'),  # sku_id
                'sku_url': item.get('p_sku_url'),  # 详情页url
                'spu_name': item.get('p_spu_name'),  # 商品名称
                'spu_pic': item.get('p_spu_pic'),  # spu产品图片地址
                'list_url': item.get('p_list_url'),  # 商品所在列表页url
                'three_category_code': item.get('p_three_category'),  # 商品所属三级类目名称
                'brand_name': item.get('p_brand_name'),  # 商品所属品牌名称
                'sku_valuation_unit': item.get('p_sku_valuation_unit'),  # 商品计量单位
                'attribute': item.get('p_attribute'),  # 属性
                'attribute_value': item.get('p_attribute_value'),  # 属性值
                'sku_pic': item.get('p_sku_pic'),  # sku图片地址
                'sku_introduce_type': item.get('p_sku_introduce_type'),  # sku介绍方式:1图片2文字3图片+文字
                'sku_introduce': item.get('p_sku_introduce'),  # 文字介绍
                'sku_introduce_pic': item.get('p_sku_introduce_pic'),
                'price_num': item.get('p_price_num'),  # 起订量
                'price': item.get('p_price'),  # 价格
                'other_info': item.get('p_other_info'),  # 商品其他信息
                'source_name': item.get('source_name'),
                'enterprise_scope': item.get('c_enterprise_scope'),  # 企业经营范围/主营业务
                'customer_introduce_type': item.get('c_customer_introduce_type'),  # 企业介绍方式:1图片2文字3文字+图片
                'customer_introduce': item.get('c_customer_introduce'),  # 企业简介
                'customer_introduce_pic': item.get('c_customer_introduce_pic'),
                'customer_address': item.get('c_customer_address'),  # 企业注册地址
                'customer_number': item.get('c_customer_number'),  # 座机
                'customer_phone': item.get('c_customer_phone'),  # 手机号
                'customer_url': item.get('c_customer_url'),
                'cid': item.get('p_customer_id'),  # 店铺在网站中的id
                'vandream_flag': item.get('vandream_flag')
            })  # 商品与店铺信息
        }
        data_key = list(sql_data.keys())
        data_value = list(sql_data.values())
        insert_sql = 'insert into product_house_info (' + ','.join(data_key) + ') values (' + ','.join(
            '%r' % i for i in data_value) + ')'
        if spider.name not in ['zgw', 'wuage']:
            try:
                cursor.execute(insert_sql)
            except Exception as e:
                print(e, '错误在{}'.format(spider.name))
            conn1.commit()
        else:
            try:
                cursor_wj.execute(insert_sql)
                self.count += 1
                print(spider.name, self.count)
            except Exception as e:
                print(e, '错误在{}'.format(spider.name))
            conn2.commit()
        product_item = {
            'ROW': item.get('p_id'),  # 商品在目标网站中的唯一标识
            'spu_id': item.get('spu_id'),  #
            'sku_id': item.get('sku_id'),
            'sku_url': item.get('p_sku_url'),  # 详情页url
            'customer_name': item.get('p_customer_name'),  # 店铺名称
            'spu_code': item.get('p_spu_code'),  # spu编码
            'spu_name': item.get('p_spu_name'),  # 商品名称
            'spu_pic': item.get('p_spu_pic'),  # spu产品图片地址
            'sku_pic': item.get('p_sku_pic'),  # sku图片地址
            'list_url': item.get('p_list_url'),  # 商品所在列表页url
            'three_category_code': item.get('p_three_category'),  # 商品所属三级类目名称
            'category': item.get('category'),
            'brand_name': item.get('p_brand_name'),  # 商品所属品牌名称
            'sku_valuation_unit': item.get('p_sku_valuation_unit'),  # 商品计量单位
            'sku_auxiliary_unit': item.get('p_sku_auxiliary_unit'),  # 辅助单位
            'sku_auxiliary_num': item.get('p_sku_auxiliary_num'),  # 辅助单位数量
            'sku_packaging_method': item.get('p_sku_packaging_method'),  # 包装方式
            'attribute': item.get('p_attribute'),  # 属性
            'attribute_value': item.get('p_attribute_value'),  # 属性值
            'sku_introduce_type': item.get('p_sku_introduce_type'),  # sku介绍方式:1图片2文字3图片+文字
            'sku_introduce': item.get('p_sku_introduce'),  # 文字介绍
            'sku_introduce_pic': item.get('p_sku_introduce_pic'),
            'price_num': item.get('p_price_num'),  # 起订量
            'price': item.get('p_price'),  # 价格
            'other_info': item.get('p_other_info'),  # 商品其他信息
            'source': item.get('p_source'),  # 数据来源网站id
            'source_name': item.get('source_name'),
            'version': item.get('p_version'),  # 数据版本号
            'create_time': item.get('p_create_time'),  # 创建时间
            'deleted': item.get('p_deleted'),  # 删除标识:0代表未删除，1代表删除
            'vandream_flag': item.get('vandream_flag')
        }
        customer_item = {
            'ROW': item.get('p_customer_id'),  # 店铺在网站中的唯一标识
            'customer_name': item.get('p_customer_name'),  # 店铺名称
            'enterprise_scope': item.get('c_enterprise_scope'),  # 企业经营范围/主营业务
            'customer_introduce_type': item.get('c_customer_introduce_type'),  # 企业介绍方式:1图片2文字3文字+图片
            'customer_introduce': item.get('c_customer_introduce'),  # 企业简介
            'customer_introduce_pic': item.get('c_customer_introduce_pic'),
            'customer_address': item.get('c_customer_address'),  # 企业注册地址
            'customer_number': item.get('c_customer_number'),  # 座机
            'customer_phone': item.get('c_customer_phone'),  # 手机号
            'customer_url': item.get('c_customer_url'),  # 店铺url
            'other_info': item.get('c_other_info'),  # 其他信息
            'source': item.get('p_source'),  # 数据来源网站id
            'version': item.get('p_version'),  # 数据版本号
            'create_time': item.get('p_create_time'),  # 创建时间
            'deleted': item.get('p_deleted'),  # 删除标识0代表未删除1代表已删除
            'customer_follow_state': 0  # 跟进状态
        }
        self.products.append(product_item)
        if customer_item not in self.customers:
            self.customers.append(customer_item)
        if len(self.products) > 19:
            # 传入hbase
            data1 = json.dumps(self.products, indent=2, ensure_ascii=False)  # 已经处理的数据
            res1 = requests.post(p_url, data=data1.encode('utf-8'), headers=header)
            data2 = json.dumps(self.customers, indent=2, ensure_ascii=False)  # 已经处理的数据
            res2 = requests.post(c_url, data=data2.encode('utf-8'), headers=header)
            # 清空列表
            print(res1.text, res2.status_code)  # 推送状态码
            self.products = []
            self.customers = []


def close_spider(self, spider):
    if self.products or self.customers:
        data1 = json.dumps(self.products, indent=2, ensure_ascii=False)  # 已经处理的数据
        res1 = requests.post(p_url, data=data1.encode('utf-8'), headers=header)
        data2 = json.dumps(self.customers, indent=2, ensure_ascii=False)  # 已经处理的数据
        res2 = requests.post(c_url, data=data2.encode('utf-8'), headers=header)
        # 清空列表
        print(res1.status_code, res2.status_code)  # 推送状态码
        self.products = []
        self.customers = []
        print("最后一次推送入库！！！")

# insert_sql = 'insert into product_house_info(pid,shop_info,category_full_name,p_source,follow_status,deleted,version,product_info) values(%s,%s,%s,%s,%s,%s,%s,%s)'
# cursor.execute(insert_sql,
#                [pid, shop_info, category_full_name, p_source, follow_status, deleted, version, product_info])
# def process_item(self, item, spider):
#     data_key = list(item.keys())
#     data_value = list(item.values())
#     insert_sql = 'insert into goods (' + ','.join(data_key) + ') values (' + ','.join(
#         '%r' % i for i in data_value) + ')'
#     update_sql = 'update goods set ' + ','.join(
#         [i + '=%s' for i in data_key if i != 'p_id']) + ' where p_id=%s;'
#     try:
#         cursor.execute(insert_sql)
#     except:
#         cursor.execute(update_sql, data_value[1:] + [data_value[0]])
#     conn.commit()
#     return item
