import json, requests

rowKey = input('请输入社会统一信用代码:')
business = [
    {
        "name": "轻型钢结构",
        "value": 2359071133
    },
    {
        "name": "设备钢结构",
        "value": 1387384471.84
    },
    {
        "name": "建筑重钢结构",
        "value": 2882318127.55
    },
    {
        "name": "桥梁钢结构",
        "value": 548500837.71
    },
    {
        "name": "空间钢结构",
        "value": 838883634.14
    },
    {
        "name": "智能车库",
        "value": 48805299.50
    },
    {
        "name": "装配式建筑",
        "value": 1825353405.75
    },
    {
        "name": "围护产品",
        "value": 311912106.15
    },
    {
        "name": "其它业务",
        "value": 552689369.87
    }
]

business = json.dumps(business, ensure_ascii=False)
data = json.dumps({"tableName": "company", "dataList": [{'rowKey': rowKey, 'business': business}]},
                  ensure_ascii=False)
s_url = 'http://47.113.200.109:3012/digital-oc/dataset/data/list/'  # hb接口
header = {'Content-Type': 'application/json;charset=utf-8'}
res = requests.post(s_url, data=data.encode('utf-8'), headers=header)
print(res.status_code)
print(data)
