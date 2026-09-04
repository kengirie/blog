SOUPAULT ?= soupault

.PHONY: build build-live serve clean preview new

# ローカル用ビルド (リンクはルート相対のまま)
build:
	python3 scripts/build_posts.py
	$(SOUPAULT)

# 本番相当ビルド (GitHub Pages の URL 起点の絶対リンクに書き換え)
build-live:
	python3 scripts/build_posts.py
	$(SOUPAULT) --profile live

serve: build
	python3 -m http.server 8000 --directory build

clean:
	rm -rf build site/posts site/images .soupault-cache

# Zenn のローカルプレビュー
preview:
	npx zenn-cli preview

# 新規記事: make new slug=my-article-slug (12〜50 文字, a-z0-9-_)
new:
	npx zenn-cli new:article --slug $(slug)
