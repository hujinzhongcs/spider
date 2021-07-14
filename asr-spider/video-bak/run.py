from spider import *
#from washer import *
#from uploader.Uploader import push_to_es, append_to_es
import sys
#import re
import os
import time
#from util import *


def run_spider():
    start = time.time()
    if not os.path.exists('./data/url'):
        os.makedirs('./data/url')
    if not os.path.exists('./data/raw'):
        os.makedirs('./data/raw')
    # 爱奇艺
    iqiyiSpider = IQiYiSpider()
    iqiyiSpider.get_album_urls('./data/url/iqiyi.txt')
    iqiyiSpider.get_album_info('./data/url/iqiyi.txt', './data/raw/iqiyi.txt', 5)
    # 腾讯视频
    tencent = TencentSpider()
    tencent.get_album_urls('./data/url/tencent_child_urls.txt')
    tencent.get_album_urls_for_batch('./data/url/tencent_urls.txt')
    tencent.get_album_info('./data/url/tencent_urls.txt', './data/raw/tencent_data.txt', 10)
    tencent.get_album_info('./data/url/tencent_cartoon_urls.txt', './data/raw/tencent_cartoon_data.txt', 10)
    tencent.get_album_info('./data/url/tencent_child_urls.txt', './data/raw/tencent_child_data.txt', 30)
    tencent.get_album_info('./data/url/tencent_doco_urls.txt', './data/raw/tencent_doco_data.txt', 20)
    tencent.get_album_info('./data/url/tencent_variety_urls.txt', './data/raw/tencent_variety_data.txt', 10)
    tencent.get_album_info('./data/url/tencent_movies_urls.txt', './data/raw/tencent_movies_data.txt', 50)
    tencent.get_album_info('./data/url/tencent_tv_urls.txt', './data/raw/tencent_tv_data.txt', 30)

    # 豆瓣
    douban = DoubanSpider()
    douban.get_album_urls('./data/url/douban_urls.txt')
    douban.get_album_info('./data/url/douban_movies_urls.txt', './data/raw/douban_movies_data.txt', 10)
    douban.get_album_info('./data/url/douban_other_urls.txt', './data/raw/douban_other_data.txt', 30)

    end = time.time()
    print("time cost: {}m".format(round((end - start) / 60, 2)))


if __name__ == '__main__':
    run_spider()