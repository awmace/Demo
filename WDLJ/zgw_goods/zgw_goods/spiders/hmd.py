# -*- coding: utf-8 -*-
import json, requests
import logging
import re
import math
import scrapy, time
from lxml import etree
from scrapy.utils.project import get_project_settings
from ..comm.get_week_one import get_current_week
from ..comm.dao import UseSQL
from ..items import ZgwGoodsItem

settings = get_project_settings()
logger = logging.getLogger(__name__)
formdata = {"source": "all50keyword",
            "searchType": "1",
            "keyword": "",
            "categoryId": "",
            "categoryLevel": '3',
            "brandId": "",
            "showFlag": "1,3",
            "selectType": '2',
            "productSource": "",
            "deliveryAddress": "",
            "propertys": "",
            "startPrice": "",
            "endPrice": "",
            "isExcludeMianYi": "",
            "isCustom": "",
            "promotionChannelType": "2",
            "isExcludeJiCai": "1",
            "appId": "110001",
            "platform": "pc",
            "ip": "113.116.187.55, 113.96.140.72, 118.178.15.112",
            "sortBy": "vcdesc",
            "page": "",
            "pageSize": '40'}
headers = {'x-csrf-token': '1ymHTzYJZCRR40ZNryeTWYGW',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'
           }
cookie = {'homedoLogCID': '1b3d31e2-0783-4887-bb20-a2151b50bb50',
          'homedoLogTID': '7ee66c37-1986-4fd0-ab2e-8948d71e4d09',
          'homedoLogFpth': 'https%3A%2F%2Fb2b.homedo.com%2Fproduct%2Fsearch%3FcategoryId%3D10028',
          'homedoLogFpthST': '1611023333297', 'ARK_ID': 'JS8939d0c90ce7bcb8fd6c7e996acad37f8939',
          'HMD_R': '160973825985188122', 'UM_distinctid': '176cbe090e4ab3-0fb0f6f2a435bf-c791039-240000-176cbe090e5d18',
          'gr_user_id': 'a026e177-e9f0-41b2-ba76-4f37873b7aa2', 'grwng_uid': '478f95b2-af76-49aa-ba80-50c6bf8a8c03',
          'NTKF_T2D_CLIENTID': 'guest4B38EA92-E7EA-7836-A72C-CBE0AC385551',
          'OriginCode': '%3futm_source%3dwmt_sem_baidupc%26utm_medium%3dCPC%26utm_term%3d180524%26utm_content%3d180009516%26utm_campaign%3d18013&2021/1/18 17:42:47',
          'Hm_lvt_d1d21a226b3b6cbb96842713353fc9f7': '1609738261,1610326869,1610933466,1610962970',
          'csrfToken': '1ymHTzYJZCRR40ZNryeTWYGW', 'BrowseInfo': '100595464',
          'acw_tc': '76b20f6316110227270182972e2bfcc9a7781766db97114ec91d5ae8970991',
          'ARK_STARTUP': 'eyJTVEFSVFVQIjp0cnVlLCJTVEFSVFVQVElNRSI6IjIwMjEtMDEtMTkgMTA6MTg6NDkuNzUzIn0%3D',
          'CNZZDATA1257983938': '1843867308-1609734998-https%253A%252F%252Fwww.homedo.com%252F%7C1611019571',
          'calendarData': '19', 'a016ee4c2a76b6bb_gr_session_id': 'e4b92ae3-ac5f-40bb-a585-a5b5aab249ff',
          'a016ee4c2a76b6bb_gr_session_id_e4b92ae3-ac5f-40bb-a585-a5b5aab249ff': 'true', 'calendarProp': 'true',
          'browseNumber': '%5B%7B%22aId%22%3A0%2C%22num%22%3A8%7D%5D',
          'FZ_STROAGE.homedo.com': 'eyJBUktTVVBFUiI6eyJwbGF0Zm9ybV9leHRyYSI6IlBDIn0sIlNFRVNJT05JRCI6IjMxNWI2MGUzNDFkYzMyOGMiLCJTRUVTSU9OREFURSI6MTYxMTAyMzMzMjgyOCwiQU5TQVBQSUQiOiI2NmYyNzcwNGQzMTYyMjQ3IiwiQU5TJERFQlVHIjoyLCJBTlNVUExPQURVUkwiOiJodHRwczovL3Nkay5ob21lZG8uY29tIiwiRlJJU1REQVkiOiIyMDIxMDEwNCIsIkZSSVNUSU1FIjpmYWxzZSwiQVJLX0lEIjoiSlM4OTM5ZDBjOTBjZTdiY2I4ZmQ2YzdlOTk2YWNhZDM3Zjg5MzkiLCJBUktGUklTVFBST0ZJTEUiOiIyMDIxLTAxLTA0IDEzOjMxOjAwLjQwOCJ9',
          'Hm_lpvt_d1d21a226b3b6cbb96842713353fc9f7': '1611023333'}


class save_HmdSpider(scrapy.Spider):
    name = 'save_hmd'

    def __init__(self):
        self.head_url = 'https://b2b.homedo.com/product/directsearch/newSearch'  # 列表页url
        self.user = UseSQL(9)
        self.table_id = None

    def start_requests(self):
        result = self.user.get_product()
        if result[1] != None:
            logger.info(str(9) + '站点，已经存在生产者')
        else:
            count, self.table_id = self.user.tobe_product()
            start_url = 'https://www.homedo.com/?utm_source=wmt_sem_baidupc&utm_medium=CPC&utm_term=180524&utm_content=180009516&utm_campaign=18013'
            yield scrapy.Request(start_url, callback=self.traverse_url)

    def traverse_url(self, response):  # 解析河姆渡主页
        ele_start_response = etree.HTML(response.text)
        class_urls = ele_start_response.xpath('//ul[@class="menu-sun"]/li/p/a/@href')
        # 获取类别首页url
        for class_url in class_urls:
            if '\r\n' in class_url:
                class_url = re.sub('\r\n', '', class_url)
            if 'Id=' in class_url:
                cate_id = class_url.split('Id=')[-1]
                formdata["categoryId"] = cate_id
                yield scrapy.FormRequest(self.head_url, formdata=formdata, cookies=cookie, headers=headers,
                                         callback=self.save_list_url, meta={'cate_id': cate_id})

    def save_list_url(self, response):  # 解析类别首页
        data = json.loads(response.text)['data']
        cate_id = response.meta['cate_id']  # 类别id
        pages = math.ceil(data[0]['total'] / 40)  # 页数
        for page in range(1, pages + 1):
            url = cate_id + '_' + str(page)  # 类别id_页码
            self.user.insert_url_by_id(self.table_id, url)


class HmdSpider(scrapy.Spider):
    name = 'hmd'

    def __init__(self):
        self.head_url = 'https://b2b.homedo.com/product/directsearch/newSearch'  # 列表页url
        self.parse_url1 = 'https://b2b.homedo.com/goods/{}.html'
        self.parse_url2 = 'https://shop.homedo.com/item.html?item_id={}'
        self.user = UseSQL(9)
        self.source = 9
        self.source_name = '河姆渡'
        self.version = get_current_week()
        self.digital = '1234567890.'

    def start_requests(self):
        # 消费url
        while True:  # 循环获取列表页url
            result = self.user.get_product()
            if result[1] == None:
                break
            else:
                # 删除此条记录
                id = result[1].get('id')  # 表中id,根据表中id删除数据
                url = result[1].get('url')
                p_list_url = self.head_url + '_' + url  # 列表页为post请求:公共url+类别id+页码
                cate_id, page = url.split('_')
                formdata["categoryId"] = cate_id
                formdata["page"] = page
                res = self.user.delete_url_by_id(id)  # 根据id删除表中数据
                if res:
                    logger.info("delete success count:" + str(result))
                    yield scrapy.FormRequest(self.head_url, formdata=formdata, cookies=cookie, headers=headers,
                                             callback=self.parse, meta={'p_list_url': p_list_url})
                else:
                    logger.info('其它消费者消费了数据:' + str(url))

    def parse(self, response):  # 解析列表页
        list_data = json.loads(response.text)['data'][0]['docs']
        p_list_url = response.meta['p_list_url']
        for li in list_data:
            data = ZgwGoodsItem()  # 定义内容
            data['p_id'] = str(self.source) + '_' + str(li['Id']) + '_1'  # 商品在网站中的唯一标识id
            data['spu_id'] = str(self.source) + '_' + str(li['Id'])
            data['sku_id'] = str(self.source) + '_1'
            data['p_spu_name'] = li['Name']  # 商品/spu名称
            data['p_list_url'] = p_list_url  # 所在页链接
            data['category'] = li['CategoryName1'] + '>>' + li['CategoryName2'] + '>>' + li['CategoryName3']
            data['p_three_category'] = li.get('CategoryName3')  # 三级分类名称
            data['p_brand_name'] = li.get('brandName')  # 品牌名称
            data['p_source'] = self.source  # 来源网站id
            data['source_name'] = self.source_name
            data['vandream_flag'] = 0
            data['customer_follow_state'] = 0
            data['p_version'] = self.version  # 数据版本号
            data['p_deleted'] = 0  # 删除标识，0代表未删除，1代表删除
            if len(str(li['Id'])) > 6:
                data['p_sku_url'] = self.parse_url1.format(str(li['Id']))
                yield scrapy.Request(data['p_sku_url'], callback=self.detail1, headers=headers, meta={'data': data})
            else:
                data['p_sku_url'] = self.parse_url2.format(str(li['Id']))
                yield scrapy.Request(data['p_sku_url'], callback=self.detail2, headers=headers, meta={'data': data})

    def detail1(self, response):
        data = response.meta['data']  # item
        ele_response = etree.HTML(response.text)
        try:
            data['p_price'] = ele_response.xpath('//strong[@class="tm-price"]/text()')[0]
            quantity = ele_response.xpath('//p[@class="count"]/text()')[0].replace('≥', '')
            data['p_price_num'] = ''.join([s for s in quantity if s in self.digital])  # 起订量
            data['p_sku_valuation_unit'] = ''.join([s for s in quantity if s not in self.digital])  # 单位
        except:
            data['p_price'] = ele_response.xpath('//p[@class="NumPricet"]/text()')[0][1:]
            data['p_price_num'] = ele_response.xpath('//input[@id="txtCount"]/@value')[0]
            data['p_sku_valuation_unit'] = ''.join([s for s in
                                                    ele_response.xpath('//p[@class="NumBegin"]/text()')[0].split('~')[
                                                        -1] if
                                                    s not in self.digital])
        if '面' in data['p_price']:  # 面议
            data['p_price'] = float(0)
        data['p_spu_pic'] = ele_response.xpath('//span[@class="jqzoom "]/img/@src')  # spu图片地址
        if data['p_spu_pic']:
            data['p_spu_pic'] = 'https:' + data['p_spu_pic'][0]
        list_pic = ele_response.xpath('//div[@class="goods_items"]/ul/li/img/@src')
        data['p_sku_pic'] = json.dumps(['https:' + i for i in list_pic], ensure_ascii=False)
        keys_values = ele_response.xpath('//div[@class="pro_parameter"]/ul/li/@title')
        data['p_attribute'] = json.dumps([i.split('：')[0] for i in keys_values], ensure_ascii=False)
        data['p_attribute_value'] = json.dumps({i.split('：')[0]: i.split('：')[-1] for i in keys_values},
                                               ensure_ascii=False)
        p_sku_introduce_pic = ele_response.xpath('//div[@class="pro_description"]//img/@src')
        for index, img in enumerate(p_sku_introduce_pic):
            if 'https:' not in img:
                p_sku_introduce_pic[index] = 'https:' + img
        data['p_sku_introduce_pic'] = p_sku_introduce_pic
        data['p_sku_introduce_type'] = 1
        data['p_create_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        yield data

    def detail2(self, response):
        data = response.meta['data']  # item
        ele_response = etree.HTML(response.text)
        data['p_price'] = ele_response.xpath('//span[@class="price action-update-price"]/text()')[0][1:]
        if '面' in data['p_price']:  # 面议
            data['p_price'] = float(0)
        quantity = ele_response.xpath('//div[@class="weight"]/text()')[0].replace('≥', '')
        data['p_price_num'] = ''.join([s for s in quantity if s in self.digital])
        data['p_sku_valuation_unit'] = ''.join([s for s in quantity if s not in self.digital])
        data['p_spu_pic'] = ele_response.xpath('//img[@class="jqzoom"]/@src')
        if data['p_spu_pic']:
            data['p_spu_pic'] = data['p_spu_pic'][0]
        data['p_sku_pic'] = json.dumps(ele_response.xpath('//div[@class="slider-thumb-wrap"]/ul/li/div/span/img/@src'),
                                       ensure_ascii=False)
        keys = [i.split('：')[0] for i in ele_response.xpath('//ul[@class="detailinfo-list"]/li/span/text()')]
        values = ele_response.xpath('//ul[@class="detailinfo-list"]/li/text()')
        data['p_attribute'] = json.dumps(keys, ensure_ascii=False)
        data['p_attribute_value'] = json.dumps({i: values[index] for index, i in enumerate(keys)}, ensure_ascii=False)
        data['p_sku_introduce_pic'] = ele_response.xpath('//div[@class="goods-info"]//img/@src')
        data['p_sku_introduce_type'] = 1
        data['c_customer_url'] = ele_response.xpath('//div[@class="justify-content_flex-end"]/div/a/@href')[0]
        data['p_customer_id'] = str(self.source) + '_' + data['c_customer_url'].split('=')[-1]
        data['p_customer_name'] = ele_response.xpath('//div[@class="justify-content_flex-end"]/div/a/text()')[0]
        yield scrapy.Request(data['c_customer_url'], callback=self.detail_comp, headers=headers, meta={'data': data})

    def detail_comp(self, response):
        data = response.meta['data']
        data['customer_follow_state'] = 0  # 店铺跟进状态
        ele_response = etree.HTML(response.text)
        text = ele_response.xpath('//div[@class="fontsize12 oneLine"]/text()')
        if not text:
            text = data['p_customer_name']
        else:
            text = text[0]
        data['c_customer_introduce_pic'] = [i for i in ele_response.xpath('//img[@class="swiper-lazy"]/@src') if
                                            'http' in i]  # 去除非商家图片信息
        data['c_customer_introduce'] = text
        if data['c_customer_introduce_pic'] and not data['c_customer_introduce']:
            data['c_customer_introduce_type'] = 1
        elif not data['c_customer_introduce_pic'] and data['c_customer_introduce']:
            data['c_customer_introduce_type'] = 2
        elif data['c_customer_introduce_pic'] and data['c_customer_introduce']:
            data['c_customer_introduce_type'] = 3
        else:
            data['c_customer_introduce_type'] = 0
        data['p_create_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        yield data
