# -*- coding: utf-8 -*-
import scrapy
from jd.items import JdItem
from urllib.parse import urlencode


class JdSpiderSpider(scrapy.Spider):
    name = 'jd_spider'
    allowed_domains = ['www.jd.com']
    base_url = 'https://search.jd.com/Search?'

    def start_requests(self):
        for keyword in self.settings.get('KEYWORDS'):
            for page in range(1, self.settings.get('MAX_PAGE')+1):
                params = {
                    'keyword': keyword,
                    'enc': 'utf-8',
                    'page': page,
                    'click': '0',
                    'wq': keyword
                    }
                url = self.base_url + urlencode(params)
                yield scrapy.Request(
                    url=url, callback=self.parse, meta={'page': page}, dont_filter=True)

    def parse(self, response):
        '''
        对selenium传来的页面进行解析
        :param response: response对象
        :return:
        '''
        products = response.xpath('//ul[@class="gl-warp clearfix"]/li')
        for product in products:
            item = JdItem()
            name = ''.join(product.xpath('.//div[@class="p-name p-name-type-2"]/a/em/text()').extract()).strip().replace(' ', '')
            price = product.xpath('.//div[@class="p-price"]//i/text()').extract()[0]
            store = ''.join(product.xpath('.//span[@class="J_im_icon"]/a/text()').extract())
            comment_num = product.xpath('.//div[@class="p-commit"]/strong/a/text()').extract()[0]
            detail_url = response.urljoin(product.xpath('.//div[@class="p-name p-name-type-2"]/a/@href').extract()[0])
            try:
                if product.xpath('.//div[@class="p-icons"]/i/text()').extract()[0] == '自营':
                    jd_support = '自营'
                else:
                    jd_support = '非自营'
            except Exception:
                jd_support = '非自营'
                
            item['name'] = name
            item['price'] = price
            item['store'] = store
            item['comment_num'] = comment_num
            item['detail_url'] = detail_url
            item['jd_support'] = jd_support
            yield item
