package cafe.s17_collections;

import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

public class Menu {
    private final Map<String, Integer> prices = new LinkedHashMap<>();

    public void add(String name, int price) {
        prices.put(name, price);
    }

    public int priceOf(String name) {
        Integer price = prices.get(name);
        if (price == null) {
            throw new IllegalArgumentException(name + " はメニューにありません");
        }
        return price;
    }

    public List<String> names() {
        return new ArrayList<>(prices.keySet());
    }
}
