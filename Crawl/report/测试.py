import json, requests

s = [
    {
        "url": "http://www.crhic.cn/news_view.aspx?TypeId=4&Id=1010&Fid=t2:4:2",
        "para": {
            "title": "中铁工业总经理李建斌当选中国工程机械工业协会副会长",
            "time": "2020-11-24"
        }
    },
    {
        "url": "http://www.crhic.cn/news_view.aspx?TypeId=4&Id=1009&Fid=t2:4:2",
        "para": {
            "title": "中铁工业两个项目获国家工信部政策性支持",
            "time": " 2020-11-24"
        }
    },

    {
        "url": "http://www.crhic.cn/news_view.aspx?TypeId=4&Id=1008&Fid=t2:4:2",
        "para": {
            "title": "世界首组时速600公里高速磁浮道岔完成现场架设",
            "time": "2020-11-24"
        }
    },
    {
        "url": "http://www.crhic.cn/news_view.aspx?TypeId=4&Id=1007&Fid=t2:4:2",
        "para": {
            "title": "李军平获钢结构建造领域最高荣誉“钢结构大师”称号",
            "time": "2020-11-24"
        }
    },
    {
        "url": "http://www.crhic.cn/news_view.aspx?TypeId=4&Id=1006&Fid=t2:4:2",
        "para": {
            "title": "世界首创——矿用TBM将应用于高瓦斯煤矿巷道掘进",
            "time": "2020-11-24"
        }
    },
    {
        "url": "http://www.crhic.cn/news_view.aspx?TypeId=4&Id=1004&Fid=t2:4:2",
        "para": {
            "title": "“春风”捎来好消息，掘进突破一千米",
            "time": "2020-11-24"
        }
    },
    {
        "url": "http://www.crhic.cn/news_view.aspx?TypeId=4&Id=1003&Fid=t2:4:2",
        "para": {
            "title": "践行“三个转变”新成果 || 工业制造铸就瑞典新地标！",
            "time": "2020-11-10"
        }
    },
    {
        "url": "http://www.crhic.cn/news_view.aspx?TypeId=4&Id=1002&Fid=t2:4:2",
        "para": {
            "title": "中铁工业迅速掀起学习宣传贯彻党的十九届五中全会精神热潮",
            "time": "2020-11-10"
        }
    },
    {
        "url": "http://www.crhic.cn/news_view.aspx?TypeId=4&Id=1001&Fid=t2:4:2",
        "para": {
            "title": "践行“三个转变”新成果 || 首台使用国产3米级主轴承盾构机试掘进通过验收",
            "time": "2020-11-10"
        }
    },

    {
        "url": "http://www.crhic.cn/news_view.aspx?TypeId=4&Id=1000&Fid=t2:4:2",
        "para": {
            "title": "中铁工业三季度报告出炉",
            "time": "2020-11-10"
        }
    },
    {
        "url": "http://www.crhic.cn/news_view.aspx?TypeId=4&Id=999&Fid=t2:4:2",
        "para": {
            "title": "践行“三个转变”新成果 | 中铁工业荣获首个“中国标准创新贡献奖”",
            "time": "2020-10-28"
        }
    },
    {
        "url": "http://www.crhic.cn/news_view.aspx?TypeId=4&Id=998&Fid=t2:4:2",
        "para": {
            "title": "中铁工业举办第三期领导干部理想信念培训班",
            "time": "2020-10-28"
        }
    },
    {
        "url": "http://www.crhic.cn/news_view.aspx?TypeId=4&Id=997&Fid=t2:4:2",
        "para": {
            "title": "穿过可可西里、翻越唐古拉山，拉萨首座高架钢箱梁桥成功首架",
            "time": "2020-10-28"
        }
    },
    {
        "url": "http://www.crhic.cn/news_view.aspx?TypeId=4&Id=996&Fid=t2:4:2",
        "para": {
            "title": "中铁工业舒伟浩荣获“中央企业抗击新冠肺炎疫情先进个人”",
            "time": "2020-10-28"
        }
    },
    {
        "url": "http://www.crhic.cn/news_view.aspx?TypeId=4&Id=995&Fid=t2:4:2",
        "para": {
            "title": "世界最大矩形盾构机“南湖号”顺利实现全线贯通",
            "time": "2020-10-28"
        }
    },
    {
        "url": "http://www.crhic.cn/news_view.aspx?TypeId=4&Id=994&Fid=t2:4:2",
        "para": {
            "title": "中铁工业“十四五”战略研讨会暨党委理论学习中心组（扩大）学习会在京召开",
            "time": " 2020-10-28"
        }
    },
    {
        "url": "http://www.crhic.cn/news_view.aspx?TypeId=4&Id=993&Fid=t2:4:2",
        "para": {
            "title": "中铁工业2020年前三季度完成新签合同额309.67亿元，同比增长35.26%",
            "time": "2020-10-28"
        }
    },
    {
        "url": "http://www.crhic.cn/news_view.aspx?TypeId=4&Id=991&Fid=t2:4:2",
        "para": {
            "title": "国内最大海上风机导管架顺利交付",
            "time": "2020-10-09"
        }
    },
    {
        "url": "http://www.crhic.cn/news_view.aspx?TypeId=4&Id=990&Fid=t2:4:2",
        "para": {
            "title": "小天鹅”号海上风力发电稳桩平台开合试验取得圆满成功",
            "time": "2020-10-09"
        }
    },
    {
        "url": "http://www.crhic.cn/news_view.aspx?TypeId=4&Id=989&Fid=t2:4:2",
        "para": {
            "title": "世界首台超小转弯半径硬岩TBM实现全线贯通",
            "time": "2020-10-09"
        }
    },
    {
        "url": "http://www.crhic.cn/news_view.aspx?TypeId=4&Id=976&Fid=t2:4:2",
        "para": {
            "title": "我国首台使用国家强基工程国产主轴承盾构成功始发",
            "time": "2020-09-28"
        }
    },
    {
        "url": "http://www.crhic.cn/news_view.aspx?TypeId=4&Id=975&Fid=t2:4:2",
        "para": {
            "title": "中铁工业与浪潮集团签订战略合作协议",
            "time": "2020-09-28"
        }
    },
    {
        "url": "http://www.crhic.cn/news_view.aspx?TypeId=4&Id=969&Fid=t2:4:2",
        "para": {
            "title": "中铁工业自主研发出智能储能供电系统",
            "time": "2020-09-07"
        }
    },
    {
        "url": "http://www.crhic.cn/news_view.aspx?TypeId=4&Id=968&Fid=t2:4:2",
        "para": {
            "title": "中铁工业党委调整中铁山桥主要领导",
            "time": "2020-09-07"
        }
    },
    {
        "url": "http://www.crhic.cn/news_view.aspx?TypeId=4&Id=967&Fid=t2:4:2",
        "para": {
            "title": "中铁工业荣获上市公司信息披露“三连A”",
            "time": "2020-09-02"
        }
    },
    {
        "url": "http://www.crhic.cn/news_view.aspx?TypeId=4&Id=966&Fid=t2:4:2",
        "para": {
            "title": "国产大直径盾构机“孪生”4兄弟全部顺利下线",
            "time": "2020-09-02"
        }
    },
    {
        "url": "http://www.crhic.cn/news_view.aspx?TypeId=4&Id=965&Fid=t2:4:2",
        "para": {
            "title": "承压上扬！中铁工业2020年上半年业绩亮眼",
            "time": "2020-09-02"
        }
    },
    {
        "url": "http://www.crhic.cn/news_view.aspx?TypeId=4&Id=964&Fid=t2:4:2",
        "para": {
            "title": "中铁工业代表队包揽全国行业职业技能竞赛团体、个人总成绩、青年组个人总成绩三项第一",
            "time": "2020-09-02"
        }
    },
    {
        "url": "http://www.crhic.cn/news_view.aspx?TypeId=4&Id=963&Fid=t2:4:2",
        "para": {
            "title": "实力见证！中铁工业参建的四个桥梁项目获2020年桥梁界国际大奖",
            "time": " 2020-09-02"
        }
    },
    {
        "url": "http://www.crhic.cn/news_view.aspx?TypeId=4&Id=962&Fid=t2:4:2",
        "para": {
            "title": "钱永刚到中铁工业讲述“钱学森创新事迹”",
            "time": "2020-09-02"
        }
    }
]
result = []
for i in s:
    if i.get('para') and len(result) < 10:
        d = dict()
        d['1'] = i['para']['title']
        d['2'] = i['url']
        d['3'] = i['para']['time']
        d['4'] = '企业官网'
        result.append(d)
    else:
        break
s_url = 'http://47.113.200.109:3012/digital-oc/dataset/data/list/'
header = {'Content-Type': 'application/json;charset=utf-8'}  # 请求头
rowKey = input('请输入企业统一信用代码:')
result_json = json.dumps(result, ensure_ascii=False)
target_json = json.dumps({"tableName": "company", "dataList": [{'rowKey': rowKey, 'dynamic': result_json}]},
                         ensure_ascii=False)  # 未处理的数据
res = requests.post(s_url, data=target_json.encode('utf-8'), headers=header)
