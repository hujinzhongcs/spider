# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class MusicPipeline:
    def process_item(self, item, spider):
        print(item)
        music=spider.music
        music_detail=spider.music_detail

        todayDate=spider.todayDate

        title=item['title']
        singer=item['singer']

        # 向music中插入歌曲名，如果存在则不再插入
        music_find={"title": title}
        music_document={ "title": title, "create_date": todayDate }
        music.update_one(music_find,{'$set': music_document},upsert=True)

        # 向music_detail中插入歌曲名和歌手名，如果存在则不再插入
        music_detail_find={"title": title,"singer":singer}
        music_detail_document={ "title": title, "singer":singer,"create_date": todayDate }
        music_detail.update_one(music_detail_find,{'$set': music_detail_document},upsert=True)

        # if music.find_one({"title": title}):
        #     print("该音乐名称已经保存")
        # else:
        #     music.insert_one({ "title": title, "create_date": todayDate })
        #     # with open('../videoName.txt', 'a',encoding="utf-8") as wf:
        #     #     wf.write(title+'\n')
        #     print("添加成功")
        # if not music_detail.find_one({"title": title,"singer":singer}):
        #     music_detail.insert_one({"title": title, "singer":singer,"create_date": todayDate })

        return item