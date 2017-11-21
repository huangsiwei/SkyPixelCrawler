# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SkypixelcrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class MediaResourceItem(scrapy.Item):
    resource_id = scrapy.Field()
    account_id = scrapy.Field()
    account_name = scrapy.Field()
    resource_type = scrapy.Field()
    resource_url = scrapy.Field()
    resource_title = scrapy.Field()
    resource_time = scrapy.Field()
    resource_video_url = scrapy.Field()
