package cafe.s12_polymorphism;

import static org.junit.jupiter.api.Assertions.assertEquals;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

class PolymorphismTest {
    private final MenuItem[] order = {
        new Drink("カフェラテ", 520, "L"),
        new Food("ホットサンド", 650, true),
        new Drink("ブレンドコーヒー", 480, "S"),
        new Food("チーズケーキ", 450, false),
    };

    @Test
    @DisplayName("total: 各品の getPrice() の合計(ドリンクは追加料金込み)")
    void total() {
        assertEquals(2200, Register.total(order));
    }

    @Test
    @DisplayName("countDrinks: ドリンクの数")
    void countDrinks() {
        assertEquals(2, Register.countDrinks(order));
        assertEquals(0, Register.countDrinks(new MenuItem[] {new Food("クロワッサン", 320, false)}));
    }

    @Test
    @DisplayName("label: 種類ごとの表示名")
    void label() {
        assertEquals("カフェラテ(L)", Register.label(order[0]));
        assertEquals("ホットサンド(温め)", Register.label(order[1]));
        assertEquals("チーズケーキ", Register.label(order[3]));
        assertEquals("季節のスープ", Register.label(new MenuItem("季節のスープ", 600)));
    }
}
