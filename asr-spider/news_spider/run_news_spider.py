import time
import os

while True:
    os.system("scrapy crawl chinanews &")
    os.system("scrapy crawl sina &")
    os.system("scrapy crawl baidu &")
    os.system("scrapy crawl people &")
    os.system("scrapy crawl wangyi &")
    os.system("scrapy crawl cctv &")
    os.system("scrapy crawl qq &")
    os.system("scrapy crawl xinhuanet &")
    os.system("scrapy crawl ifeng &")
    time.sleep(86400)  #每隔一天运行一次 24*60*60=86400s