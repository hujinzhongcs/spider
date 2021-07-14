import time
import os

# while True:
os.system("scrapy crawl baidushiping &")
os.system("scrapy crawl baidushousuo &")
os.system("scrapy crawl douban_film_tv &")
os.system("scrapy crawl douban &")
os.system("scrapy crawl people &")
os.system("scrapy crawl iqiyi &")
os.system("scrapy crawl qq &")
os.system("scrapy crawl shouguou &")
    # time.sleep(604800)  #每隔一周运行一次 24*60*60*7=604800s