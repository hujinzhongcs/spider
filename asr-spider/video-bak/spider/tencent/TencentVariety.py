from spider.tencent.TencentVideoCategory import TencentVideoCategory


class TencentVariety(TencentVideoCategory):
    def __init__(self, album_url, album):
        super(TencentVariety, self).__init__(album_url, album)

    # 导演和演员
    def get_directors_and_actors(self):
        roles = self.html.xpath('//div[@class="mod_bd"]/ul[@class="intro_content"]/li[@class="mod_summary intro_item"]/div[@class="director"]//text()')
        if roles and len(roles) > 0:
            parse_results = self.parse_roles(roles)
            self.album.directors = parse_results[0]
            self.album.actors = parse_results[1]

    def parse_roles(self, roles):
        invalid_chars = ['/', '\n', '\xa0\xa0\xa0']
        directors = []
        actors = []
        for role in roles:
            break_flag = False
            for c in invalid_chars:
                if c in role:
                    break_flag = True
            if break_flag:
                continue
            if '嘉宾:' in role:
                continue
            actors.append(role)
        return directors, actors