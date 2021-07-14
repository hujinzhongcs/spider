import scrapy
from selenium import webdriver
from music.items import MusicItem
import datetime
from pymongo import MongoClient
from urllib import parse
import requests
import json
import math


class KuwoSpider(scrapy.Spider):
    name = 'kuwo'
    # allowed_domains = ['www.kuwo.cn']
    start_urls = ['http://www.kuwo.cn/singers']
    custom_settings = {
        'DOWNLOAD_DELAY': 3,
        'COOKIES_ENABLED' : False,
        'DOWNLOAD_TIMEOUT':1000,
        'LOG_LEVEL':'DEBUG'
        # 'DEPTH_PRIORITY' : 1,
        # 'SCHEDULER_DISK_QUEUE' : 'scrapy.squeues.PickleFifoDiskQueue',
        # 'SCHEDULER_MEMORY_QUEUE' : 'scrapy.squeues.FifoMemoryQueue'
    }
    headers = {
    'Cookie': 'kw_token=MXLBIUEPWEA',
    'csrf': 'MXLBIUEPWEA'
    }
    singerList_url='http://www.kuwo.cn/api/www/artist/artistInfo?category=0&prefix=&pn={}&rn=102&httpsStatus=1&reqId=c6fd22a0-a707-11eb-bd3e-672547198574'
    artistMusic_url='http://www.kuwo.cn/api/www/artist/artistMusic?artistid={}&pn={}&rn=100&httpsStatus=1&reqId=f46f1040-a725-11eb-b5c5-9f145f6e9326'
    music_count=0


    def __init__(self):
        # 获取爬取当天日期
        now=datetime.datetime.now()
        self.todayDate=now.strftime('%Y-%m-%d')

        #连接数据库
        #连接数据库
        client = MongoClient('mongodb://admin:azero123@172.16.10.14:27027/')
        db = client['asrspider']
        self.music = db["music"]
        self.music_detail=db["music_detail"]
        self.kuwo_music=db["kuwo_music"]

         # 建立mongodb索引
        self.music.create_index([('title',1)], unique=True, background = True)
        self.music_detail.create_index([('title',1),('singer',1)], unique=True, background = True)
        self.kuwo_music.create_index([('title',1),('singer',1)], unique=True, background = True)


    def parse(self, response):
        for pn in range(1,215):
            artistList_url=self.singerList_url.format(pn)
            yield response.follow(artistList_url, callback=self.parse_singerList)

    def parse_singerList(self,response):
        result = json.loads(response.text,strict=False)
        if result.get('data'):
            artistList = result['data']['artistList']
            for artist in artistList:
                artistname= artist['name']
                artist=artist['id']
                item=MusicItem()
                item['singer_id']=artist
                singer_url=self.artistMusic_url.format(artist,1)
                yield response.follow(singer_url, callback=self.parse_singer,meta={'item':item})


    def parse_singer(self,response):
        print("parse_singer")
        # print(response.text)
        item=response.meta['item']
        singer_id=item['singer_id']

        result = json.loads(response.text,strict=False)
        if result.get('data'):
            musicList = result['data']['list']
            total_num = result['data']['total']
            total_page=math.ceil(int(total_num)/100)
            for page in range(1,total_page+1,1):
                music_url=self.artistMusic_url.format(singer_id,page)
                yield response.follow(music_url,callback=self.parse_musicList)


    def parse_musicList(self,response):
        print('parse_musicList')
        result = json.loads(response.text,strict=False)
        if result.get('data'):
            musicList = result['data']['list']
            for music in musicList:
                title=music['name']
                singer=music['artist']
                rid=music['rid']

                kuwo_music_find={"title": title,"singer":singer}
                kuwo_music_document={"title": title, "singer":singer,'rid':rid,"detail":music,"create_date": self.todayDate }
                self.kuwo_music.update_one(kuwo_music_find,{'$set': kuwo_music_document},upsert=True)

                # if not self.kuwo_music.find_one({"title": title,"singer":singer,'rid':rid }):
                #     self.kuwo_music.insert_one({"title": title, "singer":singer,'rid':rid,"detail":music,"create_date": self.todayDate })

                item=MusicItem()
                item['title']=title
                item['singer']=singer
                self.music_count += 1
                yield item


    def closed(self,spider):
        now=datetime.datetime.now()
        nowtime=now.strftime('%Y-%m-%d %H:%M:%S')
        with open('./musicspider.log', 'a',encoding="utf-8") as wf:
            wf.write('酷我音乐全量爬虫:\t'+str(self.music_count)+'条\t'+nowtime+'\n')
        print("酷我音乐爬虫结束")
        print(nowtime)