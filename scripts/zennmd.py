"""Zenn 形式 (フラットな YAML frontmatter) の Markdown を扱う共通モジュール。

外部ライブラリ非依存。Zenn の frontmatter はフラットな key: value
(topics のみインライン配列) なので、その範囲だけをパースする。
"""

import re
import subprocess
from pathlib import Path

FRONTMATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n?", re.DOTALL)


def parse_file(path):
    """(meta, body) を返す。frontmatter が無ければ meta は空 dict。"""
    text = Path(path).read_text(encoding="utf-8")
    m = FRONTMATTER_RE.match(text)
    if not m:
        return {}, text
    meta = {}
    for line in m.group(1).splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or ":" not in stripped:
            continue
        key, _, value = stripped.partition(":")
        meta[key.strip()] = _parse_value(value.strip())
    return meta, text[m.end():]


def _parse_value(value):
    if value.startswith("[") and value.endswith("]"):
        items = [v.strip().strip('"').strip("'") for v in value[1:-1].split(",")]
        return [v for v in items if v]
    if value in ("true", "false"):
        return value == "true"
    return value.strip('"').strip("'")


def slug_of(path):
    return Path(path).stem


def first_commit_timestamp(path):
    """ファイルが最初にコミットされた unix time。git 履歴に無ければ None。"""
    try:
        out = subprocess.run(
            ["git", "log", "--follow", "--diff-filter=A", "--format=%at", "--", str(path)],
            capture_output=True, text=True, check=True,
        ).stdout.split()
        return int(out[-1]) if out else None
    except (subprocess.CalledProcessError, FileNotFoundError, ValueError):
        return None
