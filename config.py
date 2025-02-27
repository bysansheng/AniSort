# 请前往 TMDB 注册 api_key (32位的那个)
# https://www.themoviedb.org/settings/api
TMDB_API_KEY: str = "your_api_key_here"

# 是否手动选择 TMDB 的搜索结果
TMDB_SELECTED: bool = False

# 是否生成对照表
GENERATE_COMPARISON_TABLE: bool = True

# 是否生成 .ignore 文件
GENERATE_IGNORE_FILE: bool = False

# 分类规则 
PATTERN: list = [
    # 特典
    {
        "type": "IV",
        "regex": r"(?i)(IV|Interview)[ _-]?(\d*(?:v\d+){0,1})",
        "normalize": "Interviews/{ani_name} - IV{match2}",
        "priority": 4
    },
    {
        "type": "SP",
        "regex": r"(?i)(SP|OVA|EXTRAS|Special|特別編|特别篇)[ _-]?(\d*(?:v\d+){0,1})",
        "normalize": "Other/SP{match2}",
        "priority": 1
    },

    # 正片集数
    {
        "type": "SE_EP",
        "regex": r"(?i)(?:S|Season)[ _-]?(\d+)[ _-]?(?:E|Episode)[ _-]?(\d+(?:v\d+){0,1})",
        "normalize": "Season {season}/{ani_name} - S{season}E{match2}",
        "priority": 2
    },
    {
        "type": "EP",
        "regex": r"(?i)(?:EP|E|Episode|第)[ _-]?(\d+(?:v\d+){0,1})",
        "normalize": "Season {season}/{ani_name} - S{season}E{match2}",
        "priority": 5
    },
    {
        "type": "EP",
        "regex": r"(?i)\b(\d{2,3}(?:v\d+))?\.(?:mkv|mp4|mka|ass)",
        "normalize": "Season {season}/{ani_name} - S{season}E{match2}",
        "priority": 3
    },
    {
        "type": "EP",
        "regex": r"(?i)\[(\d{2,3}(?:v\d+))\].*\.(?:mkv|mp4|mka|ass)",
        "normalize": "Season {season}/{ani_name} - S{season}E{match2}",
        "priority": 3
    },
    {
        "type": "SP",
        "regex": r"(?i)S00E[ _-]?(\d+(?:v\d+){0,1})",
        "normalize": "Season 00/{ani_name} - S00E{match2}",
        "priority": 1
    },

    # 菜单
    {
        "type": "Menu",
        "regex": r"(?i)(Menu)[ _-]?(\d+_\d+|\d+)",
        "normalize": "Other/Menu{match2}",
        "priority": 3
    },
    
    # CD/BD/DVD（实体介质）
    {
        "type": "CD",
        "regex": r"(?i)(CD|BD|DVD|DISC|Disk|Vol)[ _-]?(\d*(?:v\d+){0,1})",
        "normalize": "Other/CD{match2}",
        "priority": 4
    },

    # OP/ED
    {
        "type": "OP/ED",
        "regex": r"(?i)(OP|ED|NCED\d*_EP\d+|NCOP|NCED)[ _-]?(\d*(?:v\d+){0,1})",
        "normalize": "Other/{raw_match}",
        "priority": 4
    },

    # NC
    {
        "type": "NC",
        "regex": r"(?i)(NC.*EP)(\d*(?:v\d+){0,1})",
        "normalize": "Other/{raw_match}",
        "priority": 4
    },

    # 预告类
    {
        "type": "Preview",
        "regex": r"(?i)(Preview|Prev)[ _-]?(\d*(?:v\d+){0,1})",
        "normalize": "Trailers/{ani_name} - Preview{match2}",
        "priority": 4
    },

    # 宣传片
    {
        "type": "PV",
        "regex": r"(?i)(PV|Trailer|Teaser)[ _-]?(\d*(?:v\d+){0,1})",
        "normalize": "Trailers/{ani_name} - {raw_match}",
        "priority": 4
    },

    # 广告
    {
        "type": "CM",
        "regex": r"(?i)(CM|SPOT)[ _-]?(\d*(?:v\d+){0,1})",
        "normalize": "Trailers/{ani_name} - CM{raw_match}",
        "priority": 4
    },

    # 音乐视频
    {
        "type": "MV",
        "regex": r"(?i)\b(MV)[ _-]?(\d*(?:v\d+){0,1})",
        "normalize": "Other/MV{match2}",
        "priority": 4
    },

    # Collection
    {
        "type": "Collection",
        "regex": r"(?i)(CM Collection)[ _-]?(\d*(?:v\d+){0,1})",
        "normalize": "Other/Collection{match2}",
        "priority": 4
    },
    {
        "type": "Collection",
        "regex": r"(?i)(PV Collection)[ _-]?(\d*(?:v\d+){0,1})",
        "normalize": "Trailers/{ani_name} - Collection{match2}",
        "priority": 4
    },

    # 保留标签
    {
        "type": "Label",
        "regex": r"(?i)\s(\[.+?(\d*(?:v\d+){0,1})\])",
        "normalize": "Other/{raw_match}",
        "priority": 114514
    }
]

PATTERN.sort(key=lambda x: x['priority'])