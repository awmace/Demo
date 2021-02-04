# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Item, Field


class ZgwGoodsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    p_id = Field()  # 站点id_spu_id_sku_id
    spu_id = Field()  # 详情页id
    sku_id = Field()  # sku_id，默认1
    p_customer_id = Field()  # 供方唯一id，来源_供方唯一标识
    p_customer_name = Field()  # 供应商名称
    p_spu_code = Field()  # spu编码，配置文件设置，不设置为空
    p_spu_name = Field()  # spu名称
    p_spu_pic = Field()  # spu产品图片地址
    source_name = Field()  # 来源网站名称
    p_three_category = Field()  # 末级类目名称
    p_three_category_code = Field()  # 末级类目对应万郡code
    p_brand_name = Field()  # 品牌名称
    p_sku_valuation_unit = Field()  # 计价单位，计量单位
    p_sku_auxiliary_unit = Field()  # 辅助单位
    p_sku_auxiliary_num = Field()  # 辅助单位数量
    p_sku_packaging_method = Field()  # 包装方式
    p_attribute = Field()  # 属性
    p_attribute_value = Field()  # 属性值
    p_sku_pic = Field()  # sku图片地址
    p_sku_url = Field()  # 商品详情页url
    p_sku_introduce_type = Field()  # sku介绍方式；1:图片2:文字3:文字＋图片
    p_sku_introduce = Field()  # sku产品
    p_price_num = Field()  # 起订量
    p_price = Field()  # 价格
    p_other_info = Field()  # 其他信息
    p_source = Field()  # 数据来源，1:1688
    p_version = Field()  # 数据版本号:20201015
    p_create_time = Field()  # 创建时间
    p_deleted = Field()  # 删除标识  0:未删除  1:已删除
    p_list_url = Field()
    category = Field()  # 商品对应的类目关系:>>连接
    c_enterprise_scope = Field()  # 企业经营范围，主营业务
    c_customer_introduce_type = Field()  # 企业介绍方式；1图片2文字3文字＋图片
    c_customer_introduce = Field()  # 文字
    c_customer_introduce_pic = Field()  # 图片
    c_customer_address = Field()  # 企业这册地址、企业所在地区
    c_customer_number = Field()  # 座机
    c_customer_phone = Field()  # 手机号
    c_customer_url = Field()  # 店铺首页url
    c_other_info = Field()  # 其他信息
    c_source = Field()  # 数据来源，1:1688
    c_version = Field()  # 数据版本号:20201015
    c_create_time = Field()  # 创建时间
    c_deleted = Field()  # 删除标识0:未删除1:已删除
    vandream_flag = Field()  # 是否符合万郡入库标准,1:符合0:不符合
    customer_follow_state = Field()  # 店铺跟进状态1:已入住 0:待跟进
    p_sku_introduce_pic = Field()  # 图片;
