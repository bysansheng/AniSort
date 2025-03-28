# 请前往 TMDB 注册 api_key (32位的那个)
# https://www.themoviedb.org/settings/api
TMDB_API_KEY: str = "your_api_key_here"

# 是否手动选择 TMDB 的搜索结果
TMDB_SELECTED: bool = False

# 是否调用 AI 进行番剧信息解析
CALL_AI: bool = True

# 请前往 DeepSeek 注册 api_key（仅在 CALL_AI 的值为 True 时需要）
# https://platform.deepseek.com/api_keys
AI_API_KEY: str = "your_api_key_here"

# 是否生成对照表
GENERATE_COMPARISON_TABLE: bool = True

# 是否生成 .ignore 文件
GENERATE_IGNORE_FILE: bool = True

# 分类规则 
PATTERN: list = [
    # ova
    {
        "type": "ova",
        "regex": r"(?i)\b(OVA|OAD)(\d*)\b",
        "normalize": None,
        "priority": 1
    },

    # 正片集数
    {
        "type": "SP",
        "regex": r"(?i)S00E[ _-]?(\d+(?:[v|_]\d+){0,1})",
        "normalize": "Season 00/{ani_name} - S00E{match_2}",
        "priority": 1
    },
    {
        "type": "SE_EP",
        "regex": r"(?i)(?:S|Season)[ _-]?(\d+)[ _-]?(?:E|Episode)[ _-]?(\d+(?:[v|_]\d+){0,1})",
        "normalize": "Season {season}/{ani_name} - S{season}E{match_2}",
        "priority": 2
    },
    {
        "type": "EP",
        "regex": r"(?i)\s(\d{2,3}(?:[v|_]\d+){0,1})\s.*\.(?:mkv|mp4|mka|ass)",
        "normalize": "Season {season}/{ani_name} - S{season}E{match_2}",
        "priority": 3
    },
    {
        "type": "EP",
        "regex": r"(?i)\[(\d{2,3}(?:[v|_]\d+){0,1})\].*\.(?:mkv|mp4|mka|ass)",
        "normalize": "Season {season}/{ani_name} - S{season}E{match_2}",
        "priority": 3
    },
    {
        "type": "EP",
        "regex": r"(?i)(?:EP|E|Episode|第)[ _-]?(\d+(?:[v|_]\d+){0,1})",
        "normalize": "Season {season}/{ani_name} - S{season}E{match_2}",
        "priority": 7
    },

    # 菜单
    {
        "type": "Menu",
        "regex": r"(?i)\b(Chapter Menu)[ _-]?(\d+_\d+|\d+){0,1}",
        "normalize": "Other/S{season}_角色菜单{match_2}",
        "priority": 3
    },
    {
        "type": "Menu",
        "regex": r"(?i)\b(Menu)[ _-]?(\d+_\d+|\d+){0,1}",
        "normalize": "Other/S{season}_BD播放选择菜单{match_2}",
        "priority": 4
    },
    
    # 特典
    {
        "type": "IV",
        "regex": r"(?i)\b(IV|Interview)[ _-]?(\d*(?:[v|_]\d+){0,1})",
        "normalize": "Interviews/S{season}_访谈{match_2}",
        "priority": 5
    },
    {
        "type": "SP",
        "regex": r"(?i)\b(SP|OVA|EXTRAS|Special|特別編|特别篇)[ _-]?(\d*(?:[v|_]\d+){0,1})",
        "normalize": "Other/S{season}_特别篇{match_2}",
        "priority": 5
    },

    # CD/BD/DVD（实体介质）
    {
        "type": "CD",
        "regex": r"(?i)\b(CD|BD|DVD|DISC|Disk|Vol)[ _-]?(\d*(?:[v|_]\d+){0,1})",
        "normalize": "Other/S{season}_CD{match_2}",
        "priority": 5
    },

    # OP/ED
    {
        "type": "OP",
        "regex": r"(?i)\b(NCOP(?:\d*_EP\d+){0,1})[ _-]?(\d*(?:[v|_]\d+){0,1})",
        "normalize": "Other/S{season}_无字幕片头{match_2}",
        "priority": 5
    },
    {
        "type": "OP",
        "regex": r"(?i)\b(OP(?:\d*_EP\d+){0,1})[ _-]?(\d*(?:[v|_]\d+){0,1})",
        "normalize": "Other/S{season}_片头{match_2}",
        "priority": 6
    },
    {
        "type": "ED",
        "regex": r"(?i)\b(NCED(?:\d*_EP\d+){0,1})[ _-]?(\d*(?:[v|_]\d+){0,1})",
        "normalize": "Other/S{season}_无字幕片尾{match_2}",
        "priority": 5
    },
    {
        "type": "ED",
        "regex": r"(?i)\b(ED(?:\d*_EP\d+){0,1})[ _-]?(\d*(?:[v|_]\d+){0,1})",
        "normalize": "Other/S{season}_片尾{match_2}",
        "priority": 6
    },

    # 预告类
    {
        "type": "Preview",
        "regex": r"(?i)\b(Preview|Prev)[ _-]?(\d*(?:[v|_]\d+){0,1})",
        "normalize": "Trailers/S{season}_预告{match_2}",
        "priority": 5
    },

    # 音乐视频
    {
        "type": "MV",
        "regex": r"(?i)\b(MV)[ _-]?(\d*(?:[v|_]\d+){0,1})",
        "normalize": "Other/S{season}_MV{match_2}",
        "priority": 5
    },

    # Collection
    {
        "type": "Collection",
        "regex": r"(?i)\b(PV&CM Collection)[ _-]?(\d*(?:[v|_]\d+){0,1})",
        "normalize": "Trailers/S{season}_PV&CM合集{match_2}",
        "priority": 5
    },
    {
        "type": "Collection",
        "regex": r"(?i)\b(CM Collection)[ _-]?(\d*(?:[v|_]\d+){0,1})",
        "normalize": "Other/S{season}_CM合集{match_2}",
        "priority": 5
    },
    {
        "type": "Collection",
        "regex": r"(?i)\b(PV Collection)[ _-]?(\d*(?:[v|_]\d+){0,1})",
        "normalize": "Trailers/S{season}_PV合集{match_2}",
        "priority": 5
    },

    # 广告
    {
        "type": "CM",
        "regex": r"(?i)\b(CM|SPOT)[ _-]?(\d*(?:[v|_]\d+){0,1})",
        "normalize": "Trailers/S{season}_广告{match_2}",
        "priority": 6
    },

    # 宣传片
    {
        "type": "PV",
        "regex": r"(?i)\b(PV|Trailer|Teaser)[ _-]?(\d*(?:[v|_]\d+){0,1})",
        "normalize": "Trailers/S{season}_宣传片{match_2}",
        "priority": 6
    },

    # 保留标签
    {
        "type": "Label",
        "regex": r"(?i)\s(\[.+?(\d*(?:[v|_]\d+){0,1})\])",
        "normalize": "Other/S{season}_{raw_match}",
        "priority": 114514
    }
]

PATTERN.sort(key=lambda x: x['priority'])