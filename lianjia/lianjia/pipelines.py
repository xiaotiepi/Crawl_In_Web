# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from sqlalchemy.orm import sessionmaker
from db import engine, HouseModel
from lianjia.items import LianjiaItem
from datetime import datetime


class LianjiaPipeline(object):
    def open_spider(self, spider):
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def close_spider(self, spider):
        self.session.commit()
        self.session.close()

    def process_item(self, item, spider):
        if isinstance(item, LianjiaItem):
            return self._process_house_item(item)
        else:
            return item
  
    def _process_house_item(self, item):
        item['release_time'] = datetime.strptime(
            item['release_time'], '%Y-%m-%d')
        self.session.add(HouseModel(**item))
        return item
