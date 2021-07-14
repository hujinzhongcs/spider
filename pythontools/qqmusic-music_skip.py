from pymongo import MongoClient
from datetime import datetime, timedelta
now=datetime.now()
todayDate=now.strftime('%Y-%m-%d')    #字符串形式的日期


client = MongoClient('mongodb://admin:azero123@172.16.10.14:27027/')
db = client['asrspider']
music = db["music"]
music_detail=db['music_detail']
qq_music=db['qq_music']

count=0
music_count=0
# musicupdate_count=0

qqmusic_data_num = 3393303
for num in range(0,qqmusic_data_num,1000):

    # result = qq_music.find({},{ "_id": 0, "title": 1, "singer": 1 },no_cursor_timeout=True).skip(num).limit(1000)
    result = qq_music.find({},{ "_id": 0, "title": 1},no_cursor_timeout=True).skip(num).limit(1000)

    titleName=[]
    # title_singerName=[]
    for title_data in result:
        title=title_data['title']
        # singer=title_data['singer']

        count+=1
        if count % 10 == 0:
            print('count:'+str(count))

        if not music.find_one({"title": title},no_cursor_timeout=True):
            titleName.append({ "title": title, "create_date": todayDate })
            music_count+=1
            if music_count % 100 == 0:
                print('music:'+str(music_count))


        # if not music_detail.find_one({"title": title,"singer":singer},no_cursor_timeout=True):
        #     title_singerName.append({"title": title, "singer":singer,"create_date": todayDate })
        #     musicupdate_count+=1
        #     if musicupdate_count % 100 == 0:
        #         print('musicupdate:'+str(musicupdate_count))
    if len(titleName)!=0:
        music.insert_many(titleName)
    # music_detail.insert_many(title_singerName)

print('count_end:'+str(count))
print('music_end:'+str(music_count))
# print('musicupdate_end:'+str(musicupdate_count))

music.close()
qq_music.close()

