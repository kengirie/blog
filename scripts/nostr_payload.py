"""記事ファイルから snow-actions/nostr へ渡す content / tags (NIP-23) を生成する。

GITHUB_OUTPUT が設定されていれば step output として書き出し、
無ければ標準出力に表示する (ローカル確認用)。
"""

import json
import os
import sys
import time
import uuid
from pathlib import Path

import zennmd


def write_output(name, value):
    out_path = os.environ.get("GITHUB_OUTPUT")
    if not out_path:
        print(f"--- {name} ---\n{value}")
        return
    delimiter = f"EOF_{uuid.uuid4().hex}"
    with open(out_path, "a", encoding="utf-8") as f:
        f.write(f"{name}<<{delimiter}\n{value}\n{delimiter}\n")


def main():
    if len(sys.argv) != 2:
        sys.exit("usage: nostr_payload.py <articles/xxx.md>")
    path = Path(sys.argv[1])
    meta, body = zennmd.parse_file(path)
    if meta.get("published") is not True:
        sys.exit(f"{path} is not published: true")

    slug = zennmd.slug_of(path)
    title = meta.get("title", slug)
    published_at = zennmd.first_commit_timestamp(path) or int(time.time())
    tags = [
        ["d", slug],
        ["title", title],
        ["published_at", str(published_at)],
    ]
    for topic in meta.get("topics") or []:
        tags.append(["t", topic])

    write_output("content", body.strip() + "\n")
    write_output("tags", json.dumps(tags, ensure_ascii=False))


if __name__ == "__main__":
    main()
