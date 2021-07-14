import scrapy
from selenium import webdriver
from news.items import NewsItem
import xml.dom.minidom as xmldom
import time
import re
import os
import os.path as osp
import json

class CctvSpider(scrapy.Spider):
    name = 'cctv'
    # allowed_domains = ['www.xxx.com']
    start_urls = []
    links=[]
    # dynamicUrl_people=['http://news.people.com.cn/']   #需要动态加载的网页

    def __init__(self):
        maxPage=5   #每个模块每次最多爬多少页(每页50条数据)，军事每次最多爬8页
        start_news_category = ['china','world','society','law','health','economy_zixun','edu']     #'world','society','law','health','economy_zixun','edu'
        news_url_head = "https://news.cctv.com/2019/07/gaiban/cmsdatainterface/page/"
        news_url_tail = ".js?callback=data_callback"
        for category in start_news_category:
            for count in range(1, maxPage+1):
                if count == 1:
                    category_url = news_url_head + category +'_1' +'.jsonp?cb='+category
                else:
                    category_url = news_url_head + category+ "_" +str(count)+'.jsonp?cb=t&cb='+category

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
        # https://news.cctv.com/2019/07/gaiban/cmsdatainterface/page/china_1.jsonp?cb=china
        sort=re.split('[=]',response.url)[-1]
        detail_data = json.loads(re.findall(r"\((.*)\)",response.text)[0],strict=False)
        dic_list=detail_data['data']['list']
        for message in dic_list:
            detail_url=message["url"]
            time=message['focus_date'].split()[0]
            filename=message['id']
            filename=time.replace('-','')+'-cctv-'+filename
            if (re.match(r'https://tv.cctv.com.*',detail_url)):
                pass
            elif detail_url not in self.links:
                # https://photo.cctv.com/2021/01/06/PHOAFZJSd9pUll5WXBI0rWcj210106.shtml
                # https://photo.cctv.com/2021/01/06/PHOAFZJSd9pUll5WXBI0rWcj210106.xml?randomNum=57
                # https://photo.cctv.com/2021/01/06/PHOAIvl5Gx3QK7vYdnmJZAJJ210106.xml?randomNum=65
                if (re.match(r'https://photo.cctv.com.*',detail_url)):
                    dynamic_detail_url=detail_url.replace('shtml','xml')
                    item=NewsItem()
                    item['sort']=sort
                    item['time']=time
                    item['filename']=filename
                    item['url']=detail_url
                    yield response.follow(dynamic_detail_url, self.parse_photoContent,meta={'item':item})
                else:
                    item=NewsItem()
                    item['sort']=sort
                    item['time']=time
                    item['filename']=filename
                    item['url']=detail_url
                    yield response.follow(detail_url, self.parse_content,meta={'item':item})
            else:
                pass


    def parse_content(self,response):
        item=response.meta['item']
        content=re.sub('\n+','\n','\n'.join(response.xpath('''//*[@class="content_area"]/p/text()|
                                                            //*[@class="cnt_bd"]/p/text()|
                                                            //*[@class="text_area"]/p/text()''').extract()))
        item['content'] = content
        item['website'] = 'cctv'
        yield item
    def parse_photoContent(self,response):
        item=response.meta['item']
        domobj = xmldom.parseString(response.text)
        content = domobj.documentElement.getElementsByTagName("li")[0].childNodes[0].data
        item['content'] = content
        item['website'] = 'cctv'
        yield item


    def closed(self,spider):
        localtime = time.asctime( time.localtime(time.time()) )
        print("cctv爬虫结束")
        print(localtime)