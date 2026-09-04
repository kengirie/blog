# blog

Markdown 原稿 (`articles/`) を 1 か所で管理し、3 か所へ同時公開するリポジトリ。

| 出力先 | 仕組み |
| --- | --- |
| [Zenn](https://zenn.dev/) | GitHub 連携が `articles/` を直接読む |
| Nostr (kind 30023, NIP-23) | main への push で [snow-actions/nostr](https://github.com/snow-actions/nostr) が送信 ([nostr.yml](.github/workflows/nostr.yml)) |
| 自分のブログ (GitHub Pages) | [soupault](https://soupault.net/) でビルドしてデプロイ ([deploy.yml](.github/workflows/deploy.yml)) |

## 仕組み

```
articles/*.md (Zenn 形式 frontmatter が正)
   ├─→ Zenn連携がそのまま記事として取り込む
   ├─→ scripts/build_posts.py → site/posts/*.md → soupault → build/ → GitHub Pages
   └─→ scripts/changed_articles.py → scripts/nostr_payload.py → snow-actions/nostr (kind 30023)
```

- `published: true` の記事だけがブログ / Nostr に公開される
- Nostr の `d` タグ = ファイル名 (slug)。記事を編集して push すると Nostr 側も同じ記事が更新される (replaceable event)
- `published_at` タグと記事の日付には、そのファイルの初回コミット日時を使う (更新しても変わらない)

## 初回セットアップ

1. **Zenn 連携**: [Zenn のデプロイ設定](https://zenn.dev/dashboard/deploys) でこのリポジトリを連携する
2. **Nostr の Secret / Variable** をリポジトリに設定する (Settings → Secrets and variables → Actions)
   - Secret `NOSTR_PRIVATE_KEY`: 秘密鍵 (nsec または hex)。**必ず自分で設定すること**
   - Variable `NOSTR_RELAYS`: 改行区切りのリレー URL。例:
     ```
     wss://relay.damus.io
     wss://nos.lol
     wss://yabu.me
     ```
   - 未設定の間、Nostr workflow は警告を出してスキップする (失敗はしない)
3. **GitHub Pages**: 初回の deploy workflow が自動で有効化する (Settings → Pages で Source が "GitHub Actions" になっていることを確認)

## 記事を書く

```sh
make new slug=my-article-slug   # zenn-cli で新規記事 (slug は 12〜50 文字, a-z0-9-_)
make preview                    # Zenn プレビュー (localhost:8000)
```

frontmatter は Zenn 形式:

```yaml
---
title: "記事タイトル"
emoji: "😸"
type: "tech"
topics: ["nostr", "soupault"]
published: false   # true にして push すると 3 か所に公開される
---
```

公開は `published: true` にして main へ push するだけ。

## ローカルでブログをビルドする

soupault のバイナリを [Releases](https://github.com/PataphysicalSociety/soupault/releases) から取得して PATH に置くか、`SOUPAULT=/path/to/soupault` を指定する。

```sh
make build   # articles/ → site/posts/ → build/
make serve   # localhost:8000 で確認
```

## 注意点

- Zenn 独自記法 (`:::message` など) は soupault / Nostr ではそのまま表示される。3 か所で共通に見せたい記事は素の CommonMark で書くのが安全
- 画像はリポジトリ直下の `images/` に置く (Zenn の仕様)。ビルド時に `site/images/` へコピーされるが、記事中のパス `/images/...` は Pages では `https://kengirie.github.io/blog/images/...` に絶対リンク化される
- Nostr へは「その push で追加・変更された `published: true` の記事」だけが送られる。任意の記事を再送信したい場合は Actions の "Publish to Nostr" を workflow_dispatch で実行し、ファイルパスを指定する
