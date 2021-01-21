import random, json,requests

n_id = 0
l_id = 0
m_comp = [['鸿路钢构', '165'],
          ['中建钢构', '104.5'],
          ['中铁高新', '100.6'],
          ['东南网架', '91.2'],
          ['上海宝冶', '76.1'],
          ['长江精工', '71.6'],
          ['江苏沪宁', '66'],
          ['杭萧钢构', '51.5'],
          ['二十二冶', '42'],
          ['中铁宝桥', '32'],
          ['中建二局', '28.5'],
          ['中铁山桥', '28.2'],
          ['山东重工', '28.2'],
          ['浙江精工', '26'],
          ['安徽鸿翔', '25.9'],
          ['潮峰钢构', '24.5'],
          ['多维联合', '24.3'],
          ['中铁九桥', '23.6'],
          ['湖南金海', '23.2'],
          ['安徽富煌', '22.2']]
up_comp = [['湖北金诺置业有限公司', '衢州市柯城区利民城乡建设投资开发有限责任公司', '宣城市盛鸿建筑科技有限公司', '涡阳县金诺置业有限公司'],
           ['上海市松江区教育局', '泰州市高港高新区开发建设有限责任公司', '济宁经开城建开发有限公司', '深圳锦洲工程管理有限公司'],
           ['北京轨道交通门头沟线投资有限责任公司', '福州中铁城置业有限公司', '贵阳市城市轨道交通有限公司', '闽侯县荆溪镇人民政府'],
           ['德清联创科技新城建设有限公司', '杭州市萧山区临浦镇人民政府', '乐清慢方适文化旅游有限公司'],
           ['重庆九黎旅游控股集团有限公司', '上海市奉贤区青村镇城镇建设管理事务中心', '广州市重点公共建设项目管理中心', '港投工程咨询有限公司'],
           ['安徽泫氏铸造有限责任公司', '国网青海省电力公司电力科学研究院', '杉杉时尚产业园宿迁有限公司', '南京世界村汽车动力有限公司'],
           ['海南云盛投资有限公司', '北京城建集团有限责任公司', '江苏京沪重工有限公司', '无锡公共工程建设中心建设单位'],
           ['宁波方太厨具有限公司', '上海奉贤二建股份有限公司', '山东泰和建设管理有限公司', '万邦国际农产品物流股份有限公司'],
           ['嘉兴市南湖区交投祥生房地产开发有限公司', '河北中鸿记食品科技有限公司', '邢东新区社会发展局', '徐州经济技术开发区金龙湖城市投资有限公司'],
           ['广东省高速公路有限公司深汕西分公司扩建管理处', '安徽省交通控股集团有限公司', '邯黄铁路有限责任公司', '中国铁路广州局集团有限公司工程管理所'],
           ['西安国际陆港文汇置业有限公司', '北京市通州区住房保障事务中心', '共青团阿坝县委', '深圳市罗湖人才安居有限公司'],
           ['中国铁路广州局集团有限公司江门工程建设指挥部', '中交第二公路工程局有限公司'],
           ['泰州市高港高新区开发建设有限责任公司'],
           ['丽水南城新泓产业开发有限责任公司', '鞍钢金固（杭州）金属材料有限公司', '绍兴市棒垒球场建设运营有限公司', '广州环投南沙环保能源有限公司'],
           ['贵州贵深投资发展有限公司'],
           ['杭州市临安区新锦产业发展集团有限公司', '杭州萧山经济技术开发区国有资产经营有限公司', '内蒙古盛乐文化产业发展投资有限公司'],
           ['多维绿建科技（天津）有限公司', '特变电工京津冀智能科技有限公司', '北京市第三建筑工程有限公司', '艾斯帝钢结构南通有限公司'],
           ['福州青口投资区开发建设有限公司', '贵州贵深投资发展有限公司', '中建宜昌伍家岗大桥建设运营有限公司'],
           ['常德经济技术开发区石门桥镇康家吉小学', '新邵县教育局', '常德金海装配式建筑集成技术有限公司'],
           ['安徽巢湖经济开发区诚信建设投资（集团）有限公司', '蜂巢动力系统（江苏）有限公司', '合肥海恒项目投资控股集团公司']]
nodes = []
links = []
for li in m_comp:
    m = dict()  # 竞争公司
    m['id'] = str(n_id)
    m['name'] = li[0]
    m['value'] = float(li[1]) / 2
    m['category'] = 0
    nodes.append(m)
    n_id += 1
for index, ups in enumerate(up_comp):
    for up in ups:
        u = dict()  # 甲方公司
        u['id'] = str(n_id)
        u['name'] = up
        u['value'] = random.randint(10, 25)
        u['category'] = random.randint(1, 6)
        nodes.append(u)
        n_id += 1
        link = dict()  # 关系
        link['id'] = str(l_id)
        link['source'] = str(index)
        link['target'] = u['id']
        links.append(link)
        l_id += 1
result = dict()
result['nodes'] = nodes
result['links'] = links
data = json.dumps([result], ensure_ascii=False, indent=2)
s_url = 'http://47.113.200.109:3012/digital-oc/dataset/data/list/'
header = {'Content-Type': 'application/json;charset=utf-8'}  # 请求头
data_json = json.dumps({"tableName": "competitive_relationship", "dataList": [{'rowKey': 'software1234', 'figure': data}]},
                       ensure_ascii=False)  # 已经处理的数据
res = requests.post(s_url, data=data_json.encode('utf-8'), headers=header)
print(res.status_code)

# nodes = []
# links = []
# for index, li in enumerate(m_comp):
#     m = dict()  # 目标公司
#     m['id'] = str(n_id)
#     m['name'] = li[0]
#     m['value'] = float(li[1])/2
#     m['category'] = 0
#     nodes.append(m)
#     n_id += 1
#     ups = up_comp[index]
#     for up in ups:
#         u = dict()  # 甲方公司
#         u['id'] = str(n_id)
#         u['name'] = up
#         u['value'] = random.randint(10, 25)
#         u['category'] = random.randint(1, 6)
#         nodes.append(u)
#         n_id += 1
#         link = dict()  # 关系
#         link['id'] = str(l_id)
#         link['source'] = m['id']
#         link['target'] = u['id']
#         links.append(link)
#         l_id += 1
# result = dict()
# result['nodes'] = nodes
# result['links'] = links
# print(json.dumps([result], ensure_ascii=False, indent=1))
