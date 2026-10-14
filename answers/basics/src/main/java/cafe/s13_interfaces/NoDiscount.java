package cafe.s13_interfaces;

public class NoDiscount implements DiscountPolicy {
    @Override
    public int discount(int subtotal) {
        return 0;
    }
}
