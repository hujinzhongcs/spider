# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ChatSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    first_sort = scrapy.Field()
    second_sort = scrapy.Field()
    third_sort = scrapy.Field()
    content = scrapy.Field()
    filename = scrapy.Field()
    time = scrapy.Field()
    url = scrapy.Field()
    website = scrapy.Field()