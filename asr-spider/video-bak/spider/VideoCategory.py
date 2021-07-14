from lxml import etree
import requests


# 视频分类基类
class VideoCategory(object):
    def __init__(self, album_url, album):
        self._headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36'}
        self._timeout = 30
        self.album_url = album_url
        self.html = ''
        self.album = album

    def get_html(self, url):
        resp = requests.get(url, headers=self._headers, timeout=self._timeout)
        resp.encoding = 'utf-8'
        return resp.text

    def get_album_info(self):
        self.html = etree.HTML(self.get_html(self.album_url))
        self.get_album_name()
        self.get_directors()
        self.get_actors()
        self.get_video_tags()
        self.get_play_nums()
        self.get_year()
        self.get_region()
        self.get_language()
        return self.album

    # 标题
    def get_album_name(self):
        self.album._album_name = ''

    # 导演
    def get_directors(self):
        self.album.directors = []

    # 演员
    def get_actors(self):
        self.album._artists = []

    # 视频标签
    def get_video_tags(self):
        self.album.tags = []

    # 视频播放量
    def get_play_nums(self):
        self.album.hits = 0

    # 年份
    def get_year(self):
        self.album.period = ''

    # 地区
    def get_region(self):
        self.album.region = ''

    # 语言
    def get_language(self):
        self.album.language = ''
