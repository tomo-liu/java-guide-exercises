package cafe.s13_interfaces;

// 割引額はいつも 0
public class NoDiscount implements DiscountPolicy {
    @Override
    public int discount(int subtotal) {
        // TODO
        return -1;
    }
}
