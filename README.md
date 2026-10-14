# Java解体新書 課題リポジトリ

学習アプリ「Java解体新書」の各カテゴリの最後にある「手元でやってみよう」の課題です。
カフェの注文システムを、変数からSpring BootのWebアプリまで、少しずつ育てていきます。

## 必要なもの

- JDK 25(Eclipse Temurin など)
- VS Code と拡張機能「Extension Pack for Java」

Maven はインストール不要です(各フォルダの `mvnw` が自動で用意します)。

## 構成

| フォルダ | 使う部 | 中身 |
| --- | --- | --- |
| `basics/` | 第1〜3部 | 1つのMavenプロジェクト。課題ごとのパッケージ(`cafe.s01_hello` 〜 `cafe.s19_testing`)と採点テスト |
| `web/w1-spring` 〜 `web/w4-database` | 第4部 | ステップごとのSpring Bootプロジェクト。前のステップの解答が入った状態から始まる |
| `answers/` | 全部 | 解答例(`basics/`・`web/` と同じ構成)。テストが通ってから見比べよう |

## 進め方

1. VS Code で `basics`(第4部は `web/w1-spring` など)のフォルダを開く
2. 課題のファイルの `TODO` を埋める
3. 対応するテストファイルを開き、▶ でテストを実行する。全部緑になれば合格

ターミナルで動かす場合(`basics` の例):

```bash
# Mac / Linux
./mvnw test -Dtest=cafe.s04_conditions.*Test
# Windows(PowerShell)
.\mvnw.cmd test "-Dtest=cafe.s04_conditions.*Test"
```

第4部は、そのステップのフォルダで `./mvnw test`(全テスト)、`./mvnw spring-boot:run`(起動。http://localhost:8080/menu)を使います。

最初の状態では、まだ解いていない課題のテストが失敗します。1つずつ緑にしていきましょう。
