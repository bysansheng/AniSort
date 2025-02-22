## AniSort

这是一个批量 **整理番剧视频文件** 的工具，主要适用于 **VCBStudio压制组** 的资源

整理逻辑参考 [mikusa的媒体库管理方案](https://www.himiku.com/archives/how-i-organize-my-animation-library.html)

## 使用方式

* 在命令行中使用
```
python ani_sort.py
D:\anime\xxx
```

* 可在 **ani_sort.py** 的同级目录下进行调用
```python
from ani_sort import AniSort
AniSort("./xxx").move_files()
```

## 整理流程

首先通过 TMDB API 获取元数据对可识别的文件进行格式化重命名

然后采用 PLEX 推荐的分类标准：

| 文件夹  | 包含内容类型                          |
|------------|------------------------------------|
| Interviews | IV（访谈）                          |
| Trailers   | PV / CM / SPOT / Teaser / Trailer  |
| Other      | Menu / NCOP / NCED等               |

对于无法识别的文件（如图片、音乐）将丢到 `Unknown_Files` 目录

## 效果

* 整理前
```bash
[xxx]title/
├── CDs/
│   ├── [xxx]title - CD.mkv
│   └── [xxx]title - CD2.mkv
├── [xxx]title - CM.mkv
├── [xxx]title - PV.mkv
├── [xxx]title - 01.mkv
└── [xxx]title - S01E02.mkv
```

* 整理后
```bash
title (2018)/
├── Other/
│   ├── title (2018) - CD1.mkv
│   └── title (2018) - CD2.mkv
├── Trailers/
│   ├── title (2018) - CM.mkv
│   └── title (2018) - PV.mkv
├── Season 01
│   └── title (2018) - S01E01.mkv
└── └── title (2018) - S01E02.mkv
```

## 配置项

可在 **config.py** 中进行配置的修改

```python
# API配置（必需），需自行注册 tmdb 的 api_key
# https://developer.themoviedb.org/reference
TMDB_API_KEY = "your_api_key_here" 

# 分类规则（可自行编写和添加）
PATTERN = [
    {
        "type": "IV",
        "regex": r"(?i)(IV|Interview|Program|Stage|Talk|Event)(\d*)",
        "normalize": "Interviews/{ani_name} - IV{number:02d}.{file_type}",
        "priority": 4
    },
    ...
]
```

## 反馈与建议

欢迎通过 QQ 1789685745 提交分类规则建议或功能需求
