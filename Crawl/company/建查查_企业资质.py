import hashlib
import json

import requests, re, time
from lxml import etree

s_url = 'http://47.113.200.109:3012/digital-oc/dataset/data/list/'  # hb接口


def md5_jm(v):
    md5 = hashlib.md5()
    md5.update(v.encode())
    res = str(md5.hexdigest())
    return res


def set_comp(y_data, n_data):
    header = {'Content-Type': 'application/json;charset=utf-8'}  # 请求头
    data1 = json.dumps({"tableName": "raw_company", "dataList": y_data}, indent=2, ensure_ascii=False)  # 未处理的数据
    data2 = json.dumps({"tableName": "company", "dataList": n_data}, indent=2, ensure_ascii=False)  # 已经处理的数据
    res1 = requests.post(s_url, data=data1.encode('utf-8'), headers=header)
    res2 = requests.post(s_url, data=data2.encode('utf-8'), headers=header)
    print(len(y_data), len(n_data))
    print(res1.status_code, res2.status_code)


headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Cookie': 'NTWID=c8e74965badd3070504f875a46035e6bb90a83c1f0696d3753fcbe674afb13f4; Hm_lvt_5129fed3c068d823ed3dce2e7b44709c=1603866913,1605778778,1605835851,1606096670; salesIntroVisible=false; userToken=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJjdXJyZW50VGltZU1pbGxpcyI6IjE2MDYyMDEyNTU3NTAiLCJleHAiOjE2MDY4MTk4NjIsImFjY291bnQiOiIxMzI2ODI2MzY2NjIxODY4MDMyIn0.pXDKraDzgWpbRFMgXE94E83Ja-Dx-iPOIQoKb1Y9RAE; Hm_lpvt_5129fed3c068d823ed3dce2e7b44709c=1606201272',
    'Host': 'www.jianchacha.com',
    'Referer': 'https://www.jianchacha.com/company/1253628577558343697/staff',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJjdXJyZW50VGltZU1pbGxpcyI6IjE2MDYyOTIxMjAyNTEiLCJleHAiOjE2MDY5MTA3MjcsImFjY291bnQiOiIxMzI2ODI2MzY2NjIxODY4MDMyIn0.DRnPN_FsZe1hIlqAaHu3BZXb92YsxGdP_3H4kcu5n5I',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
}
for page in range(1, 100):
    result1 = []  # 原始数据
    result2 = []  # 字段数据
    # page_url = 'https://www.jianchacha.com/webApi/company/list?qualificationCode=D101A,D209A&andOr=and&pageNum={}&pageSize=20'.format(
    #     page)
    page_url = 'https://www.jianchacha.com/webApi/company/list?qualificationCode=D101A-D101T,D209A&andOr=and&pageNum={}&pageSize=20'.format(
        page)
    # page_url='https://www.jianchacha.com/webApi/company/list?searchString=%E6%B9%96%E5%8D%97%E9%87%91%E6%B5%B7%E9%92%A2%E7%BB%93%E6%9E%84%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8&pageNum=1&pageSize=15'
    response = requests.get(page_url, headers=headers).json()  # 公司列表页
    for comp in response['data']['list']:  # 公司详情页
        comp_code = comp['creditCode']  # 统一社会信用代码
        comp_name = comp['name']  # 公司名称
        comp_url = "https://www.jianchacha.com/company/{}/quality".format(comp['id'])  # 资质
        comp_res = requests.get(comp_url, headers=headers).text
        ele_comp = etree.HTML(comp_res)  # xpath解析公司详情页-资质页
        builds = ele_comp.xpath('//div[@id="Building"]/div[@class="table-component"]/table/tbody/tr/td/div/text()')
        build = [b for b in builds if '承包' in b]  # 施工资质
        designs = ele_comp.xpath('//div[@id="Design"]/div[@class="table-component"]/table/tbody/tr/td/div/text()')
        design = [d for d in designs if '设计' in d]  # 设计资质
        build = json.dumps(build, ensure_ascii=False)
        design = json.dumps(design, ensure_ascii=False)
        counts = \
            ele_comp.xpath('//*[@id="layout-content"]/div[1]/div/div[2]/div/div/div[1]/ul[1]/li[2]/a/i/text()')[0]
        counts = int(counts) // 20 + 1  # 人员页数
        persons1 = []  # 完整信息
        persons2 = []  # 目标信息
        for p in range(1, counts + 1):  # 解析人员每一页
            data = {
                "id": comp['id'],
                "pageNum": str(p),
                "pageSize": "20",
                "prjSection": "0"
            }
            person_url = 'https://www.jianchacha.com/webApi/company/person'  # 注册人员url
            try:
                person_res = requests.post(person_url, data=data, headers=headers)  # 注册人员列表
                person_res = person_res.json()['data']['list']
            except:
                print('解析人员列表页失败')
                print(person_res.json())
                continue
            for per in person_res:  # 单个人员信息
                persons1.append([per['certs'][0]['type'], per['certs'][0]['major'], per['certs'][0]['regEndDate']])
                persons2.append(per['certs'][0]['type'])
        classify = []
        for g in set(persons2):
            classify.append({'classifg': g, 'count': persons2.count(g)})
        persons1 = json.dumps(persons1, ensure_ascii=False)
        classify = json.dumps(classify, ensure_ascii=False)
        result1.append(
            {'rowKey': comp_code, 'name': comp_name, 'build': build, 'design': design, 'reg_per': persons1})
        result2.append(
            {'rowKey': comp_code, 'name': comp_name, 'build': build, 'design': design, 'reg_per': classify})
    set_comp(result1, result2)