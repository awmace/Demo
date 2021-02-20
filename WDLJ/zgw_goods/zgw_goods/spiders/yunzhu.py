import os
import re
import time
import logging
import scrapy
from scrapy import Request
from scrapy.utils.project import get_project_settings
from ..items import ZgwGoodsItem
from ..comm.dao import UseSQL
from ..comm.upload_picture import UploadPic
from ..comm.get_week_one import get_current_week

settings = get_project_settings()

logger = logging.getLogger(__name__)


class YunzhuSpider(scrapy.Spider):
    name = 'yunzhu'
    allowed_domains = ['mro.yzw.cn']
    start_urls = ['http://mro.yzw.cn']
    key_words = ['建筑钢材']

    def __init__(self):
        self.own_id = '4'
        self.source_name = '云筑优选'
        self.u = UploadPic()
        self.dao = UseSQL(int(self.own_id))
        self.version = get_current_week()

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
        # print(response.url)
        # 使用正则获取页面data信息
        url_list = response.url
        res = re.search(r'window.g_initialData = { "/search/product": ({"data":.*) };</script>',
                        str(response.body, encoding='utf-8')).group(1)
        null = None
        true = True
        false = False
        res = eval(res)['data']
        max_page = res['totalPage']
        if max_page == 0:
            max_page = 1
        current_page = res['currentPage']
        # 提取sku_id
        items = res['items'][0]['itemList']
        skuId_list = [item['skuId'] for item in items]
        if skuId_list:
            for skuId in skuId_list:
                detail_url = 'https://mro.yzw.cn/product/' + skuId
                # print(detail_url)
                yield Request(detail_url, callback=self.parse_detail, meta={'url_list': url_list})

    def parse_detail(self, response):
        url_list = response.meta['url_list']
        product_item = ZgwGoodsItem()
        res = re.search(r'window.g_initialData = { "/product.*({"defaultSku":.*) };</script>',
                        str(response.body, encoding='utf-8')).group(1)
        undefined = ''
        null = None
        true = True
        false = False
        res = eval(res)
        sku_list = res['skuList']
        if sku_list:
            for sku in sku_list:
                product_item['p_list_url'] = url_list
                product_item['source_name'] = self.source_name
                product_item['spu_id'] = response.url.split('/')[-1]
                product_item['sku_id'] = sku.get('id')
                product_item['p_id'] = self.own_id + '_' + product_item['spu_id'] + '_' + sku.get('id')
                product_item['p_sku_url'] = 'https://mro.yzw.cn/product/{}'.format(sku.get('id'))
                product_item['p_customer_id'] = self.own_id + '_' + sku.get('brandId')
                product_item['p_customer_name'] = ''
                product_item['p_spu_code'] = ''
                product_item['p_spu_name'] = sku.get('itemName')
                product_item['p_spu_pic'] = sku.get('attachmentModels')[0].get('content')
                product_item['p_spu_pic'] = self.u.generate(product_item['p_spu_pic'])
                product_item['category'] = ';'.join(response.xpath(
                    "(//span[@class='ant-breadcrumb-link']/a/text())[2]").extract())
                product_item['p_three_category'] = response.xpath(
                    "(//span[@class='ant-breadcrumb-link']/a/text())[2]").extract_first()
                product_item['p_brand_name'] = sku.get('brandName')
                product_item['p_sku_valuation_unit'] = response.xpath(
                    "(//div[@class='info-value']/text())[4]").extract_first()
                product_item['p_sku_auxiliary_unit'] = ''
                product_item['p_sku_auxiliary_num'] = ''
                product_item['p_sku_packaging_method'] = ''
                res = response.xpath("//ul[@class='sku-attributes']/li//text()").extract()
                desc_info = {}
                try:
                    for index, item in enumerate(res):
                        if index % 2 == 0:
                            desc_info[item] = res[index + 1]
                except Exception as e:
                    print(str(e))
                print(desc_info)
                if '品牌' in desc_info:
                    del desc_info['品牌']
                product_item['p_attribute'] = str([i for i in desc_info]).replace("'",
                                                                                  "\"")  # '直径：φ8#（4.0mm）；长度：300mm；类型：镀锌'
                product_item['p_attribute_value'] = str(desc_info).replace("'", "\"")
                product_item['p_sku_pic'] = product_item['p_spu_pic']
                product_item['p_sku_introduce_type'] = 1
                product_item['p_sku_introduce_pic'] = self.u.generate(
                    response.xpath("//div[@class='sku-richtext']/p/img/@src").extract())
                if response.xpath("(//div[@class='info-value']/text())[3]").extract_first():
                    product_item['p_price_num'] = int(
                        response.xpath("(//div[@class='info-value']/text())[3]").extract_first())
                else:
                    product_item['p_price_num'] = None
                if sku.get('price'):
                    product_item['p_price'] = int(sku.get('price'))
                else:
                    product_item['p_price'] = None
                product_item['p_other_info'] = str(desc_info).replace("'", "\"")
                product_item['p_source'] = int(self.own_id)
                product_item['p_version'] = self.version
                product_item['p_create_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                product_item['p_deleted'] = 0
                product_item['c_enterprise_scope'] = None
                product_item['c_customer_introduce_type'] = 0
                product_item['c_customer_introduce'] = None
                product_item['c_customer_address'] = None
                product_item['c_customer_number'] = None
                product_item['c_other_info'] = None
                product_item['c_customer_url'] = 'https://mro.yzw.cn/search/product?categories=brand%3A{}'.format(
                    sku.get('brandId'))
                product_item['c_source'] = int(self.own_id)
                product_item['c_version'] = self.version
                product_item['c_create_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                product_item['c_deleted'] = 0
                product_item['customer_follow_state'] = 0
                product_item['vandream_flag'] = 0
                yield product_item


if __name__ == '__main__':
    os.system('scrapy crawl yunzhu')
