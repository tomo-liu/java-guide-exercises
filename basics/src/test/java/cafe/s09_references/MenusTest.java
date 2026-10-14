package cafe.s09_references;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotSame;
import static org.junit.jupiter.api.Assertions.assertNull;
import static org.junit.jupiter.api.Assertions.assertSame;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

class MenusTest {
    private MenuItem[] menu() {
        return new MenuItem[] {
            new MenuItem("ブレンドコーヒー", 480),
            new MenuItem("カフェラテ", 520),
        };
    }

    @Test
    @DisplayName("findByName: 見つかった品そのものを返し、なければ null")
    void findByName() {
        MenuItem[] menu = menu();
        assertSame(menu[1], Menus.findByName(menu, "カフェラテ"), "配列に入っている品そのものを返す");
        assertNull(Menus.findByName(menu, "カフェモカ"));
        String name = "ブレンド" + "コーヒー".repeat(1);
        assertSame(menu[0], Menus.findByName(menu, name), "文字列は equals で比べる");
    }

    @Test
    @DisplayName("raiseAll: 渡された品そのものが値上がりする")
    void raiseAll() {
        MenuItem[] menu = menu();
        MenuItem latte = menu[1];
        Menus.raiseAll(menu, 20);
        assertEquals(500, menu[0].price);
        assertEquals(540, latte.price, "同じオブジェクトを指す別の変数からも値上がりが見える");
    }

    @Test
    @DisplayName("copyOf: 中身が同じ別のオブジェクトを返し、コピーを変えても元は変わらない")
    void copyOf() {
        MenuItem original = new MenuItem("カフェラテ", 520);
        MenuItem copy = Menus.copyOf(original);
        assertNotSame(original, copy, "同じオブジェクトではなく、new で作り直す");
        assertEquals("カフェラテ", copy.name);
        assertEquals(520, copy.price);
        copy.price = 999;
        assertEquals(520, original.price, "コピーを変えても元は変わらない");
    }
}
