import os
import re
import time
import logging
import scrapy
import random
import requests
from lxml import html
from datetime import datetime
from scrapy import Request
from ..items import ZgwGoodsItem
from ..comm.upload_picture import UploadPic
from scrapy.utils.project import get_project_settings
from ..comm.dao import UseSQL
from ..comm.get_week_one import get_current_week

settings = get_project_settings()

logger = logging.getLogger(__name__)


class WuageSpider(scrapy.Spider):
    name = 'wuage'
    # allowed_domains = ['hc360.com']
    start_urls = ['https://www.wuage.com/']
    key_words = ['H型钢']

    def __init__(self):
        self.own_id = '7'
        self.dao = UseSQL(int(self.own_id))
        self.source_name = '五阿哥'
        self.version = get_current_week()
        self.u = UploadPic()
        self.count = 0

    def start_requests(self):
        # 消费url
        while True:
            result = self.dao.get_product()
            if result[1] == None:
                break
            else:
                # 删除此条记录
                id = result[1].get('id')
                url = result[1].get('url')
                res = self.dao.delete_url_by_id(id)
                if res:
                    logger.info("delete success count:" + str(result))
                    yield Request(url, callback=self.parse_list)
                else:
                    logger.info('其他消费者消费了数据：' + str(url))

    def parse_list(self, response):
        # 提取详情页地址
        url_list = response.url
        detail_url = response.xpath("//ul[@class='mod-img fe-row']/li/a[1]/@href").extract()
        for url in detail_url:
            yield Request(url, callback=self.parse_detail, meta={'url_list': url_list})

    def parse_detail(self, response):
        product_item = ZgwGoodsItem()
        # 获取spu_id
        product_id = re.search(r'https://item.wuage.com/(.*).html', response.url).group(1)
        # 获取sku_id
        sku_id_list = response.xpath(
            "//div[@class='sku-main']//div[@class='item-content']//li/div[@class='sku']/@data-id").extract()
        sku_attr_list = response.xpath(
            "//div[@class='sku-main']//div[@class='item-content']//li/div[@class='sku']/@title").extract()
        sku_price_list = response.xpath(
            "//div[@class='sku-main']//div[@class='item-content']//li/div[@class='price']/@title").extract()
        sku_num_list = response.xpath(
            "//div[@class='sku-main']//div[@class='item-content']//li/div[@class='moq']/em/text()").extract()
        product_item['p_spu_name'] = response.xpath('//h1/text()').extract_first()
        # 公司相关信息
        customer_url = 'http:' + response.xpath("//li[@class='top-nav-contactinfo nav-item ']/a/@href").extract_first()
        product_item['p_customer_name'] = response.xpath("//h2[@class='company-name']/text()").extract_first()
        product_item['c_customer_url'] = customer_url
        if customer_url:
            customer_id = re.search(r'shop.wuage.com/(.*)/page/', customer_url).group(1)
        else:
            customer_id = '1000000002'
        product_item['p_customer_id'] = self.own_id + '_' + customer_id
        product_item = self.get_customer(customer_url, product_item)
        for i in range(len(sku_id_list)):
            product_item['p_id'] = self.own_id + '_' + product_id + '_' + sku_id_list[i]
            product_item['spu_id'] = product_id
            product_item['sku_id'] = sku_id_list[i]
            p_attribute = response.xpath("//div[@class='details-body']/ul/li/em/text()").extract()
            p_attribute_value = response.xpath("//div[@class='details-body']/ul/li/span/@title").extract()
            desc_dict = dict(zip(p_attribute, p_attribute_value))
            if '钢厂' in desc_dict:
                product_item['p_brand_name'] = desc_dict['钢厂']
                del desc_dict['钢厂']
            elif '品牌' in desc_dict:
                product_item['p_brand_name'] = desc_dict['品牌']
                del desc_dict['品牌']
            else:
                product_item['p_brand_name'] = None
            product_item['p_three_category'] = desc_dict.get('品名')
            product_item['category'] = product_item['p_three_category']
            product_item['p_attribute'] = str([i for i in desc_dict]).replace("'", "\"")
            product_item['p_attribute_value'] = str(desc_dict).replace("'", "\"")
            product_item['p_other_info'] = str(desc_dict).replace("'", "\"")
            product_item['p_sku_url'] = response.url
            product_item['p_list_url'] = response.meta['url_list']
            product_item['p_spu_code'] = ''
            pic_list = ['http:' + i for i in response.xpath("//div[@class='spec-items']/ul/li/img/@big-img").extract()]
            product_item['p_spu_pic'] = pic_list[0] if pic_list else None
            product_item['p_spu_pic'] = self.u.generate(product_item['p_spu_pic'])
            product_item['p_sku_valuation_unit'] = response.xpath(
                "//strong[@class='price']/following-sibling::em/text()").extract_first().replace('/', '')
            product_item['p_sku_auxiliary_unit'] = None
            product_item['p_sku_auxiliary_num'] = None
            product_item['p_sku_packaging_method'] = None
            product_item['p_sku_pic'] = self.u.generate(pic_list)
            product_item['p_sku_introduce_type'] = 3
            introduce_list = response.xpath("//div[@id='descriptionHtml']//text()").extract()
            if introduce_list:
                intro_new = [re.sub('\s*', '', i) for i in introduce_list]
                introduce_str = ','.join(intro_new)
            else:
                introduce_str = ''
            product_item['p_sku_introduce'] = introduce_str
            product_item['p_sku_introduce_pic'] = ['http:' + i if 'http' not in i else i for i in
                                                   response.xpath('//div[@id="descriptionHtml"]//img/@src').extract()]
            product_item['p_sku_introduce_pic'] = self.u.generate(product_item['p_sku_introduce_pic'])
            product_item['p_price'] = sku_price_list[i]
            product_item['p_price_num'] = sku_num_list[i]
            product_item['p_source'] = int(self.own_id)
            product_item['source_name'] = self.source_name
            product_item['p_version'] = self.version
            product_item['p_create_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            product_item['p_deleted'] = 0
            if product_item['c_customer_phone']:
                product_item['vandream_flag'] = 1
            else:
                product_item['vandream_flag'] = 0
            yield product_item

    def get_customer(self, url, product_item):
        # 获取公司消息
        r = requests.get(url)
        tree = html.fromstring(r.text)
        product_item['c_deleted'] = 0
        product_item['c_customer_introduce_type'] = 2
        product_item['c_source'] = self.own_id
        product_item['c_version'] = self.version
        product_item['c_create_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        product_item['c_enterprise_scope'] = None
        product_item['c_customer_introduce'] = None
        phone_none = str(tree.xpath("//input[@id='contact-m-p']/@value")[0]).replace('mp', '')
        phone_number = str(tree.xpath("//span[@class='mobile-phone mobile-hide']/text()")[0]).replace('****',
                                                                                                      phone_none)
        address = tree.xpath("//div[@class='address']/span[@class='content']/@title")
        if address:
            product_item['c_customer_address'] = str(address[0])
        else:
            product_item['c_customer_address'] = None
        if phone_number:
            product_item['c_customer_phone'] = phone_number
        else:
            product_item['c_customer_phone'] = None
        product_item['c_other_info'] = None
        product_item['customer_follow_state'] = 0
        return product_item

# if __name__ == '__main__':
#     os.system('scrapy crawl wuage')
