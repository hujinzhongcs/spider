import scrapy
from video_spider_update.items import VideoSpiderUpdateItem
from video_spider_update.items import baidushipinSpiderItem
import datetime
import os
import os.path as osp
import json
from pymongo import MongoClient


class SougouSpider(scrapy.Spider):
    name = 'sougou'
    allowed_domains = ['v.sogou.com']
    start_urls = ['http://v.sogou.com/']
    custom_settings = {
        'DOWNLOAD_DELAY': 3
    }
    querys=['电影','电视剧','动漫','纪录片','综艺','小品','相声','二人转']
    urlPattern='''https://v.sogou.com/api/video/result?style=&zone=&year=&
        starring=&fee=&order=time&emcee=&req=class&query={0}&entity=film&page
        ={1}&pagesize=100'''

    def __init__(self):
        # 获取爬取当天日期
        now=datetime.datetime.now()
        self.todayDate=now.strftime('%Y-%m-%d')
        nowtime=now.strftime('%Y-%m-%d %H:%M:%S')
        print("sougou更新开始  "+nowtime)

        #连接数据库
        client = MongoClient('mongodb://admin:azero123@172.16.10.14:27027/')
        db = client['asrspider']
        self.video_titles = db["video_titles"]
        self.sougou=db["sougou"]

    def parse(self, response):
        for query in self.querys:
            detail_url = self.urlPattern.format(query,1)
            tab=baidushipinSpiderItem()
            tab['style']=query
            yield response.follow(detail_url, self.parse_page,meta={'item':tab})

    def parse_page(self,response):
        result = json.loads(response.text,strict=False)
        if result.get('longVideo'):
            page = result['longVideo']['pages']
            tab=response.meta['item']
            query=tab['style']
            for i in range(1, int(page)+1,1):
                detail_url = self.urlPattern.format(query,i)
                yield response.follow(detail_url, self.parse_list,meta={'item':tab})

    def parse_list(self, response):
        tab=response.meta['item']
        category=tab['style']
        result = json.loads(response.text,strict=False)
        if result.get('longVideo'):
            filmlist = result['longVideo']['results']
            if filmlist != []:
                for film in filmlist:
                    title = film.get('name')
                    dockey=film.get('dockey')
                    rawData=film
                    item=VideoSpiderUpdateItem()
                    item['title']=title
                    item['category']=category
                    if self.sougou.find_one({"_id": dockey}):
                        # print("该原始数据已经保存")
                        pass
                    else:
                        self.sougou.insert_one({ "_id":dockey,"title": title, "rawData":rawData,"category":category,"create_date": self.todayDate })
                        # with open('../nameDate/shouguoName.txt', 'a',encoding="utf-8") as wf:
                        #     wf.write(title+'\n')
                        # print("原始数据添加成功")
                    yield item

    def closed(self,spider):
        now=datetime.datetime.now()
        nowtime=now.strftime('%Y-%m-%d %H:%M:%S')
        print("sougou更新结束  "+nowtime)