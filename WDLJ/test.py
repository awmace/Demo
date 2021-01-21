import MySQLdb, re
import requests, time, json
from lxml import etree
from urllib import parse
import pandas as pd

data = {"source": "all50keyword",
        "searchType": "1",
        # "showSubProduct": False,
        "keyword": "",
        "categoryId": "",
        "categoryLevel": '3',
        "brandId": "",
        "showFlag": "1,3",
        "selectType": '2',
        "productSource": "",
        "deliveryAddress": "",
        "propertys": "",
        "startPrice": "",
        "endPrice": "",
        "isExcludeMianYi": "",
        "isCustom": "",
        "promotionChannelType": "2",
        "isExcludeJiCai": "1",
        "appId": "110001",
        "platform": "pc",
        "ip": "113.116.187.55, 113.96.140.72, 118.178.15.112",
        "sortBy": "vcdesc",
        "page": '1',
        "pageSize": '40'}
headers = {'x-csrf-token': '1ymHTzYJZCRR40ZNryeTWYGW',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
           'Cookie': 'homedoLogCID=1b3d31e2-0783-4887-bb20-a2151b50bb50; homedoLogTID=7ee66c37-1986-4fd0-ab2e-8948d71e4d09; homedoLogFpth=https%3A%2F%2Fb2b.homedo.com%2Fproduct%2Fsearch%3FcategoryId%3D10028; homedoLogFpthST=1611023333297; ARK_ID=JS8939d0c90ce7bcb8fd6c7e996acad37f8939; HMD_R=160973825985188122; UM_distinctid=176cbe090e4ab3-0fb0f6f2a435bf-c791039-240000-176cbe090e5d18; gr_user_id=a026e177-e9f0-41b2-ba76-4f37873b7aa2; grwng_uid=478f95b2-af76-49aa-ba80-50c6bf8a8c03; NTKF_T2D_CLIENTID=guest4B38EA92-E7EA-7836-A72C-CBE0AC385551; OriginCode=%3futm_source%3dwmt_sem_baidupc%26utm_medium%3dCPC%26utm_term%3d180524%26utm_content%3d180009516%26utm_campaign%3d18013&2021/1/18 17:42:47; Hm_lvt_d1d21a226b3b6cbb96842713353fc9f7=1609738261,1610326869,1610933466,1610962970; csrfToken=1ymHTzYJZCRR40ZNryeTWYGW; BrowseInfo=100595464; acw_tc=76b20f6316110227270182972e2bfcc9a7781766db97114ec91d5ae8970991; ARK_STARTUP=eyJTVEFSVFVQIjp0cnVlLCJTVEFSVFVQVElNRSI6IjIwMjEtMDEtMTkgMTA6MTg6NDkuNzUzIn0%3D; CNZZDATA1257983938=1843867308-1609734998-https%253A%252F%252Fwww.homedo.com%252F%7C1611019571; calendarData=19; a016ee4c2a76b6bb_gr_session_id=e4b92ae3-ac5f-40bb-a585-a5b5aab249ff; a016ee4c2a76b6bb_gr_session_id_e4b92ae3-ac5f-40bb-a585-a5b5aab249ff=true; calendarProp=true; browseNumber=%5B%7B%22aId%22%3A0%2C%22num%22%3A8%7D%5D; FZ_STROAGE.homedo.com=eyJBUktTVVBFUiI6eyJwbGF0Zm9ybV9leHRyYSI6IlBDIn0sIlNFRVNJT05JRCI6IjMxNWI2MGUzNDFkYzMyOGMiLCJTRUVTSU9OREFURSI6MTYxMTAyMzMzMjgyOCwiQU5TQVBQSUQiOiI2NmYyNzcwNGQzMTYyMjQ3IiwiQU5TJERFQlVHIjoyLCJBTlNVUExPQURVUkwiOiJodHRwczovL3Nkay5ob21lZG8uY29tIiwiRlJJU1REQVkiOiIyMDIxMDEwNCIsIkZSSVNUSU1FIjpmYWxzZSwiQVJLX0lEIjoiSlM4OTM5ZDBjOTBjZTdiY2I4ZmQ2YzdlOTk2YWNhZDM3Zjg5MzkiLCJBUktGUklTVFBST0ZJTEUiOiIyMDIxLTAxLTA0IDEzOjMxOjAwLjQwOCJ9; Hm_lpvt_d1d21a226b3b6cbb96842713353fc9f7=1611023333'}
head_url = 'https://b2b.homedo.com/product/directsearch/newSearch'
start_url = 'https://www.homedo.com/?utm_source=wmt_sem_baidupc&utm_medium=CPC&utm_term=180524&utm_content=180009516&utm_campaign=18013'
ele_start_response = etree.HTML(requests.get(start_url).text)
class_urls = ele_start_response.xpath('//ul[@class="menu-sun"]/li/p/a/@href')
# 获取类别首页url
for class_url in class_urls:
    if '\r\n' in class_url:
        class_url = re.sub('\r\n', '', class_url)
    if 'Id=' in class_url:
        cate_id = class_url.split('Id=')[1]
        data["categoryId"] = cate_id
        print(cate_id)
        print(requests.post(head_url, data=data, headers=headers).json()['data'][0]['docs'][0])
        #