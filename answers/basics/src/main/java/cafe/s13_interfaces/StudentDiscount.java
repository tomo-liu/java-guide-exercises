package cafe.s13_interfaces;

public class StudentDiscount implements DiscountPolicy {
    @Override
    public int discount(int subtotal) {
        return subtotal / 10;
    }
}
