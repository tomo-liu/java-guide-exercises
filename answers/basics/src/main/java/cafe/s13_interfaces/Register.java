package cafe.s13_interfaces;

public class Register {
    private DiscountPolicy policy;

    public Register(DiscountPolicy policy) {
        this.policy = policy;
    }

    public int checkout(int subtotal) {
        return subtotal - policy.discount(subtotal);
    }

    public void changePolicy(DiscountPolicy policy) {
        this.policy = policy;
    }
}
