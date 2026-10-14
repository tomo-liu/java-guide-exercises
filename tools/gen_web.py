# 課題リポジトリ web/ の4ステップ(Spring Boot)を生成する。
#   python gen_web.py <リポジトリのルート> <initializrで作ったプロジェクト(pom・mvnwの元)>
# 各ステップの「解答」は、そのステップまでの ANSWERS を順に重ねたもの。
# 各ステップの「開始コード」は、前のステップの解答に、そのステップの STARTS(TODO入りの雛形)を重ねたもの。
import os, shutil, sys

ROOT = sys.argv[1]
BASE = sys.argv[2]
J = "src/main/java/com/example/cafe/"
T = "src/test/java/com/example/cafe/"
R = "src/main/resources/"

STEPS = ["w1-spring", "w2-thymeleaf", "w3-rest", "w4-database"]
ANSWERS = {s: {} for s in STEPS}
STARTS = {s: {} for s in STEPS}

# ======================= w1: Spring入門(DI) =======================
ANSWERS["w1-spring"][J + "CafeApplication.java"] = r'''package com.example.cafe;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class CafeApplication {

    public static void main(String[] args) {
        SpringApplication.run(CafeApplication.class, args);
    }
}
'''

ANSWERS["w1-spring"][R + "application.yml"] = r'''spring:
  application:
    name: cafe

# お店の情報(ShopInfo が読み込む)
cafe:
  name: ひだまりカフェ
  hours: "8:00-20:00"
'''

ANSWERS["w1-spring"][J + "menu/MenuItem.java"] = r'''package com.example.cafe.menu;

public class MenuItem {
    private final String name;
    private final int price;
    private final String category;

    public MenuItem(String name, int price, String category) {
        this.name = name;
        this.price = price;
        this.category = category;
    }

    public String getName() {
        return name;
    }

    public int getPrice() {
        return price;
    }

    public String getCategory() {
        return category;
    }
}
'''

ANSWERS["w1-spring"][J + "menu/MenuNotFoundException.java"] = r'''package com.example.cafe.menu;

// メニューにない品を指定されたときの例外
public class MenuNotFoundException extends RuntimeException {
    public MenuNotFoundException(String name) {
        super(name + " はメニューにありません");
    }
}
'''

ANSWERS["w1-spring"][J + "menu/MenuService.java"] = r'''package com.example.cafe.menu;

import java.util.List;
import org.springframework.stereotype.Service;

@Service
public class MenuService {
    private final List<MenuItem> items = List.of(
        new MenuItem("ブレンドコーヒー", 480, "ドリンク"),
        new MenuItem("カフェラテ", 520, "ドリンク"),
        new MenuItem("抹茶ラテ", 560, "ドリンク"),
        new MenuItem("チーズケーキ", 450, "フード"),
        new MenuItem("ホットサンド", 650, "フード"),
        new MenuItem("クロワッサン", 320, "フード")
    );

    public List<MenuItem> findAll() {
        return items;
    }

    public MenuItem findByName(String name) {
        return items.stream()
            .filter(item -> item.getName().equals(name))
            .findFirst()
            .orElseThrow(() -> new MenuNotFoundException(name));
    }

    public int priceOf(String name) {
        return findByName(name).getPrice();
    }
}
'''
STARTS["w1-spring"][J + "menu/MenuService.java"] = r'''package com.example.cafe.menu;

import java.util.List;

// TODO: Spring に管理してもらうためのアノテーションを付ける
public class MenuService {
    private final List<MenuItem> items = List.of(
        new MenuItem("ブレンドコーヒー", 480, "ドリンク"),
        new MenuItem("カフェラテ", 520, "ドリンク"),
        new MenuItem("抹茶ラテ", 560, "ドリンク"),
        new MenuItem("チーズケーキ", 450, "フード"),
        new MenuItem("ホットサンド", 650, "フード"),
        new MenuItem("クロワッサン", 320, "フード")
    );

    public List<MenuItem> findAll() {
        return items;
    }

    // 名前が一致する品を返す。なければ MenuNotFoundException を投げる
    public MenuItem findByName(String name) {
        // TODO
        return null;
    }

    // 名前から価格を返す(findByName を使う)
    public int priceOf(String name) {
        // TODO
        return 0;
    }
}
'''

ANSWERS["w1-spring"][J + "discount/DiscountPolicy.java"] = r'''package com.example.cafe.discount;

public interface DiscountPolicy {
    int discount(int subtotal);
}
'''

ANSWERS["w1-spring"][J + "discount/ThousandYenDiscount.java"] = r'''package com.example.cafe.discount;

import org.springframework.stereotype.Component;

@Component
public class ThousandYenDiscount implements DiscountPolicy {
    @Override
    public int discount(int subtotal) {
        return subtotal >= 1000 ? 100 : 0;
    }
}
'''
STARTS["w1-spring"][J + "discount/ThousandYenDiscount.java"] = r'''package com.example.cafe.discount;

// TODO: Spring に部品として登録するアノテーションを付ける
public class ThousandYenDiscount implements DiscountPolicy {
    // 小計が1000円以上なら100円、それ未満は0
    @Override
    public int discount(int subtotal) {
        // TODO
        return 0;
    }
}
'''

ANSWERS["w1-spring"][J + "order/CheckoutService.java"] = r'''package com.example.cafe.order;

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
'''
STARTS["w1-spring"][J + "order/CheckoutService.java"] = r'''package com.example.cafe.order;

// TODO: Spring に管理してもらうためのアノテーションを付ける
public class CheckoutService {
    // TODO: DiscountPolicy をフィールドで持ち、コンストラクタで受け取る(自分で new しない)

    // 割引後の金額を返す
    public int checkout(int subtotal) {
        // TODO
        return 0;
    }
}
'''

ANSWERS["w1-spring"][J + "ShopInfo.java"] = r'''package com.example.cafe;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

// application.yml に書いたお店の情報
@Component
public class ShopInfo {
    private final String name;
    private final String hours;

    public ShopInfo(@Value("${cafe.name}") String name, @Value("${cafe.hours}") String hours) {
        this.name = name;
        this.hours = hours;
    }

    public String getName() {
        return name;
    }

    public String getHours() {
        return hours;
    }
}
'''
STARTS["w1-spring"][J + "ShopInfo.java"] = r'''package com.example.cafe;

// TODO: Spring に部品として登録するアノテーションを付ける
public class ShopInfo {
    private final String name;
    private final String hours;

    // TODO: @Value を使い、application.yml の cafe.name と cafe.hours を受け取る
    public ShopInfo(String name, String hours) {
        this.name = name;
        this.hours = hours;
    }

    public String getName() {
        return name;
    }

    public String getHours() {
        return hours;
    }
}
'''

ANSWERS["w1-spring"][T + "CafeServicesTest.java"] = r'''package com.example.cafe;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

import com.example.cafe.menu.MenuNotFoundException;
import com.example.cafe.menu.MenuService;
import com.example.cafe.order.CheckoutService;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

// w1: Spring が部品を組み立ててくれるか(DI)を確かめる
@SpringBootTest
class CafeServicesTest {
    @Autowired
    MenuService menuService;

    @Autowired
    CheckoutService checkoutService;

    @Autowired
    ShopInfo shopInfo;

    @Test
    @DisplayName("MenuService: 6品のメニューと、名前からの価格")
    void menu() {
        assertEquals(6, menuService.findAll().size());
        assertEquals(520, menuService.priceOf("カフェラテ"));
        assertThrows(MenuNotFoundException.class, () -> menuService.priceOf("カフェモカ"));
    }

    @Test
    @DisplayName("CheckoutService: Spring が渡した割引ルール(千円以上で100円引き)で会計する")
    void checkout() {
        assertEquals(1310, checkoutService.checkout(1410));
        assertEquals(999, checkoutService.checkout(999));
    }

    @Test
    @DisplayName("ShopInfo: 設定ファイルの値を読み込む")
    void shopInfo() {
        assertEquals("ひだまりカフェ", shopInfo.getName());
        assertEquals("8:00-20:00", shopInfo.getHours());
    }
}
'''

# ======================= w2: 画面(Thymeleaf) =======================
ANSWERS["w2-thymeleaf"][J + "web/OrderForm.java"] = r'''package com.example.cafe.web;

import jakarta.validation.constraints.Max;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotBlank;

// 注文フォームの入力を受け取る入れ物
public class OrderForm {
    @NotBlank(message = "品を選んでください")
    private String name;

    @Min(value = 1, message = "個数は1以上にしてください")
    @Max(value = 10, message = "個数は10以下にしてください")
    private int quantity = 1;

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public int getQuantity() {
        return quantity;
    }

    public void setQuantity(int quantity) {
        this.quantity = quantity;
    }
}
'''
STARTS["w2-thymeleaf"][J + "web/OrderForm.java"] = r'''package com.example.cafe.web;

// 注文フォームの入力を受け取る入れ物
public class OrderForm {
    // TODO: 空なら「品を選んでください」というメッセージで弾く
    private String name;

    // TODO: 1未満なら「個数は1以上にしてください」、10より大きければ「個数は10以下にしてください」で弾く
    private int quantity = 1;

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public int getQuantity() {
        return quantity;
    }

    public void setQuantity(int quantity) {
        this.quantity = quantity;
    }
}
'''

ANSWERS["w2-thymeleaf"][J + "web/MenuController.java"] = r'''package com.example.cafe.web;

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
'''
STARTS["w2-thymeleaf"][J + "web/MenuController.java"] = r'''package com.example.cafe.web;

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
'''

ANSWERS["w2-thymeleaf"][R + "templates/menu.html"] = r'''<!DOCTYPE html>
<html xmlns:th="http://www.thymeleaf.org" lang="ja">
<head>
    <meta charset="UTF-8">
    <title th:text="${shopName}">カフェ</title>
</head>
<body>
<h1 th:text="${shopName}">カフェの名前</h1>
<table>
    <tr th:each="item : ${items}">
        <td th:text="${item.name}">品名</td>
        <td th:text="${item.price} + '円'">0円</td>
    </tr>
</table>
<p><a th:href="@{/order}">注文する</a></p>
</body>
</html>
'''
ANSWERS["w2-thymeleaf"][R + "templates/order.html"] = r'''<!DOCTYPE html>
<html xmlns:th="http://www.thymeleaf.org" lang="ja">
<head>
    <meta charset="UTF-8">
    <title>ご注文</title>
</head>
<body>
<h1>ご注文</h1>
<form th:action="@{/order}" th:object="${orderForm}" method="post">
    <p>
        <label>品
            <select th:field="*{name}">
                <option value="">選んでください</option>
                <option th:each="item : ${items}" th:value="${item.name}" th:text="${item.name}">品名</option>
            </select>
        </label>
        <span th:if="${#fields.hasErrors('name')}" th:errors="*{name}">エラー</span>
    </p>
    <p>
        <label>個数 <input type="number" th:field="*{quantity}"></label>
        <span th:if="${#fields.hasErrors('quantity')}" th:errors="*{quantity}">エラー</span>
    </p>
    <button type="submit">注文する</button>
</form>
</body>
</html>
'''
ANSWERS["w2-thymeleaf"][R + "templates/order-complete.html"] = r'''<!DOCTYPE html>
<html xmlns:th="http://www.thymeleaf.org" lang="ja">
<head>
    <meta charset="UTF-8">
    <title>ご注文ありがとうございます</title>
</head>
<body>
<h1>ご注文ありがとうございます</h1>
<p>お支払い: <span th:text="${total} + '円'">0円</span></p>
<p><a th:href="@{/menu}">メニューに戻る</a></p>
</body>
</html>
'''

ANSWERS["w2-thymeleaf"][T + "MenuPageTest.java"] = r'''package com.example.cafe;

import static org.hamcrest.Matchers.containsString;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.content;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.view;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.webmvc.test.autoconfigure.AutoConfigureMockMvc;
import org.springframework.test.web.servlet.MockMvc;

// w2: 画面(Thymeleaf)とフォームの入力チェックを確かめる
@SpringBootTest
@AutoConfigureMockMvc
class MenuPageTest {
    @Autowired
    MockMvc mockMvc;

    @Test
    @DisplayName("GET /menu: 店名とメニューが表示される")
    void menuPage() throws Exception {
        mockMvc.perform(get("/menu"))
            .andExpect(status().isOk())
            .andExpect(view().name("menu"))
            .andExpect(content().string(containsString("ひだまりカフェ")))
            .andExpect(content().string(containsString("カフェラテ")))
            .andExpect(content().string(containsString("520円")));
    }

    @Test
    @DisplayName("GET /order: 注文フォームが表示される")
    void orderForm() throws Exception {
        mockMvc.perform(get("/order"))
            .andExpect(status().isOk())
            .andExpect(view().name("order"))
            .andExpect(content().string(containsString("チーズケーキ")));
    }

    @Test
    @DisplayName("POST /order: 正しい注文なら、割引後の金額を表示する")
    void orderOk() throws Exception {
        mockMvc.perform(post("/order").param("name", "カフェラテ").param("quantity", "2"))
            .andExpect(status().isOk())
            .andExpect(view().name("order-complete"))
            .andExpect(content().string(containsString("940円")));
    }

    @Test
    @DisplayName("POST /order: 個数が0ならフォームに戻り、メッセージが出る")
    void orderInvalid() throws Exception {
        mockMvc.perform(post("/order").param("name", "カフェラテ").param("quantity", "0"))
            .andExpect(status().isOk())
            .andExpect(view().name("order"))
            .andExpect(content().string(containsString("個数は1以上にしてください")));
    }

    @Test
    @DisplayName("POST /order: 品を選ばないとフォームに戻る")
    void orderNoItem() throws Exception {
        mockMvc.perform(post("/order").param("name", "").param("quantity", "1"))
            .andExpect(view().name("order"))
            .andExpect(content().string(containsString("品を選んでください")));
    }
}
'''

# ======================= w3: REST API =======================
ANSWERS["w3-rest"][J + "api/OrderRequest.java"] = r'''package com.example.cafe.api;

import jakarta.validation.constraints.Max;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotBlank;

// POST /api/orders で受け取るJSON
public record OrderRequest(
    @NotBlank(message = "品を選んでください") String name,
    @Min(value = 1, message = "個数は1以上にしてください") @Max(value = 10, message = "個数は10以下にしてください") int quantity) {
}
'''
STARTS["w3-rest"][J + "api/OrderRequest.java"] = r'''package com.example.cafe.api;

// POST /api/orders で受け取るJSON
// TODO: OrderForm と同じ入力チェック(品は必須、個数は1〜10)を付ける
public record OrderRequest(String name, int quantity) {
}
'''
ANSWERS["w3-rest"][J + "api/OrderResponse.java"] = r'''package com.example.cafe.api;

// POST /api/orders が返すJSON
public record OrderResponse(String name, int quantity, int total) {
}
'''
ANSWERS["w3-rest"][J + "api/ErrorResponse.java"] = r'''package com.example.cafe.api;

// エラーのときに返すJSON
public record ErrorResponse(String message) {
}
'''
ANSWERS["w3-rest"][J + "api/MenuApiController.java"] = r'''package com.example.cafe.api;

import com.example.cafe.menu.MenuItem;
import com.example.cafe.menu.MenuService;
import com.example.cafe.order.CheckoutService;
import jakarta.validation.Valid;
import java.util.List;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api")
public class MenuApiController {
    private final MenuService menuService;
    private final CheckoutService checkoutService;

    public MenuApiController(MenuService menuService, CheckoutService checkoutService) {
        this.menuService = menuService;
        this.checkoutService = checkoutService;
    }

    @GetMapping("/menu")
    public List<MenuItem> menu() {
        return menuService.findAll();
    }

    @GetMapping("/menu/{name}")
    public MenuItem item(@PathVariable String name) {
        return menuService.findByName(name);
    }

    @PostMapping("/orders")
    public ResponseEntity<OrderResponse> order(@Valid @RequestBody OrderRequest request) {
        int subtotal = menuService.priceOf(request.name()) * request.quantity();
        int total = checkoutService.checkout(subtotal);
        return ResponseEntity.status(HttpStatus.CREATED).body(new OrderResponse(request.name(), request.quantity(), total));
    }
}
'''
STARTS["w3-rest"][J + "api/MenuApiController.java"] = r'''package com.example.cafe.api;

import com.example.cafe.menu.MenuItem;
import com.example.cafe.menu.MenuService;
import com.example.cafe.order.CheckoutService;
import java.util.List;
import org.springframework.http.ResponseEntity;

// TODO: JSON を返すコントローラーにし、URL の先頭を /api にそろえる
public class MenuApiController {
    private final MenuService menuService;
    private final CheckoutService checkoutService;

    public MenuApiController(MenuService menuService, CheckoutService checkoutService) {
        this.menuService = menuService;
        this.checkoutService = checkoutService;
    }

    // TODO: GET /api/menu で全メニューを返す
    public List<MenuItem> menu() {
        return List.of();
    }

    // TODO: GET /api/menu/{name} で1品を返す(ない名前なら MenuNotFoundException がそのまま投げられてよい)
    public MenuItem item(String name) {
        return null;
    }

    // TODO: POST /api/orders で JSON を受け取って入力をチェックし、
    //       201 Created と OrderResponse(品名・個数・割引後の金額)を返す
    public ResponseEntity<OrderResponse> order(OrderRequest request) {
        return null;
    }
}
'''
ANSWERS["w3-rest"][J + "api/ApiExceptionHandler.java"] = r'''package com.example.cafe.api;

import com.example.cafe.menu.MenuNotFoundException;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestControllerAdvice;

// API で起きた例外を、まとめてエラーのJSONに変える
@RestControllerAdvice
public class ApiExceptionHandler {
    @ExceptionHandler(MenuNotFoundException.class)
    @ResponseStatus(HttpStatus.NOT_FOUND)
    public ErrorResponse notFound(MenuNotFoundException e) {
        return new ErrorResponse(e.getMessage());
    }

    @ExceptionHandler(MethodArgumentNotValidException.class)
    @ResponseStatus(HttpStatus.BAD_REQUEST)
    public ErrorResponse invalid(MethodArgumentNotValidException e) {
        return new ErrorResponse(e.getBindingResult().getFieldErrors().get(0).getDefaultMessage());
    }
}
'''
STARTS["w3-rest"][J + "api/ApiExceptionHandler.java"] = r'''package com.example.cafe.api;

import com.example.cafe.menu.MenuNotFoundException;
import org.springframework.web.bind.MethodArgumentNotValidException;

// TODO: API で起きた例外をまとめて受け止めるクラスにする
public class ApiExceptionHandler {
    // TODO: MenuNotFoundException を 404 Not Found と ErrorResponse(例外のメッセージ)にする
    public ErrorResponse notFound(MenuNotFoundException e) {
        return null;
    }

    // TODO: 入力チェックの失敗を 400 Bad Request と ErrorResponse(最初の項目のメッセージ)にする
    //       メッセージは e.getBindingResult().getFieldErrors().get(0).getDefaultMessage() で取れる
    public ErrorResponse invalid(MethodArgumentNotValidException e) {
        return null;
    }
}
'''

ANSWERS["w3-rest"][T + "MenuApiTest.java"] = r'''package com.example.cafe;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.webmvc.test.autoconfigure.AutoConfigureMockMvc;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;

// w3: REST API(JSON の入出力・ステータスコード・エラー処理)を確かめる
@SpringBootTest
@AutoConfigureMockMvc
class MenuApiTest {
    @Autowired
    MockMvc mockMvc;

    @Test
    @DisplayName("GET /api/menu: 6品のJSON配列")
    void menu() throws Exception {
        mockMvc.perform(get("/api/menu"))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.length()").value(6))
            .andExpect(jsonPath("$[1].name").value("カフェラテ"))
            .andExpect(jsonPath("$[1].price").value(520));
    }

    @Test
    @DisplayName("GET /api/menu/{name}: 1品のJSON")
    void item() throws Exception {
        mockMvc.perform(get("/api/menu/{name}", "抹茶ラテ"))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.price").value(560))
            .andExpect(jsonPath("$.category").value("ドリンク"));
    }

    @Test
    @DisplayName("GET /api/menu/{name}: ない品は 404 とエラーメッセージ")
    void itemNotFound() throws Exception {
        mockMvc.perform(get("/api/menu/{name}", "カフェモカ"))
            .andExpect(status().isNotFound())
            .andExpect(jsonPath("$.message").value("カフェモカ はメニューにありません"));
    }

    @Test
    @DisplayName("POST /api/orders: 201 Created と割引後の金額")
    void order() throws Exception {
        mockMvc.perform(post("/api/orders")
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"name\": \"カフェラテ\", \"quantity\": 2}"))
            .andExpect(status().isCreated())
            .andExpect(jsonPath("$.name").value("カフェラテ"))
            .andExpect(jsonPath("$.quantity").value(2))
            .andExpect(jsonPath("$.total").value(940));
    }

    @Test
    @DisplayName("POST /api/orders: 個数が0なら 400 とエラーメッセージ")
    void orderInvalid() throws Exception {
        mockMvc.perform(post("/api/orders")
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"name\": \"カフェラテ\", \"quantity\": 0}"))
            .andExpect(status().isBadRequest())
            .andExpect(jsonPath("$.message").value("個数は1以上にしてください"));
    }
}
'''

# ======================= w4: DB(Spring Data JPA) =======================
ANSWERS["w4-database"][R + "application.yml"] = r'''spring:
  application:
    name: cafe
  jpa:
    # テーブルを作ってから data.sql で最初のメニューを入れる
    defer-datasource-initialization: true
    # 実行されたSQLをログに出す(学習用)
    show-sql: true
  sql:
    init:
      encoding: UTF-8

# お店の情報(ShopInfo が読み込む)
cafe:
  name: ひだまりカフェ
  hours: "8:00-20:00"
'''
ANSWERS["w4-database"][R + "data.sql"] = r'''INSERT INTO menu_item (name, price, category, stock) VALUES
    ('ブレンドコーヒー', 480, 'ドリンク', 100),
    ('カフェラテ', 520, 'ドリンク', 100),
    ('抹茶ラテ', 560, 'ドリンク', 50),
    ('チーズケーキ', 450, 'フード', 10),
    ('ホットサンド', 650, 'フード', 10),
    ('クロワッサン', 320, 'フード', 3);
'''
ANSWERS["w4-database"][J + "menu/MenuItem.java"] = r'''package com.example.cafe.menu;

import com.example.cafe.order.OutOfStockException;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;

// menu_item テーブルの1行に対応するエンティティ
@Entity
public class MenuItem {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String name;
    private int price;
    private String category;
    private int stock;

    // JPA がDBから読み込むときに使う(自分では使わない)
    protected MenuItem() {
    }

    public MenuItem(String name, int price, String category, int stock) {
        this.name = name;
        this.price = price;
        this.category = category;
        this.stock = stock;
    }

    // 在庫を減らす。足りなければ OutOfStockException
    public void reduceStock(int quantity) {
        if (quantity > stock) {
            throw new OutOfStockException(name, quantity, stock);
        }
        stock -= quantity;
    }

    public Long getId() {
        return id;
    }

    public String getName() {
        return name;
    }

    public int getPrice() {
        return price;
    }

    public String getCategory() {
        return category;
    }

    public int getStock() {
        return stock;
    }
}
'''
STARTS["w4-database"][J + "menu/MenuItem.java"] = r'''package com.example.cafe.menu;

import com.example.cafe.order.OutOfStockException;

// TODO: menu_item テーブルの1行に対応するエンティティにする
//   1. クラスに @Entity を付ける
//   2. id に @Id と @GeneratedValue(strategy = GenerationType.IDENTITY) を付ける
public class MenuItem {
    private Long id;

    private String name;
    private int price;
    private String category;
    private int stock;

    // JPA がDBから読み込むときに使う(自分では使わない)
    protected MenuItem() {
    }

    public MenuItem(String name, int price, String category, int stock) {
        this.name = name;
        this.price = price;
        this.category = category;
        this.stock = stock;
    }

    // 在庫を減らす。足りなければ OutOfStockException
    public void reduceStock(int quantity) {
        if (quantity > stock) {
            throw new OutOfStockException(name, quantity, stock);
        }
        stock -= quantity;
    }

    public Long getId() {
        return id;
    }

    public String getName() {
        return name;
    }

    public int getPrice() {
        return price;
    }

    public String getCategory() {
        return category;
    }

    public int getStock() {
        return stock;
    }
}
'''
ANSWERS["w4-database"][J + "menu/MenuItemRepository.java"] = r'''package com.example.cafe.menu;

import java.util.List;
import java.util.Optional;
import org.springframework.data.jpa.repository.JpaRepository;

// メソッドの名前から、Spring Data JPA が SQL を組み立ててくれる
public interface MenuItemRepository extends JpaRepository<MenuItem, Long> {
    Optional<MenuItem> findByName(String name);

    List<MenuItem> findByPriceLessThanEqualOrderByPriceAsc(int price);
}
'''
ANSWERS["w4-database"][J + "menu/MenuService.java"] = r'''package com.example.cafe.menu;

import java.util.List;
import org.springframework.data.domain.Sort;
import org.springframework.stereotype.Service;

@Service
public class MenuService {
    private final MenuItemRepository repository;

    public MenuService(MenuItemRepository repository) {
        this.repository = repository;
    }

    public List<MenuItem> findAll() {
        return repository.findAll(Sort.by("id"));
    }

    public MenuItem findByName(String name) {
        return repository.findByName(name).orElseThrow(() -> new MenuNotFoundException(name));
    }

    public int priceOf(String name) {
        return findByName(name).getPrice();
    }
}
'''
STARTS["w4-database"][J + "menu/MenuService.java"] = r'''package com.example.cafe.menu;

import java.util.List;
import org.springframework.stereotype.Service;

// TODO: メニューを List で持つのをやめ、MenuItemRepository(DB)から読むように書き換える
//   - コンストラクタで MenuItemRepository を受け取る
//   - findAll は id の順(repository.findAll(Sort.by("id")))
//   - findByName は repository.findByName(name) を使い、なければ MenuNotFoundException
@Service
public class MenuService {
    private final List<MenuItem> items = List.of();

    public List<MenuItem> findAll() {
        return items;
    }

    public MenuItem findByName(String name) {
        return items.stream()
            .filter(item -> item.getName().equals(name))
            .findFirst()
            .orElseThrow(() -> new MenuNotFoundException(name));
    }

    public int priceOf(String name) {
        return findByName(name).getPrice();
    }
}
'''
ANSWERS["w4-database"][J + "order/OutOfStockException.java"] = r'''package com.example.cafe.order;

// 在庫切れ(RuntimeException なので、@Transactional のメソッドから投げられるとロールバックされる)
public class OutOfStockException extends RuntimeException {
    public OutOfStockException(String name, int requested, int remaining) {
        super(name + "の在庫が足りません(注文" + requested + "、残り" + remaining + ")");
    }
}
'''
ANSWERS["w4-database"][J + "order/CafeOrder.java"] = r'''package com.example.cafe.order;

import com.example.cafe.menu.MenuItem;
import jakarta.persistence.CascadeType;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.OneToMany;
import jakarta.persistence.Table;
import java.util.ArrayList;
import java.util.List;

// 1回の注文(orders テーブル)。注文明細(OrderLine)を複数持つ
@Entity
@Table(name = "orders")
public class CafeOrder {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private int total;

    @OneToMany(mappedBy = "order", cascade = CascadeType.ALL)
    private List<OrderLine> lines = new ArrayList<>();

    public void addLine(MenuItem item, int quantity) {
        lines.add(new OrderLine(this, item, quantity));
    }

    public Long getId() {
        return id;
    }

    public int getTotal() {
        return total;
    }

    public void setTotal(int total) {
        this.total = total;
    }

    public List<OrderLine> getLines() {
        return lines;
    }
}
'''
ANSWERS["w4-database"][J + "order/OrderLine.java"] = r'''package com.example.cafe.order;

import com.example.cafe.menu.MenuItem;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.ManyToOne;

// 注文明細(order_line テーブル)。どの注文の、どの品を、何個か
@Entity
public class OrderLine {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne
    private CafeOrder order;

    @ManyToOne
    private MenuItem item;

    private int quantity;

    protected OrderLine() {
    }

    public OrderLine(CafeOrder order, MenuItem item, int quantity) {
        this.order = order;
        this.item = item;
        this.quantity = quantity;
    }

    public MenuItem getItem() {
        return item;
    }

    public int getQuantity() {
        return quantity;
    }

    public int subtotal() {
        return item.getPrice() * quantity;
    }
}
'''
ANSWERS["w4-database"][J + "order/CafeOrderRepository.java"] = r'''package com.example.cafe.order;

import org.springframework.data.jpa.repository.JpaRepository;

public interface CafeOrderRepository extends JpaRepository<CafeOrder, Long> {
}
'''
ANSWERS["w4-database"][J + "order/OrderService.java"] = r'''package com.example.cafe.order;

import com.example.cafe.api.OrderRequest;
import com.example.cafe.menu.MenuItem;
import com.example.cafe.menu.MenuService;
import java.util.List;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
public class OrderService {
    private final MenuService menuService;
    private final CheckoutService checkoutService;
    private final CafeOrderRepository orderRepository;

    public OrderService(MenuService menuService, CheckoutService checkoutService, CafeOrderRepository orderRepository) {
        this.menuService = menuService;
        this.checkoutService = checkoutService;
        this.orderRepository = orderRepository;
    }

    // 在庫を減らし、注文を保存する。途中で在庫切れが起きたら、全部なかったことにする
    @Transactional
    public CafeOrder placeOrder(List<OrderRequest> requests) {
        CafeOrder order = new CafeOrder();
        int subtotal = 0;
        for (OrderRequest request : requests) {
            MenuItem item = menuService.findByName(request.name());
            item.reduceStock(request.quantity());
            order.addLine(item, request.quantity());
            subtotal += item.getPrice() * request.quantity();
        }
        order.setTotal(checkoutService.checkout(subtotal));
        return orderRepository.save(order);
    }
}
'''
STARTS["w4-database"][J + "order/OrderService.java"] = r'''package com.example.cafe.order;

import com.example.cafe.api.OrderRequest;
import com.example.cafe.menu.MenuService;
import java.util.List;
import org.springframework.stereotype.Service;

@Service
public class OrderService {
    private final MenuService menuService;
    private final CheckoutService checkoutService;
    private final CafeOrderRepository orderRepository;

    public OrderService(MenuService menuService, CheckoutService checkoutService, CafeOrderRepository orderRepository) {
        this.menuService = menuService;
        this.checkoutService = checkoutService;
        this.orderRepository = orderRepository;
    }

    // TODO: 注文を受け付ける。途中で在庫切れが起きたら、それまでの在庫の減少も全部取り消されるようにする
    //   1. new CafeOrder() を作る
    //   2. 注文の品ごとに、menuService.findByName で品を探し、item.reduceStock(個数) で在庫を減らし、
    //      order.addLine(品, 個数) で明細を足し、価格 × 個数 を小計に足す
    //   3. order.setTotal(checkoutService.checkout(小計)) で割引後の金額を入れる
    //   4. orderRepository.save(order) で保存して返す
    public CafeOrder placeOrder(List<OrderRequest> requests) {
        throw new UnsupportedOperationException("TODO");
    }
}
'''
ANSWERS["w4-database"][J + "api/MenuApiController.java"] = r'''package com.example.cafe.api;

import com.example.cafe.menu.MenuItem;
import com.example.cafe.menu.MenuService;
import com.example.cafe.order.CafeOrder;
import com.example.cafe.order.OrderService;
import jakarta.validation.Valid;
import java.util.List;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api")
public class MenuApiController {
    private final MenuService menuService;
    private final OrderService orderService;

    public MenuApiController(MenuService menuService, OrderService orderService) {
        this.menuService = menuService;
        this.orderService = orderService;
    }

    @GetMapping("/menu")
    public List<MenuItem> menu() {
        return menuService.findAll();
    }

    @GetMapping("/menu/{name}")
    public MenuItem item(@PathVariable String name) {
        return menuService.findByName(name);
    }

    // DBに注文を保存し、在庫を減らす
    @PostMapping("/orders")
    public ResponseEntity<OrderResponse> order(@Valid @RequestBody OrderRequest request) {
        CafeOrder order = orderService.placeOrder(List.of(request));
        return ResponseEntity.status(HttpStatus.CREATED).body(new OrderResponse(request.name(), request.quantity(), order.getTotal()));
    }
}
'''
ANSWERS["w4-database"][J + "api/ApiExceptionHandler.java"] = r'''package com.example.cafe.api;

import com.example.cafe.menu.MenuNotFoundException;
import com.example.cafe.order.OutOfStockException;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestControllerAdvice;

// API で起きた例外を、まとめてエラーのJSONに変える
@RestControllerAdvice
public class ApiExceptionHandler {
    @ExceptionHandler(MenuNotFoundException.class)
    @ResponseStatus(HttpStatus.NOT_FOUND)
    public ErrorResponse notFound(MenuNotFoundException e) {
        return new ErrorResponse(e.getMessage());
    }

    @ExceptionHandler(MethodArgumentNotValidException.class)
    @ResponseStatus(HttpStatus.BAD_REQUEST)
    public ErrorResponse invalid(MethodArgumentNotValidException e) {
        return new ErrorResponse(e.getBindingResult().getFieldErrors().get(0).getDefaultMessage());
    }

    @ExceptionHandler(OutOfStockException.class)
    @ResponseStatus(HttpStatus.CONFLICT)
    public ErrorResponse outOfStock(OutOfStockException e) {
        return new ErrorResponse(e.getMessage());
    }
}
'''
ANSWERS["w4-database"][T + "OrderServiceTest.java"] = r'''package com.example.cafe;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertThrows;

import com.example.cafe.api.OrderRequest;
import com.example.cafe.menu.MenuItem;
import com.example.cafe.menu.MenuItemRepository;
import com.example.cafe.order.CafeOrder;
import com.example.cafe.order.OrderService;
import com.example.cafe.order.OutOfStockException;
import java.util.List;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

// w4: DB(エンティティ・リポジトリ・トランザクション)を確かめる
@SpringBootTest
class OrderServiceTest {
    @Autowired
    OrderService orderService;

    @Autowired
    MenuItemRepository menuItemRepository;

    private int stockOf(String name) {
        return menuItemRepository.findByName(name).orElseThrow().getStock();
    }

    @Test
    @DisplayName("リポジトリ: data.sql のメニューが入っていて、名前や価格で探せる")
    void repository() {
        assertEquals(6, menuItemRepository.count());
        List<String> cheap = menuItemRepository.findByPriceLessThanEqualOrderByPriceAsc(450).stream()
            .map(MenuItem::getName)
            .toList();
        assertEquals(List.of("クロワッサン", "チーズケーキ"), cheap);
    }

    @Test
    @DisplayName("placeOrder: 注文が保存され、在庫が減る")
    void placeOrder() {
        int before = stockOf("ホットサンド");
        CafeOrder order = orderService.placeOrder(List.of(new OrderRequest("ホットサンド", 2)));
        assertNotNull(order.getId(), "保存されると id が振られる");
        assertEquals(1300 - 100, order.getTotal(), "650円×2 = 1300円、千円以上で100円引き");
        assertEquals(1, order.getLines().size());
        assertEquals(before - 2, stockOf("ホットサンド"));
    }

    @Test
    @DisplayName("placeOrder: 途中で在庫切れになったら、全部取り消される(ロールバック)")
    void rollback() {
        int latteBefore = stockOf("カフェラテ");
        assertThrows(OutOfStockException.class, () -> orderService.placeOrder(List.of(
            new OrderRequest("カフェラテ", 1),
            new OrderRequest("クロワッサン", 99)
        )));
        assertEquals(latteBefore, stockOf("カフェラテ"), "先に減らしたカフェラテの在庫も元に戻る");
    }
}
'''


def write(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)


def copy_base(dest):
    os.makedirs(dest, exist_ok=True)
    for name in ["pom.xml", "mvnw", "mvnw.cmd"]:
        shutil.copy(os.path.join(BASE, name), os.path.join(dest, name))
    shutil.copytree(os.path.join(BASE, ".mvn"), os.path.join(dest, ".mvn"), dirs_exist_ok=True)


answer_so_far = {}
for step in STEPS:
    previous_answer = dict(answer_so_far)
    answer_so_far.update(ANSWERS[step])
    start = dict(previous_answer)
    # そのステップで新しく出てくるファイルは、解答版をまず入れてから TODO 版で上書きする
    for path, content in ANSWERS[step].items():
        start[path] = content
    start.update(STARTS[step])
    # 開始コードでは、そのステップのテスト以外(前のステップまでのテスト)も含める
    start_dir = os.path.join(ROOT, "web", step)
    answer_dir = os.path.join(ROOT, "answers", "web", step)
    for d in (start_dir, answer_dir):
        if os.path.exists(d):
            shutil.rmtree(d)
        copy_base(d)
    for path, content in start.items():
        write(os.path.join(start_dir, path), content)
    for path, content in answer_so_far.items():
        write(os.path.join(answer_dir, path), content)
    print("wrote", step, len(start), "files (start),", len(answer_so_far), "files (answer)")
