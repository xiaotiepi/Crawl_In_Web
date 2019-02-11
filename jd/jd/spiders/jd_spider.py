# -*- coding: utf-8 -*-
import scrapy
from jd.items import JdItem
from urllib.parse import urlencode


class JdSpiderSpider(scrapy.Spider):
    name = 'jd_spider'
    allowed_domains = ['www.jd.com']
    
    base_url = 'https://search.jd.com/Search?'
    page = 1
    params = {
            'keyword': '键盘',
            'enc': 'utf-8',
            'page': page,
            'click': '0',
            'wq': '键盘'
        }
    url = base_url + urlencode(params)

    def start_requests(self):
        yield scrapy.Request(
            url=self.url, callable=self.parse, meta={'page': self.page}, dont_filter=True)

    def parse(self, response):
        pass
