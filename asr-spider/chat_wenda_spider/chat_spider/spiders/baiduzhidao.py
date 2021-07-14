import scrapy
from selenium import webdriver
# from baike_spider.items import BaikeSpiderItem
import xml.dom.minidom as xmldom
import datetime
import re
import os
import os.path as osp
import json



class BaiduzhidaoSpider(scrapy.Spider):
    name = 'baiduzhidao'
    # allowed_domains = ['zhidao.baidu.com']
    start_urls = ['http://zhidao.baidu.com/']

    # startPage = 1
    # endPage = 22752797    #百度百科所有词条的数目2021-1-12      592309045         1183305341540833219
    # # urlPattern = "http://baike.baidu.com/view/{0}.html"    #http://baike.baidu.com/view/1.html  https://baike.baidu.com/item/%E7%99%BE%E5%BA%A6%E7%99%BE%E7%A7%91
    # urlPattern = "https://zhidao.baidu.com/question/{0}.html"    #https://zhidao.baidu.com/question/76900103.html
    #                                                         # https://zhidao.baidu.com/daily/view?id=230433
    # urlPattern="https://zhidao.baidu.com/daily/view?id={0}"   #https://zhidao.baidu.com/daily/view?id=1
    # links=[]
    # def __init__(self):
    #     if  osp.exists(r'baikeMessage'):
    #         with open(r'baikeMessage', 'r') as rf:
    #             for line in rf:
    #                 line = line.strip()
    #                 if not line:
    #                     continue
    #                 link=line.split()[-1]
    #                 self.links.append(link)



    # def parse(self, response):
    #     for i in range(self.startPage, self.endPage):
    #         detail_url = self.urlPattern.format(i)
    #         if detail_url not in self.links:
    #             item=BaikeSpiderItem()
    #             item['filename']='baiduzhidao'+str(i)
    #             item['url']=detail_url
    #             yield response.follow(detail_url, self.parse_content,meta={'item':item})

