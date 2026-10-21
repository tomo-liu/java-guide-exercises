# Java解体新書 課題リポジトリ

学習アプリ「Java解体新書」の各カテゴリの最後にある「手元でやってみよう」の課題です。
第1〜3部はカフェの注文システムを題材に Java の基礎を、第4・5部はユーザー管理アプリ(User)を1つ育てながら Spring Boot を学びます(第4部から始めても大丈夫です)。

## 必要なもの

- JDK 25(Eclipse Temurin など)
- VS Code と拡張機能「Extension Pack for Java」

Maven はインストール不要です(各フォルダの `mvnw` が自動で用意します)。

## 構成

| フォルダ | 使う部 | 中身 |
| --- | --- | --- |
| `basics/` | 第1〜3部 | 1つのMavenプロジェクト。課題ごとのパッケージ(`cafe.s01_hello` 〜 `cafe.s19_testing`)と採点テスト |
| `web/s1-hello` 〜 `web/s6-view` | 第4・5部 | 同じ User アプリを育てるステップ。各ステップは前のステップの解答が入った状態から始まる(s1 文字を返す/s2 層をつくる/s3 CRUD 5つの操作/s4 DB につなぐ/s5 入力チェックと検索/s6 画面とフォーム) |
| `web/e1-book-arraylist` 〜 `web/e3-signup-form` | 第5部 | 課題文(各フォルダの README.md)だけを読んで、ファイルから自分で作る演習 |
| `answers/` | 全部 | 解答例(`basics/`・`web/` と同じ構成)。テストが通ってから見比べよう |

## 進め方

1. VS Code で `basics`(第4部以降は `web/s1-hello` など)のフォルダを開く
2. 課題のファイルの `TODO` を埋める
3. 対応するテストファイルを開き、▶ でテストを実行する。全部緑になれば合格

ターミナルで動かす場合(`basics` の例):

```bash
# Mac / Linux
./mvnw test -Dtest=cafe.s04_conditions.*Test
# Windows(PowerShell)
.\mvnw.cmd test "-Dtest=cafe.s04_conditions.*Test"
```

`web/` の各フォルダでは `./mvnw test`(全テスト)、`./mvnw spring-boot:run`(起動。http://localhost:8080/ …)を使います。
DB は H2(アプリと一緒に動くメモリの DB)を使うので、インストールは要りません。研修の MariaDB の設定例は、`application.properties` のコメントにあります。

最初の状態では、まだ解いていない課題のテストが失敗します。1つずつ緑にしていきましょう。
