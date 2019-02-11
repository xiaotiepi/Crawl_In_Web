# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo


class JdPipeline(object):
    def __init__(self):
        self.client = pymongo.MongoClient()
        self.db = self.client['jd']
        self.collection = self.db['keyboard']

    def process_item(self, item, spider):
        self.collection.insert(dict(item))
        return item

    def close_spider(self, spider):
        self.client.close()
