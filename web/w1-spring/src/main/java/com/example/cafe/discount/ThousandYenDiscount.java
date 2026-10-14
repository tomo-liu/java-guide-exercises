package com.example.cafe.discount;

// TODO: Spring に部品として登録するアノテーションを付ける
public class ThousandYenDiscount implements DiscountPolicy {
    // 小計が1000円以上なら100円、それ未満は0
    @Override
    public int discount(int subtotal) {
        // TODO
        return 0;
    }
}
