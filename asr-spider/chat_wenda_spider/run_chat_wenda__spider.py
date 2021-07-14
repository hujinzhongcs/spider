import time
import os

# while True:
#     os.system("scrapy crawl tianya &")
#     time.sleep(86400)  #每隔一天运行一次 24*60*60=86400s

os.system("scrapy crawl tianya &")      #把历史数据爬完再每天运行 到时候得改爬虫中爬取的深度
# os.system("scrapy crawl baiduZhidaoDaily &")    #爬百度知道时ip被封,目前爬不到东西了