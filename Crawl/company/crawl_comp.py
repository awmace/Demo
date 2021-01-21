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


result1 = []  # 原始数据
result2 = []  # 字段数据
for page in range(1, 72):
    # page_url = 'https://www.jianchacha.com/webApi/company/list?qualificationCode=D101A,D209A&andOr=and&pageNum={}&pageSize=20'.format(
    #     page)
    page_url = 'https://www.jianchacha.com/webApi/company/list?qualificationCode=D101A-D101T,D209A&andOr=and&pageNum={}&pageSize=20'.format(
        page)
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Cookie": "salesIntroVisible=false; userToken=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJjdXJyZW50VGltZU1pbGxpcyI6IjE2MDU3Nzg4MDg0MDkiLCJleHAiOjE2MDYzOTc0MTUsImFjY291bnQiOiIxMzI2ODI2MzY2NjIxODY4MDMyIn0.3GUKSsWc60iWlYFkyoIb0btzrzL9GzY-wqoq3ffgWp0; NTWID=c8e74965badd3070504f875a46035e6bb90a83c1f0696d3753fcbe674afb13f4; Hm_lvt_5129fed3c068d823ed3dce2e7b44709c=1603866913,1605778778,1605835851; screenPosterCookie=Y; Hm_lpvt_5129fed3c068d823ed3dce2e7b44709c=1605837493",
        "Host": "www.jianchacha.com",
        "Referer": "https://www.jianchacha.com/company?searchString=%E9%92%A2%E7%BB%93%E6%9E%84",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJjdXJyZW50VGltZU1pbGxpcyI6IjE2MDU3Nzg4MDg0MDkiLCJleHAiOjE2MDYzOTc0MTUsImFjY291bnQiOiIxMzI2ODI2MzY2NjIxODY4MDMyIn0.3GUKSsWc60iWlYFkyoIb0btzrzL9GzY-wqoq3ffgWp0",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
    }
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
            person_res = requests.post(person_url, data=data, headers=headers).json()['data']['list']  # 注册人员列表
            for per in person_res:  # 单个人员信息
                persons1.append([per['certs'][0]['type'], per['certs'][0]['major'], per['certs'][0]['regEndDate']])
                persons2.append(per['certs'][0]['type'])
        classify = []
        for g in set(persons2):
            classify.append({'classifg': g, 'count': persons2.count(g)})
        result1.append(
            {'rowKey': md5_jm(comp_code), 'name': comp_name, 'build': build, 'design': design, 'reg_per': persons1})
    header = {'Content-Type': 'application/json;charset=utf-8'}  # 请求头
    data1 = json.dumps({"tableName": "raw_company", "dataList": result1}, indent=2, ensure_ascii=False)  # 未处理的数据
    print(len(result1))
    res1 = requests.post(s_url, data=data1.encode('utf-8'), headers=header)
    print(res1.status_code)
    break
