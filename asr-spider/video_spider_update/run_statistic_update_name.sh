#!/bin/bash
# * 3 * * 0 /home/hujinzhong/spider/video_spider_update/run_statistic_update_name.sh > /dev/null 2>&1 > /home/hujinzhong/spider/video_spider_update/run_statistic_update_name.log
source ~/.bash_profile
echo "开始统计更新的影视剧名称"
source /home/hujinzhong/.pyenv/versions/3.8.3/envs/spider_virtual/bin/activate
cd /home/hujinzhong/spider/video_spider_update/ && python statistic_update_name.py


