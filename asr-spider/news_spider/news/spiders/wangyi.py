import scrapy
from selenium import webdriver
from news.items import NewsItem
import time
import re
import os
import os.path as osp
import json


class ChinanewsSpider(scrapy.Spider):

    name = 'wangyi'
    # allowed_domains = ['www.xxxx.com']
    # start_urls = ['http://www.xxxx.com/']

    start_urls = []
    links=[]
    # dynamicUrl_people=['http://news.people.com.cn/']   #需要动态加载的网页

    def __init__(self):
        # https://edu.163.com/special/002987KB/newsdata_edu_hot.js?callback=data_callback   教育
        maxPage=3   #每个模块每次最多爬多少页，军事每次最多爬8页
        start_news_category = ["guonei", "guoji", "yaowen", "shehui", "war", "money",
                            "tech", "sports", "ent","lady", "auto", "jiaoyu", "jiankang", "hangkong"]
        news_url_head = "http://temp.163.com/special/00804KVA/"
        news_url_tail = ".js?callback=data_callback"
        for category in start_news_category:
            category_item = "cm_" + category
            for count in range(1, maxPage+1):  # 每个版块最多爬取前3页数据
                if count == 1:
                    category_url = news_url_head + category_item + news_url_tail
                else:
                    category_url = news_url_head + category_item + "_0" +str(count) +news_url_tail

                self.start_urls.append(category_url)

        # print(self.start_urls)
        if  osp.exists(r'../webMessage'):
            with open(r'../webMessage', 'r') as rf:
                for line in rf:
                    line = line.strip()
                    if not line:
                        continue
                    link=line.split()[-1]
                    # print(link)
                    self.links.append(link)

    def parse(self, response):
        # http://temp.163.com/special/00804KVA/cm_yaowen_05.js?callback=data_callback
        # print(response.url)
        sort=re.split('[_.]',response.url)[3]
        detail_url_dics = json.loads(response.text[14:-1],strict=False)  # 去掉"data_callback()"

        for message in detail_url_dics:
            detail_url=message["docurl"]
            if message["time"]!="":
                month,day,year=message["time"].split()[0].split('/')
                time=year+'-'+month+'-'+day
                if detail_url not in self.links:
                    item=NewsItem()
                    item['sort']=sort
                    item['time']=time
                    yield response.follow(detail_url, self.parse_content,meta={'item':item})

    def parse_content(self,response):
        item=response.meta['item']
        time= item['time']
        filename= re.split(r'[/.]', response.url)[-2]
        filename=time.replace('-','')+'-wangyi-'+filename
        content=re.sub('\n+','\n','\n'.join(response.xpath('''//*[@class="overview"]/p/text()|
                                                            //*[@class="post_body"]//p/text()|
                                                            //*[@class="post_body"]//p/strong/text()|
                                                            //*[@class="post_body"]/article/p/text()|
                                                            //*[@id="endText"]/p/text()'''
                                                            ).extract()))
        item['content'] = content
        item['filename']= filename
        item['url'] = response.url
        item['website'] = 'wangyi'
        yield item

    def closed(self,spider):
        localtime = time.asctime( time.localtime(time.time()) )
        print("wangyi爬虫结束")
        print(localtime)
