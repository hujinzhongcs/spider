import os
import time
import shutil
import requests
import threading
from datetime import datetime
from selenium import webdriver
from bs4 import BeautifulSoup as bs
from util.ResourceObj import ResourceObj, ItemObj

class IQiYiSpider:
    def __init__(self):
        self._headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.57 Safari/537.36'}
        self._timeout = 30
        self._root_url = 'https://www.iqiyi.com'
        self._lst_category_url = {
            '电影':'https://list.iqiyi.com/www/1/-----------{period}--24-1-1-iqiyi--.html',
            '电视剧':'https://list.iqiyi.com/www/2/-----------{period}--24-1-1-iqiyi--.html',
            '纪录片':'https://list.iqiyi.com/www/3/-----------{period}--24-1-1-iqiyi--.html',
            '动漫':'https://list.iqiyi.com/www/4/-----------{period}--24-1-1-iqiyi--.html',
            '综艺':'https://list.iqiyi.com/www/6/-----------{period}--24-1-1-iqiyi--.html',
            '教育':'https://list.iqiyi.com/www/12/-----------{period}--24-1-1-iqiyi--.html',
            '儿童':'https://list.iqiyi.com/www/15/-----------{period}--24-1-1-iqiyi--.html',
        }

        self._lst_period = list()
        for i in range(1910, 1980, 10):
            self._lst_period.append('{}_{}'.format(i, i+9))
        for i in range(1980, 2021):
            self._lst_period.append(str(i))

    def get_album_urls(self, out_path):
        if os.path.isfile(out_path):
            print('[IQiYiSpider]{} exists'.format(out_path))
            return
        lst_type = self._get_type_urls()
        print(lst_type)
        driver = webdriver.Chrome()
        f_out = open(out_path, 'w', encoding='utf-8')
        # f_out = open(out_path, 'a', encoding='utf-8')
        for video_type in lst_type:
            type_name = video_type[0]
            type_url = video_type[1]

            print('[IQiYiSpider]{}\t{}'.format(datetime.now(), type_name))
            print(type_url)
            driver.get(type_url)
            js = "var q=document.documentElement.scrollTop=document.body.scrollHeight"
            last_cnt = 0
            retry_times = 0
            while True:
                driver.execute_script(js)
                time.sleep(1)
                soup = bs(driver.page_source, 'lxml')
                album_nodes = soup.select('li.qy-mod-li > div > div.title-wrap > p > a')
                print(len(album_nodes))
                if len(album_nodes) == last_cnt:
                    if len(album_nodes) % 48 == 0 and retry_times < 5:
                        retry_times += 1
                        continue
                    if album_nodes and len(album_nodes) > 0:
                        for album_node in album_nodes:
                            f_out.write('{}\t{}{}\n'.format(type_name, 'https:', album_node.get('href')))
                    break
                else:
                    last_cnt = len(album_nodes)
        driver.close()
        f_out.close()
        self._merge_duplicate(out_path)

    def get_album_info(self, in_path, out_path, thr_cnt=30):
        def thread_work(lines, out_path, idx):
            out_path_real = '{}_{}'.format(out_path, idx)
            if os.path.isfile(out_path_real):
                print('[IQiYiSpider]{} exists'.format(out_path_real))
                return
            driver = webdriver.Chrome()
            f_out = open(out_path_real, 'w', encoding='utf-8')
            for line in lines:
                out_string = self._parse(line, driver)
                if out_string != '':
                    f_out.write(out_string + '\n')
                    f_out.flush()
            f_out.close()
            self._get_album_info_redo(out_path_real)

        f_in = open(in_path, 'r', encoding='utf-8')
        lines = f_in.readlines()
        f_in.close()
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

    def _get_album_info_redo(self, in_path):
        tmp_path = in_path + '_tmp'
        f_out = open(tmp_path, 'w', encoding='utf-8')
        driver = webdriver.Chrome()

        with open(in_path, 'r', encoding='utf-8') as f_in:
            line = f_in.readline()
            while line:
                line = line.strip()
                if line == '':
                    continue
                if line.startswith('FAIL:'):
                    out_string = self._parse(line[5:], driver)
                    if out_string != '':
                        f_out.write(out_string + '\n')
                else:
                    f_out.write(line + '\n')
                line = f_in.readline()
        f_out.close()
        # shutil.move(tmp_path, in_path)

    def _parse(self, line, driver):
        line = line.strip()
        parts = line.split('\t')
        if len(parts) != 2:
            return ''
        type_name = parts[0]
        album_url = parts[1]
        try:
            album = ResourceObj()
            album.source = 'iqiyi'
            album.category = type_name
            album.url = album_url
            # html = requests.get(album_url, headers=self._headers, timeout=self._timeout)
            # html.encoding = 'utf-8'
            # soup = bs(html.text, 'lxml')
            driver.get(album_url)
            retry_time = 0
            while len(driver.find_elements_by_css_selector('div.qy-player-basic-intro > article > div > span.basic-txt')) <= 0:
                if retry_time > 10:
                    break
                retry_time += 1
                time.sleep(1)
            # while len(soup.select('div.qy-player-basic-intro > article > div > span.basic-txt')) <= 0:
            #     time.sleep(1)
            soup = bs(driver.page_source, 'lxml')
            # print(soup)
            # 标题
            album_name_nodes = soup.select('div.qy-player-side-head > div.head-title > h2 > span')
            if album_name_nodes and len(album_name_nodes) > 0:
                album.raw_name = album_name_nodes[0].get_text().strip()
            else:
                album_name_nodes = soup.select('div.qy-player-side-head > div.head-title > h2 > a')
                if album_name_nodes and len(album_name_nodes) > 0:
                    album.raw_name = album_name_nodes[0].get('title').strip()
            # 标签
            tag_nodes = soup.select('#titleRow > div.intro-mn > div > div.qy-player-tag > a')
            if tag_nodes and len(tag_nodes) > 0:
                for tag_node in tag_nodes:
                    album.tags.add(tag_node.get_text().strip())
            # 热度
            hits_nodes = soup.select('div.qy-player-basic-intro > article > div > span.basic-txt')
            if hits_nodes and len(hits_nodes) > 0:
                album.hits = hits_nodes[0].get_text().strip()
            # 导演 演员 角色
            intro_item_nodes = soup.select('li.intro-detail-item')
            if intro_item_nodes and len(intro_item_nodes) > 0:
                for intro_item_node in intro_item_nodes:
                    # print(intro_item_node)
                    em_nodes = intro_item_node.select('em.item-title')
                    if em_nodes == None or len(em_nodes) == 0:
                        continue
                    elif em_nodes[0].get_text() in ['导演：']:
                        director_nodes = intro_item_node.select('a.name-link')
                        if director_nodes and len(director_nodes) > 0:
                            for director_node in director_nodes:
                                album.directors.add(director_node.get_text().strip())
                    elif em_nodes[0].get_text() in ['主演：', '嘉宾：']:
                        artist_nodes = intro_item_node.select('a.name-link')
                        if artist_nodes and len(artist_nodes) > 0:
                            for artist_node in artist_nodes:
                                album.actors.add(artist_node.get_text().strip())
                        role_nodes = intro_item_node.select('span.name-span')
                        if role_nodes and len(role_nodes) > 0:
                            for role_node in role_nodes:
                                album.roles.add(role_node.get_text().replace('饰 ', '').strip())
                    else:
                        continue
            # 简介 补充标签
            if type_name in ['电视剧', '综艺']:
                detail_nodes = soup.select('div.qy-player-intro-pop > div.intro-left > a.intro-more')
                if detail_nodes and len(detail_nodes) > 0:
                    html = requests.get('http:' + detail_nodes[0].get('href'), headers=self._headers, timeout=self._timeout)
                    html.encoding = 'utf-8'
                    soup = bs(html.text, 'lxml')
                    tag_nodes = soup.select('div.episodeIntro > div.episodeIntro-item > a')
                    if tag_nodes and len(tag_nodes) > 0:
                        for tag_node in tag_nodes:
                            album.tags.add(tag_node.get_text().strip())
                    # intro_nodes = soup.select('div.episodeIntro > div.episodeIntro-brief')
                    # if intro_nodes and len(intro_nodes) > 0:
                    #     album._desc = intro_nodes[0].get('title')
            out_string = album.to_string()
        except Exception as e:
            out_string = 'FAIL:{}'.format(line)
            # print(str(e))
            print(line)
            print(str(e))
        return out_string

    def _get_type_urls(self):
        ret = list()
        for category in self._lst_category_url:
            for period in self._lst_period:
                new_url = self._lst_category_url[category].replace('{period}', period)
                ret.append((category, new_url))
        return ret

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