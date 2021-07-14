from spider.tencent.TencentCartoon import TencentCartoon
from spider.tencent.TencentChild import TencentChild
from spider.tencent.TencentDoco import TencentDoco
from spider.tencent.TencentMovie import TencentMovie
from spider.tencent.TencentTV import TencentTV
from spider.tencent.TencentVariety import TencentVariety


class TencentCategoryFactory(object):
    def __init__(self, album_url, album):
        self.album_url = album_url
        self.album = album

    def get_movie(self):
        return TencentMovie(self.album_url, self.album)

    def get_cartoon(self):
        return TencentCartoon(self.album_url, self.album)

    def get_child(self):
        return TencentChild(self.album_url, self.album)

    def get_doco(self):
        return TencentDoco(self.album_url, self.album)

    def get_tv(self):
        return TencentTV(self.album_url, self.album)

    def get_variety(self):
        return TencentVariety(self.album_url, self.album)

    def get_category(self, category):
        if category == '电影':
            return self.get_movie()
        elif category == '电视剧':
            return self.get_tv()
        elif category == '纪录片':
            return self.get_doco()
        elif category == '动漫':
            return self.get_cartoon()
        elif category == '综艺':
            return self.get_variety()
        elif category == '儿童':
            return self.get_child()
