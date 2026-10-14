package com.example.cafe.menu;

import java.util.List;

// TODO: Spring に管理してもらうためのアノテーションを付ける
public class MenuService {
    private final List<MenuItem> items = List.of(
        new MenuItem("ブレンドコーヒー", 480, "ドリンク"),
        new MenuItem("カフェラテ", 520, "ドリンク"),
        new MenuItem("抹茶ラテ", 560, "ドリンク"),
        new MenuItem("チーズケーキ", 450, "フード"),
        new MenuItem("ホットサンド", 650, "フード"),
        new MenuItem("クロワッサン", 320, "フード")
    );

    public List<MenuItem> findAll() {
        return items;
    }

    // 名前が一致する品を返す。なければ MenuNotFoundException を投げる
    public MenuItem findByName(String name) {
        // TODO
        return null;
    }

    // 名前から価格を返す(findByName を使う)
    public int priceOf(String name) {
        // TODO
        return 0;
    }
}
