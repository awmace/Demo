import requests

url = 'http://47.113.195.31:3012/digital-oc/query/product_info/statis_by_date?days={}&table=customer_info'
li = []
for day in range(1, 16):
    response = requests.get(url.format(day)).json()[0]['value']
    li.append(int(response))
print(li)
poor = []
for index, i in enumerate(li):
    if index == 0:
        poor.append(None)
    else:
        li.append(i - li[index - 1])
