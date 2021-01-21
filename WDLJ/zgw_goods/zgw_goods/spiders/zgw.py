# -*- coding: utf-8 -*-
import json, requests
import re

import MySQLdb
import scrapy, time
from lxml import etree

from WDLJ.zgw_goods.zgw_goods.items import ZgwGoodsItem

p_list_s = 'https://zmall.zhaogang.com/?pn={}&ps=50&qz=true&ct=zg_arr_countrywide'
p_version = time.strftime('%Y%m%d', time.localtime(time.time()))
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
}
contrast = {'镀锌方管': '镀锌管', '无缝管': '无缝管', '普卷': '普卷', '高线': '高线', '三级抗震螺纹钢': '螺纹钢', '三级抗震盘螺': '盘螺', '普碳开平板': '其他配套材料',
            '低合金开平板': '其他配套材料', '镀锌矩形管': '镀锌管', '三级盘螺': '盘螺', '四级抗震螺纹钢': '螺纹钢', '三级螺纹钢': '螺纹钢', '等边角钢': '角钢',
            '低合金板': '其他配套材料', '方矩管': '方矩管', '低合金卷': '低合金卷', '螺旋管': '螺旋管', 'Z向板': '其他配套材料', '高建钢': '其他配套材料',
            '花纹开平板': '其他配套材料', '花纹卷': '花纹卷', '镀锌管': '镀锌管', '槽钢': '槽钢', '工字钢': '工字钢', '不等边角钢': '角钢', '焊管': '其他配套材料',
            '扁钢': '扁钢', '方钢': '其他配套材料', '建筑圆钢': '圆钢', '碳结钢': '其他配套材料', '合结钢': '其他配套材料', '普碳钢': '其他配套材料', '镀锌槽钢': '槽钢',
            '镀锌角钢': '角钢', '镀锌工字钢': '工字钢', '普板': '其他配套材料', 'C料': '其他配套材料', '钢轨': '钢轨', '重轨': '其他配套材料', 'H型钢': '热轧H型钢',
            '冷拉圆钢': '圆钢', '冷拉方钢': '其他配套材料', '冷拉扁钢': '扁钢', '冷拉六角钢': '其他配套材料', '锚杆钢': '其他配套材料', '带钢': '带钢',
            '高强度船板': '其他配套材料', '汽车大梁卷': '其他配套材料', '汽车钢': '其他配套材料', '不锈钢管材': '其他金属管', '低合金高强度结板': '其它模板',
            '锅炉容器板': '其他配套材料', '耐磨板': '其它模板', '不锈钢冷轧板': '冷轧板', '不锈钢热轧平板': '不锈钢热轧板', '船中板': '其它模板', '船板': '其它模板',
            '不锈钢冷轧卷': '不锈钢冷轧卷', '不锈钢热轧卷': '不锈钢热轧卷', '出厂平板': '其它模板', '桥梁板': '其它模板', '不锈钢型材': '铝型材', '六角棒': '棒材',
            '黑棒': '棒材', '冷扁': '扁钢', '割方': '其他配套材料', '割圆': '圆钢', '齿轮钢': '其他配套材料', '铬钼钢': '其他配套材料', '不锈钢钢带': '其他配套材料',
            '低温容器板': '其他配套材料', '碳结板': '其他配套材料', '高强板': '其他配套材料', '合金板': '其他配套材料', '五级抗震螺纹钢': '螺纹钢', '木架': '其他配套材料',
            '四级螺纹钢': '螺纹钢', '优碳卷': '其他配套材料', '四级抗震盘螺': '盘螺', '钢绞线': '预应力钢绞线', '耐酸钢': '其他配套材料'}


class ZgwSpider(scrapy.Spider):
    name = 'zgw'

    def __init__(self):
        self.goods = 0

    def start_requests(self):
        for page in range(1, 1050):
            meta = dict()
            meta['p_list_url'] = p_list_s.format(page)
            yield scrapy.Request(meta['p_list_url'], headers=headers, callback=self.parse, meta=meta)

    def parse(self, response):
        meta = response.meta
        ele_response = etree.HTML(response.text)
        list_urls = ele_response.xpath('//a[@class="shop-title"]/@href')  # 获取详情页url
        meta['shop_names'] = ele_response.xpath('//a[@class="shop-link"]/@href')  # 店铺url关键部分信息
        meta['titles'] = ele_response.xpath('//div[@class="shop-bio"]/a/span/text()')
        meta['address'] = ele_response.xpath('//div[@class="detail-cont-wrap"]/div[2]/span[2]/text()')  # 企业详细地址
        meta['ele_response'] = ele_response
        for index, li in enumerate(list_urls):  # 遍历详情页url
            data = ZgwGoodsItem()
            data['p_id'] = '2_' + li.split('/')[-1]
            data['p_sku_url'] = 'https://zmall.zhaogang.com' + li
            meta['index'] = index
            meta['data'] = data
            yield scrapy.Request(data['p_sku_url'], headers=headers, callback=self.details_a, meta=meta)

    def details_a(self, response):  # 商品详情页
        meta = response.meta  # 接受上一个函数传过来的参数
        ele_res = etree.HTML(response.text)  # 解析商品详情页
        data = meta['data']
        data['p_source'] = 2
        data['c_source'] = data['p_source']
        data['p_version'] = p_version
        data['c_version'] = data['p_version']
        data['p_list_url'] = meta['p_list_url']
        data['p_spu_name'] = ele_res.xpath('//span[@class="title"]/text()')[0]
        three_code = data['p_spu_name'].split(' ')[0]
        data['p_three_category_code'] = three_code
        # data['p_three_category_code'] = contrast.get(three_code)
        # if not data['p_three_category_code']:
        #     data['p_three_category_code'] = '其他配套材料'
        data['p_spu_pic'] = ele_res.xpath('//meta[@name="og:image"]/@content')[0].split('?')[0]
        data['p_price'] = float(ele_res.xpath('//span[@class="num"]/text()')[0].strip())
        data['p_sku_valuation_unit'] = ele_res.xpath('//span[@class="sep"]/text()')[1].split('/')[-1]
        p_price_num = ele_res.xpath('//td[@class="sku-item-td info-box"]/div[1]/text()')[0].split(' ')[0]
        data['p_price_num'] = float(re.sub('[\u4e00-\u9fa5]', '', p_price_num))
        data['p_sku_pic'] = ele_res.xpath('//meta[@name="og:image"]/@content')[0].split('?')[0]
        attribute_num = ele_res.xpath('//div[@class="params-item fl"]')
        data['p_attribute'] = ele_res.xpath('//span[@class="label fl"]/text()')
        p_attribute_value = dict()
        p_brand_name = ele_res.xpath('//div[@class="params-data clearfix"]/div[5]/span[@class="value fl"]/text()')
        if p_brand_name:
            data['p_brand_name'] = p_brand_name[0]
        else:
            data['p_brand_name'] = '自营'
        for i in range(len(attribute_num)):
            value = ele_res.xpath(
                '//div[@class="params-data clearfix"]/div[{}]/span[@class="value fl"]/text()'.format(i + 1))
            if value:
                p_attribute_value[data['p_attribute'][i]] = value[0].strip()
            else:
                p_attribute_value[data['p_attribute'][i]] = '——'
        data['p_attribute'] = json.dumps(data['p_attribute'], ensure_ascii=False)
        data['p_attribute_value'] = json.dumps(p_attribute_value, ensure_ascii=False)
        data['p_sku_introduce_type'] = 3
        data['p_sku_introduce'] = data['p_spu_pic'] + '@@' + json.dumps(p_attribute_value, ensure_ascii=False)
        shop_name = meta['shop_names'][meta['index']]
        data['p_customer_id'] = '2_' + shop_name.split('/')[-1]
        data['c_customer_url'] = 'https://zmall.zhaogang.com' + shop_name + '/search?pn=1&ps=50&qz=true'
        data['p_customer_name'] = meta['titles'][meta['index']]
        data['c_customer_address'] = meta['address'][meta['index']].strip()
        phone = meta['ele_response'].xpath(
            '//div[@class="gc-item-table-list"]/div[{}]//div[@class="detail-cont-wrap"]/div[4]/span[2]/text()'.format(
                meta['index'] + 1))
        if phone and (len(phone[0]) > 6):
            data['c_customer_number'] = phone[0]
        else:
            data['c_customer_number'] = ""
        data['c_customer_introduce_type'] = '2'
        yield scrapy.Request(data['c_customer_url'], headers=headers, callback=self.details_b, meta=meta,
                             dont_filter=True)

    def details_b(self, response):
        ele_res_c = etree.HTML(response.text)
        data = response.meta['data']
        data['c_enterprise_scope'] = ele_res_c.xpath('//div[@class="detail"]/div[3]/div[2]/text()')
        if data['c_enterprise_scope']:
            data['c_enterprise_scope'] = data['c_enterprise_scope'][0]
        else:
            data['c_enterprise_scope'] = '暂无信息'
        data['p_create_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        data['c_create_time'] = data['p_create_time']
        data['p_deleted'] = 0
        data['c_deleted'] = 0
        self.goods += 1
        print(self.goods)
        yield data
