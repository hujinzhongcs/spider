import scrapy
from selenium import webdriver
from news.items import NewsItem
import time
import re
import os
import os.path as osp

class SinaSpider(scrapy.Spider):

    name = 'sina'
    # allowed_domains = ['www.xxxx.com']
    start_urls=[]
    links=[]
    dynamicUrl=start_urls  #需要动态加载的网页

    def __init__(self):
        maxPage=40   #每个模块每次最多爬多少页，新浪新闻每次最多爬50页
        lidlist=[2510,2511,2669,2512,2513,2514,2515,2516,2517,2518] #2510,2511,2669,2512,2513,2514,2515,2516,2517,2518
        urlTemplate='https://news.sina.com.cn/roll/#pageid=153&lid={}&k=&num=50&page={}'
        # lidlistNames=['国内','国际','社会','体育','娱乐','军事','科技','财经','股市','美股']
        for lid in lidlist:
            for i in range(1,maxPage+1):
                detailUrl=urlTemplate.format(lid,i)
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
        li_list=response.xpath('//*[@class="d_list_txt"]/ul/li')
        for li in li_list:
            sort=li.xpath("./span[1]/text()").extract_first()[1:-1]
            detail_url = li.xpath('./span[2]/a/@href').extract_first()
            # time = li.xpath('./span[3]/text()').extract_first().split()[0]
            if detail_url not in self.links:
                item=NewsItem()
                item['sort']=sort
                # item['time']=time
                yield response.follow(detail_url, self.parse_detail,meta={'item':item})

    # https://sports.sina.com.cn/l/2020-12-21/doc-iiznctke7667926.shtml
    def parse_detail(self,response):
        content= '\n'.join('\n'.join(response.xpath('//*[@class="article"]/p/text()').extract()).split('\n'))
        filename= re.split(r'[-.]', response.url)[-2]
        time=re.split(r'[/]', response.url)[-2]
        filename=time.replace('-','')+'-sina-'+filename
        item = response.meta['item']
        item['filename'] = filename
        item['time']=time
        item['content'] = content
        item['url'] = response.url
        item['website'] = 'sina'
        yield item


    def closed(self,spider):
        self.bro.quit()
        localtime = time.asctime( time.localtime(time.time()) )
        print("sina爬虫结束")
        print(localtime)
