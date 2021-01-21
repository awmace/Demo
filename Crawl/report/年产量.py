import json, requests

hl_code = input('请输入社会信用统一代码')
product = []
year = 2015
for i in range(5):
    s = '请输入{}年年产量:'.format(year)
    print(s)
    t = float(input())
    product.append(t)
    year += 1
hl = [
    {
        "x": 2015,
        "y": product[0],
        "s": "竞争企业产量"
    },
    {
        "x": 2016,
        "y": product[1],
        "s": "竞争企业产量"
    },
    {
        "x": 2017,
        "y": product[2],
        "s": "竞争企业产量"
    },
    {
        "x": 2018,
        "y": product[3],
        "s": "竞争企业产量"
    },
    {
        "x": 2019,
        "y": product[4],
        "s": "竞争企业产量"
    }
]
# 杭萧
hx = [
    {
        "x": 2015,
        "y": 56.73,
        "s": "杭萧产量"
    },
    {
        "x": 2016,
        "y": 51.95,
        "s": "杭萧产量"
    },
    {
        "x": 2017,
        "y": 60.92,
        "s": "杭萧产量"
    },
    {
        "x": 2018,
        "y": 71.61,
        "s": "杭萧产量"
    },
    {
        "x": 2019,
        "y": 78.01,
        "s": "杭萧产量"
    }
]
hl.extend(hx)
hl = json.dumps(hl, ensure_ascii=False)
data = json.dumps({"tableName": "company", "dataList": [{'rowKey': hl_code, 'production': hl}]},
                  ensure_ascii=False)
s_url = 'http://47.113.200.109:3012/digital-oc/dataset/data/list/'  # hb接口
header = {'Content-Type': 'application/json;charset=utf-8'}
res1 = requests.post(s_url, data=data.encode('utf-8'), headers=header)
print(res1.status_code)
print(data)
