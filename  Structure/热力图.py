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
count_province = []
sums = 0
province_adcode = {
    '北京市': 110000,
    '天津市': 120000,
    '河北省': 130000,
    '山西省': 140000,
    '内蒙古自治区': 150000,
    '辽宁省': 210000,
    '吉林省': 220000,
    '黑龙江省': 230000,
    '上海市': 310000,
    '江苏省': 320000,
    '浙江省': 330000,
    '安徽省': 340000,
    '福建省': 350000,
    '江西省': 360000,
    '山东省': 370000,
    '河南省': 410000,
    '湖北省': 420000,
    '湖南省': 430000,
    '广东省': 440000,
    '广西壮族自治区': 450000,
    '海南省': 460000,
    '重庆市': 500000,
    '四川省': 510000,
    '贵州省': 520000,
    '云南省': 530000,
    '西藏自治区': 540000,
    '陕西省': 610000,
    '甘肃省': 620000,
    '青海省': 630000,
    '宁夏回族自治区': 640000,
    '新疆维吾尔自治区': 650000
}
for data in response:
    try:
        count_province.append(data["province"])
    except:
        pass
provict_set = set(count_province)
result = []
for i in provict_set:
    try:
        d = dict()
        d["area_id"] = str(province_adcode[i])
        d['value'] = count_province.count(i)
        result.append(d)
    except:
        pass
rowKey = 'software1234'
json_result = json.dumps(result, indent=2)
json_data = json.dumps({"tableName": "competitive_relationship", "dataList": [{'rowKey': rowKey, 'thermal': json_result}]})
res = requests.post(s_url, json_data.encode('utf-8'), headers=header)
print(res.status_code)
