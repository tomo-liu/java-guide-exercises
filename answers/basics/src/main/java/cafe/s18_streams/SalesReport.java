package cafe.s18_streams;

import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.stream.Collectors;

public class SalesReport {
    private final List<Sale> sales;

    public SalesReport(List<Sale> sales) {
        this.sales = sales;
    }

    public int total() {
        return sales.stream().mapToInt(Sale::price).sum();
    }

    public List<String> itemsAtLeast(int price) {
        return sales.stream()
            .filter(s -> s.price() >= price)
            .map(Sale::item)
            .distinct()
            .toList();
    }

    public Map<String, Integer> totalByCategory() {
        return sales.stream()
            .collect(Collectors.groupingBy(Sale::category, Collectors.summingInt(Sale::price)));
    }

    public Map<String, Long> countByItem() {
        return sales.stream()
            .collect(Collectors.groupingBy(Sale::item, Collectors.counting()));
    }

    public Optional<String> bestSeller() {
        return countByItem().entrySet().stream()
            .max(Map.Entry.comparingByValue())
            .map(Map.Entry::getKey);
    }
}
