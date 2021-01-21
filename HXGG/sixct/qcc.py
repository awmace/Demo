import re, random
import time

import requests
from lxml import etree
import pandas as pd
from HXGG.sixct.ip_agent import get_ip, check_ip
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains

ip = get_ip()[0]
s_time = int(time.time())
sums = 1
header = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'max-age=0',
    'cookie': 'zg_did=%7B%22did%22%3A%20%22175b565d9aa3f2-0bfb6658c52f73-230346d-100200-175b565d9ab43d%22%7D; UM_distinctid=175b565d9c33d6-0d972b6042514d-230346d-100200-175b565d9c438b; _uab_collina=160506615262957937267342; QCCSESSID=o2fet42n3ggnmr8e71v84maej6; acw_tc=7169ab2716087738793616797ee67dacb0cfdae9958f3434d81250054a; CNZZDATA1254842228=216668287-1605062221-https%253A%252F%252Fwww.baidu.com%252F%7C1608771644; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201608773882454%2C%22updated%22%3A%201608773928381%2C%22info%22%3A%201608686151507%2C%22superProperty%22%3A%20%22%7B%5C%22%E5%BA%94%E7%94%A8%E5%90%8D%E7%A7%B0%5C%22%3A%20%5C%22%E4%BC%81%E6%9F%A5%E6%9F%A5%E7%BD%91%E7%AB%99%5C%22%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22%22%2C%22zs%22%3A%200%2C%22sc%22%3A%200%2C%22cuid%22%3A%20%22dfe7d4f6e4b739a39ccc12e67ac0b318%22%7D',
    'referer': 'https://www.qcc.com/search_adsearchmultilist?key=%E5%9F%8E%E6%8A%95',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
}
start_url = 'https://www.qcc.com/web/search?key=%E5%9F%8E%E6%8A%95%E5%85%AC%E5%8F%B8&filter=%7B%22ichain%22%3A%5B%22E%22%5D%7D'
start_res = requests.get(start_url, headers=header, proxies=ip).text
ele_start_res = etree.HTML(start_res)
provinces = ele_start_res.xpath('//a[@class="pills-item"]/text()')[:62]
provinces = [i.strip()[:-1] for index, i in enumerate(provinces) if index % 2 == 0]
counts_p = ele_start_res.xpath('//a[@class="pills-item"]/span/text()')[:31]
u = ['GD', 'BJ', 'JS', 'SH', 'ZJ', 'SC', 'SD', 'HB', 'HEN', 'FJ', 'HUB', 'AH', 'CQ', 'SAX', 'HUN', 'LN', 'TJ', 'JX',
     'YN', 'GX', 'SX', 'GZ', 'JL', 'HLJ', 'NMG', 'XJ', 'GS', 'HAIN', 'NX', 'QH', 'XZ']
for index, i in enumerate(u):
    city_url = 'https://www.qcc.com/web/search?key=%E5%9F%8E%E6%8A%95%E5%85%AC%E5%8F%B8&filter=%7B%22ichain%22%3A%5B%22E%22%5D,%22rchain%22%3A%5B%7B%22pr%22%3A%22{}%22%7D%5D%7D'.format(
        i)
    company = []
    counts = int(counts_p[index])  # 数据条数
    for page in range(1, counts // 20 + 2):
        s_time, ip = check_ip(s_time, ip)
        response = requests.get(city_url, headers=header, proxies=ip).text  # 列表页
        ele_response = etree.HTML(response)
        li_urls = ele_response.xpath('//a[@class="title"]/@href')
        for li in li_urls:
            try:
                s_time, ip = check_ip(s_time, ip)
                res = requests.get(li, headers=header, proxies=ip).text
                ele_res = etree.HTML(res)
                d = ele_res.xpath('//*[@id="company-top"]/div[2]/div[2]/div[2]/span/text()')
                if "注销" in d:
                    continue
                comp = dict()
                comp['comp_name'] = ele_res.xpath('/html/head/title/text()')[0][:-6]  # 公司名称
                phone = ele_res.xpath(
                    '//*[@id="company-top"]/div[2]/div[2]/div[3]/div[1]/span[1]/span[2]/span[2]/text()')  # 联系方式
                if phone:
                    comp['phone'] = phone[0]
                else:
                    comp['phone'] = ''
                comp['leg_person'] = ele_res.xpath('//a[@class="bname"]/h2/text()')[0]  # 法人
                names = ele_res.xpath('//div[@id="employeeslist"]//span[@class="seo font-14"]/text()')  # 主要人员
                positions = ele_res.xpath(
                    '//div[@id="employeeslist"]/table[@class="ntable ntable-odd"]/tr/td[3]/text()')  # 人员职称
                address = ele_res.xpath('//span[@class="tdpath"]/a/text()')  # 地址
                jss = []  # 监事及监事长
                if names and positions:
                    for inde, pos in enumerate(positions):
                        if '董事长' in pos or '执行董事' in pos:
                            comp['director'] = names[inde]  # 董事长
                        if '总经理' in pos or '经理' in pos:
                            comp['tgm'] = names[inde]  # 总经理
                        if '监事会主席' in pos:
                            jss.insert(0, names[inde])  # 监事会主席
                        elif '监事' in pos:
                            jss.append(names[inde])
                    comp['supervisor'] = jss[0]
                if address:
                    comp['address'] = address[0].strip()
                else:
                    comp['address'] = ''
                comp['province'] = provinces[index]  # 省份
                company.append(comp)
                print(sums)
                sums += 1
            except Exception as e:
                print('请手动维护')
                time.sleep(30)
        city_url = 'https://www.qcc.com/web/search?key=%E5%9F%8E%E6%8A%95%E5%85%AC%E5%8F%B8&p={}&filter=%7B%22ichain%22%3A%5B%22E%22%5D,%22rchain%22%3A%5B%7B%22pr%22%3A%22{}%22%7D%5D%7D'.format(
            page + 1, i)
    df = pd.DataFrame(company)
    df.to_csv('compdata.csv', mode='a', encoding='utf_8_sig', index=False, header=False)
