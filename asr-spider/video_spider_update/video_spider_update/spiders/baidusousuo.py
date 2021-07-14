import scrapy
from video_spider_update.items import VideoSpiderUpdateItem
import datetime
import os
import os.path as osp
import json
from pymongo import MongoClient

class BaidusousuoSpider(scrapy.Spider):
    name = 'baidusousuo'
    # allowed_domains = ['www.baidu.com']
    start_urls = ['''https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&tn=baidu&wd
        =%E7%94%B5%E8%A7%86%E5%89%A7&oq=%25E7%2594%25B5%25E5%25BD%25B1&rsv_pq=
        bccb26fb0005c61b&rsv_t=6678tI494pDjM2r6%2BbU0%2BsTB5d8eOHCZga%2FPFSBSM
        b%2FTg38DIElDfY1X8C0&rqlang=cn&rsv_enter=1&rsv_dl=tb&rsv_sug3=11&rsv_s
        ug1=9&rsv_sug7=100&rsv_sug2=0&rsv_btype=t&inputT=3910&rsv_sug4=3910''']

    custom_settings = {
        'DOWNLOAD_DELAY': 10
    }
    urlPattern_film='''https://sp0.baidu.com/8aQDcjqpAAV3otqbppnN2DJv/api.php?
    resource_id=28286&from_mid=1&&format=json&ie=utf-8&oe=utf-8&query=电影
    &sort_key=17&sort_type=1&stat0=&stat1=&stat2=&stat3=&pn={}&rn=100'''
    urlPattern_tvplay='''https://sp0.baidu.com/8aQDcjqpAAV3otqbppnN2DJv/api.php?
    resource_id=28287&from_mid=1&&format=json&ie=utf-8&oe=utf-8&query=电视剧
    &sort_key=17&sort_type=1&stat0=&stat1=&stat2=&stat3=&pn={}&rn=100'''
    urlPattern_tvshow='''https://sp0.baidu.com/8aQDcjqpAAV3otqbppnN2DJv/api.php?
    resource_id=28212&from_mid=1&&format=json&ie=utf-8&oe=utf-8&query=综艺
    &sort_key=17&sort_type=1&stat0=&stat1=&stat2=&stat3=&pn={}&rn=100'''
    urlPattern_comic='''https://sp0.baidu.com/8aQDcjqpAAV3otqbppnN2DJv/api.php?
    resource_id=28213&from_mid=1&&format=json&ie=utf-8&oe=utf-8&query=动漫
    &sort_key=17&sort_type=1&stat0=&stat1=&stat2=&stat3=&pn={}&rn=100'''
    urlPattern__netmove='''https://sp0.baidu.com/8aQDcjqpAAV3otqbppnN2DJv/api.php?
    resource_id=28286&from_mid=1&&format=json&ie=utf-8&oe=utf-8&query=网络电影
    &sort_key=17&sort_type=1&stat0=&stat1=&stat2=&stat3=&pn={}&rn=100'''

    def __init__(self):
        # 获取爬取当天日期
        now=datetime.datetime.now()
        self.todayDate=now.strftime('%Y-%m-%d')
        nowtime=now.strftime('%Y-%m-%d %H:%M:%S')
        print("baidusousuo更新开始  "+nowtime)

        #连接数据库
        client = MongoClient('mongodb://admin:azero123@172.16.10.14:27027/')
        db = client['asrspider']
        self.video_titles = db["video_titles"]
        self.baidusousuo=db["baidusousuo"]

    def parse(self, response):
        # 电视剧
        for i in range(0 , 2000 , 100):
            detail_url = self.urlPattern_tvplay.format(i)
            item=VideoSpiderUpdateItem()
            item['category']='电视剧'
            yield response.follow(detail_url, self.parse_list,meta={'item':item})
        # 电影
        for i in range(0, 2000 ,100):
            detail_url = self.urlPattern_film.format(i)
            item=VideoSpiderUpdateItem()
            item['category']='电影'
            yield response.follow(detail_url, self.parse_list,meta={'item':item})
        # 综艺
        for i in range(0, 2000 ,100):
            detail_url = self.urlPattern_tvshow.format(i)
            item=VideoSpiderUpdateItem()
            item['category']='综艺'
            yield response.follow(detail_url, self.parse_list,meta={'item':item})
        # 动漫
        for i in range(0, 2000 ,100):
            detail_url = self.urlPattern_comic.format(i)
            item=VideoSpiderUpdateItem()
            item['category']='动漫'
            yield response.follow(detail_url, self.parse_list,meta={'item':item})
        # 网络电影
        for i in range(0, 2000 ,100):
            detail_url = self.urlPattern__netmove.format(i)
            item=VideoSpiderUpdateItem()
            item['category']='网络电影'
            yield response.follow(detail_url, self.parse_list,meta={'item':item})

    def parse_list(self, response):
        item=response.meta['item']
        category=item['category']
        result = json.loads(response.text,strict=False)
        # 返回数据形式{"data":[{'result':[],'data'："no result"}]"status":0}
        if result.get('data'):
            if 'data' not in result['data'][0]:     #data："no result"无数据
                filmlist = result['data'][0]['result']
                if filmlist != []:
                    for film in filmlist:
                        title = film.get('name')
                        rawData=film
                        item['title']=title
                        if self.baidusousuo.find_one({"title": title}):
                            # print("该baidusousuo原始数据已经保存")
                            pass
                        else:
                            self.baidusousuo.insert_one({"title": title, "rawData":rawData,"category":category,"area":"未区分","create_date": self.todayDate })
                            # with open('../nameDate/baidusousuoName.txt', 'a',encoding="utf-8") as wf:
                            #     wf.write(title+'\n')
                        yield item

    def closed(self,spider):
        now=datetime.datetime.now()
        nowtime=now.strftime('%Y-%m-%d %H:%M:%S')
        print("baidusousuo更新结束  "+nowtime)

