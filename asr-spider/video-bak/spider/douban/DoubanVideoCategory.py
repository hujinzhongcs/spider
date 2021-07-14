from spider.VideoCategory import VideoCategory


# 视频分类基类
class DoubanVideoCategory(VideoCategory):
    def __init__(self, album_url, album):
        super(DoubanVideoCategory, self).__init__(album_url, album)

    # 标题
    def get_album_name(self):
        # titles = self.html.xpath('//h1/span[@property="v:itemreviewed"]/text()')
        titles = self.html.xpath('//head/title/text()')
        if titles and len(titles) > 0:
            self.album.raw_name = titles[0].replace('(豆瓣)', '').replace('\n', '').strip()

    # 年份
    def get_year(self):
        years = self.html.xpath('//h1/span[@class="year"]/text()')
        if years and len(years) > 0:
            self.album.period = years[0][1:5]

    # 导演
    def get_directors(self):
        directors = self.html.xpath('//div[@id="info"]/span/span/a[@rel="v:directedBy"]/text()')
        if directors and len(directors) > 0:
            self.album.directors = directors

    # 演员
    def get_actors(self):
        actors = self.html.xpath('//div[@id="info"]/span/span/a[@rel="v:starring"]/text()')
        if actors and len(actors) > 0:
            self.album.actors = actors

    # 视频标签
    def get_video_tags(self):
        tags = self.html.xpath('//div[@id="info"]/span[@property="v:genre"]/text()')
        if tags and len(tags) > 0:
            self.album.tags = tags

    # 地区
    def get_region(self):
        info = self.html.xpath('//div[@id="info"]//text()')
        if info and len(info) > 0:
            region_index = info.index('制片国家/地区:')
            self.album.region = info[region_index + 1].strip()

    # 语言
    def get_language(self):
        info = self.html.xpath('//div[@id="info"]//text()')
        if info and len(info) > 0:
            lan_index = info.index('语言:')
            self.album.language = info[lan_index + 1].strip()

    # 视频播放量
    def get_play_nums(self):
        voite = self.html.xpath('//div[@class="rating_sum"]/a/span[@property="v:votes"]/text()')
        if voite and len(voite) > 0:
            self.album.hits = voite[0]
