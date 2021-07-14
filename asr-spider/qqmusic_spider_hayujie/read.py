from pymongo import MongoClient
client = MongoClient('mongodb://admin:azero123@172.16.10.14:27027/')
db = client['asrspider']
qq_music = db["qq_music"]

with open('title_nums', 'r', encoding='utf-8') as rf:
    for line in rf:
        line = line.strip()
        if not line:
            continue
        try:
            _id,title,singer,album,genre,language,time,company,comment = line.split("|||")
            # if not qq_music.find_one({"_id": _id}):
            qq_music.insert_one({"_id": _id, "title":title,"singer":singer,"albumd": album ,"genre": genre,"language": language,"time": time,"company": company,"comment": comment})
        except:
            print(line)