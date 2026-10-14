package cafe.s16_exceptions;

public class Inventory {
    private final String name;
    private int stock;

    public Inventory(String name, int stock) {
        this.name = name;
        this.stock = stock;
    }

    public void take(int qty) throws OutOfStockException {
        if (qty <= 0) {
            throw new IllegalArgumentException("個数は1以上");
        }
        if (qty > stock) {
            throw new OutOfStockException(name, qty, stock);
        }
        stock -= qty;
    }

    public int getStock() {
        return stock;
    }
}
