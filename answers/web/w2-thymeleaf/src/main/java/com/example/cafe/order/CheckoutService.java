package com.example.cafe.order;

import com.example.cafe.discount.DiscountPolicy;
import org.springframework.stereotype.Service;

@Service
public class CheckoutService {
    private final DiscountPolicy policy;

    // DiscountPolicy の実装は、Spring が探して渡してくれる(コンストラクタインジェクション)
    public CheckoutService(DiscountPolicy policy) {
        this.policy = policy;
    }

    public int checkout(int subtotal) {
        return subtotal - policy.discount(subtotal);
    }
}
