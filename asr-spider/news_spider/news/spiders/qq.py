import scrapy
from selenium import webdriver
from news.items import NewsItem
import xml.dom.minidom as xmldom
import time
import re
import os
import os.path as osp
import json

class QqSpider(scrapy.Spider):
    name = 'qq'
    # allowed_domains = ['https://news.qq.com/']
    start_urls = []
    links=[]
    # allsort=[]

    # dynamicUrl_people=['http://news.people.com.cn/']   #需要动态加载的网页

    def __init__(self):
        # https://edu.163.com/special/002987KB/newsdata_edu_hot.js?callback=data_callback   教育
        maxPage=1   #每个模块每次最多爬多少页，军事每次最多爬8页            zfw政务往事  'politics',政务
        start_news_category = ['24hours','antip','ent','milite','world','tech','finance','auto','fashion','video','games','emotion','cul','nstock','house','comic','digi','astro','health','visit','baby','pet','history','football','newssh','rushidao','edu','licai','sports','lifes','kepu']     #'world','society','law','health','economy_zixun','edu'
        provinces=['bj','sh','tj','cq','qinghai','ln','guizhou','hainan','gansu','sd','jiangxi','ningxia','hn','hebei','jilin','heilongjiang','fj','neimenggu','xian','shanxi','cd','hb','jiangsu','henan','zj','yn']   #,'anhui'没有数据
        news_url_head = "https://i.news.qq.com/trpc.qqnews_web.kv_srv.kv_srv_http_proxy/list?sub_srv_id="
        news_url_tail = '&srv_id=pc&offset=0&limit=199&strategy=1&ext={"pool":["high","top"],"is_filter":10,"check_type":true}'   #"high","top"
        for category in start_news_category:
            for count in range(1, maxPage+1):  # 每个版块最多爬取前3页数据
                # if count == 1:
                #     category_url = news_url_head + category +'_1' +'.jsonp?cb='+category
                # else:
                #     category_url = news_url_head + category+ "_" +str(count)+'.jsonp?cb=t&cb='+category

                category_url = news_url_head + category+ news_url_tail
                self.start_urls.append(category_url)
        for province in provinces:
                category_url = news_url_head + province+ news_url_tail
                self.start_urls.append(category_url)
        # print(self.start_urls)
        if  osp.exists(r'../webMessage'):
            with open(r'../webMessage', 'r') as rf:
                for line in rf:
                    line = line.strip()
                    if not line:
                        continue
                    link=line.split()[-1]
                    # print(link)
                    self.links.append(link)

    def parse(self, response):
        a={"cms_id":"20210106A07VTW00",
        "title":"石景山区第十六届人民代表大会第七次会议召开第一次全体会议",
        "subtitle":"","url":"https://new.qq.com/omn/20210106/20210106A07VTW00.html",
        "thumb_nail":"http://inews.gtimg.com/newsapp_ls/0/13006527604_150120/0",
        "thumb_nail_2x":"http://inews.gtimg.com/newsapp_ls/0/13006527604_640330/0",
        "top_big_img":["http://inews.gtimg.com/newsapp_ls/0/13006527604_485350/0","http://inews.gtimg.com/newsapp_ls/0/13006527605_485350/0","http://inews.gtimg.com/newsapp_ls/0/13006527607_485350/0"],
        "category_id":"3",
        "category_name":"politics",
        "category_cn":"时政",
        "sub_category_id":"303",
        "sub_category_name":"politics_zhongda",
        "sub_category_cn":"重大民生",
        "status":4,"tags":[{"tag_id":"7628738","tag_word":"石景山区","tag_score":"0.527262"},{"tag_id":"60226872","tag_word":"疫情防控","tag_score":"0.268504"},{"tag_id":"4659814","tag_word":"北京","tag_score":"0.048374"}],
        "media_id":"5448185",
        "media_name":"北京石景山",
        "point":"3",
        "article_type":0,"pool_name":"bj_pool",
        "security_field":1,
        "article_id":"20210106A07VTW",
        "source":"om",
        "comment_id":"6356548379",
        "comment_num":"0",
        "create_time":"2021-01-06 15:21:58",
        "update_time":"2021-01-06 15:21:58",
        "publish_time":"2021-01-06 15:17:33",
        "img_exp_type":"3",
        "img":"http://inews.gtimg.com/newsapp_ls/0/13006527604_640330/0"}
        b=['时政', '社会', '娱乐', '财经', '职场', '房产', '科技', '天气', '汽车', '法律', '教育', '美食', '情感', '农林牧副渔', '体育', '旅游', '健康', '军事', '文化', '科学', '育儿', '鸡汤', '时尚', '数码', '游戏', '彩票', '摄影', '历史', '宠物', '动漫', '生活方式', '家居', '占卜', '', '生活百科', '搞笑', '移民', '宗教']

        c=['politics', 'social', 'finance', 'career', 'house', 'tech', 'weather', 'auto', 'ent', 'law', 'edu', 'food', 'emotion', 'agriculture', 'sports', 'travel', 'health', 'mil', 'baby', 'cul', 'science', 'inspiration', 'women', 'digital', 'game', 'photography', 'history', 'pet', 'lottery', 'comic', 'lifestyle', 'houseliving', 'astro', '', 'life', 'funny', 'chuguo', 'religion']


        # https://news.cctv.com/2019/07/gaiban/cmsdatainterface/page/china_1.jsonp?cb=china
        sort=re.split('[=]',response.url)[-1]
        detail_data = json.loads(response.text,strict=False)
        dic_list=detail_data['data']['list']
        for message in dic_list:
            detail_url=message["url"]
            time=message['create_time'].split()[0]
            sort=message['category_name']
            # if sort not in self.allsort:
            #     self.allsort.append(sort)
            filename=message['cms_id'][8:]
            filename=time.replace('-','')+'-qq-'+filename

            if detail_url not in self.links:
                item=NewsItem()
                item['sort']=sort
                item['time']=time
                item['filename']=filename
                item['url']=detail_url
                yield response.follow(detail_url, self.parse_content,meta={'item':item})


# https://new.qq.com/omn/20210103/20210103A030E300.html
# https://new.qq.com/omn/20210104/20210104A0HAE200.html
    def parse_content(self,response):
        item=response.meta['item']
        content=re.sub('\n+','\n','\n'.join(response.xpath('''//*[@class="content-article"]/p/text()''').extract()))
        item['content'] = content
        item['website'] = 'qq'
        yield item

    def closed(self,spider):
        localtime = time.asctime( time.localtime(time.time()) )
        print("腾讯新闻爬虫结束")
        print(localtime)
        # print(self.allsort)