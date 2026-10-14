package com.example.cafe.web;

import com.example.cafe.ShopInfo;
import com.example.cafe.menu.MenuService;
import com.example.cafe.order.CheckoutService;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.validation.BindingResult;

@Controller
public class MenuController {
    private final MenuService menuService;
    private final CheckoutService checkoutService;
    private final ShopInfo shopInfo;

    public MenuController(MenuService menuService, CheckoutService checkoutService, ShopInfo shopInfo) {
        this.menuService = menuService;
        this.checkoutService = checkoutService;
        this.shopInfo = shopInfo;
    }

    // TODO: GET /menu で、店名(shopName)と全メニュー(items)を Model に入れ、menu.html を表示する
    public String menu(Model model) {
        return "menu";
    }

    // TODO: GET /order で、空の OrderForm(orderForm)と全メニュー(items)を Model に入れ、order.html を表示する
    public String orderForm(Model model) {
        return "order";
    }

    // TODO: POST /order で入力をチェックし、誤りがあれば order.html に戻す(items も入れ直す)。
    //       正しければ、価格 × 個数 を CheckoutService で会計した金額を total に入れ、order-complete.html を表示する
    public String order(OrderForm orderForm, BindingResult result, Model model) {
        return "order";
    }
}
