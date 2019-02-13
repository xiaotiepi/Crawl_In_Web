# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JdItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 商品名
    name = scrapy.Field()
    # 价格
    price = scrapy.Field()
    # 店铺名
    store = scrapy.Field()
    # 评论数
    comment_num = scrapy.Field()
    # 是否自营
    jd_support = scrapy.Field()
    # 链接
    detail_url = scrapy.Field()

