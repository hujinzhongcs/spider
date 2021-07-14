import scrapy
import re
from selenium import webdriver
from music_update.items import MusicUpdateItem
import datetime
from pymongo import MongoClient

class KugouSpider(scrapy.Spider):
    name = 'kugou'
    # allowed_domains = ['www.kugou.com']
    custom_settings = {
        'DOWNLOAD_DELAY': 5,
        # 'LOG_LEVEL':'DEBUG'
        # 'DEPTH_PRIORITY' : 1,
        # 'SCHEDULER_DISK_QUEUE' : 'scrapy.squeues.PickleFifoDiskQueue',
        # 'SCHEDULER_MEMORY_QUEUE' : 'scrapy.squeues.FifoMemoryQueue'
    }
    start_urls = ['https://www.kugou.com/yy/html/rank.html']
    music_count=0
    increase=0

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
        hot_list=response.xpath('//*[@class="pc_temp_side"]//li/a/@href').extract()
        for list_url in hot_list:
                yield response.follow(list_url, self.parse_list)

    def parse_list(self,response):
        singer_songs=response.xpath('//*[@class="pc_temp_songlist "]//li/@title').extract()
        for singer_song in singer_songs:
            singer= re.split('-', singer_song)[0]
            title= re.split('-', singer_song)[1]
            item=MusicUpdateItem()
            item['singer']=singer
            item['title']=title
            self.music_count += 1
            yield item

    def closed(self,spider):
        now=datetime.datetime.now()
        nowtime=now.strftime('%Y-%m-%d %H:%M:%S')
        with open('./musicspider.log', 'a',encoding="utf-8") as wf:
            wf.write('酷狗音乐更新爬虫:\t'+'爬取数量:\t'+str(self.music_count)+'\t'+'更新入库数量:\t'+str(self.increase)+'\t'+nowtime+'\n')
        print('酷狗音乐更新爬虫:\t'+'爬取数量:\t'+str(self.music_count)+'\t'+'更新入库数量:\t'+str(self.increase)+'\t'+nowtime+'\n')
        print(nowtime)
