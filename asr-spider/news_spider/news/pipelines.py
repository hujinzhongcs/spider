# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import os
import os.path as osp

# 百科，闲聊/社交/论坛，教育'education'，金融/财经'finance'，军事'military'，新闻'news'，问答，文学/小说，医疗'medical'、体育'sports'、科技'technology'


#  文件名 时间 站点 领域 链接
class NewsPipeline:
    def process_item(self, item, spider):
        # if isinstance(item,NewsItem)
        if spider.name == 'baidu':
            print(item)

            statistics_Dic={'guonei':'news','guoji':'news','internet':'news','sports':'sports','ent':'news',
            'mil':'military','tech':'technology','finance':'finance','game':'news','lady':'news','auto':'news',
            'house':'news'}

            storage_Dic={'guonei':'国内','guoji':'国际','internet':'互联网','sports':'体育','ent':'娱乐','mil':'军事',
             'tech':'科技','finance':'财经','game':'游戏','lady':'女人','auto':'汽车','house':'房产'}

            url=item['url']
            time=item['time']
            website=item['website']
            filename=item['filename']
            content=item['content']
            sort=item['sort']

            if sort in storage_Dic:
                website_sort=storage_Dic[sort]
            else:
                website_sort='其他'

            if sort in statistics_Dic:
                statistics_sort=statistics_Dic[sort]
            else:
                statistics_sort='other'

            sort_dir='../data/'+website+'/'+website_sort+'/'
            if not osp.exists(sort_dir):
                os.makedirs(sort_dir)
            file_dir=osp.join(sort_dir,filename)

            if content =='':
                with open('../webMessage', 'a',encoding="utf-8") as wf:
                    wf.write(time+'\t'+website+'\t'+statistics_sort+'\t'+website_sort+'\t'+str(0)+'\t'+filename+'\t'+ url+'\t'+'\n')
            else:
                with open(file_dir, 'w',encoding="utf-8") as h:
                    h.write(content)

                with open('../webMessage', 'a',encoding="utf-8") as wf:
                    wf.write(time+'\t'+website+'\t'+statistics_sort+'\t'+website_sort+'\t'+str(1)+'\t'+filename+'\t'+ url+'\t'+'\n')

            return item


        if spider.name == 'sina':
            print(item)
            statistics_Dic={'国内':'news','国际':'news','社会':'news','体育':'sports','娱乐':'news',
            '军事':'military','科技':'technology','财经':'finance','股市':'finance','美股':'finance'}

            url=item['url']
            time=item['time']
            website=item['website']
            filename=item['filename']
            content=item['content']
            sort=item['sort']

            website_sort=sort

            if sort in statistics_Dic:
                statistics_sort=statistics_Dic[sort]
            else:
                statistics_sort='other'

            sort_dir='../data/'+website+'/'+website_sort+'/'
            if not osp.exists(sort_dir):
                os.makedirs(sort_dir)
            file_dir=osp.join(sort_dir,filename)

            if content =='':
                with open('../webMessage', 'a',encoding="utf-8") as wf:
                    wf.write(time+'\t'+website+'\t'+statistics_sort+'\t'+website_sort+'\t'+str(0)+'\t'+filename+'\t'+ url+'\t'+'\n')
            else:
                with open(file_dir, 'w',encoding="utf-8") as h:
                    h.write(content)

                with open('../webMessage', 'a',encoding="utf-8") as wf:
                    wf.write(time+'\t'+website+'\t'+statistics_sort+'\t'+website_sort+'\t'+str(1)+'\t'+filename+'\t'+ url+'\t'+'\n')

            return item


        elif spider.name == 'chinanews':
            print(item)

            statistics_Dic={'国内':'news','国际':'news','社会':'news','军事':'military',
            '港澳':'news','台湾':'news','华人':'news','财经':'finance','金融':'finance',
            '产经':'finance','房产':'news','汽车':'news','能源':'news','I T':'technology',
            '文化':'news','娱乐':'news','体育':'sports','教育':'education','健康':'medical',
            '生活':'news','葡萄酒':'news','图片':'news','视频':'news','精选':'news'}

            url=item['url']
            time=item['time']
            website=item['website']
            filename=item['filename']
            content=item['content']
            sort=item['sort']

            website_sort=sort

            if sort in statistics_Dic:
                statistics_sort=statistics_Dic[sort]
            else:
                statistics_sort='other'

            sort_dir='../data/'+website+'/'+website_sort+'/'
            if not osp.exists(sort_dir):
                os.makedirs(sort_dir)
            file_dir=osp.join(sort_dir,filename)

            if content =='':
                with open('../webMessage', 'a',encoding="utf-8") as wf:
                    wf.write(time+'\t'+website+'\t'+statistics_sort+'\t'+website_sort+'\t'+str(0)+'\t'+filename+'\t'+ url+'\t'+'\n')
            else:
                with open(file_dir, 'w',encoding="utf-8") as h:
                    h.write(content)

                with open('../webMessage', 'a',encoding="utf-8") as wf:
                    wf.write(time+'\t'+website+'\t'+statistics_sort+'\t'+website_sort+'\t'+str(1)+'\t'+filename+'\t'+ url+'\t'+'\n')

            return item

        elif spider.name == 'people':
            print(item)

            statistics_Dic={'politics': 'news', 'world': 'news', 'finance': 'finance', 'tw': 'news',
             'military': 'military', 'opinion': 'news', 'leaders': 'news', 'v': 'news', 'renshi': 'news',
            'theory': 'news', 'legal': 'news', 'society': 'news', 'industry': 'news', 'edu': 'education',
            'lxjk': 'news', 'sports': 'sports', 'culture': 'news', 'art': 'news', 'house': 'news',
            'auto': 'news', 'health': 'medical', 'scitech': 'technology', 'pic': 'news', 'dangjian': 'news',
            'dangshi': 'news', 'fanfu': 'news', 'hm': 'news', 'media': 'news', 'rmfp': 'news',
            'ccnews': 'news', 'fangtan': 'news', 'tc': 'news', 'it': 'technology', 'capital': 'news',
            'yuqing': 'news', 'graphicnews': 'news', 'mooc': 'news', 'coo': 'news', 'country': 'news',
            'money': 'finance', 'energy': 'news', 'gongyi': 'news', 'env': 'news', 'shipin': 'news',
            'jiu': 'news', 'fashion': 'news', 'ent': 'news', 'xiaofei': 'news', 'game': 'news',
            'caipiao': 'news', 'travel': 'news', '5gcenter': 'news', 'unn': 'news', 'yunying': 'news',
            'blockchain': 'news', 'ip': 'news', 'ru':'news', 'korea':'news','cpc':'news','usa':'news',
            'qipai':'news', 'australia':'news','japan':'news','kpzg':'news'}

            storage_Dic={'politics': '时政', 'world': '国际', 'finance': '财经', 'tw': '台湾',
             'military': '军事', 'opinion': '观点', 'leaders': '领导', 'v': '视频', 'renshi': '人事',
            'theory': '理论', 'legal': '法制', 'society': '社会', 'industry': '产经', 'edu': '教育',
            'lxjk': 'news', 'sports': '体育', 'culture': '文化', 'art': '书画', 'house': '房产',
            'auto': '汽车', 'health': '健康', 'scitech': '科技', 'pic': '图片', 'dangjian': '党建',
            'dangshi': '党史', 'fanfu': '反腐', 'hm': '港澳', 'media': '传媒', 'rmfp': '扶贫',
            'ccnews': '央企', 'fangtan': '访谈', 'tc': '通信', 'it': 'IT', 'capital': '创投',
            'yuqing': '舆情', 'graphicnews': '图解新闻', 'mooc': '慕课', 'coo': '人民智作', 'country': '美丽乡村',
            'money': '金融', 'energy': '能源', 'gongyi': '公益', 'env': '环保', 'shipin': '食品',
            'jiu': '酒业', 'fashion': '时尚', 'ent': '娱乐', 'xiaofei': '消费', 'game': '游戏',
            'caipiao': '彩票', 'travel': '旅游', '5gcenter': '5G', 'unn': '地方', 'yunying': '运营',
            'blockchain': '区块链', 'ip': '知识产权', 'ru':'俄罗斯', 'korea':'韩国','cpc':'中国共产党','usa':'美国频道',
            'qipai':'棋牌', 'australia':'澳大利亚','japan':'日本','kpzg':'科普','npc': '中国人大'}

            url=item['url']
            time=item['time']
            website=item['website']
            filename=item['filename']
            content=item['content']
            sort=item['sort']

            if sort in storage_Dic:
                website_sort=storage_Dic[sort]
            else:
                website_sort='其他'

            if sort in statistics_Dic:
                statistics_sort=statistics_Dic[sort]
            else:
                statistics_sort='other'

            sort_dir='../data/'+website+'/'+website_sort+'/'
            if not osp.exists(sort_dir):
                os.makedirs(sort_dir)
            file_dir=osp.join(sort_dir,filename)

            if content =='':
                with open('../webMessage', 'a',encoding="utf-8") as wf:
                    wf.write(time+'\t'+website+'\t'+statistics_sort+'\t'+website_sort+'\t'+str(0)+'\t'+filename+'\t'+ url+'\t'+'\n')
            else:
                with open(file_dir, 'w',encoding="utf-8") as h:
                    h.write(content)

                with open('../webMessage', 'a',encoding="utf-8") as wf:
                    wf.write(time+'\t'+website+'\t'+statistics_sort+'\t'+website_sort+'\t'+str(1)+'\t'+filename+'\t'+ url+'\t'+'\n')

            return item


        elif spider.name == 'wangyi':
            print(item)
            statistics_Dic = {"guonei":"news", "guoji":"news", "yaowen":"news", "shehui":"news",
            "war":"military", "money":"finance","tech":"technology", "sports":"sports",
            "ent":"news","lady":"news", "auto":"news", "jiaoyu":"education",
            "jiankang":"medical", "hangkong":"news"}
            storage_Dic={"guonei":"国内", "guoji":"国际", "yaowen":"要闻", "shehui":"社会", "war":"军事", "money":"财经",
            "tech":"科技", "sports":"体育", "ent":"娱乐", "lady":"时尚","auto":"汽车", "jiaoyu":"教育", "jiankang":"健康",
             "hangkong":"航空"}
            url=item['url']
            time=item['time']
            website=item['website']
            filename=item['filename']
            content=item['content']
            sort=item['sort']

            if sort in storage_Dic:
                website_sort=storage_Dic[sort]
            else:
                website_sort='其他'

            if sort in statistics_Dic:
                statistics_sort=statistics_Dic[sort]
            else:
                statistics_sort='other'

            sort_dir='../data/'+website+'/'+website_sort+'/'
            if not osp.exists(sort_dir):
                os.makedirs(sort_dir)
            file_dir=osp.join(sort_dir,filename)

            if content =='':
                with open('../webMessage', 'a',encoding="utf-8") as wf:
                    wf.write(time+'\t'+website+'\t'+statistics_sort+'\t'+website_sort+'\t'+str(0)+'\t'+filename+'\t'+ url+'\t'+'\n')
            else:
                with open(file_dir, 'w',encoding="utf-8") as h:
                    h.write(content)

                with open('../webMessage', 'a',encoding="utf-8") as wf:
                    wf.write(time+'\t'+website+'\t'+statistics_sort+'\t'+website_sort+'\t'+str(1)+'\t'+filename+'\t'+ url+'\t'+'\n')

            return item

        elif spider.name == 'cctv':
            print(item)
            statistics_Dic = {'china':'news','world':'news','society':'news','law':'news','health':'news',
            'economy_zixun':'finance','edu':'education'}
            storage_Dic = {'china':'国内','world':'国际','society':'社会','law':'法制','health':'健康',
            'economy_zixun':'经济','edu':'教育'}
            url=item['url']
            time=item['time']
            website=item['website']
            filename=item['filename']
            content=item['content']
            sort=item['sort']

            if sort in storage_Dic:
                website_sort=storage_Dic[sort]
            else:
                website_sort='其他'

            if sort in statistics_Dic:
                statistics_sort=statistics_Dic[sort]
            else:
                statistics_sort='other'

            sort_dir='../data/'+website+'/'+website_sort+'/'
            if not osp.exists(sort_dir):
                os.makedirs(sort_dir)
            file_dir=osp.join(sort_dir,filename)

            if content =='':
                with open('../webMessage', 'a',encoding="utf-8") as wf:
                    wf.write(time+'\t'+website+'\t'+statistics_sort+'\t'+website_sort+'\t'+str(0)+'\t'+filename+'\t'+ url+'\t'+'\n')
            else:
                with open(file_dir, 'w',encoding="utf-8") as h:
                    h.write(content)

                with open('../webMessage', 'a',encoding="utf-8") as wf:
                    wf.write(time+'\t'+website+'\t'+statistics_sort+'\t'+website_sort+'\t'+str(1)+'\t'+filename+'\t'+ url+'\t'+'\n')

            return item

        elif spider.name == 'qq':
            print(item)
            statistics_Dic={'politics':'news', 'social':'news', 'finance':'finance', 'career':'news', 'house':'news',
            'tech':'technology', 'weather':'news', 'auto':'news', 'ent':'news', 'law':'news', 'edu':'education',
            'food':'news', 'emotion':'news', 'agriculture':'news', 'sports':'sports', 'travel':'news',
            'health':'medical', 'mil':'military', 'baby':'news', 'cul':'news', 'science':'technology',
            'inspiration':'news', 'women':'news', 'digital':'news', 'game':'news', 'photography':'news',
            'history':'news', 'pet':'news', 'lottery':'news', 'comic':'news', 'lifestyle':'news',
            'houseliving':'news', 'astro':'news', 'life':'news', 'funny':'news', 'chuguo':'news',
            'religion':'news'}
            storage_Dic={'politics': '时政', 'social': '社会', 'finance': '财经', 'career': '职场', 'house': '房产',
            'tech': '科技', 'weather': '天气', 'auto': '汽车', 'ent': '娱乐', 'law': '法律', 'edu': '教育', 'food': '美食',
            'emotion': '情感', 'agriculture': '农林牧副渔', 'sports': '体育', 'travel': '旅游', 'health': '健康',
            'mil': '军事', 'baby': '育儿', 'cul': '文化', 'science': '科学', 'inspiration': '鸡汤', 'women': '时尚',
            'digital': '数码', 'game': '游戏', 'photography': '摄影', 'history': '历史', 'pet': '宠物', 'lottery': '彩票',
            'comic': '动漫', 'lifestyle': '生活方式', 'houseliving': '家居', 'astro': '占卜', 'life': '生活百科',
            'funny': '搞笑', 'chuguo': '移民', 'religion': '宗教'}
            url=item['url']
            time=item['time']
            website=item['website']
            filename=item['filename']
            content=item['content']
            sort=item['sort']

            if sort in storage_Dic:
                website_sort=storage_Dic[sort]
            else:
                website_sort='其他'

            if sort in statistics_Dic:
                statistics_sort=statistics_Dic[sort]
            else:
                statistics_sort='other'

            sort_dir='../data/'+website+'/'+website_sort+'/'
            if not osp.exists(sort_dir):
                os.makedirs(sort_dir)
            file_dir=osp.join(sort_dir,filename)

            if content =='':
                with open('../webMessage', 'a',encoding="utf-8") as wf:
                    wf.write(time+'\t'+website+'\t'+statistics_sort+'\t'+website_sort+'\t'+str(0)+'\t'+filename+'\t'+ url+'\t'+'\n')
            else:
                with open(file_dir, 'w',encoding="utf-8") as h:
                    h.write(content)

                with open('../webMessage', 'a',encoding="utf-8") as wf:
                    wf.write(time+'\t'+website+'\t'+statistics_sort+'\t'+website_sort+'\t'+str(1)+'\t'+filename+'\t'+ url+'\t'+'\n')


            return item

        elif spider.name == 'xinhuanet':
            print(item)
            statistics_Dic={'时政':'news','国际':'news','财经':'finance','科技':'technology',
                    '文化':'news','理论':'news','网评':'news','法制':'news','人事':'news',
                    '廉政':'news','地方':'news','港澳':'news','台湾':'news','教育':'education','科普':'news'}

            url=item['url']
            time=item['time']
            website=item['website']
            filename=item['filename']
            content=item['content']
            sort=item['sort']

            website_sort=sort

            if sort in statistics_Dic:
                statistics_sort=statistics_Dic[sort]
            else:
                statistics_sort='other'

            sort_dir='../data/'+website+'/'+website_sort+'/'
            if not osp.exists(sort_dir):
                os.makedirs(sort_dir)
            file_dir=osp.join(sort_dir,filename)

            if content =='':
                with open('../webMessage', 'a',encoding="utf-8") as wf:
                    wf.write(time+'\t'+website+'\t'+statistics_sort+'\t'+website_sort+'\t'+str(0)+'\t'+filename+'\t'+ url+'\t'+'\n')
            else:
                with open(file_dir, 'w',encoding="utf-8") as h:
                    h.write(content)

                with open('../webMessage', 'a',encoding="utf-8") as wf:
                    wf.write(time+'\t'+website+'\t'+statistics_sort+'\t'+website_sort+'\t'+str(1)+'\t'+filename+'\t'+ url+'\t'+'\n')

            return item

        elif spider.name == 'ifeng':
            print(item)
            statistics_Dic={'资讯':'news','财经':'finance','股票':'finance','娱乐':'news',
                    '体育':'sports','文化':'news','科技':'technology','佛教':'news','军事':'military',
                    '旅游':'news','健康':'medical','汽车':'news','读书':'news','国学':'news',
                    '教育':'education','历史':'news','政务':'news'}

            url=item['url']
            time=item['time']
            website=item['website']
            filename=item['filename']
            content=item['content']
            sort=item['sort']

            website_sort=sort

            if sort in statistics_Dic:
                statistics_sort=statistics_Dic[sort]
            else:
                statistics_sort='other'

            sort_dir='../data/'+website+'/'+website_sort+'/'
            if not osp.exists(sort_dir):
                os.makedirs(sort_dir)
            file_dir=osp.join(sort_dir,filename)

            if content =='':
                with open('../webMessage', 'a',encoding="utf-8") as wf:
                    wf.write(time+'\t'+website+'\t'+statistics_sort+'\t'+website_sort+'\t'+str(0)+'\t'+filename+'\t'+ url+'\t'+'\n')
            else:
                with open(file_dir, 'w',encoding="utf-8") as h:
                    h.write(content)

                with open('../webMessage', 'a',encoding="utf-8") as wf:
                    wf.write(time+'\t'+website+'\t'+statistics_sort+'\t'+website_sort+'\t'+str(1)+'\t'+filename+'\t'+ url+'\t'+'\n')
            return item


