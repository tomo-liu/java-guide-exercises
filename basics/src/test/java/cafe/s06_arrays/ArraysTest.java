package cafe.s06_arrays;

import static org.junit.jupiter.api.Assertions.assertEquals;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

class ArraysTest {
    private final int[] prices = {480, 520, 560, 450, 650, 320};
    private final String[] names = {"ブレンドコーヒー", "カフェラテ", "抹茶ラテ", "チーズケーキ", "ホットサンド", "クロワッサン"};

    @Test
    @DisplayName("total: 6品の合計")
    void total() {
        assertEquals(2980, Order.total(prices));
    }

    @Test
    @DisplayName("max: 最高値")
    void max() {
        assertEquals(650, Order.max(prices));
        assertEquals(320, Order.max(new int[] {320}), "1品だけのとき");
        assertEquals(480, Order.max(new int[] {480, 320}), "先頭が最大のとき");
    }

    @Test
    @DisplayName("countAtLeast: しきい値以上の数(ちょうども含む)")
    void countAtLeast() {
        assertEquals(3, Order.countAtLeast(prices, 500));
        assertEquals(4, Order.countAtLeast(prices, 480), "480円ちょうども数える");
        assertEquals(0, Order.countAtLeast(prices, 1000));
    }

    @Test
    @DisplayName("indexOf: 名前の位置。なければ-1")
    void indexOf() {
        assertEquals(0, Order.indexOf(names, "ブレンドコーヒー"));
        assertEquals(3, Order.indexOf(names, "チーズケーキ"));
        assertEquals(-1, Order.indexOf(names, "カフェモカ"));
        // == で比べると見つからない、実行中に作った文字列でも探せること
        String latte = "カフェ" + "ラテ".repeat(1);
        assertEquals(1, Order.indexOf(names, latte), "文字列は equals で比べる");
    }
}
