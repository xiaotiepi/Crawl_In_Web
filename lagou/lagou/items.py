# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LagouItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    city = scrapy.Field()
    salary_range = scrapy.Field()
    experience = scrapy.Field()
    education = scrapy.Field()
    tags = scrapy.Field()
    company = scrapy.Field()
    industry = scrapy.Field()
    scale = scrapy.Field()
