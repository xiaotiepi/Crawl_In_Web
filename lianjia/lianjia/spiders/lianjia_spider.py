# -*- coding: utf-8 -*-
import scrapy


class LianjiaSpiderSpider(scrapy.Spider):
    name = 'lianjia_spider'
    allowed_domains = ['www.lianjia.com']
    start_urls = ['http://www.lianjia.com/']

    def parse(self, response):
        pass
