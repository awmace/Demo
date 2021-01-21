import requests
from lxml import etree
from HXGG.sixct.ip_agent import get_ip, check_ip
import time


def relation(ns, t):
    ps = []
    switch = 1
    for index1, i in enumerate(t):
        if switch:
            if '，' in i:
                i = i + t[index1 + 1]
                ps.append(i)
                switch = 0
            else:
                ps.append(i)
        else:
            switch = 1
    dsz = '暂无'
    zjl = '暂无'
    dw = '暂无'
    for index, p in enumerate(ps):
        if '董事长' in p:
            dsz = ns[index]
        elif '执行董事' in p:
            dsz = ns[index]
        if '总经理' in p:
            zjl = ns[index]
        elif '经理' in p:
            zjl = ns[index]
        if '监事会主席' in p:
            dw = ns[index]
        elif '监事' in p:
            dw = ns[index]
    if dsz == zjl and zjl == dw:
        dsz = zjl = dw = ns[0]
    return dsz, zjl, dw


# 发送请求
def send_requests(url, tail, t_time, ip):
    list_urls = []
    while url:
        t_time, ip = check_ip(t_time, ip)
        list_res = requests.get(url, headers=headers, proxies=ip).text
        ele_list = etree.HTML(list_res)
        states = ele_list.xpath('//div[@class="result-list sv-search-container"]/div/div/div[3]/div[1]/div/text()')
        list_url = ele_list.xpath('//div[@class="result-list sv-search-container"]/div/div/div[3]/div[1]/a/@href')
        city = ele_list.xpath('//a[@class="button -normal -xs custom-space"]/text()')
        if city:
            city = city[0].split('：')[-1].strip()
        for index, sta in enumerate(states):  # 判断公司是否存在
            if '存续' == sta:
                list_urls.append(list_url[index])
        url = ele_list.xpath('//a[@class="num -next"]/@href')
        if url:
            url = url[0].split('key=')[0] + 'key=%E5%9F%8E%E6%8A%95%E5%85%AC%E5%8F%B8&base={}'.format(tail)
        else:
            return list_urls, t_time, ip, city


# 进入详情页
def parse_detail(item_list, t_time, ip, city):
    for url in item_list:
        t_time, ip = check_ip(t_time, ip)
        res = requests.get(url, headers=headers, proxies=ip)
        ele_res = etree.HTML(res.text)
        if res.status_code == 200:
            try:
                comp_name = ele_res.xpath('//h2[@class="name"]/text()')[0]  # 企业名称
                legal_entity = \
                    ele_res.xpath(
                        '//table[@class="table -striped-col -breakall"]/tbody//a[@class="link-click"]/text()')[
                        0]  # 法人
                only_code = ele_res.xpath(
                    '//table[@class="table -striped-col -breakall"]/tbody/tr[5]/td[2]/text()')[0]  # 社会统一信用代码/纳税人识别号
                address = ele_res.xpath(
                    '//table[@class="table -striped-col -breakall"]/tbody/tr[10]/td[2]/text()')[0]  # 注册地址
                phone = ele_res.xpath('//div[@class="f0"]/div[1]/span[4]/text()')[0]
                names = ele_res.xpath('//div[@id="_container_staff"]//table[@class="table"]/tbody/tr/td[2]//a/text()')
                positions = ele_res.xpath(
                    '//div[@id="_container_staff"]//table[@class="table"]/tbody/tr/td[3]/span/text()')
                d, z, j = relation(names, positions)  # 董事长，总经理，监事会主席
                print(comp_name, legal_entity, only_code, address, phone, d, z, j, city)
            except Exception as e:
                if '我们只是确认一下你不是机器人' in res.text:
                    yz = input('需要手动验证了!!!')
        else:
            yz = input('需要手动验证了!!!')
    return t_time, ip


if __name__ == '__main__':
    ip = get_ip()[0]
    t_time = int(time.time())
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36",
        "Cookie": 'TYCID=962f4000249811eb9e61bf3c7947de23; ssuid=1711976450; _ga=GA1.2.2111412679.1605152336; auth_token=eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxODUxMDc0NDgxOCIsImlhdCI6MTYwNTc3ODY2MywiZXhwIjoxNjM3MzE0NjYzfQ.Ipnh-8RtG8LkrMNQZGZRLfbIhDaxy1QGI7mkHluPAp0NYad3KDd_fisAhrmIHq_ywHGxIWOyPWr0HiE9VO5Tmg; tyc-user-info-save-time=1605778664546; tyc-user-phone=%255B%252218510744818%2522%252C%2522183%25201746%25203727%2522%255D; jsid=SEM-BAIDU-PZ-SY-20201109-BIAOTI; tyc-user-info={%22claimEditPoint%22:%220%22%2C%22vipToMonth%22:%22false%22%2C%22explainPoint%22:%220%22%2C%22personalClaimType%22:%22none%22%2C%22integrity%22:%2210%25%22%2C%22score%22:%221333%22%2C%22state%22:%225%22%2C%22messageShowRedPoint%22:false%2C%22announcementPoint%22:%220%22%2C%22surday%22:%22406%22%2C%22bidSubscribe%22:%22-1%22%2C%22vipManager%22:%220%22%2C%22onum%22:%223%22%2C%22discussCommendCount%22:%220%22%2C%22monitorUnreadCount%22:%2221%22%2C%22showPost%22:null%2C%22messageBubbleCount%22:0%2C%22claimPoint%22:%220%22%2C%22schoolAuthStatus%22:%222%22%2C%22userId%22:%2219968605%22%2C%22vipToTime%22:%221643174878148%22%2C%22scoreUnit%22:%22%22%2C%22redPoint%22:%220%22%2C%22myTidings%22:%220%22%2C%22companyAuthStatus%22:%222%22%2C%22originalScore%22:%221333%22%2C%22myAnswerCount%22:%220%22%2C%22myQuestionCount%22:%220%22%2C%22nickname%22:%22%E6%8C%AF%E4%BC%97%22%2C%22privateMessagePointWeb%22:%220%22%2C%22bossStatus%22:%222%22%2C%22privateMessagePoint%22:%220%22%2C%22isClaim%22:%220%22%2C%22yellowDiamondEndTime%22:%220%22%2C%22isExpired%22:%220%22%2C%22yellowDiamondStatus%22:%22-1%22%2C%22pleaseAnswerCount%22:%220%22%2C%22vnum%22:%2250%22%2C%22bizCardUnread%22:%220%22%2C%22mobile%22:%2218510744818%22%2C%22sysConfig%22:{%22state%22:%22ok%22%2C%22message%22:%22%22%2C%22special%22:%22%22%2C%22vipMessage%22:%22%22%2C%22isLogin%22:0%2C%22data%22:{%22companyCertificationStyle%22:0%2C%22stopZombieMonitor%22:%220%22%2C%22pleaseClaimButton%22:%221%22%2C%22increaseEntCertifiPrice%22:%220%22%2C%22uploadLog%22:%221%22%2C%22humanSearchAB%22:%22%22%2C%22claimLevelUpInCompany%22:%220%22%2C%22vipPageStyle%22:0%2C%22autoEventSave%22:%221%22%2C%22mySpaceDisplay%22:0%2C%22humanCardStyle%22:0%2C%22claimLevelUpInUserCenter%22:%220%22%2C%22sign-in%22:%221%22%2C%22appCompanyDetailPageVersion%22:0%2C%22humanDetailAB1018_ABConfig%22:%223%22%2C%22monitorUpgrade%22:{%22enabled%22:%221%22%2C%22buttonContent%22:%22%E5%8D%87%E7%BA%A7%E7%9B%91%E6%8E%A7%E6%95%B0%E9%87%8F%22}%2C%22companySearchAB_ABConfig%22:%222%2C4%2C6%2C7%2C9%2CA%2CB%2CC%22%2C%22vipPageStyleConfig%22:%2250%22%2C%22privilegeCount%22:%2225%22%2C%22claimSwitch%22:%221%22%2C%22baseInfoEditNotice%22:%22%E6%AF%8F%E6%9C%88%E5%8F%AF%E5%85%8D%E8%B4%B9%E6%8F%90%E4%BA%A41%E6%AC%A1%E5%9F%BA%E7%A1%80%E4%BF%A1%E6%81%AF%E4%BF%AE%E6%94%B9%22%2C%22humanDetailAB%22:%221%2C2%2C3%2C4%2C5%2C6%2C7%2C8%2C9%2C0%2CA%2CB%2CC%2CD%2CE%22%2C%22focusObj%22:{%22state%22:%22ok%22%2C%22message%22:%22%22%2C%22special%22:%22%22%2C%22vipMessage%22:%22%22%2C%22isLogin%22:0%2C%22errorCode%22:0%2C%22data%22:{%22month%22:12%2C%22year%22:2020%2C%22isOffline%22:false%2C%22day%22:27}}}}%2C%22token%22:%22eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxODUxMDc0NDgxOCIsImlhdCI6MTYwNTc3ODY2MywiZXhwIjoxNjM3MzE0NjYzfQ.Ipnh-8RtG8LkrMNQZGZRLfbIhDaxy1QGI7mkHluPAp0NYad3KDd_fisAhrmIHq_ywHGxIWOyPWr0HiE9VO5Tmg%22}; csrfToken=gx44clc2zAR_sFIzQhREZyS0; bannerFlag=true; Hm_lvt_e92c8d65d92d534b0fc290df538b4758=1607933965,1608104530,1608170416,1608775393; _gid=GA1.2.1539969803.1608775394; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22175dfdd4c52c7-046890c421ab5b-930346c-1049088-175dfdd4c532cd%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22%24device_id%22%3A%22175dfdd4c52c7-046890c421ab5b-930346c-1049088-175dfdd4c532cd%22%7D; RTYCID=efac1c0b987642069cef6acc37015c5d; CT_TYCID=f45ad1f71bfa40a9829b38c2eaae7ce3; acw_tc=2760821a16088679222373796e7bd756be8878c0099ac3f63fe009994dcb6d; acw_sc__v2=5fe5607b8a37f75769a94579ae216e4266e0692b; token=9640d69808a946cea2d6b5d6bb576a8f; _utm=6c0efc2de900448094e8b7c44d1dce8e; Hm_lpvt_e92c8d65d92d534b0fc290df538b4758=1608867990; cloud_token=a5097220eece47eea6a408d56a81acb8; cloud_utm=5be62800d9fc42dba0c33a890586cc2e',
        "Content-Type": "application/json; charset=UTF-8",
        "Accept-Encoding": "gzip, deflate, br",
    }
    provinces = ['bj', 'sh', 'tj', 'cq', 'heb', 'sx', 'nmg', 'ln', 'jl', 'hlj', 'js', 'zj', 'ah', 'fj', 'jx', 'sd',
                 'hen',
                 'hub',
                 'hun', 'gd', 'gx', 'sc', 'gz', 'yn', 'han', 'snx', 'gs', 'nx', 'qh', 'xj', 'xz']
    for pro in provinces:
        start_url = 'https://www.tianyancha.com/search/ocE?key=%E5%9F%8E%E6%8A%95%E5%85%AC%E5%8F%B8&base={}'.format(pro)
        comp_urls, t_time, ip, city = send_requests(start_url, pro, t_time, ip)
        t_time, ip = parse_detail(comp_urls, t_time, ip, city)
        print(pro)
