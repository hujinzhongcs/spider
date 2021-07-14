# *-* coding:utf8 *-*
import sys
import os
import os.path
import time

import requests

from selenium import webdriver
from concurrent.futures import ThreadPoolExecutor
import lxml
from bs4 import BeautifulSoup
import json

# open('F:/music_spider/musics/004ZmNJ42o5I74/0035gCdF1lpsAc', 'r', encoding='utf8')
# exit()

requests.adapters.DEFAULT_RETRIES = 50

#歌手列表
#file_singer_list='F:/music_spider/singer_list'
file_singer_list='F:/music_spider/singer_list_child'
#歌手info，包含热度，单曲列表连接和专辑列表连接
#file_singer_info='F:/music_spider/singer_info'
file_singer_info='F:/music_spider/singer_info_child'
#歌手最终表，记录歌名处理后的歌手信息。
file_artist_table = 'F:/music_spider/artist_table'
#歌曲信息表，待热度
#file_title_nums = 'F:/music_spider/title_nums'
file_title_nums = 'F:/music_spider/title_nums_child'
#音乐title数据文件夹
#dir_music = 'F:/music_spider/musics/'
dir_music = 'F:/music_spider/child_musics/'

def get_artist_list():
    artist_dict = {}
    with open(file_singer_list, 'r', encoding='utf8') as rf:
        for line in rf:
            line = line.strip()
            items = line.split('')
            if len(items) != 2:
                continue
            artist_dict[items[0]] = line


    wf = open(file_singer_list, 'a', encoding='utf8')
    index_list = list(range(1, 28))
    driver = webdriver.Chrome()
    for index in index_list:
        url = "https://y.qq.com/portal/singer_list.html#page=1&index=" + str(index) + "&"
        driver.get(url)
        page_list = []
        while len(page_list) == 0:
            time.sleep(1)
            soup = BeautifulSoup(driver.page_source, 'lxml')
            page_list = soup.find_all(class_="js_pageindex")
            max_index = 0
            for page in page_list:
                data_index = page.attrs['data-index']
                if int(data_index) > max_index:
                    max_index = int(data_index)

        for i in range(1, max_index+1):
            url = "https://y.qq.com/portal/singer_list.html#page=" + str(i) + "&index=" + str(index) + "&"
            print("get url:" + url)
            driver.get(url)
            singer_list = []
            while len(singer_list) == 0:
                time.sleep(1)
                soup = BeautifulSoup(driver.page_source, 'lxml')
                singer_list = soup.find_all(class_='singer_list_txt__item')
            for singer in singer_list:
                a = singer.a
                href = a.attrs['href']
                title = a.attrs['title']
                wf.write(title + "|||" + href + "\n")
                wf.flush()
            print("get url success")
    driver.close()

def get_artist_info():
    artist_set = set()
    if os.path.exists(file_singer_info):
        with open(file_singer_info, 'r', encoding='utf8') as rf:
            for line in rf:
                items = line.strip().split('|||')
                if len(items) != 4: continue
                if items[1] == '0' or items[2] == '' or items[3] == '': continue
                artist_set.add(items[0])

    driver = webdriver.Chrome(executable_path="F:/chromdriver/chromedriver.exe")
    wf = open(file_singer_info, 'a', encoding='utf8')
    with open(file_singer_list, 'r', encoding='utf8') as rf:
        for line in rf:
            items = line.strip().split('|||')
            name, href = items
            if(name in artist_set):
                print(name)
                continue

            driver.get(href)

            time.sleep(1)
            soup = BeautifulSoup(driver.page_source, 'lxml')

            #获取关注度
            hot = 0
            for i in range(3):
                btn = soup.find_all(class_="mod_btn js_follow")
                if len(btn) < 1:
                    continue
                tmp = btn[0].get_text().strip()
                tmp = tmp.split(' ')
                if len(tmp) == 2:
                    hot = tmp[1]
                    break
                time.sleep(1)
                soup = BeautifulSoup(driver.page_source, 'lxml')

            #获取单曲,专辑连接
            title_href = ""
            album_href = ""
            data = soup.find_all(class_="mod_data_statistic")
            if len(data) < 1:
                wf.write(name + '|||' + str(hot) + '|||' + title_href + '|||' + album_href + '\n')
                wf.flush()
                continue
            data = soup.find_all(class_="mod_data_statistic")[0].find_all(class_="data_statistic__item")
            for li in data:
                data_tab = li.a.attrs['data-tab']
                if data_tab == 'song':
                    title_href = 'https:' + li.a.attrs['href']
                elif data_tab == 'album':
                    album_href = 'https:' + li.a.attrs['href']

            wf.write(name + '|||' + str(hot) + '|||' + title_href + '|||' + album_href + '\n')
            wf.flush()
            print("get singer name:" + name + " success!")
    driver.close()

def get_title_info():
    get_info_by_artist()


def get_info_by_artist():
    artist_dict = {}
    with open('F:/music_spider/totle_nums', 'r', encoding='utf8') as rf:
        for line in rf:
            line = line.strip().split('|||')
            if len(line) != 3: continue
            mid = line[1]
            totalNum = line[2]
            artist_dict[mid] = int(totalNum)
        ttn = open('F:/music_spider/totle_nums', 'a', encoding='utf8')



    param = {"order": 1, "singerMid": "002J4UUk29y8BY", "begin": 0, "num": 100}
    url = "https://u.y.qq.com/cgi-bin/musicu.fcg?"
    data = {"comm":{"ct":24,"cv":0},"singerSongList":{"method":"GetSingerSongList",
            "param":param,"module":"musichall.song_list_server"}}

    with open(file_singer_info, 'r', encoding='utf8') as rf:
        for line in rf:
            line = line.strip()
            items = line.split('|||')
            if len(items) < 3: continue

            if(items[2] == ''): continue

            mid = items[2].split('.')[-2].split('/')[-1]

            if mid == "0025NhlN2yWrP4":
                print(mid)

            artist = items[0]
            artist_dir = 'F:/music_spider/musics/' + mid

            if mid == '002Tf3bV0hrUVH' or mid == '003XhiKn0FP6Nu' or mid == '002BUZcl2OSALk':
                continue



            if mid in artist_dict:
                totalNum = artist_dict[mid]
                if totalNum == 43720:
                    continue
            if (os.path.exists(artist_dir)):
                files = os.listdir(artist_dir)
                if len(files) == totalNum:
                    print("deal artist: " + artist + " alreday success! mid = " + str(mid) + " totle num = " + str(totalNum))
                    continue

            begin = 0
            total = 0
            param['singerMid'] = mid
            param['begin'] = begin
            data['param'] = param
            postUrl = url + "data=" + json.dumps(data)
            result = requests.get(postUrl.encode()).json()

            singerSongList = result['singerSongList']['data']


            totalNum = int(singerSongList['totalNum'])
            if totalNum <= 0:
                print(postUrl)
                print(result)

            ttn.write(artist + '|||' + str(mid) + '|||' + str(totalNum) + '\n')

            if (os.path.exists(artist_dir)):
                files = os.listdir(artist_dir)
                if len(files) == totalNum:
                    print("deal artist: " + artist + " success! mid = " + str(mid) + " totle num = " + str(totalNum))
                    continue
            else:
                os.mkdir(artist_dir)

            songList = singerSongList['songList']
            total = len(os.listdir(artist_dir))
            try_num = 0
            while total < totalNum and try_num < 5:
                print(mid)
                print(totalNum)
                print(total)
                print(len(songList))
                for song in songList:
                    songInfo = song['songInfo']
                    song_mid = songInfo['mid']
                    name = songInfo['name']
                    name = removeStop(name)
                    file_song = artist_dir + '/' + str(song_mid)
                    with open(file_song, 'w', encoding='utf8') as wf:
                        wf.write(str(songInfo))

                total = len(os.listdir(artist_dir))
                if total < totalNum:
                    if(begin > totalNum):
                        try_num += 1
                        begin = 0
                    else:
                        begin += 90
                    param['begin'] = begin
                    data['param'] = param
                    postUrl = url + "data=" + json.dumps(data)
                    result = requests.get(postUrl.encode()).json()
                    singerSongList = result['singerSongList']['data']
                    songList = singerSongList['songList']
            print("deal artist: " + artist + " success! mid = " + str(mid) + " totle num = " + str(totalNum))

def removeStop(input):
    input = input.replace('?', '')
    input = input.replace('"', '')
    input = input.replace('*', '').replace('/', '')
    input = input.replace('?', '')
    input = input.replace('.', '')
    input = input.replace('!', '')
    input = input.replace('$', '')
    input = input.replace('.', '')
    input = input.replace('`', '')
    input = input.replace('[', '')
    input = input.replace(']', '')
    input = input.replace('(', '')
    input = input.replace(')', '')
    input = input.replace('<', '')
    input = input.replace('>', '')
    return input

def is_chinese(string):
    """
    检查整个字符串是否包含中文
    :param string: 需要检查的字符串
    :return: bool
    """
    for ch in string:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True

    return False

def artist_name_normalize():
    wf = open(file_artist_table, 'w', encoding='utf8')
    max_hot = 0
    with open(file_singer_info, 'r', encoding='utf8') as rf:
        for line in rf:
            line = line.strip()
            items = line.split('|||')
            artist_name = items[0]
            hot = 0
            if len(items) >= 2:
                if items[1].endswith('万'):
                    hot = float(items[1][:-1]) * 10000
                else: hot = int(items[1])

            artist_name = removeStop(artist_name)

            if '(' in artist_name and ')' in artist_name:
                artist_items = artist_name.split('(')
                name1 = artist_items[0].strip()
                name2 = artist_items[1].split(')')[0].strip()

                if not is_chinese(name1) and len(name1) <= 3 and hot > 500:
                    print(name1)
                if not is_chinese(name2) and len(name2) <= 3 and hot > 500:
                    print(name2)

                wf.write(name1 + '|||' + str(hot) + '\n')
                wf.write(name2 + '|||' + str(hot) + '\n')
            else:
                if not is_chinese(artist_name) and len(artist_name) <= 3 and hot > 500:
                    print(artist_name)

                wf.write(artist_name + '|||' + str(hot) + '\n')

def jsonFormat(jsonStr):
    print('input:' + jsonStr)
    jsonStr = jsonStr.strip()
    ret = ''
    if jsonStr == '':
        ret = jsonStr
    if jsonStr[0] == '{':
        items = jsonStr[1:-1].split(',')
        for i in range(len(items)):
            item = items[i].strip()
            idx = item.find(':')
            print(item)
            key = item[:idx]
            val = item[idx+1:]

            print(key)
            print(val)

            key = jsonFormat(key)
            val = jsonFormat(val)
            items[i] = str(key) + ':' + str(val)
        ret = '{' + ",".join(items) + '}'
    elif jsonStr[0] == '[':
        items = jsonStr[1:-1].split(',')
        for i in range(len(items)):
            items[i] = str(jsonFormat(items[i]))
        ret = '[' + ",".join(items) + ']'
    else:
        if not jsonStr.isdigit():
            tmpStr = jsonStr[1:-1]
            tmpStr = tmpStr.replace('"', '')
            jsonStr = '"' + tmpStr + '"'

            ret = jsonStr
        else:
            ret = jsonStr

    print('output:' + ret)
    return ret


def get_title_info_thread(song_mid, song_id):
    print("get_title_info_thread")
    try:
        headers = {"Connection": "close",}
        url = 'https://u.y.qq.com/cgi-bin/musicu.fcg?&'
        param = {"song_type": 0, "song_mid": song_mid, "song_id": song_id}
        data = {"comm": {"ct": 24, "cv": 0},
                "songinfo": {"method": "get_song_detail_yqq", "param": param, "module": "music.pf_song_detail_svr"}}
        postUrl = url + "data=" + json.dumps(data)
        result = requests.get(postUrl.encode(), headers=headers).json()
        data = result['songinfo']['data']
        data_info = data['info']
        company = ''
        genre = ''
        lan = ''
        pub_time = ''
        name = ''
        track_id = 0
        singer = ''
        album = ''
        hot = 0

        if 'company' in data_info and len(data_info['company']) > 0:
            company = data_info['company']['content'][0]['value']
        if 'genre' in data_info and len(data_info['genre']) > 0:
            genre = data_info['genre']['content'][0]['value']
        if 'lan' in data_info and len(data_info['lan']) > 0:
            lan = data_info['lan']['content'][0]['value']
        if 'pub_time' in data_info and len(data_info['pub_time']) > 0:
            pub_time = data_info['pub_time']['content'][0]['value']

        if 'extras' in data:
            name = data['extras']['name']

        if 'track_info' in data:
            track_id = data['track_info']['id']
            if 'singer' in data['track_info'] and len(data['track_info']['singer']) > 0:
                singer = data['track_info']['singer'][0]['name']
            if 'album' in data['track_info']:
                album = data['track_info']['album']['name']
        topUrl = 'https://c.y.qq.com/base/fcgi-bin/fcg_global_comment_h5.fcg?g_tk_new_20200303=5381&g_tk=5381&hostUin=0&format=json&inCharset=utf8&outCharset=GB2312&notice=0&platform=yqq.json&needNewCode=0&cid=205360772&reqtype=1&biztype=1&cmd=4&needmusiccrit=0&pagenum=0&pagesize=0&lasthotcommentid=&domain=qq.com&topid=' + str(
            track_id)
        topResult = requests.get(topUrl.encode()).json()
        if 'commenttotal' in topResult:
            hot = topResult['commenttotal']
        wline = "|||".join([str(song_mid), name, singer, album, genre, lan, pub_time, company, str(hot)])
    except Exception as e:
        print(e)
        return -1
    return wline


def get_title_hot():
    worksnum = 20
    executor = ThreadPoolExecutor(max_workers=worksnum)
    workers = []

    title_dict = {}
    with open(file_title_nums, 'r', encoding='utf8') as rf:
        for line in rf:
            items = line.strip().split('|||')
            if len(items) >= 1:
                mid = items[0]
                title_dict[mid] = line
    title_num = open(file_title_nums, 'a', encoding='utf8')

    artist_filter = []

    count = 0

    dirs = os.listdir(dir_music)
    for dir in dirs:
        singer_dir = dir_music + dir

        if dir in artist_filter:
            continue

        files = os.listdir(singer_dir)
        for file in files:
            count += 1
            if count % 10000 == 0:
                print(count)

            title_file = singer_dir + '/' + file
            #print(title_file)
            with open(title_file, 'r', encoding='utf8') as rf:
                try:
                    for line in rf:
                        try:
                            #data = json.loads(line)
                            data = eval(line.strip())
                        except Exception as e:
                            print(e)
                            print('json load error! line = ' + line)
                            continue
                        song_id = data['id']
                        song_mid = data['mid']

                        if song_mid in title_dict:
                            #print(str(song_mid) + " is alerade success!")
                            continue

                        print("work nums = " + str(len(workers)))

                        while len(workers) >= worksnum:
                            time.sleep(1)
                            tmp_list = []
                            for work in workers:
                                if work.done() == True:
                                    ret = work.result()
                                    print('ret = ' + str(ret))
                                    if ret != -1:
                                        title_num.write(ret + '\n')
                                        title_num.flush()
                                else:
                                    tmp_list.append(work)
                            workers = tmp_list
                        workers.append(executor.submit(get_title_info_thread, song_mid, song_id))
                        tmp_list = []
                        for work in workers:
                            if work.done() == True:
                                ret = work.result()
                                print('ret = ' + str(ret))
                                if ret != -1:
                                    title_num.write(ret + '\n')
                                    title_num.flush()
                            else:
                                tmp_list.append(work)
                        workers = tmp_list

                except Exception as e:
                    print('error:' + str(e))

def findword(str):
    wordlist = []
    title = ''
    stack = []
    for i in range(len(str)):
        ch = str[i]
        if ch == '(' or ch == '（':
            stack.append((ch, i))
        elif (ch == ')' or ch == '）') and len(stack) > 0:
            if (ch == ')' and stack[-1][0] == '(') or (ch == '）' and stack[-1][0] == '（'):
                (_, start_idx) = stack.pop()
                word = str[start_idx+1:i]
                wordlist.append(word)
        else:
            if len(stack) == 0:
                title += ch
    return  [title, wordlist]

def title_name_normalize():
    title_dict = {}
    wf = open('F:/music_spider/title_norm', 'w', encoding='utf8')
    with open('F:/music_spider/title_nums', 'r', encoding='utf8') as rf:
        count = 0
        for line in rf:
            line = line.strip()
            items = line.split('|||')
            if len(items) != 9:
                continue

            mid, title, artist, album, _, language, date, _, hot = items

            if not hot.isdigit():
                continue
            if hot.isdigit() and int(hot) < 250:
                continue

            title_name, wordlist = findword(title)
            tmpstrs = []
            if '+' in title_name:
                title_names = title_name.split('+')
                for x in title_names:
                    count += 1
                    tmpstrs.append(x.strip())
            elif '＋' in title_name:
                title_names = title_name.split('＋')
                for x in title_names:
                    count += 1
                    tmpstrs.append(x.strip)
            elif '曲' in title_name:
                flag = True
                filter_list = ['曲目', '歌曲', '舞曲', '选集', '主题曲', '插曲', '片尾曲', '《']
                for filter in filter_list:
                    if filter in title_name:
                        flag = False
                        break
                if flag == True:
                    count += 1
                    tmpstrs.append(title_name.strip())
            elif '英语阅读' in title_name:
                pass
            elif '古诗' in title_name:
                pass
            elif '《' in title_name:
                pass
            elif '有声绘本' in title_name or '有声漫画' in title_name or '有声读物' in title_name or '有声书' in title_name or '有声配乐' in title_name or '有声节目' in title_name:
                pass
            elif '朗诵' in title_name:
                pass
            else:
                count += 1
                tmpstrs.append(title_name)

            for tmp in tmpstrs:
                if tmp == '': continue
                if tmp in title_dict:
                    dict_hot = title_dict[tmp]
                    if int(hot) > dict_hot:
                        title_dict[tmp] = int(hot)
                else:
                    title_dict[tmp] = int(hot)
                #print(tmp + '\t' + hot)

            # for word in wordlist:
            #     flag = False
            #     video_sign_list = ['主题曲', '插曲', '片尾曲', '片头曲', '电视剧', '影视剧']
            #     for sign in video_sign_list:
            #         if sign in word:
            #             flag = True
            #             break
            #     if flag == True:
            #         #count += 1
            #         if '《' in word:
            #             pass
            #             #print(word)
            #         else:
            #             pass
        print(count)

        with open('F:/music_spider/title', 'r', encoding='utf8') as rf:
            for line in rf:
                line = line.strip()
                title, hot = line.split('\t')
                if int(hot) < 250: continue

                if title in title_dict:
                    dict_hot = title_dict[title]
                    if int(hot) > dict_hot:
                        title_dict[title] = int(hot)
                else:
                    title_dict[title] = int(hot)

        for key, val in title_dict.items():
            if val >= 3093539615:
                continue
            print(type(key))
            if type(key) != str: continue
            key = removeStop(key)
            wf.write(str(key) + '\t' + str(val) + '\n')






#获取歌手列表
#get_artist_list()
#获取歌手信息
#get_artist_info()
#获取歌曲信息
#get_title_info()
#获取歌手表最终结果
#artist_name_normalize()
#获取歌曲热度
get_title_hot()

#获取歌曲最终结果
#title_name_normalize()
