import scrapy
from selenium import webdriver
from music_update.items import MusicUpdateItem
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
        'LOG_LEVEL':'DEBUG',
        'DEFAULT_REQUEST_HEADERS' : {
            'Cookie': 'kw_token=WIRQUBZHL8A',
            'csrf': 'WIRQUBZHL8A'
        }
    }
    # 如果'DEBUG'中(failed 1 times): 504 Gateway Time-out错误过多，可将url中的rn=300改为rn=30
    musicList_url='http://www.kuwo.cn/api/www/bang/bang/musicList?bangId={}&pn=1&rn=300&httpsStatus=1&reqId=1c9dc140-a7d7-11eb-8d55-d94fcff98d55'
    rankList=['93','17','16','158','145','242','284','187','154','176','153',
        '26','278','185','64','294','291','292','290','279','296','297','295',
        '283','282','264','255','281']
    # rankList=['187']
    music_count=0
    increase=0

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
        for sort in self.rankList:
            musicList_url=self.musicList_url.format(sort)
            yield response.follow(musicList_url, callback=self.parse_musicList,meta={'download_timeout': 60})

    def parse_musicList(self,response):
        # print(response.text)
        result = json.loads(response.text,strict=False)
        if result.get('data'):
            musicList = result['data']['musicList']
            for music in musicList:
                title=music['name']
                singer=music['artist']
                rid=music['rid']

                kuwo_music_find={"title": title,"singer":singer}
                kuwo_music_document={"title": title, "singer":singer,'rid':rid,"detail":music,"create_date": self.todayDate }
                self.kuwo_music.update_one(kuwo_music_find,{'$set': kuwo_music_document},upsert=True)

                # if not self.kuwo_music.find_one({"title": title,"singer":singer,'rid':rid }):
                #     self.kuwo_music.insert_one({"title": title, "singer":singer,'rid':rid,"detail":music,"create_date": self.todayDate })

                item=MusicUpdateItem()
                item['title']=title
                item['singer']=singer
                self.music_count += 1
                yield item

    def closed(self,spider):
        now=datetime.datetime.now()
        nowtime=now.strftime('%Y-%m-%d %H:%M:%S')
        with open('./musicspider.log', 'a',encoding="utf-8") as wf:
            wf.write('酷我音乐更新爬虫:\t'+'爬取数量:\t'+str(self.music_count)+'\t'+'更新入库数量:\t'+str(self.increase)+'\t'+nowtime+'\n')
        print('酷我音乐更新爬虫:\t'+'爬取数量:\t'+str(self.music_count)+'\t'+'更新入库数量:\t'+str(self.increase)+'\t'+nowtime+'\n')
        print(nowtime)