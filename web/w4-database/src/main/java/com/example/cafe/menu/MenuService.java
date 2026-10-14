package com.example.cafe.menu;

import java.util.List;
import org.springframework.stereotype.Service;

// TODO: メニューを List で持つのをやめ、MenuItemRepository(DB)から読むように書き換える
//   - コンストラクタで MenuItemRepository を受け取る
//   - findAll は id の順(repository.findAll(Sort.by("id")))
//   - findByName は repository.findByName(name) を使い、なければ MenuNotFoundException
@Service
public class MenuService {
    private final List<MenuItem> items = List.of();

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
