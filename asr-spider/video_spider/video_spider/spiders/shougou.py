import scrapy
from selenium import webdriver
from video_spider.items import VideoSpiderItem
from video_spider.items import baidushipinSpiderItem
import datetime
import re
import os
import os.path as osp
import json
from pymongo import MongoClient

class ShougouSpider(scrapy.Spider):
    name = 'sougou'
    # allowed_domains = ['v.sogou.com']
    start_urls = ['http://v.sogou.com/']
    custom_settings = {
        'DOWNLOAD_DELAY': 3,
        'LOG_LEVEL':'DEBUG'
    }

    # 电影url模板
    urlPattern_film=('''https://v.sogou.com/api/video/result?style={0}&zone={1}&
year={2}&starring=&fee=&order=&emcee=&req=class&query=
电影&entity=film&page={3}&pagesize=100''')
    # 电视剧
    urlPattern_tvplay='''https://v.sogou.com/api/video/result?style={0}&zone={1}
&year={2}&starring=&fee=&order=&emcee=&req=class&query=
电视剧&entity=teleplay&page={3}&pagesize=100'''
    # 动漫
    urlPattern_comic='''https://v.sogou.com/api/video/result?style={0}&zone={1}&
year={2}&starring=&fee=&order=&emcee=&req=class&query=
动漫&entity=cartoon&page={3}&pagesize=100'''
    # 纪录片
    urlPattern_documentary=('''https://v.sogou.com/api/video/result?style={0}&zone
={1}&year={2}&starring=&fee=&order=&emcee=&req=class
&query=纪录片&entity=documentary&page={3}&pagesize=100''')

    # 综艺
    urlPattern_tvshow='''https://v.sogou.com/api/video/result?style={0}&zone=&
year=&starring=&fee=&order=&emcee=&req=class&query=
综艺&entity=tvshow&page={1}&pagesize=100'''
    # 小品
    urlPattern_essay='''https://v.sogou.com/api/video/result?style=&zone=&
year=&starring=&fee=&order=&emcee=&req=class&query=
小品&entity=essay&page={0}&pagesize=100'''
    # 相声
    urlPattern_crosstalk='''https://v.sogou.com/api/video/result?style=&zone=&
year=&starring=&fee=&order=&emcee=&req=class&query=
相声&entity=crosstalk&page={0}&pagesize=100'''
    # 二人转
    urlPattern_pair='''https://v.sogou.com/api/video/result?style=&zone=&
year=&starring=&fee=&order=&emcee=&req=class&query=
二人转&entity=pair&page={0}&pagesize=100'''


    # 电影url模板
    styles_films=["剧情", "喜剧", "动作", "奇幻", "动画", "爱情", "冒险", "温情", "警匪", "悬疑", "亲情", "科幻", "经典", "战争", "成长", "魔幻", "青春", "文艺", "音乐", "推理"]
    zones_films=["内地", "美国", "香港", "日本", "英国", "韩国", "意大利", "台湾", "加拿大", "俄罗斯", "德国", "澳大利亚", "西班牙", "墨西哥", "泰国","新西兰", "土耳其", "肯尼亚", "其他"]
    years_films=["2030", "2028", "2027", "2026", "2025", "2024", "2023", "2022","2021", "2020", "2019", "2018", "2017", "2016", "2015", "2014", "2013", "2012", "2011", "2010"]
    # 电视剧
    styles_tvplays=["剧情", "爱情", "古装", "喜剧", "悬疑", "奇幻", "警匪",  "科幻", "成长", "武侠", "冒险", "经典", "家庭", "动作", "推理", "温情", "亲情", "历史", "战争"]
    zones_tvplays=["内地", "美国", "香港", "日本", "英国", "韩国", "意大利", "台湾", "加拿大", "俄罗斯", "德国", "澳大利亚", "西班牙", "墨西哥", "泰国", "欧美","新西兰", "土耳其", "肯尼亚", "其他"]
    years_tvplays=["2030", "2025", "2023", "2022", "2021", "2020", "2019", "2018", "2017", "2016", "2015", "2014", "2013", "2012", "2011", "2010", "2009", "2007", "2006", "2005"]
    # 动漫
    styles_comics=["动画","喜剧","冒险","励志","剧情", "科幻",  "悬疑", "青春","奇幻","魔幻", "爱情","校园","推理", "历史", "经典", "动作","温情", "警匪", "亲情",  "战争", "成长",  "青春",  "音乐", ]
    zones_comics=["内地", "美国", "香港", "日本", "英国", "韩国", "意大利", "台湾", "加拿大", "俄罗斯", "德国", "澳大利亚", "西班牙", "墨西哥", "泰国","新西兰", "土耳其", "肯尼亚", "欧美", "国漫", "日韩", "欧美","日漫", "法漫", "其他"]
    years_comics=["2021", "2020", "2019", "2018", "2017", "2016", "2015", "2014", "2013", "2012", "2011", "2010", "2009", "2007", "2006", "2005", "2004", "2003", "2002", "2000", "1999"]
    # 纪录片
    styles_documentars=["社会", "历史", "战争","运动", "温情", "人生", "青春", "剧情", "儿童", "传记", "成长"]
    zones_documentars=["内地", "美国", "香港", "日本", "英国", "韩国", "意大利", "台湾", "加拿大", "俄罗斯", "德国", "澳大利亚", "西班牙", "墨西哥", "泰国", "欧美", "新西兰", "土耳其", "欧美",  "肯尼亚","其他"]
    years_documentars=["2022", "2021", "2020", "2019", "2018", "2017", "2016", "2015", "2014", "2013", "2012", "2011", "2010", "2009", "2007", "2006", "2005", "2004", "2003"]
    # 综艺
    styles_tvshows=["喜剧", "社会", "音乐","历史", "温情", "儿童"]

    def __init__(self):
        # 获取爬取当天日期
        now=datetime.datetime.now()
        self.todayDate=now.strftime('%Y-%m-%d')

        #连接数据库
        client = MongoClient('mongodb://admin:azero123@172.16.10.14:27027/')
        db = client['asrspider']
        self.video_titles = db["video_titles"]
        self.sougou=db["sougou"]

    def parse(self, response):
        # 电影film
        for style in self.styles_films:
            for zone in self.zones_films:
                for year in self.years_films:
                    detail_url = self.urlPattern_film.format(style,zone,year,1)
                    tab=baidushipinSpiderItem()
                    tab['style']=style
                    tab['area']=zone
                    tab['year']=year
                    tab['urlPattern']=self.urlPattern_film
                    tab['category']='电影'
                    yield response.follow(detail_url, self.parse_page1,meta={'item':tab})

        # 电视剧tvplay
        for style in self.styles_tvplays:
            for zone in self.zones_tvplays:
                for year in self.years_tvplays:
                    detail_url = self.urlPattern_tvplay.format(style,zone,year,1)
                    tab=baidushipinSpiderItem()
                    tab['style']=style
                    tab['area']=zone
                    tab['year']=year
                    tab['urlPattern']=self.urlPattern_tvplay
                    tab['category']='电视剧'
                    yield response.follow(detail_url, self.parse_page1,meta={'item':tab})

        # 动漫comic
        for style in self.styles_comics:
            for zone in self.zones_comics:
                for year in self.years_comics:
                    detail_url = self.urlPattern_comic.format(style,zone,year,1)
                    tab=baidushipinSpiderItem()
                    tab['style']=style
                    tab['area']=zone
                    tab['year']=year
                    tab['urlPattern']=self.urlPattern_comic
                    tab['category']='动漫'
                    yield response.follow(detail_url, self.parse_page1,meta={'item':tab})

        # 纪录片documentar
        for style in self.styles_documentars:
            for zone in self.zones_documentars:
                for year in self.years_documentars:
                    detail_url = self.urlPattern_documentary.format(style,zone,year,1)
                    tab=baidushipinSpiderItem()
                    tab['style']=style
                    tab['area']=zone
                    tab['year']=year
                    tab['urlPattern']=self.urlPattern_documentary
                    tab['category']='纪录片'
                    print(detail_url)
                    yield response.follow(detail_url, self.parse_page1,meta={'item':tab})

        # 综艺tvshow
        for style in self.styles_tvshows:
            detail_url = self.urlPattern_tvshow.format(style,1)
            tab=baidushipinSpiderItem()
            tab['style']=style
            tab['urlPattern']=self.urlPattern_tvshow
            tab['category']='综艺'
            yield response.follow(detail_url, self.parse_page2,meta={'item':tab})

        # 小品essay
        detail_url = self.urlPattern_essay.format(1)
        tab=baidushipinSpiderItem()
        tab['urlPattern']=self.urlPattern_essay
        tab['category']='小品'
        yield response.follow(detail_url, self.parse_page3,meta={'item':tab})

        # 相声crosstalk
        detail_url = self.urlPattern_crosstalk.format(1)
        tab=baidushipinSpiderItem()
        tab['urlPattern']=self.urlPattern_crosstalk
        tab['category']='相声'
        yield response.follow(detail_url, self.parse_page3,meta={'item':tab})

        # 二人转pair
        detail_url = self.urlPattern_pair.format(1)
        tab=baidushipinSpiderItem()
        tab['urlPattern']=self.urlPattern_pair
        tab['category']='二人转'
        yield response.follow(detail_url, self.parse_page3,meta={'item':tab})

    def parse_page1(self,response):
        result = json.loads(response.text,strict=False)
        if result.get('longVideo'):
            page = result['longVideo']['pages']
            tab=response.meta['item']
            style=tab['style']
            zone=tab['area']
            year=tab['year']
            urlPattern=tab['urlPattern']
            for i in range(1, int(page)+1,1):
                detail_url = urlPattern.format(style,zone,year,i)
                print(detail_url)
                yield response.follow(detail_url, self.parse_list,meta={'item':tab})

    def parse_page2(self,response):
        result = json.loads(response.text,strict=False)
        if result.get('longVideo'):
            page = result['longVideo']['pages']
            tab=response.meta['item']
            style=tab['style']
            urlPattern=tab['urlPattern']
            for i in range(1, int(page)+1,1):
                detail_url = urlPattern.format(style,i)
                yield response.follow(detail_url, self.parse_list,meta={'item':tab})

    def parse_page3(self,response):
        result = json.loads(response.text,strict=False)
        if result.get('longVideo'):
            page = result['longVideo']['pages']
            tab=response.meta['item']
            urlPattern=tab['urlPattern']
            for i in range(1, int(page)+1,1):
                detail_url = urlPattern.format(i)
                yield response.follow(detail_url, self.parse_list,meta={'item':tab})

    def parse_list(self, response):
        tab=response.meta['item']
        category=tab['category']
        result = json.loads(response.text,strict=False)
        if result.get('longVideo'):
            filmlist = result['longVideo']['results']
            if filmlist != []:
                for film in filmlist:
                    title = film.get('name')
                    dockey=film.get('dockey')
                    rawData=film
                    item=VideoSpiderItem()
                    item['title']=title

                    if self.sougou.find_one({"_id": dockey}):
                        print("该sougou原始数据已经保存")
                    else:
                        self.sougou.insert_one({ "_id":dockey,"title": title, "rawData":rawData,"category":category,"create_date": self.todayDate })
                        with open('../nameDate/shouguoName.txt', 'a',encoding="utf-8") as wf:
                            wf.write(title+'\n')
                        print("原始数据添加成功")
                    yield item

    def closed(self,spider):
        now=datetime.datetime.now()
        nowtime=now.strftime('%Y-%m-%d %H:%M:%S')
        print("sougou爬虫结束")
        print(nowtime)

