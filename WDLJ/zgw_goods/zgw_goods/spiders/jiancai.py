import re
import time
import random
import logging
import scrapy
import requests
from scrapy import Request
from numpy import random
from lxml import html
from datetime import datetime
from scrapy.utils.project import get_project_settings
from ..useragents import USER_AGENTS
from ..items import ZgwGoodsItem
from ..comm.dao import UseSQL
from ..comm.get_week_one import get_current_week

settings = get_project_settings()

logger = logging.getLogger(__name__)


class JianCaiSpider(scrapy.Spider):
    name = 'jiancai'
    allowed_domains = ['jc.net.cn']

    def __init__(self):
        self.own_id = '6'
        self.source_name = '建材在线'
        self.sku_id = '1'
        self.dao = UseSQL(int(self.own_id))
        self.version = get_current_week()
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
                    # test_url = 'http://www.jc.net.cn/market/search.html?keys=&area_name=&province=0&city=0&t1=%E9%BB%91%E8%89%B2%E5%8F%8A%E6%9C%89%E8%89%B2%E9%87%91%E5%B1%9E&t2=%E9%92%9B%E6%9D%90&st=&jgjs=&pno=2'
                    yield Request(url, callback=self.parse_list, meta={'id': id})
                else:
                    logger.info('其他消费者消费了数据：' + str(url))

    def parse_list(self, response):
        product_item = ZgwGoodsItem()
        category = '>'.join(
            [i.replace('>', '') for i in response.xpath('//div[@class="nav-king"]/span/text()').extract() if i])
        category = category.replace(' ', '')[3:]
        title = response.xpath("//tr[@id='tableHead']/td/text()").extract()
        product_title = response.xpath("//tbody[@id='tbody']/tr/td[contains(@class,'gray_FONT')]/a/@title").extract()
        detail_url_list = response.xpath("//a[@class='a_size12 blue_FONT']/@href").extract()  # url中获取id
        product_list = [re.search(r'shop/(.*)/product', i).group(1) for i in detail_url_list]
        spu_name = response.xpath("//a[@class='a_size12 blue_FONT']/@title").extract()  # 只保留中文
        if spu_name:
            res = [re.findall(r'[\u4e00-\u9fff]+', i) for i in spu_name]
            res = [','.join(i) for i in res]
            spu_name_list = [i.replace(',', '') for i in res]
        else:
            spu_name_list = []
        brand_list = re.findall(r'<td class="gray_FONT" style="width: 100px;">(.*)</td>', response.text)
        if brand_list:
            res = [re.findall(r'[\u4e00-\u9fff]+', i) for i in brand_list]
            res = [','.join(i) for i in res]
            brand_name = [i.replace(',', '') for i in res]
        else:
            brand_name = []
        # model = re.findall(r'<td class="gray_FONT" style="text-align: center;width: 216px">(.*)</td>',response.text)
        model = response.xpath("//tbody[@id='tbody']/tr[@onselectstart]/td[3]/text()").extract()
        model_list = [re.sub('\s*', '', i) for i in model]
        model_list = [i for i in model_list if i != '']
        # '<td style="width: 96px;" class="gray_FONT">Q235</td>'
        caizhi_str = response.xpath("//tbody[@id='tbody']/tr[@onselectstart]/td[4]").extract()
        caizhi = [re.search(r'FONT">(.*)</td>', i).group(1) for i in caizhi_str]
        price_outoftax = response.xpath("//tbody[@id='tbody']/tr[@onselectstart]/td[5]/text()").extract()
        price_outoftax = [re.sub('\s*', '', i) for i in price_outoftax]
        price = response.xpath("//tbody[@id='tbody']/tr[@onselectstart]/td[6]/text()").extract()
        price = [re.sub('\s*', '', i) for i in price]
        tax = response.xpath("//tbody[@id='tbody']/tr[@onselectstart]/td[7]/text()").extract()
        tax = [re.sub('\s*', '', i) for i in tax]
        sku_valuation_unit = response.xpath("//tbody[@id='tbody']/tr[@onselectstart]/td[8]/text()").extract()
        customer_url = response.xpath("//a[@class='a_size12 relative blue_FONT']/@href").extract()
        customer_name = response.xpath("//a[@class='a_size12 relative blue_FONT']/text()").extract()
        customer_name = [re.sub('\s*', '', i) for i in customer_name]
        customer_no_url = 'http://shop.jc.net.cn/shop/{}/index.html'
        # 由于部分页面商家url为javascript:void(0); 随机生成7位数字替换，正常shop_id 为6位
        customer_list = [customer_no_url.format(
            random.randint(low=1000000, high=9999999, size=None, dtype='l')) if i == 'javascript:void(0);' else i for i
                         in customer_url]
        customer_list = [re.search(r'shop/(.*)/index', i).group(1) for i in customer_list]
        for i in range(len(product_title)):
            try:
                other_info = {
                    title[0]: spu_name_list[i],
                    title[1]: brand_name[i],
                    title[2]: model_list[i],
                    title[3]: caizhi[i],
                    title[4]: price_outoftax[i],
                    title[5]: price[i],
                    title[6]: tax[i],
                    title[7]: sku_valuation_unit[i]
                }
            except Exception as e:
                print(str(e))
            if '品牌' in other_info:
                product_item['p_brand_name'] = other_info['品牌']
                del other_info['品牌']
            else:
                product_item['p_brand_name'] = ''  # 品牌名称
            product_item['p_id'] = self.own_id + '_' + product_list[i] + '_' + self.sku_id  # 商品唯一id, 来源_商品唯一标识
            product_item['spu_id'] = self.own_id + '_' + product_list[i]
            product_item['sku_id'] = self.own_id + '_' + self.sku_id
            product_item['source_name'] = self.source_name
            product_item['vandream_flag'] = 0
            product_item['category'] = category
            product_item['p_three_category'] = category.split('>')[-1]
            product_item['p_customer_id'] = self.own_id + '_' + customer_list[i]  # 供方唯一id，来源_供方唯一标识
            product_item['p_customer_name'] = customer_name[i]  # 供应商名称
            product_item['p_spu_name'] = spu_name_list[i] + ' ' + model_list[i] + ' ' + caizhi[i]  # spu名称
            product_item['p_spu_pic'] = ''  # spu产品图片地址
            product_item['p_sku_valuation_unit'] = sku_valuation_unit[i]  # 计价单位，计量单位
            product_item['p_sku_auxiliary_unit'] = ''  # 辅助单位
            product_item['p_sku_auxiliary_num'] = None  # 辅助单位数量
            product_item['p_sku_packaging_method'] = ''  # 包装方式
            product_item['p_attribute'] = str([i for i in other_info]).replace("'", "\"")  # 属性
            product_item['p_attribute_value'] = str(other_info).replace("'", "\"")  # 属性值
            product_item['p_sku_pic'] = ''  # sku图片地址
            product_item['p_sku_url'] = detail_url_list[i]  # 商品详情页url
            product_item['p_sku_introduce_type'] = 2  # sku介绍方式；1:图片2:文字3:文字＋图片
            product_item['p_sku_introduce'] = ''  # sku产品
            product_item['p_price_num'] = 1  # 起订量
            if price[i]:
                product_item['p_price'] = float(price[i])  # 价格
            else:
                product_item['p_price'] = None
            product_item['p_other_info'] = str(other_info).replace("'", "\"")  # 其他信息
            product_item['p_source'] = int(self.own_id)  # 数据来源，1:1688
            product_item['p_version'] = self.version  # 数据版本号:20201015
            product_item['p_create_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))  # 创建时间
            product_item['p_deleted'] = 0  # 删除标识0:未删除1:已删除
            product_item['p_list_url'] = response.url
            product_item['customer_follow_state'] = 0
            product_item['c_customer_introduce_type'] = 0
            # product_item['c_enterprise_scope'] = ''  # 企业经营范围，主营业务
            # product_item['c_customer_introduce_type'] = ''  # 企业介绍方式；1图片2文字3文字＋图片
            # product_item['c_customer_introduce'] = ''  # 企业简介
            # product_item['c_customer_address'] = ''  # 企业这册地址、企业所在地区
            # product_item['c_customer_number'] = ''  # 联系方式
            # product_item['c_customer_url'] = customer_url[i]  # 店铺首页url
            # product_item['c_other_info'] = ''  # 其他信息
            # product_item['c_source'] = self.own_id  # 数据来源，1:1688
            # product_item['c_version'] = self.version  # 数据版本号:20201015
            # product_item['c_create_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))  # 创建时间
            # product_item['c_deleted'] = '0'  # 删除标识0:未删除1:已删除
            self.count += 1
            print(self.count, product_item['category'], product_item['p_customer_name'])
            # yield product_item
