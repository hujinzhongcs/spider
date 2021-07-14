import os
import os.path as osp
import xlwt
import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

now=datetime.datetime.now()
todayDate=now.strftime('%Y-%m-%d')
today=datetime.datetime.strptime(todayDate,'%Y-%m-%d')

timeRange=7   #t统计最近7天的数据
filename=todayDate+'.xls'


class WebsiteStatistic:
    website_week_total=0
    website_history_total=0
    news=0
    education=0
    finance=0
    military=0
    medical=0
    sports=0
    technology=0
    baike=0
    chat=0
    wenda=0
    literature=0
    other=0

    week_total=0
    news_week=0
    education_week=0
    finance_week=0
    military_week=0
    medical_week=0
    sports_week=0
    technology_week=0
    baike_week=0
    chat_week=0
    wenda_week=0
    literature_week=0
    other_week=0

    history_total=0
    news_total=0
    education_total=0
    finance_total=0
    military_total=0
    medical_total=0
    sports_total=0
    technology_total=0
    baike_total=0
    chat_total=0
    wenda_total=0
    literature_total=0
    other_total=0

    #统计每个网站的历史数据
    def WebsiteStatistic(self,time,sort):
        try:
            newstime=datetime.datetime.strptime(time,'%Y-%m-%d')
        except:
            newstime=datetime.datetime.strptime('1997-05-14','%Y-%m-%d')
        interval = (today - newstime).days
        self.website_history_total+=1
            #统计各模块爬取总数
        if int(interval) <= timeRange:
            self.website_week_total+=1
            #统计各模块爬取总数
            if(sort=='news'):
                self.news=self.news+1
            elif(sort=='sports'):
                self.sports=self.sports+1
            elif(sort=='finance'):
                self.finance=self.finance+1
            elif(sort=='technology'):
                self.technology=self.technology+1
            elif(sort=='military'):
                self.military=self.military+1
            elif(sort=='education'):
                self.education=self.education+1
            elif(sort=='medical'):
                self.medical=self.medical+1
            elif(sort=='baike'):
                self.baike=self.baike+1
            elif(sort=='chat'):
                self.chat=self.chat+1
            elif(sort=='wenda'):
                self.wenda=self.wenda+1
            elif(sort=='literature'):
                self.literature=self.literature+1
            elif(sort=='other'):
                self.literature=self.other+1
            else:
                pass
        else:
            pass

    #统计一个分类的一周的数据
    def SortWeek(self,time,sort):
        try:
            newstime=datetime.datetime.strptime(time,'%Y-%m-%d')
        except:
            newstime=datetime.datetime.strptime('2000-01-01','%Y-%m-%d')
        interval = (today - newstime).days
        # self.all_sort_week_total+=1
        #     #统计各模块爬取总数
        if int(interval) <= timeRange:
            self.week_total+=1
            #统计各分类爬取总数
            if(sort=='news'):
                self.news_week+=1
            elif(sort=='sports'):
                self.sports_week+=1
            elif(sort=='finance'):
                self.finance_week+=1
            elif(sort=='technology'):
                self.technology_week+=1
            elif(sort=='military'):
                self.military_week+=1
            elif(sort=='education'):
                self.education_week+=1
            elif(sort=='medical'):
                self.medical_week+=1
            elif(sort=='baike'):
                self.baike_week+=1
            elif(sort=='chat'):
                self.chat_week+=1
            elif(sort=='wenda'):
                self.wenda_week+=1
            elif(sort=='literature'):
                self.literature_week+=1
            elif(sort=='other'):
                self.other_week+=1
            else:
                pass
        else:
            pass

    #历史分类信息汇总
    def HistorySortStatistic(self,sort):
        self.history_total+=1
        if(sort=='news'):
            self.news_total+=1
        elif(sort=='sports'):
            self.sports_total+=1
        elif(sort=='finance'):
            self.finance_total+=1
        elif(sort=='technology'):
            self.technology_total+=1
        elif(sort=='military'):
            self.military_total+=1
        elif(sort=='education'):
            self.education_total+=1
        elif(sort=='medical'):
            self.medical_total+=1
        elif(sort=='baike'):
            self.baike_total+=1
        elif(sort=='chat'):
            self.chat_total+=1
        elif(sort=='wenda'):
            self.wenda_total+=1
        elif(sort=='literature'):
            self.literature_total+=1
        elif(sort=='other'):
            self.other_total+=1
        else:
            pass




    def Totaldata(self):
        websit_sort_Total=[self.news,self.sports,self.finance,self.technology,self.military,
                        self.education,self.medical,self.baike,self.chat,self.wenda,self.literature,self.other]
        # self.website_history_total=[self.news_total,self.sports_total,self.finance_total,self.technology_total,self.military_total,
        #                 self.education_total,self.medical_total,self.baike_total,self.chat_total,self.wenda_total,self.literature_total,self.other_total]
        return websit_sort_Total,self.website_week_total,self.website_history_total   #,self.website_history_total

    def WeekSortData(self):
        sort_week_total=[self.news_week,self.sports_week,self.finance_week,
        self.technology_week,self.military_week,self.education_week,
        self.medical_week,self.baike_week,self.chat_week,self.wenda_week,
        self.literature_week,self.other_week]
        return sort_week_total,self.week_total

    def HistorySortData(self):
        sort_history_total=[self.news_total,self.sports_total,self.finance_total,
        self.technology_total,self.military_total,self.education_total,
        self.medical_total,self.baike_total,self.chat_total,self.wenda_total,
        self.literature_total,self.other_total]
        return sort_history_total,self.history_total






def Statistic():
    #表格首行,与类中的sortTotal=[]对应
    allSort=['新闻','体育','财经','科技','军事','教育','医疗','百科','社交','问答','文学','其他','网站一周','网站历史总计']

    HistorySort=WebsiteStatistic()

    Sina=WebsiteStatistic()
    Chinanews=WebsiteStatistic()
    Baidu=WebsiteStatistic()
    People=WebsiteStatistic()
    Wangyi=WebsiteStatistic()
    CCTV=WebsiteStatistic()
    QQ=WebsiteStatistic()
    Xinhuanet=WebsiteStatistic()
    Ifeng=WebsiteStatistic()
    BaiduBaike=WebsiteStatistic()
    TianYa=WebsiteStatistic()

    SortWeekTotal=WebsiteStatistic()

    if  osp.exists(r'./webMessage'):
        with open(r'./webMessage', 'r') as rf_news:
            for line in rf_news:
                line = line.strip()
                if not line:
                    continue
                time,website,sort=line.split()[0:3]
                # 统计历史各分类爬取个数
                HistorySort.HistorySortStatistic(sort)

                # 统计一周各分类爬取个数
                SortWeekTotal.SortWeek(time,sort)

                # 统计一周各分类各网站爬取个数
                if website=='sina':
                    Sina.WebsiteStatistic(time,sort)
                if website=='chinanews':
                    Chinanews.WebsiteStatistic(time,sort)
                if website=='baidu':
                    Baidu.WebsiteStatistic(time,sort)
                if website=='people':
                    People.WebsiteStatistic(time,sort)
                if website=='wangyi':
                    Wangyi.WebsiteStatistic(time,sort)
                if website=='cctv':
                    CCTV.WebsiteStatistic(time,sort)
                if website=='qq':
                    QQ.WebsiteStatistic(time,sort)
                if website=='xinhuanet':
                    Xinhuanet.WebsiteStatistic(time,sort)
                if website=='ifeng':
                    Ifeng.WebsiteStatistic(time,sort)
                if website=='tianya':
                    TianYa.WebsiteStatistic(time,sort)

    if  osp.exists(r'./baike_spider/baikeMessage'):
        with open(r'./baike_spider/baikeMessage', 'r') as rf_baike:
            for line in rf_baike:
                line = line.strip()
                if not line:
                    continue
                time,website,sort=line.split()[0:3]
                # 统计一周各分类爬取个数
                SortWeekTotal.SortWeek(time,sort)

                # 统计历史各分类爬取个数
                HistorySort.HistorySortStatistic(sort)


                if website=='baiduBaike':
                    BaiduBaike.WebsiteStatistic(time,sort)

    log_dir='./log/'
    if not osp.exists(log_dir):
        os.makedirs(log_dir)
    file_dir=osp.join(log_dir,filename)


    # 表格首行
    f=xlwt.Workbook()
    sheet=f.add_sheet("爬虫信息统计",cell_overwrite_ok=True)
    for i in range(len(allSort)):
        sheet.write(0,i+1,allSort[i])

    # 表格新浪网的一行
    sheet.write(1,0,'sina')
    websit_sort_Total,website_week_total,website_history_total=Sina.Totaldata()
    for i in range(len(websit_sort_Total)):
        sheet.write(1,i+1,websit_sort_Total[i])
        sheet.write(1,len(websit_sort_Total)+1,website_week_total)
        sheet.write(1,len(websit_sort_Total)+2,website_history_total)

    #表格中国新闻网的一行
    sheet.write(2,0,'Chinanews')
    websit_sort_Total,website_week_total,website_history_total=Chinanews.Totaldata()
    for i in range(len(websit_sort_Total)):
        sheet.write(2,i+1,websit_sort_Total[i])
        sheet.write(2,len(websit_sort_Total)+1,website_week_total)
        sheet.write(2,len(websit_sort_Total)+2,website_history_total)

    #表格百度闻网的一行
    sheet.write(3,0,'baidu')
    websit_sort_Total,website_week_total,website_history_total=Baidu.Totaldata()
    for i in range(len(websit_sort_Total)):
        sheet.write(3,i+1,websit_sort_Total[i])
        sheet.write(3,len(websit_sort_Total)+1,website_week_total)
        sheet.write(3,len(websit_sort_Total)+2,website_history_total)

    #表格人民网的一行
    sheet.write(4,0,'people')
    websit_sort_Total,website_week_total,website_history_total=People.Totaldata()
    for i in range(len(websit_sort_Total)):
        sheet.write(4,i+1,websit_sort_Total[i])
        sheet.write(4,len(websit_sort_Total)+1,website_week_total)
        sheet.write(4,len(websit_sort_Total)+2,website_history_total)


    #表格网易新闻的一行
    sheet.write(5,0,'wangyi')
    websit_sort_Total,website_week_total,website_history_total=Wangyi.Totaldata()
    for i in range(len(websit_sort_Total)):
        sheet.write(5,i+1,websit_sort_Total[i])
        sheet.write(5,len(websit_sort_Total)+1,website_week_total)
        sheet.write(5,len(websit_sort_Total)+2,website_history_total)

    #表格cctv新闻的一行
    sheet.write(6,0,'cctv')
    websit_sort_Total,website_week_total,website_history_total=CCTV.Totaldata()
    for i in range(len(websit_sort_Total)):
        sheet.write(6,i+1,websit_sort_Total[i])
        sheet.write(6,len(websit_sort_Total)+1,website_week_total)
        sheet.write(6,len(websit_sort_Total)+2,website_history_total)

    #表格腾讯新闻的一行
    sheet.write(7,0,'qq')
    websit_sort_Total,website_week_total,website_history_total=QQ.Totaldata()
    for i in range(len(websit_sort_Total)):
        sheet.write(7,i+1,websit_sort_Total[i])
        sheet.write(7,len(websit_sort_Total)+1,website_week_total)
        sheet.write(7,len(websit_sort_Total)+2,website_history_total)

    #表格新华闻的一行
    sheet.write(8,0,'xinhuanet')
    websit_sort_Total,website_week_total,website_history_total=Xinhuanet.Totaldata()
    for i in range(len(websit_sort_Total)):
        sheet.write(8,i+1,websit_sort_Total[i])
        sheet.write(8,len(websit_sort_Total)+1,website_week_total)
        sheet.write(8,len(websit_sort_Total)+2,website_history_total)

    #表格凤凰闻的一行
    sheet.write(9,0,'ifeng')
    websit_sort_Total,website_week_total,website_history_total=Ifeng.Totaldata()
    for i in range(len(websit_sort_Total)):
        sheet.write(9,i+1,websit_sort_Total[i])
        sheet.write(9,len(websit_sort_Total)+1,website_week_total)
        sheet.write(9,len(websit_sort_Total)+2,website_history_total)

    #表格百度百科的一行
    sheet.write(10,0,'baidubaike')
    websit_sort_Total,website_week_total,website_history_total=BaiduBaike.Totaldata()
    for i in range(len(websit_sort_Total)):
        sheet.write(10,i+1,websit_sort_Total[i])
        sheet.write(10,len(websit_sort_Total)+1,website_week_total)
        sheet.write(10,len(websit_sort_Total)+2,website_history_total)

    #表格天涯论坛的一行
    sheet.write(11,0,'tianya')
    websit_sort_Total,website_week_total,website_history_total=TianYa.Totaldata()
    for i in range(len(websit_sort_Total)):
        sheet.write(11,i+1,websit_sort_Total[i])
        sheet.write(11,len(websit_sort_Total)+1,website_week_total)
        sheet.write(11,len(websit_sort_Total)+2,website_history_total)

    #一周各分类爬取个数
    sheet.write(12,0,'一周')
    sort_week_total,week_total=SortWeekTotal.WeekSortData()
    for i in range(len(sort_week_total)):
        sheet.write(12,i+1,sort_week_total[i])
        sheet.write(12,len(sort_week_total)+1,week_total)

    #历史总计各分类爬取个数
    sheet.write(13,0,'历史总计')
    # total_all=0
    sort_history_total,history_total=HistorySort.HistorySortData()
    for i in range(len(sort_history_total)):
        sheet.write(13,i+1,sort_history_total[i])
        # total_all=total_all+sort_history_total[i]
        sheet.write(13,len(sort_history_total)+2,history_total)

    f.save(file_dir)

def Mail():

    info="详情见表格"
    cc_reciver=['zhaoang@soundai.com']   #zhaoang@soundai.com
    sender='hujinzhong@soundai.com'
    passward='Hu123456'
    to_reciver=[sender]  #给自己也发一份
    reciver=to_reciver+cc_reciver
    try:

        msg = MIMEMultipart()
        msg.attach(MIMEText(info, 'plain', 'utf-8'))
        # msg=MIMEText(info,'plain','utf-8')

        # 构造附件1，传送当前目录下的 test.txt 文件
        file_dir=osp.join('./log/',filename)
        att1 = MIMEText(open(file_dir, 'rb').read(), 'base64', 'utf-8')
        att1["Content-Type"] = 'application/octet-stream'
        # 这里的filename可以任意写，写什么名字，邮件中显示什么名字
        att1["Content-Disposition"] = 'attachment; filename="statistic.xls"'
        msg.attach(att1)

        msg['From'] = sender
        msg['To'] = ';'.join(to_reciver)
        msg['Cc'] = ';'.join(cc_reciver)
        msg['Subject']=todayDate+'爬虫信息统计'
        server=smtplib.SMTP('smtp.exmail.qq.com')
        server.connect('smtp.exmail.qq.com',25)
        server.login(sender,passward)
        server.sendmail(sender,reciver,msg.as_string())
        server.quit
        print("成功")
    except Exception as e:
        print ("发送失败",e)



if __name__ == '__main__':
    Statistic()
    Mail()
