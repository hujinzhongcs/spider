#!/bin/bash
# * 1 * * 5 /home/hujinzhong/spider/music_update/run_updatespider.sh > /dev/null 2>&1 > /home/hujinzhong/spider/music_update/run_updatespider.log
source ~/.bash_profile
echo "开始执行音乐更新爬虫"
source /home/hujinzhong/.pyenv/versions/3.8.3/envs/spider_virtual/bin/activate
cd /home/hujinzhong/spider/music_update/ && scrapy crawl kugou;scrapy crawl kuwo;scrapy crawl qq;scrapy crawl wangyiyun


# * */1 * * * /home/hujinzhong/spider/music_update/run_updatespider.sh  > /home/hujinzhong/spider/music_update/run_updatespider.log