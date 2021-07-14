# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import os
import os.path as osp

class BaikeSpiderPipeline:
    def process_item(self, item, spider):
        if spider.name == 'baiduBaike':
            sortDic={'baike':'baike'}
            print(item)
            url=item['url']
            time=item['time']
            website=item['website']
            content=item['content']
            sort=item['sort']
            filename=item['filename']

            if sort in sortDic:
                sort=sortDic[sort]
            else:
                sort='other'

            sort_dir='../data/'+website+sort+'/'
            if not osp.exists(sort_dir):
                os.makedirs(sort_dir)
            file_dir=osp.join(sort_dir,filename)

            if content =='':
                with open('baikeMessage', 'a',encoding="utf-8") as wf:
                    wf.write(time+'\t'+website+'\t'+sort+'\t'+sort+'\t'+str(0)+'\t'+filename+'\t'+ url+'\t'+'\n')
            else:
                with open(file_dir, 'w',encoding="utf-8") as h:
                    h.write(content)

                with open('baikeMessage', 'a',encoding="utf-8") as wf:
                    wf.write(time+'\t'+website+'\t'+sort+'\t'+sort+str(1)+'\t'+filename+'\t'+ url+'\t'+'\n')

            return item