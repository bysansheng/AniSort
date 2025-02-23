from pathlib import Path
from typing import Union
import requests
import shutil
import os
import re

from config import TMDB_API_KEY, PATTERN


class AniSort(object):

    def __init__(self, path: Union[Path, str]) -> None:
        self.patterns = self.compile_patterns()
        self.path: Path = path if isinstance(path, Path) else Path(path)
        self.ani_info: dict = self.get_ani_info(self.path.name)
        self.ani_name: str = f'{self.ani_info["name"]} ({self.ani_info["date"]})'
        self.table: dict = {
            str(file): self.normalize(file)
            for file in self.get_all_files(self.path)
        }

    def compile_patterns(self) -> dict:
        """预编译正则表达式"""
        return [{
            "type": p["type"],
            "regex": re.compile(p["regex"]),
            "normalize": p["normalize"]
        } for p in PATTERN]

    def get_all_files(self, path: Path) -> list:
        """获取文件夹内所有文件
        path: 文件路径
        """
        return [f for f in self.path.rglob("*") if f.is_file()]
    
    def get_ani_info(self, name: str) -> dict:
        """获取番剧的信息
        name: 要查询的番剧的名称
        """
        try:
            res = requests.get("https://api.themoviedb.org/3/search/tv", params={
                "query": re.sub(r"\s*(\[|\().*?(\]|\))\s*", '', name), "language": "zh-CN"
            }, headers={
                "Authorization": f"Bearer {TMDB_API_KEY}",
                "accept": "application/json"
            }, timeout=None)
            res.raise_for_status()
        except:
            raise ValueError("无法连接到 TMDB，请更换网络环境后再试一次")

        try:
            info: dict = res.json()["results"][0]
        except:
            raise ValueError("无法在 TMDB 中搜索到该动漫，请更改文件夹名称后再试一次")
        
        return {
            "name": info["name"],
            "date": info["first_air_date"].split('-')[0] if info["first_air_date"] else "年份位置"
        }
    
    def parse(self, name: str) -> dict:
        """解析番剧文件名
        name: 番剧文件名
        """
        for p in self.patterns:
            if match := p["regex"].search(name):
                p_type: str = p["type"]
                season: int = 1
                number: int = None

                if p_type  == "EP":
                    number: int = match.group(1)
                elif p_type == "SE_EP":
                    season: int = int(match.group(1))
                    number: int = match.group(2)
                else:
                    # 特殊处理无数字的 SP/OP 等情况（如 "SP.mkv"）
                    number: int = match.group(2) or match.group(1)
                return {
                    "type": p_type,
                    "season": season,
                    "number": int(number) if number and number.isdigit() else 0,
                    "raw_match": match.group(),
                    "normalize": p["normalize"],
                }
            
        return None

    def normalize(self, path: Path) -> str:
        """获取文件规范化命名
        path: 文件路径
        """
        if (parse_info :=  self.parse(path.name)) and parse_info["normalize"]:
            # 处理字幕文件
            if (suffix := path.suffix) == ".ass":
                lang: str = path.name.split('.')[-2]
                if lang in ['chs', 'sc', 'JPSC']:
                    suffix = '.zh-CN.forced.ass'
                elif lang in ['cht', 'tc', 'JPTC']:
                    suffix = '.zh-TW.ass'

            return f"./{self.ani_name}/" + parse_info["normalize"].format(
                ani_name=self.ani_name,
                season=parse_info["season"],
                number=parse_info["number"],
                raw_match=parse_info['raw_match'],
            ) + suffix

        return f"./{self.ani_name}/Unknown_Files/{path.name}"
    
    def move_files(self) -> None:
        """移动并重命名所有文件"""
        # 创建所有目标目录
        dest_dirs = {os.path.dirname(dest) for dest in self.table.values()}
        for d in dest_dirs:
            os.makedirs(d, exist_ok=True)

        # 批量移动文件
        for src, dest in self.table.items():
            if not(os.path.isfile(dest)):
                shutil.move(src, dest)
    
        # 删除原文件夹
        if self.get_all_files(self.path):
            shutil.move(self.path, f"./{self.ani_name}/Unknown_Files")
        else:
            shutil.rmtree(self.path)

        # 写入对照表
        with open(f"./{self.ani_name}/Comparison_Table.txt", "w", encoding="utf-8") as file:
            file.write("\n\n".join(
                "{}\n└── {}".format('/'.join(Path(v).parts[-2:]), Path(k).name)
                for k, v in self.table.items()
            ))


if __name__ == "__main__":
    AniSort(input("请输入文件夹路径: ")).move_files()