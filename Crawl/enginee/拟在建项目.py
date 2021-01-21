import hashlib
import json, requests, re, time

import MySQLdb
from lxml import etree
from Crawl.enginee.ip_agent import get_ip, check_ip


def md5_jm(v):
    md5 = hashlib.md5()
    md5.update(v.encode())
    md5_v = str(md5.hexdigest())
    return md5_v


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


provinces = ['bj', 'tj', 'he', 'sx', 'nm', 'ln', 'jl', 'hl', 'sh', 'js', 'zj', 'ah', 'fj', 'jx', 'sd', 'hn', 'hb', 'gd',
             'gx', 'hi', 'cq', 'sc', 'gz', 'yn', 'xz', 'sn', 'gs', 'qh', 'nx', 'xj']
s_time = int(time.time())  # 起始时间
ip = get_ip()[0]  # 起始ip
conn = connection_mysql()
counts = 0
for pro in provinces:  # 遍历省份列表
    start_url = 'http://www.zgazxxw.com/{}-000101c7-0.html'.format(pro)  # 列表页url
    s_time, ip = check_ip(s_time, ip)  # 判断ip是否过期
    try:
        response = requests.get(start_url, proxies=ip).text
    except Exception as e:
        print(e)  # 爬取失败则放入队列重新爬取
        continue
    ele_response = etree.HTML(response)
    list_urls = ele_response.xpath('//*[@id="searchcontent"]/table/tbody/tr/td[1]/a/@href')
    head = 'http://www.zgazxxw.com'
    cursor = conn.cursor()
    while list_urls:
        li = list_urls.pop()
        url = head + li
        s_time, ip = check_ip(s_time, ip)
        try:
            res = requests.get(url, proxies=ip).text
        except Exception as e:
            list_urls.insert(0, li)
            continue
        ele_res = etree.HTML(res)
        rowkey = md5_jm(url)
        try:
            title = ele_res.xpath('//div[@class="list_content fl"]/h5/text()')[0]  # 项目名称
            money = ele_res.xpath('//table[@class="xfjs_bg"]/tbody/tr[3]/td[2]/text()')[0].strip()  # 投资金额(不一定都显示)
            publish_time = ele_res.xpath('//table[@class="xfjs_bg"]/tbody/tr[1]/td[4]/text()')[0].strip()  # 发布时间
            owner = ele_res.xpath('//table[@class="xfjs_bg"]/tbody/tr[4]/td[2]/text()')[0].strip()  # 业主
            nature = ele_res.xpath('//table[@class="xfjs_bg"]/tbody/tr[2]/td[2]/text()')[0].strip()  # 项目性质
            project_data = ele_res.xpath('//div[@class="list_content fl"]/div[4]/text()')
            address = project_data[0]  # 项目所在地
            content = project_data[1].replace('\r\n\r\n', '').strip()  # 主要建设内容
            owner_phone = ele_res.xpath('//table[@class="xfjs_bg"]/tbody/tr[2]/td[2]/text()')[1]  # 业主方联系方式
        except Exception as e:
            print(e)  # 返回错误原因
            continue
        s_sql = 'insert into project_data values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        u_sql = 'update project_data set title=%s, url=%s, money=%s, publish_time=%s, owner=%s, nature=%s, address=%s, content=%s, owner_phone=%s where rowkey=%s'
        try:
            cursor.execute(s_sql,
                           [rowkey, title, url, money, publish_time, owner, nature, address, content, owner_phone])
        except:
            cursor.execute(u_sql,
                           [title, url, money, publish_time, owner, nature, address, content, owner_phone, rowkey])
        counts += 1
        print(counts)
    conn.commit()
