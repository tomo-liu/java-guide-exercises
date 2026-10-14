package cafe.s19_testing;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

class PointCardTest {
    @Test
    @DisplayName("1050円の買い物で10ポイントたまる")
    void earn() {
        PointCard card = new PointCard();
        card.earn(1050);
        assertEquals(10, card.getPoints());
    }

    @Test
    @DisplayName("ためたポイントの一部を使うと、その分減る")
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
    @DisplayName("持っているより多いポイントを使うと IllegalArgumentException")
    void useTooMany() {
        PointCard card = new PointCard();
        card.earn(500);
        assertThrows(IllegalArgumentException.class, () -> card.use(6));
    }
}
