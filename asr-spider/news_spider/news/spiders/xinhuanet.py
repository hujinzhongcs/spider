import scrapy
from selenium import webdriver
from news.items import NewsItem
import xml.dom.minidom as xmldom
import time
import re
import os
import os.path as osp
import json


class XinhuanetSpider(scrapy.Spider):
    name = 'xinhuanet'
    # allowed_domains = ['www.xinhuanet.com']
    start_urls = []
    links=[]
    # allsort=[]

    # dynamicUrl_people=[]   #需要动态加载的网页

    def __init__(self):
        # https://edu.163.com/special/002987KB/newsdata_edu_hot.js?callback=data_callback   教育
        maxPage=1   #每个模块每次最多爬多少页，军事每次最多爬8页            zfw政务往事  'politics',政务
        start_news_category1 = ['politics','world','fortune','tech','culture']
        start_news_category2 = ['114435','11228286','11227928','11230270','11230846','11227970','11228405','11228415','11228087','11203988']

        provinces=[]   #,'anhui'没有数据
        news_url_head1 = "http://www.news.cn/"
        news_url_head2='http://da.wa.news.cn/nodeart/page?nid='
        news_url_tail2 = '&pgnum=1&cnt=100&attr=&tp=1&orderby=1'
        for category in start_news_category1:
            category_url = news_url_head1 + category+ 'pro/json/xh_'+category+'proDepth.js'
            self.start_urls.append(category_url)
        for category in start_news_category2:
                category_url = news_url_head2 + category+ news_url_tail2
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
        sortdic={'politicspro':'时政','worldpro':'国际','fortunepro':'财经','techpro':'科技',
        'culturepro':'文化','114435':'理论','11228286':'网评','11227928':'法制','11230270':'人事',
        '11230846':'廉政','11227970':'地方','11228405':'港澳','11228415':'台湾','11228087':'教育','11203988':'科普'}
        # http://www.news.cn/politicspro/json/xh_politicsproDepth.js
        if (re.match(r'http://www.news.cn.*',response.url)):
            detail_data = json.loads(re.findall(r"\=(.*)",response.text)[0],strict=False)
            sort=response.url.split('/')[3]
            sort=sortdic[sort]
            dic_list=detail_data['data']['list']
            for message in dic_list:
                time=message['pubtime'].split()[0]
                detail_url=message['artDetails'][0]['url']
                filename=message['id']
                filename=time.replace('-','')+'-xinhuanet-'+filename
                # print(detail_url)
                if detail_url not in self.links:
                    item=NewsItem()
                    item['sort']=sort
                    item['time']=time
                    item['filename']=filename
                    item['url']=detail_url
                    yield response.follow(detail_url, self.parse_content,meta={'item':item})

        # http://da.wa.news.cn/nodeart/page?nid=11227928&pgnum=1&cnt=100&attr=&tp=1&orderby=1
        else:
            detail_data = json.loads(response.text,strict=False)
            sort=re.split('[=&]',response.url)[1]
            sort=sortdic[sort]
            dic_list=detail_data['data']['list']
            for message in dic_list:
                time=message['PubTime'].split()[0]
                detail_url=message['LinkUrl']
                filename=message['DocID']
                filename=time.replace('-','')+'-xinhuanet-'+str(filename)
                # print(detail_url)
                if detail_url not in self.links:
                    item=NewsItem()
                    item['sort']=sort
                    item['time']=time
                    item['filename']=filename
                    item['url']=detail_url
                    yield response.follow(detail_url, self.parse_content,meta={'item':item})


    def parse_content(self,response):
        # if (re.match(r'http://www.xinhuanet.com.*|http://travel.news.cn.*',response.url)):
            item=response.meta['item']
            content=re.sub('\n+','\n','\n'.join(response.xpath('''//*[@id="detail"]/p/text()|
                                                                //*[@id="detail"]/p/font/strong/text()|
                                                                //*[@id="detail"]/p/strong/font/text()|
                                                                //*[@id="detail"]/p/strong/text()|
                                                                //*[@id="detail"]/div/p/text()|
                                                                //*[@id="p-detail"]/p/text()|
                                                                //*[@id="content"]/p/text()|
                                                                //*[@id="content"]/span/p/text()|
                                                                //*[@id="detail"]/p/span/font/text()''').extract()))
            item['content'] = content
            item['website'] = 'xinhuanet'
            yield item
    def closed(self,spider):
        localtime = time.asctime( time.localtime(time.time()) )
        print("新华网爬虫结束")
        print(localtime)
        # print(self.allsort)