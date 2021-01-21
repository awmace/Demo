import random

import requests, json, hashlib, time, re, copy
from lxml import etree
from Crawl.tender4.es1 import filter_data, set_data, connection_mysql
from Crawl.tender4.ip_agent import get_ip, get_page_ip


def md5_jm(v):
    md5 = hashlib.md5()
    md5.update(v.encode())
    md5_v = str(md5.hexdigest())
    return md5_v


def page_data(page_urls, p_ip, p_t, sums):
    conn = connection_mysql()
    while page_urls:
        page_url = page_urls.pop()
        if int(time.time()) - p_t > 52:  # 更换ip
            p_ip = get_ip()[0]
            p_t = int(time.time())
        try:
            print(page_url)
            response = requests.get(page_url, proxies=p_ip).text
        except Exception as e:
            print(e)
            page_urls.insert(0, page_url)
            continue
        ele_response = etree.HTML(response)
        urls = ele_response.xpath('/html/body/div[5]/div[1]/div[4]/div[2]/table//tr/td[1]/a/@href')
        old_data, p_ip, p_t, sums = details(urls, p_ip, p_t, sums)
        if old_data:  # 判断是否爬取到信息
            print('111')
            new_data = filter_data(copy.deepcopy(old_data))
            print('222')
            if new_data:
                print('提取成功')
                set_data(old_data, new_data, conn)


def details(urls, d_ip, d_t, sums):
    old_data = []
    while urls:
        s = urls.pop()
        url = 'http://www.zgazxxw.com/' + s
        single = dict()
        single['rowKey'] = md5_jm(url)
        if int(time.time()) - d_t > 55:  # 更换ip
            d_ip = get_ip()[0]
            d_t = int(time.time())
        try:
            res = requests.get(url, proxies=d_ip, timeout=2).text
            ele_res = etree.HTML(res)
            single['title'] = ele_res.xpath('//title/text()')[0].split(' - （安装信息网）36企业库')[0][:-8]
            single['url'] = url
            try:  # 对发布时间进行个性化处理
                single['publish_time'] = ele_res.xpath('//div[@class="detail"]/text()')[0]
            except:
                print('发布时间获取出错')
                continue
            else:
                single['publish_time'] = ele_res.xpath('//div[@class="detail"]/text()')[0].strip()[:-3]
            single['crawl_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))[:-3]
            single['source'] = '天津市公告资源交易中心'
            single['d_type'] = '招标公告'
            single['elements'] = re.findall('<body>(.*?)</body>', res, re.S)[0]
            single['text'] = re.sub(r'\s+|<.+?>', '', single['elements'])
            old_data.append(single)
            print(sums)
            sums += 1
        except Exception as e:
            print(e)
            urls.insert(0, s)
    return old_data, d_ip, d_t, sums


if __name__ == '__main__':
    ip = get_ip()[0]  # 起始ip
    t = int(time.time())  # 起始时间
    page_urls = ['http://www.zgazxxw.com/tj-000001l772c7-{}.html'.format(page) for
                 page in range(31)]  # 创建列表页url
    page_data(page_urls, ip, t, 0)
