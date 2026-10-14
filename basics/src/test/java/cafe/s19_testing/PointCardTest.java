package cafe.s19_testing;

import static org.junit.jupiter.api.Assertions.assertEquals;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

// あなたが書くテスト。例を1つ書いておいたので、まねして増やそう
class PointCardTest {
    @Test
    @DisplayName("1050円の買い物で10ポイントたまる")
    void earn() {
        // 準備
        PointCard card = new PointCard();
        // 実行
        card.earn(1050);
        // 確認
        assertEquals(10, card.getPoints());
    }

    // TODO: 「ためたポイントの一部を使うと、その分減る」テストを書く

    // TODO: 「持っているポイントをちょうど全部使える」テストを書く

    // TODO: 「持っているより多いポイントを使うと IllegalArgumentException」のテストを書く(assertThrows を使う)
}
