import os
import re
import logging
import random
import scrapy
import urllib
import requests
from urllib import parse
from scrapy import Request
import pandas as pd
from ..comm.dao import UseSQL
from scrapy.utils.project import get_project_settings
# from ..comm.key_words import caicbao_three_category

df = pd.read_excel(r'G:\Pycharm\Demo\WDLJ\采集关键词.xlsx')
class_names = df['三级分类名称'].tolist()

settings = get_project_settings()
logger = logging.getLogger(__name__)

# class UploadCaicbao(scrapy.Spider):
#
#     name = 'uploadcaicbao'
#     # key_words = ['螺纹钢','信号电缆','方管','圆钢','工程辅料'] # 二级目录
#     key_words = caicbao_three_category # 二级目录
#
#
#
#     def __init__(self):
#         self.own_id = 1
#         self.dao = UseSQL(self.own_id)
#         self.start_url = 'https://www.caicbao.com/center/frontProduct/productListIframe'
#
#     def start_requests(self):
#         area_list = self.get_area()
#         result = self.dao.get_product()
#         if result[1] != None:
#             logger.info('other Node is running product')
#         else:
#             # 插入一条记录
#             count,table_id = self.dao.tobe_product()
#             if count >= 1:
#                 for key_word in self.key_words:
#                     for area in area_list:
#                         yield scrapy.FormRequest(
#                             url=self.start_url,
#                             formdata={
#                                 'id': '40d5d3aeea1a4b11b8d2e554e55f97a5',
#                                 'name': '',
#                                 'brandName': '',
#                                 'brandId': '',
#                                 'productStandardCode': '',
#                                 'propertyId': '',
#                                 'propertyValue': '',
#                                 'keyword': key_word,
#                                 'status': '',
#                                 'sortStatus': '',
#                                 'type': 'productList',
#                                 'pageNo': '',
#                                 # 'currentArea': '0e9015ecbd5a4751b91485c4908378d9'
#                                 # 'currentArea': '330102'
#                                 'currentArea': area
#                             },
#                             callback=self.parse_list,
#                             meta={'key_word': key_word, 'table_id': table_id,'area_code':area}
#                         )
#             else:
#                 logger.info('other Node insert data')
#     def get_area(self):
#         area_url = 'https://www.caicbao.com/getAreaRangeListData'
#         area_info = requests.get(area_url).text.replace('false', 'None')
#         area_info_L = eval(area_info)
#         get_area = 'https://www.caicbao.com/getChildren'
#         headers = {
#             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'}
#         # area_info_L
#         area_info = []
#         for i in area_info_L:
#             code = i.get('id')
#             data = {'parentId': code}
#             #     print(data)
#             res = requests.post(get_area, data).text.replace('false', 'None')
#             first_list = eval(res)
#             for two in first_list:
#                 code_2 = two.get('id')
#                 data_2 = {'parentId': code_2}
#                 if i.get('name') in ['天津市', '上海市']:
#                     area_info.append(two.get('code'))
#                     print('11111111111')
#                 res_2 = requests.post(get_area, data).text.replace('false', 'None')
#                 second_list = eval(res_2)
#                 for three in second_list:
#                     area_info.append(three.get('code'))
#         return area_info
#
#     def parse_list(self,response):
#         # 获取key_word
#         key_word = response.meta['key_word']
#         table_id = response.meta['table_id']
#         # 提取页数
#         try:
#             page_max = response.xpath('//div[@class="ctrl-text"]/span/text()')[0].extract()
#         except Exception as e:
#             print(key_word + ':未找到此类别下的任何商品,id:' + str(self.own_id))
#             return
#         print('key_word:{},page_max:{}'.format(key_word,page_max))
#         for i in range(1, int(page_max) + 1):
#             formdata = {
#                 'id': '40d5d3aeea1a4b11b8d2e554e55f97a5',
#                 'name': '',
#                 'brandName': '',
#                 'brandId': '',
#                 'productStandardCode': '',
#                 'propertyId': '',
#                 'propertyValue': '',
#                 'keyword': key_word,
#                 'status': '',
#                 'sortStatus': '',
#                 'type': 'productList',
#                 'pageNo': str(i),
#                 # 'currentArea': '0e9015ecbd5a4751b91485c4908378d9'
#                 'currentArea': response.meta['area_code']
#             }
#             # 将url写入mysql distributed_schedul_url表中
#             self.dao.insert_url_by_id(table_id,str(formdata))



# class UploadZhaogang(scrapy.Spider):
#
#     name = 'uploadzhaogang'
#
#     def __init__(self):
#         # 找钢网采集全量数据，不设置维护列表
#         self.own_id = 2
#         self.dao = UseSQL(self.own_id)
#         # self.start_url = 'https://zmall.zhaogang.com'
#         self.start_url = 'https://zmall.zhaogang.com/?pn=1&ps=50&qz=false&ct=zg_arr_countrywide'
#         self.UserAgents = [
#             'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE',
#             'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE',
#             'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
#         ]
#
#     # 定义起始url
#     def start_requests(self):
#         result = self.dao.get_product()
#         if result[1] != None:
#             logger.info(str(self.own_id) + '站点，已经存在生产者')
#         else:
#             # 成为生产者
#             count,id = self.dao.tobe_product()
#             UserAgent = random.choice(self.UserAgents)
#             headers = {'User-Agent': UserAgent}
#             # https://zmall.zhaogang.com/?pn=1&ps=50&qz=false&ct=zg_arr_countrywide
#             # url = 'https://zmall.zhaogang.com/?pn=1&ps=50&qz=false&ct=zg_arr_countrywide'
#             # yield Request(url, callback=self.parse_next, meta={'table_id': id})
#             # 向队列中加入get请求
#             # data = {'pn': '1','ps': '50','qz': 'false','ct': 'zg_arr_countrywide'}
#             yield scrapy.FormRequest(
#                 url=self.start_url,
#                 headers=headers,
#                 method='POST',
#                 callback=self.parse_next,
#                 meta={'table_id':id},
#                 dont_filter=True
#             )
#
#     # 解析下一页
#     def parse_next(self, response):
#         # print(response.url)
#         # 获取所有页码数组成url,传递给自己
#         # 获取每页产品详情页，传递给Parse_detail
#         # print(response.meta)
#         table_id = response.meta.get('table_id')
#         page_max = response.xpath('//div//li[@class="number"][last()]/text()').extract_first()
#         # page_max = 1156
#         # print(page_max)
#         # 拼接url
#         if page_max:
#             for page_id in range(1, int(page_max) + 1):
#                 UserAgent = random.choice(self.UserAgents)
#                 headers = {'User-Agent': UserAgent}
#                 # 向队列中加入get请求
#                 next_url = 'https://zmall.zhaogang.com/?pn={}&ps=50&qz=true&ct=zg_arr_countrywide'.format(
#                     str(page_id))
#                 # 写入mysql
#                 self.dao.insert_url_by_id(table_id,next_url)



# class UploadYunzhu(scrapy.Spider):
#     name = 'uploadyunzhu'
#     allowed_domains = ['mro.yzw.cn']
#     start_urls = ['http://mro.yzw.cn']
#     key_words = ['安全防护',
#                  '卫浴照明',
#                  '工具耗材',
#                  '给水排水',
#                  '消防暖通',
#                  '防水保护',
#                  '装饰材料',
#                  '日杂用品',
#                  '机械设备',
#                  '办公用品',
#                  '电工电气',
#                  '建筑钢材',
#                  '五金紧固']
#
#     def __init__(self):
#         self.own_id = 4
#         self.dao = UseSQL(self.own_id)
#
#
#     def parse(self, response):
#         result = self.dao.get_product()
#         if result[1] != None:
#             logger.info(str(self.own_id) + '站点，已经存在生产者')
#         else:
#             count, table_id = self.dao.tobe_product()
#             for key in self.key_words:
#                 xpath_str = '//span[@id="cate-menu-list-item-name" and contains(text(),"{}")]/parent::div/following-sibling::div[1]//@href'.format(key)
#                 goods_list = response.xpath(xpath_str).extract()
#                 # print(len(goods_list))
#                 for url in goods_list:
#                     goodsList_url = self.start_urls[0] + url
#                     # print(goodsList_url)
#                     # 写入mysql
#                     self.dao.insert_url_by_id(table_id, goodsList_url)


class UploadHc360(scrapy.Spider):
    name = 'uploadhc360'
    start_urls = ['http://hc360.com/']
    key_words = class_names

    def __init__(self):
        self.own_id = 3
        self.dao = UseSQL(self.own_id)

    def start_requests(self):
        result = self.dao.get_product()
        if result[1] != None:
            logger.info(str(self.own_id) + '站点，已经存在生产者')
        else:
            count, table_id = self.dao.tobe_product()
            for i in self.key_words:
                url = 'https://s.hc360.com/seller/search.html?kwd={}'.format(i)
                yield Request(url,callback=self.parse,meta={'table_id':table_id})

    def parse(self, response):
        # 提取详情页地址
        table_id =  response.meta['table_id']
        self.dao.insert_url_by_id(table_id, response.url)
        # detail_url = response.xpath('//div[@class="picmid pRel"]/a/@href').extract()
        # for url in detail_url:
        #     url = 'https:' + url
        #     yield Request(url, callback=self.parse_detail)
        # 提取下一页
        next_url = response.xpath('//span[@class="page_next page-n"]/a/@href').extract_first()
        if next_url:
            next_url = 'https:' + next_url
            # self.dao.insert_url_by_id(table_id, next_url)
            yield Request(next_url, callback=self.parse,meta={'table_id':table_id})


# class Uploadbaba(scrapy.Spider):
#     name = 'uploadbaba'
#     allowed_domains = ['1688.com']
#     start_urls = ['https://www.1688.com/']
#     key_words = class_names
#     # key_words = ['钢材']
#
#     def __init__(self):
#         self.own_id = 5
#         self.dao = UseSQL(self.own_id)
#
#     def start_requests(self):
#         result = self.dao.get_product()
#         if result[1] != None:
#             logger.info(str(self.own_id) + '站点，已经存在生产者')
#         else:
#             count, table_id = self.dao.tobe_product()
#             for key in self.key_words:
#                 # 编码
#                 key_enc = parse.quote(key,encoding='gb2312')
#                 url = 'https://s.1688.com/selloffer/offer_search.htm?keywords={}&n=y&netType=1%2C11%2C16&spm=a260k.dacugeneral.search.0'.format(key_enc)
#                 yield Request(url,callback=self.parse,meta={'table_id':table_id})
#
#     # 解析下一页
#     def parse(self, response):
#         table_id = response.meta.get('table_id')
#         page_max = re.search(r'pageCount":(\d*)',response.text).group(1)
#         print(page_max)
#         # 拼接url
#         if page_max:
#             for page_id in range(1, int(page_max) + 1):
#                 # 加入队列
#                 next_url = 'https://s.1688.com/selloffer/offer_search.htm?keywords=%B8%D6%B2%C4&n=y&netType=16&spm=a260k.dacugeneral.search.0&beginPage={}#sm-filtbar'.format(str(page_id))
#                 # 写入mysql
#                 self.dao.insert_url_by_id(table_id, next_url)



class UploadJiancai(scrapy.Spider):
    name = 'uploadjiancai'
    start_urls = ['http://www.jc.net.cn']
    # key_words = ['黑色及有色金属']
    # key_words = ['黑色及有色金属',
    #              '水泥、砖瓦灰砂石及混凝土制品',
    #              '防腐、防水材料',
    #              '绝热（保温）、耐火材料',
    #              '成型构件及加工件',
    #              '砼、砂浆及其它配合比材料',
    #              '木、竹材料及其制品',
    #              '玻璃及玻璃制品',
    #              '墙砖、地砖、地板、地毯类材料',
    #              '装饰石材及石材制品',
    #              '墙面、天棚及屋面饰面材料',
    #              '龙骨、龙骨配件',
    #              '门窗及楼梯制品',
    #              '装饰线条、装饰件、栏杆、扶手及其它',
    #              '涂料']

    key_words = ['黑色及有色金属',
                 '水泥、砖瓦灰砂石及混凝土制品',
                 '防腐、防水材料',
                 '绝热（保温）、耐火材料',
                 '成型构件及加工件',
                 '砼、砂浆及其它配合比材料',
                 '木、竹材料及其制品']
                 # '玻璃及玻璃制品',
                 # '墙砖、地砖、地板、地毯类材料',
                 # '装饰石材及石材制品',
                 # '墙面、天棚及屋面饰面材料',
                 # '龙骨、龙骨配件',
                 # '门窗及楼梯制品',
                 # '装饰线条、装饰件、栏杆、扶手及其它',
                 # '涂料',
                 # '吸声、抗辐射及无损探伤材料',
                 # '洁具及燃气器具',
                 # '管材',
                 # '管件及管道用器材',
                 # '阀门',
                 # '法兰及其垫片',
                 # '水暖及通风空调器材',
                 # '消防器材',
                 # '灯具、光源',
                 # '开关、插座',
                 # '保险、绝缘及电热材料',
                 # '电线电缆及光纤光缆',
                 # '电气线路敷设材料',
                 # '弱电及信息类器材',
                 # '橡胶、塑料及非金属材料',
                 # '五金制品',
                 # '油品、化工原料及胶粘材料',
                 # '电极及劳保用品等其它材料',
                 # '周转材料及五金工具',
                 # '仿古建筑材料',
                 # '园林绿化',
                 # '道路桥梁专用材料',
                 # '道路桥梁专用材料'
                 # ]

    def __init__(self):
        self.own_id = 6
        self.dao = UseSQL(self.own_id)

    def parse(self, response):
        result = self.dao.get_product()
        if result[1] != None:
            logger.info(str(self.own_id) + '站点，已经存在生产者')
        else:
            count, table_id = self.dao.tobe_product()
            # 获取所有三级类目url
            for key in self.key_words:
                three_url = response.xpath('//a[contains(text(), '+key+')]/../../dd/a/@href').extract()
                three_name = response.xpath('//a[contains(text(), '+key+')]/../../dd/a/text()').extract()
                for i in range(len(three_url)):
                    url = self.start_urls[0] + three_url[i]
                    yield Request(url, callback=self.parse_three, meta={'three_name': three_name[i],'table_id':table_id})

    def parse_three(self,response):
        three_name = response.meta['three_name']
        table_id = response.meta['table_id']
        self.dao.insert_url_by_id(table_id, response.url)
        # 获取下一页链接
        next_url = response.xpath("//a[@class='page-next']/@href").extract_first()
        if next_url:
            url = self.start_urls[0] + next_url
            yield Request(url, callback=self.parse_three, meta={'three_name': three_name, 'table_id': table_id})



class UploadWuage(scrapy.Spider):
    name = 'uploadwuage'
    start_urls = ['https://www.wuage.com/']
    # key_words = ['钢材']
    key_words = class_names

    def __init__(self):
        self.own_id = 7
        self.dao = UseSQL(self.own_id)

    def start_requests(self):
        result = self.dao.get_product()
        if result[1] != None:
            logger.info(str(self.own_id) + '站点，已经存在生产者')
        else:
            count, table_id = self.dao.tobe_product()
            for i in self.key_words:
                keys = urllib.parse.quote(i)
                url = 'https://s.wuage.com/product/search?keywords={}&psa=W1.a211.0.109'.format(keys)
                yield Request(url,callback=self.parse,meta={'table_id':table_id})

    def parse(self, response):
        # 提取详情页地址
        table_id =  response.meta['table_id']
        self.dao.insert_url_by_id(table_id, response.url)
        total_page = response.xpath("//div[@class='fe-page']/@total-size").extract_first()
        if total_page:
            for i in range(2,int(total_page)):
                next_url = 'https://s.wuage.com/product/search?keywords=H%E5%9E%8B%E9%92%A2&page={}&psa=W2.a269.a108.j11'.format(i)
                self.dao.insert_url_by_id(table_id, next_url)


class UploadNewBaba(scrapy.Spider):
    name = 'uploadnewbaba'
    start_urls = ['http://www.1688.com/']
    # key_words = ['钢材']
    # key_words = class_names

    def __init__(self):
        self.own_id = 5
        self.dao = UseSQL(self.own_id)

    def parse(self,response):
        result = self.dao.get_product()
        if result[1] != None:
            logger.info(str(self.own_id) + '站点，已经存在生产者')
        else:
            count, table_id = self.dao.tobe_product()
            # 获取一级标题url
            url_list = response.xpath("//a[@class='f-14 c-name']/@href").extract()
            one_category_name_list = response.xpath("//a[@class='f-14 c-name']/text()").extract()
            for i in range(len(url_list)):
                url = url_list[i]
                one_category_name = one_category_name_list[i]
                yield Request(url,callback=self.parse_category,meta={'one_category_name':one_category_name,'table_id':table_id})


    def parse_category(self, response):
        # 提取详情页地址
        table_id =  response.meta['table_id']
        one_category_name =  response.meta['one_category_name']
        # self.dao.insert_url_by_id(table_id, response.url)
        total_category_list = response.xpath("//li[@class='item']/a/@href").extract()
        total_category_name_list = response.xpath("//li[@class='item']/a/p/text()").extract()
        for i in range(len(total_category_list)):
            url = total_category_list[i]
            category_name = one_category_name + '>>' + total_category_name_list[i]
            print(url)
            print(category_name)

        # if total_page:
        #     for i in range(2,int(total_page)):
        #         next_url = 'https://s.wuage.com/product/search?keywords=H%E5%9E%8B%E9%92%A2&page={}&psa=W2.a269.a108.j11'.format(i)
        #         self.dao.insert_url_by_id(table_id, next_url)


if __name__ == '__main__':
    os.system('scrapy crawl uploadcaicbao')