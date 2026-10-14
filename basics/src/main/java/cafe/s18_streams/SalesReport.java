package cafe.s18_streams;

import java.util.List;
import java.util.Map;
import java.util.Optional;

// for 文を使わず、Stream で書く
public class SalesReport {
    private final List<Sale> sales;

    public SalesReport(List<Sale> sales) {
        this.sales = sales;
    }

    // 売上合計
    public int total() {
        // TODO
        return 0;
    }

    // price 円以上で売れた品の名前(重複なし、最初に出てきた順)
    public List<String> itemsAtLeast(int price) {
        // TODO
        return List.of();
    }

    // カテゴリごとの売上合計
    public Map<String, Integer> totalByCategory() {
        // TODO
        return Map.of();
    }

    // 品ごとの販売数
    public Map<String, Long> countByItem() {
        // TODO
        return Map.of();
    }

    // 最も多く売れた品の名前(売上が0件なら空)
    public Optional<String> bestSeller() {
        // TODO
        return Optional.empty();
    }
}
