package cafe.s15_design;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

class DesignTest {
    private final Priced latte = new Item("カフェラテ", 520);
    private final Priced sandwich = new Item("ホットサンド", 650);

    @Test
    @DisplayName("LunchSet: 名前と、100円引きの価格")
    void lunchSet() {
        LunchSet set = new LunchSet(latte, sandwich);
        assertEquals("カフェラテとホットサンドのセット", set.getName());
        assertEquals(1070, set.getPrice());
    }

    @Test
    @DisplayName("LunchSet: 継承ではなく合成で作る(Item などを継承しない)")
    void lunchSetUsesComposition() {
        assertEquals(Object.class, LunchSet.class.getSuperclass(), "LunchSet は他のクラスを extends しない");
        assertFalse(Item.class.isAssignableFrom(LunchSet.class));
    }

    @Test
    @DisplayName("Order: セットもふつうの品と同じように合計できる")
    void orderTotal() {
        Order order = new Order(new Priced[] {new LunchSet(latte, sandwich), new Item("クロワッサン", 320)});
        assertEquals(1390, order.total());
    }

    @Test
    @DisplayName("ReceiptPrinter: 1品ずつの行と合計の行")
    void receipt() {
        Order order = new Order(new Priced[] {latte, new Item("チーズケーキ", 450)});
        assertEquals("カフェラテ 520円\nチーズケーキ 450円\n合計 970円", new ReceiptPrinter().print(order));
    }

    @Test
    @DisplayName("ReceiptPrinter: 合計は Order の total() の結果を使う")
    void receiptUsesOrderTotal() {
        Order discounted = new Order(new Priced[] {latte}) {
            @Override
            public int total() {
                return 500;
            }
        };
        assertEquals("カフェラテ 520円\n合計 500円", new ReceiptPrinter().print(discounted));
    }
}
