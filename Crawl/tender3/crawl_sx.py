import requests, json, hashlib, time, re
from lxml import etree
from Crawl.tender3.es1 import filter_data, set_data


def md5_jm(v):
    md5 = hashlib.md5()
    md5.update(v.encode())
    md5_v = str(md5.hexdigest())
    return md5_v


page_url = 'http://www.sxggzyjy.cn/jydt/001001/001001001/001001001001/subPage_jyxx.html'
while True:
    head_url = 'http://www.sxggzyjy.cn'
    response = requests.get(page_url).text
    ele_response = etree.HTML(response)
    titles = ele_response.xpath('//*[@id="categorypagingcontent"]/ul/li/a/@title')
    urls = ele_response.xpath('//*[@id="categorypagingcontent"]/ul/li/a/@href')
    pu_times = ele_response.xpath('//*[@id="categorypagingcontent"]/ul/li/span/text()')
    old_data = []
    for index, s in enumerate(urls):
        single = dict()
        url = head_url + s
        single['rowKey'] = md5_jm(url)
        res = requests.get(url).text
        ele_res = etree.HTML(res)
        single['title'] = titles[index]
        single['url'] = url
        single['publish_time'] = pu_times[index]
        single['crawl_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        single['source'] = '陕西省公共资源交易平台'
        single['d_type'] = '招标公告'
        single['elements'] = res
        single['text'] = re.sub(r'\s+|<.+?>', '', single['elements'])
        old_data.append(single)
    new_data = filter_data(old_data)
    print(json.dumps(new_data, indent=2, ensure_ascii=False))
    # set_data(old_data, new_data)
    next_page = ele_response.xpath('//*[@id="categorypagingcontent"]/div/ul/li[8]/a/@href')[0]
    page_url = head_url + next_page