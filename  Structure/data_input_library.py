import hashlib

from simhash import Simhash
import happybase as hb
import hanlp, requests, simhash, time, json, re
import jieba


def get_data(page):  # 楼下接口拿数据
    page_url = 'http://10.0.102.39:5004/apis/steel/{}'.format(page)
    response = requests.get(page_url).json()
    page_data = []
    for i in response['hits']['hits']:
        try:
            if i['_source'].get('crawl_type') and '中标' in i['_source'].get('crawl_type') or '结果' in i['_source'].get(
                    "crawl_type") or '成交公告' in i['_source'].get("crawl_type"):
                dicts = dict()
                dicts['rowKey'] = i['_source']['_id']
                dicts['elements_html'] = i['_source']['elements']
                page_data.append(dicts)
        except:
            pass
    return page_data


def extract_data(t):  # 提取
    t = json.dumps(t)
    # t = json.dumps(t, ensure_ascii=False)
    t = requests.post(extract_url, t.encode('utf-8')).json()['data']
    # t = requests.post(e_url, t).json()['data']
    return t


if __name__ == '__main__':

    s_url = 'http://47.113.200.109:3012/digital-oc/dataset/data'
    extract_url = 'http://192.168.140.86:5003/api/extract_bidden_wa/'
    s_header = {'Content-Type': 'application/json;charset=utf-8'}  # 请求头
    sums = 0  # 统计数据条数
    transition = []  # 过渡
    for p in range(1, 501):  # 页码
        get_result = get_data(p)
        transition.extend(get_result)
        if len(transition) > 20:
            extract_result = extract_data(transition)
            for i in extract_result:
                print(i)
            transition = []  # 清空过渡0
