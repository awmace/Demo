# -*- coding: utf-8 -*-
import hashlib
import re
import time

import requests
import scrapy
from lxml import etree

from Crawl.public_resource.public_resource.items import PublicResourceItem


def md5_jm(v):
    md5 = hashlib.md5()
    md5.update(v.encode())
    md5_v = str(md5.hexdigest())
    return md5_v


class QgzySpider(scrapy.Spider):
    name = 'qgzy'
    start_urls = ['http://www.zgazxxw.com/bj-000001l772c7-3.html']

    def parse(self, response):
        ele_start_response = etree.HTML(response.text)
        province_urls = ele_start_response.xpath('//*[@id="selectDisplayPop"]/div/p/a/@href')[:-3]
        for province_url in province_urls:  # 省份页
            for page in range(0, 201):
                page_url = 'http://www.zgazxxw.com' + province_url[:-5] + 'l772c7-{}'.format(page) + province_url[-5:]
                yield scrapy.Request(page_url, callback=self.parse_a)

    def parse_a(self, response):  # 列表页
        ele_response = etree.HTML(response.text)
        urls = ele_response.xpath('/html/body/div[5]/div[1]/div[4]/div[2]/table//tr/td[1]/a/@href')
        titles = ele_response.xpath('/html/body/div[5]/div[1]/div[4]/div[2]/table//tr/td[1]/a/@title')
        for index, url in enumerate(urls):
            head_url = 'http://www.zgazxxw.com/'
            url = head_url + url
            title = titles[index]
            yield scrapy.Request(url, callback=self.parse_b, meta={'url': url, 'title': title})

    def parse_b(self, response):  # 详情页
        ele_res = etree.HTML(response.text)
        item = PublicResourceItem()
        url = response.meta['url']
        item['rowKey'] = md5_jm(url)
        item['title'] = response.meta['title']
        item['url'] = url
        item['publish_time'] = ele_res.xpath('//div[@class="detail"]/text()')[0].strip()[:-3]
        item['crawl_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))[:-3]
        item['source'] = ele_res.xpath('//div[@class="location fl"]/a[4]/text()')[0]
        item['d_type'] = '招标公告'
        item['elements'] = response.text
        item['text'] = re.sub(r'\s+|<.+?>', '', item['elements'])
        # yield item
