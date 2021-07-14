from pymongo import MongoClient
from datetime import datetime, timedelta
now=datetime.now()
todayDate=now.strftime('%Y-%m-%d')    #字符串形式的日期


client = MongoClient('mongodb://admin:azero123@172.16.10.14:27027/')
db = client['asrspider']
music_detail=db["music_detail"]
qq_music=db['qq_music']

music_count=0

# 以title为music建立索引
music_detail.create_index([('title',1),('singer',1)], unique=True, background = True)


for title_data in qq_music.find({},{ "_id": 0, "title": 1, "singer": 1},no_cursor_timeout=True):
    title=title_data['title']
    singer= title_data['singer']

    document={ "title": title, "singer":singer,"create_date": todayDate }
    result_find={"title": title,"singer":singer}
    music_detail.update_one(result_find,{'$set': document},upsert=True)
    music_count+=1
    if music_count % 1000 == 0:
        print('music:'+str(music_count))


print('music_end:'+str(music_count))

