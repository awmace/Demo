import json, requests

# m_comp = ['鸿路钢构',
#           '中建钢构',
#           '中铁高新',
#           '东南网架',
#           '上海宝冶',
#           '长江精工',
#           '江苏沪宁',
#           '杭萧钢构',
#           '二十二冶',
#           '中铁宝桥',
#           '中建二局',
#           '中铁山桥',
#           '山东重工',
#           '浙江精工',
#           '安徽鸿翔',
#           '潮峰钢构',
#           '多维联合',
#           '中铁九桥',
#           '湖南金海',
#           '安徽富煌']
a_comp = ['鸿路钢构', '中铁高新', '东南网架', '长江精工', '安徽富煌']
b_comp = [
    [
        '汝阳生产基地',
        '南川生产基地',
        '合肥生产基地',
        '金寨生产基地',
        '涡阳生产基地',
        '宣城生产基地',
        '蚌埠生产基地',
        '颍上生产基地'
    ],
    [
        '北京生产基地',
    ],
    [
        '浙江生产基地',
        '天津生产基地',
        '广州生产基地',
        '成都生产基地',
    ],
    [
        '上海生产基地',
        '安徽生产基地',
        '武汉生产基地',
        '广东生产基地',
        '北京生产基地',
        '浙江生产基地'
    ],
    [
        '合肥生产基地'
    ],
]
c_comp = [
    [
        '河南省汝阳市汝安路罗葛路口北行300米',
        '重庆市南神路',
        '安徽省合肥市长丰县魏武路1号',
        '安徽省六安市金寨县天堂湖路41号',
        '安徽省亳州市涡阳县兴业路与将军大道交叉口南150米',
        '安徽省宣城市宣州区凤萃路与青弋江西大道交叉路口往东约50米',
        '安徽省蚌埠市秦集镇金家洼',
        '安徽省阜阳市颍上县G345',
    ],
    [
        '北京市丰台区汽车博物馆东路一号院三号楼',
    ],
    [
        '浙江省杭州市萧山区衙前路428号',
        '天津市东丽区空港物流开发区西十四道31号',
        '广东省广州市番禺区石基镇石基村前锋路44号',
        '四川省成都市新津区兴园8路318'
    ],
    [
        '上海市黎安路999号大虹桥国际3032楼',
        '安徽省六安市金安区经济技术开发区长江精工工业园',
        '湖北省武汉市黄陂盘龙城楚天工业园',
        '广东省佛山市三水区锦翔路1号',
        '北京市朝阳区立水桥甲3号院立城苑小区10号楼',
        '浙江省绍兴市柯桥区鉴湖路1587号'
    ],
    [
        '安徽省合肥市巢湖市黄麓镇烔忠路富煌工业园'
    ],
]
comp_product = []
for comp_index, comp_name in enumerate(a_comp):
    for product_index, product_name in enumerate(b_comp[comp_index]):
        comp_product.append({'name': comp_name + product_name, 'address': c_comp[comp_index][product_index]})
for i in comp_product:
    param = {  # 地址编码参数
        'key': '24fd2a7bd631dc2f071f3c76f8e5b76a',
        'address': i['address'],
        'output': 'JSON'
    }
    res = requests.get('https://restapi.amap.com/v3/geocode/geo?parameters', params=param).json()  # 地图编码的请求
    j, w = res['geocodes'][0]['location'].split(',')  # 成功的返回结构
    i['lng'] = float(j)
    i['lat'] = float(w)
    del i['address']
comp_product = json.dumps(comp_product, ensure_ascii=False,indent=2)
print(comp_product)
