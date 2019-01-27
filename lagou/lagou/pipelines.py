# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from sqlalchemy.orm import sessionmaker
from db import engine, JobModel
from lagou.items import LagouItem


class LagouPipeline(object):
    def open_spider(self, spider):
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def close_spider(self, spider):
        self.session.commit()
        self.session.close()

    def process_item(self, item, spider):
        if isinstance(item, LagouItem):
            return self._process_job_item(item)
        else:
            return item

    def _process_job_item(self, item):
        """
        处理items用于保存到数据库
        :param：LagouCrawlItem
        :return: item
        """
        
        city = item['city'].replace("·", "市")

        model = JobModel(
            title=item['title'],
            city=city,
            salary_range=item['salary_range'],
            experience=item['experience'],
            education=item['education'],
            company=item['company'],
            tags=item['tags'],
            industry=item['industry'],
            scale=item['scale']
        )
        self.session.add(model)

        return item

