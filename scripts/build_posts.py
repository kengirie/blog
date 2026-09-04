"""articles/*.md (Zenn 形式) から soupault 用の site/posts/*.md を生成する。

- published: true の記事だけを対象にする
- frontmatter を除去し、タイトル (h1) と日付 (<time>) を注入する
- images/ があれば site/images/ にコピーする
"""

import datetime
import shutil
import sys
from pathlib import Path

import zennmd

ROOT = Path(__file__).resolve().parent.parent
ARTICLES = ROOT / "articles"
POSTS = ROOT / "site" / "posts"
IMAGES = ROOT / "images"
SITE_IMAGES = ROOT / "site" / "images"


def post_date(path):
    ts = zennmd.first_commit_timestamp(path)
    if ts is None:
        return datetime.date.today().isoformat()
    return datetime.datetime.fromtimestamp(ts, tz=datetime.timezone.utc).date().isoformat()


def main():
    if POSTS.exists():
        shutil.rmtree(POSTS)
    POSTS.mkdir(parents=True)

    count = 0
    for article in sorted(ARTICLES.glob("*.md")):
        meta, body = zennmd.parse_file(article)
        if meta.get("published") is not True:
            continue
        date = post_date(article)
        title = meta.get("title", article.stem)
        topics = meta.get("topics") or []
        topic_html = " ".join(f'<span class="topic">{t}</span>' for t in topics)
        out = (
            f"# {title}\n\n"
            f'<p class="post-meta"><time datetime="{date}">{date}</time> {topic_html}</p>\n\n'
            f"{body}"
        )
        (POSTS / article.name).write_text(out, encoding="utf-8")
        count += 1

    if IMAGES.is_dir():
        shutil.rmtree(SITE_IMAGES, ignore_errors=True)
        shutil.copytree(IMAGES, SITE_IMAGES)

    print(f"generated {count} post(s) in {POSTS}", file=sys.stderr)


if __name__ == "__main__":
    main()
