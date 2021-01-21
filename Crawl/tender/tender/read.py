# from scrapy import cmdline
# import os

# cmdline.execute(['scrapy', 'crawl', 'comp'])
# os.system('scrapy crawl comp')

import json, hashlib

# with open('data.json', 'r', encoding='utf-8') as r:
#     s = json.load(r)
# print(len(s))

# def md5_jm(v):
#     md5 = hashlib.md5()
#     md5.update(v.encode())
#     md5_v = str(md5.hexdigest())
#     return md5_v

import requests, time, random
from lxml import etree

Ua = ['Chrome/75.0.3770.142 Safari/537.36',
      'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0)Gecko/20100101 Firefox/69.0',
      'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) ',
      'Chrome/76.0.3809.100 Safari/537.36OPR/63.0.3368.43',
      'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36Edge/18.18362',
      'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
      ]
headers = {
    'Cookie': '__jsluid_h=76a5e3c93b7e227db7b8f86bdb462bb3; __jsluid_s=ea25941e622d3a784753e4f9085dbac2; UM_distinctid=175afca5fb246-0a6e8cc68d96e7-230346d-100200-175afca5fb3308; Hm_lvt_47b9a4b804f6b4f81affae66cb8a57e9=1604972077,1604972098,1605685989; CNZZDATA1271464574=172602590-1604971081-https%253A%252F%252Fwww.zbytb.com%252F%7C1605766293; Hm_lpvt_47b9a4b804f6b4f81affae66cb8a57e9=1605768368; __jsl_captcha=3Sb4Vqn9dZFoTyzYDb7j; __jsl_clearance_s=1605770196.905|1|7FhGXjWmaetsmxf24haj9eLrZmU%3D',
    'user-agent': Ua[-1]}
url = 'https://www.zbytb.com/s-zb-11491905.html'
for i in range(100):
    ip = {'http': '119.116.14.218'}
    response = requests.get(url, headers=headers).text
    ele_response = etree.HTML(response)
    if "招标编号" in response:
        print('1111111')
    else:
        print(response)
        break
