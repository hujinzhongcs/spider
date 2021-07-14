from spider.tencent.TencentVideoCategory import TencentVideoCategory


class TencentTV(TencentVideoCategory):
    def __init__(self, album_url, album):
        super(TencentTV, self).__init__(album_url, album)

