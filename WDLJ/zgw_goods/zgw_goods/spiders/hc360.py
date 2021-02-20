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
from scrapy.utils.project import get_project_settings
from ..comm.dao import UseSQL
from ..useragents import USER_AGENTS
from ..comm.upload_picture import UploadPic
from ..comm.get_week_one import get_current_week
settings = get_project_settings()

logger = logging.getLogger(__name__)


class Hc360Spider(scrapy.Spider):
    name = 'hc360'
    start_urls = ['http://hc360.com/']
    key_words = ['钢材']

    def __init__(self):
        self.own_id = '3'
        self.dao = UseSQL(int(self.own_id))
        self.version = get_current_week()
        self.sku_id = '1'
        self.source_name = '慧聪网'
        self.u = UploadPic()

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
                url, category = url.split('_')
                res = self.dao.delete_url_by_id(id)
                if res:
                    logger.info("delete success count:" + str(result))
                    yield Request(url, callback=self.parse_list, meta={'category': category})
                else:
                    logger.info('其他消费者消费了数据：' + str(url))

    def parse_list(self, response):
        # 提取详情页地址
        url_list = response.url
        detail_url = response.xpath('//div[@class="picmid pRel"]/a/@href').extract()
        for url in detail_url:
            url = 'https:' + url
            yield Request(url, callback=self.parse_detail,
                          meta={'url_list': url_list, 'category': response.meta['category']})

    def parse_detail(self, response):
        category = response.meta['category']
        product_item = ZgwGoodsItem()
        product_id = re.search(r'/(\d*).html', response.url).group(1)
        product_item['p_id'] = self.own_id + '_' + product_id + '_' + self.sku_id
        product_item['spu_id'] = self.own_id + '_' + product_id
        product_item['sku_id'] = self.own_id + '_' + self.sku_id
        product_item['p_three_category'] = category
        product_item['category'] = category
        product_item['source_name'] = self.source_name
        customer_url = response.xpath('//div[@class="itemName"]/a/@href').extract_first()
        customer_id = re.search(r'https://(.*).b2b.hc360.com', customer_url).group(1)
        p_attribute = response.xpath("//div[@class='d-vopy  parameter ']//li/span/text()").extract()
        p_attribute_value = response.xpath("//div[@class='d-vopy  parameter ']//li/p/text()").extract()
        desc_dict = dict(zip(p_attribute, p_attribute_value))
        if '品牌' in desc_dict:
            product_item['p_brand_name'] = desc_dict['品牌']
            del desc_dict['品牌']
        else:
            product_item['p_brand_name'] = desc_dict.get('类型')
        product_item['p_attribute'] = str([i for i in desc_dict]).replace("'", "\"")
        product_item['p_attribute_value'] = str(desc_dict).replace("'", "\"")
        product_item['p_other_info'] = str(desc_dict).replace("'", "\"")
        product_item['p_customer_id'] = self.own_id + '_' + customer_id
        product_item['p_sku_url'] = response.url
        product_item['p_list_url'] = response.meta['url_list']
        product_item['p_customer_name'] = response.xpath('//div[@class="itemName"]/a/@title').extract_first()
        product_item['p_spu_name'] = response.xpath('//h1/text()').extract_first()
        # product_item['p_brand_name'] = response.xpath('//div[@class="itemName"]/a/@title').extract_first()
        unit_all = response.xpath("//span[@class='supply-numb']/text()").extract_first()
        product_item['p_sku_valuation_unit'] = re.search(r'\d*\s*(.*)', str(unit_all)).group(1)
        product_item['p_sku_auxiliary_unit'] = ''
        product_item['p_sku_auxiliary_num'] = ''
        product_item['p_sku_packaging_method'] = ''
        # product_item['p_sku_pic'] = response.xpath("//div[@class='zoomPad']/img/@src").extract_first()
        # "bigPicUrl": "//img002.hc360.cn/k3/M00/E6/67/M27030eb9a5f1c83c6b2912D1f43f4e87b.jpg", "brandName
        p_spu_pic = re.findall(r'bigPicUrl":"(.*)","brandName', response.text)
        if p_spu_pic:
            p_spu_pic = [i if 'http' in i else 'http:' + i for i in p_spu_pic]
            product_item['p_spu_pic'] = self.u.generate(p_spu_pic[0])
            product_item['p_sku_pic'] = self.u.generate(p_spu_pic)
        product_item['p_sku_introduce_type'] = 2
        introduce_list = response.xpath("//div[@id='introduce']//text()").extract()
        if introduce_list:
            intro_new = [re.sub('\s*', '', i) for i in introduce_list]
            introduce_str = ','.join(intro_new)
        else:
            introduce_str = ''
        product_item['p_sku_introduce'] = introduce_str
        price_num = response.xpath("//tr[@class='item-cur-tab']/td[1]/text()").extract_first()
        if price_num:
            p_price_num = re.search(r'\d+(.\d+)?', price_num).group()
            if '-' in p_price_num:
                product_item['p_price_num'] = float(p_price_num.split('-')[0])
            else:
                product_item['p_price_num'] = float(re.search(r'\d+(.\d+)?', price_num).group())
        else:
            product_item['p_price_num'] = None
        try:
            price = response.xpath("//div[@class='topPriceRig']/text()").extract()[-1]
        except Exception as e:
            print(str(e))
            price = None
        if price:
            price_str = re.sub('\s*', '', price)
            try:
                price_str = re.findall(r'¥?(\d*\.*\d*)', price_str)
                price_str = list(filter(None, price_str))
                price_str = price_str[-1]
            except Exception as e:
                print(str(e))
        else:
            pass
        product_item['p_price'] = float(price_str)
        product_item['p_source'] = int(self.own_id)
        product_item['p_version'] = self.version
        product_item['p_create_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        product_item['p_deleted'] = 0
        customer_url = 'https://{}.b2b.hc360.com/shop/show.html'.format(customer_id)
        product_item['c_customer_url'] = 'https://{}.b2b.hc360.com/shop/show.html'.format(customer_id)
        product_item = self.get_customer(customer_url, product_item)
        if product_item.get('c_customer_phone'):
            product_item['vandream_flag'] = 1
        else:
            product_item['vandream_flag'] = 0
        product_item['customer_follow_state'] = 0
        yield product_item

    def get_customer(self, url, product_item):
        # 获取公司消息
        r = requests.get(url)
        tree = html.fromstring(r.text)
        product_item['c_deleted'] = 0
        product_item['c_customer_introduce_type'] = 2
        product_item['c_source'] = int(self.own_id)
        product_item['c_version'] = self.version
        product_item['c_create_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        enterprise_scope = str(tree.xpath("//a[@style='font-family: ']/text()")).replace("'", "\"")
        product_item['c_enterprise_scope'] = str(enterprise_scope)
        customer_introduce = str(tree.xpath("//p[@style='font-size:16px']/text()"))
        product_item['c_customer_introduce'] = customer_introduce.replace("'", "\"")
        # 获取联系方式  //div[@node-name='mp']
        phone_url = url.replace('show', 'company')
        UserAgent = random.choice(USER_AGENTS)
        headers = {'User-Agent': UserAgent}
        r = requests.get(phone_url, headers=headers)
        tree = html.fromstring(r.text)
        phone_number = tree.xpath("//div[@node-name='mp']")
        address = tree.xpath(
            "//div[@class='con3Left']/span[contains(text(), '地址')]/../following-sibling::div[1]/text()")
        if address:
            product_item['c_customer_address'] = address[0]
        else:
            product_item['c_customer_address'] = None
        if phone_number:
            product_item['c_customer_phone'] = phone_number[0].text
        else:
            product_item['c_customer_phone'] = None
        product_item['c_other_info'] = ''
        return product_item


if __name__ == '__main__':
    os.system('scrapy crawl hc360')
