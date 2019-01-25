# -*- coding: utf-8 -*-
import scrapy


class LagouJobsSpider(scrapy.Spider):
    name = 'lagou_jobs'
    allowed_domains = ['lagou.com']
    start_urls = ['http://lagou.com/']

    def parse(self, response):
        pass
