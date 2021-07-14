import scrapy
from selenium import webdriver
from news.items import NewsItem
import time
import json
import re
import os
import os.path as osp


class PeopleSpider(scrapy.Spider):
    name = 'people'
    # allowed_domains = ['http://http://news.people.com.cn/']
    url='http://news.people.com.cn/210801/211150/index.js?_='+str(int(time.time()))
    start_urls = [url]
    links=[]  #增量爬虫中已经爬取的新闻
    dynamicUrl_people=[]#需要动态加载的网页


    def __init__(self):
        # self.bro = webdriver.Chrome(executable_path=r'D:\apkdriver\chromedriver\chromedriver.exe')
        # self.bro = webdriver.PhantomJS()

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
        jsons=json.loads(response.body)
        for it in jsons['items']:
            time=it['date'].split()[0]
            filename=it['id']
            filename=time.replace('-','')+'-people-'+filename
            detail_url=it['url']
            if detail_url not in self.links:
                item=NewsItem()
                # item['sort']=sort
                item['time']=time
                item['filename']=filename

                yield response.follow(detail_url, self.parse_content,meta={'item':item})

    def parse_content(self,response):
        sort=re.split('[/.]',response.url)[2]
        item=response.meta['item']
        item['sort']=sort
        item['url'] = response.url
        item['website'] = 'people'
        if (re.match(r'http://capital.people.com.*',response.url)):
            content=re.sub('\n+','\n','\n'.join(response.xpath('//*[@class="gray box_text"]/p/text()').extract()))
            item['content'] = content
            yield item

        # http://renshi.people.com.cn/n1/2020/1230/c139617-31983658.html
        elif (re.match(r'http://theory.people.com.*|http://renshi.people.com',response.url)):
            content=re.sub('\n+','\n','\n'.join(response.xpath('//*[@class="show_text"]/p/text()').extract()))
            item['content'] = content
            yield item

        elif (re.match(r'http://health.people.com.*',response.url)):
            content=re.sub('\n+','\n','\n'.join(response.xpath('//*[@class="artDet"]/p/text()').extract()))
            item['content'] = content
            yield item

        elif (re.match(r'http://pic.people.com.*',response.url)):
            content=re.sub('\n+','\n','\n'.join(response.xpath('//*[@class="gray box_text"]/p/text()').extract()))
            item['content'] = content
            yield item

        elif (re.match(r'http://sports.people.com.*',response.url)):
            content=re.sub('\n+','\n','\n'.join(response.xpath('//*[@class="content clear clearfix"]/p/text()|//*[@class="box_con"]/p/text()').extract()))
            item['content'] = content
            yield item

        # http://cpc.people.com.cn/n1/2020/1229/c164113-31983247.html
        # http://v.people.cn/n1/2020/1229/c61600-31983279.html
        # 没有文字内容不做处理
        elif (re.match(r'http://cpc.people.com.*http://v.people.cn.*',response.url)):
            pass

        else :
            content=re.sub('\n+','\n','\n'.join(response.xpath('//*[@class="content clear clearfix"]/p/text()|//*[@class="box_con"]//p/text()|//*[@class="rm_txt_con cf"]/p/text()').extract()))
            item['content'] = content
            yield item



    def closed(self,spider):
        # self.bro.quit()
        localtime = time.asctime( time.localtime(time.time()) )
        print("people爬虫结束")
        print(localtime)

