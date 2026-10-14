package cafe.s16_exceptions;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertThrows;

import java.lang.reflect.Modifier;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

class ExceptionsTest {
    @Test
    @DisplayName("OutOfStockException: 検査例外で、決まった形のメッセージを持つ")
    void exceptionMessage() {
        assertFalse(RuntimeException.class.isAssignableFrom(OutOfStockException.class), "RuntimeException ではなく Exception を継承する");
        OutOfStockException e = new OutOfStockException("カフェラテ", 2, 1);
        assertEquals("カフェラテの在庫が足りません(注文2、残り1)", e.getMessage());
    }

    @Test
    @DisplayName("Inventory: 在庫の範囲なら減る")
    void take() throws OutOfStockException {
        Inventory inventory = new Inventory("クロワッサン", 3);
        inventory.take(2);
        assertEquals(1, inventory.getStock());
        inventory.take(1);
        assertEquals(0, inventory.getStock(), "ちょうど在庫分は注文できる");
    }

    @Test
    @DisplayName("Inventory: 在庫より多いと OutOfStockException、在庫は減らない")
    void outOfStock() {
        Inventory inventory = new Inventory("カフェラテ", 1);
        OutOfStockException e = assertThrows(OutOfStockException.class, () -> inventory.take(2));
        assertEquals("カフェラテの在庫が足りません(注文2、残り1)", e.getMessage());
        assertEquals(1, inventory.getStock());
    }

    @Test
    @DisplayName("Inventory: 0以下の個数は IllegalArgumentException")
    void invalidQuantity() {
        Inventory inventory = new Inventory("カフェラテ", 5);
        assertThrows(IllegalArgumentException.class, () -> inventory.take(0));
        assertThrows(IllegalArgumentException.class, () -> inventory.take(-1));
        assertEquals(5, inventory.getStock());
    }

    @Test
    @DisplayName("OrderService.tryOrder: 例外を外に漏らさず、結果を文字列で返す")
    void tryOrder() {
        Inventory inventory = new Inventory("チーズケーキ", 2);
        assertEquals("注文を受け付けました", OrderService.tryOrder(inventory, 1));
        assertEquals("チーズケーキの在庫が足りません(注文3、残り1)", OrderService.tryOrder(inventory, 3));
        assertEquals("個数が正しくありません", OrderService.tryOrder(inventory, 0));
        assertEquals(1, inventory.getStock());
    }
}
