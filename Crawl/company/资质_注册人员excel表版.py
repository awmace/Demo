import json, urllib.parse
import requests
from lxml import etree
import pandas as pd
import numpy as np

comp_list = [
    "安徽鸿路钢结构(集团)股份有限公司",
    "中建钢构有限公司",
    "中铁高新工业股份有限公司",
    "浙江东南网架股份有限公司",
    "上海宝冶集团有限公司",
    "长江精工钢结构（集团）股份有限公司",
    "江苏沪宁钢机股份有限公司",
    "杭萧钢构股份有限公司",
    "中国二十二冶集团有限公司",
    "中铁宝桥集团有限公司",
    "中国建筑第二工程局有限公司",
    "中铁山桥集团有限公司",
    "山东经典重工集团股份有限公司",
    "浙江精工钢结构集团有限公司",
    "安徽鸿翔建材有限公司",
    "潮峰钢构集团有限公司",
    "多维联合集团有限公司",
    "中铁九桥工程有限公司",
    "湖南金海钢结构有限公司",
    "安徽富煌钢构股份有限公司"
]

for comp_name in comp_list:
    comp_data = dict()
    url_name = urllib.parse.quote(comp_name)
    url = 'http://jzzzcx.com/Search/{}'.format(url_name)
    res = requests.get(url).text
    ele_res = etree.HTML(res)
    quali = ele_res.xpath('//div[@class="company active"]/table/tbody/tr/td[4]/text()')
    sg = [i for i in quali if '承包' in i]
    sg.insert(0, '施工资质')
    sj = [i for i in quali if '设计' in i]
    sj.insert(0, '设计资质')
    comp_persons = ele_res.xpath('//div[@class="manager"]/table/tbody/tr/td[3]/text()')
    target = dict()
    for name in comp_persons:
        if name in target:
            target[name] += 1
        else:
            target[name] = 1
    tar = list(target.keys())
    tar.insert(0, '注册人员')
    num = list(target.values())
    num.insert(0, '人数')
    result1 = [['公司名称', comp_name], sg, sj]
    result1 = pd.DataFrame(result1).T
    result1.to_csv('资质_注册人员信息/{}1.csv'.format(comp_name), encoding="utf_8_sig", index=False, header=False)
    result2 = [['公司名称', comp_name], tar, num]
    result2 = pd.DataFrame(result2).T
    result2.to_csv('资质_注册人员信息/{}2.csv'.format(comp_name), encoding="utf_8_sig", index=False, header=False)
