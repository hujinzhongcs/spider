import scrapy
import re
from selenium import webdriver
from music.items import MusicItem
import datetime
from pymongo import MongoClient



class WangyiyunSpider(scrapy.Spider):
    name = 'wangyiyun'
    # allowed_domains = ['music.163.com']
    start_urls = ['https://music.163.com/discover/artist/cat?id=1001&amp;initial=65']
    group_ids = ['1001']

    urlPattern='http://music.163.com/discover/artist/cat?id={gid}&initial={initial}'

    initials=['65','66','67','68','69','70','71','72','73','74','75','76','77',
        '78','79','80','81','82','83','84','85','86','87','88','89','90','0']
    group_ids = ['1001','1002','1003','2001','2002','2003','6001','6002','6003','7001',
        '7002','7003','4001','4002','4003']
    base_url = 'https://music.163.com'
    custom_settings = {
        'DOWNLOAD_DELAY': 3 ,
        # 'LOG_LEVEL':'DEBUG'
    }
    music_count=0


    def __init__(self):
        # 无头浏览器
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

    def start_requests(self):
        for group_id in self.group_ids:
            for initial in self.initials:
                url = 'https://music.163.com/discover/artist/cat?id={group_id}&amp;\
                    initial={initial}'.format(group_id=group_id,initial=initial)
                yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        artists = response.xpath('//*[@id="m-artist-box"]/li/p/a[1]/@href|//*[@id="m-artist-box"]/li/a[1]/@href').extract()
        for artist in artists:
            artist_url = 'https://music.163.com/artist/album?' + artist[8:]+'&limit=200&offset=0'
            yield response.follow(artist_url, callback=self.parse_singer)


    def parse_singer(self,response):
        albums = response.xpath('//*[@id="m-song-module"]/li/div/a[@class="msk"]/@href').extract()
        for album in albums:
            album_url = 'https://music.163.com' + album
            yield response.follow(album_url, callback=self.parse_album)
        next_button=response.xpath('//*[@class="u-page"]/a[last()]')
        a_class_name=next_button.xpath('./@class').extract_first()
        if a_class_name == 'zbtn znxt':
            next_album_url =next_button.xpath('./@href').extract_first()
            yield response.follow(next_album_url, self.parse_singer)


    def parse_album(self,response):
        trs = response.xpath('//*[@class="j-flag"]//tbody/tr')
        for tr in trs:
            title=tr.xpath('.//b/@title').extract_first()
            title=" ".join(title.split())
            singer=tr.xpath('.//*[@class="text"]/@title').extract_first()
            item=MusicItem()
            item['title']=title
            item['singer']=singer
            self.music_count += 1
            yield item


    def closed(self,spider):
        now=datetime.datetime.now()
        nowtime=now.strftime('%Y-%m-%d %H:%M:%S')
        with open('./musicspider.log', 'a',encoding="utf-8") as wf:
            wf.write('网易云全量爬虫:\t'+str(self.music_count)+'条\t'+nowtime+'\n')
        print("网易云音乐全量爬虫结束")
        print(nowtime)