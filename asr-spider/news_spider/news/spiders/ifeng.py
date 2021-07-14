import scrapy
from selenium import webdriver
from news.items import NewsItem
import xml.dom.minidom as xmldom
import time
import re
import os
import os.path as osp
import json

class IfengSpider(scrapy.Spider):
    name = 'ifeng'
    # allowed_domains = ['www.ifeng.com']
    start_urls = []
    links=[]

    def __init__(self):
        # self.bro = webdriver.Chrome(executable_path=r'D:\apkdriver\chromedriver\chromedriver.exe')
        self.bro = webdriver.PhantomJS()
        # http://shankapi.ifeng.com/shanklist/_/getColumnInfo/_/default/6740529774893999062/1610077546000/100/4-20077-/
        # http://shankapi.ifeng.com/shanklist/_/getColumnInfo/_/default/6752520925331067401/1610078487000/100/11-35121-
        start_news_category1 = ['3-35190-','3-35191-','3-35199-','3-35204-','1-64-','1-62-83-','1-125387-','240131',
        '1-62-90-','1-62-84-','1-62-90-','1-69-41-','1-69-35249-','1-69-35251-','1-69-35253-','1-69-35255-',
        '1-69-35257-','1-69-35260-','4-20074-','4-20075-','4-20076-','4-20077-','11-35122-','11-35124-','11-35127-',
        '17-','17-35104-','17-35106-','5-185384-','5-35057-','5-35058-','5-35059-','5-35055-','5-75005-','16-',
        '16-60006-','16-60016-','16-60007-','16-60015-','16-60008-','16-60011-','16-60010-','16-60009-','14-35083-',
        '14-35084-','14-35086-','33-60139-','33-60148-','33-60141-','33-60140-','33-60143-','33-60142-','33-60147-',
        '12-','12-35223-','12-35224-','12-35227-','12-35226-','12-35228-','10-586-','10-606-','10-602-','10-587-',
        '17-','17-35104-','17-35108-','20-','20-35097-','20-35099-','20-35101-','18-','18-275800-','18-275802-',
        '18-275803-','18-275804-','18-245652-','15-35075-','22-','22-35141-','22-35143-','22-35145-','22-35146-',
        '22-35147-']
        news_url_head1 = "http://shankapi.ifeng.com/shanklist/_/getColumnInfo/_/default/6752520925331067401/"
        for category in start_news_category1:
            category_url = news_url_head1 + str(int(time.time()))+ '000/100/'+category
            self.start_urls.append(category_url)
        # https://shankapi.ifeng.com/season/xijinping/index/getCustomNewsTfList/20/10/getCustomData?callback=getCustomData&_=120
        start_news_category2=['xijinping','xuanzhan']

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
        sortdic={'3-35190-':'资讯','3-35191-':'资讯','3-35199-':'资讯','3-35204-':'资讯','1-64-':'财经',
        '1-62-83-':'财经','1-125387-':'财经','240131':'财经','1-62-90-':'财经','1-62-84-':'财经','1-62-90-':'财经',
        '1-69-41-':'股票','1-69-35249-':'股票','1-69-35251-':'股票','1-69-35253-':'股票','1-69-35255-':'股票',
        '1-69-35257-':'股票','1-69-35260-':'股票','4-20074-':'娱乐','4-20075-':'娱乐','4-20076-':'娱乐','4-20077-':'娱乐',
        '11-35122-':'体育','11-35124-':'体育','11-35127-':'体育','17-':'文化','17-35104-':'文化','17-35106-':'文化',
        '5-185384-':'科技','5-35057-':'科技','5-35058-':'科技','5-35059-':'科技','5-35055-':'科技','5-75005-':'科技',
        '16-':'佛教','16-60006-':'佛教','16-60016-':'佛教','16-60007-':'佛教','16-60015-':'佛教','16-60008-':'佛教',
        '16-60011-':'佛教','16-60010-':'佛教','16-60009-':'佛教','14-35083-':'军事','14-35084-':'军事','14-35086-':'军事',
        '33-60139-':'旅游','33-60148-':'旅游','33-60141-':'旅游','33-60140-':'旅游','33-60143-':'旅游','33-60142-':'旅游',
        '33-60147-':'旅游','12-':'健康','12-35223-':'健康','12-35224-':'健康','12-35227-':'健康','12-35226-':'健康',
        '12-35228-':'健康','10-586-':'汽车','10-606-':'汽车','10-602-':'汽车','10-587-':'汽车','17-':'读书',
        '17-35104-':'读书','17-35108-':'读书','20-':'国学','20-35097-':'国学','20-35099-':'国学','20-35101-':'国学',
        '18-':'教育','18-275800-':'教育','18-275802-':'教育','18-275803-':'教育','18-275804-':'教育','18-245652-':'教育',
        '15-35075-':'历史','22-':'政务','22-35141-':'政务','22-35143-':'政务','22-35145-':'政务','22-35146-':'政务',
        '22-35147-':'政务'}
        # http://shankapi.ifeng.com/shanklist/_/getColumnInfo/_/default/6752520925331067401/1610078487000/100/11-35121-
        detail_data = json.loads(response.text,strict=False)
        sort=response.url.split('/')[-1]
        sort=sortdic[sort]
        dic_list=detail_data['data']['newsstream']
        for message in dic_list:
            time=message['newsTime'].split()[0]
            detail_url=message['url']
            filename=message['id']
            filename=time.replace('-','')+'-xinhuanet-'+filename
            if detail_url not in self.links:
                item=NewsItem()
                item['sort']=sort
                item['time']=time
                item['filename']=filename
                item['url']=detail_url
                yield response.follow(detail_url, self.parse_content,meta={'item':item})

    def parse_content(self,response):
            item=response.meta['item']
            content=re.sub('\n+','\n','\n'.join(response.xpath('''//*[@class="picTxt-2OruuyP0"]/ul/li//text()|
                                                                //*[@class="des_center-ehaoKy_2 clearfix"]/p/text()|
                                                                //*[@class="text-3w2e3DBc"]/p/text()''').extract()))
            item['content'] = content
            item['website'] = 'ifeng'
            yield item
    def closed(self,spider):
        self.bro.quit()
        localtime = time.asctime( time.localtime(time.time()) )
        print("凤凰网爬虫结束")
        print(localtime)