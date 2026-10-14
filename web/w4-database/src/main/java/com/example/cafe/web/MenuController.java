package com.example.cafe.web;

import com.example.cafe.ShopInfo;
import com.example.cafe.menu.MenuService;
import com.example.cafe.order.CheckoutService;
import jakarta.validation.Valid;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.validation.BindingResult;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.PostMapping;

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

    // メニュー一覧の画面
    @GetMapping("/menu")
    public String menu(Model model) {
        model.addAttribute("shopName", shopInfo.getName());
        model.addAttribute("items", menuService.findAll());
        return "menu";
    }

    // 注文フォームの画面
    @GetMapping("/order")
    public String orderForm(Model model) {
        model.addAttribute("orderForm", new OrderForm());
        model.addAttribute("items", menuService.findAll());
        return "order";
    }

    // 注文を受け付ける。入力に誤りがあればフォームに戻す
    @PostMapping("/order")
    public String order(@Valid @ModelAttribute OrderForm orderForm, BindingResult result, Model model) {
        if (result.hasErrors()) {
            model.addAttribute("items", menuService.findAll());
            return "order";
        }
        int subtotal = menuService.priceOf(orderForm.getName()) * orderForm.getQuantity();
        model.addAttribute("total", checkoutService.checkout(subtotal));
        return "order-complete";
    }
}
