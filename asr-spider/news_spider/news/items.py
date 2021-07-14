# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

# 链接 文件名 时间 站点 领域

class NewsItem(scrapy.Item):
    sort = scrapy.Field()
    content = scrapy.Field()
    filename=scrapy.Field()
    time=scrapy.Field()
    url=scrapy.Field()
    website=scrapy.Field()

# class ChinanewsItem(scrapy.Item):
#     sort = scrapy.Field()
#     content = scrapy.Field()
#     filename=scrapy.Field()
#     time=scrapy.Field()
#     url=scrapy.Field()
#     website=scrapy.Field()
