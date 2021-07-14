import os
# * * */1 * * source ~/.bash_profile;source /home/hujinzhong/.pyenv/versions/3.8.3/envs/spider_virtual/bin/activate;cd /home/hujinzhong/spider/video_spider_update/;scrapy crawl qq > /home/hujinzhong/spider/video_spider_update/updateSpider.log
os.system('cd /home/hujinzhong/spider/video_spider_update/')
os.system("scrapy crawl baidushipin &")
os.system("scrapy crawl baidusousuo &")
os.system("scrapy crawl douban &")
os.system("scrapy crawl iqiyi &")
os.system("scrapy crawl qq &")
os.system("scrapy crawl sougou &")
