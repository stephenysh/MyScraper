# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MyscraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    index = scrapy.Field()
    pass

class WikiItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    filename = scrapy.Field()
    pass


class SentenceItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    content = scrapy.Field()
    pass

class CamDictItem(scrapy.Item):
    # define the fields for your item here like:
    en_wd = scrapy.Field()
    ar_wd = scrapy.Field()
    url = scrapy.Field()
    pass

class BabItem(scrapy.Item):
    # define the fields for your item here like:
    idx = scrapy.Field()
    en_str = scrapy.Field()
    ar_str = scrapy.Field()
    url = scrapy.Field()
    pass