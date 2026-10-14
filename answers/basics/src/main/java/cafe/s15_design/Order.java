package cafe.s15_design;

public class Order {
    private final Priced[] items;

    public Order(Priced[] items) {
        this.items = items;
    }

    public Priced[] getItems() {
        return items;
    }

    public int total() {
        int sum = 0;
        for (Priced item : items) {
            sum += item.getPrice();
        }
        return sum;
    }
}
