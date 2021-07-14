import json

class ResourceObj:
    def __init__(self):
        self.raw_name = ''                         # 原节目名
        self.series_name = list()                  # 原节目名中提取的系列名
        self.items = list()                        # 节目列表
        self.category = ''                         # 类别
        self.directors = set()                     # 导演
        self.actors = set()                        # 演员
        self.roles = set()                         # 角色
        self.tags = set()                          # 标签
        self.period = ''                           # 年代
        self.region = ''                           # 地区
        self.language = ''                         # 语种
        self.source = ''                           # 来源
        self.hits = 0                              # 播放量
        self.url = ''                              # URL
        self.desc = ''                             # 简介
        self.terms = list()                        # 匹配项

    def to_dict(self):
        return {
            'raw_name': self.raw_name,
            'series_name': self.series_name,
            'items': [item.to_dict() for item in self.items],
            'category': self.category,
            'directors': list(self.directors),
            'actors': list(self.actors),
            'roles': list(self.roles),
            'tags': list(self.tags),
            'period': self.period,
            'region': self.region,
            'language': self.language,
            'source': self.source,
            'hits': self.hits,
            'url': self.url,
            'desc': self.desc,
            'terms': self.terms
        }

    def from_dict(self, fields):
        self.raw_name = fields['raw_name']
        self.series_name = fields['series_name']
        self.items = list()
        if fields['items'] and len(fields['items']) > 0:
            for item_dict in fields['items']:
                item = ItemObj('', list(), 0, list())
                item.from_dict(item_dict)
                self.items.append(item)
        self.category = fields['category']
        self.directors = set(fields['directors'])
        self.actors = set(fields['actors'])
        self.roles = set(fields['roles'])
        self.tags = set(fields['tags'])
        if 'period' in fields:
            self.period = fields['period']
        elif 'year' in fields:
            self.period = fields['year']
        else:
            self.period = ''
        self.region = fields['region']
        self.language = fields['language']
        self.hits = fields['hits']
        self.url = fields['url']
        self.desc = fields['desc']
        self.source = fields['source']
        if 'terms' in fields:
            self.terms = fields['terms']
        else:
            self.terms = fields['series_name']

    def to_string(self):
        return json.dumps(self.to_dict(), ensure_ascii=False)


    def from_string(self, json_string):
        json_obj = json.loads(json_string)
        self.from_dict(json_obj)


class ItemObj:
    def __init__(self, rawname, itemname, hits, terms):
        self.raw_name = rawname                         # 节目名
        self.item_name = itemname               # 清洗后节目名，爬取时不需填写
        self.hits = hits
        self.terms = terms                         # 播放量

    def to_dict(self):
        return {
            'raw_name': self.raw_name,
            'item_name': self.item_name,
            'hits': self.hits,
            'terms': self.terms
        }

    def from_dict(self, fields):
        self.raw_name = fields['raw_name']
        self.item_name = fields['item_name']
        self.hits = fields['hits']
        if 'terms' in fields:
            self.terms = fields['terms']
        else:
            self.terms = fields['title_split']

    def to_string(self):
        return json.dumps(self.to_dict(), ensure_ascii=False)

    def from_string(self, json_string):
        json_obj = json.loads(json_string)
        self.from_dict(json_obj)


def load_data(filename):
    lst_album = list()
    with open(filename, 'r', encoding='utf-8') as f_in:
        lines = f_in.readlines()
        for line in lines:
            line = line.strip()
            if not line:
                continue
            album_obj = ResourceObj()
            album_obj.from_string(line)
            lst_album.append(album_obj)
    return lst_album


def write_data(lst_data, filename):
    f_out = open(filename, 'w', encoding='utf-8')
    for album_obj in lst_data:
        f_out.write(album_obj.to_string() + '\n')
    f_out.close()

