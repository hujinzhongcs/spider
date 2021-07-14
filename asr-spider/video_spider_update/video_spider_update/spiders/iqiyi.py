import scrapy
from video_spider_update.items import VideoSpiderUpdateItem
import datetime
from pymongo import MongoClient
import json


class IqiyiSpider(scrapy.Spider):
    name = 'iqiyi'
    # allowed_domains = ['list.iqiyi.com']
    start_urls = ['http://list.iqiyi.com/']
    channels=['2','1','6','4','3','16','15']
    categorys_dic={'2':'电视剧','1':'电影','6':'综艺','4':'动漫','3':'纪录片','16':'网络电影','15':'儿童'}
    urlPattern='''https://pcw-api.iqiyi.com/search/recommend/list?channel_id={}&data_type=1&mode=4&page_id=1&ret_num=1000'''

    def __init__(self):

        # 获取爬取当天日期
        now=datetime.datetime.now()
        self.todayDate=now.strftime('%Y-%m-%d')
        nowtime=now.strftime('%Y-%m-%d %H:%M:%S')
        print("iqiyi更新开始  "+nowtime)

        #连接数据库
        client = MongoClient('mongodb://admin:azero123@172.16.10.14:27027/')
        db = client['asrspider']
        self.video_titles = db["video_titles"]
        self.iqiyi=db["iqiyi"]

    def parse(self, response):
        for channel in self.channels:
            item=VideoSpiderUpdateItem()
            item['category']=self.categorys_dic[channel]
            detail_url = self.urlPattern.format(channel)
            yield response.follow(detail_url, self.parse_list,meta={'item':item})

    def parse_list(self, response):
        item=response.meta['item']
        category=item['category']
        result = json.loads(response.text,strict=False)
        if result.get('data'):
            filmlist = result['data']['list']
            if filmlist != []:
                for film in filmlist:
                    title = film.get('title')
                    _id=film.get('albumId')
                    rawData=film
                    item['title']=title
                    if self.iqiyi.find_one({"_id": _id}):
                        # print("该iqiyi原始数据已经保存")
                        pass
                    else:
                        self.iqiyi.insert_one({ "_id":_id,"title": title, "rawData":rawData,"category":category,"create_date": self.todayDate })
                        # with open('../nameDate/iqiyiName.txt', 'a',encoding="utf-8") as wf:
                        #     wf.write(title+'\n')
                        # print("原始数据添加成功")
                    yield item

    def closed(self,spider):
        now=datetime.datetime.now()
        nowtime=now.strftime('%Y-%m-%d %H:%M:%S')
        print("iqiyi更新结束  "+nowtime)