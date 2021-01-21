import requests
from lxml import etree
from urllib import parse

class_encode = parse.quote('热轧H型钢')  # 编码转换
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
}
page_list_url = 'https://s.hc360.com/seller/search.html?kwd={}'.format(class_encode)
while page_list_url:
    response = requests.get(page_list_url, headers=headers)
    ele_response = etree.HTML(response.text)
    list_urls = ele_response.xpath('//div[@class="picmid pRel"]/a/@href')
    for li in list_urls:
        url = 'https:' + li
        print(url)
    page_list_url = ele_response.xpath('//span[@class="page_next page-n"]/a/@href')
    if page_list_url:
        page_list_url = 'https:' + page_list_url[0]
    print(page_list_url)
    break
