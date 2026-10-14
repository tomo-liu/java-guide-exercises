package cafe.s17_collections;

import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;

public class Sorting {
    public static List<MenuItem> byPrice(List<MenuItem> items) {
        List<MenuItem> sorted = new ArrayList<>(items);
        sorted.sort(Comparator.comparingInt(MenuItem::price).thenComparing(MenuItem::name));
        return sorted;
    }
}
