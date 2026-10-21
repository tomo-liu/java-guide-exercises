# Java解体新書 課題リポジトリ

学習アプリ「Java解体新書」の各カテゴリの最後にある「手元でやってみよう」の課題です。
第1〜3部はカフェの注文システムを題材に Java の基礎を、第4〜8部は研修(Day4〜8)と同じ題材(Student・User・MyForm)で Spring Boot を学びます。

## 必要なもの

- JDK 25(Eclipse Temurin など)
- VS Code と拡張機能「Extension Pack for Java」

Maven はインストール不要です(各フォルダの `mvnw` が自動で用意します)。

## 構成

| フォルダ | 使う部 | 中身 |
| --- | --- | --- |
| `basics/` | 第1〜3部 | 1つのMavenプロジェクト。課題ごとのパッケージ(`cafe.s01_hello` 〜 `cafe.s19_testing`)と採点テスト |
| `web/w1-controller` 〜 `web/w4-form` | 第4〜7部 | 研修 Day4〜8 に合わせた Spring Boot プロジェクト(Controller・DI / Entity・DAO・Service / REST API / フォーム)。ファイルの `TODO` を埋める |
| `web/e1-book-arraylist` 〜 `web/e3-signup-form` | 第8部 | 課題文(各フォルダの README.md)だけを読んで、ファイルから自分で作る演習 |
| `answers/` | 全部 | 解答例(`basics/`・`web/` と同じ構成)。テストが通ってから見比べよう |

## 進め方

1. VS Code で `basics`(第4部以降は `web/w1-controller` など)のフォルダを開く
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
