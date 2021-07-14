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

def baidu_search():
    url = "https://www.baidu.com/s?wd=许冠杰的纸船"
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(1)
    soup = BeautifulSoup(driver.page_source, 'lxml')
    print(soup)


baidu_search()