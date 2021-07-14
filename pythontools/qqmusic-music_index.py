from pymongo import MongoClient
from datetime import datetime, timedelta
now=datetime.now()
todayDate=now.strftime('%Y-%m-%d')    #字符串形式的日期


client = MongoClient('mongodb://admin:azero123@172.16.10.14:27027/')
db = client['asrspider']
music = db["music"]
qq_music=db['qq_music']

music_count=0

# 以title为music建立索引
music.create_index([('title',1)], unique=True, background = True)


for title_data in qq_music.find({},{ "_id": 0, "title": 1},no_cursor_timeout=True):
    title=title_data['title']
    document={ "title": title, "create_date": todayDate }
    result_find={"title": title}
    music.update_one(result_find,{'$set': document},upsert=True)
    music_count+=1
    if music_count % 1000 == 0:
        print('music:'+str(music_count))


print('music_end:'+str(music_count))

