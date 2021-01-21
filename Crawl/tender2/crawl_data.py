import jieba, json
import scrapy, requests
import time, hashlib, re
from simhash import Simhash
from lxml import etree
from Crawl.tender2.read_data import filter_data, set_data


def md5_jm(v):
    md5 = hashlib.md5()
    md5.update(v.encode())
    md5_v = str(md5.hexdigest())
    return md5_v


for page in range(1, 100):
    page_url = 'http://search.ccgp.gov.cn/bxsearch?searchtype=1&page_index={}&bidSort=0&buyerName=&projectId=&pinMu=0&bidType=0&dbselect=bidx&kw=%E9%92%A2&start_time=2020%3A05%3A12&end_time=2020%3A11%3A10&timeType=5&displayZone=&zoneId=&pppStatus=0&agentName='.format(
        page)
    headers = {
        'Referer': 'http://search.ccgp.gov.cn/bxsearch?searchtype=1&page_index=1&bidSort=0&buyerName=&projectId=&pinMu=0&bidType=0&dbselect=bidx&kw=%E9%92%A2&start_time=2020%3A08%3A10&end_time=2020%3A11%3A10&timeType=4&displayZone=&zoneId=&pppStatus=0&agentName=',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36'
    }
    response = requests.get(page_url, headers=headers).text
    ele = etree.HTML(response)
    li_urls = ele.xpath('//ul[@class="vT-srch-result-list-bid"]/li/a/@href')
    old_data = []
    for index, li_url in enumerate(li_urls):
        res = requests.get(li_url)
        res.encoding = 'utf-8'
        res = res.text
        data = dict()
        try:
            data['rowKey'] = md5_jm(li_url)  # 唯一标识
            data['crawl_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            data['title'] = re.findall('<title>(.*?)</title>', res)[0]
            print(data['title'])
            data['url'] = li_url
            data['source'] = '中国政府采购网'
            publish_time = re.findall('<span id="pubTime">(.*?)</span>', res)[0]
            data['publish_time'] = publish_time.replace('年', '-').replace('月', '-').replace('日', '')
            data['d_type'] = re.findall('<a.*?class="CurrChnlCls">(.*?)</a>', res)[-1]
            data['elements'] = \
            re.findall('<div class="vF_deail_maincontent">(.*?)<div class="footer mt13">', res, re.S)[0]
            data['text'] = re.sub(r'\s+|<.+?>', '', data['elements'])
            old_data.append(data)
        except:
            pass
    # new_data = filter_data(old_data)
    # print(new_data)
    # set_data(old_data, new_data)
    # print(page)
    time.sleep(2)
