"""发布文案的用词替换表。

表本身是运营资料，放在 private/social_ops/word_map.json（private/ 在 .gitignore 里，不进仓库）。
没有这个文件时返回空表，文案原样输出。
"""
import json
from pathlib import Path

WORD_MAP_PATH = Path(__file__).resolve().parent.parent / "private" / "social_ops" / "word_map.json"


def load_word_map(kind: str) -> list:
    """kind="regex" 给按正则替换的脚本，kind="plain" 给按原文替换的脚本；返回 [(旧, 新), ...]。"""
    try:
        data = json.loads(WORD_MAP_PATH.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return []
    return [tuple(pair) for pair in data.get(kind, [])]
