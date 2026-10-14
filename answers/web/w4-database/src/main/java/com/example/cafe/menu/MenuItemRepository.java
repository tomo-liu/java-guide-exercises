package com.example.cafe.menu;

import java.util.List;
import java.util.Optional;
import org.springframework.data.jpa.repository.JpaRepository;

// メソッドの名前から、Spring Data JPA が SQL を組み立ててくれる
public interface MenuItemRepository extends JpaRepository<MenuItem, Long> {
    Optional<MenuItem> findByName(String name);

    List<MenuItem> findByPriceLessThanEqualOrderByPriceAsc(int price);
}
