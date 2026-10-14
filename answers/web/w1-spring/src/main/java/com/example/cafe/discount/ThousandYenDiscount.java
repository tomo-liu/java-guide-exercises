package com.example.cafe.discount;

import org.springframework.stereotype.Component;

@Component
public class ThousandYenDiscount implements DiscountPolicy {
    @Override
    public int discount(int subtotal) {
        return subtotal >= 1000 ? 100 : 0;
    }
}
