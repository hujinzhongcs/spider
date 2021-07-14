from pymongo import MongoClient
from datetime import datetime, timedelta
import os
import os.path as osp

timeRange=7  #统计最近7天的数据
now=datetime.now()
todayDate=now.strftime('%Y-%m-%d')    #字符串形式的日期
today=datetime.strptime(todayDate,'%Y-%m-%d')


client = MongoClient('mongodb://admin:azero123@172.16.10.14:27027/')
db = client['asrspider']
movie_titles = db["video_titles"]

# /home/asrhotwords/2021-03-08/hotwords.txt

filename='hotwords.txt'
asrhotwords_dir='/home/asrhotwords/'+todayDate+'/'

if not osp.exists(asrhotwords_dir):
    os.makedirs(asrhotwords_dir)
file_dir=osp.join(asrhotwords_dir,filename)

with open(file_dir, 'w',encoding="utf-8") as wf:
    for title_data in movie_titles.find(no_cursor_timeout=True):
        title=title_data['title']
        create_date=title_data['create_date']
        create_date=datetime.strptime(create_date,'%Y-%m-%d')
        interval = (today - create_date).days
        if int(interval) < timeRange:
            wf.write(title+'\n')

print('更新完成')
