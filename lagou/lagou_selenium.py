from selenium import webdriver
from pymongo import MongoClient
from lxml import etree
import time
import re

'''
    拉钩的职位详细查询列表采用Ajax加载，在不登录的情况下post该接口会出现请求频繁，
    因此采用selenium进行爬虫也是一种选择（虽然比较慢）
    思路：打开列表第一页-->获取职位详情的url-->打开职位详情进行爬虫<-->关闭职位详情-->打开下一页
'''

# 无头模式
# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--headless')
# broswer = webdriver.Chrome(chrome_options=chrome_options)
broswer = webdriver.Chrome()
broswer.implicitly_wait(10)
jobname = '爬虫'
city = '广州'
client = MongoClient()
db = client['lagoujob']
collection = db[jobname + '-' + city]
url = "https://www.lagou.com/jobs/list_{}?city={}".format(jobname, city)


def run_spider(url):
    '''
    爬虫主循环
    :param url:爬虫开始链接
    :return:
    '''
    broswer.get(url)
    try:
        while True:
            source = broswer.page_source
            page_current = broswer.find_element_by_xpath(
                '//div[@class="pager_container"]/span[@class="pager_is_current"]').text
            print('正在爬取第{}页'.format(page_current))
            next_page_btn = broswer.find_element_by_xpath(
                '//div[@class="pager_container"]/span[contains(@action,"next")]')
            get_url(source)
            # 如果是最后一页就退出循环
            if 'pager_next_disabled' in next_page_btn.get_attribute('class'):
                break
            else:
                next_page_btn.click()
    except Exception as e:
        print('爬取中断:', str(e))
     

def get_url(source):
    '''
    将页面进行解析，获取职位详情的url
    :param source:js渲染好的页面
    :return:
    '''
    r = etree.HTML(source)
    links = r.xpath('//a[@class="position_link"]/@href')
    for link in links:
        request_detail(link)
        time.sleep(1)


def request_detail(link):
    '''
    来回切换列表和职位详情页面，爬取数据
    :param link:职位详情的url
    :return:
    '''
    broswer.execute_script('window.open("{}")'.format(link))
    broswer.switch_to_window(broswer.window_handles[1])
    detail_source = broswer.page_source
    get_datas(detail_source)
    broswer.close()
    broswer.switch_to_window(broswer.window_handles[0])


def get_datas(detail_source):
    '''
    用xpath解析页面和爬数据
    :param detail_source:渲染好的职位详情页面
    :return:
    '''
    datas = etree.HTML(detail_source)
    company = ''.join(datas.xpath('//h2[@class="fl"]/text()'))
    jobname = ''.join(datas.xpath('//div[@class="job-name"]/@title'))
    salary = ''.join(datas.xpath('//span[@class="salary"]/text()')).strip()
    city = datas.xpath('//dd[@class="job_request"]//span/text()')[1]
    work_experience = datas.xpath('//dd[@class="job_request"]//span/text()')[2]
    study_experience = datas.xpath('//dd[@class="job_request"]//span/text()')[3]
    publish_time = ''.join(datas.xpath('//p[@class="publish_time"]/text()'))
    address_city = datas.xpath("//div[@class='work_addr']//a/text()")[0]
    address_region = datas.xpath("//div[@class='work_addr']//a/text()")[1]
    address_detail = datas.xpath("//div[@class='work_addr']//text()")[6]
    detail_address = address_city + address_region + address_detail.strip()
    tags = ''.join(datas.xpath('//dd[@class="job-advantage"]/p/text()'))
    desc = '\n'.join(datas.xpath('//dd[@class="job_bt"]/div/p/text()'))
    company_scale = ''.join(datas.xpath("//ul[@class='c_feature']//li[3]/text()"))
    company_field = datas.xpath("//ul[@class='c_feature']//text()")[2]
    
    # 简单处理数据
    item = {
        'company': re.findall(r'\s*(.*)\n', company)[0],
        'jobname': jobname,
        'salary': salary,
        'city': re.findall(r'/(\S*)\s*/', city)[0],
        'work_experience': re.findall(r'(\S*).*', work_experience)[0],
        'study_experience': re.findall(r'(\S*)\s*/', study_experience)[0],
        'publish_time': re.findall(r'(\d*-\d*-\d*)', publish_time)[0],
        'detail_address': detail_address,
        'tags': tags,
        'desc': desc,
        'company_scale': re.findall(r'\s*(\S*)\n', company_scale)[0],
        'company_field': re.findall(r'\s*(.*)\n', company_field)[0]
    }
    print(item)
    save_data(item)


def save_data(item):
    '''
    存储数据到mongodb
    :param item:含有数据的字典
    :return:
    '''
    if collection.insert(item):
        print('Saved to mongo')


if __name__ == '__main__':
    run_spider(url)