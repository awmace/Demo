import json, requests
import random


def get_ip():
    re_ip = requests.get(
        'http://ip.ipjldl.com/index.php/api/entry?method=proxyServer.hdtiqu_api_url&packid=0&fa=0&groupid=0&fetch_key=&time=100&qty=1&port=1&format=json&ss=5&css=&dt=0&pro=&city=&usertype=4'
    ).json()
    ips = []
    for i in re_ip['data']:
        ip = 'http://' + i['IP'] + ':' + str(i['Port'])
        ips.append({'http': ip})
    return ips


def get_page_ip():
    re_ip = requests.get(
        'http://ip.ipjldl.com/index.php/api/entry?method=proxyServer.hdtiqu_api_url&packid=0&fa=0&groupid=0&fetch_key=&time=100&qty=1&port=1&format=json&ss=5&css=&dt=0&pro=&city=&usertype=4').json()
    ips = []
    for i in re_ip['data']:
        ip = 'http://' + i['IP'] + ':' + str(i['Port'])
        ips.append({'http': ip})
    return random.choice(ips)
