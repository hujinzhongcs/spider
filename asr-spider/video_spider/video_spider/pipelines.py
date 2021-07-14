# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient
import datetime

# 获取爬取当天日期
# now=datetime.datetime.now()
# todayDate=now.strftime('%Y-%m-%d')

# client = MongoClient('mongodb://admin:azero123@172.16.10.14:27027/')
# db = client['asrspider']
# video_titles = db["video_titles"]


class VideoSpiderPipeline:
    def process_item(self, item, spider):
        print(item)
        video_titles=spider.video_titles
        todayDate=spider.todayDate

        title=item['title']
        if video_titles.find_one({"title": title}):
            # print("影视剧名称已存在")
            pass
        else:
            video_titles.insert_one({ "title": title, "create_date": todayDate })
            # print("添加成功")
        return item