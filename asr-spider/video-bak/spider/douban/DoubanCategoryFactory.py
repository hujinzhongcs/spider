from spider.douban.DoubanCartoon import DoubanCartoon
from spider.douban.DoubanDoco import DoubanDoco
from spider.douban.DoubanMovie import DoubanMovie
from spider.douban.DoubanTV import DoubanTV
from spider.douban.DoubanVariety import DoubanVariety


class DoubanCategoryFactory(object):
    def __init__(self, album_url, album):
        self.album_url = album_url
        self.album = album

    def get_movie(self):
        return DoubanMovie(self.album_url, self.album)

    def get_cartoon(self):
        return DoubanCartoon(self.album_url, self.album)

    def get_doco(self):
        return DoubanDoco(self.album_url, self.album)

    def get_tv(self):
        return DoubanTV(self.album_url, self.album)

    def get_variety(self):
        return DoubanVariety(self.album_url, self.album)

    def get_category(self, category):
        tvs = ['电影','美剧','英剧','韩剧','日剧','国产','港剧','动漫','综艺','纪录片']
        if category == '电影':
            return self.get_movie()
        elif category in tvs:
            return self.get_tv()
        elif category == '纪录片':
            return self.get_doco()
        elif category == '动漫':
            return self.get_cartoon()
        elif category == '综艺':
            return self.get_variety()
        else:
            return self.get_movie()



