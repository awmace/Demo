# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import time
from Crawl.tender3.es1 import filter_data, set_data


class PublicResourcePipeline(object):
    def __init__(self):
        self.sums = 0
        self.old_data = []

    # 爬虫 pipeline 接收到 Scrapy 引擎发来的 item 数据时，执行的方法
    def process_item(self, item, spider):
        single = dict()
        single['rowKey'] = item['rowKey']
        single['title'] = item['title']
        single['url'] = item['url']
        single['publish_time'] = item['publish_time']
        single['crawl_time'] = item['crawl_time']
        single['source'] = item['source']
        single['d_type'] = item['d_type']
        single['elements'] = item['elements']
        single['text'] = item['text']
        self.old_data.append(single)
        self.sums += 1
        if self.sums > 200:
            new_data = filter_data(self.old_data)
            set_data(self.old_data, new_data)
            self.old_data = []
            self.sums = 0
        yield item
