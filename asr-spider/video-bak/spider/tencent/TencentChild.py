from spider.tencent.TencentVideoCategory import TencentVideoCategory


class TencentChild(TencentVideoCategory):
    def __init__(self, album_url, album):
        super(TencentChild, self).__init__(album_url, album)

