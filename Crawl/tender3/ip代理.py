# import requests, random
#
# local = requests.get('http://www.httpbin.org/ip').text
#
#
# def get_ip():
#     s_ip = []
#     ips = requests.get('http://http.tiqu.alicdns.com/getip3?num=10&type=2&pro=&city=0&yys=0&port=1&pack=128786&ts=1&ys=0&cs=1&lb=1&sb=0&pb=4&mr=2&regions=&gm=4').json()
#     for i in ips:
#         s_ip.append({'http': 'http://{}'.format(i["proxy"])})
#     return s_ip
#
#
# def check_ip(ip):
#     try:
#         target = requests.get('http://www.httpbin.org/ip', proxies=ip, timeout=4).text
#         if local != target and '"origin":' in target:  # 满足条件，则代理可用
#             return True
#     except:
#         return False
#     return False
#
#
# def set_ip():
#     l_ip = []
#     # vir_ips = random.sample(get_ip(), 5)
#     for vir_ip in get_ip():
#         if check_ip(vir_ip):
#             l_ip.append(vir_ip)
#         else:
#             pass
#     print('ip池构建完成')
#     return l_ip
#

import json, requests
import random


def get_ip():
    re_ip = requests.get(
        'http://ip.ipjldl.com/index.php/api/entry?method=proxyServer.hdtiqu_api_url&packid=0&fa=0&groupid=0&fetch_key=&time=100&qty=1&port=1&format=json&ss=5&css=&dt=0&pro=&city=&usertype=4').json()
    ips = []
    for i in re_ip['data']:
        ip = 'http://' + i['IP'] + ':' + str(i['Port'])
        ips.append({'http': ip})
    return ips


def get_page_ip():
    re_ip = requests.get(
        'http://ip.ipjldl.com/index.php/api/entry?method=proxyServer.hdtiqu_api_url&packid=0&fa=0&groupid=0&fetch_key=&time=3&qty=3&port=1&format=json&ss=5&css=&dt=0&pro=&city=&usertype=4').json()
    ips = []
    for i in re_ip['data']:
        ip = 'http://' + i['IP'] + ':' + str(i['Port'])
        ips.append({'http': ip})
    return random.choice(ips)
