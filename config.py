# 请前往 TMDB 注册 api_key
# https://developer.themoviedb.org/reference
TMDB_API_KEY: str = "your_api_key_here"

# 分类规则 
PATTERN: list = [
    # 特典
    {
        "type": "IV"，
        "regex": r"(?i)(IV|Interview)[ _-]?(\d*)"，
        "normalize": "Interviews/{ani_name} - IV{number:02d}"，
        "priority": 4
    }，
    {
        "type": "SP"，
        "regex": r"(?i)(SP|OVA|EXTRAS|Special|特別編|特别篇|S00E)[ _-]?(\d*)"，
        "normalize": "Other/{ani_name} - SP{number:02d}"，
        "priority": 1
    }，

    # 正片集数
    {
        "type": "SE_EP"，
        "regex": r"(?i)(?:S|Season)[ _-]?(\d+)[ _-]?(?:E|Episode)[ _-]?(\d+)"，
        "normalize": "Season {season:02d}/{ani_name} - S{season:02d}E{number:02d}"，
        "priority": 2
    }，
    {
        "type": "EP"，
        "regex": r"(?i)(?:EP|E|Episode|第)[ _-]?(\d+)"，
        "normalize": "Season {season:02d}/{ani_name} - S{season:02d}E{number:02d}"，
        "priority": 5
    }，
    {
        "type": "EP"，
        "regex": r"(?i)\b(\d{2,3})(?:v\d+)?\.(?:mkv|mp4|mka|ass)"，
        "normalize": "Season {season:02d}/{ani_name} - S{season:02d}E{number:02d}"，
        "priority": 3
    }，
    {
        "type": "EP"，
        "regex": r"(?i)\[(\d{2,3})\].*\.(?:mkv|mp4|mka|ass)"，
        "normalize": "Season {season:02d}/{ani_name} - S{season:02d}E{number:02d}"，
        "priority": 3
    }，

    # CD/BD/DVD（实体介质）
    {
        "type": "CD"，
        "regex": r"(?i)(CD|BD|DVD|DISC|Disk|Vol)[ _-]?(\d*)"，
        "normalize": "Other/{ani_name} - CD{number:02d}"，
        "priority": 4
    }，

    # OP/ED
    {
        "type": "OP/ED"，
        "regex": r"(?i)(OP|ED|NCED\d*_EP\d+|NCOP|NCED)[ _-]?(\d*)"，
        "normalize": "Other/{ani_name} - {raw_match}"，
        "priority": 4
    }，

    # NC
    {
        "type": "NC"，
        "regex": r"(?i)(NC.*EP)(\d*)"，
        "normalize": "Other/{ani_name} - {raw_match}"，
        "priority": 4
    }，

    # 预告类
    {
        "type": "Preview"，
        "regex": r"(?i)(Preview|Prev)[ _-]?(\d*)"，
        "normalize": "Trailers/{ani_name} - Preview{number:02d}"，
        "priority": 4
    }，

    # 宣传片
    {
        "type": "PV"，
        "regex": r"(?i)(PV|Trailer|Teaser)[ _-]?(\d*)"，
        "normalize": "Trailers/{ani_name} - {raw_match}"，
        "priority": 4
    }，

    # 广告
    {
        "type": "CM"，
        "regex": r"(?i)(CM|SPOT)[ _-]?(\d*)"，
        "normalize": "Trailers/{ani_name} - CM{raw_match}"，
        "priority": 4
    }，

    # 菜单
    {
        "type": "Menu"，
        "regex": r"(?i)(Menu)[ _-]?(\d+_\d+|\d+)"，
        "normalize": "Other/{ani_name} - Menu{number:02d}"，
        "priority": 4
    }，

    # 音乐视频
    {
        "type": "MV"，
        "regex": r"(?i)\b(MV)[ _-]?(\d*)"，
        "normalize": "Other/{ani_name} - MV{number:02d}"，
        "priority": 4
    }，

    # Collection
    {
        "type": "Collection"，
        "regex": r"(?i)(CM Collection)[ _-]?(\d*)"，
        "normalize": "Other/{ani_name} - Collection{number:02d}"，
        "priority": 4
    }，
    {
        "type": "Collection"，
        "regex": r"(?i)(PV Collection)[ _-]?(\d*)"，
        "normalize": "Trailers/{ani_name} - Collection{number:02d}"，
        "priority": 4
    }
]

PATTERN.sort(key=lambda x: x['priority'])
