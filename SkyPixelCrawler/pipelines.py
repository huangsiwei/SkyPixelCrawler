# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
import pymongo
from scrapy.conf import settings
from scrapy.exceptions import DropItem
from scrapy import log


class SkypixelcrawlerPipeline(object):
    pass


class MysqlPipeline(object):
    def __init__(self):
        self.conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='test', db='skypixel',
                                    use_unicode=True, charset="utf8")
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        insert_sql = '''
          insert into hot_media_resource(account_id,account_name,resource_id,resource_time,resource_title,resource_type,resource_url) VALUES ("%s","%s","%s","%s","%s","%s","%s")
          '''
        self.cursor.execute(insert_sql % (item["resource_id"], item["account_id"], item["account_name"],
                                          item["resource_time"],
                                          item["resource_title"], item["resource_type"], item["resource_url"]))
        self.conn.commit()


class MongoDBPipeline(object):
    def __init__(self):
        client = pymongo.MongoClient(settings['MONGODB_SERVER'],
                                     settings['MONGODB_PORT'])

        self.client = client
        self.collection = client[settings['MONGODB_DB']][settings['MONGODB_COLLECTION']]

    def process_item(self, item, spider):
        valid = True
        for data in item:
            if not data:
                valid = False
                raise DropItem("Missing {0}!".format(data))
        if valid:
            self.collection.insert(dict(item))
        return item

    def close_spider(self, spider):
        self.client.close()
