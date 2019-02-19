# -*- coding: utf-8 -*-
import scrapy
from lagou.items import LagouItem


class LagouSpiderSpider(scrapy.Spider):
    '''
    拉钩职位数据爬虫
    '''
    name = 'lagou_spider'
    allowed_domains = ['lagou.com']
    headers = {
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Cookie': 'WEBTJ-ID=20181227220739-167effdfc0362a-021e18aff567df-162a1c0b-2073600-167effdfc041c; _ga=GA1.2.355303414.1545919659; user_trace_token=20181227220739-c4fdde43-09e0-11e9-ad84-5254005c3644; LGUID=20181227220739-c4fde4e6-09e0-11e9-ad84-5254005c3644; JSESSIONID=ABAAABAAAFCAAEG306C351D7F694112C64A149066A55419; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2216886a72a651373-03ebda91e54f2-162a1c0b-2073600-16886a72a66b07%22%2C%22%24device_id%22%3A%2216886a72a651373-03ebda91e54f2-162a1c0b-2073600-16886a72a66b07%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; index_location_city=%E6%B7%B1%E5%9C%B3; TG-TRACK-CODE=search_code; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1548447328; _gid=GA1.2.232714927.1548580356; X_MIDDLE_TOKEN=6bd49b3916d7881fec8452635998eb2a; SEARCH_ID=51e94ef850714833b6f82f4e282557c7; _gat=1; LGSID=20190127174331-018d928b-2218-11e9-b804-5254005c3644; PRE_UTM=; PRE_HOST=; PRE_SITE=; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Fzhaopin%2F; LGRID=20190127174340-070eeaea-2218-11e9-b804-5254005c3644; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1548582221',
        'Host': 'www.lagou.com',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
        }

    def start_requests(self):
        '''
        生成爬虫链接，最大30页
        '''
        urls = [
            'https://www.lagou.com/zhaopin/Python/{}/'.format(i) for i in range(1, 31)
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, headers=self.headers)

    def parse(self, response):
        '''
        解析页面,生成items
        '''
        for job in response.xpath('//ul[@class="item_con_list"]/li'):
            title = job.xpath('.//div[@class="p_top"]/a/h3/text()').extract_first()
            city = job.xpath('.//span[@class="add"]/em/text()').extract_first()
            salary_range = job.xpath('.//span[@class="money"]/text()').extract_first()
            experience, education = job.xpath('.//div[@class="li_b_l"]/text()').re(r'(.*)\s*/\s*(.*)')
            company = job.xpath('.//div[@class="company_name"]/a/text()').extract_first()
            tags = job.xpath('.//div[@class="li_b_r"]/text()').extract_first()
            industry, scale = job.xpath('.//div[@class="industry"]/text()').re(r'\n\s*(.*)/.*/\s*(.*)')

            item = LagouItem({
                'title': title,
                'city': city,
                'salary_range': salary_range,
                'experience': experience,
                'education': education,
                'company': company,
                'tags': tags,
                'industry': industry,
                'scale': scale
            })
            yield item
