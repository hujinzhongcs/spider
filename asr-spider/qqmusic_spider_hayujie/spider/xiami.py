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

requests.adapters.DEFAULT_RETRIES = 50

def get_artist_list():
    artist_set = set()
    wf = open('F:/music_spider/xiami_singer_list', 'a', encoding='utf8')

    genre_id_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 18, 19, 20, 21, 22, 24, 25]
    gender_list = ['F', 'M', 'B', 'DJ']
    location_list = ['安徽', '北京', '重庆', '福建', '甘肃', '广东', '广西', '贵州', '海南', '河北', '黑龙江', '河南', '香港', '湖北',
                     '湖南', '江苏', '江西', '吉林', '辽宁', '澳门', '内蒙古', '宁夏', '青海', '山东', '上海', '山西', '陕西', '四川',
                     '台湾', '天津', '新疆', '西藏', '云南', '浙江', '海外']
    order_list = [0, 1, 2]

    url = "https://i.xiami.com/musician/artists?genre="

    driver = webdriver.Chrome()
    for genre in genre_id_list:
        for gender in gender_list:
            for loc in location_list:
                for order in order_list:
                    success_flag = False

                    for page in range(1, 100):
                        posturl = url + str(genre) + '&gender=' + str(gender) + '&location=' + str(loc) + '&order=' + str(order) + '&page=' + str(page)
                        print(posturl)
                        driver.get(posturl)

                        artists = ''
                        while artists == '':
                            time.sleep(1)
                            soup = BeautifulSoup(driver.page_source, 'lxml')
                            artists = soup.find(class_='artists')
                            artist_list = artists.find_all(class_='artist')

                            if len(artist_list) <= 0:
                                success_flag = True
                            for artist in artist_list:
                                artist_info = artist.find(class_='info')
                                artist_name = artist_info.p.strong.a.string
                                if artist_name not in artist_set:
                                    artist_set.add(artist_name)
                                    print(artist_name)

                        if success_flag:
                            break

    driver.close()

    for artist in artist_set:
        wf.write(artist + '\n')

get_artist_list()