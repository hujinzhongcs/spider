from pymongo import MongoClient
from datetime import datetime, timedelta
now=datetime.now()
todayDate=now.strftime('%Y-%m-%d')    #字符串形式的日期


client = MongoClient('mongodb://admin:azero123@172.16.10.14:27027/')
db = client['asrspider']
music = db["music"]
music_detail=db['music_detail']
qq_music=db['qq_music']

music_count=0
musicupdate_count=0

for title_data in qq_music.find(no_cursor_timeout=True):
    title=title_data['title']
    singer=title_data['singer']
    # print(title)
    if not music.find_one({"title": title}):
        music.insert_one({ "title": title, "create_date": todayDate })
        music_count+=1
        if music_count % 100 == 0:
            print('music:'+str(music_count))


    if not music_detail.find_one({"title": title,"singer":singer}):
        music_detail.insert_one({"title": title, "singer":singer,"create_date": todayDate })
        musicupdate_count+=1
        if musicupdate_count % 100 == 0:
            print('musicupdate:'+str(musicupdate_count))

print(music_count)
print(musicupdate_count)
