# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient
import re


class HhruPipeline(object):
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.vacancy206

    def process_item(self, item, spider):
        item['title']  = " ".join(item['title'])
        salary = "".join(item['salary'])
        item['salary'] = salary.replace('\\xa0', ' ')
        item['source'] = item['link'].split("/")[2]

#        collection = self.mongo_base[spider.name + '_Gry']
        collection = self.mongo_base['Xxru_Gry']
        collection.insert_one(item)
        return item

class SjruPipeline(object):
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.vacancy206

    def process_item(self, item, spider):
        p = re.compile(r"<.*?>")
        item['title'] = " ".join(item['title'])
        salary = item['salary'][0]
        salary = p.sub("", salary)
        item['salary'] = salary.replace('\\xa0', ' ')
        item['source'] = item['link'].split("/")[2]

        collection = self.mongo_base['Xxru_Gry']
        collection.insert_one(item)
        return item
