import scrapy
from video_spider_update.items import VideoSpiderUpdateItem
import datetime
import os
import os.path as osp
import json
from pymongo import MongoClient


class BaidushipinSpider(scrapy.Spider):
    name = 'baidushipin'
    # allowed_domains = ['v.baidu.com/movie/list/order-pubtime+pn-1+channel-movie']
    start_urls = ['http://v.baidu.com/movie/list/order-pubtime+pn-1+channel-movie/']

    custom_settings = {
        'DOWNLOAD_DELAY': 5
    }
    # 电影
    urlPattern_movie="http://v.baidu.com/commonapi/movie2level/?filter=false&type=&area=&actor=&start=&complete=&order=pubtime&pn={0}&rating=&prop=&channel=movie"
    #电视剧
    urlPattern_tvplay="http://v.baidu.com/commonapi/tvplay2level/?filter=false&type=&area=&actor=&start=&complete=&order=pubtime&pn={0}&rating=&prop=&channel=tvplay"
    # 综艺
    urlPattern_tvshow="http://v.baidu.com/commonapi/tvshow2level/?filter=false&type=&area=&actor=&start=&complete=&order=pubtime&pn={0}&rating=&prop=&channel=tvshow"
    # 动漫
    urlPattern_comic="http://v.baidu.com/commonapi/comic2level/?filter=false&type=&area=&actor=&start=&complete=&order=pubtime&pn={0}&rating=&prop=&channel=comic"
    # 动画片
    urlPattern_shaoer="http://v.baidu.com/channel/commonapi/shaoer2level/?filter=false&type=&area=&actor=&start=&complete=&order=pubtime&pn={0}&rating=&prop=&channel=shaoer"

    def __init__(self):
        # 获取爬取当天日期
        now=datetime.datetime.now()
        self.todayDate=now.strftime('%Y-%m-%d')
        nowtime=now.strftime('%Y-%m-%d %H:%M:%S')
        print("baiduhsipin更新开始  "+nowtime)

        #连接数据库
        client = MongoClient('mongodb://admin:azero123@172.16.10.14:27027/')
        db = client['asrspider']
        self.video_titles = db["video_titles"]
        self.baidushipin=db["baidushipin"]

    def parse(self, response):
        # 电影
        for i in range(1, 20,1):
            detail_url = self.urlPattern_movie.format(i)
            item=VideoSpiderUpdateItem()
            item['category']='电影'
            yield response.follow(detail_url, self.parse_list,meta={'item':item})
        # 电视剧
        for i in range(1, 20,1):
            detail_url = self.urlPattern_tvplay.format(i)
            item=VideoSpiderUpdateItem()
            item['category']='电视剧'
            yield response.follow(detail_url, self.parse_list,meta={'item':item})

        # 综艺
        for i in range(1, 20,1):
            detail_url = self.urlPattern_tvshow.format(i)
            item=VideoSpiderUpdateItem()
            item['category']='综艺'
            yield response.follow(detail_url, self.parse_list,meta={'item':item})
        # 动漫
        for i in range(1, 20,1):
            detail_url = self.urlPattern_comic.format(i)
            item=VideoSpiderUpdateItem()
            item['category']='动漫'
            yield response.follow(detail_url, self.parse_list,meta={'item':item})

        # 动画片
        for i in range(1, 20,1):
            detail_url = self.urlPattern_shaoer.format(i)
            item=VideoSpiderUpdateItem()
            item['category']='动画片'
            yield response.follow(detail_url, self.parse_list,meta={'item':item})

    def parse_list(self, response):
        item=response.meta['item']
        category=item['category']
        result = json.loads(response.text,strict=False)
        if result.get('videoshow'):
            filmlist = result['videoshow']['videos']
            if filmlist != []:
                for film in filmlist:
                    title = film.get('title')
                    _id=film.get('id')
                    rawData=film
                    item['title']=title

                    if self.baidushipin.find_one({"_id": _id}):
                        # print("该baidu原始数据已经保存")
                        pass
                    else:
                        self.baidushipin.insert_one({ "_id":_id,"title": title, "rawData":rawData,"category":category,"create_date": self.todayDate })
                        # with open('../nameDate/baidushipinName.txt', 'a',encoding="utf-8") as wf:
                        #     wf.write(title+'\n')
                        # print("原始数据添加成功")
                    yield item

    def closed(self,spider):
        now=datetime.datetime.now()
        nowtime=now.strftime('%Y-%m-%d %H:%M:%S')
        print("baiduhsipin更新结束  "+nowtime)