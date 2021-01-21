from pyhanlp import *
from datetime import datetime
import hanlp, hashlib
import json
import time

# def md5_jm(v):
#     md5 = hashlib.md5()
#     md5.update(v.encode())
#     result = str(md5.hexdigest())
#     return result
# print(md5_jm('123'))

# 格式化显示当前时间：时间戳-》时间格式
# print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))

# GMT转datatime时间格式
# gmt = "Tue, 03 Nov 2020 00:00:00 GMT"
# GMT_FORMAT = '%a, %d %b %Y %H:%M:%S GMT'
# t = {'time': str(datetime.strptime(gmt, GMT_FORMAT))}
# print(t)

# json的保存与读取
# a = {'json': 12}
# b = {'妞': 12}
# with open('test6.json', 'a', encoding='utf-8') as w:
#     json.dump([a, b], w, indent=2, ensure_ascii=False)

# with open('test6.json', 'r',encoding='utf-8') as w:
#     s = json.load(w)
# print(s)

# xpath匹配实例
# from lxml import etree
#
# with open('新建文本文档.txt', 'r', encoding='utf-8')as r:
#     text = r.read()
# ele = etree.HTML(text)
# t = ele.xpath('//p/text()')
# print([i.strip() for i in t])

# 中文实体识别
# h = hanlp.load(hanlp.pretrained.ner.MSRA_NER_BERT_BASE_ZH)
# print(h(list(t)))
