import os
import json
import time
import logging
import scrapy
from scrapy import Request
from ..items import ZgwGoodsItem
from scrapy.utils.project import get_project_settings
from ..comm.dao import UseSQL
from ..comm.upload_picture import UploadPic
from ..comm.get_week_one import get_current_week

settings = get_project_settings()
logger = logging.getLogger(__name__)


class CaicbaoSpider(scrapy.Spider):
    name = 'caicbao'
    start_urls = ['https://www.caicbao.com']

    def __init__(self):
        self.version = get_current_week()
        self.own_id = '1'
        self.start_url = 'https://www.caicbao.com/center/frontProduct/productListIframe'
        self.sku_url = 'https://www.caicbao.com/center/frontProduct/getProductDetailByProductId?productId='
        self.detail_url = 'https://www.caicbao.com/center/frontProduct/productDetails?id='
        self.dao = UseSQL(int(self.own_id))
        self.u = UploadPic()

    def start_requests(self):
        # mysql中获取待消费的url
        print('############')
        while True:
            result = self.dao.get_product()
            if result[1] == None:
                break
            else:
                # 删除此条记录
                id = result[1].get('id')
                url = result[1].get('url')
                params = eval(url)
                res = self.dao.delete_url_by_id(id)
                if res:
                    logger.info("delete success count:" + str(result))
                    yield scrapy.FormRequest(
                        url=self.start_url,
                        formdata=params,
                        callback=self.parse_list,
                        meta={'params': params})
                else:
                    logger.info("其他消费者消费了数据:" + str(url))

    def parse_list(self, response):
        params = response.meta['params']
        list_url = response.url
        spu_id_list = response.xpath("//tbody/tr/@data-productid").extract()
        if spu_id_list:
            for id in spu_id_list:
                url = self.sku_url + id
                yield Request(url=url, callback=self.parse_detail,
                              meta={'spu_id': id, 'list_url': list_url, 'params': params})

    def parse_detail(self, response):
        params = response.meta['params']
        product_item = ZgwGoodsItem()
        info = json.loads(response.text)
        spu_id = response.meta['spu_id']
        list_url = response.meta['list_url']
        sku_id = '1'
        product_item['p_id'] = self.own_id + '_' + spu_id + '_' + sku_id
        product_item['spu_id'] = spu_id
        product_item['sku_id'] = sku_id
        product_item['p_customer_id'] = '000001'
        product_item['p_customer_name'] = '采材宝官方旗舰店'
        product_item['p_spu_code'] = None
        product_item['p_spu_name'] = info.get('title')
        product_item['p_spu_pic'] = self.u.generate(self.start_urls[0] + info.get('pictureUrl'))
        product_item['source_name'] = '采材宝'
        product_item['category'] = info.get('title')
        product_item['p_three_category'] = info.get('title')
        product_item['p_brand_name'] = info.get('barndName')
        product_item['p_sku_valuation_unit'] = None
        product_item['p_sku_auxiliary_unit'] = None
        product_item['p_sku_auxiliary_num'] = None
        product_item['p_sku_packaging_method'] = None
        product_item['p_attribute'] = None
        product_item['p_attribute_value'] = None
        product_item['p_sku_pic'] = product_item['p_spu_pic']
        product_item['p_sku_url'] = self.detail_url + info.get('pictureUrl')
        product_item['p_sku_introduce_type'] = 2
        product_item['p_sku_introduce'] = None
        product_item['p_sku_introduce_pic'] = None
        product_item['p_price_num'] = 1
        product_item['p_price'] = None
        product_item['p_other_info'] = str(info)
        product_item['p_source'] = int(self.own_id)
        product_item['p_list_url'] = list_url
        product_item['p_version'] = self.version
        product_item['p_create_time'] = time.strftime('%Y-%m-%d %H:%M:%S',
                                                      time.localtime(time.time()))
        product_item['p_deleted'] = 0
        product_item['c_customer_url'] = None
        product_item['category'] = None
        product_item['c_enterprise_scope'] = None
        product_item['c_customer_introduce_type'] = None
        product_item['c_customer_introduce'] = None
        product_item['c_customer_introduce_pic'] = None
        product_item['c_customer_address'] = None
        product_item['c_customer_number'] = None
        product_item['c_customer_phone'] = None
        product_item['c_customer_url'] = None
        product_item['c_other_info'] = None
        product_item['c_source'] = int(self.own_id)
        product_item['c_version'] = self.version
        product_item['c_create_time'] = time.strftime('%Y-%m-%d %H:%M:%S',
                                                      time.localtime(time.time()))
        product_item['c_deleted'] = 0
        product_item['vandream_flag'] = 0
        product_item['customer_follow_state'] = 0
        yield product_item


if __name__ == '__main__':
    os.system('scrapy crawl caicbao')
