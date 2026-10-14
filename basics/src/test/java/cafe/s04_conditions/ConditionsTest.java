package cafe.s04_conditions;

import static org.junit.jupiter.api.Assertions.assertEquals;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

class ConditionsTest {
    @Test
    @DisplayName("taxRate: 持ち帰りは8、店内は10")
    void taxRate() {
        assertEquals(8, Register.taxRate(true));
        assertEquals(10, Register.taxRate(false));
    }

    @Test
    @DisplayName("discount: 2000円以上は200、1000円以上は100、それ以外は0")
    void discount() {
        assertEquals(200, Register.discount(2500), "2500円のとき");
        assertEquals(200, Register.discount(2000), "ちょうど2000円のとき");
        assertEquals(100, Register.discount(1999), "1999円のとき");
        assertEquals(100, Register.discount(1000), "ちょうど1000円のとき");
        assertEquals(0, Register.discount(999), "999円のとき");
        assertEquals(0, Register.discount(0), "0円のとき");
    }

    @Test
    @DisplayName("priceOf: メニュー6品の価格と、ない名前は-1")
    void priceOf() {
        assertEquals(480, Register.priceOf("ブレンドコーヒー"));
        assertEquals(520, Register.priceOf("カフェラテ"));
        assertEquals(560, Register.priceOf("抹茶ラテ"));
        assertEquals(450, Register.priceOf("チーズケーキ"));
        assertEquals(650, Register.priceOf("ホットサンド"));
        assertEquals(320, Register.priceOf("クロワッサン"));
        assertEquals(-1, Register.priceOf("カフェモカ"));
    }
}
