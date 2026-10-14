package cafe.s05_loops;

import static org.junit.jupiter.api.Assertions.assertEquals;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

class LoopsTest {
    @Test
    @DisplayName("stampCard: 押した数だけ●、残りは○の10文字")
    void stampCard() {
        assertEquals("●●●○○○○○○○", Loops.stampCard(3));
        assertEquals("○○○○○○○○○○", Loops.stampCard(0));
        assertEquals("●●●●●●●●●●", Loops.stampCard(10));
    }

    @Test
    @DisplayName("cupsToReach: 売上が目標に届くまでの杯数")
    void cupsToReach() {
        assertEquals(11, Loops.cupsToReach(5000), "5000円のとき(11杯で5280円)");
        assertEquals(1, Loops.cupsToReach(480), "ちょうど1杯分のとき");
        assertEquals(2, Loops.cupsToReach(481), "1杯分を1円超えるとき");
        assertEquals(0, Loops.cupsToReach(0), "目標0円のとき");
    }

    @Test
    @DisplayName("total: 全部の価格の合計")
    void total() {
        assertEquals(1450, Loops.total(new int[] {480, 520, 450}));
        assertEquals(0, Loops.total(new int[] {}));
    }
}
