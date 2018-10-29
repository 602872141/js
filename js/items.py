# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JsItem(scrapy.Item):

    if_data=scrapy.Field()
    url=scrapy.Field()
    name = scrapy.Field()
    id_url = scrapy.Field()
    startname = scrapy.Field()
    endname = scrapy.Field()
    starttime = scrapy.Field()
    endtime = scrapy.Field()
    mun = scrapy.Field()
    price_list = scrapy.Field()




    pass
