package cafe.s16_exceptions;

public class OutOfStockException extends Exception {
    public OutOfStockException(String itemName, int requested, int remaining) {
        super(itemName + "の在庫が足りません(注文" + requested + "、残り" + remaining + ")");
    }
}
