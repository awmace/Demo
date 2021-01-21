import hashlib
import json

import requests


def md5_jm(v):
    md5 = hashlib.md5()
    md5.update(v.encode())
    s = str(md5.hexdigest())
    return s


url = 'http://47.113.200.109:3012/digital-oc/dataset/data/list?tableName=building_project'  # hb数据库拿数据url
s_url = 'http://47.113.200.109:3012/digital-oc/dataset/data/list/'  # 存数据url
header = {'Content-Type': 'application/json;charset=utf-8'}  # 存数据请求头
response = requests.get(url).json()
result = []
sums = 0
for data in response:
    try:
        param = {  # 地址编码参数
            'key': '24fd2a7bd631dc2f071f3c76f8e5b76a',
            'address': data['project_location'],
            'output': 'JSON'
        }
        res = requests.get('https://restapi.amap.com/v3/geocode/geo?parameters', params=param).json()  # 地图编码的请求
        j, w = res['geocodes'][0]['location'].split(',')  # 成功的返回结构
    except:
        continue
    rowKey = md5_jm(data['url'])
    result.append({'rowKey': rowKey, 'lng': float(j), 'lat': float(w)})
    if len(result) > 30:
        json_result = json.dumps({"tableName": "building_project", "dataList": result}, indent=2, ensure_ascii=False)
        res = requests.post(s_url, data=json_result.encode('utf-8'), headers=header)
        sums += 31
        print(res.status_code)
        result = []  # 清空result重新开始该过程
else:  # 循环结束后进行最后一次转化
    json_result = json.dumps({"tableName": "building_project", "dataList": result}, indent=2, ensure_ascii=False)
    res = requests.post(s_url, data=json_result.encode('utf-8'), headers=header)
    print(res.status_code)
print('程序执行完毕，共:', sums)
