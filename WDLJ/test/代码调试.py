import requests, json, time

d = {
    1: 'product_info',
    2: 'customer_info'
}
save_url = 'http://47.113.195.31:3012/digital-oc/subject/38/object/list/'
header = {'Content-Type': 'application/json'}  # 请求头
get_url = 'http://47.113.195.31:3012/digital-oc/query/record/traverse_record_n?table_id={}&num=7'
count_url = 'http://47.113.195.31:3012/digital-oc/query/product_info/tablename_count?tableName={}'
now_count = ''
old_data = requests.get(get_url).json()
print(old_data)

# for index, i in enumerate(p_list):
#     d = {'ROW': '', 'counts': '', 'increase': '', 'create_time': '', 'week': '', 'table_id': ''}
#     version = int(time.time()) - 86400 * index
#     create_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(version))
#     logo = logos[index]
#     if index == 0:
#         result = ['customer_{}'.format(str(version)), 111428, p_list[0], create_time, logo, table_id]
#     else:
#         result = ['customer_{}'.format(str(version)), 111428 - p_list[index - 1], p_list[index] - p_list[index - 1],
#                   create_time, logo, table_id]
#     keys = list(d.keys())
#     for k, key in enumerate(keys):
#         d[key] = result[k]
#     products.append(d)
# data1 = json.dumps(products, indent=2, ensure_ascii=False)  # 已经处理的数据
# print(data1)
# res1 = requests.post(p_url, data=data1.encode('utf-8'), headers=header)
# print(res1.text)
