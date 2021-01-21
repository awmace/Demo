import random

import requests, json, hashlib, time, re
from lxml import etree
from Crawl.tender3.es1 import filter_data, set_data
from Crawl.tender3.ip代理 import get_ip, get_page_ip


def md5_jm(v):
    md5 = hashlib.md5()
    md5.update(v.encode())
    md5_v = str(md5.hexdigest())
    return md5_v


start_url = 'http://www.zgazxxw.com/he-000001l772c7-0.html'  # 招标
# start_url = 'http://www.zgazxxw.com/he-000001l772c7-0.html'  # 中标
start_response = requests.get(start_url).text
ele_start_response = etree.HTML(start_response)
provinces_urls = ele_start_response.xpath('//*[@id="selectDisplayPop"]/div/p/a/@href')
sources = ele_start_response.xpath('//*[@id="selectDisplayPop"]/div/p/a/@title')
ip = get_ip()[0]  # 起始ip
t = int(time.time())  # 起始时间


# sum1 = 1
# for pro_index, provinces_url in enumerate(provinces_urls):
#     page = 0
#     pagecrawl_url = set()
#     uncrawl_url = set()
#     while page < 201:
#         page_url = 'http://www.zgazxxw.com' + provinces_url[:-5] + 'l772c7-{}'.format(page) + provinces_url[-5:]
#         if int(time.time()) - t > 55:  # 更换ip
#             ip = get_ip()[0]
#             t = int(time.time())
#         try:
#             response = requests.get(page_url, proxies=ip).text
#         except Exception as e:
#             pagecrawl_url.add(page_url, e)
#             continue
#         ele_response = etree.HTML(response)
#         urls = ele_response.xpath('/html/body/div[5]/div[1]/div[4]/div[2]/table//tr/td[1]/a/@href')
#         head_url = 'http://www.zgazxxw.com/'
#         old_data = []
#         for index, s in enumerate(urls):
#             try:
#                 single = dict()
#                 url = head_url + s
#                 single['rowKey'] = md5_jm(url)
#                 if int(time.time()) - t > 55:  # 更换ip
#                     ip = get_ip()[0]
#                     t = int(time.time())
#                 res = requests.get(url, proxies=ip, timeout=1).text
#                 ele_res = etree.HTML(res)
#                 single['title'] = ele_res.xpath('//title/text()')[0].split(' - （安装信息网）36企业库')[0]
#                 single['url'] = url
#                 try:  # 对发布时间进行个性化处理
#                     single['publish_time'] = ele_res.xpath('//div[@class="detail"]/text()')[0]
#                 except:
#                     continue
#                 else:
#                     single['publish_time'] = ele_res.xpath('//div[@class="detail"]/text()')[0].strip()[:-3]
#                 single['crawl_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))[:-3]
#                 single['source'] = sources[pro_index]
#                 single['d_type'] = '招标公告'
#                 single['elements'] = res
#                 single['text'] = re.sub(r'\s+|<.+?>', '', single['elements'])
#                 old_data.append(single)
#                 print(sum1)  # 记录当前爬取量
#                 sum1 += 1
#             except Exception as e:
#                 print(head_url + s, e)
#                 uncrawl_url.add(head_url + s)
#         if old_data:  # 判断是否爬取到信息
#             new_data = filter_data(old_data)
#             set_data(old_data, new_data)
#         page += 1


def page_data(page_urls, ip, t, sums):
    for page_url in page_urls:
        print(page_url)
        if int(time.time()) - t > 55:  # 更换ip
            ip = get_ip()[0]
            t = int(time.time())
        try:
            response = requests.get(page_url, proxies=ip).text
        except Exception as e:
            pagecrawl_url.add(page_url, e)
            continue
        ele_response = etree.HTML(response)
        urls = ele_response.xpath('/html/body/div[5]/div[1]/div[4]/div[2]/table//tr/td[1]/a/@href')
        old_data, ip, t, sums = details(urls, ip, t, sums)
        if old_data:  # 判断是否爬取到信息
            # new_data = filter_data(old_data)
            # set_data(old_data, new_data)
            pass


def details(urls, ip, t, sums):
    old_data = []
    head_url = 'http://www.zgazxxw.com/'
    for index, s in enumerate(urls):
        try:
            single = dict()
            url = head_url + s
            print(url)
            single['rowKey'] = md5_jm(url)
            if int(time.time()) - t > 55:  # 更换ip
                ip = get_ip()[0]
                t = int(time.time())
            res = requests.get(url, proxies=ip, timeout=1).text
            ele_res = etree.HTML(res)
            single['title'] = ele_res.xpath('//title/text()')[0].split(' - （安装信息网）36企业库')[0]
            single['url'] = url
            try:  # 对发布时间进行个性化处理
                single['publish_time'] = ele_res.xpath('//div[@class="detail"]/text()')[0]
            except:
                continue
            else:
                single['publish_time'] = ele_res.xpath('//div[@class="detail"]/text()')[0].strip()[:-3]
            single['crawl_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))[:-3]
            single['source'] = '北京市公告资源交易中心'
            single['d_type'] = '招标公告'
            single['elements'] = res
            single['text'] = re.sub(r'\s+|<.+?>', '', single['elements'])
            old_data.append(single)
            print(sums)
            sums += 1
        except Exception as e:
            print(head_url + s, e)
            uncrawl_url.add(head_url + s)
    return old_data, ip, t, sums


page_urls = ['http://www.zgazxxw.com' + provinces_urls[0][:-5] + 'l772c7-{}'.format(page) + '.html' for
             page in range(101)]
pagecrawl_url = set()  # 记录未爬取列表页
uncrawl_url = set()  # 记录未爬取详情页
sums = 0
page_data(page_urls, ip, t, sums)
