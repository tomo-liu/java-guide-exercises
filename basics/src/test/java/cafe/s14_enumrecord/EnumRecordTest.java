package cafe.s14_enumrecord;

import static org.junit.jupiter.api.Assertions.assertEquals;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

class EnumRecordTest {
    @Test
    @DisplayName("Size: 追加料金とラベル")
    void size() {
        assertEquals(0, Size.SMALL.extra());
        assertEquals(50, Size.MEDIUM.extra());
        assertEquals(100, Size.LARGE.extra());
        assertEquals("S", Size.SMALL.label());
        assertEquals("M", Size.MEDIUM.label());
        assertEquals("L", Size.LARGE.label());
    }

    @Test
    @DisplayName("OrderLine: (単価+追加料金)× 個数")
    void subtotal() {
        assertEquals(1240, new OrderLine("カフェラテ", 520, Size.LARGE, 2).subtotal());
        assertEquals(480, new OrderLine("ブレンドコーヒー", 480, Size.SMALL, 1).subtotal());
    }

    @Test
    @DisplayName("OrderLine: record なので中身が同じなら equals が true")
    void recordEquality() {
        assertEquals(new OrderLine("カフェラテ", 520, Size.MEDIUM, 1), new OrderLine("カフェラテ", 520, Size.MEDIUM, 1));
    }

    @Test
    @DisplayName("Order.total: 明細の合計")
    void total() {
        OrderLine[] lines = {
            new OrderLine("カフェラテ", 520, Size.LARGE, 2),
            new OrderLine("抹茶ラテ", 560, Size.MEDIUM, 1),
        };
        assertEquals(1850, Order.total(lines));
        assertEquals(0, Order.total(new OrderLine[] {}));
    }
}
