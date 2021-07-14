import scrapy
from video_spider.items import baidushipinSpiderItem
from video_spider.items import VideoSpiderItem
import datetime
import re
import os
import os.path as osp
import json
from pymongo import MongoClient


class BaidusousuoSpider(scrapy.Spider):
    name = 'baidusousuo'
    # allowed_domains = ['www.baidu.com']
    start_urls = ['http://www.baidu.com/']
    custom_settings = {
        'DOWNLOAD_DELAY': 10
    }
    urlPattern_film='''https://sp0.baidu.com/8aQDcjqpAAV3otqbppnN2DJv/api.php?resource_id=28286&from_mid=1&&format=json&ie=utf-8&oe=utf-8&query=电影&sort_key=16&sort_type=1&stat0=&stat1={}&stat2=&stat3=&pn={}&rn=100'''
    urlPattern_tvplay='''https://sp0.baidu.com/8aQDcjqpAAV3otqbppnN2DJv/api.php?resource_id=28287&from_mid=1&&format=json&ie=utf-8&oe=utf-8&query=电视剧&sort_key=16&sort_type=1&stat0=&stat1=&stat2=&stat3=&pn={}&rn=100'''
    urlPattern_tvshow='''https://sp0.baidu.com/8aQDcjqpAAV3otqbppnN2DJv/api.php?resource_id=28212&from_mid=1&&format=json&ie=utf-8&oe=utf-8&query=综艺&sort_key=16&sort_type=1&stat0=&stat1=&stat2=&stat3=&pn={}&rn=100'''
    urlPattern_comic='''https://sp0.baidu.com/8aQDcjqpAAV3otqbppnN2DJv/api.php?resource_id=28213&from_mid=1&&format=json&ie=utf-8&oe=utf-8&query=动漫&sort_key=16&sort_type=1&stat0=&stat1=&stat2=&stat3=&pn={}&rn=100'''
    urlPattern__netmove='''https://sp0.baidu.com/8aQDcjqpAAV3otqbppnN2DJv/api.php?resource_id=28286&from_mid=1&&format=json&ie=utf-8&oe=utf-8&query=网络电影&sort_key=16&sort_type=1&stat0=&stat1=&stat2=&stat3=&pn={}&rn=100'''



    areas_films=['大陆','香港','台湾','美国','韩国','日本','泰国','英国','德国','法国','意大利','加拿大','印度','俄罗斯','澳大利亚','西班牙','墨西哥','泰国','新西兰','巴西','土耳其']

    def __init__(self):
        # 获取爬取当天日期
        now=datetime.datetime.now()
        self.todayDate=now.strftime('%Y-%m-%d')

        #连接数据库
        client = MongoClient('mongodb://admin:azero123@172.16.10.14:27027/')
        db = client['asrspider']
        self.video_titles = db["video_titles"]
        self.baidusousuo=db["baidusousuo"]

    def parse(self, response):
        # 电视剧
        for i in range(0, 51834,100):
            detail_url = self.urlPattern_tvplay.format(i)
            tab=baidushipinSpiderItem()
            tab['category']='电视剧'
            tab['area']='未区分'
            yield response.follow(detail_url, self.parse_list,meta={'item':tab})
        # 综艺
        for i in range(0, 8719,100):
            detail_url = self.urlPattern_tvshow.format(i)
            tab=baidushipinSpiderItem()
            tab['category']='综艺'
            tab['area']='未区分'
            yield response.follow(detail_url, self.parse_list,meta={'item':tab})
        # 动漫
        for i in range(0, 18907,100):
            detail_url = self.urlPattern_comic.format(i)
            tab=baidushipinSpiderItem()
            tab['category']='动漫'
            tab['area']='未区分'
            yield response.follow(detail_url, self.parse_list,meta={'item':tab})
        # 网络电影
        for i in range(0, 159,100):
            detail_url = self.urlPattern__netmove.format(i)
            tab=baidushipinSpiderItem()
            tab['category']='网络电影'
            tab['area']='未区分'
            yield response.follow(detail_url, self.parse_list,meta={'item':tab})
        # 电影
        for area in self.areas_films:
            detail_url = self.urlPattern_film.format(area,0)
            tab=baidushipinSpiderItem()
            tab['category']='电影'
            tab['area']=area
            tab['urlPattern']=self.urlPattern_film
            yield response.follow(detail_url, self.parse_total_page,meta={'item':tab})


    def parse_total_page(self, response):
        tab=response.meta['item']
        area=tab['area']
        urlPattern=tab['urlPattern']
        # result = json.loads(re.findall(r"\((.*)\)",response.text)[0],strict=False)
        result = json.loads(response.text,strict=False)
        total_num = int(result['data'][0]['dispNum'])
        for i in range(0, total_num+1,100):
            detail_url = urlPattern.format(area,i)
            yield response.follow(detail_url, self.parse_list,meta={'item':tab})

    def parse_list(self, response):
        tab=response.meta['item']
        area=tab['area']
        category=tab['category']
        result = json.loads(response.text,strict=False)
        if result.get('data'):
            filmlist = result['data'][0]['result']
            if filmlist != []:
                for film in filmlist:
                    title = film.get('name')
                    rawData=film
                    item=VideoSpiderItem()
                    item['title']=title
                    if self.baidusousuo.find_one({"title": title}):
                        print("该baidu原始数据已经保存")
                    else:
                        self.baidusousuo.insert_one({"title": title, "rawData":rawData,"category":category,"area":area,"create_date": self.todayDate })
                        with open('../nameDate/baidusousuoName.txt', 'a',encoding="utf-8") as wf:
                            wf.write(title+'\n')
                        print("原始数据添加成功")
                    yield item

    def closed(self,spider):
        now=datetime.datetime.now()
        nowtime=now.strftime('%Y-%m-%d %H:%M:%S')
        print("baidusousuo爬虫结束")
        print(nowtime)

