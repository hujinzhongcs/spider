import requests
import re
import time
import json
from pymongo import MongoClient

mongo_url = 'mongodb://172.16.10.14:27017/'
database = 'jindong'
asr_text = "comment_time"

def connectdb(url,database,collection):

    client = MongoClient(url)
    db = client[database]
    collection = db[collection]

    return collection

commentdb=connectdb(mongo_url,database,asr_text)
# 'path': '/comment/productPageComments.action?callback=fetchJSON_comment98&productId=100011058759&score=0&sortType=5&page=1&pageSize=10&isShadowSku=0&rid=0&fold=1',
# https://club.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98&productId=100011058759&score=0&sortType=5&page=1&pageSize=10&isShadowSku=0&rid=0&fold=1
# https://club.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98&productId=100011058759&score=0&sortType=5&page=2&pageSize=10&isShadowSku=0&rid=0&fold=1
# https://club.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98&productId=100011058759&score=0&sortType=6&page=0&pageSize=10&isShadowSku=0&fold=1
headers={
'authority': 'club.jd.com',
'method': 'GET',
'scheme': 'https',
'accept': '*/*',
'accept-encoding': 'gzip, deflate, br',
'accept-language': 'zh-CN,zh;q=0.9',
'cookie': '__jdu=16207837823911868860816; shshshfpa=ac6f4f2e-b0b4-7ee6-fb8d-20b031964b02-1622429425; shshshfpb=xNWzv%20s5qgii3%2FeP%2FdbJOJQ%3D%3D; __jdv=122270672|direct|-|none|-|1624614796066; __jda=122270672.16207837823911868860816.1620783782.1622533623.1624614796.4; __jdc=122270672; areaId=1; jwotest_product=99; ipLoc-djd=1-2800-55811-0; shshshfp=fda09430c60b0ef5f3458741d4145625; shshshsID=010ea5effc5fcc00cdd308488ac635df_3_1624615590977; __jdb=122270672.3.16207837823911868860816|4.1624614796; JSESSIONID=9DA017FD59E102EA537F54CC694452F9.s1; 3AB9D23F7A4B3C9B=H73CYLXV7U53SGR5XKXEJ6EY3GX5XAUUIR2QTXF24WG46W26Y4RY763DFXGEWUUVTJJ7OWJU2TLSLZCR7IX6BVGDEQ',
'referer': 'https://item.jd.com/',
'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
'sec-ch-ua-mobile': '?0',
'sec-fetch-dest': 'script',
'sec-fetch-mode': 'no-cors',
'sec-fetch-site': 'same-site',
'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
}
def get_comment():
    with open('./jindongcomment_time.txt', 'a',encoding="utf-8") as wf:
        for i in range(100):
            # print(i)
            url='https://club.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98&productId=100011058759&score=0&sortType=6&page={}&pageSize=10&isShadowSku=0&fold=1'
            # 构建循环用的ur
            url = url.format(i)
            # print(url)
            content = requests.get(url,headers=headers).text#获取相关内容的源代码
            content = json.loads(re.findall(r"\((.*)\)",content)[0],strict=False)
            comments=content['comments']
            for comment in comments:
                content=comment['content']
                creationTime=comment['creationTime']
                wf.write(creationTime+'\n'+content+'\n\n')
                document={ "time": creationTime,"content":content}
                commentdb.insert_one(document)
                print(content+'\n'+creationTime)

            time.sleep(2)#访问间隔


if __name__ == "__main__":
    get_comment()
