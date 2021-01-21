# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Item, Field


class TenderItem(scrapy.Item):
    rowKey = Field()  # md5对url进行加密
    crawl_time = Field()  # 爬取时间
    source = Field()  # 来源网站
    d_type = Field()  # 信息类型
    url = Field()  # 信息页面url
    publish_time = Field()  # 发布时间
    title = Field()  # 标题
    elements = Field()  # url页面信息
    text = Field()  # html页面的文本内容

