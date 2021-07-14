import scrapy
import re
import os
import os.path as osp
from news.items import NewsItem
# from baiduNews.items import NewsItem
from selenium import webdriver
import time

class BaiduSpider(scrapy.Spider):
    name = 'baidu'
    # allowed_domains = ['http://news.baidu.com/']
    start_urls = ['http://news.baidu.com/']
    links=[]  #增量爬虫中已经爬取的新闻url
    dynamicUrl_baidu=[]#需要动态加载的网页

    def __init__(self):
        # self.bro = webdriver.Chrome(executable_path=r'D:\apkdriver\chromedriver\chromedriver.exe')
        self.bro = webdriver.PhantomJS()

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
        #1国内，2国际，3军事，4财经，5娱乐，6体育，7互联网，8科技，9游戏，10女人，11汽车，12房产
        menus_list= response.xpath('//*[@id="channel-all"]//a/@href').extract()

        alist1=[1,2,3,4,5,6,8,10]        #1国内，2国际，3军事，4财经，5娱乐，6体育，8科技，10女人  1,2,3,4,5,6,8,10
        alist2=[7]     #7互联网
        alist3=[9]    #9游戏
        alist4=[11]    #11汽车     .wrapper li a,#related li a,.wrapper .auto-pic-p a:nth-child(1)
        alist5=[12]   #12房产     .tlc li a

        for index in alist1:
            menu_url = menus_list[index]
            menu_url='http://news.baidu.com'+menu_url
            self.dynamicUrl_baidu.append(menu_url)
            yield response.follow(menu_url, self.get_title_urls1)

        for index in alist2:
            menu_url = menus_list[index]
            menu_url='http://news.baidu.com'+menu_url
            self.dynamicUrl_baidu.append(menu_url)
            yield response.follow(menu_url, self.get_title_urls2)
        for index in alist3:
            menu_url = menus_list[index]
            menu_url='http://news.baidu.com'+menu_url
            self.dynamicUrl_baidu.append(menu_url)
            yield response.follow(menu_url, self.get_title_urls3)

        for index in alist4:
            menu_url = menus_list[index]
            menu_url='http://news.baidu.com'+menu_url
            self.dynamicUrl_baidu.append(menu_url)
            yield response.follow(menu_url, self.get_title_urls4)

        for index in alist5:
            menu_url = menus_list[index]
            menu_url='http://news.baidu.com'+menu_url
            self.dynamicUrl_baidu.append(menu_url)
            yield response.follow(menu_url, self.get_title_urls5)


    def get_title_urls1(self, response):
        print(response.url)
        sort= re.split('/', response.url)[-1]
        headlines_list=response.css('.ulist a')
        for headline in headlines_list:
            news_content_url=headline.attrib['href']
            if news_content_url not in self.links:
                    item=NewsItem()
                    item['sort']=sort
                    yield response.follow(news_content_url,callback=self.parse_content,meta={'item':item})

    def get_title_urls2(self, response):
        print(response.url)
        sort= re.split('/', response.url)[-1]
        headlines_list=response.xpath('//*[@class="title"]//a |//*[@class="item"]/a')
        for headline in headlines_list:
            news_content_url=headline.attrib['href']
            if news_content_url not in self.links:
                    item=NewsItem()
                    item['sort']=sort
                    yield response.follow(news_content_url,callback=self.parse_content,meta={'item':item})
        # yield from self.title_urls_sort(sort,headlines_list)

    def get_title_urls3(self, response):
        print(response.url)
        sort= re.split('/', response.url)[-1]
        headlines_list=response.css('#col-left a,#col-right a:nth-child(1)')
        for headline in headlines_list:
            news_content_url=headline.attrib['href']
            if news_content_url not in self.links:
                    item=NewsItem()
                    item['sort']=sort
                    yield response.follow(news_content_url,callback=self.parse_content,meta={'item':item})


    def get_title_urls4(self, response):
        print(response.url)
        sort= re.split('/', response.url)[-1]
        headlines_list=response.css('.wrapper li a,#related li a,.wrapper .auto-pic-p a:nth-child(1)')
        for headline in headlines_list:
            news_content_url=headline.attrib['href']
            if news_content_url not in self.links:
                    item=NewsItem()
                    item['sort']=sort
                    yield response.follow(news_content_url,callback=self.parse_content,meta={'item':item})

    def get_title_urls5(self, response):
        print(response.url)
        sort= re.split('/', response.url)[-1]
        headlines_list=response.css('.tlc li a')
        for headline in headlines_list:
            news_content_url=headline.attrib['href']
            if news_content_url not in self.links:
                    item=NewsItem()
                    item['sort']=sort
                    yield response.follow(news_content_url,callback=self.parse_content,meta={'item':item})


    def parse_content(self, response):
        # http://baijiahao.baidu.com/s?id=1685702409658905392
        if (re.match(r'http://baijiahao.baidu.com.*',response.url)):
            time=response.xpath('//*[@class="date"]/text()').extract_first().split('：')[1]
            if len(time.split('-'))==2:
                time='2021-'+time                  #到2021时记得修改  01-02
            else:
                time='20'+time    #20-12-31
            filename= re.split(r'=', response.url)[-1]
            filename=time.replace('-','')+'-baidu-'+filename
            content=re.sub('\n+','\n','\n'.join(response.xpath('//*[@class="article-content"]/p/span/text()|//*[@class="article-content"]/p/text()').extract()))
            item = response.meta['item']
            item['filename']=filename
            item['content']=content
            item['url'] = response.url
            item['website'] = 'baidu'
            item['time']=time
            yield item
        # https://m.thepaper.cn/baijiahao_10302578
        elif (re.match(r'https://m.thepaper.cn/baijiahao.*',response.url)):
            time=response.xpath('//*[@class="info link"]/span/text()').extract_first().split()[1]
            filename= re.split(r'_', response.url)[-1]
            filename=time.replace('-','')+'-baidu-'+filename
            content=re.sub('\n+','\n','\n'.join(response.xpath('//*[@class="contentFont"]/text()').extract()))
            item = response.meta['item']
            item['filename']=filename
            item['content']=content
            item['url'] = response.url
            item['website'] = 'baidu'
            item['time']=time
            yield item
        # https://m.gmw.cn/baijia/2020-12/10/1301922825.html
        elif (re.match(r'https://m.gmw.cn/baijia.*',response.url)):
            year,month_day=re.split('[/]',response.url)[4:6]
            time=year+'-'+month_day
            filename= re.split(r'[/.]', response.url)[-2]
            filename=time.replace('-','')+'-baidu-'+filename
            content=re.sub('\n+','\n','\n'.join(response.xpath('//*[@class="contentFont"]/text()').extract()))
            item = response.meta['item']
            item['filename']=filename
            item['content']=content
            item['url'] = response.url
            item['website'] = 'baidu'
            item['time']=time
            yield item
        else:
            pass

    def closed(self,spider):
        self.bro.quit()
        localtime = time.asctime( time.localtime(time.time()) )
        print("baidu爬虫结束")
        print(localtime)