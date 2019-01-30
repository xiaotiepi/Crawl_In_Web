# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LianjiaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    house_type = scrapy.Field()
    area = scrapy.Field()
    rent = scrapy.Field()
    location = scrapy.Field()
    label = scrapy.Field()
    release_time = scrapy.Field()
    floor = scrapy.Field()
    rent_period = scrapy.Field()
    check_in = scrapy.Field()
    house_view_time = scrapy.Field()
