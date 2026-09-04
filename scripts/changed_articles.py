"""push で変更された articles/*.md のうち published: true のものを matrix JSON で出力する。

GitHub Actions から環境変数で受け取る:
- BEFORE / AFTER: push イベントのコミット SHA。BEFORE が全ゼロ (初回 push) なら全記事を対象にする
- INPUT_FILE: workflow_dispatch で指定された記事ファイル (指定時はそれだけを対象にする)
"""

import json
import os
import subprocess
import sys

import zennmd

ZERO_SHA = "0" * 40


def changed_files():
    input_file = os.environ.get("INPUT_FILE", "").strip()
    if input_file:
        return [input_file]
    before = os.environ.get("BEFORE", "")
    after = os.environ.get("AFTER", "HEAD")
    if not before or before == ZERO_SHA:
        out = subprocess.run(
            ["git", "ls-files", "articles/*.md"],
            capture_output=True, text=True, check=True,
        ).stdout
    else:
        out = subprocess.run(
            ["git", "diff", "--name-only", "--diff-filter=AM",
             f"{before}..{after}", "--", "articles/*.md"],
            capture_output=True, text=True, check=True,
        ).stdout
    return [line for line in out.splitlines() if line.endswith(".md")]


def main():
    targets = []
    for path in changed_files():
        if not os.path.isfile(path):
            continue
        meta, _ = zennmd.parse_file(path)
        if meta.get("published") is True:
            targets.append(path)

    files_json = json.dumps(targets)
    print(f"changed published articles: {files_json}", file=sys.stderr)
    lines = f"files={files_json}\ncount={len(targets)}\n"
    out_path = os.environ.get("GITHUB_OUTPUT")
    if out_path:
        with open(out_path, "a", encoding="utf-8") as f:
            f.write(lines)
    else:
        print(lines, end="")


if __name__ == "__main__":
    main()
