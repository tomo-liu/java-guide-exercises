package cafe.s16_exceptions;

public class OrderService {
    public static String tryOrder(Inventory inventory, int qty) {
        try {
            inventory.take(qty);
            return "注文を受け付けました";
        } catch (OutOfStockException e) {
            return e.getMessage();
        } catch (IllegalArgumentException e) {
            return "個数が正しくありません";
        }
    }
}
