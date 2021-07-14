from spider.tencent.TencentVideoCategory import TencentVideoCategory


class TencentCartoon(TencentVideoCategory):
    def __init__(self, album_url, album):
        super(TencentCartoon, self).__init__(album_url, album)


