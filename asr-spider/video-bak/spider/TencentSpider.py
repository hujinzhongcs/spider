import json
import shutil
import threading
import time
from datetime import datetime

import requests
from lxml import etree
from selenium import webdriver

from spider.tencent.TencentCategoryFactory import TencentCategoryFactory
from util.ResourceObj import ResourceObj

class TencentSpider:
    def __init__(self):
        self._headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36'}
        self._timeout = 30
        self._root_url = 'https://v.qq.com/'
        self._lst_category_url = {
            # '电影':'https://v.qq.com/channel/movie?listpage=1&channel=movie&sort=18&_all=1',
            # '电视剧':'https://v.qq.com/channel/tv?_all=1&channel=tv&feature=-1&iarea=-1&listpage=1&pay=-1&sort=18&year=-1',
            '纪录片':'https://v.qq.com/channel/doco?listpage=1&channel=doco&sort=18&_all=1',
            '动漫':'https://v.qq.com/channel/cartoon?listpage=1&channel=cartoon&sort=18&_all=1',
            '综艺':'https://v.qq.com/channel/variety?listpage=1&channel=variety&sort=4&_all=1',
            '儿童':'https://v.qq.com/channel/child?listpage=1&channel=child&sort=18&_all=1',
        }
        self._batch_category_url = {
            '电影': [
                'https://v.qq.com/channel/movie?_all=1&channel=movie&listpage=1&sort=18&year=2020',
                'https://v.qq.com/channel/movie?_all=1&channel=movie&listpage=1&sort=18&year=20',
                'https://v.qq.com/channel/movie?_all=1&channel=movie&listpage=1&sort=18&year=2018',
                'https://v.qq.com/channel/movie?_all=1&channel=movie&listpage=1&sort=18&year=2017',
                'https://v.qq.com/channel/movie?_all=1&channel=movie&listpage=1&sort=18&year=2016',
                'https://v.qq.com/channel/movie?_all=1&channel=movie&listpage=1&sort=18&year=100063',
                'https://v.qq.com/channel/movie?_all=1&channel=movie&listpage=1&sort=18&year=100034',
                'https://v.qq.com/channel/movie?_all=1&channel=movie&listpage=1&sort=18&year=100035',
                'https://v.qq.com/channel/movie?_all=1&channel=movie&listpage=1&sort=18&year=100036',
                'https://v.qq.com/channel/movie?_all=1&channel=movie&listpage=1&sort=18&year=100037',
                'https://v.qq.com/channel/movie?_all=1&channel=movie&listpage=1&sort=18&year=100038',
                'https://v.qq.com/channel/movie?_all=1&channel=movie&listpage=1&sort=18&year=100039',
                'https://v.qq.com/channel/movie?_all=1&channel=movie&listpage=1&sort=18&year=100040'
            ],
            '电视剧': [
                'https://v.qq.com/channel/tv?_all=1&channel=tv&listpage=1&sort=18&year=2020',
                'https://v.qq.com/channel/tv?_all=1&channel=tv&listpage=1&sort=18&year=4061',
                'https://v.qq.com/channel/tv?_all=1&channel=tv&listpage=1&sort=18&year=4060',
                'https://v.qq.com/channel/tv?_all=1&channel=tv&listpage=1&sort=18&year=2017',
                'https://v.qq.com/channel/tv?_all=1&channel=tv&listpage=1&sort=18&year=859',
                'https://v.qq.com/channel/tv?_all=1&channel=tv&listpage=1&sort=18&year=860',
                'https://v.qq.com/channel/tv?_all=1&channel=tv&listpage=1&sort=18&year=861',
                'https://v.qq.com/channel/tv?_all=1&channel=tv&listpage=1&sort=18&year=862',
                'https://v.qq.com/channel/tv?_all=1&channel=tv&listpage=1&sort=18&year=863',
                'https://v.qq.com/channel/tv?_all=1&channel=tv&listpage=1&sort=18&year=864',
                'https://v.qq.com/channel/tv?_all=1&channel=tv&listpage=1&sort=18&year=865',
                'https://v.qq.com/channel/tv?_all=1&channel=tv&listpage=1&sort=18&year=866'
            ]
        }

    def get_html(self, url):
        resp = requests.get(url, headers=self._headers, timeout=self._timeout)
        resp.encoding = 'utf-8'
        return resp.text

    def get_album_urls(self, out_path):
        lst_type = self._get_type_urls()
        print(lst_type)
        f_out = open(out_path, 'w+', encoding='utf-8')
        for video_type in lst_type:
            type_name = video_type[0]
            type_url = video_type[1]

            print('[TencentSpider]{}\t{}'.format(datetime.now(), type_name))
            driver = webdriver.Chrome()
            driver.get(type_url)
            js = "var q=document.documentElement.scrollTop=document.body.scrollHeight"
            last_cnt = 0
            retry_cnt = 0
            while True:
                driver.execute_script(js)
                time.sleep(2)
                html = etree.HTML(driver.page_source)
                album_nodes = html.xpath('//div[@class="list_item"]/a/@href')
                curr_cnt = len(album_nodes)
                print('current cnt {}', curr_cnt)
                if curr_cnt == last_cnt:
                    if retry_cnt > 2:
                        if album_nodes and curr_cnt > 0:
                            if album_nodes and curr_cnt > 0:
                                for album_node in album_nodes:
                                    f_out.write('{}\t{}\n'.format(type_name, album_node))
                        break
                    else:
                        retry_cnt += 1
                        print('retry...{}', retry_cnt)
                else:
                    last_cnt = curr_cnt
                    retry_cnt = 0
        f_out.close()
        self._merge_duplicate(out_path)

    def get_album_urls_for_batch(self, out_path):
        def thread_url_task(key, urls):
            out_path_real = "{}.{}".format(out_path, key)
            f_out = open(out_path_real, 'w+', encoding='utf-8')
            lines = set()
            for type_url in urls:
                type_name = key
                print('[TencentSpider]{}\t{}'.format(datetime.now(), type_name))
                driver = webdriver.Chrome()
                driver.get(type_url)
                js = "var q=document.documentElement.scrollTop=document.body.scrollHeight"
                last_cnt = 0
                retry_cnt = 0
                while True:
                    driver.execute_script(js)
                    time.sleep(2)
                    html = etree.HTML(driver.page_source)
                    album_nodes = html.xpath('//div[@class="list_item"]/a/@href')
                    curr_cnt = len(album_nodes)
                    print('{} current cnt {}'.format(key, curr_cnt))
                    if curr_cnt == last_cnt:
                        if retry_cnt > 2:
                            if album_nodes and curr_cnt > 0:
                                if album_nodes and curr_cnt > 0:
                                    for album_node in album_nodes:
                                        lines.add('{}\t{}\n'.format(type_name, album_node))
                            break
                        else:
                            retry_cnt += 1
                            print('retry...{}'.format(retry_cnt))
                    else:
                        last_cnt = curr_cnt
                        retry_cnt = 0
            for line in lines:
                f_out.write(line)
            f_out.close()
            print('{} task finished'.format(key))

        for key in self._batch_category_url:
            urls = self._batch_category_url[key]
            thread = threading.Thread(thread_url_task(key, urls))
            thread.start()

    def get_album_info(self, in_path, out_path, thr_cnt=30):
        def thread_work(lines, out_path, idx):
            out_path_real = '{}_{}'.format(out_path, idx)
            f_out = open(out_path_real, 'w+', encoding='utf-8')
            for line in lines:
                parts = line.strip().split('\t')
                if len(parts) != 2:
                    continue
                type_name = parts[0]
                album_url = parts[1]
                try:
                    album = ResourceObj()
                    album.category = type_name
                    album.url = album_url
                    album.source = 'tencent'

                    factory = TencentCategoryFactory(album_url, album)
                    category = factory.get_category(type_name)
                    album = category.get_album_info()

                    # out_string = json.dumps(album.to_dict(), ensure_ascii=False)
                    out_string = album.to_string()
                except Exception as e:
                    out_string = 'FAIL:{}'.format(line)
                f_out.write(out_string + '\n')
            f_out.close()
            print('thread {} finished'.format(idx))

        f_in = open(in_path, 'r', encoding='utf-8')
        lines = f_in.readlines()
        f_in.close()

        if len(lines) <= thr_cnt:
            thread = threading.Thread(target=thread_work, args=(lines, out_path, 0))
            thread.start()
        else:
            num_per_thr = (len(lines) - 1) // thr_cnt + 1
            lst_thr = list()
            for i in range(thr_cnt):
                thread = threading.Thread(target=thread_work, args=(lines[i * num_per_thr:(i + 1) * num_per_thr], out_path, i))
                lst_thr.append(thread)
            for thread in lst_thr:
                thread.start()
                time.sleep(1)
            for thread in lst_thr:
                thread.join()

    def _get_type_urls(self):
        return [(name, self._lst_category_url[name]) for name in self._lst_category_url]

    def _merge_duplicate(self, filepath):
        f_in = open(filepath, 'r', encoding='utf-8')
        map_url = dict()
        line = f_in.readline()
        while line:
            parts = line.strip().split('\t')
            if len(parts) != 2:
                line = f_in.readline()
                continue
            if parts[1] in map_url:
                map_url[parts[1]] += ' ' + parts[0]
            else:
                map_url[parts[1]] = parts[0]
            line = f_in.readline()
        f_in.close()

        filepath_tmp = filepath + '_tmp'
        with open(filepath_tmp, 'w', encoding='utf-8') as f_tmp:
            for url in map_url:
                f_tmp.write('{}\t{}\n'.format(map_url[url], url))

        shutil.move(filepath, filepath + '_raw')
        shutil.move(filepath_tmp, filepath)

    def parse_roles(self, roles):
        invalid_chars = ['/', '\n', '\xa0\xa0\xa0']
        directors = []
        actors = []
        # True 导演， False演员
        flag = True
        for role in roles:
            break_flag = False
            for c in invalid_chars:
                if c in role:
                    break_flag = True
            if break_flag:
                continue
            if '演员:' in role:
                flag = False
                continue
            elif '导演:' in role:
                flag = True
                continue
            if flag:
                directors.append(role)
            else:
                actors.append(role)
        return directors, actors