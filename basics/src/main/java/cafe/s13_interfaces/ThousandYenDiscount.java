package cafe.s13_interfaces;

// 小計が1000円以上なら100円、それ未満は 0
public class ThousandYenDiscount implements DiscountPolicy {
    @Override
    public int discount(int subtotal) {
        // TODO
        return 0;
    }
}
