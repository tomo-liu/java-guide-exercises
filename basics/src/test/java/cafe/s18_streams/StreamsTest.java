package cafe.s18_streams;

import static org.junit.jupiter.api.Assertions.assertEquals;

import java.util.List;
import java.util.Map;
import java.util.Optional;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

class StreamsTest {
    private final List<Sale> sales = List.of(
        new Sale("カフェラテ", "ドリンク", 520, 9),
        new Sale("チーズケーキ", "フード", 450, 10),
        new Sale("ブレンドコーヒー", "ドリンク", 480, 10),
        new Sale("カフェラテ", "ドリンク", 520, 13),
        new Sale("ホットサンド", "フード", 650, 12),
        new Sale("カフェラテ", "ドリンク", 520, 15)
    );
    private final SalesReport report = new SalesReport(sales);

    @Test
    @DisplayName("total: 売上合計")
    void total() {
        assertEquals(3140, report.total());
    }

    @Test
    @DisplayName("itemsAtLeast: 重複なし・最初に出てきた順")
    void itemsAtLeast() {
        assertEquals(List.of("カフェラテ", "ホットサンド"), report.itemsAtLeast(500));
        assertEquals(List.of("カフェラテ", "ブレンドコーヒー", "ホットサンド"), report.itemsAtLeast(480));
    }

    @Test
    @DisplayName("totalByCategory: カテゴリごとの売上合計")
    void totalByCategory() {
        assertEquals(Map.of("ドリンク", 2040, "フード", 1100), report.totalByCategory());
    }

    @Test
    @DisplayName("countByItem: 品ごとの販売数")
    void countByItem() {
        assertEquals(Map.of("カフェラテ", 3L, "チーズケーキ", 1L, "ブレンドコーヒー", 1L, "ホットサンド", 1L), report.countByItem());
    }

    @Test
    @DisplayName("bestSeller: 最も多く売れた品。売上0件なら空")
    void bestSeller() {
        assertEquals(Optional.of("カフェラテ"), report.bestSeller());
        assertEquals(Optional.empty(), new SalesReport(List.of()).bestSeller());
    }
}
