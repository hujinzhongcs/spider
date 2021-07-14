import json
import shutil
import threading
import time

import requests

from spider.douban.DoubanCategoryFactory import DoubanCategoryFactory
from util.ResourceObj import ResourceObj


class DoubanSpider:
    def __init__(self):
        self._headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36'}
        self._timeout = 30
        self._root_url = 'https://www.douban.com/'
        self._lst_category_url = {
            # '电影':'https://movie.douban.com/j/search_subjects?type=movie&tag=%E7%83%AD%E9%97%A8&sort=recommend&page_limit=2000&page_start=0',
            # '美剧':'https://movie.douban.com/j/search_subjects?type=tv&tag=%E7%BE%8E%E5%89%A7&sort=recommend&page_limit=2000&page_start=0',
            # '英剧':'https://movie.douban.com/j/search_subjects?type=tv&tag=%E8%8B%B1%E5%89%A7&sort=recommend&page_limit=2000&page_start=0',
            # '韩剧':'https://movie.douban.com/j/search_subjects?type=tv&tag=%E9%9F%A9%E5%89%A7&sort=recommend&page_limit=2000&page_start=0',
            # '日剧':'https://movie.douban.com/j/search_subjects?type=tv&tag=%E6%97%A5%E5%89%A7&sort=recommend&page_limit=2000&page_start=0',
            # '国产':'https://movie.douban.com/j/search_subjects?type=tv&tag=%E5%9B%BD%E4%BA%A7%E5%89%A7&sort=recommend&page_limit=2000&page_start=0',
            # '港剧':'https://movie.douban.com/j/search_subjects?type=tv&tag=%E6%B8%AF%E5%89%A7&sort=recommend&page_limit=2000&page_start=0',
            # '动漫':'https://movie.douban.com/j/search_subjects?type=tv&tag=%E6%97%A5%E6%9C%AC%E5%8A%A8%E7%94%BB&sort=recommend&page_limit=2000&page_start=0',
            # '综艺':'https://movie.douban.com/j/search_subjects?type=tv&tag=%E7%BB%BC%E8%89%BA&sort=recommend&page_limit=2000&page_start=0',
            # '纪录片':'https://movie.douban.com/j/search_subjects?type=tv&tag=%E7%BA%AA%E5%BD%95%E7%89%87&sort=recommend&page_limit=2000&page_start=0'

            '热门': 'https://movie.douban.com/j/search_subjects?type=movie&tag=%E7%83%AD%E9%97%A8&sort=time&page_limit=2000&page_start=0',
            '最新': 'https://movie.douban.com/j/search_subjects?type=movie&tag=%E6%9C%80%E6%96%B0&page_limit=2000&page_start=0',
            '经典': 'https://movie.douban.com/j/search_subjects?type=movie&tag=%E7%BB%8F%E5%85%B8&sort=time&page_limit=2000&page_start=0',
            '可播放': 'https://movie.douban.com/j/search_subjects?type=movie&tag=%E5%8F%AF%E6%92%AD%E6%94%BE&sort=time&page_limit=2000&page_start=0',
            '豆瓣高分': 'https://movie.douban.com/j/search_subjects?type=movie&tag=%E8%B1%86%E7%93%A3%E9%AB%98%E5%88%86&sort=time&page_limit=2000&page_start=0',
            '冷门佳作': 'https://movie.douban.com/j/search_subjects?type=movie&tag=%E5%86%B7%E9%97%A8%E4%BD%B3%E7%89%87&sort=time&page_limit=2000&page_start=0',
            '华语': 'https://movie.douban.com/j/search_subjects?type=movie&tag=%E5%8D%8E%E8%AF%AD&sort=time&page_limit=2000&page_start=0',
            '欧美': 'https://movie.douban.com/j/search_subjects?type=movie&tag=%E6%AC%A7%E7%BE%8E&sort=time&page_limit=2000&page_start=0',
            '韩国': 'https://movie.douban.com/j/search_subjects?type=movie&tag=%E9%9F%A9%E5%9B%BD&sort=time&page_limit=2000&page_start=0',
            '日本': 'https://movie.douban.com/j/search_subjects?type=movie&tag=%E6%97%A5%E6%9C%AC&sort=time&page_limit=2000&page_start=0',
            '动作': 'https://movie.douban.com/j/search_subjects?type=movie&tag=%E5%8A%A8%E4%BD%9C&sort=time&page_limit=2000&page_start=0',
            '喜剧': 'https://movie.douban.com/j/search_subjects?type=movie&tag=%E5%96%9C%E5%89%A7&sort=time&page_limit=2000&page_start=0',
            '爱情': 'https://movie.douban.com/j/search_subjects?type=movie&tag=%E7%88%B1%E6%83%85&sort=time&page_limit=2000&page_start=0',
            '科幻': 'https://movie.douban.com/j/search_subjects?type=movie&tag=%E7%A7%91%E5%B9%BB&sort=time&page_limit=2000&page_start=0',
            '悬疑': 'https://movie.douban.com/j/search_subjects?type=movie&tag=%E6%82%AC%E7%96%91&sort=time&page_limit=2000&page_start=0',
            '恐怖': 'https://movie.douban.com/j/search_subjects?type=movie&tag=%E6%81%90%E6%80%96&sort=time&page_limit=2000&page_start=0',
            '成长': 'https://movie.douban.com/j/search_subjects?type=movie&tag=%E6%88%90%E9%95%BF&sort=time&page_limit=2000&page_start=0'
        }

    def req(self, url):
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
            result = self.req(type_url)
            json_result = json.loads(result)
            for item in json_result['subjects']:
                print('{}\t{}'.format(type_name, item['url']))
                f_out.write('{}\t{}\n'.format(type_name, item['url']))

        f_out.close()
        self._merge_duplicate(out_path)

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
                    # album._category = '电影'
                    album.url = album_url
                    album.source = 'douban'

                    factory = DoubanCategoryFactory(album_url, album)
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