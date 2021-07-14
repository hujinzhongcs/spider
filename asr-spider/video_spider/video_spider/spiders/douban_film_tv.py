import scrapy
from selenium import webdriver
from video_spider.items import VideoSpiderItem
import datetime
import re
import os
import os.path as osp
import json
from pymongo import MongoClient


class DoubanFilmTvSpider(scrapy.Spider):
    name = 'douban_film_tv'
    # allowed_domains = ['movie.douban.com']
    start_urls = ['http://movie.douban.com/']

    custom_settings = {
        'DOWNLOAD_DELAY': 30,
        'LOG_LEVEL':'DEBUG'
    }

    startPage = 0
    endPage = 1000
    urlPattern_tv="https://movie.douban.com/j/search_subjects?type=tv&tag={0}&sort=time&page_limit=2000&page_start={1}"
    urlPattern_movie="https://movie.douban.com/j/search_subjects?type=movie&tag={0}&sort=time&page_limit=2000&page_start={1}"
    tv_tags=['美剧','英剧','韩剧','日剧','国产剧','港剧','日本动画','综艺','纪录片']
    movie_tags=['热门','最新','经典','可播放','豆瓣高分','冷门佳作','华语','欧美','韩国','日本','动作','喜剧','爱情','科幻','悬疑','恐怖','成长']

    def __init__(self):
        # 获取爬取当天日期
        now=datetime.datetime.now()
        self.todayDate=now.strftime('%Y-%m-%d')

        #连接数据库
        client = MongoClient('mongodb://admin:azero123@172.16.10.14:27027/')
        db = client['asrspider']
        self.video_titles = db["video_titles"]
        self.douban=db["douban"]


    def parse(self, response):
        for tv_tag in self.tv_tags:
            for i in range(self.startPage, self.endPage+1,500):
                detail_url = self.urlPattern_tv.format(tv_tag,i)
                item=VideoSpiderItem()
                item['category']="电视剧"
                yield response.follow(detail_url, self.parse_list,meta={'item':item})

        for movie_tag in self.movie_tags:
            for i in range(self.startPage, self.endPage+1,500):
                detail_url = self.urlPattern_movie.format(movie_tag,i)
                item=VideoSpiderItem()
                item['category']="电影"
                yield response.follow(detail_url, self.parse_list,meta={'item':item})


    def parse_list(self, response):
        # print(response.text)
        item=response.meta['item']
        category=item['category']
        result = json.loads(response.text,strict=False)
        if result.get('subjects'):
            filmlist = result.get('subjects')
            if filmlist != []:
                for film in filmlist:
                    title = film.get('title')
                    item['title']=title
                    _id = film.get('id')
                    rawData=film
                    print(item)
                    # 存入原始数据
                    if self.douban.find_one({"_id": _id}):
                        print("该原始数据已经保存")
                    else:
                        self.douban.insert_one({ "_id":_id,"title": title, "rawData":rawData,"category":category,"create_date": self.todayDate })
                        with open('../nameDate/doubanName.txt', 'a',encoding="utf-8") as wf:
                            wf.write(title+'\n')
                        print("原始数据添加成功")
                    yield item


    def closed(self,spider):
        now=datetime.datetime.now()
        nowtime=now.strftime('%Y-%m-%d %H:%M:%S')
        print("douban_film_tv爬虫结束")
        print(nowtime)




