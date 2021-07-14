import scrapy
from selenium import webdriver
from video_spider_update.items import VideoSpiderUpdateItem
import datetime
from pymongo import MongoClient

class QqSpider(scrapy.Spider):
    name = 'qq'
    # allowed_domains = ['v.qq.com']
    start_urls =['https://v.qq.com/']
    channel_urls = ['https://v.qq.com/channel/movie?_all=1&channel=movie&listpage=1&sort=19',
        'https://v.qq.com/channel/tv?_all=1&channel=tv&listpage=1&sort=19',
        'https://v.qq.com/channel/variety?_all=1&channel=variety&listpage=1&sort=5',
        'https://v.qq.com/channel/cartoon?_all=1&channel=cartoon&listpage=1&sort=23',
        # 'https://v.qq.com/channel/child?_all=1&channel=child&listpage=1&sort=19',    #少儿中课程较多
        'https://v.qq.com/channel/doco?_all=1&channel=doco&listpage=1&sort=19']
    categorys=['电影','电视剧','综艺','动漫','纪录片']

    def __init__(self):
        self.bro = webdriver.PhantomJS()
        # 获取爬取当天日期
        now=datetime.datetime.now()
        self.todayDate=now.strftime('%Y-%m-%d')
        nowtime=now.strftime('%Y-%m-%d %H:%M:%S')
        print("腾讯视频更新开始  "+nowtime)

        #连接数据库
        client = MongoClient('mongodb://admin:azero123@172.16.10.14:27027/')
        db = client['asrspider']
        self.video_titles = db["video_titles"]
        self.qq=db["qq"]

    def parse(self,response):
        for i in range(5):
            detail_url=self.channel_urls[i]
            category=self.categorys[i]
            item=VideoSpiderUpdateItem()
            item['category']=category
            yield response.follow(detail_url, self.prase_page,meta={'item':item})


    def prase_page(self, response):
        item=response.meta['item']
        category=item['category']
        titleList=response.xpath('//*[@class="list_item"]/div/a/text()').extract()
        for title in titleList:
            item['title']=title
            if self.qq.find_one({"title": title}):
                # print("该qq原始数据已经保存")
                pass
            else:
                self.qq.insert_one({"title": title, "category":category,"create_date": self.todayDate })
                # with open('../nameDate/qqName.txt', 'a',encoding="utf-8") as wf:
                #     wf.write(title+'\n')
                # print("原始数据添加成功")
            yield item

    def closed(self,spider):
        self.bro.quit()
        now=datetime.datetime.now()
        nowtime=now.strftime('%Y-%m-%d %H:%M:%S')
        print("腾讯视频更新结束  "+nowtime)
