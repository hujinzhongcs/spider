# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import os
import os.path as osp

class ChatSpiderPipeline:
    sort=['news','sports','finance','technology','military','education','medical','baike','chat','wenda','literature']
    def process_item(self, item, spider):
        # if isinstance(item,NewsItem)
        if spider.name == 'tianya':
            print(item)
            sortDic={'天涯杂谈': 'chat', '我的大学': 'chat', '百姓声音': 'chat', '经济论坛': 'finance', '股市论谈': 'chat',
             '掘金网络股': 'finance', '区块链星球': 'chat', '交换空间': 'chat', '视频专区': 'chat', '情感天地': 'chat',
             '时尚资讯': 'chat', '球迷一家': 'chat', '游戏地带': 'chat', '天涯银河': 'chat', '红袖天涯': 'chat',
             '舞文弄墨': 'chat', '莲蓬鬼话': 'chat', ' 煮酒论史': 'chat', '关天茶舍': 'chat', '闲闲书话': 'chat',
             '天涯诗会': 'chat', '诗词比兴': 'chat', '房产观澜': 'chat', '海南自贸港': 'chat', '理财前线': 'chat',
             '职场天地': 'chat', '创业家园': 'chat', '汽车时代': 'chat', '彩票天地': 'chat', ' 法治论坛': 'chat',
             '新闻众评': 'chat', '国际观察': 'chat', '台湾风云': 'chat', '未知学院': 'chat', '饮食男女': 'chat',
             '我爱网购': 'chat', '亲子中心': 'chat', '海外华人': 'chat', ' 天涯医院': 'chat', '心灵热线': 'chat',
             '婆媳关系': 'chat', '三十不嫁': 'chat', '灌水专区': 'chat', '娱乐八卦': 'chat', '生活那点事': 'chat',
             '天涯真我': 'chat', '影视评论': 'chat', '开心乐园': 'chat', '贴图专区': 'chat', '家居装饰': 'chat',
             '了望天涯': 'chat', '天香赌坊': 'chat', '天涯竞猜': 'chat', '天涯志': 'chat', '天涯共此时': 'chat',
             '天涯婚礼堂': 'chat', '天涯玫瑰园': 'chat', '天涯居委会': 'chat', '主播天地': 'chat', '天涯有我': 'chat',
             '大话天涯': 'chat', '天涯交易所': 'chat', '学术中国': 'chat', '人物研究': 'chat', '个性90后': 'chat',
             '生于八十': 'chat', '七十年代': 'chat', '环保先锋': 'chat', '天涯互助': 'chat', '实话实说': 'chat',
             '公益同行': 'chat', '留学生涯': 'chat', '消费者报道': 'chat', '全景视界': 'chat', '亚洲论坛': 'chat',
             '拈花微笑': 'literature', '书话红楼': 'literature', '灯谜天地': 'literature', '寓言格言': 'literature',
             '栀子花开': 'literature','打油诗社': 'literature', '文学批评': 'literature', '先锋阵地': 'literature',
             '今古传奇': 'literature', '左岸花开': 'literature','天涯读书': 'literature', '书画商场': 'literature',
             '悦读中国': 'literature', '短文故乡': 'literature', '奇幻文学': 'literature','对联雅座': 'literature',
             '仗剑天涯': 'literaturet', '金石书画': 'literature', '散文天下': 'literature', '国学明道': 'literature',
             '民间语文': 'literature', '时尚男装': 'chat', '珠宝首饰': 'chat', '花田囍事': 'chat', '美颜靓妆': 'chat',
             '营养保健': 'chat', '快乐备孕': 'chat', '家有学童': 'chat', '品酒论情': 'chat', '都市生活': 'chat',
             '宠物乐园': 'chat', '墨色茶坊': 'chat', '中医养生': 'chat', '女人公社': 'chat', '天涯丽人': 'chat',
             '我爱我家': 'chat', '爱情诊所': 'chat', '馨馨相印': 'chat', '温暖迹忆': 'chat', '星座情緣': 'chat',
             '都市拍客': 'chat', '数码摄影': 'chat', '配音公社': 'chat', '天涯观光团': 'chat', 'ＩＱ无 限': 'chat',
             '周公解梦': 'chat', '怡情棋斋': 'chat', '动漫前线': 'chat', '超级秀场': 'chat', '天涯摄影': 'chat',
             '吉他伊甸园': 'chat', '华语 电影': 'chat', '天涯剧社': 'chat', '音乐共享': 'chat', '摇滚乐章': 'chat',
             '古典音乐': 'chat', '老歌会': 'chat', '天涯飙歌台': 'chat', '音乐天地': 'chat', '风云众创': 'chat',
             '管理前线': 'chat', '网上谈兵': 'chat', '三国纵横': 'chat', '收藏天地': 'chat', '科幻奥秘': 'chat',
             '风土人情': 'chat', '乡村季风': 'chat', '家电天下': 'chat', '体育聚焦': 'chat', '体育贴图': 'chat',
             '约跑马拉松': 'chat', '电脑网络': 'chat', '数码生活': 'chat', 'ＩＴ视界': 'chat', '篮球公园': 'chat',
             '王者聚集地': 'chat', '英语杂谈': 'chat', '科技论坛': 'technology', '蓝色老人': 'chat', '没话找话': 'chat',
             '百姓酒馆': 'chat', '八卦春秋': 'chat', '品牌阵地': 'chat', '众说网购': 'chat', '天涯购物街': 'chat',
             '现货先锋': 'chat', '食在天涯': 'chat', '天天315': 'chat', '商业信息': 'chat', '深圳牙科医院': 'chat',
             '耳鼻喉医院': 'chat', '北京': 'chat', '天津': 'chat', '河北': 'chat', '河南': 'chat', '山东': 'chat',
             '山西': 'chat', '内蒙古': 'chat', '辽宁': 'chat', '吉林': 'chat', '黑龙江': 'chat', '上海': 'chat',
             '江苏': 'chat', '浙江': 'chat', '安徽': 'chat', '江西': 'chat', '广东': 'chat', '广西': 'chat',
             '湖南': 'chat', '湖北': 'chat', '福建': 'chat', '阳光海南': 'chat', '巴渝名城': 'chat', '四川': 'chat',
             '多彩贵州': 'chat', '云南': 'chat', '西藏': 'chat', '甘肃': 'chat', '陕西': 'chat', '宁夏': 'chat',
             '青海': 'chat', '新疆': 'chat', '香港': 'chat', '澳门时 光': 'chat', '我是海归': 'chat', '出国咨询': 'chat',
             '天涯欧洲': 'chat', '美国': 'chat', '加拿大': 'chat', '巴西': 'chat', '新西 兰': 'chat', ' 澳大利亚': 'chat',
             '日本': 'chat', '韩国': 'chat', '迪拜': 'chat', '新加坡': 'chat', '马尔代夫': 'chat', '马来西亚': 'chat',
             '泰国': 'chat', '越南': 'chat', '菲律宾': 'chat', '印度尼西亚': 'chat', '印 度': 'chat', '英国': 'chat',
             '德国': 'chat', '法国': 'chat', '西班牙': 'chat', '俄罗斯': 'chat', '南非': 'chat', '工薪一族': 'chat',
             '职业女性': 'chat', '求职招聘': 'chat', '语文学习': 'chat', '众创空间': 'chat', '经理人': 'chat',
             '工程师': 'chat', '程序员': 'chat', '设计师': 'chat', '医护人员': 'chat', '会计': 'chat', '教师': 'chat',
             '人力资源': 'chat', '编 辑记者': 'chat', '市场营销': 'chat', '采购人': 'chat', '物流管理': 'chat',
             '公务员': 'chat', '警察天地': 'chat', '军人': 'chat', '农庄梦想': 'chat', '零售业': 'chat',
             '服装纺织业': 'chat', '建筑业': 'chat', '交通业': 'chat', '通信业': 'chat', '进出口贸易': 'chat',
             '酒店服务业': 'chat', '金融业': 'chat', '图书出版': 'chat', '文体娱乐业': 'chat', '传媒江湖': 'chat',
             '华为世界': 'chat', '中兴通讯': 'chat', '海南航空': 'chat', '富士康': 'chat', '国美': 'chat',
             '苏宁': 'chat', '沃尔玛': 'chat', '中国石化油': 'chat', '中国人寿': 'chat', '国家电网': 'chat',
             '铅笔森林': 'chat', '中学时代': 'chat', '青涩情怀': 'chat', '时尚乐院': 'chat', '校园歌曲': 'chat',
             '北京大学': 'chat', '  清华大学': 'chat', '浙江大学': 'chat', '上海交大': 'chat', '复旦大学': 'chat',
             '南京大学': 'chat', '武汉大学': 'chat', '四川大学': 'chat', '中山大学': 'chat', '中山大学校友': 'chat',
             '哈工大': 'chat', '敢问敢答': 'wenda', '寻医问药': 'chat', '旅游休闲': 'chat', '异国风情': 'chat',
             '结伴同游': 'chat', '天涯客栈': 'chat', '山地旅游': 'chat', '旅游315': 'chat', '浪漫三亚': 'chat',
             '粤游天下': 'chat', '乐游上海': 'chat', '畅游台湾': 'chat', '美在广西': 'chat', '辽阔东北': 'chat',
             '北京攻略': 'chat', '水韵江苏': 'chat', '天府之国': 'chat', '乐游天下': 'chat', '柔软丽江': 'chat',
             '走进西藏': 'chat', '灵秀湖北': 'chat', '好客山东': 'chat', '老家河南': 'chat', '西子浙江': 'chat',
             '内蒙风情': 'chat', '天山南北': 'chat', '飞天甘肃': 'chat', '行走安徽': 'chat', '锦绣潇湘': 'chat',
             '江西神韵': 'chat', '八闽鼓浪': 'chat', '炎黄陕西': 'chat', '桂林山水': 'chat', '相逢阳朔': 'chat',
             '彩云之南': 'chat', '焕彩香江': 'chat', '走进峨眉': 'chat', '斑斓美国': 'chat', '乐享澳洲': 'chat',
             '非常新加坡': 'chat', '精品旅行': 'chat', '旅游12季': 'chat', '贵州旅游': 'chat', '海岛攻略': 'chat',
             '邮轮世界': 'chat', '巴山蜀水': 'chat', '旅游杂谈': 'chat', '城市快讯': 'chat', '签证专区': 'chat',
             '导游心声': 'chat', '骑乐无穷': 'chat', '玩转高球': 'chat', '潜水俱乐部': 'chat', '蜜月之旅': 'chat',
             '信天助学': 'chat', '社区公告': 'chat', '建议申请': 'chat', '用户投诉': 'chat', '上诉申诉': 'chat',
             '议事广场': 'chat', '社区帮助': 'chat', '天涯实验场': 'chat'}

            url=item['url']
            time=item['time']
            website=item['website']
            filename=item['filename']
            content=item['content']
            first_sort=item['first_sort']
            second_sort=item['second_sort']
            third_sort=item['third_sort']

            if second_sort in sortDic:
                statistics_sort=sortDic[second_sort]
            else:
                statistics_sort='other'

            if(second_sort and third_sort):
                sort_dir='../data/'+website+'/'+first_sort+'/'+second_sort+'/'+third_sort+'/'

            if not osp.exists(sort_dir):
                os.makedirs(sort_dir)
            file_dir=osp.join(sort_dir,filename)

            if content =='':
                with open('../webMessage', 'a',encoding="utf-8") as wf:
                    wf.write(time+'\t'+website+'\t'+statistics_sort+'\t'+second_sort+'\t'+str(0)+'\t'+filename+'\t'+ url+'\t'+'\n')
            else:
                with open(file_dir, 'w',encoding="utf-8") as h:
                    h.write(content)

                with open('../webMessage', 'a',encoding="utf-8") as wf:
                    wf.write(time+'\t'+website+'\t'+statistics_sort+'\t'+second_sort+'\t'+str(1)+'\t'+filename+'\t'+ url+'\t'+'\n')

            return item

        #百度知道日报暂时爬不了
        if spider.name == 'baiduZhidaoDaily':
            print(item)
            # sortDic={}
            # url=item['url']
            # time=item['time']
            # website=item['website']
            # filename=item['filename']
            # content=item['content']
            # first_sort=item['first_sort']

            # statistics_sort='wenda'
            # website_sort=first_sort

            # sort_dir='../data/'+website+'/'
            # if not osp.exists(sort_dir):
            #     os.makedirs(sort_dir)
            # file_dir=osp.join(sort_dir,filename)

            # # 2021-01-18	qq	news	1	20210118-qq-A0F7Q500	https://new.qq.com/omn/20210118/20210118A0F7Q500.html
            # if content =='':
            #     with open('../webMessage', 'a',encoding="utf-8") as wf:
            #         wf.write(time+'\t'+website+'\t'+statistics_sort+'\t'+website_sort+'\t'+str(0)+'\t'+filename+'\t'+ url+'\t'+'\n')
            # else:
            #     with open(file_dir, 'w',encoding="utf-8") as h:
            #         h.write(content)


            #     with open('../webMessage', 'a',encoding="utf-8") as wf:
            #         wf.write(time+'\t'+website+'\t'+statistics_sort+'\t'+website_sort+'\t'+str(1)+'\t'+filename+'\t'+ url+'\t'+'\n')

            # return item