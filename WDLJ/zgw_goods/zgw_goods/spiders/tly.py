# -*- coding: utf-8 -*-
import json, requests
import re
from urllib import parse

import MySQLdb
import scrapy, time
from lxml import etree
import pandas as pd
from WDLJ.zgw_goods.zgw_goods.items import ZgwGoodsItem

p_source = '8'
p_version = time.strftime('%Y%m%d', time.localtime(time.time()))
df = pd.read_excel('G:\Pycharm\Demo\WDLJ\采集关键词.xlsx')
class_names = df['三级分类名称'].tolist()


# class_names.reverse()


class TlySpider(scrapy.Spider):
    name = 'tly'

    def __init__(self):
        self.counts = 0

    def start_requests(self):
        for p_three_category_code in class_names[34:]:
            class_encode = parse.quote(p_three_category_code)  # 编码转换:商品类别
            p_list_url = 'http://www.teleyi.com/search?onlyHasStock=false&keyword={}'.format(class_encode)
            yield scrapy.Request(p_list_url, callback=self.turn_page,
                                 meta={'p_three_category_code': p_three_category_code})

    def turn_page(self, response):
        ele_first_page = etree.HTML(response.text)
        pages = ele_first_page.xpath('//span[@class="b"]/text()')
        head_url = 'http://www.teleyi.com'
        if pages:
            tail_url = ele_first_page.xpath('//ul[@class="pagination "]/li[@class="active"]/a/@href')[0][:-1]
            for page in range(1, int(pages[0]) + 1):
                meta = response.meta
                meta['p_list_url'] = head_url + tail_url + str(page)
                yield scrapy.Request(meta['p_list_url'], callback=self.parse, meta=meta)

    def parse(self, response):
        ele_list_res = etree.HTML(response.text)
        list_urls = ele_list_res.xpath('//a[@class="col-xs-8"]/@href')  # 列表页url
        for index, li in enumerate(list_urls):
            if ';' in li:
                li = li.split(';')[0]
            tid = li.split('/')[-1].split('.')[0]
            aid = li.split('/')[-2].split('.')[0]
            meta = response.meta
            data = ZgwGoodsItem()
            data['p_id'] = p_source + '_' + tid
            data['p_sku_url'] = 'http://www.teleyi.com' + li
            data['p_list_url'] = meta['p_list_url']
            data['p_three_category_code'] = meta['p_three_category_code']
            yield scrapy.Request(data['p_sku_url'], callback=self.detail, meta={'tid': tid, 'aid': aid, 'data': data},
                                 dont_filter=True)

    def detail(self, response):
        tid = response.meta['tid']
        aid = response.meta['aid']
        data = response.meta['data']
        state = 1  # 状态
        ele_response = etree.HTML(response.text)
        p_sku_valuation_unit = ele_response.xpath('//span[@class="price_font"]/text()')
        if p_sku_valuation_unit:  # 计量单位
            data['p_sku_valuation_unit'] = p_sku_valuation_unit[0].split('/')[-1].strip()
        else:
            state = 0
            data['p_sku_valuation_unit'] = ele_response.xpath('//span[@id="product_detail_price"]/text()')[1][
                                           1:].strip()
        if data['p_sku_valuation_unit'] == '价格待议':
            data['p_sku_valuation_unit'] = ''
        p_spu_name = ele_response.xpath('//div[@id="product_detail_title"]/@data-title')[0]
        p_spu_pic = ele_response.xpath('//img[@id="product_detail_image"]/@src')[0]
        if 'http' not in p_spu_pic:
            p_spu_pic = 'http://www.teleyi.com' + p_spu_pic
        data['p_spu_pic'] = p_spu_pic
        data['p_sku_pic'] = p_spu_pic
        if state:
            if '价格待议' not in response.text:  # 单价，单位重量，规格
                data['p_price'] = float(
                    ele_response.xpath('//tr[@data-tid="{}"]/td[@class="text-primary"]/text()'.format(tid))[0])
                data['p_price_num'] = float(
                    ele_response.xpath('//tr[@data-tid="{}"]/td[2]/text()'.format(tid))[0])
                specifications = ele_response.xpath('//tr[@data-tid="{}"]/td[1]/text()'.format(tid))[0]  # 规格
                data['p_spu_name'] = p_spu_name + specifications
            key_value = [i for i in ele_response.xpath('//div[@class="row"]/div/text()') if i.strip()]
            p_attribute_value = dict()
            for i in key_value:
                p_attribute_value[i.split('：')[0]] = i.split('：')[1]
            p_attribute = list(p_attribute_value.keys())
        else:
            p_price = ele_response.xpath('//a[@data-tid={}]/@data-price'.format(tid))[0].strip()
            if p_price == '价格待议':
                pass
            else:
                data['p_price'] = float(p_price)
                data['p_price_num'] = float(ele_response.xpath('//input[@class="form-control input-sm"]/@value')[0])
            specifications = ele_response.xpath('//a[@data-tid={}]/span/text()'.format(tid))[0].strip()
            data['p_spu_name'] = p_spu_name + specifications
            p_attribute = [i.split('：')[0] for i in ele_response.xpath('//div[@class="row"]/div/span/text()')]
            value = [i for i in ele_response.xpath('//div[@class="row"]/div/text()') if i.strip()]
            p_attribute_value = dict(zip(p_attribute, value))
        data['p_attribute'] = json.dumps(p_attribute, ensure_ascii=False)
        data['p_attribute_value'] = json.dumps(p_attribute_value, ensure_ascii=False)
        p_brand_name = p_attribute_value.get('品牌')
        if not p_brand_name:
            p_brand_name = '自营'
        data['p_brand_name'] = p_brand_name
        data['p_source'] = p_source
        data['p_create_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        data['p_deleted'] = 0
        data['p_version'] = p_version
        data['p_customer_name'] = ele_response.xpath('//a[@class="company-title"]/@title')[0]
        data['p_customer_id'] = p_source + '_' + ele_response.xpath('//a[@class="company-title"]/@href')[0].split('/')[
            -1]
        data['c_customer_url'] = 'http://www.teleyi.com' + \
                                 ele_response.xpath('//a[@class="company-title"]/@href')[0]
        yield scrapy.Request(data['c_customer_url'], callback=self.detail_comp, dont_filter=True,
                             meta={'data': data, 'aid': aid})

    def detail_comp(self, response):
        data = response.meta['data']
        aid = response.meta['aid']
        ele_comp = etree.HTML(response.text)
        other_key = ele_comp.xpath(
            '//div[@class="col-sm-6"]/dl/dt/text()')
        other_value = ele_comp.xpath(
            '//div[@class="col-sm-6"]/dl/dd/text()')
        c_other_info = dict()
        if len(other_key) == len(other_value):
            for index, i in enumerate(other_key):
                c_other_info[i.split('：')[0]] = "".join(other_value[index].split())
        c_customer_introduce = ele_comp.xpath('//p[@class="text-indent"]/text()')  # 公司简介
        if c_customer_introduce:
            c_customer_introduce = c_customer_introduce[0]
        else:
            c_customer_introduce = '暂无公司简介'
        comp_img = ele_comp.xpath('//div[@class="photo-box"]/img/@src')
        c_img_s = '&&'.join(comp_img)
        if c_customer_introduce and not c_img_s:
            c_customer_introduce_type = '1'
        elif c_customer_introduce == '暂无公司简介' and c_img_s:
            c_customer_introduce_type = '2'
            c_customer_introduce = c_img_s
        elif c_customer_introduce != '暂无公司简介' and c_img_s:
            c_customer_introduce_type = '3'
            c_customer_introduce = c_img_s + '@@' + c_customer_introduce
        data['c_enterprise_scope'] = c_other_info.get("主营业务")
        data['c_customer_address'] = c_other_info.get("注册地址")
        if c_other_info:
            data['c_other_info'] = json.dumps(c_other_info, ensure_ascii=False)
        data['c_customer_introduce_type'] = c_customer_introduce_type
        data['c_customer_introduce'] = c_customer_introduce
        introduce_url = 'http://www.teleyi.com/product/detail/ajax/desc/{}'.format(aid)
        yield scrapy.Request(introduce_url, callback=self.detail_1, dont_filter=True, meta={'data': data})

    def detail_1(self, response):
        data = response.meta['data']
        introduce_html = json.loads(response.text).get('content')
        if introduce_html:
            img_url = [i for i in re.findall('src="(.*?)"', introduce_html, re.S) if len(i) < 120]
            img_head = 'http://www.teleyi.com'
            text = re.sub(r'\s+|<.+?>', '', introduce_html)
            if text.strip() == "&nbsp;":
                text = ''
            for index, u in enumerate(img_url):
                if u and ('http' not in u):
                    img_url[index] = img_head + u
            if img_url and not text:
                p_sku_introduce_type = '1'
                p_sku_introduce = '&&'.join(img_url)
            elif text and not img_url:
                p_sku_introduce_type = '2'
                p_sku_introduce = text
            else:
                p_sku_introduce_type = '3'
                p_sku_introduce = '&&'.join(img_url) + '@@' + text
            data['p_sku_introduce_type'] = p_sku_introduce_type
            data['p_sku_introduce'] = p_sku_introduce
        yield data
