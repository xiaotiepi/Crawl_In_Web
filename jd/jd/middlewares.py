# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
# 导入 webdriver
from selenium import webdriver
from selenium.webdriver.common.by import By
# WebDriverWait库，负责循环等待
from selenium.webdriver.support.ui import WebDriverWait
# excepted_conditions类，负责条件出发
from selenium.webdriver.support import expected_conditions as EC

from scrapy.http import HtmlResponse
from scrapy.conf import settings
import random
import time


class JdUseragentMiddleware(object):
    def __init__(self):
        self.useragents = settings['USER_AGENTS']

    def process_request(self, request, spider):
        useragent = random.choice(self.useragents)
        # request.headers.setdefault('User-Agent', useragent)
        request.headers['User-Agent'] = useragent
        print(useragent)


class JdSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    def __init__(self, timeout=20):
        self.timeout = timeout
        # Chrome浏览器
        options = webdriver.ChromeOptions()
        # 设置中文
        options.add_argument('lang=zh_CN.UTF-8')
        # 设置无图加载 1 允许所有图片; 2 阻止所有图片; 3 阻止第三方服务器图片
        prefs = {
            'profile.default_content_setting_values': {'images': 2}
        }
        options.add_experimental_option('prefs', prefs)
        # 设置无头浏览器
        options.add_argument('--headless')
        self.browser = webdriver.Chrome(chrome_options=options)
        # 设置等待请求网页时间最大为self.timeout
        self.wait = WebDriverWait(self.browser, self.timeout)
        self.browser.set_page_load_time(self.timeout)
        self.logger.debug('Chorme浏览器已打开')

    def __del__(self):
        # print('关闭Chorme')
        self.logger.debug('关闭Chorme浏览器')
        self.browser.close()

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

    def process_request(self, request, spider):
        page = request.meta.get('page', 1)
        try:
            # print('Selenium启动解析')
            
            self.browser.get(request.url)
            # 滚动条下拉到底
            self.browser.execute_script('window.scrollTo(0,document.body.scrollHeight)')
            time.sleep(2)
            if page > 1:
                input = self.wait.until(EC.presence_of_element_located((By.XPATH, './/span[@class="p-skip"]/input')))  # 获取输入页面数框
                submit = self.wait.until(EC.element_to_be_clickable((By.XPATH, './/span[@class="p-skip"]/a')))  # 获取确定按钮
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
            print('selenium开始访问第'+str(page)+'页')

            return HtmlResponse(url=request.url, body=body, encoding='utf-8', request=request)
        
        except Exception as E:
            print(str(E))
            return HtmlResponse(url=request.url, status=500, request=request)


