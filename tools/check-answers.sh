#!/usr/bin/env bash
# 解答を入れたときに全テストが通るかを確かめる(リポジトリの管理用)。
#   tools/check-answers.sh
# basics は開始コードに answers を重ねたコピーで、web は answers/web の各ステップで ./mvnw test を実行する。
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

cp -r "$ROOT/basics" "$TMP/basics"
cp -r "$ROOT/answers/basics/src/." "$TMP/basics/src/"
(cd "$TMP/basics" && ./mvnw -q test) && echo "basics: OK"

for step in s1-hello s2-layers s3-crud s4-db s5-errors s6-view e1-book-arraylist e2-book-db e3-signup-form; do
  cp -r "$ROOT/answers/web/$step" "$TMP/$step"
  (cd "$TMP/$step" && ./mvnw -q test) && echo "$step: OK"
done
