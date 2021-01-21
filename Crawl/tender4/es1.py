import json
import re
import time

import MySQLdb
import requests


def filter_data(old_dat):
    f_url = 'http://192.168.140.86:5003/api/extract_wa/'
    old_dat2 = []  # 传的参
    for data in old_dat:
        try:
            old_dat2.append({'url': data['url'], 'elements': data['text'], 'elements_html': data['elements']})
            del data['text'], data['elements']
        except:
            pass
    new_data2 = []
    for i in range(2):  # 分批处理
        try:
            if i == 0:
                print('333')
                old_dat1 = json.dumps(old_dat2[:12], indent=2, ensure_ascii=False)
                new_data2.extend(requests.post(f_url, old_dat1.encode('utf-8')).json()['data'])  # 提取2的列表
                print('444')
            else:
                print('555')
                old_dat1 = json.dumps(old_dat2[12:], indent=2, ensure_ascii=False)
                new_data2.extend(requests.post(f_url, old_dat1.encode('utf-8')).json()['data'])
                print('666')
        except Exception as e:
            print(e, '提取失败')
            return []

    for index, d in enumerate(new_data2):  # 字段融合
        del d['id'], d['position']
        try:
            param = {  # 地址编码参数
                'key': '24fd2a7bd631dc2f071f3c76f8e5b76a',
                'address': d['project_location'],
                'output': 'JSON'
            }
            res = requests.get('https://restapi.amap.com/v3/geocode/geo?parameters', params=param).json()  # 地图编码的请求
            j, w = res['geocodes'][0]['location'].split(',')
            d['lng'] = float(j)
            d['lat'] = float(w)
        except:
            pass
        old_dat[index].update(d)
    return old_dat


def connection_mysql():
    conn = MySQLdb.connect(
        host='localhost',
        # mysql所在主机的ip
        port=3306,  # mysql的端口号
        user="root",  # mysql 用户名
        password="123456",  # mysql 的密码
        db="demo",  # 要使用的库名
        charset="utf8"  # 连接中使用的字符集
    )

    return conn


def set_data(old_da, new_das, con):
    cursor = con.cursor()
    for index, r in enumerate(old_da):
        b = new_das[index]
        sql1 = 'insert into raw_bid value(%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        ls = [(k, b[k]) for k in b if b[k]]
        sql2 = 'insert into building_project (' + ','.join(i[0] for i in ls) + ') values (' + ','.join(
            '%r' % i[1] for i in ls) + ')'
        try:  # 插入
            cursor.execute(sql1, list(r.values()))
        except:  # 修改
            sql1 = 'update raw_bid set title=%s,url=%s,publish_time=%s,crawl_time=%s,source=%s,d_type=%s,elements_html=%s,elements=%s where rowKey=%s'
            cursor.execute(sql1, list(r.values())[1:] + list(r.values())[:1])
        try:  # 插入
            cursor.execute(sql2)
        except:  # 修改
            sql2 = 'update building_project set ' + ','.join(
                i[0] + '=%s' for i in ls if i[0] != 'rowKey') + ' where rowKey=%s;'
            cursor.execute(sql2, [i[1] for i in ls[1:]] + [ls[0][1]])
        con.commit()

# def set_data(old_da, new_das):
#     s_url = 'http://47.113.200.109:3012/digital-oc/dataset/data/list/'
#     header = {'Content-Type': 'application/json;charset=utf-8'}  # 请求头
#     new_da = []
#     for single in new_das:
#         if single.get('project_num'):
#             if len(single.get('project_num')) > 26 and '.' in single.get('project_num'):
#                 single['project_num'] = single['project_num'].split('.')[0]
#             new_da.append(single)
#     data1 = json.dumps({"tableName": "raw_bid", "dataList": old_da}, indent=2, ensure_ascii=False)  # 未处理的数据
#     data2 = json.dumps({"tableName": "building_project", "dataList": new_da}, indent=2, ensure_ascii=False)  # 已经处理的数据
#     # print(data1)
#     res1 = requests.post(s_url, data=data1.encode('utf-8'), headers=header)
#     res2 = requests.post(s_url, data=data2.encode('utf-8'), headers=header)
#     print(res1.status_code, res2.status_code, len(old_da), len(new_da))
