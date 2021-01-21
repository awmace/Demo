import re

import MySQLdb
import requests, time, json
from lxml import etree
from urllib import parse

# conn = MySQLdb.connect(
#     host='localhost',
#     # mysql所在主机的ip
#     port=3306,  # mysql的端口号
#     user="root",  # mysql 用户名
#     password="123456",  # mysql 的密码
#     db="demo",  # 要使用的库名
#     charset="utf8"  # 连接中使用的字符集
# )

conn = MySQLdb.connect(
    host='47.113.200.109',
    # mysql所在主机的ip
    port=33063,  # mysql的端口号
    user="aiit",  # mysql 用户名
    password="aiit9876",  # mysql 的密码
    db="hx_sales",  # 要使用的库名
    charset="utf8"  # 连接中使用的字符集
)
cursor = conn.cursor()
error_count = 0
good_count = 0
repeat_count = 0
p_version = time.strftime('%Y%m%d', time.localtime(time.time()))
class_encode = parse.quote('热轧H型钢')  # 编码转换
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
}
p_list_s = 'https://zmall.zhaogang.com/?pn={}&ps=50&qz=true&ct=zg_arr_countrywide'
page = 1  # 当前页码
while 1:
    p_list_url = p_list_s.format(page)  # 列表页url
    print(p_list_url)
    response = requests.get(p_list_url, headers=headers)
    ele_response = etree.HTML(response.text)
    list_urls = ele_response.xpath('//a[@class="shop-title"]/@href')  # 获取详情页url
    shop_names = ele_response.xpath('//a[@class="shop-link"]/@href')  # 店铺url关键部分信息
    titles = ele_response.xpath('//a[@class="shop-link"]/@title')
    address = ele_response.xpath('//div[@class="detail-cont-wrap"]/div[2]/span[2]/text()')  # 企业详细地址
    for index, li in enumerate(list_urls):  # 遍历详情页url
        p_sku_url = 'https://zmall.zhaogang.com' + li
        data = dict()
        data['p_id'] = '2_' + li.split('/')[-1]
        try:
            res = requests.get(p_sku_url, headers=headers).text
            ele_res = etree.HTML(res)
            data['p_spu_name'] = ele_res.xpath('//span[@class="title"]/text()')[0]
            data['p_three_category_code'] = data['p_spu_name'].split(' ')[0]
            data['p_spu_pic'] = ele_res.xpath('//meta[@name="og:image"]/@content')[0].split('?')[0]
            data['p_price'] = float(ele_res.xpath('//span[@class="num"]/text()')[0].strip())
            data['p_sku_valuation_unit'] = ele_res.xpath('//span[@class="sep"]/text()')[1].split('/')[-1]
            p_price_num = ele_res.xpath('//td[@class="sku-item-td info-box"]/div[1]/text()')[0].split(' ')[0]
            data['p_price_num'] = float(re.sub('[\u4e00-\u9fa5]', '', p_price_num))
            print(data['p_price_num'])
            data['p_sku_pic'] = ele_res.xpath('//meta[@name="og:image"]/@content')[0].split('?')[0]
            attribute_num = ele_res.xpath('//div[@class="params-item fl"]')
            data['p_attribute'] = ele_res.xpath('//span[@class="label fl"]/text()')
            p_attribute_value = dict()
            p_brand_name = ele_res.xpath('//div[@class="params-data clearfix"]/div[5]/span[@class="value fl"]/text()')
            if p_brand_name:
                data['p_brand_name'] = p_brand_name[0]
            else:
                data['p_brand_name'] = '自营'
            for i in range(len(attribute_num)):
                value = ele_res.xpath(
                    '//div[@class="params-data clearfix"]/div[{}]/span[@class="value fl"]/text()'.format(i + 1))
                if value:
                    p_attribute_value[data['p_attribute'][i]] = value[0].strip()
                else:
                    p_attribute_value[data['p_attribute'][i]] = '——'
            data['p_attribute'] = json.dumps(data['p_attribute'], ensure_ascii=False)
            data['p_attribute_value'] = json.dumps(p_attribute_value, ensure_ascii=False)
            data['p_sku_introduce_type'] = '3'
            data['p_sku_introduce'] = data['p_spu_pic'] + '@@' + json.dumps(p_attribute_value, ensure_ascii=False)
            shop_name = shop_names[index]
            data['c_customer_url'] = 'https://zmall.zhaogang.com' + shop_name + '/search?pn=1&ps=50&qz=true'
            data['p_customer_id'] = '2_' + shop_name.split('/')[-1]

            res_c = requests.get(data['c_customer_url'], headers=headers).text
            ele_res_c = etree.HTML(res_c)
            # data['p_customer_name'] = ele_res_c.xpath('//span[@class="f-14 mr-4"]/text()')[0]
            # data['p_customer_name'] = ele_response.xpath('//div[@class="shop-bio"]/a/span/text()')[index]
            data['p_customer_name'] = titles[index]
            data['c_enterprise_scope'] = ele_res_c.xpath('//div[@class="detail"]/div[3]/div[2]/text()')[0]
            data['c_customer_address'] = address[index].strip()
            phone = ele_response.xpath(
                '//div[@class="gc-item-table-list"]/div[{}]//div[@class="detail-cont-wrap"]/div[4]/span[2]/text()'.format(
                    index + 1))
            if phone and (len(phone[0]) > 6):
                data['c_customer_number'] = phone[0]
            else:
                data['c_customer_number'] = ""
            data['c_customer_introduce_type'] = '2'

            data['p_source'] = '2'
            data['p_version'] = p_version
            data['p_list_url'] = p_list_url
            data['p_sku_url'] = p_sku_url
            data_key = list(data.keys())
            data_value = list(data.values())
            insert_sql = 'insert into goods (' + ','.join(data_key) + ') values (' + ','.join(
                '%r' % i for i in data_value) + ')'
            update_sql = 'update goods set ' + ','.join(
                [i + '=%s' for i in data_key if i != 'p_id']) + ' where p_id=%s;'
            try:
                cursor.execute(insert_sql)
                good_count += 1
            except:
                cursor.execute(update_sql, data_value[1:] + [data_value[0]])
                good_count += 1
                repeat_count += 1  # 初次运行时该数值理论上不会改变
            conn.commit()
        except Exception as e:
            error_count += 1
            print(e, error_count)
        print(good_count, repeat_count)
    # 翻页
    pages = ele_response.xpath('//div[@class="page-num"]/text()')[0].strip().split('/')[-1]
    if page < int(pages):
        page += 1
    else:
        break
