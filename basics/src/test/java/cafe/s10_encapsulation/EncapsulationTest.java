package cafe.s10_encapsulation;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.lang.reflect.Field;
import java.lang.reflect.Modifier;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

class EncapsulationTest {
    private static void assertAllFieldsPrivate(Class<?> type) {
        Field[] fields = type.getDeclaredFields();
        assertTrue(fields.length > 0, type.getSimpleName() + " にフィールドを用意する");
        for (Field field : fields) {
            assertTrue(Modifier.isPrivate(field.getModifiers()),
                type.getSimpleName() + " のフィールド " + field.getName() + " を private にする");
        }
    }

    @Test
    @DisplayName("MenuItem: フィールドがすべて private")
    void menuItemFieldsArePrivate() {
        assertAllFieldsPrivate(MenuItem.class);
    }

    @Test
    @DisplayName("MenuItem: getter と税込価格")
    void menuItemGetters() {
        MenuItem latte = new MenuItem("カフェラテ", 520);
        assertEquals("カフェラテ", latte.getName());
        assertEquals(520, latte.getPrice());
        assertEquals(561, latte.priceWithTax(true));
        assertEquals(572, latte.priceWithTax(false));
    }

    @Test
    @DisplayName("MenuItem: changePrice は0以下を受け付けない")
    void changePrice() {
        MenuItem latte = new MenuItem("カフェラテ", 520);
        assertFalse(latte.changePrice(-100));
        assertFalse(latte.changePrice(0));
        assertEquals(520, latte.getPrice(), "不正な値では価格は変わらない");
        assertTrue(latte.changePrice(540));
        assertEquals(540, latte.getPrice());
    }

    @Test
    @DisplayName("StampCard: フィールドがすべて private")
    void stampCardFieldsArePrivate() {
        assertAllFieldsPrivate(StampCard.class);
    }

    @Test
    @DisplayName("StampCard: 10個で無料券になり、スタンプは0に戻る")
    void stampCard() {
        StampCard card = new StampCard();
        for (int i = 0; i < 9; i++) {
            card.addStamp();
        }
        assertEquals(9, card.getStamps());
        assertEquals(0, card.getFreeDrinks());
        card.addStamp();
        assertEquals(0, card.getStamps(), "10個目で0に戻る");
        assertEquals(1, card.getFreeDrinks());
        for (int i = 0; i < 12; i++) {
            card.addStamp();
        }
        assertEquals(2, card.getStamps());
        assertEquals(2, card.getFreeDrinks());
    }
}
