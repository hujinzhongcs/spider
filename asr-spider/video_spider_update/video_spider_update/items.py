# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class VideoSpiderUpdateItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    category = scrapy.Field()


class baidushipinSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    style = scrapy.Field()
    area = scrapy.Field()
    year = scrapy.Field()
    urlPattern = scrapy.Field()
