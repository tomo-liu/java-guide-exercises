package cafe.s17_collections;

import java.util.ArrayList;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Set;

public class Order {
    private final List<String> items = new ArrayList<>();

    public void add(String name) {
        items.add(name);
    }

    public int count(String name) {
        int count = 0;
        for (String item : items) {
            if (item.equals(name)) {
                count++;
            }
        }
        return count;
    }

    public Set<String> kinds() {
        return new LinkedHashSet<>(items);
    }

    public int total(Menu menu) {
        int sum = 0;
        for (String item : items) {
            sum += menu.priceOf(item);
        }
        return sum;
    }
}
