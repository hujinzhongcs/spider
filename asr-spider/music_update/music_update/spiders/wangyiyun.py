import scrapy
import re
from selenium import webdriver
from music_update.items import MusicUpdateItem
import datetime
from pymongo import MongoClient
import os.path as osp
import os


class WangyiyunSpider(scrapy.Spider):
    name = 'wangyiyun'
    # allowed_domains = ['music.163.com']
    start_urls = ['https://music.163.com/discover/toplist']
    sortid=['19723756', '3779629', '2884035', '3778678', '5453912201', '991319590',
     '71384707', '1978921795', '71385702', '745956260', '10520166', '180106',
     '60198', '3812895', '21845217', '11641012', '60131', '2809513713',
     '2809577409', '27135204', '3001835560', '3001795926', '3001890046',
     '3112516681', '5059644681', '5059633707', '5059642708', '5338990334',
     '5059661515']
    urlPattern='https://music.163.com/discover/toplist?id={}'
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
        for sort in self.sortid:
            sort_url=self.urlPattern.format(sort)
            # print(sort_url)
            yield response.follow(sort_url,self.parse_sort)

    def parse_sort(self,response):
        print(response.url)
        path='../musicName/'
        if not osp.exists(path):
            os.makedirs(path)
        trs=response.xpath('//*[@class="m-table m-table-rank"]/tbody/tr')
        for tr in trs:
            song = tr.xpath('.//*[@class="txt"]/a/b/@title').extract_first()
            singer=tr.xpath('.//*[@class="text"]/@title').extract_first()
            if '-' in song:
                title = song.split('-')[0]
            else:
                title = song
            item=MusicUpdateItem()
            item['title']=title
            item['singer']=singer
            self.music_count += 1
            yield item

    def closed(self,spider):
        now=datetime.datetime.now()
        nowtime=now.strftime('%Y-%m-%d %H:%M:%S')
        with open('./musicspider.log', 'a',encoding="utf-8") as wf:
            wf.write('网易云更新爬虫:\t'+'爬取数量:\t'+str(self.music_count)+'\t'+'更新入库数量:\t'+str(self.increase)+'\t'+nowtime+'\n')
        print('网易云更新爬虫:\t'+'爬取数量:\t'+str(self.music_count)+'\t'+'更新入库数量:\t'+str(self.increase)+'\t'+nowtime+'\n')
        print(nowtime)