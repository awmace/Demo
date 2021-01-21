import hashlib

import requests, json


def md5_jm(v):
    md5 = hashlib.md5()
    md5.update(v.encode())
    md5_v = str(md5.hexdigest())
    return md5_v


# rowKey = input('请输入社会统一信用代码:')
# url = 'http://47.113.200.109:3012/digital-oc/dataset/data/field/array?tableName=company&rowKey={}&field=region'.format(
#     rowKey)
url = 'http://47.113.200.109:3012/digital-oc/dataset/data/list?tableName=important_project'
response = requests.get(url).json()
region = []
for i in response:
    d = dict()
    i['value'] = float('%.2f' % (float(i['value']) / 10000))
    d['rowKey'] = md5_jm(i['url'])
    d.update(i)
    region.append(d)
# region = json.dumps(region, ensure_ascii=False)  [{'rowKey': rowKey, 'region': region}]
data = json.dumps({"tableName": "important_project", "dataList": region},
                  ensure_ascii=False)
s_url = 'http://47.113.200.109:3012/digital-oc/dataset/data/list/'  # hb接口
header = {'Content-Type': 'application/json;charset=utf-8'}
res = requests.post(s_url, data=data.encode('utf-8'), headers=header)
print(res.status_code)
print(data)
