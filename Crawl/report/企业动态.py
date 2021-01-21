import hashlib
import json, urllib.parse

import requests, re, time
from lxml import etree

s_url = 'http://47.113.200.109:3012/digital-oc/dataset/data/list/'  # hb接口


def set_comp(rowKey, data):
    header = {'Content-Type': 'application/json;charset=utf-8'}  # 请求头
    data_json = json.dumps({"tableName": "company", "dataList": [{'rowKey': rowKey, 'dynamic': data}]}, ensure_ascii=False)  # 已经处理的数据
    res = requests.post(s_url, data=data_json.encode('utf-8'), headers=header)
    print(res.status_code)


headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Cookie': 'NTWID=c8e74965badd3070504f875a46035e6bb90a83c1f0696d3753fcbe674afb13f4; Hm_lvt_5129fed3c068d823ed3dce2e7b44709c=1603866913,1605778778,1605835851,1606096670; salesIntroVisible=false; userToken=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJjdXJyZW50VGltZU1pbGxpcyI6IjE2MDYyMDEyNTU3NTAiLCJleHAiOjE2MDY4MTk4NjIsImFjY291bnQiOiIxMzI2ODI2MzY2NjIxODY4MDMyIn0.pXDKraDzgWpbRFMgXE94E83Ja-Dx-iPOIQoKb1Y9RAE; Hm_lpvt_5129fed3c068d823ed3dce2e7b44709c=1606201272',
    'Host': 'www.jianchacha.com',
    'Referer': 'https://www.jianchacha.com/company/1253628577558343697/staff',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJjdXJyZW50VGltZU1pbGxpcyI6IjE2MDYyOTIxMjAyNTEiLCJleHAiOjE2MDY5MTA3MjcsImFjY291bnQiOiIxMzI2ODI2MzY2NjIxODY4MDMyIn0.DRnPN_FsZe1hIlqAaHu3BZXb92YsxGdP_3H4kcu5n5I',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
}
comp_name = input('请输入公司名称:')
page_url = 'https://www.jianchacha.com/webApi/company/list?searchString={}&pageNum=1&pageSize=15'.format(
    urllib.parse.quote(comp_name))
response = requests.get(page_url, headers=headers).json()  # 公司列表页
comp = response['data']['list'][0]  # 公司详情页
comp_code = comp['creditCode']  # 统一社会信用代码
comp_url = "https://www.jianchacha.com/company/{}/dynamic".format(comp['id'])  # 动态
comp_res = requests.get(comp_url, headers=headers).text
ele_comp = etree.HTML(comp_res)  # xpath解析公司详情页-资质页
urls = ele_comp.xpath('//*[@id="dynamic"]/div[1]/div/div[1]/a/@href')
titles = ele_comp.xpath('//*[@id="dynamic"]/div[1]/div/div[1]/a/text()')
publishTimes = ele_comp.xpath('//*[@id="dynamic"]/div[1]/div/div[3]/div[2]/span[2]/text()')
result = []
for index, li in enumerate(urls):
    d = dict()
    d['1'] = titles[index]
    d['2'] = 'https://www.jianchacha.com' + li
    d['3'] = publishTimes[index]
    d['4'] = '建查查'
    result.append(d)
result = json.dumps(result, ensure_ascii=False)
print(result)
set_comp(comp_code, result)
