# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

import random
import time
from logging import getLogger
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from scrapy.http import HtmlResponse
# 导入信号和信号调度
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher


class JdUseragentMiddleware(object):
    '''
    UserAgents中间件
    使用时要在setting.py里先设置
    'scrapy.downloadermiddleware.useragent.UserAgentMiddleware': None
    并添加该中间件进去
    '''
    def __init__(self, settings):
        self.useragents = settings.get('USER_AGENTS')

    def process_request(self, request, spider):
        useragent = random.choice(self.useragents)
        request.headers['User-Agent'] = useragent
        print('现在使用的UA为：{}'.format(useragent))

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)


class JdDownloaderMiddleware(object):
    '''
    京东selenium对接scrapy中间件
    滚动条下拉到底后的sleep()参数建议2以上
    防止页面还没加载出来就翻页
    '''
    def __init__(self, settings):
        self.logger = getLogger(__name__)
        self.timeout = settings.get('SELENIUM_TIMEOUT')
        options = webdriver.ChromeOptions()
        # 设置中文
        options.add_argument('lang=zh_CN.UTF-8')
        # 设置无图加载 1 允许所有图片; 2 阻止所有图片; 3 阻止第三方服务器图片
        # prefs = {
        #     'profile.default_content_setting_values': {'images': 2}
        # }
        prefs = {'profile.managed_default_content_settings.images': 2}
        options.add_experimental_option('prefs', prefs)
        # 设置无头浏览器
        # options.add_argument('--headless')
        self.browser = webdriver.Chrome(chrome_options=options)
        # 设置等待请求网页时间最大为self.timeout
        self.wait = WebDriverWait(self.browser, self.timeout)
        self.browser.set_page_load_timeout(self.timeout)
        # spider启动信号和spider_opened函数绑定
        dispatcher.connect(self.spider_opened, signals.spider_opened)
        # spider关闭信号和spider_closed函数绑定
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    # 销毁内存时启用
    # def __del__(self):
    #     # print('关闭Chorme')
    #     self.logger.debug('关闭Chorme浏览器')
        # self.browser.close()

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s', spider.name)
        self.logger.debug('Chorme浏览器已打开')
    
    def spider_closed(self, spider):
        spider.logger.info('Spider closed: %s', spider.name)
        self.logger.debug('Chorme浏览器已关闭')
        self.browser.quit()
    
    def process_request(self, request, spider):
        """
        用chorme抓取页面
        :param request: Request对象
        :param spider: Spider对象
        :return: HtmlResponse
        """
        page = request.meta.get('page', 1)
        try:
            self.browser.get(request.url)
            # 滚动条下拉到底
            self.browser.execute_script('window.scrollTo(0,document.body.scrollHeight)')
            time.sleep(2)
            if page > 1:
                input = self.wait.until(EC.presence_of_element_located((By.XPATH, './/span[@class="p-skip"]/input')))
                submit = self.wait.until(EC.element_to_be_clickable((By.XPATH, './/span[@class="p-skip"]/a')))
                input.clear()
                input.send_keys(page)
                submit.click()
                self.browser.execute_script('window.scrollTo(0,document.body.scrollHeight)')
                time.sleep(2)
            # 如果当 str(page),即当前页码出现在高亮文本的时候，就代表页面成功跳转
            self.wait.until(
                EC.text_to_be_present_in_element((By.XPATH, './/span[@class="p-num"]/a[@class="curr"]'), str(page)))
            # 等待加载完所有的商品list 然后进一步解析
            self.wait.until(EC.presence_of_element_located((By.XPATH, './/ul[@class="gl-warp clearfix"]/li')))
            time.sleep(1)
            body = self.browser.page_source
            return HtmlResponse(url=request.url, body=body, encoding='utf-8', request=request)
        
        except Exception as E:
            print(str(E))
            return HtmlResponse(url=request.url, status=500, request=request)
