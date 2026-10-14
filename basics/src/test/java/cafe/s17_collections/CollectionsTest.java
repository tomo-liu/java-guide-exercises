package cafe.s17_collections;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

import java.util.List;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

class CollectionsTest {
    private Menu menu() {
        Menu menu = new Menu();
        menu.add("ブレンドコーヒー", 480);
        menu.add("カフェラテ", 520);
        menu.add("チーズケーキ", 450);
        return menu;
    }

    @Test
    @DisplayName("Menu: 名前で価格を引け、ない名前は例外")
    void menuPrice() {
        Menu menu = menu();
        assertEquals(520, menu.priceOf("カフェラテ"));
        assertThrows(IllegalArgumentException.class, () -> menu.priceOf("カフェモカ"));
    }

    @Test
    @DisplayName("Menu: 名前は登録順、同じ名前の add は価格の上書き")
    void menuNames() {
        Menu menu = menu();
        menu.add("カフェラテ", 540);
        assertEquals(List.of("ブレンドコーヒー", "カフェラテ", "チーズケーキ"), menu.names());
        assertEquals(540, menu.priceOf("カフェラテ"));
    }

    @Test
    @DisplayName("Order: 品ごとの注文数・種類・合計")
    void order() {
        Order order = new Order();
        order.add("カフェラテ");
        order.add("チーズケーキ");
        order.add("カフェラテ");
        assertEquals(2, order.count("カフェラテ"));
        assertEquals(0, order.count("ブレンドコーヒー"));
        assertEquals(List.of("カフェラテ", "チーズケーキ"), List.copyOf(order.kinds()));
        assertEquals(1490, order.total(menu()));
    }

    @Test
    @DisplayName("Sorting.byPrice: 安い順、同じ価格なら名前順。元のリストは変えない")
    void byPrice() {
        List<MenuItem> items = List.of(
            new MenuItem("カフェラテ", 520),
            new MenuItem("クロワッサン", 320),
            new MenuItem("チーズケーキ", 450),
            new MenuItem("アイスティー", 450)
        );
        List<MenuItem> sorted = Sorting.byPrice(items);
        assertEquals(List.of("クロワッサン", "アイスティー", "チーズケーキ", "カフェラテ"),
            sorted.stream().map(MenuItem::name).toList());
        assertEquals("カフェラテ", items.get(0).name(), "元のリストは並べ替えない");
    }
}
