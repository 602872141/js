# -*- coding: utf-8 -*-
import pymongo
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class JsPipeline(object):
    def process_item(self, item, spider):
        return item
class MongoPipeline(object):
    def __init__(self):
        self.client = pymongo.MongoClient("localhost", 27017)
        self.db = self.client["hanban"]

    def process_item(self, item, spider):
        if item.get('if_data'):
            self.db["Camdodia"].update({"id_url":item.get('id_url')},{'$set':item},True)
            return item

