## AniSort

这是一个批量 **整理番剧文件** 的工具，通过正则表达式进行匹配

整理逻辑参考 [mikusa的媒体库管理方案](https://www.himiku.com/archives/how-i-organize-my-animation-library.html)

## 使用方式

* 在命令行中使用
```
python ani_sort.py
请输入文件夹路径: D:\anime\xxx

python ani_sort.py
请输入文件夹路径: ./anime/xxx
```

* 可在 **ani_sort.py** 的同级目录下进行调用
```python
from ani_sort import AniSort
AniSort("./xxx").move_files()
```

## 整理流程

首先通过 **TMDB API** 与 **原文件夹的名称** 获取番剧信息

Ps：可在文件夹后面添加数字来指明 Season，例如 **[xxx] 赛马娘2 [1080p]**

再根据元数据对可识别的文件进行格式化重命名

然后采用 PLEX 推荐的分类标准进行分类：

| 文件夹     | 包含内容类型                      |
|------------|------------------------------------|
| Interviews | IV（访谈）                         |
| Trailers   | PV / CM / SPOT / Teaser / Trailer  |
| Other      | Menu / NCOP / NCED 等              |

最后会将所有文件移动到 **新文件夹** 内

并且会在 **新文件夹** 内生成 **Comparison_Table.txt**

该文本内写入了所有文件更改前后的名称，可以对照是否有识别错误

```txt
Season 01/title (2018) - S01E01.mkv
└── [xxx]title - 01.mkv

Season 01/title (2018) - S01E02.mkv
└── [xxx]title - S01E02.mkv
```

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
├── Season 01/
│   └── title (2018) - S01E01.mkv
└── └── title (2018) - S01E02.mkv
└── Comparison_Table.txt
```

## 配置项

可在 **config.py** 中进行配置的修改

```python
# 请前往 TMDB 注册 api_key (32位的那个)
# https://www.themoviedb.org/settings/api
TMDB_API_KEY = "your_api_key_here"

# 是否手动选择 TMDB 的搜索结果
TMDB_SELECTED: bool = True

# 是否生成对照表
GENERATE_COMPARISON_TABLE: bool = True

# 是否生成 .ignore 文件
GENERATE_IGNORE_FILE: bool = False

# 分类规则（可自行编写和添加）
PATTERN = [
    {
        "type": "IV",
        "regex": r"(?i)(IV|Interview)[ _-]?(\d*(?:v\d+))",
        "normalize": "Interviews/{ani_name} - IV{match2}",
        "priority": 4
    },
    ...
]
```

## 反馈与建议

如要提供分类规则建议或功能需求，可以来找 qq1789685745
