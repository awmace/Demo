import requests, json, hashlib, time, re
from lxml import etree
from Crawl.tender3.es2 import filter_data, set_data


def md5_jm(v):
    md5 = hashlib.md5()
    md5.update(v.encode())
    md5_v = str(md5.hexdigest())
    return md5_v


page_list = ['about']
page_list.extend(list(range(2, 31)))
for page in page_list:
    page_url = 'http://www.hbbidcloud.cn/shengbenji/jyxx/004005/004005001/{}.html'.format(page)
    response = requests.get(page_url).text
    ele_response = etree.HTML(response)
    titles = ele_response.xpath('//*[@id="main"]/div/div[2]/ul/li/div/a/@title')
    urls = ele_response.xpath('//*[@id="main"]/div/div[2]/ul/li/div/a/@href')
    old_data = []
    for index, s in enumerate(urls):
        single = dict()
        url = 'http://www.hbbidcloud.cn' + s
        single['rowKey'] = md5_jm(url)
        res = requests.get(url).text
        ele_res = etree.HTML(res)
        try:
            single['title'] = re.findall('】(.*?)\(', titles[index])
            if single['title']:
                pass
            else:
                single['title'] = re.findall('】(.*?)\[', titles[index])
            single['title'] = single['title'][0]
            single['url'] = url
            single['publish_time'] = ele_res.xpath('/html/body/div[2]/div[2]/div/div[1]/text()[2]')[0].split('：')[-1]
        except:
            continue
        single['crawl_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        single['source'] = '湖北省公共资源交易平台'
        single['d_type'] = '中标结果公告'
        single['elements'] = re.findall('(<body>.*?</body>)', res, re.S)[0]
        single['text'] = re.sub(r'\s+|<.+?>', '', single['elements'])
        old_data.append(single)
    new_data = filter_data(old_data)
    print(json.dumps(new_data, indent=2, ensure_ascii=False))
    # set_data(old_data, new_data)

# with open('win.json', 'a', encoding='utf-8') as w:
#     json.dump(old_data, w, ensure_ascii=False, indent=2)
