import jieba, json
import scrapy, requests
import time, hashlib, re
from simhash import Simhash

from Crawl.tender.tender.items import TenderItem


class CompSpider(scrapy.Spider):
    name = 'comp'
    q = dict()  # 存储网页内容的hash值

    def start_requests(self):
        url = 'http://deal.ggzy.gov.cn/ds/deal/dealList_find.jsp'

        for page in range(1, 110):
            data = {'TIMEBEGIN_SHOW': '2020 - 11 - 19',
                    'TIMEEND_SHOW': time.strftime('%Y - %m - %d', time.localtime(time.time())),
                    'TIMEBEGIN': '2020 - 11 - 19',
                    'TIMEEND': time.strftime('%Y - %m - %d', time.localtime(time.time())), 'SOURCE_TYPE': '1',
                    'DEAL_TIME': '05', 'DEAL_CLASSIFY': '01', 'DEAL_STAGE': '0100', 'DEAL_PROVINCE': '0',
                    'DEAL_CITY': '0', 'DEAL_PLATFORM': '0', 'BID_PLATFORM': '0',
                    'DEAL_TRADE': '0', 'isShowAll': '1', 'PAGENUMBER': str(page), 'FINDTXT': '钢',
                    }
            yield scrapy.FormRequest(url, formdata=data, callback=self.parse, meta={'q': self.q})

    def parse(self, response):
        q = response.meta['q']
        result = json.loads(response.text, encoding='utf-8')['data']
        for li in result:
            item = TenderItem()
            item['rowKey'] = self.md5_jm(li['url'])
            item['url'] = li['url']
            item['crawl_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            item['title'] = li['title']
            item['publish_time'] = li['timeShow']
            if '开标' in li['stageShow']:
                continue
            elif '结果' in li['stageShow']:
                item['d_type'] = '中标公告'
            else:
                item['d_type'] = li['stageShow']
            if li['platformName']:
                item['source'] = li['platformName']
            else:
                item['source'] = '全国公共资源交易平台'
            yield scrapy.Request(li['url'], callback=self.parse_a, meta={'item': item, 'q': q})

    def parse_a(self, response):
        item = response.meta['item']
        q = response.meta['q']
        page_a = response.text
        s = re.findall('<p class="p_o">(.*?)</span><span>', page_a, re.S)[0] + '</span>'
        yield scrapy.Request(item['url'].replace('/a/', '/b/'), callback=self.detail_parse,
                             meta={'item': item, 'q': q, 's': s})

    def detail_parse(self, response):
        item = response.meta['item']
        q = response.meta['q']
        s = response.meta['s']
        elements = re.findall('<div class="detail">\n(.*?)\n</div>\n<script>', response.text, re.S)[0]
        item['text'] = re.sub(r'\s+|<.+?>', '', elements)  # 去html标签
        item['elements'] = s + elements
        word = jieba.lcut(elements, cut_all=True)
        if q.get(Simhash(word).value):  # 内容去重复
            pass
        else:
            q[Simhash(word).value] = 1  # 不相同则进列表用于和之后的判断
            yield item

    def md5_jm(self, v):
        md5 = hashlib.md5()
        md5.update(v.encode())
        md5_v = str(md5.hexdigest())
        return md5_v
