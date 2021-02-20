import os
import re
import time
import logging
import scrapy
import json
import random
import requests
from lxml import html
from datetime import datetime, date, timedelta
from scrapy import Request
from ..items import ZgwGoodsItem
from scrapy.utils.project import get_project_settings
from ..comm.baba_category import category_dict
from ..comm.upload_picture import UploadPic
from ..comm.get_week_one import get_current_week

settings = get_project_settings()

logger = logging.getLogger(__name__)


class NewBabaSpider(scrapy.Spider):
    name = 'newbaba'

    start_urls = ['http://widget.1688.com/front/ajax/getJsonComponent.json']

    def __init__(self):
        self.own_id = '5'
        self.version = get_current_week()
        self.u = UploadPic()
        # 获取明天时间戳
        self.ali_time = str(self.get_tomorrow())
        self.cookie = {'__mbox_csrf_token': 'F6bGYIfjkEvy8MAp_{}111'.format(self.ali_time)}
        self.headers = {
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'cookie': '__mbox_csrf_token=F6bGYIfjkEvy8MAp_{}111'.format(self.ali_time),
            'origin': 'https://widget.1688.com',
            'referer': 'https://widget.1688.com/front/ajax/bridge.html?target=brg-2852',
            'sec-ch-ua': '"Chromium";v="88", "Google Chrome";v="88", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
        }
        self.parms_data = {
            'namespace': 'cateMarketOfferList',
            'widgetId': 'cateMarketOfferList',
            'methodName': 'execute',
            'params': '{"sceneId":"1681","curPage":1,"pageSize":20,"sortType":null,"descendOrder":null,"priceStart":null,"priceEnd":null,"province":"","city":""}',
            'sceneId': '5564',
            'curPage': '1',
            'pageSize': '50',
            '__mbox_csrf_token': 'F6bGYIfjkEvy8MAp_{}111'.format(self.ali_time)
        }

    def get_tomorrow(self):
        tomorrow = date.today() + timedelta(days=1)
        return int(time.mktime(tomorrow.timetuple()))

    def parse(self, response, **kwargs):
        # 发送post请求
        for key, value in category_dict.items():
            self.parms_data['sceneId'] = str(key)
            category = value
            yield scrapy.FormRequest(
                url=self.start_urls[0],
                formdata=self.parms_data,
                headers=self.headers,
                cookies=self.cookie,
                callback=self.parse_category, meta={'category': category, 'category_id': str(key), 'page': 1})

    def parse_category(self, response):
        product_item = ZgwGoodsItem()
        page = response.meta['page'] + 1
        category = response.meta['category']
        category_id = response.meta['category_id']
        data_info = json.loads(response.text)
        result_content = data_info.get('content')
        if result_content:
            info_result = result_content.get('result')
            result_dict = info_result[0] if info_result else None
            if result_dict:
                result_data = result_dict.get('data')
                if result_data:
                    result_list = result_data.get('list')
                    if result_list:
                        for info in result_list:
                            spu_id = str(info.get('offerId'))
                            sku_id = '1'
                            product_item['p_id'] = self.own_id + '_' + spu_id + '_' + sku_id
                            product_item['spu_id'] = spu_id
                            product_item['sku_id'] = sku_id
                            product_item['p_customer_id'] = None
                            product_item['p_customer_name'] = info.get('company')
                            product_item['p_spu_code'] = None
                            product_item['p_spu_name'] = info.get('title')
                            product_item['p_spu_pic'] = self.u.generate(info.get('imgUrl'))
                            product_item['source_name'] = '阿里巴巴'
                            product_item['p_three_category'] = category.split('>>')[-1]
                            product_item['p_brand_name'] = None
                            product_item['p_sku_valuation_unit'] = info.get('unit')
                            product_item['p_sku_auxiliary_unit'] = None
                            product_item['p_sku_auxiliary_num'] = None
                            product_item['p_sku_packaging_method'] = None
                            product_item['p_attribute'] = str(info.get('propertyTags'))
                            product_item['p_attribute_value'] = str({key: True for key in info.get('propertyTags')})
                            product_item['p_sku_pic'] = product_item['p_spu_pic']
                            product_item['p_sku_url'] = info.get('detailUrl')
                            product_item['p_sku_introduce_type'] = 2
                            product_item['p_sku_introduce'] = ','.join(info.get('services'))
                            product_item['p_sku_introduce_pic'] = None
                            product_item['p_price_num'] = 1
                            product_item['p_price'] = info.get('bPrice')
                            product_item['p_other_info'] = str(info)
                            product_item['p_source'] = int(self.own_id)
                            product_item['p_list_url'] = None
                            product_item['p_version'] = self.version
                            product_item['p_create_time'] = time.strftime('%Y-%m-%d %H:%M:%S',
                                                                          time.localtime(time.time()))
                            product_item['p_deleted'] = 0
                            product_item['c_customer_url'] = None
                            product_item['category'] = category
                            product_item['c_enterprise_scope'] = None
                            product_item['c_customer_introduce_type'] = 0
                            product_item['c_customer_introduce'] = None
                            product_item['c_customer_introduce_pic'] = None
                            product_item['c_customer_address'] = info.get('offerSendAddr')
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
                        self.parms_data['curPage'] = str(page)
                        yield scrapy.FormRequest(
                            url=self.start_urls[0],
                            formdata=self.parms_data,
                            headers=self.headers,
                            cookies=self.cookie,
                            callback=self.parse_category,
                            meta={'category': category, 'category_id': category_id, 'page': page})


if __name__ == '__main__':
    os.system('scrapy crawl newbaba')
