# -*- coding: utf-8 -*-
import json, requests
import re
from urllib import parse
import logging
import re
import math
import MySQLdb
import scrapy, time
from lxml import etree
from ..items import ZgwGoodsItem
from ..comm.dao import UseSQL
from scrapy.utils.project import get_project_settings
from ..comm.upload_picture import UploadPic
from ..comm.get_week_one import get_current_week

settings = get_project_settings()
logger = logging.getLogger(__name__)


class save_ClwSpider(scrapy.Spider):
    name = 'clw_url'

    def __init__(self):
        self.source = 10
        self.version = time.strftime('%Y%m%d', time.localtime(time.time()))
        self.user = UseSQL(self.source)
        self.table_id = None

    def start_requests(self):
        result = self.user.get_product()
        if result[1] != None:
            logger.info(str(self.source) + '站点，已经存在生产者')
        else:
            count, self.table_id = self.user.tobe_product()
            url = 'http://cailiao.com/tradeinfo/'
            yield scrapy.Request(url, callback=self.categorys)

    def categorys(self, response):
        ele_response = etree.HTML(response.text)
        three_cate_urls = ele_response.xpath('//div[@class="list-des"]/div/div[@class="content"]/a/@href')
        for url in three_cate_urls:
            time.sleep(0.25)
            yield scrapy.Request(url, callback=self.save_list_url, meta={'url': url})

    def save_list_url(self, response):
        ele_response = etree.HTML(response.text)
        url = response.meta['url']
        cate_name = url.split('//')[-1].split('.')[0]
        pages = ele_response.xpath('//span[@class="txt"]/text()')
        if pages:
            pages = pages[0].split()[1]
            for page in range(1, int(pages) + 1):
                list_url = url + '/?name={}&__domain__={}&page={}'.format(cate_name, cate_name, page)
                self.user.insert_url_by_id(self.table_id, list_url)
        else:
            self.user.insert_url_by_id(self.table_id, url)


class ClwSpider(scrapy.Spider):
    name = 'clw'

    def __init__(self):
        self.counts = 0
        self.source = 10
        self.source_name = '材料网'
        self.sku_id = 1
        self.version = get_current_week()
        self.user = UseSQL(self.source)
        self.u = UploadPic()

    def start_requests(self):
        while True:  # 循环获取列表页url
            result = self.user.get_product()
            if result[1] == None:
                break
            else:
                # 删除此条记录
                id = result[1].get('id')  # 表中id,根据表中id删除数据
                p_list_url = result[1].get('url')
                list_page_data = {'p_list_url': p_list_url}
                res = self.user.delete_url_by_id(id)  # 根据id删除表中数据
                if res:
                    logger.info("delete success count:" + str(result))
                    yield scrapy.FormRequest(p_list_url, callback=self.parse, meta={'list_page_data': list_page_data})
                else:
                    logger.info('其它消费者消费了数据:' + str(p_list_url))

    def parse(self, response):
        list_page_data = response.meta['list_page_data']
        ele_response = etree.HTML(response.text)
        category = '>>'.join(ele_response.xpath('//a[@class="c99"]/text()')[1:])
        p_three_category = category.split('>>')[-1]
        list_page_data['category'] = category
        list_page_data['p_three_category'] = p_three_category
        li_url = ele_response.xpath('//a[@class="suport-imgbox"]/@href')
        spu_names = ele_response.xpath('//div[@class="suport-des"]/text()')
        for index, url in enumerate(li_url):
            data = ZgwGoodsItem()
            spu_id = url[:-5].split('/')[-1]
            data['p_id'] = str(self.source) + '_' + spu_id + "_" + str(self.sku_id)
            data['spu_id'] = spu_id
            data['sku_id'] = self.sku_id
            data["p_spu_name"] = spu_names[index]
            data['p_source'] = self.source  # 来源网站id
            data['p_version'] = self.version  # 数据版本号
            data['source_name'] = self.source_name
            data['p_deleted'] = 0  # 删除标识，0代表未删除，1代表删除
            data['category'] = category
            data['p_three_category'] = p_three_category
            data['p_sku_url'] = url
            data.update(list_page_data)
            yield scrapy.Request(url, callback=self.detail, meta={'data': data})
            time.sleep(0.30)

    def detail(self, response):
        ele_response = etree.HTML(response.text)
        data = response.meta['data']
        data['p_spu_pic'] = ele_response.xpath('//a[@class="jqzoom"]/img/@src')
        if data['p_spu_pic']:
            data['p_spu_pic'] = self.u.generate(data['p_spu_pic'][0])  # 图片处理
            data['p_sku_pic'] = self.u.generate(ele_response.xpath('//a[@class="jqzoom"]/img/@src'))
            try:  # 分支
                data['p_sku_introduce'] = ''.join(
                    [i.strip() for i in ele_response.xpath('//p[@class="ql-align-justify"]/..//text()')])
                data['p_sku_introduce_pic'] = self.u.generate(ele_response.xpath('//div[@class="box"]//img/@src'))
                data['p_price'] = ele_response.xpath('//div[@class="table-r-col1"]/div[last()]/text()')
                if data['p_price']:
                    data['p_price'] = data['p_price'][-1]
                    quantity_unit = ele_response.xpath('//div[@class="table-r-col1"]/div[last()]/text()')[0]
                    data['p_price_num'] = re.findall('\d{1,3}', quantity_unit)[0]
                    data['p_sku_valuation_unit'] = re.findall('[一-龟]', quantity_unit)
                    if data['p_sku_valuation_unit']:
                        data['p_sku_valuation_unit'] = data['p_sku_valuation_unit'][0]
                    else:
                        data['p_sku_valuation_unit'] = re.findall('([a-zA-Z]+)', quantity_unit)
                else:
                    quantity_unit = ele_response.xpath('//span[@class="row2-val"]/text()')
                    data['p_price'] = quantity_unit[0][:-1]
                    data['p_price_num'] = 1
                    data['p_sku_valuation_unit'] = re.findall('[一-龟]', quantity_unit[-1])
                    if data['p_sku_valuation_unit']:
                        data['p_sku_valuation_unit'] = data['p_sku_valuation_unit'][0]
                    else:
                        data['p_sku_valuation_unit'] = re.findall('([a-zA-Z]+)', quantity_unit[-1])
                data['c_customer_address'] = ele_response.xpath(
                    '//div[@class="col-m-row4 clearfix addborder"]/div[last()]/text()')[0]
                data['p_customer_name'] = ele_response.xpath('//div[@class="shop-name"]/text()')[0]
                data['c_customer_number'] = None
                data['c_customer_phone'] = ele_response.xpath('//div[@class="object-row m-t-15"]/span[last()]/text()')[
                    0]
                data['c_enterprise_scope'] = \
                    ele_response.xpath('//div[@class="object-row m-t-15"]/span[last()]/text()')[-1]
                data['c_customer_url'] = ele_response.xpath('//a[@class="toshop"]/@href')[0]
                data['p_customer_id'] = str(self.source) + '_' + \
                                        re.findall('http://(.*?).cailiao.com', data['c_customer_url'], re.S)[0]
                data['p_attribute'] = ele_response.xpath('//div[@class="table-row"]/span[@class="table-key"]/text()')
                key_values = dict()
                for i in range(len(data['p_attribute'])):
                    value = ele_response.xpath(
                        '//div[@class="detail-content clearfix"]/div[{}]/span[@class="table-val"]/text()'.format(i + 1))
                    key_values[data['p_attribute'][i]] = value[0] if value else None
                data['p_brand_name'] = key_values.get('品牌')
                data['p_attribute_value'] = json.dumps(key_values, ensure_ascii=False)  # 转json
                data['p_attribute'] = json.dumps(data['p_attribute'], ensure_ascii=False)  # 转json

            except:
                data['p_sku_introduce'] = ''.join(
                    [i.strip() for i in ele_response.xpath('//div[@class="img-box"]//text()')])
                data['p_sku_introduce_pic'] = self.u.generate(ele_response.xpath('//div[@class="img-box"]//img/@src'))
                data['p_price'] = ele_response.xpath('//span[@class="price same same1"]/text()')[0]
                try:
                    data['p_price'] = float(data['p_price'])
                except:
                    data['p_price'] = float(0)
                quantity_unit = ele_response.xpath('//span[@class="same same2"]/text()')[0]
                data['p_price_num'] = 1
                data['p_sku_valuation_unit'] = re.findall('[一-龟]', quantity_unit)
                if data['p_sku_valuation_unit']:
                    data['p_sku_valuation_unit'] = data['p_sku_valuation_unit'][0]
                else:
                    data['p_sku_valuation_unit'] = re.findall('([a-zA-Z]+)', quantity_unit)
                    if data['p_sku_valuation_unit']:
                        data['p_sku_valuation_unit'] = data['p_sku_valuation_unit'][0]
                    else:
                        data['p_sku_valuation_unit'] = '个'
                data['c_customer_address'] = ele_response.xpath('//span[@class="same same4"]/text()')[0]
                data['p_customer_name'] = ele_response.xpath('//div[@class="info"]/p[@class="name"]/text()')[0]
                data['c_customer_phone'] = ele_response.xpath('//p[@class="row3 row"]/span[@class="color"]/text()')[0]
                data['c_customer_number'] = None
                data['c_enterprise_scope'] = ele_response.xpath('//p[@class="row7 row"]/span[last()]/text()')[0]
                data['c_customer_url'] = ele_response.xpath('//a[@class="shop"]/@href')[0]
                data['p_customer_id'] = str(self.source) + '_' + \
                                        re.findall('http://(.*?).cailiao.com', data['c_customer_url'], re.S)[0]
                address = ele_response.xpath('//p[@class="row6 row"]/span[last()]/text()')
                if address:
                    data['c_customer_address'] = address[0]
                data['p_attribute'] = ele_response.xpath('//div[@class="table"]/div[@class="t-l"]/text()')
                key_values = dict()
                for index, key in enumerate(data['p_attribute']):
                    if ' :' in key:
                        key = key[:-2]
                        data['p_attribute'][index] = key
                    value = ele_response.xpath('//div[@class="table"]/div[{}]/text()'.format(index + 1))
                    key_values[key] = value[0] if value else None
                data['p_brand_name'] = key_values.get('品牌')
                data['p_attribute_value'] = json.dumps(key_values)
                data['p_attribute'] = json.dumps(data['p_attribute'])
            if data['c_customer_phone'] and data['c_customer_address']:
                data['vandream_flag'] = 1
            else:
                data['vandream_flag'] = 0
            data['customer_follow_state'] = 0
            data['c_customer_introduce_type'] = 0
            if data['p_sku_introduce_pic'] and not data['p_sku_introduce']:
                data['p_sku_introduce_type'] = 1
            elif not data['p_sku_introduce_pic'] and data['p_sku_introduce']:
                data['p_sku_introduce_type'] = 2
            elif data['p_sku_introduce_pic'] and data['p_sku_introduce']:
                data['p_sku_introduce_type'] = 3
            else:
                data['p_sku_introduce_type'] = 0
            yield data
