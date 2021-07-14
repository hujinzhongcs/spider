#!/bin/bash
# * 1 * * 5 /home/hujinzhong/spider/video_spider_update/run_updatespider.sh > /dev/null 2>&1 > /home/hujinzhong/spider/video_spider_update/run_updatespider.log
source ~/.bash_profile
echo "开始执行爬虫"
source /home/hujinzhong/.pyenv/versions/3.8.3/envs/spider_virtual/bin/activate
cd /home/hujinzhong/spider/video_spider_update/ && scrapy crawl baidushipin;scrapy crawl baidusousuo;scrapy crawl douban;scrapy crawl iqiyi;scrapy crawl qq;scrapy crawl sougou


# * */1 * * * /home/hujinzhong/spider/video_spider_update/run_updatespider.sh  > /home/hujinzhong/spider/video_spider_update/run_updatespider.log