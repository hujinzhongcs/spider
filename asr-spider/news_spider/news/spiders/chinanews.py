import scrapy
from selenium import webdriver
from news.items import NewsItem
import time
import re
import os
import os.path as osp


class ChinanewsSpider(scrapy.Spider):
    name = 'chinanews'
    # allowed_domains = ['www.xxxx.com']
    start_urls = []
    links=[]
    dynamicUrl=[]   #需要动态加载的网页

    def __init__(self):
        maxPage=10   #每个模块每次最多爬多少页，中国新闻网每次最多爬10页
        urlTemplate='http://www.chinanews.com/scroll-news/news{}.html'
        # lidlistNames=['国内','国际','社会','体育','娱乐','军事','科技','财经','股市','美股']
        for i in range(1,maxPage+1):
            detailUrl=urlTemplate.format(i)
            self.start_urls.append(detailUrl)

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

        # self.bro = webdriver.Chrome(executable_path=r'D:\apkdriver\chromedriver\chromedriver.exe')
        self.bro = webdriver.PhantomJS()


    def parse(self, response):
        li_list=response.css('.content_list ul li:not(.nocontent)')
        for li in li_list:
            sort=li.xpath("./div[1]/a/text()").extract_first()
            detail_url = li.xpath('./div[2]/a/@href').extract_first()
            # time = li.xpath('./div[3]/text()').extract_first().split()[0]
            detail_url='http:'+detail_url
            # print(detail_url)
            # print(sort)
            # print(time)
            if detail_url not in self.links:
                item=NewsItem()
                item['sort']=sort
                # item['time']=time
                yield response.follow(detail_url, self.parse_content,meta={'item':item})

    def parse_content(self,response):
        # print(response.url)
        #    http://www.chinanews.com/shipin/cns-d/2020/12-27/news876206.shtml         20201227-chinanews-news876206
        if (re.match(r'http://www.chinanews.com/shipin.*',response.url)):
            year,month_day,filename=re.split('[/.]',response.url)[-4:-1]
            time=year+'-'+month_day
            filename=time.replace('-','')+'-chinanews-'+filename
            content= '\n'.join('\n'.join(response.xpath('//*[@class="content_desc"]/p/text()|//*[@class="txt"]/p[1]/text()').extract()).split('\n'))
            item=response.meta['item']
            item['content'] = content
            item['filename']=filename
            item['url'] = response.url
            item['time'] = time
            item['website'] = 'chinanews'
            yield item
        # http://www.chinanews.com/tp/hd2011/2020/12-27/965571.shtml
        elif (re.match(r'http://www.chinanews.com/tp.*',response.url)):
            year,month_day,filename=re.split('[/.]',response.url)[-4:-1]
            time=year+'-'+month_day
            filename=time.replace('-','')+'-chinanews-'+filename
            content = '\n'.join('\n'.join(response.xpath('//*[@class="t3"]/text()|//*[@class="content_desc"]/p/text()').extract()).split('\n'))
            item = response.meta['item']
            item['content'] = content
            item['filename']= filename
            item['url'] = response.url
            item['time'] = time
            item['website'] = 'chinanews'
            yield item
        # http://www.chinanews.com/gn/2020/12-27/9372219.shtml
        # http://www.chinanews.com/sh/2020/12-27/9372215.shtml
        # http://www.chinanews.com/ll/2020/12-27/9372218.shtml
        elif (re.match(r'http://www.chinanews.com.*',response.url)):
            year,month_day,filename=re.split('[/.]',response.url)[-4:-1]
            time=year+'-'+month_day
            filename=time.replace('-','')+'-chinanews-'+filename
            content = '\n'.join('\n'.join(response.xpath('//*[@class="left_zw"]/p/text()').extract()).split('\n'))
            item = response.meta['item']
            item['content'] = content
            item['filename']= filename
            item['url'] = response.url
            item['time'] = time
            item['website'] = 'chinanews'
            yield item
        else:
            pass

    def closed(self,spider):
        self.bro.quit()
        localtime = time.asctime( time.localtime(time.time()) )
        print("chinanews爬虫结束")
        print(localtime)
