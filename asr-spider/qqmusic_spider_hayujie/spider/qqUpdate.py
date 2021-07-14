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

class QqUpdate():
    def __init__(self):
        self.driver = webdriver.Chrome(executable_path="F:/chromdriver/chromedriver.exe")
        self.updateDir = './add/'
        self.updateToplistTitle = self.updateDir + 'updateToplistTitle'
        self.updateToplistArtist = self.updateDir + 'updateToplistArtist'

    def update(self):
        titleDict = {}
        artistDict = {}
        self.toplist_travel(titleDict, artistDict)
        print(titleDict)
        self.getTitleInfo()

    def getTitleInfo(self, titleDict):
        wf = open(self.updateToplistTitle, 'w', encoding='utf8')
        for titleName in titleDict:
            titleItem = titleDict[titleName]
            if len(titleItem) != 2:
                continue
            titleHref = titleItem[1]
            self.driver.get(titleHref)
            time.sleep(1)
            soup = BeautifulSoup(self.driver.page_source, 'lxml')

            titledata = soup.find(class_="data_cont")


    #获取全部榜单的歌曲，歌手的链接信息
    def toplist_travel(self, titleDict, artistDict):

        #toplistNums = [62, 26, 27, 4, 67, 5, 59, 61, 28, 63, 74, 60, 64, 29, 65, 58, 57, 72, 73, 70, 36, 52, 126, 114, 127]
        toplistNums = [62]
        toplistBaseHref = 'https://y.qq.com/n/yqq/toplist/'

        for toplistNum in toplistNums:
            toplistHref = toplistBaseHref + str(toplistNum) + '.html'
            self.driver.get(toplistHref)
            time.sleep(1)
            soup = BeautifulSoup(self.driver.page_source, 'lxml')

            songlist = soup.find(class_="songlist__list")
            songitems = songlist.find_all(class_="songlist__item")
            for item in songitems:
                titleItem = item.find(class_="js_song")
                artistItems = item.find_all(class_="singer_name")

                titleName = titleItem.get_text()
                titleHref = titleItem.attrs["href"]
                if titleName not in titleDict:
                    titleDict[titleName] = [titleName, titleHref]

                for artistItem in artistItems:
                    artistName = artistItem.get_text()
                    artistHref = artistItem.attrs["href"]
                    if artistName not in artistDict:
                        artistDict[artistName] = [artistName, artistHref]

def main():
    qqUpdate = QqUpdate()
    titleDict = {}
    artistDict = {}
    qqUpdate.toplist_travel(titleDict, artistDict)
    print(titleDict)
    print(artistDict)

if __name__ == '__main__':
    main()