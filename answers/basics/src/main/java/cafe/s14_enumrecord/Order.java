package cafe.s14_enumrecord;

public class Order {
    public static int total(OrderLine[] lines) {
        int sum = 0;
        for (OrderLine line : lines) {
            sum += line.subtotal();
        }
        return sum;
    }
}
