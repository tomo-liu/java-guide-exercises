package cafe.s16_exceptions;

public class Inventory {
    private final String name;
    private int stock;

    public Inventory(String name, int stock) {
        this.name = name;
        this.stock = stock;
    }

    // 在庫を qty 個減らす。
    // qty が0以下なら IllegalArgumentException、在庫より多ければ OutOfStockException を投げる
    public void take(int qty) throws OutOfStockException {
        // TODO
    }

    public int getStock() {
        return stock;
    }
}
