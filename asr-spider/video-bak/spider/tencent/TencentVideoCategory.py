from lxml import etree
from spider.VideoCategory import VideoCategory


# 腾讯视频分类基类
class TencentVideoCategory(VideoCategory):
    def __init__(self, album_url, album):
        super(TencentVideoCategory, self).__init__(album_url, album)

    def get_album_info(self):
        self.html = etree.HTML(self.get_html(self.album_url))
        self.get_album_name()
        self.get_directors_and_actors()
        self.get_video_tags()
        self.get_play_nums()
        return self.album

    # 标题
    def get_album_name(self):
        player_titles = self.html.xpath('//h2[@class="player_title"]/a/text()')
        if player_titles and len(player_titles) > 0:
            self.album.raw_name = player_titles[0]

    # 导演和演员
    def get_directors_and_actors(self):
        roles = self.html.xpath('//div[@class="mod_bd"]/ul[@class="intro_content"]/li[@class="mod_summary intro_item"]/div[@class="director"]//text()')
        if roles and len(roles) > 0:
            parse_results = self.parse_roles(roles)
            self.album.directors = parse_results[0]
            self.album.actors = parse_results[1]

    # 视频标签
    def get_video_tags(self):
        video_infos = self.html.xpath('//div[@class="video_info"]/div[@class="video_tags _video_tags"]/a/text()')
        if video_infos and len(video_infos) > 0:
            self.album.tags = video_infos

    # 视频播放量
    def get_play_nums(self):
        playnums = self.html.xpath('//em[@id="mod_cover_playnum"]/text()')
        if playnums and len(playnums) > 0:
            self.album.hits = playnums[0]

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
            if '演员:' in role or '嘉宾:' in role:
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