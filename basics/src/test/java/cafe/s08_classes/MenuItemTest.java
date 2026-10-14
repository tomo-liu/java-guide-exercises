package cafe.s08_classes;

import static org.junit.jupiter.api.Assertions.assertEquals;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

class MenuItemTest {
    @Test
    @DisplayName("toString: 「名前(価格円)」の形")
    void toStringFormat() {
        assertEquals("カフェラテ(520円)", new MenuItem("カフェラテ", 520).toString());
        assertEquals("クロワッサン(320円)", new MenuItem("クロワッサン", 320).toString());
    }

    @Test
    @DisplayName("priceWithTax: その品の税込価格")
    void priceWithTax() {
        MenuItem coffee = new MenuItem("ブレンドコーヒー", 480);
        assertEquals(518, coffee.priceWithTax(true));
        assertEquals(528, coffee.priceWithTax(false));
    }

    @Test
    @DisplayName("オブジェクトごとに別々の値を持つ")
    void eachObjectHasOwnValues() {
        MenuItem a = new MenuItem("カフェラテ", 520);
        MenuItem b = new MenuItem("抹茶ラテ", 560);
        assertEquals("カフェラテ(520円)", a.toString());
        assertEquals("抹茶ラテ(560円)", b.toString());
        assertEquals(616, b.priceWithTax(false));
    }
}
