package cafe.s19_testing;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

// 採点用のテスト(このファイルは書き換えない)
class PointCardSpecTest {
    @Test
    @DisplayName("100円ごとに1ポイント(端数切り捨て)")
    void earn() {
        PointCard card = new PointCard();
        card.earn(1050);
        card.earn(99);
        assertEquals(10, card.getPoints());
    }

    @Test
    @DisplayName("一部を使うとその分減る")
    void usePart() {
        PointCard card = new PointCard();
        card.earn(1000);
        card.use(3);
        assertEquals(7, card.getPoints());
    }

    @Test
    @DisplayName("持っているポイントをちょうど全部使える")
    void useAll() {
        PointCard card = new PointCard();
        card.earn(500);
        card.use(5);
        assertEquals(0, card.getPoints());
    }

    @Test
    @DisplayName("持っているより多い・0以下のポイントは使えない")
    void useInvalid() {
        PointCard card = new PointCard();
        card.earn(500);
        assertThrows(IllegalArgumentException.class, () -> card.use(6));
        assertThrows(IllegalArgumentException.class, () -> card.use(0));
        assertEquals(5, card.getPoints());
    }
}
