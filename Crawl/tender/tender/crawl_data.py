import json, time, re, os
import requests


def get_data():
    with open('data.json', 'r', encoding='utf-8') as r:
        s = json.load(r)
    old_data = []
    for va in s:
        if len(old_data) == 20:
            new_data = filter_data(old_data)  # 提取数据
            set_data(old_data, new_data)  # 存储数据
            old_data = []  # 清空暂存列表
        else:
            old_data.append(va)  # 添加数据到暂存列表中
    else:  # 最后部分数据进行提取
        if len(old_data):  # 判断最后是否有数据剩余
            new_data = filter_data(old_data)
            set_data(old_data, new_data)


def filter_data(old_dat):
    old_dat1 = []  # 传的参
    for data in old_dat:
        elements = re.sub(r'\s+|<.+?>', '', data['elements'])  # 去html标签
        old_dat1.append({'url': data['url'], 'elements': elements, 'elements_html': data['elements']})
    old_dat1 = json.dumps(old_dat1)
    try:  # 失败后单条处理,减少数据量
        new_data2 = requests.post(f_url, old_dat1).json()['data']  # 提取2的列表
    except:
        old_dat1 = json.loads(old_dat1)  # json转回来
        new_data2 = []
        for d in old_dat1:
            try:
                new_data2.append(requests.post(f_url, json.dumps([d]))['data'][0])
            except:
                new_data2.append({'Exception': '处理异常'})
    for index, d in enumerate(new_data2):  # 字段融合
        del old_dat[index]['elements'], old_dat[index]['text']
        old_dat[index].update(d)
    return old_dat


def set_data(old_da, new_das):
    new_da = []
    for single in new_das:
        if single.get('bid_person') and single.get('project_num'):
            new_da.append(single)
    data1 = json.dumps({"tableName": "raw_bid", "dataList": old_da}, indent=2, ensure_ascii=False)  # 未处理的数据
    data2 = json.dumps({"tableName": "building_project", "dataList": new_da}, indent=2, ensure_ascii=False)  # 已经处理的数据
    res1 = requests.post(s_url, data=data1.encode('utf-8'), headers=header)
    res2 = requests.post(s_url, data=data2.encode('utf-8'), headers=header)
    print(res1.status_code, res2.status_code)


if __name__ == "__main__":
    os.system('scrapy crawl comp')
    s_url = 'http://47.113.200.109:3012/digital-oc/dataset/data/list/'
    f_url = 'http://192.168.140.86/api/extract_wa/'
    header = {'Content-Type': 'application/json;charset=utf-8'}  # 请求头
    time.sleep(5)
    print('********执行读取过程******')
    get_data()
    print('********执行完毕******')
