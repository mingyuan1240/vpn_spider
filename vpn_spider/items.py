# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class Server(scrapy.Item):
    host = scrapy.Field()
    port = scrapy.Field()
    anonymous_type = scrapy.Field()
    type = scrapy.Field()
    region = scrapy.Field()
