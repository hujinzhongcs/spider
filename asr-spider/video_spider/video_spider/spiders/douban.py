import scrapy
from video_spider.items import VideoSpiderItem
import datetime
import json
from pymongo import MongoClient
import requests
from time import sleep

class DoubanSpider(scrapy.Spider):
    name = 'douban'
    # allowed_domains = ['https://movie.douban.com']
    start_urls = ['https://movie.douban.com/']
    startPage = 0
    endPage = 10000   #豆瓣一个分类最多能展示10000条以内条数据
    custom_settings = {
        'DOWNLOAD_DELAY': 30,
        'LOG_LEVEL':'DEBUG',
        # 'DEPTH_PRIORITY' : 1,
        # 'SCHEDULER_DISK_QUEUE' : 'scrapy.squeues.PickleFifoDiskQueue',
        # 'SCHEDULER_MEMORY_QUEUE' : 'scrapy.squeues.FifoMemoryQueue'
    }

    tags=['电影','电视剧','综艺','动漫','纪录片','短片']
    urlPattern="https://movie.douban.com/j/new_search_subjects?sort=U&range=0,10&tags={0}&start={1}&countries={2}&year_range={3}"
    countries=['中国大陆','欧美','美国','中国香港','中国台湾','日本','韩国','英国','法国','德国','意大利','西班牙','印度','泰国','俄罗斯','伊朗','加拿大','澳大利亚','爱尔兰','瑞典','巴西','丹麦']
    year_ranges=['2019,2021','2016,2018','2013,2015','2010,2012','2005,2009','2000,2004','1995,1999','1990,1994','1980,1989','1970,1979','1960,1969','1,1959']

    # genres=['剧情','喜剧','动作','爱情','科幻','动画','悬疑','惊恐','恐怖','犯罪','同性','音乐','歌舞','传记','历史','战争','西部','奇幻','冒险','灾难','武侠','情色']

    def __init__(self):
        # 获取爬取当天日期
        now=datetime.datetime.now()
        self.todayDate=now.strftime('%Y-%m-%d')

        #连接数据库
        client = MongoClient('mongodb://admin:azero123@172.16.10.14:27027/')
        db = client['asrspider']
        self.video_titles = db["video_titles"]
        self.douban=db["douban"]

    def parse(self, response):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36'}
        for tag in self.tags:
            for country in self.countries:
                for year_range in self.year_ranges:
                    for i in range(self.startPage, self.endPage+1,20):
                        detail_url = self.urlPattern.format(tag,i,country,year_range)
                        print(detail_url)
                        sleep(30)
                        responseResult = requests.get(detail_url, headers=headers)
                        result = json.loads(responseResult.text,strict=False)
                        # print(result)
                        if result.get('data'):
                            filmlist = result.get('data')
                            if filmlist != []:
                                for film in filmlist:
                                    _id = film.get('id')
                                    rawData=film
                                    title = film.get('title')
                                    item=VideoSpiderItem()
                                    item['title']=title
                                    item['category']=tag
                                    category=tag
                                    # print(item)

                                    # 存入原始数据
                                    if self.douban.find_one({"_id": _id}):
                                        print("该原始数据已经保存")
                                    else:
                                        self.douban.insert_one({ "_id":_id,"title": title, "rawData":rawData,"category":category,"create_date": self.todayDate })
                                        with open('../nameDate/doubanName.txt', 'a',encoding="utf-8") as wf:
                                            wf.write(title+'\n')
                                        print("原始数据添加成功")

                                    yield item

                            else:
                                print(result)
                                print("no data")
                                break
                        else:
                            print(result)
                            break


    def closed(self,spider):
        now=datetime.datetime.now()
        nowtime=now.strftime('%Y-%m-%d %H:%M:%S')
        print("douban爬虫结束")
        print(nowtime)



