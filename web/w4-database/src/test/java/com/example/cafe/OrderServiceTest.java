package com.example.cafe;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertThrows;

import com.example.cafe.api.OrderRequest;
import com.example.cafe.menu.MenuItem;
import com.example.cafe.menu.MenuItemRepository;
import com.example.cafe.order.CafeOrder;
import com.example.cafe.order.OrderService;
import com.example.cafe.order.OutOfStockException;
import java.util.List;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

// w4: DB(エンティティ・リポジトリ・トランザクション)を確かめる
@SpringBootTest
class OrderServiceTest {
    @Autowired
    OrderService orderService;

    @Autowired
    MenuItemRepository menuItemRepository;

    private int stockOf(String name) {
        return menuItemRepository.findByName(name).orElseThrow().getStock();
    }

    @Test
    @DisplayName("リポジトリ: data.sql のメニューが入っていて、名前や価格で探せる")
    void repository() {
        assertEquals(6, menuItemRepository.count());
        List<String> cheap = menuItemRepository.findByPriceLessThanEqualOrderByPriceAsc(450).stream()
            .map(MenuItem::getName)
            .toList();
        assertEquals(List.of("クロワッサン", "チーズケーキ"), cheap);
    }

    @Test
    @DisplayName("placeOrder: 注文が保存され、在庫が減る")
    void placeOrder() {
        int before = stockOf("ホットサンド");
        CafeOrder order = orderService.placeOrder(List.of(new OrderRequest("ホットサンド", 2)));
        assertNotNull(order.getId(), "保存されると id が振られる");
        assertEquals(1300 - 100, order.getTotal(), "650円×2 = 1300円、千円以上で100円引き");
        assertEquals(1, order.getLines().size());
        assertEquals(before - 2, stockOf("ホットサンド"));
    }

    @Test
    @DisplayName("placeOrder: 途中で在庫切れになったら、全部取り消される(ロールバック)")
    void rollback() {
        int latteBefore = stockOf("カフェラテ");
        assertThrows(OutOfStockException.class, () -> orderService.placeOrder(List.of(
            new OrderRequest("カフェラテ", 1),
            new OrderRequest("クロワッサン", 99)
        )));
        assertEquals(latteBefore, stockOf("カフェラテ"), "先に減らしたカフェラテの在庫も元に戻る");
    }
}
