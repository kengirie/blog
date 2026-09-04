---
title: "Zenn / Nostr / soupault に同時公開するブログを作った"
emoji: "🍜"
type: "tech"
topics: ["nostr", "soupault", "zenn", "githubactions"]
published: false
---

このリポジトリは Markdown 原稿 (`articles/`) を 1 か所で管理し、次の 3 か所へ同時公開します。

1. **Zenn** — GitHub 連携でこのリポジトリの `articles/` がそのまま記事になる
2. **Nostr** — main への push で [snow-actions/nostr](https://github.com/snow-actions/nostr) が kind 30023 (長文記事) を送信
3. **自分のブログ** — [soupault](https://soupault.net/) でビルドして GitHub Pages に公開

`published: true` にして push すると、この記事も 3 か所すべてに公開されます。
