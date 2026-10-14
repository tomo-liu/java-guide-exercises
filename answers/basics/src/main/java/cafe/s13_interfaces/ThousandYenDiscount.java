package cafe.s13_interfaces;

public class ThousandYenDiscount implements DiscountPolicy {
    @Override
    public int discount(int subtotal) {
        return subtotal >= 1000 ? 100 : 0;
    }
}
