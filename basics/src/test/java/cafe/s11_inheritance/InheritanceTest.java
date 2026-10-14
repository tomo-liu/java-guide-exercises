package cafe.s11_inheritance;

import static org.junit.jupiter.api.Assertions.assertEquals;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

class InheritanceTest {
    @Test
    @DisplayName("Drink: サイズを覚えていて、M は+50円・L は+100円")
    void drinkPrice() {
        assertEquals("L", new Drink("カフェラテ", 520, "L").getSize());
        assertEquals(520, new Drink("カフェラテ", 520, "S").getPrice());
        assertEquals(570, new Drink("カフェラテ", 520, "M").getPrice());
        assertEquals(620, new Drink("カフェラテ", 520, "L").getPrice());
    }

    @Test
    @DisplayName("Drink: 親の describe() も追加料金込みの価格で表示される")
    void drinkDescribe() {
        assertEquals("カフェラテ 620円", new Drink("カフェラテ", 520, "L").describe());
    }

    @Test
    @DisplayName("Drink: MenuItem 型の変数に入れても、Drink の getPrice() が使われる")
    void drinkAsMenuItem() {
        MenuItem item = new Drink("ブレンドコーヒー", 480, "M");
        assertEquals("ブレンドコーヒー", item.getName());
        assertEquals(530, item.getPrice());
    }

    @Test
    @DisplayName("Food: 温める場合だけ「(温め)」が付く")
    void foodDescribe() {
        assertEquals("ホットサンド 650円(温め)", new Food("ホットサンド", 650, true).describe());
        assertEquals("チーズケーキ 450円", new Food("チーズケーキ", 450, false).describe());
    }
}
