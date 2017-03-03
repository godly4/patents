# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from items import PatentsItem

class PatentsPipeline(object):
    def __init__(self):
        mongoClient = pymongo.MongoClient("localhost", 27017)
        db = mongoClient["patent_db"]
        self.Patent = db["patents"]
    
    def process_item(self, item, spider):
        if isinstance(item, PatentsItem):
            self.Patent.insert(dict(item))
