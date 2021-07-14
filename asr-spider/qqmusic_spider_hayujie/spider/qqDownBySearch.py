import requests, time
import math
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from bs4 import BeautifulSoup
import requests
import json
import os

from selenium.webdriver.chrome.options import Options

from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

# 创建请求头和会话
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
}
session = requests.session()


# 下载歌曲
def download(guid, songmid, cookie_dict, music_path):
    # 参数guid来自cookies的pgv_pvid
    url = 'https://u.y.qq.com/cgi-bin/musicu.fcg?-=getplaysongvkey11136773093082608&g_tk=5381&loginUin=0&hostUin=0&format=json&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq.json&needNewCode=0&data={"req":{"module":"CDN.SrfCdnDispatchServer","method":"GetCdnDispatch","param":{"guid":"' + guid + '","calltype":0,"userip":""}},"req_0":{"module":"vkey.GetVkeyServer","method":"CgiGetVkey","param":{"guid":"' + guid + '","songmid":["' + songmid + '"],"songtype":[0],"uin":"0","loginflag":1,"platform":"20"}},"comm":{"uin":0,"format":"json","ct":24,"cv":0}}'
    print(url)
    r = session.get(url, headers=headers, cookies=cookie_dict)
    purl = r.json()['req_0']['data']['midurlinfo'][0]['purl']
    # 下载歌曲
    if purl:
        url = 'http://isure.stream.qqmusic.qq.com/%s' % (purl)
        r = requests.get(url, headers=headers)
        f = open(music_path, 'wb')
        f.write(r.content)
        f.close()
        return True
    else:
        return False


def getCookies():
    # 某个歌手的歌曲信息，用于获取Cookies，因为不是全部请求地址都有Cookies
    url = 'https://c.y.qq.com/soso/fcgi-bin/client_search_cp?ct=24&qqmusic_ver=1298&new_json=1&remoteplace=txt.yqq.top&searchid=20194704345758042&t=0&aggr=1&cr=1&catZhida=1&lossless=0&flag_qc=0&p=1&n=20&w=%E5%86%AF%E6%8F%90%E8%8E%AB&g_tk=5381&loginUin=0&hostUin=0&format=json&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq.json&needNewCode=0'
    chrome_options = Options()
    # 设置浏览器参数
    # --headless是不显示浏览器启动以及执行过程
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(executable_path="F:/chromdriver/chromedriver.exe", chrome_options=chrome_options)
    # 访问两个URL，QQ网站才能生成Cookies
    driver.get('https://y.qq.com/')
    time.sleep(5)
    driver.get(url)
    time.sleep(5)
    one_cookie = driver.get_cookies()
    driver.quit()
    # Cookies格式化
    cookie_dict = {}
    for i in one_cookie:
        cookie_dict[i['name']] = i['value']
    print(cookie_dict['pgv_pvid'])
    return cookie_dict

def normallize(name):
    return name.strip().lower().replace(" ", "").replace("·", "").replace(" ", "")

def getInfoByQQSearch():
    driver = webdriver.Chrome(executable_path="F:/chromdriver/chromedriver.exe")
    url = "https://y.qq.com/portal/search.html#page=1&searchid=1&remoteplace=txt.yqq.top&t=song&w="
    with open("F:/titles", 'r', encoding='utf8') as rf:
        for line in rf:
            line = line.strip().lower()
            posturl = url + line
            #posturl = "https://y.qq.com/portal/search.html#page=1&searchid=1&remoteplace=txt.yqq.top&t=song&w=人生总是会遇见各式各样的问题"
            print(posturl)
            driver.get(posturl)
            time.sleep(1)
            #element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "songlist__list")))
            soup = BeautifulSoup(driver.page_source, 'lxml')
            songlist = soup.find_all(class_="songlist__list")[0]
            songlist = songlist.find_all('li')
            for song in songlist:
                #print("------" + str(song.find(class_="songlist__songname_txt").a.span))
                if(song.find(class_="songlist__songname_txt").a.span == None):
                    continue
                songname = song.find(class_="songlist__songname_txt").a.span.get_text()
                #print(songname)
                if(normallize(str(songname)) != normallize(line)):
                    continue
                else:
                    song_url = song.find(class_="songlist__songname_txt").a.attrs['href']
                    mid = song_url.split('.')[-2].split('/')[-1]
                    artist_name = song.find(class_="songlist__artist").attrs['title']
                    album_name = song.find(class_="songlist__album").a.attrs['title']
                    song_time = song.find(class_="songlist__time").get_text()

                    wline = "----" + line + "," + songname + "," + mid + "," + artist_name + "," + album_name + "," + song_time + "," + song_url
                    print(wline)
                    break
def getOtherInfo():
    driver = webdriver.Chrome(executable_path="F:/chromdriver/chromedriver.exe")
    with open("F:/titil_infos.txt", 'r', encoding='utf8') as rf:
        for line in rf:
            line = line.strip()
            items = line.split(",")
            key = items[0]
            url = items[-1]
            print(url)
            driver.get(url)
            time.sleep(1)
            soup = BeautifulSoup(driver.page_source, 'lxml')

            non_str = soup.find(class_="none_txt__symbol")
            if non_str != None:
                continue

            infos = soup.find(class_="data__info").find_all("li")

            genre = ""
            lan = ""
            pubtime = ""
            for info in infos:
                tmp_str = info.get_text()
                if "语种" in tmp_str:
                    lan = info.get_text().split('：')[1]
                elif "流派" in tmp_str:
                    genre = info.get_text().split('：')[1]
                elif "时间" in tmp_str:
                    pubtime = info.get_text().split('：')[1]

            lyric = soup.find(class_="lyric__cont_box").get_text()

            image_src = soup.find(class_="data__cover").img.attrs['src']

            wline = line + "," + genre + "," + lan + "," + pubtime + "," + image_src + "------"

            file_name = "F:/data/" + key + "lyric.txt"
            with open(file_name, 'w', encoding='utf8') as wf:
                wf.write(lyric)

            print(wline)

def down():
    with open("F:/titil_infos.txt", 'r', encoding='utf8') as rf:
        for line in rf:
            line = line.strip()
            items = line.split(",")

            key = items[0]
            mid = items[2]
            img_src = items[-1]
            img_src = "http:" + img_src

            r = requests.get(img_src, stream=True)
            img_path = "F:/data/" + key + "_img.png"
            music_path = "F:/data/" + key + ".m4a"

            with open(img_path, 'wb') as wf:
                wf.write(r.content)

            cookie_dict = getCookies()
            download(cookie_dict['pgv_pvid'], mid, cookie_dict, music_path)

def makeExcel():

    result = {}
    with open("F:/titil_infos.txt", 'r', encoding='utf8') as rf:
        for line in rf:
            line = line.strip()
            items = line.split(",")
            #print(len(items))
            if len(items) != 11:
                continue
            #print(items)

            key = items[0]
            genre = items[7]
            lan = items[8]
            artist = items[3]
            pubtime = items[9]
            long = items[5]
            album = items[4]
            lyric = ""
            img = ""
            music = ""

            lyric_path = "F:/data/" + key + "lyric.txt"
            if os.path.exists(lyric_path):
                lyric = key + "lyric.txt"
            img_path = "F:/data/" + key + "_img.png"
            if os.path.exists(img_path):
                img = key + "_img.png"
            music_path = "F:/data/" + key + ".m4a"
            if os.path.exists(music_path):
                music = key + ".m4a"

            result[key] = [key, genre, '', '', lan, artist, pubtime, '', '', long, album, lyric, img, music]

    print(result)

    with open("F:/titles", 'r', encoding='utf8') as rf:
        for line in rf:
            line = line.strip()
            if line in result:
                wline = ",".join(result[line])
            else:
                wline = ",".join(['', '', '', '', '', '', '', '', '', '', '', '', '', ''])
            print("-----" + wline)



# 源码更新后可以与书本的源码对比分析，更新后的爬虫代码只修改了部分代码
# 变动最大是歌曲下载的代码，同时注意函数之间调用的参数都比之前的源码有所变化。
if __name__ == '__main__':
    # getInfoByQQSearch()
    # getOtherInfo()
    down()
    #makeExcel()
    # cookie_dict = getCookies()
    # download(cookie_dict['pgv_pvid'], "0039MnYb0qxYhV", cookie_dict, "F:/music/mojito.mp3")

    # songmid = '004Mkw5K1oI9K9'
    # cookie_dict = getCookies()
    # download(cookie_dict['pgv_pvid'], songmid, cookie_dict)