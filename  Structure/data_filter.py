from simhash import Simhash
from datetime import datetime
import happybase as hb
import hanlp, requests, simhash, time, json, re
import jieba


# 获取数据
def get_data(p):
    url = 'http://10.0.102.39:5004/apis/steel/{}'.format(p)
    datas = requests.get(url).json()
    result = []
    for i in datas['hits']['hits']:
        i = i['_source']
        rep = dict()
        try:
            word = jieba.lcut(i['elements'], cut_all=True)
            if Simhash(word).value not in ele_hash:
                ele_hash.append(Simhash(word).value)  # 不相同则进列表用于和之后的判断
                rep['rowKey'] = i['_id']
                del i['_id']
                rep.update(i)
                # 标题筛选
                if '钢构' in rep['title'] or '钢材' in rep['title'] or '工程' in rep['title']:
                    result.append(rep)  # 不相同则添加进列表用于返回
        except:
            print('获取失败')

    return result


# 处理数据
def filter_data(old_dat):
    new_data1 = []  # 提取结果1
    old_dat1 = []  # 传的参

    for data in old_dat:
        dicts = dict()
        dicts['rowKey'] = data['rowKey']  # 唯一标识
        dicts['d_type'] = data.get("crawl_type")  # 类别
        dicts['crawl_time'] = str(datetime.strptime(data['crawl_time'], GMT_FORMAT))  # 爬取时间
        dicts['source'] = data['source']  # 来源网站名称
        dicts['url'] = data['url']  # 来源页面url
        dicts['publish_time'] = str(datetime.strptime(data['publish_time'], GMT_FORMAT))  # 发布时间
        dicts['title'] = data['title']  # 标题
        elements = re.sub(r'\s+|<.+?>', '', data['elements'])  # 去html标签
        new_data1.append(dicts)  # 提取1的列表
        old_dat1.append({'url': data['url'], 'elements': elements, 'elements_html': data['elements']})
    old_dat1 = json.dumps(old_dat1, indent=2, ensure_ascii=False)
    try:  # 失败后单条处理,减少数据量
        print('开始...')
        new_data2 = requests.post(e_url, old_dat1)  # 提取2的列表
        print(new_data2.status_code)
    except:
        old_dat1 = json.loads(old_dat1)  # json转回来
        new_data2 = []
        for d in old_dat1:
            try:
                res = requests.post(e_url, json.dumps([d]))['data'][0]
                new_data2.append(res)
            except:
                pass
    for index, d in enumerate(new_data2):
        del d['id'], d['url'], d['position']
        new_data1[index].update(d)
    return new_data1


# 存储数据
def set_data(old_das, new_das):
    new_da = []
    old_da = []
    for single in new_das:
        if single.get('bid_person') and single.get('project_num'):
            new_da.append(single)
    for old in old_das:
        old_da.append(
            {'rowKey': old.get('rowKey'), "crawl_time": old["crawl_time"], "crawl_type": old.get("crawl_type"),
             "elements": old.get("elements"), "publish_time": old.get("publish_time"), "source": old.get("source"),
             "text": old.get("text"), "title": old.get("title"), "url": old.get("url")})
    data1 = json.dumps({"tableName": "raw_bid", "dataList": old_da}, indent=2, ensure_ascii=False)  # 未处理的数据
    data2 = json.dumps({"tableName": "building_project", "dataList": new_da}, indent=2, ensure_ascii=False)  # 已经处理的数据
    try:
        if data1 and data2:
            res1 = requests.post(s_url, data=data1.encode('utf-8'), headers=header)
            res2 = requests.post(s_url, data=data2.encode('utf-8'), headers=header)
            print(res1.status_code, res2.status_code)
    except:
        pass


if __name__ == '__main__':
    ele_hash = []  # 存储hash值用于过滤
    old_data = []  # 容纳小批量数据
    sums = 0  # 统计数据条数
    s_url = 'http://47.113.200.109:3012/digital-oc/dataset/data/list/'
    e_url = 'http://192.168.141.55:8000/api/extract_wa/'
    header = {'Content-Type': 'application/json;charset=utf-8'}  # 请求头
    GMT_FORMAT = '%a, %d %b %Y %H:%M:%S GMT'  # 时间处理格式
    for page in range(1, 501):  # 翻页
        result = get_data(page)  # 获取每一页数据
        old_data.extend(result)
        if len(old_data) > 30:
            new_data = filter_data(old_data)  # 调用提取接口
            # print(json.dumps(new_data, indent=2, ensure_ascii=False))
        #     print(new_data, page)
        # set_data(old_data, new_data)  # 数据入库
        # sums += len(new_data)
        # old_data = []  # 清空，重新下一步处理
        # new_data = []
    print('程序执行完成')
    print(sums)
