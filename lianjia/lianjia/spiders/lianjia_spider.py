# -*- coding: utf-8 -*-
import scrapy
from lianjia.items import LianjiaItem
import copy


class LianjiaSpiderSpider(scrapy.Spider):
    """链家租房数据爬虫
    """

    name = 'lianjia_spider'
    allowed_domains = ['www.lianjia.com']
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Cookie': 'lianjia_uuid=4252613a-4b28-4fe7-9d4a-b79a77b5256e; UM_distinctid=16891022919b3b-0cc69f20c15bb1-162a1c0b-1fa400-1689102291b4c0; select_city=440100; all-lj=c60bf575348a3bc08fb27ee73be8c666; lianjia_ssid=0f372352-169c-44ec-839d-4b552b2ae7ec; TY_SESSION_ID=4e457148-730c-444d-875d-57072a93fe16; Hm_lvt_9152f8221cb6243a53c83b956842be8a=1548826127; Hm_lpvt_9152f8221cb6243a53c83b956842be8a=1548826127; _smt_uid=5c51360f.13ca157b; _jzqa=1.4490426498873662000.1548826128.1548826128.1548826128.1; _jzqc=1; _jzqx=1.1548826128.1548826128.1.jzqsr=bing%2Ecom|jzqct=/.-; _jzqckmp=1; CNZZDATA1255849599=1455905830-1548824537-https%253A%252F%252Fwww.bing.com%252F%7C1548824537; CNZZDATA1254525948=1173821815-1548825516-https%253A%252F%252Fwww.bing.com%252F%7C1548825516; CNZZDATA1255633284=996010828-1548821209-https%253A%252F%252Fwww.bing.com%252F%7C1548821209; _qzja=1.1042461058.1548826127815.1548826127815.1548826127816.1548826127815.1548826127816.0.0.0.1.1; _qzjc=1; _qzjto=1.1.0; CNZZDATA1255604082=2128145077-1548825538-https%253A%252F%252Fwww.bing.com%252F%7C1548825538; _jzqb=1.1.10.1548826128.1; _qzjb=1.1548826127816.1.0.0.0; _ga=GA1.2.1444755448.1548826131; _gid=GA1.2.1683954879.1548826131; CNZZDATA1273627291=8375262-1548616372-%7C1548822975',
        'Host': 'gz.lianjia.com',
        'Referer': 'https://gz.lianjia.com/zufang/',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
    }

    def start_requests(self):
        urls = ['https://gz.lianjia.com/zufang/pg{}/'.format(i) for i in range(1, 4)]
        
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, headers=self.headers)

    def parse(self, response):
        for house in response.xpath('//div[@class="content__list--item"]'):
            item = LianjiaItem()
            title = house.xpath('.//p[@class="content__list--item--title twoline"]/a/text()').re_first(r'\n(.*)').strip()
            # 户型
            house_type = house.xpath('.//p[@class="content__list--item--des"]/text()').re(r'\n\s*(.*)\s*')[-1].strip()
            # 面积
            area = house.xpath('.//p[@class="content__list--item--des"]/text()').re(r'\n\s*(.*)\s*')[-2].strip()
            # 租金
            rent = house.xpath('.//span[@class="content__list--item-price"]/em/text()').extract_first()
            # 地址
            location = ",".join(house.xpath('.//p[@class="content__list--item--des"]/a/text()').extract())
            # 标签
            label = ",".join(house.xpath('.//p[@class="content__list--item--bottom oneline"]/i/text()').extract())
            # 楼层
            floor = "".join(house.xpath('.//span[@class="hide"]/text()').re(r'\n\s*(\S*)\s*(\S*)\s*'))
            
            item['title'] = title
            item['house_type'] = "No datas" if house_type == "" else house_type
            item['area'] = area
            item['rent'] = rent + "元/月"
            item['location'] = "No datas" if location == "" else location
            item['label'] = label
            item['floor'] = "No datas" if floor == "" else floor

            # yield item
            detail_url = response.urljoin(house.xpath('.//p[@class="content__list--item--title twoline"]/a/@href').extract_first())
            requset = scrapy.Request(
                detail_url, callback=self.detail_parse, meta={'item': item}, dont_filter=True, priority=10)

    #         # detail_url = house.xpath('.//p[@class="content__list--item--title twoline"]/a/@href').extract_first()
    #         # requset = response.follow(detail_url, callback=self.detail_parse, dont_filter=True)
            yield requset

    def detail_parse(self, response):
        item = response.meta['item']
        print(item)
        # 房源发布时间
        release_time = "".join(response.xpath('//div[@class="content__subtitle"]/text()').re(r'(\d*-\d*-\d*)\s*'))
        # 租期
        rent_period = "".join(response.xpath('//li[@class="fl oneline"][5]/text()').extract())
        # 入住时间
        check_in = "".join(response.xpath('//li[@class="fl oneline"][3]/text()').extract())
        # 看房时间
        house_view_time = "".join(response.xpath('//li[@class="fl oneline"][6]/text()').extract())

        item['release_time'] = release_time
        item['rent_period'] = "No datas" if rent_period is None else rent_period
        item['check_in'] = "No datas" if check_in is None else check_in
        item['house_view_time'] = "No datas" if house_view_time is None else house_view_time
        yield item
