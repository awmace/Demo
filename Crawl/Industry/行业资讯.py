import requests, time, urllib.parse, json, time
from lxml import etree

headers = {
    "token": "-1",
}

repeat = []  # 根据标题去重
s_url = 'http://47.113.200.109:3012/digital-oc/dataset/data/list/'  # hb接口url
header = {'Content-Type': 'application/json;charset=utf-8'}  # hb接口请求头
url = 'https://search.mysteel.com/searchapi/search/getAllData'
for page in range(1, 8):
    data = {
        "pageNo": str(page),
        "pageSize": "10",
        "platform": "pc",
        "query": "钢结构",
        "sortType": "complex"
    }
    response = requests.post(url, json=data, headers=headers).json()
    result = []
    for info in response['dataList']:
        # info['articleBean']['keyTags'][0]  分类:行业动态，企业之窗，其它动态等
        if info.get('articleBean') and info['articleBean']['title'] not in repeat:
            d = dict()
            d['rowKey'] = info['articleBean']['id']
            d['url'] = 'http:' + info['articleBean']['url']
            d['title'] = info['articleBean']['title']
            d['publishTime'] = info['publishTime']
            d['source'] = info['articleBean']['source']
            repeat.append(d['title'])
            result.append(d)
    result_json = json.dumps({"tableName": "industry_news", "dataList": result}, ensure_ascii=False)  #
    # res = requests.post(s_url, data=result_json.encode('utf-8'), headers=header)
    # print(res.status_code, len(result))
    print(result_json)
