import scrapy
from video_spider.items import VideoSpiderItem
from video_spider.items import baidushipinSpiderItem
import datetime
import json
from pymongo import MongoClient

class QqSpider(scrapy.Spider):
    name = 'qq'
    # allowed_domains = ['v.qq.com']
    custom_settings = {
        'DOWNLOAD_DELAY': 2,
        # 'LOG_LEVEL':'DEBUG'
    }
    start_urls = ['http://v.qq.com/']

    urlPattern_movie1='''https://v.qq.com/x/bu/pagesheet/list?_all=1&append=0&
        channel=movie&iarea={0}&listpage=2&offset={1}&pagesize=30&sort=19'''
    urlPattern_movie='''https://v.qq.com/x/bu/pagesheet/list?_all=1&append=0&
        channel=movie&characteristic=-1&iarea=-1&listpage=2&offset={1}&pagesize
        =30&sort=19&year={0}'''
    urlPattern_tv='''https://v.qq.com/x/bu/pagesheet/list?_all=1&append=1&
        channel=tv&feature=-1&iarea=-1&listpage=2&offset={1}&pagesize=30&sort
        =19&year={0}'''
    urlPattern_variety='''https://v.qq.com/x/bu/pagesheet/list?_all=1&append=0&
        channel=variety&iyear={0}&listpage=2&offset={1}&pagesize=30&sort=5'''
    urlPattern_cartoon='''https://v.qq.com/x/bu/pagesheet/list?_all=1&append=1&
        channel=cartoon&iyear={0}&listpage=2&offset={1}&pagesize=30&sort=23'''
    urlPattern_child='''https://v.qq.com/x/bu/pagesheet/list?_all=1&append=0
        &channel=child&itype={0}&listpage=2&offset={1}&pagesize=30&sort=18'''


    area_movies=['100024','100025','100029','100032','100026','100027','10028',
        '10030','10031','15','16','17','18','19','20','21','22','23','100033']
    year_tvs=['2021','2020','4061','4060','2017','859','860','861','862',
        '863','864','865','866']
    year_movies=['2021','2020','20','2018','2017','2016','10063','10034',
        '10035','10036','10037','10038','10039','10040']
    year_varietys=['-1']
    year_cartoons=['-1']
    type_childs=['1','2','3','4','5','7','6','8','9','10','11','12','13','14',
        '15','16']
    type_child_dic={'1':'儿歌','2':'益智','3':'手工绘画','4':'玩具','5':'英语',
        '7':'早教','6':'数学','8':'国学','9':'合家欢','10':'冒险','11':'交通工具',
        '12':'魔幻科幻','13':'动物','14':'真人特摄','15':'探索','16':'其他'}


    def __init__(self):
        # self.bro = webdriver.PhantomJS()

        # 获取爬取当天日期
        now=datetime.datetime.now()
        self.todayDate=now.strftime('%Y-%m-%d')

        #连接数据库
        client = MongoClient('mongodb://admin:azero123@172.16.10.14:27027/')
        db = client['asrspider']
        self.video_titles = db["video_titles"]
        self.qq=db["qq"]

    def parse(self, response):
        # 电影
        for area_movie in self.area_movies:
            detail_url = self.urlPattern_movie1.format(area_movie,0)
            tab=baidushipinSpiderItem()
            tab['year']='areas_movie'
            tab['category']='电影'
            tab['urlPattern']=self.urlPattern_movie1
            yield response.follow(detail_url, self.prase_page,meta={'item':tab})

        # 电影
        for year in self.year_movies:
            detail_url = self.urlPattern_movie.format(year,0)
            tab=baidushipinSpiderItem()
            tab['year']=year
            tab['category']='电影'
            tab['urlPattern']=self.urlPattern_movie
            yield response.follow(detail_url, self.prase_page,meta={'item':tab})

        # 电视剧
        for year in self.year_tvs:
            detail_url = self.urlPattern_tv.format(year,0)
            tab=baidushipinSpiderItem()
            tab['year']=year
            tab['category']='电视剧'
            tab['urlPattern']=self.urlPattern_tv
            yield response.follow(detail_url, self.prase_page,meta={'item':tab})

        # 综艺
        for year in self.year_varietys:
            detail_url = self.urlPattern_variety.format(0,year)
            tab=baidushipinSpiderItem()
            tab['year']=year
            tab['category']='综艺'
            tab['urlPattern']=self.urlPattern_variety
            yield response.follow(detail_url, self.prase_page,meta={'item':tab})

        # 动漫
        for year in self.year_cartoons:
            detail_url = self.urlPattern_cartoon.format(0,year)
            tab=baidushipinSpiderItem()
            tab['year']=year
            tab['category']='电视剧'
            tab['urlPattern']=self.urlPattern_cartoon
            yield response.follow(detail_url, self.prase_page,meta={'item':tab})

        # 少儿
        for year in self.type_childs:
            detail_url = self.urlPattern_child.format(0,year)
            tab=baidushipinSpiderItem()
            tab['year']=year
            tab['category']='少儿'
            tab['urlPattern']=self.urlPattern_child
            yield response.follow(detail_url, self.prase_page_child,meta={'item':tab})

    def prase_page(self, response):
        tab=response.meta['item']
        year=tab['year']
        urlPattern=tab['urlPattern']
        titleList=response.xpath('//*[@class="mod_pages"]/button/@data-offset').extract()
        for page in titleList:
            detail_url = urlPattern.format(year,page)
            yield response.follow(detail_url, self.parse_list,meta={'item':tab})

    def prase_page_child(self, response):
        tab=response.meta['item']
        year=tab['year']
        urlPattern=tab['urlPattern']
        titleList=response.xpath('//*[@class="mod_pages"]/button/@data-offset').extract()
        for page in titleList:
            detail_url = urlPattern.format(year,page)
            yield response.follow(detail_url, self.parse_list_child,meta={'item':tab})


    def parse_list(self, response):
        tab=response.meta['item']
        category=tab['category']
        titleList=response.xpath('//*[@class="list_item"]/div/a/@title').extract()
        for title in titleList:
            item=VideoSpiderItem()
            item['title']=title
            if self.qq.find_one({"title": title}):
                print("该baidu原始数据已经保存")
            else:
                self.qq.insert_one({"title": title, "category":category,"create_date": self.todayDate })
                with open('../nameDate/qqName.txt', 'a',encoding="utf-8") as wf:
                    wf.write(title+'\n')
                print("原始数据添加成功")
            # print(title)
            yield item

    def parse_list_child(self, response):
        tab=response.meta['item']
        category=tab['category']
        sort=tab['year']
        titleList=response.xpath('//*[@class="list_item"]/div/a/@title').extract()
        for title in titleList:
            item=VideoSpiderItem()
            item['title']=title
            if self.qq.find_one({"title": title}):
                print("该baidu原始数据已经保存")
            else:
                self.qq.insert_one({"title": title, "category":category,"sort":sort,"create_date": self.todayDate })
                with open('../nameDate/qqName.txt', 'a',encoding="utf-8") as wf:
                    wf.write(title+'\n')
                print("原始数据添加成功")
            print(title)
            yield item



    def closed(self,spider):
        now=datetime.datetime.now()
        nowtime=now.strftime('%Y-%m-%d %H:%M:%S')
        print("腾讯视频爬虫结束")
        print(nowtime)

