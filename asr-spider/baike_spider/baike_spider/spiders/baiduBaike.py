import scrapy
from selenium import webdriver
from baike_spider.items import BaikeSpiderItem
import xml.dom.minidom as xmldom
import datetime
import re
import os
import os.path as osp
import json


class BaidubaikeSpider(scrapy.Spider):
    name = 'baiduBaike'
    # allowed_domains = ['baike.baidu.com']
    start_urls = ['http://baike.baidu.com/']
    startPage = 1
    endPage = 22752797    #百度百科所有词条的数目2021-1-12
    urlPattern = "http://baike.baidu.com/view/{0}.html"    #http://baike.baidu.com/view/1.html  https://baike.baidu.com/item/%E7%99%BE%E5%BA%A6%E7%99%BE%E7%A7%91
    links=[]
    def __init__(self):
        if  osp.exists(r'baikeMessage'):
            with open(r'baikeMessage', 'r') as rf:
                for line in rf:
                    line = line.strip()
                    if not line:
                        continue
                    link=line.split()[-1]
                    self.links.append(link)

    def parse(self, response):
        for i in range(self.startPage, self.endPage):
            detail_url = self.urlPattern.format(i)
            if detail_url not in self.links:
                item=BaikeSpiderItem()
                item['filename']='baiduBaike'+str(i)
                item['url']=detail_url
                yield response.follow(detail_url, self.parse_content,meta={'item':item})

    def parse_content(self,response):
        baikelist=response.xpath('//*[@class="custom_dot  para-list list-paddingleft-1"]/li/div/a/@href').extract()
        if len(baikelist)!=0:
            i=1
            for a in baikelist:
                item=response.meta['item'].copy()
                filename=item['filename']
                name=filename+'_'+str(i)
                item['filename']=name
                url='https://baike.baidu.com'+a
                i=i+1
                yield response.follow(url, self.parse_content,meta={'item':item})
        else:
            item=response.meta['item'].copy()
            now=datetime.datetime.now()
            todayDate=now.strftime('%Y-%m-%d')
            content=re.sub('\n+','\n',''.join(response.xpath('''//*[@class="para"]//text()|
                                                                //*[@class="lemmaWgt-lemmaTitle-title"]/h1/text()|
                                                                //*[@class="title-text"]/text()''').extract()))
            item['content'] = content
            item['website'] = 'baiduBaike'
            item['time']=todayDate
            item['sort']='baike'

            yield item

    def closed(self,spider):
        now=datetime.datetime.now()
        nowtime=now.strftime('%Y-%m-%d %H:%M:%S')
        print("百度百科爬虫结束")
        print(nowtime)