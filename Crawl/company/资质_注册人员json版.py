import json, urllib.parse

import requests
from lxml import etree

comp_list = ['安徽鸿路钢结构(集团)股份有限公司', '中建钢构有限公司',
             '浙江东南网架股份有限公司', '长江精工钢结构（集团）股份有限公司',
             '杭萧钢构股份有限公司']
result = []
for comp_name in comp_list:
    comp_data = dict()
    comp_data['公司名称'] = comp_name
    url_name = urllib.parse.quote(comp_name)
    url = 'http://jzzzcx.com/Search/{}'.format(url_name)
    res = requests.get(url).text
    ele_res = etree.HTML(res)
    quali = ele_res.xpath('//div[@class="company active"]/table/tbody/tr/td[4]/text()')
    comp_data['施工资质'] = [i for i in quali if '承包' in i]
    comp_data['设计资质'] = [i for i in quali if '设计' in i]
    comp_persons = ele_res.xpath('//div[@class="manager"]/table/tbody/tr/td[3]/text()')
    target = dict()
    for name in comp_persons:
        if name in target:
            target[name] += 1
        else:
            target[name] = 1
    person_list = []
    for name in target:
        person_list.append({'name': name, 'value': target[name]})
    comp_data['注册人员'] = person_list
    result.append(comp_data)

result_json = json.dumps(result, ensure_ascii=False, indent=2)
with open('资质_注册人员信息/comp_data.json', 'w', encoding='utf-8') as w:
    json.dump(result_json, w)
