from .ani_db.ani_db import AniDBUDPClient

from .config import (
    TMDB_API_KEY,
    PATTERN,
    TMDB_SELECTED,
    GENERATE_COMPARISON_TABLE,
    GENERATE_IGNORE_FILE,
    CALL_AI,
    AI_API_KEY,
    PROXIES,
    DELETE_UNKNOWN_FILES
)

from datetime import datetime
from pathlib import Path
from typing import Union
import difflib
import requests
import shutil
import re

SUFFIX_MAP = {
    "chs": ".zh-CN.forced", "sc": ".zh-CN.forced", "jpsc": ".zh-CN.forced", "scjp": ".zh-CN.forced",
    "cht": ".zh-TW", "tc": ".zh-TW", "jptc": ".zh-TW", "tcjp": ".zh-TW"
}

AI_PROMPT1: str = "请你解析这个番剧文件名，最后只返回番剧对应的名称，不包含季数和标题，也不需要翻译，注意与字幕组区分，例如：[LKSUB][mono][11][1080P].mp4 => mono"
AI_PROMPT2: str = "请你根据我发送的相关信息解析这个番剧文件名，最后只返回番剧的季数对应的阿拉伯数字，默认为 1，注意不要与集数搞混"

ANIDB = AniDBUDPClient()


class AniSort(object):

    def __init__(self, path: Union[str, Path], parent_dir: Union[str, Path] = None) -> None:
        self.path: Path = Path(path.strip('"\'')) if isinstance(path, str) else path

        self.season: int = None
        self.ani_info: dict = self.get_ani_info(self.path.stem)
        self.ani_name: str = f'{self.ani_info["name"]} ({self.ani_info["date"]})'.replace(':', '：').replace('?', '？')
        self.parent_dir: str = f"{str(parent_dir).rstrip('/') if parent_dir else self.path.parent}/{self.ani_name}"

        self.patterns: dict = [{
            **p,
            "regex": re.compile(p["regex"]),
        } for p in PATTERN]

        self.table: dict = {
            str(file): self.normalize(file)
            for file in self.get_all_files(self.path)
        }

    def get_all_files(self, path: Path) -> list:
        """获取文件夹内所有文件
        path: 文件路径
        """
        return sorted(
            [f for f in path.rglob("*") if f.is_file()],
            key=lambda x: difflib.SequenceMatcher(None, str(x), str(path)).ratio(),
            reverse=True
        ) if path.is_dir() else [path]
    
    def call_ai(self, content: str):
        """调用 AI 进行番剧信息解析
        name: 番剧文件名
        """
        try:
            res = requests.post(url="https://api.deepseek.com/chat/completions", headers={
                "Authorization": "Bearer " + AI_API_KEY, "Content-Type": "application/json"
            }, json={
                "model": "deepseek-reasoner", "messages": [{"role": "user", "content": content}]
            }, timeout=None)
            res.raise_for_status()
            return res.json()["choices"][0]["message"]["content"]
        except Exception as e:
            raise Exception(f"连接 DeepSeek 时发生错误：{e}")

    def call_tmdb(self, url: str , params: dict = {}):
        try:
            res = requests.get(url=url, params={
                **params, "language": "zh-CN", "api_key": TMDB_API_KEY
            }, proxies=PROXIES, headers={"accept": "application/json"}, timeout=60)
            res.raise_for_status()
            return res
        except Exception as e:
            raise Exception(f"连接 TMDB 时发生错误：{e}")
    
    def get_ani_info(self, name: str) -> dict:
        """获取番剧的信息
        name: 番剧文件名
        """
        query: str = print("调用 AI - 1") or self.call_ai(f"{name}\n\n{AI_PROMPT1}") if CALL_AI \
            else (match := re.match(r"(?i)(.+?)(?:_s(\d+)){0,1}$", re.sub(r"\s*(\[|\().*?(\]|\))\s*", '', name)))[1]
        res = print("调用 TMDB") or self.call_tmdb(url=f"https://api.themoviedb.org/3/search/tv", params={"query": query})

        try:
            info: dict = res.json()["results"][0]
            if TMDB_SELECTED and res.json()["results"]:
                # 处理是否手动选择 TMDB 的搜索结果
                print("\n" + '\n'.join(
                    f'{i}、{j["name"]} ({j["first_air_date"] if j["first_air_date"] else "None"})'
                    for i, j in enumerate(res.json()["results"])
                ) + "\n")

                if (_input := input("请输入你想选择的结果的序号：")).isdigit():
                    info: dict = res.json()["results"][int(_input)]
        except:
            if not(info := ANIDB.search(name=query)):
                raise Exception("无法在 TMDB 中搜索到该动漫，请更改文件夹名称后再试一次")
            
            info["name"] = info["romaji_name"] or info["kanji_name"] or info["english_name"] or info["other_name"]
            info["first_air_date"] = datetime.fromtimestamp(int(info["air_date"])).year
        
        if CALL_AI:
            seasons_info: list = self.call_tmdb(url=f'https://api.themoviedb.org/3/tv/{info["id"]}').json()["seasons"]
            seasons_conten: list = '\n'.join([
                f'{j["name"]}: {i + 1}'
                for i, j in enumerate(seasons_info[1:] if seasons_info[0]["name"] == "特别篇" else seasons_info)
            ])
            self.season: int = print("调用 AI - 2") or int(self.call_ai(f"{name}\n\n{seasons_conten}\n\n{AI_PROMPT2}"))
        else:
            self.season: int  = int(match[2]) if match[2] else 1
            
        return {
            "name": info["name"],
            "date": info["first_air_date"].split('-')[0] or "年份未知"
        }
    
    def parse(self, name: str) -> dict:
        """解析番剧文件名
        name: 番剧文件名
        """
        for p in self.patterns:
            if match := p["regex"].search(name):
                print(p["regex"].pattern)

                if p["type"] == "SE_EP":
                    season, match_2 = int(match[1]), match[2]
                else:
                    match_2: str = match[1] if p["type"]  == "EP" else match[2] or '1'
                    season: int = self.season
                
                # 处理第0集的情况
                if (match2 := re.match(r"(\d+)(?:[v|_]\d+){0,1}", match_2)) and int(match2[1]) == 0:
                    return None

                return {
                    **p,
                    "season": f"{season:02d}",
                    "match_1": match[1],
                    "match_2": f"{int(match_2):02d}" if match_2.isdigit() else match_2.split('v')[0],
                    "raw_match": match.group(),
                }

        return None

    def normalize(self, path: Path) -> str:
        """获取文件规范化命名
        path: 文件路径
        """
        if (parse_info :=  self.parse(path.name)) and parse_info["normalize"]:
            # 处理字幕文件
            if (suffix := path.suffix) == ".ass":
                suffix: str = SUFFIX_MAP.get(path.stem.split('.')[-1].lower(), '') + suffix

            return f"{self.parent_dir}/" + parse_info["normalize"].format(
                ani_name=self.ani_name,
                raw_match=parse_info["raw_match"].strip(" []") if parse_info["type"] == "Label" else  parse_info["raw_match"],
                season=parse_info["season"],
                match_1=parse_info["match_1"],
                match_2=parse_info["match_2"]
            ) + suffix
        
        return f"{self.parent_dir}/Unknown_Files/{path.name}"
    
    def move_files(self) -> None:
        """移动并重命名所有文件"""
        # 创建所有目标目录
        dest_dirs: dict = {Path(dest).parent for dest in self.table.values()}
        [d.mkdir(parents=True, exist_ok=True) for d in dest_dirs]

        # 批量移动文件
        for src, dest in self.table.items():
            if not(Path(dest).is_file()):
                shutil.move(src, dest)
            else:
                self.table[src] = Path(src).name
            
            print(f"自动整理：{src}\n => {self.table[src]}")

        # 删除原文件（夹）
        unknown_files_path: Path = Path(self.parent_dir) / "Unknown_Files"
        try:
            if self.path.exists():
                if self.get_all_files(self.path):
                    shutil.move(self.path, unknown_files_path / f'{self.path.name}_{datetime.now().strftime("%Y%m%d%H%M%S")}')
                elif self.path.is_dir():
                    shutil.rmtree(self.path)
                else:
                    self.path.unlink()
        except:
            pass

        # 删除未知文件
        if DELETE_UNKNOWN_FILES and unknown_files_path.exists():
            shutil.rmtree(unknown_files_path)

        # 生成 .ignore 文件
        if GENERATE_IGNORE_FILE:
            for root in Path(self.parent_dir).rglob("*/"):
                if root.name in ["Interviews", "Other", "Unknown_Files"]:
                    (root / ".ignore").write_text('', encoding="utf-8")

        # 写入对照表
        if GENERATE_COMPARISON_TABLE:
            with open(f"{self.parent_dir}/Comparison_Table.txt", "a", encoding="utf-8") as file:
                file.write("\n" + "\n\n".join(
                    "{}\n└── {}".format('/'.join(Path(v).parts[-2:]), Path(k).name)
                    for k, v in self.table.items()
                ))


if __name__ == "__main__":
    while True:
        AniSort(input("请输入文件夹路径: ")).move_files()
