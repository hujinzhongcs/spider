import scrapy
from selenium import webdriver
from chat_spider.items import ChatSpiderItem
import xml.dom.minidom as xmldom
import time
import datetime
import re
import os
import os.path as osp
import json

class TianyaSpider(scrapy.Spider):
    name = 'tianya'
    # allowed_domains = ['https://bbs.tianya.cn/']
    start_urls = ['https://bbs.tianya.cn/']
    links=[]
    reply_max=10  #最多取10条评论
    reply_reply_max=5   #评论底下的回复最多取5条
    answer_max=10  #问答的回答最多取10条
    # allsort=[]
    # dynamicUrl_people=['http://news.people.com.cn/']   #需要动态加载的网页
    second_sort_dic={'free': '天涯杂谈', 'university': '我的大学', '828': '百姓声音', 'develop': '经济论坛', 'stocks': '股市论谈',
    '1151': '掘金网络股', '1179': '区块链星球', '1190': '交换空间', '665': '视频专区', 'feeling': '情感天地', 'no11': '时尚资讯',
    'fans': '球迷一家', 'play': '游戏地带', '1177': '天涯银河', '1178': '红袖天涯', 'culture': '舞文弄墨', '16': '莲蓬鬼话',
    'no05': ' 煮酒论史', 'no01': '关天茶舍', 'books': '闲闲书话', 'poem': '天涯诗会', 'no02': '诗词比兴', 'house': '房产观澜',
    '697': '海南自贸港', 'no22': '理财前线', 'no20': '职场天地', 'enterprise': '创业家园', 'cars': '汽车时代', '778': '彩票天地',
    'law': '法治论坛', 'news': '新闻众评', 'worldlook': '国际观察', '333': '台湾风云', '105': '未知学院',
    '96': '饮食男女', '768': '我爱网购', '98': '亲子中心', 'outseachina': '海外华人', '100': '天涯医院', 'spirit': '心灵热线',
    '934': '婆媳关系', 'oldgirl': '三十不嫁', 'water': '灌水专区', 'funinfo': '娱乐八卦', '1095': '生活那点事',
    'tianyamyself': '天涯真我', 'filmtv': '影视评论', '14': '开心乐园', 'no04': '贴图专区', '766': '家居装饰',
    'lookout': '了望天涯', '137': '天 香赌坊', '1171': '天涯竞猜', '174': '天涯志', '810': '天涯共此时', '24': '天涯婚礼堂',
    '409': '天涯玫瑰园', '172': '天涯居委会', '410': '主播天地', '168': '天涯有我', '31': '大话天涯', '411': '天涯交易所',
    '666': '学术中国', '113': '人物研究', '780': '个性90后', '210': '生于八十', '420': '七十年代', '157': '环保先锋',
    'help': '天涯互助', '972': '实话实说', '838': '公益同行', '22': '留学生涯', 'consumer': '消费者报道', '1175': '全景视界',
    '1089': '亚洲论坛', '67': '拈花微笑', '106': '书话红楼', '66': '灯谜天地', '241': '寓言格言', '139': '栀子花开',
    '160': '打油诗社', '187': '文学批评', '486': '先锋阵地', '218': '今古传奇', '364': '左岸花开', '390': '天涯读书',
    '901': '书画商场', '1005': '悦读中国', 'shortmessage': '短文故乡', 'no124': '奇幻文学', '23': '对联雅座', 'no17': '仗剑天涯',
    '169': '金石书画', 'no16': '散文天下', '647': '国学明道', '943': '民间语文', '762': '时尚男装', '150': '珠宝首饰',
    '737': '花田囍事', '911': '美颜靓妆', '738': '营养保健', '912': '快乐备孕', '767': '家有学童', '201': '品酒论情',
    '149': '都市生活', '75': '宠物乐园', '151': '墨色茶坊', '805': '中医养生', '358': '女人公社', '43': '天涯丽人',
    '99': '我爱我家', '166': '爱情诊所', '363': '馨馨相印', '1013': '温暖迹忆', '84': '星座情緣', '607': '都市拍客',
    '1090': '数码摄影', '108': '配音公社', '924': '天涯观光团', '71': 'ＩＱ无 限', '524': '周公解梦', '177': '怡情棋斋',
    '3d': '动漫前线', 'funstribe': '超级秀场', 'tianyaphoto': '天涯摄影', '26': '吉他伊甸园', 'indepfilm': '华语电影',
    '384': '天涯剧社', '200': '音乐共享', '38': '摇滚乐章', '138': '古典音乐', '705': '老歌会', '641': '天涯飙歌台',
    'music': '音乐天地', '967': '风云众创', 'no100': '管理前线', '20': '网上谈兵', '107': '三国纵横', '103': '收藏天地',
    '29': '科幻奥秘', '131': '风土人情', '192': '乡村季风', '743': '家电天下', 'sport': '体育聚焦', 'fansunion': '体育贴图',
    '1154': '约跑马拉松', 'it': '电脑网络', 'numtechnoloy': '数码生活', 'itinfo': 'ＩＴ视界', 'basketball': '篮球公园',
    '1181': '王者聚集地', 'english': '英语杂谈', '1182': '科技论坛', '343': '蓝色老人', '102': '没话找话', '185': '百姓酒馆',
    '952': '八卦春秋', '1185': '品牌阵地', '1021': '众说网购', '923': '天涯购物街', '1164': '现货先锋', '1138': '食在天涯',
    '837': '天天315', '1192': '商业信息', '1173': '深圳牙科医院', '1195': '耳鼻喉医院', '39': '北京', '59': '天津',
    '77': '河北', '80': '河南', '42': '山东', '88': '山西', '97': '内蒙古', '58': '辽宁', '52': '吉林', '82': '黑龙江',
    '41': '上海', '65': '江苏', '61': '浙江', '78': '安徽', '90': '江西', '44': '广东', '79': '广西', '56': '湖南',
    '46': '湖北', '92': '福建', 'hn': '海南', '45': '重庆', '63': '四川', '178': '贵州', '62': '云南', '153': '西藏',
    '183': '甘肃', '60': '陕西', '191': '宁夏', '203': '青海', '173': '新疆', '208': '香港', '331': '澳门时光',
    '1124': '我是海归', '1012': '出国咨询', '1194': '天涯欧洲', '338': '美国', '339': '加拿大', '5032': '巴西', '5153': '新西兰',
    '340': ' 澳大利亚', '5154': '日本', '388': '韩国', '5240': '迪拜', '235': '新加坡', '5230': '马尔代夫', '5038': '马来西亚',
    '5037': '泰国', '5156': '越南', '5030': '菲律宾', '5155': '印度尼西亚', '5036': '印度', '89': '英国', '393': '德国',
    '341': '法国', '5028': '西班牙', '5031': '俄罗斯', '5033': '南非', '170': '工薪一族', '443': '职业女性', '763': '求职招聘',
    '1170': '语文学习', 'saytenya': '众创空间', '415': '经理人', '417': '工程师', '414': '程序员', '444': '设计师',
    '413': '医护人员', '361': '会计', '140': '教师', '217': '人力资源', '142': '编辑记者', '152': '市场营销', '494': '采购人',
    '54': '物流管理', '188': '公务员', '158': '警察天地', '130': '军人', '470': '农庄梦想', '474': '零售业', '447': '服装纺织业',
    '144': '建筑业', '21': '交通业', '448': '通信业', '141': '进出口贸易', '143': '酒店服务业', '362': '金融业', '476': '图书出版',
    '477': '文体娱乐业', 'no06': '传媒江湖', '516': '华为世界', '845': '中兴通讯', '517': '海南航空', '863': '富士康',
    '857': '国美', '858': '苏宁', '859': '沃尔玛', '849': '中国石化油', '860': '中国人寿', '861': '国家电网', '70': '铅笔森林',
    'middleschool': '中学时代', '399': '青涩情怀', '375': '时尚乐院', '401': '校园歌曲', '1108': '北京大学', '1109': ' 清华大学',
    '370': '浙江大学', '1110': '上海交大', '371': '复旦大学', '372': '南京大学', '579': '武汉大学', '5210': '四川大学',
    '730': '中山大学', '732': '中山大学校友', '382': '哈工大', '907': '敢问敢答', '1147': '寻医问药',
    'travel': '旅游休闲', '12': '异国风情', '685': '结伴同游', '1027': '天涯客栈', '1187': '山地旅游', '96': '饮食男女',
    '1020': '旅游315', '687': '浪漫三亚', 'hn': '阳光海南', '926': '粤游天下', '928': '乐游上海', '820': '畅游台湾',
    '990': '美在广西', '874': '辽阔东北', '178': '多彩贵州', '922': '北京攻略', '884': '水韵江苏', '284': '天府之国',
    '45': '巴渝名城', '5111': '乐游天下', '686': '柔软丽江', '833': '走进西藏', '1014': '灵秀湖北', '881': '好客山东',
    '1022': '老家河南', '886': '西子浙江', '909': '内蒙风情', '739': '天山南北', '1032': '飞天甘肃', '750': '行走安徽',
    '817': '锦绣潇湘', '818': '江西神韵', '831': '八闽鼓浪', '832': '炎黄陕西', '689': '桂林山水', '1029': '相逢阳朔',
    '688': '彩云之南', '725': '焕彩香江', '331': '澳门时 光', '903': '走进峨眉', '1092': '斑斓美国', '341': '法国',
    '393': '德国', '388': '韩国', '5154': '日本', '5037': '泰国', '1142': '乐享澳洲', '1141': '非常新加坡',
    '1155': '精品旅行', '798': '旅游12季', '819': '贵州旅游', '1136': '海岛攻略', 'no21': '阳光海南', '1168': '邮轮世界',
    '769': '巴山蜀水', '843': '旅游杂谈', '1186': '城市快讯', '1025': '签证专区', '147': '导游心声', '919': '骑乐无穷',
    '840': '玩转高球', '243': '潜水俱乐部', '872': '蜜月之旅', '680': '信天助学','844': '社区公告','apply': '建议申请',
    'complaint': '用户投诉', '777': '上诉申诉', 'discuss': '议事广场', '408': '社区帮助', '797': '天涯实验场'}

    # sort=['free', 'university', '828', 'develop', 'stocks', '1151', '1179', '1190', '665', 'feeling', 'no11', 'fans',
    # 'play', '1177', '1178', 'culture', '16', 'no05', 'no01', 'books', 'poem', 'no02', 'house', '697', 'no22', 'no20',
    # 'enterprise', 'cars', '778', 'law', 'news', 'worldlook', '333', '105', 'travel', '96', '768', '98', 'outseachina',
    # '100', 'spirit', '934', 'oldgirl', 'water', 'funinfo', '1095', 'tianyamyself', 'filmtv', '14', 'no04', '766',
    # 'lookout', '137', '1171', '174', '810', '24', '409', '172', '410', '168', '31', '411', '666', '113', '780', '210',
    # '420', '157', 'help', '972', '838', '22', 'consumer', '1175', '1089', '67', '106', '66', '241', '139', '160', '187',
    # '486', '218', '364', '390', '901', '1005', 'shortmessage', 'no124', '23', 'no17', '169', 'no16', '647', '943',
    # '762', '150', '737', '911', '738', '912', '767', '201', '149', '75', '151', '805', '358', '43', '99', '166', '363',
    # '1013', '84', '607', '1090', '108', '924', '71', '524', '177', '3d', 'funstribe', 'tianyaphoto', '26', 'indepfilm',
    # '384', '200', '38', '138', '705', '641', 'music', '967', 'no100', '20', '107', '103', '29', '131', '192', '743',
    # 'sport', 'fansunion', '1154', 'it', 'numtechnoloy', 'itinfo', 'basketball', '1181', 'english', '1182', '343', '102',
    # '185', '952', '1185', '1021', '923', '1164', '1138', '837', '1192', '1173', '1195', '39', '59', '77', '80', '42',
    # '88', '97', '58', '52', '82', '41', '65', '61', '78', '90', '44', '79', '56', '46', '92', 'hn', '45', '63', '178',
    # '62', '153', '183', '60', '191', '203', '173', '208', '331', '1124', '1012', '1194', '338', '339', '5032', '5153',
    # '340', '5154', '388', '5240', '235', '5230', '5038', '5037', '5156', '5030', '5155', '5036', '89', '393', '341',
    # '5028', '5031', '5033', '170', '443', '763', '1170', 'saytenya', '415', '417', '414', '444', '413', '361', '140',
    # '217', '142', '152', '494', '54', '188', '158', '130', '470', '474', '447', '144', '21', '448', '141', '143', '362',
    # '476', '477', 'no06', '516', '845', '517', '863', '857', '858', '859', '849', '860', '861', '70', 'middleschool',
    # '399', '375', '401', '1108', '1109', '370', '1110', '371', '372', '579', '5210', '730', '732', '382', '907', '1147',
    # 'travel', '12', '685', '1027', '1187', '96', '1020', '687', 'hn', '926', '928', '820', '990', '874', '178', '922',
    # '884', '284', '45', '5111', '686', '833', '1014', '881', '1022', '886', '909', '739', '1032', '750', '817', '818',
    # '831', '832', '689', '1029', '688', '725', '331', '903', '1092', '341', '393', '388', '5154', '5037', '1142',
    # '1141', '1155', '798', '819', '1136', 'no21', '1168', '769', '843', '1186', '1025', '147', '919', '840', '243',
    # '872', '680', '844', 'apply', 'complaint', '777', 'discuss', '408','797']

    # 天涯主版
    tianYaZuBan=['free',  '828', 'develop', 'stocks', '1151', '1179', 'feeling', 'no11', 'fans', 'play', '1177', '1178',
    'culture', '16','no05', 'no01', 'books', 'poem', 'no02', 'house', '697', 'no22', 'no20', 'enterprise', 'cars',
    '778', 'law', 'news', 'worldlook','96', '768', '98',  '100',  '934', 'oldgirl', 'water', 'funinfo', '1095',
    'tianyamyself', 'filmtv', '14', 'no04', '766', ]
    # 天涯网事
    tianTaWangShi=['lookout', '137', '1171', '174', '810', '24', '409', '172', '410', '168', '31', '411']
    # 民生
    mingsheng=['666', '113', '780', '210', '420', '157', 'help', '972', '838', 'consumer','1175', '1089']
    #文学
    wenXue=['67', '106', '66', '241', '139', '160', '187', '486', '218', '364', '390', '901', '1005', 'shortmessage',
    'no124', '23', 'no17', '169','no16', '647', '943']
    #时尚
    siShang=['762', '150', '737', '911', '738', '912', '767', '201', '149', '75', '151', '805', '358', '43']
    # 情感
    qinGan=['99', '166', '363', '1013',]
    # 娱乐
    yuLe=['84','607', '1090', '108', '924', '71', '524', '177', '3d', 'funstribe', 'tianyaphoto', '26']
    # 影音
    yinYin=['indepfilm','384', '200', '38', '138', '705', '641', 'music']
    # 财经
    caiJin=['967', 'no100']
    # 兴趣
    xinQu=['20', '107', '103', '29', '131', '192', '743', 'sport', 'fansunion', '1154', 'it', 'numtechnoloy', 'itinfo',
    'basketball', '1181','english', '1182']
    # 聚会
    juHui=['343', '102', '185', '952']
    # 消费
    xiaofei=['1190', '1185', '1021', '923', '1164', '1138', '837', '1192']
    # 健康
    jiangKang=['1173', '1195']
    # 区域论坛
    quYuLunTan=['39', '59', '77', '80', '42','88', '97', '58', '52', '82', '41', '65', '61', '78', '90', '44', '79',
    '56', '46', '92', 'hn','45', '63', '178', '62', '153', '183', '60', '191','203', '173', '208', '331','333']
    # 海外论坛
    haiWaiLunTan=['outseachina','22', '1124', '1012']
    # 国际
    Guoji=['1194', '338', '339', '5032', '5153', '340', '5154', '388', '5240', '235', '5230', '5038', '5037', '5156',
    '5030', '5155', '5036', '89', '393', '341', '5028', '5031', '5033']
    # 旅游论坛
    lvYou=['travel', '12', '685', '1027', '1187', '96', '1020', '687', 'hn', '926', '928', '820', '990', '874', '178',
    '922', '884', '284', '45', '5111', '686', '833', '1014', '881', '1022', '886', '909', '739', '1032', '750', '817',
    '818', '831', '832', '689', '1029', '688', '725', '331', '903', '1092', '341', '393', '388', '5154', '5037',
    '1142', '1141', '1155', '798', '819', '1136', 'no21', '1168', '769', '843', '1186', '1025', '147', '919',
    '840', '243', '872', '680']
    # 职业综合170- saytenya
    zhiYeZhongHe=['170', '443', '763', '1170', 'saytenya']
    # 职业415-130
    zhiye=['415', '417', '414', '444', '413', '361', '140', '217', '142', '152', '494', '54','188', '158', '130',]
    # 行业
    hangye=['470','474', '447', '144', '21', '448', '141', '143', '362', '476', '477', 'no06']
    # 企业
    qiye=['516', '845', '517', '863', '857', '858','859', '849', '860', '861']
    # 大学校园
    daXueXiaoYuan=['university','70', 'middleschool', '399', '375', '401', '1108', '1109', '370', '1110', '371', '372', '579', '5210', '730', '732','382']
    # 天涯问答
    tianYaWenDa=['907', 'spirit','1147','105']
    # 社区服务
    sheQuFuWu=['844', 'apply', 'complaint', '777', 'discuss', '408', '797']

    first_sorts_list=[tianYaZuBan,tianTaWangShi,mingsheng,wenXue,siShang,qinGan,yuLe,yinYin,caiJin,xinQu,juHui,xiaofei,
             jiangKang,quYuLunTan,haiWaiLunTan,Guoji,lvYou,zhiYeZhongHe,hangye,qiye,daXueXiaoYuan,tianYaWenDa,sheQuFuWu]

    first_sort_name=['天涯主版','天涯网事','民生','文学','时尚','情感','娱乐','影音','财经','兴趣','聚会','消费','健康',
    '区域论坛','海外论坛','国际','旅游论坛','职业综合','行业','企业','大学校园','天涯问答','社区服务']

    links=[]
    def __init__(self):
        if  osp.exists(r'baikeMessage'):
            with open(r'baikeMessage', 'r') as rf:
                for line in rf:
                    line = line.strip()
                    if not line:
                        continue
                    link=line.split()[-1]
                    self.links.append(link)

    def parse(self, response):
        for first_sort_num in range(len(self.first_sorts_list)):
            first_sort=self.first_sorts_list[first_sort_num]
            for second_sort in first_sort:
                # second_sort_code=first_sort[second_sort_num]
                sort_url='http://bbs.tianya.cn/list.jsp?item=' + second_sort +'&order=1'
                item=ChatSpiderItem()
                item['first_sort']=self.first_sort_name[first_sort_num]
                item['second_sort']=self.second_sort_dic[second_sort]
                yield response.follow(sort_url, self.parse_category,meta={'item':item})



    def parse_category(self, response):
        # http://bbs.tianya.cn/post-stocks-2197416-1.shtml
        # /post-lookout-851259-1.shtml

        detail_url_list=response.xpath('//*[@class="tab-bbs-list tab-bbs-list-2"]/tbody/tr/td[1]/a/@href').extract()
        for detail_url in detail_url_list:
            if detail_url not in self.links:
                item=response.meta['item']
                yield response.follow(detail_url, self.parse_content,meta={'item':item})
        #等老帖子爬完可以把此处注释掉,然后开启每日定时爬虫,只爬最新的帖子
        next_page_url=response.xpath('//*[@class="short-pages-2 clearfix"]/div/a[@rel="nofollow"]/@href').extract_first()
        if next_page_url !='':
            item=response.meta['item']
            yield response.follow(next_page_url, self.parse_category,meta={'item':item})



    def parse_content(self,response):
        url=response.url
        category=response.xpath('//*[@class="crumbs"]/a[last()]/text()').extract_first()
        if category=='[我要发帖]':
            # 获取楼主的用户id
            louzu_id=response.xpath('//*[@class="atl-item host-item"]/@_hostid').extract_first()
            #获取楼主的第一个帖子的内容
            content=re.sub('\n+','\n','\n'.join(response.xpath('''//*[@class="atl-item host-item"]//*[@class="bbs-content clearfix"]//text()''').extract()))

            #获取所有评论及楼主的更新帖子
            div_list=response.xpath('//*[@class="atl-item"]')
            reply_count=0
            for div in div_list:
                # 获取评论用户的id,以id区分楼主和评论者
                hostid=div.xpath('./@_hostid').extract_first()
                #如果为楼主的评论，取全部评论及对评论回复的前5条
                if louzu_id==hostid:
                    #获取评论内容
                    content=content+re.sub('\n+','\n','\n'.join(div.xpath('''.//*[@class="bbs-content"]//text()''').extract()))
                    #获取对评论的回复的前五条
                    reply_reply_list=div.xpath('''.//*[@class="ir-content"]''')
                    reply_reply_count=0
                    for reply_reply in reply_reply_list:
                        if reply_reply_count<=self.reply_reply_max:
                            content=content+re.sub('\n+','\n','\n'.join(reply_reply.xpath('./text()').extract()))
                            reply_reply_count=reply_reply_count+1

                else:
                    #获取除楼主外的用户的前10条评论
                    if reply_count<=self.reply_max:
                        content=content+re.sub('\n+','\n','\n'.join(div.xpath('''.//*[@class="bbs-content"]//text()''').extract()))
                        reply_reply_list=div.xpath('''.//*[@class="ir-content"]''')
                        #获取对评论的回复的前五条
                        reply_reply_count=0
                        for reply_reply in reply_reply_list:
                            if reply_reply_count<=self.reply_reply_max:
                                content=content+re.sub('\n+','\n','\n'.join(reply_reply.xpath('./text').extract()))
                                reply_reply_count=reply_reply_count+1
                        reply_count=reply_count+1

            time=re.split('[： ]',response.xpath('//*[@id="post_head"]/div[2]/div[2]/span[2]/text()').extract_first())[1]
            filename=response.url.split('-')[2]
            filename=time.replace('-','')+'-tianya-'+filename
            item=response.meta['item']
            item['content'] = content
            item['website'] = 'tianya'
            item['time']=time
            item['filename']=filename
            item['url']=url
            item['third_sort']='论坛'
            yield item




        # <a rel="nofollow" href="compose.jsp?item=free&amp;module=1">[我要提问]</a>
        elif category=='[我要提问]':
            # 问答标题
            title=response.xpath('//*[@class="q-title"]/h1/span/text()').extract_first()
            #问答内容
            text=re.sub('\n+','\n','\n'.join(response.xpath('//*[@class="text"]/text()').extract()))
            #问答的回复取前self.answer_max条
            answer_list=response.xpath('//*[@class="content"]')
            answer_all=''
            if len(answer_list)<=self.answer_max:
                for answer in answer_list:
                    answer=re.sub('\n+','\n','\n'.join(answer.xpath('./text()').extract()))
                    answer_all=answer_all+'\n'+answer
            else:
                for answer in answer_list[0:self.answer_max]:
                    answer=re.sub('\n+','\n','\n'.join(answer.xpath('./text()').extract()))
                    answer_all=answer_all+'\n'+answer
            answer=re.sub('\n+','\n',answer_all)

            content=title+'\n'+text+'\n'+answer
            time=re.split('[： ]',response.xpath('//*[@class="ml5"]/text()[2]').extract_first())[1]
            filename=response.url.split('-')[2]
            filename=time.replace('-','')+'-tianya-'+filename
            item=response.meta['item']
            item['content'] = content
            item['website'] = 'tianya'
            item['time']=time
            item['filename']=filename
            item['url']=url
            item['third_sort']='问答'
            yield item

        else:
            pass

    def closed(self,spider):
        now=datetime.datetime.now()
        nowtime=now.strftime('%Y-%m-%d %H:%M:%S')
        print("天涯论坛爬虫结束")
        print(nowtime)