import scrapy
import re
from selenium import webdriver
from music.items import MusicItem
import datetime
from pymongo import MongoClient

class KugouSpider(scrapy.Spider):
    name = 'kugou'
    # allowed_domains = ['www.kugou.com']
    custom_settings = {
        'DOWNLOAD_DELAY': 3
        # 'LOG_LEVEL':'DEBUG'
        # 'DEPTH_PRIORITY' : 1,
        # 'SCHEDULER_DISK_QUEUE' : 'scrapy.squeues.PickleFifoDiskQueue',
        # 'SCHEDULER_MEMORY_QUEUE' : 'scrapy.squeues.FifoMemoryQueue'
    }
    start_urls = ['http://www.kugou.com/']
    # https://www.kugou.com/yy/singer/index/2-e-1.html
    urlPattern='https://www.kugou.com/yy/singer/index/{}-{}-{}.html'
    pages=[1,2,3,4,5]
    latters=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','null']
    music_count=0


    def __init__(self):
        self.bro = webdriver.PhantomJS()
        # 获取爬取当天日期
        now=datetime.datetime.now()
        self.todayDate=now.strftime('%Y-%m-%d')

        #连接数据库
        client = MongoClient('mongodb://admin:azero123@172.16.10.14:27027/')
        db = client['asrspider']
        self.music = db["music"]
        self.music_detail=db["music_detail"]

        # 建立mongodb索引
        self.music.create_index([('title',1)], unique=True, background = True)
        self.music_detail.create_index([('title',1),('singer',1)], unique=True, background = True)

    def parse(self, response):
        for latter in self.latters:
            for page in self.pages:
                for sort in range(1,12):
                    singers_page=self.urlPattern.format(page,latter,sort)
                    yield response.follow(singers_page, self.parse_singer)

    def parse_singer(self,response):
        singer_list=response.xpath('//*[@class="r"]//li/a')
        for singer in singer_list:
            singer_name=singer.xpath('./@title').extract_first()
            detail_url=singer.xpath('./@href').extract_first()
            item=MusicItem()
            item['singer']=singer_name
            yield response.follow(detail_url, self.parse_singer_detail,meta={'item':item})


    def parse_singer_detail(self,response):
        # https://www.kugou.com/yy/singer/home/1574.html
        singer_id=re.split('[./]',response.url)[-2]
        item=response.meta['item']
        singer=item['singer']
        titles=response.xpath('//*[@class="text"]/@title').extract()
        for title in titles:
            item['title']=title
            self.music_count += 1
            yield item

    def closed(self,spider):
        now=datetime.datetime.now()
        nowtime=now.strftime('%Y-%m-%d %H:%M:%S')
        with open('./musicspider.log', 'a',encoding="utf-8") as wf:
            wf.write('酷狗音乐全量爬虫:\t'+str(self.music_count)+'条\t'+nowtime+'\n')
        print("酷狗音乐全量爬虫结束")
        print(nowtime)