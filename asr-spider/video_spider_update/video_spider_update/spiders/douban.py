import scrapy
from video_spider_update.items import VideoSpiderUpdateItem
import datetime
import json
from pymongo import MongoClient

class DoubanSpider(scrapy.Spider):
    name = 'douban'
    # allowed_domains = ['movie.douban.com']
    start_urls = ['http://movie.douban.com/']
    custom_settings = {
        'DOWNLOAD_DELAY': 60
        # 'LOG_LEVEL':'DEBUG'
    }
    tags=['电影','电视剧','综艺','动漫','纪录片','短片']
    urlPattern="https://movie.douban.com/j/new_search_subjects?sort=R&range=0,10&tags={0}&start={1}"

    def __init__(self):
        # 获取爬取当天日期
        now=datetime.datetime.now()
        self.todayDate=now.strftime('%Y-%m-%d')
        nowtime=now.strftime('%Y-%m-%d %H:%M:%S')
        print("豆瓣更新开始  "+nowtime)

        #连接数据库
        client = MongoClient('mongodb://admin:azero123@172.16.10.14:27027/')
        db = client['asrspider']
        self.video_titles = db["video_titles"]
        self.douban=db["douban"]

    def parse(self, response):
        for tag in self.tags:
            for i in range(0,500,20):
                    detail_url = self.urlPattern.format(tag,i)
                    item=VideoSpiderUpdateItem()
                    item['category']=tag
                    yield response.follow(detail_url, self.parse_list,meta={'item':item})

    def parse_list(self, response):
        item=response.meta['item']
        category=item['category']
        result = json.loads(response.text,strict=False)
        if result.get('data'):
            filmlist = result.get('data')
            if filmlist != []:
                for film in filmlist:
                    _id = film.get('id')
                    rawData=film
                    title = film.get('title')
                    item['title']=title

                    # 存入原始数据
                    if self.douban.find_one({"_id": _id}):
                        # print("该原始数据已经保存")
                        pass
                    else:
                        self.douban.insert_one({ "_id":_id,"title": title, "rawData":rawData,"category":category,"create_date": self.todayDate })
                        # with open('../nameDate/doubanName.txt', 'a',encoding="utf-8") as wf:
                        #     wf.write(title+'\n')
                        # print("原始数据添加成功")
                    yield item

    def closed(self,spider):
        now=datetime.datetime.now()
        nowtime=now.strftime('%Y-%m-%d %H:%M:%S')
        print("豆瓣更新结束  "+nowtime)
