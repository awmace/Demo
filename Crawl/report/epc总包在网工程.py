import hashlib
import re

import requests, json, time


def md5_jm(v):
    md5 = hashlib.md5()
    md5.update(v.encode())
    ms = str(md5.hexdigest())
    return ms


url = 'http://deal.ggzy.gov.cn/ds/deal/dealList_find.jsp'
f_url = 'http://192.168.140.86/api/extract_wa/'
s_url = 'http://47.113.200.109:3012/digital-oc/dataset/data/list/'
header = {'Content-Type': 'application/json;charset=utf-8'}  # 请求头
old_data = []
target = []  # 目标
result = []  # 结果
counts = 1
for page in range(1, 4):
    data = {'TIMEBEGIN_SHOW': '2020 - 11 - 16',
            'TIMEEND_SHOW': time.strftime('%Y - %m - %d', time.localtime(time.time())),
            'TIMEBEGIN': '2020 - 11 - 16',
            'TIMEEND': time.strftime('%Y - %m - %d', time.localtime(time.time())), 'SOURCE_TYPE': '1',
            'DEAL_TIME': '05', 'DEAL_CLASSIFY': '01', 'DEAL_STAGE': '0104', 'DEAL_PROVINCE': '0',
            'DEAL_CITY': '0', 'DEAL_PLATFORM': '0', 'BID_PLATFORM': '0',
            'DEAL_TRADE': '0', 'isShowAll': '1', 'PAGENUMBER': str(page), 'FINDTXT': '总包',
            }
    response = requests.post(url, data).json()['data']
    for li in response:
        if '房地产' in li.get('tradeShow') or '房屋建筑' in li.get('tradeShow'):
            d = dict()
            d['rowKey'] = md5_jm(li['url'])
            d['url'] = li['url']
            d['title'] = li['title']
            print(li['title'])
            d['publish'] = li['timeShow']
            d['value'] = input('请输入中标金额')
            if d['value'] == '0':
                continue
            # res = requests.get(d['url'].replace('/a/', '/b/')).text
            # elements_html = re.findall('<div class="detail">\n(.*?)\n</div>\n<script>', res, re.S)[0]
            # elements = re.sub(r'\s+|<.+?>', '', elements_html)  # 去html标签
            # old_data.append({'url': li['url'], 'elements': elements, 'elements_html': elements_html})
            target.append(d)
        print(counts)
        counts += 1



# old_json = json.dumps(old_data)
# new_json = requests.post(f_url, old_json).json()['data']
# for index, j in enumerate(new_json):
#     print(j)

target_json = json.dumps({"tableName": "important_project", "dataList": target}, indent=2, ensure_ascii=False)  # 未处理的数据
res = requests.post(s_url, data=target_json.encode('utf-8'), headers=header)
print(res.status_code)