# -*- coding: utf-8 -*-
import json, requests
import re
import logging
import scrapy, time
from lxml import etree
from ..comm.dao import UseSQL
from ..items import ZgwGoodsItem
from ..comm.upload_picture import UploadPic
from ..comm.get_week_one import get_current_week

logger = logging.getLogger(__name__)
# 类目关系
category_2 = {
    "普卷": "热卷频道",
    "低合金卷": "热卷频道",
    "花纹卷": "热卷频道",
    "C料": "热卷频道",
    "带钢": "热卷频道",
    "船卷": "热卷频道",
    "优碳卷": "热卷频道",
    "汽车大梁卷": "热卷频道",
    "冷轧卷": "冷镀频道",
    "冷轧盒板": "冷镀频道",
    "轧硬卷": "冷镀频道",
    "镀锌卷": "冷镀频道",
    "镀铝锌卷": "冷镀频道",
    "酸洗卷": "冷镀频道",
    "有花镀锌卷": "冷镀频道",
    "无花镀锌卷": "冷镀频道",
    "镀锌板": "冷镀频道",
    "冷成型": "冷镀频道",
    "普板": "中厚板频道",
    "低合金板": "中厚板频道",
    "高强度船板": "中厚板频道",
    "船板": "中厚板频道",
    "碳结板": "中厚板频道",
    "耐磨板": "中厚板频道",
    "高建钢": "中厚板频道",
    "桥梁板": "中厚板频道",
    "锅炉容器板": "中厚板频道",
    "Z向板": "中厚板频道",
    "三级抗震螺纹钢": "建材频道",
    "三级抗震盘螺": "建材频道",
    "三级螺纹钢": "建材频道",
    "三级盘螺": "建材频道",
    "高线": "建材频道",
    "四级抗震盘螺": "建材频道",
    "五级抗震螺纹钢": "建材频道",
    "四级螺纹钢": "建材频道",
    "四级盘螺": "建材频道",
    "四级抗震螺纹钢": "建材频道",
    "H型钢": "型管频道",
    "T型钢": "型管频道",
    "扁钢": "型管频道",
    "不等边角钢": "型管频道",
    "等边角钢": "型管频道",
    "槽钢": "型管频道",
    "方矩管": "型管频道",
    "工字钢": "型管频道",
    "镀锌方管": "型管频道",
    "钢轨": "型管频道",
    "焊管": "型管频道",
    "钢护筒": "型管频道",
    "镀锌管": "型管频道",
    "螺旋管": "型管频道",
    "冷轧板": "不锈钢频道",
    "不锈钢冷轧板": "不锈钢频道",
    "不锈钢热轧平板": "不锈钢频道",
    "热轧板": "不锈钢频道",
    "型材": "不锈钢频道",
    "管材": "不锈钢频道",
    "钢带": "不锈钢频道",
    "零割板": "不锈钢频道",
    "弹簧钢": "圆钢频道",
    "建筑圆钢": "圆钢频道",
    "碳结钢": "圆钢频道",
    "钢绞线": "圆钢频道",
    "拉丝材": "圆钢频道",
    "普碳开平板": "开平板频道",
    "低合金开平板": "开平板频道",
    "出厂平板": "开平板频道",
    "花纹开平板": "开平板频道"}
# 类目编目关系
vandream_category_code_2 = {
    "三级抗震盘螺": "H01012001",
    "三级螺纹钢": "H01001002",
    "焊管": "H01001004",
    "三级抗震螺纹钢": "H01001002",
    "镀锌管": "H01013005",
    "高线": "H01012002",
    "三级盘螺": "H01012001",
    "等边角钢": "H01011004",
    "四级抗震螺纹钢": "H01001002",
    "建筑圆钢": "H01001003",
    "不等边角钢": "H01011004",
    "普碳钢": None,
    "普板": "H01009001",
    "槽钢": "H01011005",
    "不锈钢热轧平板": "H01017001",
    "普碳开平板": "H01010001",
    "不锈钢冷轧板": "H01017003",
    "工字钢": "H01001007",
    "高建钢": "H01009005",
    "普卷": "H01010001",
    "低合金板": "H01009002",
    "带钢": "H01010004",
    "碳结钢": None,
    "冷轧卷": "H01014007",
    "H型钢": "H01001009",
    "有花镀锌卷": "H01014002",
    "方矩管": "H01013004",
    "扁钢": "H01001008",
    "钢轨": "H01011007",
    "低合金卷": "H01010002",
    "冷轧带肋盘螺": "H01012003",
    "镀锌卷": "H01014002",
    "冷轧盒板": None,
    "花纹卷": "H01010003",
    "酸洗卷": None,
    "不锈钢管材": "H01011",
    "不锈钢热轧卷": "H01017002",
    "螺旋管": "H01013003",
    "无花镀锌卷": "H01014002",
    "彩涂卷": "H01016001",
    "方钢": "H01011",
    "船板": "H01009003",
    "重轨": "H01011007",
    "镀锌角钢": "H01011004",
    "不锈钢冷轧卷": "H01017004",
    "冷成型": None,
    "C料": None,
    "无缝管": "H01013001",
    "低合金开平板": "H01010002",
    "镀锌板": "H01014001",
    "合结钢": None,
    "镀锌槽钢": "H01011005",
    "镀锌工字钢": "H01011003",
    "冷拉方钢": None,
    "冷拉扁钢": None,
    "冷拉圆钢": None,
    "花纹开平板": "H01010003",
    "镀锌方管": "H01013004",
    "锅炉容器板": "H01009006",
    "耐磨板": None,
    "耐候钢板": "H01009",
    "耐酸钢": "H01009",
    "轧硬卷": "H01009",
    "铬钼钢": None,
    "齿轮钢": None,
    "Z向板": None,
    "高强度船板": "H01009003",
    "高强板": None,
    "不锈钢型材": None,
    "黑棒": None,
    "割方": None,
    "冷扁": None,
    "割圆": None,
    "六角棒": None,
    "碳结板": None,
    "鱼尾板": None,
    "四级抗震盘螺": "H01012001",
    "低合金高强度结板": "H01009002",
    "五级抗震螺纹钢": "H01001002",
    "T型钢": "H01011001",
    "锚杆钢": None,
    "冷拉六角钢": None,
    "镀铝锌卷": "H01014004",
    "汽车大梁卷": None,
    "汽车钢": None,
    "钢绞线": "H01012006",
    "四级螺纹钢": "H01001002",
    "桥梁板": "H01009004",
    "锌铁合金卷": None,
    "电镀锌卷": "H01014002",
    "船中板": "H01009003",
    "酸洗板": None,
    "出厂平板": None
}
# 属性编码对照
vandream_attribute_code_2 = {
    "是否预售": None,
    "交货期": "NX100050",
    "品名": "NX000010",
    "材质": "NX000015",
    "规格": "NX000003",
    "钢厂": "NX002091",
    "计价单位": None,
    "质量等级": "NX100280",
    "生产工艺": None,
    "表面工艺": None,
    "出厂日期": None,
    "仓库": "NX100276",
    "公差": None,
    "计量方式": None,
    "加工工艺": None,
    "切割状态": None,
    "涂层": "NX100814",
    "环保工艺": None,
    "成分": None,
    "焊接": None,
    "横截面": None,
    "退火工艺": None,
    "深冲等级": None,
    "锌层": "NX100813",
    "涂油": None,
    "颜色": "NX000005",
    "卷径": None,
    "表面等级": "NX000042"
}
p_list_s = 'https://zmall.zhaogang.com/?pn={}&ps=50&qz=true&ct=zg_arr_countrywide'

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
}


class Save_ZgwSpider(scrapy.Spider):
    name = 'zgw_url'

    def __init__(self):
        self.head_url = 'https://b2b.homedo.com/product/directsearch/newSearch'  # 列表页url
        self.source = 2
        self.user = UseSQL(self.source)
        self.table_id = None

    def start_requests(self):
        result = self.user.get_product()
        if result[1] != None:
            logger.info(str(self.source) + '站点，已经存在生产者')
        else:
            count, self.table_id = self.user.tobe_product()
            url = 'https://zmall.zhaogang.com/?pn=1&ps=50&qz=true&ct=zg_arr_countrywide'
            yield scrapy.Request(url, callback=self.save_list_url, headers=headers)

    def save_list_url(self, response):
        if self.table_id:
            ele_response = etree.HTML(response.text)
            page_num = ele_response.xpath('//div[@class="page-num"]/text()')[0].strip().split('/')[-1]
            for page in range(1, int(page_num) + 1):
                p_list_url = p_list_s.format(page)
                self.user.insert_url_by_id(self.table_id, p_list_url)


class ZgwSpider(scrapy.Spider):
    name = 'zgw'

    def __init__(self):
        self.user = UseSQL(2)
        self.goods = 0
        self.source_name = '找钢网'
        self.source = 2
        self.version = get_current_week()
        self.sku_id = 1
        self.u = UploadPic()

    def start_requests(self):
        # 消费url
        while True:  # 循环获取列表页url
            result = self.user.get_product()
            if result[1] == None:
                break
            else:
                # 删除此条记录
                id = result[1].get('id')  # 表中id,根据表中id删除数据
                p_list_url = result[1].get('url')
                res = self.user.delete_url_by_id(id)  # 根据id删除表中数据
                if res:
                    logger.info("delete success count:" + str(result))
                    yield scrapy.Request(p_list_url, headers=headers, callback=self.parse,
                                         meta={'p_list_url': p_list_url})
                else:
                    logger.info('其它消费者消费了数据:' + str(p_list_url))

    def parse(self, response):
        meta = response.meta
        ele_response = etree.HTML(response.text)
        list_urls = ele_response.xpath('//a[@class="shop-title"]/@href')  # 获取详情页url
        meta['shop_names'] = ele_response.xpath('//a[@class="shop-link"]/@href')  # 店铺url关键部分信息
        meta['titles'] = ele_response.xpath('//div[@class="shop-bio"]/a/span/text()')
        meta['address'] = ele_response.xpath('//div[@class="detail-cont-wrap"]/div[2]/span[2]/text()')  # 企业详细地址
        meta['ele_response'] = ele_response
        for index, li in enumerate(list_urls):  # 遍历详情页url
            data = ZgwGoodsItem()
            data['p_id'] = str(self.source) + '_' + li.split('/')[-1] + '_' + str(self.sku_id)
            data['spu_id'] = li.split('/')[-1]
            data['sku_id'] = self.sku_id
            data['source_name'] = self.source_name
            data['p_sku_url'] = 'https://zmall.zhaogang.com' + li
            meta['index'] = index
            meta['data'] = data
            yield scrapy.Request(data['p_sku_url'], headers=headers, callback=self.details_a, meta=meta)

    def details_a(self, response):  # 商品详情页
        meta = response.meta  # 接受上一个函数传过来的参数
        ele_res = etree.HTML(response.text)  # 解析商品详情页
        data = meta['data']
        data['p_source'] = self.source
        data['c_source'] = self.source
        data['p_version'] = self.version
        data['c_version'] = data['p_version']
        data['p_list_url'] = meta['p_list_url']
        data['p_spu_name'] = ele_res.xpath('//span[@class="title"]/text()')[0]
        data['p_three_category'] = data['p_spu_name'].split(' ')[0]
        data['p_three_category_code'] = vandream_category_code_2.get(data['p_three_category'])
        superior = category_2.get(data['p_three_category'])
        if not superior:
            data['category'] = data['p_three_category']
        else:
            data['category'] = superior + '>>' + data['p_three_category']
        # 图片处理
        spu_pic_url = ele_res.xpath('//meta[@name="og:image"]/@content')[0].split('?')[0]
        data['p_spu_pic'] = self.u.generate(spu_pic_url)
        data['p_price'] = float(ele_res.xpath('//span[@class="num"]/text()')[0].strip())
        data['p_sku_valuation_unit'] = ele_res.xpath('//span[@class="sep"]/text()')[1].split('/')[-1]
        p_price_num = ele_res.xpath('//td[@class="sku-item-td info-box"]/div[1]/text()')[0].split(' ')[0]
        data['p_price_num'] = float(re.sub('[\u4e00-\u9fa5]', '', p_price_num))
        data['p_sku_pic'] = data['p_spu_pic']
        attribute_num = ele_res.xpath('//div[@class="params-item fl"]')
        data['p_attribute'] = ele_res.xpath('//span[@class="label fl"]/text()')
        p_attribute_value = dict()
        p_brand_name = ele_res.xpath('//div[@class="params-data clearfix"]/div[5]/span[@class="value fl"]/text()')
        if p_brand_name:
            data['p_brand_name'] = p_brand_name[0]
        else:
            data['p_brand_name'] = '自营'
        for i in range(len(attribute_num)):
            value = ele_res.xpath(
                '//div[@class="params-data clearfix"]/div[{}]/span[@class="value fl"]/text()'.format(i + 1))
            if value:
                p_attribute_value[data['p_attribute'][i]] = value[0].strip()
            else:
                p_attribute_value[data['p_attribute'][i]] = '——'
        data['p_attribute'] = json.dumps(data['p_attribute'], ensure_ascii=False)
        data['p_attribute_value'] = json.dumps(p_attribute_value, ensure_ascii=False)
        data['p_sku_introduce_type'] = 0
        data['p_sku_introduce'] = None  # 只存文字
        data['p_sku_introduce_pic'] = None  # 图片url
        shop_name = meta['shop_names'][meta['index']]
        data['p_customer_id'] = '2_' + shop_name.split('/')[-1]
        data['c_customer_url'] = 'https://zmall.zhaogang.com' + shop_name + '/search?pn=1&ps=50&qz=true'
        data['p_customer_name'] = meta['titles'][meta['index']]
        data['c_customer_address'] = meta['address'][meta['index']].strip()
        phone = meta['ele_response'].xpath(
            '//div[@class="gc-item-table-list"]/div[{}]//div[@class="detail-cont-wrap"]/div[4]/span[2]/text()'.format(
                meta['index'] + 1))
        if phone:  # 判断存在不存在
            data['c_customer_phone'] = re.findall('1[35789]\d{8,9}', phone[0], re.S)
            data['c_customer_number'] = re.findall('0[1-9]\d{2,3}-[0-9]\d{6,8}', phone[0], re.S)
            data['c_customer_phone'] = data['c_customer_phone'][0] if data['c_customer_phone'] else None
            data['c_customer_number'] = data['c_customer_number'][0] if data['c_customer_number'] else None
        else:
            pass
        data['c_customer_introduce_type'] = 0
        if data.get('c_customer_number'):
            data['vandream_flag'] = 1  # 类目符合
        else:
            data['vandream_flag'] = 0  # 类目不符合
        yield scrapy.Request(data['c_customer_url'], headers=headers, callback=self.details_b, meta=meta,
                             dont_filter=True)

    def details_b(self, response):
        ele_res_c = etree.HTML(response.text)
        data = response.meta['data']
        data['c_enterprise_scope'] = ele_res_c.xpath('//div[@class="detail"]/div[3]/div[2]/text()')
        if data['c_enterprise_scope']:
            data['c_enterprise_scope'] = data['c_enterprise_scope'][0]
        else:
            data['c_enterprise_scope'] = '暂无信息'
        data['p_create_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        data['c_create_time'] = data['p_create_time']
        data['p_deleted'] = 0
        data['c_deleted'] = 0
        data['customer_follow_state'] = 0
        yield data
