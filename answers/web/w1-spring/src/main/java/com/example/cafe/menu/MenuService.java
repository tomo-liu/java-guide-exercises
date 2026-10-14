package com.example.cafe.menu;

import java.util.List;
import org.springframework.stereotype.Service;

@Service
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

    public MenuItem findByName(String name) {
        return items.stream()
            .filter(item -> item.getName().equals(name))
            .findFirst()
            .orElseThrow(() -> new MenuNotFoundException(name));
    }

    public int priceOf(String name) {
        return findByName(name).getPrice();
    }
}
