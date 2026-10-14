package cafe.s13_interfaces;

public interface DiscountPolicy {
    // 小計を受け取り、割引額を返す
    int discount(int subtotal);
}
