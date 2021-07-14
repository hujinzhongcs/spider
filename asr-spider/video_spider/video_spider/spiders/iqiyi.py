import scrapy
from video_spider.items import VideoSpiderItem
import datetime
from pymongo import MongoClient
import json

class IqiyiSpider(scrapy.Spider):
    name = 'iqiyi'
    # allowed_domains = ['list.iqiyi.com']
    start_urls = ['http://list.iqiyi.com/']
    tpyes=['2','1','6','4','3','16','15','9','31',]

    market_release_date_levels=['2021','2020','2019','2018','2017','2011-2016','2000-2010','1990-1999','1980-1989','1964-1979']
    urlPattern_movie="https://pcw-api.iqiyi.com/search/recommend/list?channel_id=1&data_type=1&market_release_date_level={0}&mode=24&page_id={1}&ret_num=1000&three_category_id={2};must"
    # 电视剧网址模板
    urlPattern_tvplay='https://pcw-api.iqiyi.com/search/recommend/list?channel_id=2&data_type=1&market_release_date_level={0}&mode=24&page_id={1}&ret_num=1000&three_category_id={2};must'
    # 综艺
    urlPattern_tvshow='https://pcw-api.iqiyi.com/search/recommend/list?channel_id=6&data_type=1&market_release_date_level={0}&mode=24&page_id={1}&ret_num=1000&three_category_id={2};must'
    # 动漫
    urlPattern_comic='https://pcw-api.iqiyi.com/search/recommend/list?channel_id=4&data_type=1&market_release_date_level={0}&mode=24&page_id={1}&ret_num=1000&three_category_id={2};must'
    # 纪录片
    urlPattern_jilupain='https://pcw-api.iqiyi.com/search/recommend/list?channel_id=3&data_type=1&market_release_date_level={0}&mode=24&page_id={1}&ret_num=1000&three_category_id={2};must'
    # 网络电影
    urlPattern_netmove='https://pcw-api.iqiyi.com/search/recommend/list?channel_id=16&data_type=1&market_release_date_level={0}&mode=24&page_id={1}&ret_num=1000&three_category_id={2};must'
    # 儿童
    urlPattern_shaoer='https://pcw-api.iqiyi.com/search/recommend/list?channel_id=15&data_type=1&market_release_date_level={0}&mode=24&page_id={1}&ret_num=1000&three_category_id={2};must'

    # 电影分类
    three_category_id_movies=['8','6','11','131','291','128','10','289','12','23756','1284','129','9','7','130']  #类型 喜剧 爱情
    # 电视剧分类
    three_category_id_tvplays=['11992','24','20','23','30','1654','1653','24064','135','27916','1655','290','32','149','148','139','21','145','34','27','29','140','24063','27881','24065','32839']
    # 综艺
    three_category_id_tvshows=['155','156','158','159','292','293','2118','2224','30278','30279','33163','33172','33173','33182','33184','33193','33195','33196','33197','33198','33199','33200','33203','33205','33206','33220','33316','33317','33318','33319','33530','33531']
    # 动漫
    three_category_id_comics=['30230','30232','30233','30234','30237','30241','30243','30245','30247','30248','30249','30252','30254','30255','30256','30258','30265','30267','30270','32792','32793']
    # 纪录片
    three_category_id_jilupains=['70','72','74','73','77','71','28119','310','28173','28138']
    # 网络电影
    three_category_id_netmovies=['8','6','11','131','291','128','10','289','12','23756','1284','129','9','7','130']
    # 儿童
    three_category_id_shaoers=['31013','31014','31016','31017','31020','31022']


    def __init__(self):
        # 获取爬取当天日期
        now=datetime.datetime.now()
        self.todayDate=now.strftime('%Y-%m-%d')

        #连接数据库
        client = MongoClient('mongodb://admin:azero123@172.16.10.14:27027/')
        db = client['asrspider']
        self.video_titles = db["video_titles"]
        self.iqiyi=db["iqiyi"]

    def parse(self, response):
    # 电影
        for three_category_id in self.three_category_id_movies:
            for market_release_date_level in self.market_release_date_levels:
                for i in range(1,6):
                    detail_url = self.urlPattern_movie.format(market_release_date_level,i,three_category_id)
                    item=VideoSpiderItem()
                    item['category']='电影'
                    yield response.follow(detail_url, self.parse_list,meta={'item':item})
    # 电视剧
        for three_category_id in self.three_category_id_tvplays:
            for market_release_date_level in self.market_release_date_levels:
                for i in range(1,6):
                    detail_url = self.urlPattern_tvplay.format(market_release_date_level,i,three_category_id)
                    item=VideoSpiderItem()
                    item['category']='电视剧'
                    yield response.follow(detail_url, self.parse_list,meta={'item':item})
    # 综艺
        for three_category_id in self.three_category_id_tvshows:
            for market_release_date_level in self.market_release_date_levels:
                for i in range(1,6):
                    detail_url = self.urlPattern_tvshow.format(market_release_date_level,i,three_category_id)
                    item=VideoSpiderItem()
                    item['category']='综艺'
                    yield response.follow(detail_url, self.parse_list,meta={'item':item})
    # 动漫
        for three_category_id in self.three_category_id_comics:
            for market_release_date_level in self.market_release_date_levels:
                for i in range(1,6):
                    detail_url = self.urlPattern_comic.format(market_release_date_level,i,three_category_id)
                    item=VideoSpiderItem()
                    item['category']='动漫'
                    yield response.follow(detail_url, self.parse_list,meta={'item':item})
    # 纪录片
        for three_category_id in self.three_category_id_jilupains:
            for market_release_date_level in self.market_release_date_levels:
                for i in range(1,6):
                    detail_url = self.urlPattern_jilupain.format(market_release_date_level,i,three_category_id)
                    item=VideoSpiderItem()
                    item['category']='记录片'
                    yield response.follow(detail_url, self.parse_list,meta={'item':item})
    # 网络电影
        for three_category_id in self.three_category_id_netmovies:
            for market_release_date_level in self.market_release_date_levels:
                for i in range(1,6):
                    detail_url = self.urlPattern_netmove.format(market_release_date_level,i,three_category_id)
                    item=VideoSpiderItem()
                    item['category']='网络电影'
                    yield response.follow(detail_url, self.parse_list,meta={'item':item})
    # 儿童
        for three_category_id in self.three_category_id_shaoers:
            for market_release_date_level in self.market_release_date_levels:
                for i in range(1,6):
                    detail_url = self.urlPattern_shaoer.format(market_release_date_level,i,three_category_id)
                    item=VideoSpiderItem()
                    item['category']='儿童'
                    yield response.follow(detail_url, self.parse_list,meta={'item':item})

    def parse_list(self, response):
        result = json.loads(response.text,strict=False)
        item=response.meta['item']
        category=item['category']
        if result.get('data'):
            filmlist = result['data']['list']
            if filmlist != []:
                for film in filmlist:
                    title = film.get('title')
                    _id=film.get('albumId')
                    rawData=film
                    item=VideoSpiderItem()
                    item['title']=title
                    if self.iqiyi.find_one({"_id": _id}):
                        print("该iqiyi原始数据已经保存")
                    else:
                        self.iqiyi.insert_one({ "_id":_id,"title": title, "rawData":rawData,"category":category,"create_date": self.todayDate })
                        with open('../nameDate/iqiyiName.txt', 'a',encoding="utf-8") as wf:
                            wf.write(title+'\n')
                        print("原始数据添加成功")
                    yield item

    def closed(self,spider):
        now=datetime.datetime.now()
        nowtime=now.strftime('%Y-%m-%d %H:%M:%S')
        print("iqiyi爬虫结束")
        print(nowtime)
