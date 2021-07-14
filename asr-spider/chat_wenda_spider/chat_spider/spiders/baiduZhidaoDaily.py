import scrapy
from selenium import webdriver
from chat_spider.items import ChatSpiderItem
import datetime
import re
import os
import os.path as osp



class BaiduzhidaodailySpider(scrapy.Spider):
    name = 'baiduZhidaoDaily'
    # allowed_domains = ['zhidao.baidu.com/daily']
    start_urls = ['http://zhidao.baidu.com/daily/']
    startPage = 1
    endPage = 230515 #截至到2021-1-19日
    #https://zhidao.baidu.com/daily/view?id=1
    urlPattern="https://zhidao.baidu.com/daily/view?id={0}"
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
        for i in range(self.startPage, self.endPage+1):
            detail_url = self.urlPattern.format(i)
            if detail_url not in self.links:
                item=ChatSpiderItem()
                item['filename']='baiduZhidaoDaily'+str(i)
                yield response.follow(detail_url, self.parse_content,meta={'item':item})

    def parse_content(self,response):
        url=response.url
        title=re.sub('\n+','',response.xpath('//*[@id="daily-title"]/text()').extract_first())
        title=response.xpath('//*[@id="daily-title"]/text()').extract_first()
        answer=re.sub('\n+','\n','\n'.join(response.xpath('''//*[@id="daily-cont"]/p//text()''').extract()))
        content=title+'\n'+answer
        time=response.xpath('//*[@class="info"]/span[1]/text()').extract_first()
        item=response.meta['item']
        item['content'] = content
        item['website'] = 'baiduZhidaoDaily'
        item['time']=time
        item['first_sort']='知道'
        item['url']=url
        # print(item)
        yield item

    def closed(self,spider):
        now=datetime.datetime.now()
        nowtime=now.strftime('%Y-%m-%d %H:%M:%S')
        print("百度知道日报爬虫结束")
        print(nowtime)