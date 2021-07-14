# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class VideoSpiderUpdatePipeline:
    def process_item(self, item, spider):
        # print(item)
        video_titles=spider.video_titles
        todayDate=spider.todayDate

        title=item['title']
        if video_titles.find_one({"title": title}):
            # print("该影视剧名称已经保存")
            pass
        else:
            video_titles.insert_one({ "title": title, "create_date": todayDate })
            # with open('../videoName.txt', 'a',encoding="utf-8") as wf:
            #     wf.write(title+'\n')
            # print("添加成功")
        return item