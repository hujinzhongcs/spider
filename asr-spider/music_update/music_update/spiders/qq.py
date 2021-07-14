import scrapy
import re
from selenium import webdriver
from music_update.items import MusicUpdateItem
import datetime
from pymongo import MongoClient

class QqSpider(scrapy.Spider):
    name = 'qq'
    # allowed_domains = ['y.qq.com']
    start_urls = ['https://y.qq.com/n/yqq/toplist/4.html']
    # 爬取条数计数
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
        music_list=response.xpath('//*[@class="toplist_nav__item"]/a/@href').extract()
        for page in music_list:
            yield response.follow(page, self.music_list)



    def music_list(self,response):
        song_list=response.xpath('//*[@class="songlist__list"]/li')
        for song in song_list:
            title=song.xpath('.//a[@class="js_song"]/text()').extract_first()
            singer=song.xpath('.//div[@class="songlist__artist"]/@title').extract_first()
            # singer_id=song.xpath('.//div[@class="songlist__artist"]/a/@data-singerid[1]').extract_first()
            item=MusicUpdateItem()
            item['title']=title
            item['singer']=singer
            self.music_count += 1
            yield item

    def closed(self,spider):
        now=datetime.datetime.now()
        nowtime=now.strftime('%Y-%m-%d %H:%M:%S')
        with open('./musicspider.log', 'a',encoding="utf-8") as wf:
            wf.write('QQ音乐更新爬虫:\t'+'爬取数量:\t'+str(self.music_count)+'\t'+'更新入库数量:\t'+str(self.increase)+'\t'+nowtime+'\n')
        print('QQ音乐更新爬虫:\t'+'爬取数量:\t'+str(self.music_count)+'\t'+'更新入库数量:\t'+str(self.increase)+'\t'+nowtime+'\n')
        print(nowtime)