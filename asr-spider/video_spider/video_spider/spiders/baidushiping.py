import scrapy
from video_spider.items import baidushipinSpiderItem
from video_spider.items import VideoSpiderItem
import datetime
import json
from pymongo import MongoClient
import math



class BaidushipinSpider(scrapy.Spider):
    name = 'baidushipin'
    # allowed_domains = ['http://v.baidu.com']
    start_urls = ['http://v.baidu.com/']
    custom_settings = {
        'DOWNLOAD_DELAY': 5 ,
        'LOG_LEVEL':'DEBUG'
    }

    urlPattern_movie="http://v.baidu.com/commonapi/movie2level/?filter=false&type={0}&area={1}&actor=&start={2}&complete=&order=pubtime&pn={3}&rating=&prop=&channel=movie"
    urlPattern_tvplay="http://v.baidu.com/commonapi/tvplay2level/?filter=false&type={0}&area={1}&actor=&start={2}&complete=&order=pubtime&pn={3}&rating=&prop=&channel=tvplay"
    urlPattern_tvshow="http://v.baidu.com/commonapi/tvshow2level/?filter=false&type={0}&area={1}&actor=&start={2}&complete=&order=pubtime&pn={3}&rating=&prop=&channel=tvshow"
    urlPattern_comic="http://v.baidu.com/commonapi/comic2level/?filter=false&type={0}&area={1}&actor=&start={2}&complete=&order=pubtime&pn={3}&rating=&prop=&channel=comic"
    urlPattern_shaoer="http://v.baidu.com/channel/commonapi/shaoer2level/?filter=false&type={0}&area={1}&actor=&start={2}&complete=&order=hot&pn={3}&rating=&prop=&channel=shaoer"



    years=["2021", "2020", "2019", "2018", "2017", "2016", "2015", "2014", "2013", "2012", "2011", "2010","00", "90", "80"]
    # 电影分类
    types_movie=["喜剧", "爱情", "恐怖", "惊悚","犯罪", "动作", "科幻", "战争","动画","剧情","青春","古装" "奇幻", "武侠" ,"冒险", "悬疑","传记", "运动", "音乐"]
    areas_movie=["内地", "美国", "香港", "台湾","韩国", "日本", "法国","英国", "德国", "泰国", "印度", "欧洲地区", "东南亚地区","其他地区"]

    #电视剧分类
    types_tvplay=['古装','都市','言情','武侠','战争','青春','喜剧','家庭','伦理','谍战','军旅','犯罪','动作','奇幻','神话','剧情','历史','经典']
    areas_tvplay=['内地','韩国','香港','台湾','日本','泰国','英国','新加坡','其他地区']

    # 综艺分类
    types_tvshow=['综合','真人秀','选秀','情感','脱口秀','访谈','相亲','播报','旅游','音乐','美食','纪实','曲艺','生活','游戏互动','财经','求职','网综']
    areas_tvshow=['港台','内地','日韩','欧美']

    # 动漫
    tpyes_comic=['情感','科幻','热血','推理','搞笑','冒险','萝莉','萝莉','校园','动作','机战','运动','战争','少年','少女','百合','社会','原创']
    areas_comic=['日本','欧美','国产','其他']

   # 动画片
    types_shaoer=['冒险','搞笑','动作','早教','幼儿','英语','动画','儿童','卡通','益智','亲子','热血','科幻','推理','幼教','经典','儿歌','励志']
    areas_shaoer=['日本','欧美','国产','其他']

    # channel=["电影","tvplay","动漫","综艺","动画片"]

    def __init__(self):
        # 获取爬取当天日期
        now=datetime.datetime.now()
        self.todayDate=now.strftime('%Y-%m-%d')

        #连接数据库
        client = MongoClient('mongodb://admin:azero123@172.16.10.14:27027/')
        db = client['asrspider']
        self.video_titles = db["video_titles"]
        self.baidushipin=db["baidushipin"]

    def parse(self, response):
        # 电影
        for ty in self.types_movie:
            for area in self.areas_movie:
                for year in self.years:
                        detail_url = self.urlPattern_movie.format(ty,area,year,1)
                        tab=baidushipinSpiderItem()
                        tab['style']=ty
                        tab['area']=area
                        tab['year']=year
                        tab['urlPattern']=self.urlPattern_movie
                        tab['category']='电影'
                        yield response.follow(detail_url, self.parse_total_page,meta={'item':tab})
        # 电视剧
        for ty in self.types_tvplay:
            for area in self.areas_tvplay:
                for year in self.years:
                        detail_url = self.urlPattern_tvplay.format(ty,area,year,1)
                        tab=baidushipinSpiderItem()
                        tab['style']=ty
                        tab['area']=area
                        tab['year']=year
                        tab['urlPattern']=self.urlPattern_tvplay
                        tab['category']='电视剧'
                        yield response.follow(detail_url, self.parse_total_page,meta={'item':tab})

        # 综艺
        for ty in self.types_tvshow:
            for area in self.areas_tvshow:
                for year in self.years:
                        detail_url = self.urlPattern_tvshow.format(ty,area,year,1)
                        tab=baidushipinSpiderItem()
                        tab['style']=ty
                        tab['area']=area
                        tab['year']=year
                        tab['urlPattern']=self.urlPattern_tvshow
                        tab['category']='综艺'
                        yield response.follow(detail_url, self.parse_total_page,meta={'item':tab})

        # 动漫
        for ty in self.tpyes_comic:
            for area in self.areas_comic:
                for year in self.years:
                        detail_url = self.urlPattern_comic.format(ty,area,year,1)
                        tab=baidushipinSpiderItem()
                        tab['style']=ty
                        tab['area']=area
                        tab['year']=year
                        tab['urlPattern']=self.urlPattern_comic
                        tab['category']='动漫'
                        yield response.follow(detail_url, self.parse_total_page,meta={'item':tab})
        # 动画片
        for ty in self.types_shaoer:
            for area in self.areas_shaoer:
                for year in self.years:
                        detail_url = self.urlPattern_shaoer.format(ty,area,year,1)
                        tab=baidushipinSpiderItem()
                        tab['style']=ty
                        tab['area']=area
                        tab['year']=year
                        tab['urlPattern']=self.urlPattern_shaoer
                        tab['category']='动画片'
                        yield response.follow(detail_url, self.parse_total_page,meta={'item':tab})

    def parse_total_page(self, response):
        result = json.loads(response.text,strict=False)
        total_num=int(result.get('total_num'))
        total_page=math.ceil(total_num/30)
        tab=response.meta['item']
        style=tab['style']
        area=tab['area']
        year=tab['year']
        urlPattern=tab['urlPattern']
        for i in range(1, total_page+1,1):
            detail_url = urlPattern.format(style,area,year,i)
            yield response.follow(detail_url, self.parse_list,meta={'item':tab})

    def parse_list(self, response):
        tab=response.meta['item']
        category=tab['category']
        result = json.loads(response.text,strict=False)
        if result.get('videoshow'):
            filmlist = result['videoshow']['videos']
            if filmlist != []:
                for film in filmlist:
                    title = film.get('title')
                    _id=film.get('id')
                    rawData=film
                    item=VideoSpiderItem()
                    item['title']=title

                    if self.baidushipin.find_one({"_id": _id}):
                        print("该Baidushipin原始数据已经保存")
                    else:
                        self.baidushipin.insert_one({ "_id":_id,"title": title, "rawData":rawData,"category":category,"create_date": self.todayDate })
                        with open('../nameDate/BaidushipinName.txt', 'a',encoding="utf-8") as wf:
                            wf.write(title+'\n')
                        print("原始数据添加成功")
                    yield item

    def closed(self,spider):
        now=datetime.datetime.now()
        nowtime=now.strftime('%Y-%m-%d %H:%M:%S')
        print("baiduhsiping爬虫结束")
        print(nowtime)
