package com.example.cafe;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

import com.example.cafe.menu.MenuNotFoundException;
import com.example.cafe.menu.MenuService;
import com.example.cafe.order.CheckoutService;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

// w1: Spring が部品を組み立ててくれるか(DI)を確かめる
@SpringBootTest
class CafeServicesTest {
    @Autowired
    MenuService menuService;

    @Autowired
    CheckoutService checkoutService;

    @Autowired
    ShopInfo shopInfo;

    @Test
    @DisplayName("MenuService: 6品のメニューと、名前からの価格")
    void menu() {
        assertEquals(6, menuService.findAll().size());
        assertEquals(520, menuService.priceOf("カフェラテ"));
        assertThrows(MenuNotFoundException.class, () -> menuService.priceOf("カフェモカ"));
    }

    @Test
    @DisplayName("CheckoutService: Spring が渡した割引ルール(千円以上で100円引き)で会計する")
    void checkout() {
        assertEquals(1310, checkoutService.checkout(1410));
        assertEquals(999, checkoutService.checkout(999));
    }

    @Test
    @DisplayName("ShopInfo: 設定ファイルの値を読み込む")
    void shopInfo() {
        assertEquals("ひだまりカフェ", shopInfo.getName());
        assertEquals("8:00-20:00", shopInfo.getHours());
    }
}
