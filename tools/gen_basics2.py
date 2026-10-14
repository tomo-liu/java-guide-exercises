# 課題リポジトリ basics の s11〜s19 を生成する(gen_basics1.py と同じ形式)。
import os, sys

ROOT = sys.argv[1]
EX = []

JUNIT = r'''import static org.junit.jupiter.api.Assertions.assertEquals;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
'''

# ---------- s11 ----------
S11_MENU = r'''package cafe.s11_inheritance;

public class MenuItem {
    private final String name;
    private final int price;

    public MenuItem(String name, int price) {
        this.name = name;
        this.price = price;
    }

    public String getName() {
        return name;
    }

    public int getPrice() {
        return price;
    }

    public String describe() {
        return name + " " + getPrice() + "円";
    }
}
'''
EX.append(dict(pkg="s11_inheritance", start={"MenuItem.java": S11_MENU, "Drink.java": r'''package cafe.s11_inheritance;

public class Drink extends MenuItem {
    // TODO: サイズ("S"・"M"・"L")を持つ private final なフィールドを追加する

    public Drink(String name, int price, String size) {
        super(name, price);
        // TODO: サイズをフィールドに入れる
    }

    public String getSize() {
        // TODO
        return null;
    }

    // TODO: getPrice() をオーバーライドし、M は +50円、L は +100円にする(S はそのまま)
}
''', "Food.java": r'''package cafe.s11_inheritance;

public class Food extends MenuItem {
    // TODO: 温めるかどうか(boolean)を持つ private final なフィールドを追加する

    public Food(String name, int price, boolean warm) {
        super(name, price);
        // TODO: 温めるかどうかをフィールドに入れる
    }

    // TODO: describe() をオーバーライドし、温める場合は親の説明の後ろに「(温め)」を付ける
}
'''}, answer={"Drink.java": r'''package cafe.s11_inheritance;

public class Drink extends MenuItem {
    private final String size;

    public Drink(String name, int price, String size) {
        super(name, price);
        this.size = size;
    }

    public String getSize() {
        return size;
    }

    @Override
    public int getPrice() {
        int extra = switch (size) {
            case "M" -> 50;
            case "L" -> 100;
            default -> 0;
        };
        return super.getPrice() + extra;
    }
}
''', "Food.java": r'''package cafe.s11_inheritance;

public class Food extends MenuItem {
    private final boolean warm;

    public Food(String name, int price, boolean warm) {
        super(name, price);
        this.warm = warm;
    }

    @Override
    public String describe() {
        return warm ? super.describe() + "(温め)" : super.describe();
    }
}
'''}, test={"InheritanceTest.java": r'''package cafe.s11_inheritance;

''' + JUNIT + r'''
class InheritanceTest {
    @Test
    @DisplayName("Drink: サイズを覚えていて、M は+50円・L は+100円")
    void drinkPrice() {
        assertEquals("L", new Drink("カフェラテ", 520, "L").getSize());
        assertEquals(520, new Drink("カフェラテ", 520, "S").getPrice());
        assertEquals(570, new Drink("カフェラテ", 520, "M").getPrice());
        assertEquals(620, new Drink("カフェラテ", 520, "L").getPrice());
    }

    @Test
    @DisplayName("Drink: 親の describe() も追加料金込みの価格で表示される")
    void drinkDescribe() {
        assertEquals("カフェラテ 620円", new Drink("カフェラテ", 520, "L").describe());
    }

    @Test
    @DisplayName("Drink: MenuItem 型の変数に入れても、Drink の getPrice() が使われる")
    void drinkAsMenuItem() {
        MenuItem item = new Drink("ブレンドコーヒー", 480, "M");
        assertEquals("ブレンドコーヒー", item.getName());
        assertEquals(530, item.getPrice());
    }

    @Test
    @DisplayName("Food: 温める場合だけ「(温め)」が付く")
    void foodDescribe() {
        assertEquals("ホットサンド 650円(温め)", new Food("ホットサンド", 650, true).describe());
        assertEquals("チーズケーキ 450円", new Food("チーズケーキ", 450, false).describe());
    }
}
'''}))

# ---------- s12 ----------
S12_GIVEN = {
    "MenuItem.java": r'''package cafe.s12_polymorphism;

public class MenuItem {
    private final String name;
    private final int price;

    public MenuItem(String name, int price) {
        this.name = name;
        this.price = price;
    }

    public String getName() {
        return name;
    }

    public int getPrice() {
        return price;
    }
}
''',
    "Drink.java": r'''package cafe.s12_polymorphism;

public class Drink extends MenuItem {
    private final String size;

    public Drink(String name, int price, String size) {
        super(name, price);
        this.size = size;
    }

    public String getSize() {
        return size;
    }

    @Override
    public int getPrice() {
        int extra = switch (size) {
            case "M" -> 50;
            case "L" -> 100;
            default -> 0;
        };
        return super.getPrice() + extra;
    }
}
''',
    "Food.java": r'''package cafe.s12_polymorphism;

public class Food extends MenuItem {
    private final boolean warm;

    public Food(String name, int price, boolean warm) {
        super(name, price);
        this.warm = warm;
    }

    public boolean isWarm() {
        return warm;
    }
}
''',
}
EX.append(dict(pkg="s12_polymorphism", start=dict(S12_GIVEN, **{"Register.java": r'''package cafe.s12_polymorphism;

public class Register {
    // 全品の価格(各品の getPrice())の合計
    public static int total(MenuItem[] order) {
        // TODO
        return 0;
    }

    // ドリンクの数(instanceof を使う)
    public static int countDrinks(MenuItem[] order) {
        // TODO
        return 0;
    }

    // switch のパターンマッチで、ドリンクは「カフェラテ(L)」、温めるフードは「ホットサンド(温め)」、それ以外は名前だけ
    public static String label(MenuItem item) {
        // TODO
        return "";
    }
}
'''}), answer={"Register.java": r'''package cafe.s12_polymorphism;

public class Register {
    public static int total(MenuItem[] order) {
        int sum = 0;
        for (MenuItem item : order) {
            sum += item.getPrice();
        }
        return sum;
    }

    public static int countDrinks(MenuItem[] order) {
        int count = 0;
        for (MenuItem item : order) {
            if (item instanceof Drink) {
                count++;
            }
        }
        return count;
    }

    public static String label(MenuItem item) {
        return switch (item) {
            case Drink d -> d.getName() + "(" + d.getSize() + ")";
            case Food f when f.isWarm() -> f.getName() + "(温め)";
            default -> item.getName();
        };
    }
}
'''}, test={"PolymorphismTest.java": r'''package cafe.s12_polymorphism;

''' + JUNIT + r'''
class PolymorphismTest {
    private final MenuItem[] order = {
        new Drink("カフェラテ", 520, "L"),
        new Food("ホットサンド", 650, true),
        new Drink("ブレンドコーヒー", 480, "S"),
        new Food("チーズケーキ", 450, false),
    };

    @Test
    @DisplayName("total: 各品の getPrice() の合計(ドリンクは追加料金込み)")
    void total() {
        assertEquals(2200, Register.total(order));
    }

    @Test
    @DisplayName("countDrinks: ドリンクの数")
    void countDrinks() {
        assertEquals(2, Register.countDrinks(order));
        assertEquals(0, Register.countDrinks(new MenuItem[] {new Food("クロワッサン", 320, false)}));
    }

    @Test
    @DisplayName("label: 種類ごとの表示名")
    void label() {
        assertEquals("カフェラテ(L)", Register.label(order[0]));
        assertEquals("ホットサンド(温め)", Register.label(order[1]));
        assertEquals("チーズケーキ", Register.label(order[3]));
        assertEquals("季節のスープ", Register.label(new MenuItem("季節のスープ", 600)));
    }
}
'''}))

# ---------- s13 ----------
S13_POLICY = r'''package cafe.s13_interfaces;

public interface DiscountPolicy {
    // 小計を受け取り、割引額を返す
    int discount(int subtotal);
}
'''
EX.append(dict(pkg="s13_interfaces", start={
    "DiscountPolicy.java": S13_POLICY,
    "NoDiscount.java": r'''package cafe.s13_interfaces;

// 割引額はいつも 0
public class NoDiscount implements DiscountPolicy {
    @Override
    public int discount(int subtotal) {
        // TODO
        return -1;
    }
}
''',
    "StudentDiscount.java": r'''package cafe.s13_interfaces;

// 小計の10%(1円未満切り捨て)
public class StudentDiscount implements DiscountPolicy {
    @Override
    public int discount(int subtotal) {
        // TODO
        return 0;
    }
}
''',
    "ThousandYenDiscount.java": r'''package cafe.s13_interfaces;

// 小計が1000円以上なら100円、それ未満は 0
public class ThousandYenDiscount implements DiscountPolicy {
    @Override
    public int discount(int subtotal) {
        // TODO
        return 0;
    }
}
''',
    "Register.java": r'''package cafe.s13_interfaces;

public class Register {
    // TODO: 割引ルール(DiscountPolicy)を持つフィールドを追加する

    public Register(DiscountPolicy policy) {
        // TODO
    }

    // 割引後の金額を返す(割引の種類を if で見分けない)
    public int checkout(int subtotal) {
        // TODO
        return 0;
    }

    // あとから割引ルールを差し替える
    public void changePolicy(DiscountPolicy policy) {
        // TODO
    }
}
'''}, answer={
    "NoDiscount.java": r'''package cafe.s13_interfaces;

public class NoDiscount implements DiscountPolicy {
    @Override
    public int discount(int subtotal) {
        return 0;
    }
}
''',
    "StudentDiscount.java": r'''package cafe.s13_interfaces;

public class StudentDiscount implements DiscountPolicy {
    @Override
    public int discount(int subtotal) {
        return subtotal / 10;
    }
}
''',
    "ThousandYenDiscount.java": r'''package cafe.s13_interfaces;

public class ThousandYenDiscount implements DiscountPolicy {
    @Override
    public int discount(int subtotal) {
        return subtotal >= 1000 ? 100 : 0;
    }
}
''',
    "Register.java": r'''package cafe.s13_interfaces;

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
'''}, test={"InterfacesTest.java": r'''package cafe.s13_interfaces;

''' + JUNIT + r'''
class InterfacesTest {
    @Test
    @DisplayName("NoDiscount: いつも0円")
    void noDiscount() {
        assertEquals(0, new NoDiscount().discount(1410));
        assertEquals(0, new NoDiscount().discount(0));
    }

    @Test
    @DisplayName("StudentDiscount: 小計の10%(切り捨て)")
    void studentDiscount() {
        assertEquals(141, new StudentDiscount().discount(1410));
        assertEquals(48, new StudentDiscount().discount(480));
    }

    @Test
    @DisplayName("ThousandYenDiscount: 1000円以上で100円")
    void thousandYenDiscount() {
        assertEquals(100, new ThousandYenDiscount().discount(1000));
        assertEquals(0, new ThousandYenDiscount().discount(999));
    }

    @Test
    @DisplayName("Register: 受け取った割引ルールで会計する")
    void checkout() {
        assertEquals(1269, new Register(new StudentDiscount()).checkout(1410));
        assertEquals(1310, new Register(new ThousandYenDiscount()).checkout(1410));
        assertEquals(1410, new Register(new NoDiscount()).checkout(1410));
    }

    @Test
    @DisplayName("Register: どんな実装でも差し込める(ここでは150円引きのルールをその場で作る)")
    void anyPolicy() {
        DiscountPolicy lunch = subtotal -> 150;
        assertEquals(1020, new Register(lunch).checkout(1170));
    }

    @Test
    @DisplayName("Register: changePolicy でルールを差し替えられる")
    void changePolicy() {
        Register register = new Register(new NoDiscount());
        register.changePolicy(new StudentDiscount());
        assertEquals(1269, register.checkout(1410));
    }
}
'''}))

# ---------- s14 ----------
EX.append(dict(pkg="s14_enumrecord", start={
    "Size.java": r'''package cafe.s14_enumrecord;

public enum Size {
    // TODO: 追加料金(0・50・100円)とラベル("S"・"M"・"L")を持たせる
    SMALL, MEDIUM, LARGE;

    // 追加料金
    public int extra() {
        // TODO
        return -1;
    }

    // 「S」「M」「L」
    public String label() {
        // TODO
        return "";
    }
}
''',
    "OrderLine.java": r'''package cafe.s14_enumrecord;

public record OrderLine(String name, int unitPrice, Size size, int quantity) {
    // (単価 + 追加料金)× 個数
    public int subtotal() {
        // TODO
        return 0;
    }
}
''',
    "Order.java": r'''package cafe.s14_enumrecord;

public class Order {
    // 明細の小計の合計
    public static int total(OrderLine[] lines) {
        // TODO
        return 0;
    }
}
'''}, answer={
    "Size.java": r'''package cafe.s14_enumrecord;

public enum Size {
    SMALL(0, "S"), MEDIUM(50, "M"), LARGE(100, "L");

    private final int extra;
    private final String label;

    Size(int extra, String label) {
        this.extra = extra;
        this.label = label;
    }

    public int extra() {
        return extra;
    }

    public String label() {
        return label;
    }
}
''',
    "OrderLine.java": r'''package cafe.s14_enumrecord;

public record OrderLine(String name, int unitPrice, Size size, int quantity) {
    public int subtotal() {
        return (unitPrice + size.extra()) * quantity;
    }
}
''',
    "Order.java": r'''package cafe.s14_enumrecord;

public class Order {
    public static int total(OrderLine[] lines) {
        int sum = 0;
        for (OrderLine line : lines) {
            sum += line.subtotal();
        }
        return sum;
    }
}
'''}, test={"EnumRecordTest.java": r'''package cafe.s14_enumrecord;

''' + JUNIT + r'''
class EnumRecordTest {
    @Test
    @DisplayName("Size: 追加料金とラベル")
    void size() {
        assertEquals(0, Size.SMALL.extra());
        assertEquals(50, Size.MEDIUM.extra());
        assertEquals(100, Size.LARGE.extra());
        assertEquals("S", Size.SMALL.label());
        assertEquals("M", Size.MEDIUM.label());
        assertEquals("L", Size.LARGE.label());
    }

    @Test
    @DisplayName("OrderLine: (単価+追加料金)× 個数")
    void subtotal() {
        assertEquals(1240, new OrderLine("カフェラテ", 520, Size.LARGE, 2).subtotal());
        assertEquals(480, new OrderLine("ブレンドコーヒー", 480, Size.SMALL, 1).subtotal());
    }

    @Test
    @DisplayName("OrderLine: record なので中身が同じなら equals が true")
    void recordEquality() {
        assertEquals(new OrderLine("カフェラテ", 520, Size.MEDIUM, 1), new OrderLine("カフェラテ", 520, Size.MEDIUM, 1));
    }

    @Test
    @DisplayName("Order.total: 明細の合計")
    void total() {
        OrderLine[] lines = {
            new OrderLine("カフェラテ", 520, Size.LARGE, 2),
            new OrderLine("抹茶ラテ", 560, Size.MEDIUM, 1),
        };
        assertEquals(1850, Order.total(lines));
        assertEquals(0, Order.total(new OrderLine[] {}));
    }
}
'''}))

# ---------- s15 ----------
S15_GIVEN = {
    "Priced.java": r'''package cafe.s15_design;

public interface Priced {
    String getName();

    int getPrice();
}
''',
    "Item.java": r'''package cafe.s15_design;

public class Item implements Priced {
    private final String name;
    private final int price;

    public Item(String name, int price) {
        this.name = name;
        this.price = price;
    }

    @Override
    public String getName() {
        return name;
    }

    @Override
    public int getPrice() {
        return price;
    }
}
''',
}
EX.append(dict(pkg="s15_design", start=dict(S15_GIVEN, **{
    "LunchSet.java": r'''package cafe.s15_design;

// ドリンクとフードを「持つ」セット(継承しない)
public class LunchSet implements Priced {
    // TODO: ドリンクとフード(どちらも Priced)をフィールドで持つ

    public LunchSet(Priced drink, Priced food) {
        // TODO
    }

    // 「カフェラテとホットサンドのセット」の形
    @Override
    public String getName() {
        // TODO
        return "";
    }

    // 2つの合計から100円引き
    @Override
    public int getPrice() {
        // TODO
        return 0;
    }
}
''',
    "Order.java": r'''package cafe.s15_design;

public class Order {
    // TODO: 注文された品(Priced の配列)をフィールドで持つ

    public Order(Priced[] items) {
        // TODO
    }

    public Priced[] getItems() {
        // TODO
        return new Priced[0];
    }

    // 合計金額
    public int total() {
        // TODO
        return 0;
    }
}
''',
    "ReceiptPrinter.java": r'''package cafe.s15_design;

public class ReceiptPrinter {
    // 1品ごとに「名前 価格円」の行、最後に「合計 ○○円」の行を、改行(\n)でつないで返す。
    // 合計の計算は Order に任せる
    public String print(Order order) {
        // TODO
        return "";
    }
}
'''}), answer={
    "LunchSet.java": r'''package cafe.s15_design;

public class LunchSet implements Priced {
    private final Priced drink;
    private final Priced food;

    public LunchSet(Priced drink, Priced food) {
        this.drink = drink;
        this.food = food;
    }

    @Override
    public String getName() {
        return drink.getName() + "と" + food.getName() + "のセット";
    }

    @Override
    public int getPrice() {
        return drink.getPrice() + food.getPrice() - 100;
    }
}
''',
    "Order.java": r'''package cafe.s15_design;

public class Order {
    private final Priced[] items;

    public Order(Priced[] items) {
        this.items = items;
    }

    public Priced[] getItems() {
        return items;
    }

    public int total() {
        int sum = 0;
        for (Priced item : items) {
            sum += item.getPrice();
        }
        return sum;
    }
}
''',
    "ReceiptPrinter.java": r'''package cafe.s15_design;

public class ReceiptPrinter {
    public String print(Order order) {
        String text = "";
        for (Priced item : order.getItems()) {
            text += item.getName() + " " + item.getPrice() + "円\n";
        }
        text += "合計 " + order.total() + "円";
        return text;
    }
}
'''}, test={"DesignTest.java": r'''package cafe.s15_design;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

class DesignTest {
    private final Priced latte = new Item("カフェラテ", 520);
    private final Priced sandwich = new Item("ホットサンド", 650);

    @Test
    @DisplayName("LunchSet: 名前と、100円引きの価格")
    void lunchSet() {
        LunchSet set = new LunchSet(latte, sandwich);
        assertEquals("カフェラテとホットサンドのセット", set.getName());
        assertEquals(1070, set.getPrice());
    }

    @Test
    @DisplayName("LunchSet: 継承ではなく合成で作る(Item などを継承しない)")
    void lunchSetUsesComposition() {
        assertEquals(Object.class, LunchSet.class.getSuperclass(), "LunchSet は他のクラスを extends しない");
        assertFalse(Item.class.isAssignableFrom(LunchSet.class));
    }

    @Test
    @DisplayName("Order: セットもふつうの品と同じように合計できる")
    void orderTotal() {
        Order order = new Order(new Priced[] {new LunchSet(latte, sandwich), new Item("クロワッサン", 320)});
        assertEquals(1390, order.total());
    }

    @Test
    @DisplayName("ReceiptPrinter: 1品ずつの行と合計の行")
    void receipt() {
        Order order = new Order(new Priced[] {latte, new Item("チーズケーキ", 450)});
        assertEquals("カフェラテ 520円\nチーズケーキ 450円\n合計 970円", new ReceiptPrinter().print(order));
    }

    @Test
    @DisplayName("ReceiptPrinter: 合計は Order の total() の結果を使う")
    void receiptUsesOrderTotal() {
        Order discounted = new Order(new Priced[] {latte}) {
            @Override
            public int total() {
                return 500;
            }
        };
        assertEquals("カフェラテ 520円\n合計 500円", new ReceiptPrinter().print(discounted));
    }
}
'''}))

# ---------- s16 ----------
EX.append(dict(pkg="s16_exceptions", start={
    "OutOfStockException.java": r'''package cafe.s16_exceptions;

// 在庫切れを表す検査例外
public class OutOfStockException extends Exception {
    // TODO: 品名・注文数・残り数を受け取り、
    //       メッセージを「カフェラテの在庫が足りません(注文2、残り1)」の形にする
    public OutOfStockException(String itemName, int requested, int remaining) {
        super("TODO");
    }
}
''',
    "Inventory.java": r'''package cafe.s16_exceptions;

public class Inventory {
    private final String name;
    private int stock;

    public Inventory(String name, int stock) {
        this.name = name;
        this.stock = stock;
    }

    // 在庫を qty 個減らす。
    // qty が0以下なら IllegalArgumentException、在庫より多ければ OutOfStockException を投げる
    public void take(int qty) throws OutOfStockException {
        // TODO
    }

    public int getStock() {
        return stock;
    }
}
''',
    "OrderService.java": r'''package cafe.s16_exceptions;

public class OrderService {
    // 注文を試みる。成功なら「注文を受け付けました」、在庫切れなら例外のメッセージ、
    // 個数が不正なら「個数が正しくありません」を返す(例外を外に漏らさない)
    public static String tryOrder(Inventory inventory, int qty) {
        // TODO
        return "";
    }
}
'''}, answer={
    "OutOfStockException.java": r'''package cafe.s16_exceptions;

public class OutOfStockException extends Exception {
    public OutOfStockException(String itemName, int requested, int remaining) {
        super(itemName + "の在庫が足りません(注文" + requested + "、残り" + remaining + ")");
    }
}
''',
    "Inventory.java": r'''package cafe.s16_exceptions;

public class Inventory {
    private final String name;
    private int stock;

    public Inventory(String name, int stock) {
        this.name = name;
        this.stock = stock;
    }

    public void take(int qty) throws OutOfStockException {
        if (qty <= 0) {
            throw new IllegalArgumentException("個数は1以上");
        }
        if (qty > stock) {
            throw new OutOfStockException(name, qty, stock);
        }
        stock -= qty;
    }

    public int getStock() {
        return stock;
    }
}
''',
    "OrderService.java": r'''package cafe.s16_exceptions;

public class OrderService {
    public static String tryOrder(Inventory inventory, int qty) {
        try {
            inventory.take(qty);
            return "注文を受け付けました";
        } catch (OutOfStockException e) {
            return e.getMessage();
        } catch (IllegalArgumentException e) {
            return "個数が正しくありません";
        }
    }
}
'''}, test={"ExceptionsTest.java": r'''package cafe.s16_exceptions;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertThrows;

import java.lang.reflect.Modifier;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

class ExceptionsTest {
    @Test
    @DisplayName("OutOfStockException: 検査例外で、決まった形のメッセージを持つ")
    void exceptionMessage() {
        assertFalse(RuntimeException.class.isAssignableFrom(OutOfStockException.class), "RuntimeException ではなく Exception を継承する");
        OutOfStockException e = new OutOfStockException("カフェラテ", 2, 1);
        assertEquals("カフェラテの在庫が足りません(注文2、残り1)", e.getMessage());
    }

    @Test
    @DisplayName("Inventory: 在庫の範囲なら減る")
    void take() throws OutOfStockException {
        Inventory inventory = new Inventory("クロワッサン", 3);
        inventory.take(2);
        assertEquals(1, inventory.getStock());
        inventory.take(1);
        assertEquals(0, inventory.getStock(), "ちょうど在庫分は注文できる");
    }

    @Test
    @DisplayName("Inventory: 在庫より多いと OutOfStockException、在庫は減らない")
    void outOfStock() {
        Inventory inventory = new Inventory("カフェラテ", 1);
        OutOfStockException e = assertThrows(OutOfStockException.class, () -> inventory.take(2));
        assertEquals("カフェラテの在庫が足りません(注文2、残り1)", e.getMessage());
        assertEquals(1, inventory.getStock());
    }

    @Test
    @DisplayName("Inventory: 0以下の個数は IllegalArgumentException")
    void invalidQuantity() {
        Inventory inventory = new Inventory("カフェラテ", 5);
        assertThrows(IllegalArgumentException.class, () -> inventory.take(0));
        assertThrows(IllegalArgumentException.class, () -> inventory.take(-1));
        assertEquals(5, inventory.getStock());
    }

    @Test
    @DisplayName("OrderService.tryOrder: 例外を外に漏らさず、結果を文字列で返す")
    void tryOrder() {
        Inventory inventory = new Inventory("チーズケーキ", 2);
        assertEquals("注文を受け付けました", OrderService.tryOrder(inventory, 1));
        assertEquals("チーズケーキの在庫が足りません(注文3、残り1)", OrderService.tryOrder(inventory, 3));
        assertEquals("個数が正しくありません", OrderService.tryOrder(inventory, 0));
        assertEquals(1, inventory.getStock());
    }
}
'''}))

# ---------- s17 ----------
EX.append(dict(pkg="s17_collections", start={
    "MenuItem.java": r'''package cafe.s17_collections;

public record MenuItem(String name, int price) {
}
''',
    "Menu.java": r'''package cafe.s17_collections;

import java.util.List;

public class Menu {
    // TODO: 名前 → 価格 の Map を、登録順を保つ形で持つ

    public void add(String name, int price) {
        // TODO
    }

    // 価格を返す。ない名前なら IllegalArgumentException
    public int priceOf(String name) {
        // TODO
        return 0;
    }

    // 登録順の名前のリスト
    public List<String> names() {
        // TODO
        return List.of();
    }
}
''',
    "Order.java": r'''package cafe.s17_collections;

import java.util.Set;

public class Order {
    // TODO: 注文された品名の List を持つ

    public void add(String name) {
        // TODO
    }

    // その品の注文数
    public int count(String name) {
        // TODO
        return 0;
    }

    // 重複を除いた品名(注文順)
    public Set<String> kinds() {
        // TODO
        return Set.of();
    }

    // メニューの価格で計算した合計金額
    public int total(Menu menu) {
        // TODO
        return 0;
    }
}
''',
    "Sorting.java": r'''package cafe.s17_collections;

import java.util.List;

public class Sorting {
    // 安い順(同じ価格なら名前順)に並べた「新しいリスト」を返す。元のリストは変えない
    public static List<MenuItem> byPrice(List<MenuItem> items) {
        // TODO
        return items;
    }
}
'''}, answer={
    "Menu.java": r'''package cafe.s17_collections;

import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

public class Menu {
    private final Map<String, Integer> prices = new LinkedHashMap<>();

    public void add(String name, int price) {
        prices.put(name, price);
    }

    public int priceOf(String name) {
        Integer price = prices.get(name);
        if (price == null) {
            throw new IllegalArgumentException(name + " はメニューにありません");
        }
        return price;
    }

    public List<String> names() {
        return new ArrayList<>(prices.keySet());
    }
}
''',
    "Order.java": r'''package cafe.s17_collections;

import java.util.ArrayList;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Set;

public class Order {
    private final List<String> items = new ArrayList<>();

    public void add(String name) {
        items.add(name);
    }

    public int count(String name) {
        int count = 0;
        for (String item : items) {
            if (item.equals(name)) {
                count++;
            }
        }
        return count;
    }

    public Set<String> kinds() {
        return new LinkedHashSet<>(items);
    }

    public int total(Menu menu) {
        int sum = 0;
        for (String item : items) {
            sum += menu.priceOf(item);
        }
        return sum;
    }
}
''',
    "Sorting.java": r'''package cafe.s17_collections;

import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;

public class Sorting {
    public static List<MenuItem> byPrice(List<MenuItem> items) {
        List<MenuItem> sorted = new ArrayList<>(items);
        sorted.sort(Comparator.comparingInt(MenuItem::price).thenComparing(MenuItem::name));
        return sorted;
    }
}
'''}, test={"CollectionsTest.java": r'''package cafe.s17_collections;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

import java.util.List;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

class CollectionsTest {
    private Menu menu() {
        Menu menu = new Menu();
        menu.add("ブレンドコーヒー", 480);
        menu.add("カフェラテ", 520);
        menu.add("チーズケーキ", 450);
        return menu;
    }

    @Test
    @DisplayName("Menu: 名前で価格を引け、ない名前は例外")
    void menuPrice() {
        Menu menu = menu();
        assertEquals(520, menu.priceOf("カフェラテ"));
        assertThrows(IllegalArgumentException.class, () -> menu.priceOf("カフェモカ"));
    }

    @Test
    @DisplayName("Menu: 名前は登録順、同じ名前の add は価格の上書き")
    void menuNames() {
        Menu menu = menu();
        menu.add("カフェラテ", 540);
        assertEquals(List.of("ブレンドコーヒー", "カフェラテ", "チーズケーキ"), menu.names());
        assertEquals(540, menu.priceOf("カフェラテ"));
    }

    @Test
    @DisplayName("Order: 品ごとの注文数・種類・合計")
    void order() {
        Order order = new Order();
        order.add("カフェラテ");
        order.add("チーズケーキ");
        order.add("カフェラテ");
        assertEquals(2, order.count("カフェラテ"));
        assertEquals(0, order.count("ブレンドコーヒー"));
        assertEquals(List.of("カフェラテ", "チーズケーキ"), List.copyOf(order.kinds()));
        assertEquals(1490, order.total(menu()));
    }

    @Test
    @DisplayName("Sorting.byPrice: 安い順、同じ価格なら名前順。元のリストは変えない")
    void byPrice() {
        List<MenuItem> items = List.of(
            new MenuItem("カフェラテ", 520),
            new MenuItem("クロワッサン", 320),
            new MenuItem("チーズケーキ", 450),
            new MenuItem("アイスティー", 450)
        );
        List<MenuItem> sorted = Sorting.byPrice(items);
        assertEquals(List.of("クロワッサン", "アイスティー", "チーズケーキ", "カフェラテ"),
            sorted.stream().map(MenuItem::name).toList());
        assertEquals("カフェラテ", items.get(0).name(), "元のリストは並べ替えない");
    }
}
'''}))

# ---------- s18 ----------
EX.append(dict(pkg="s18_streams", start={
    "Sale.java": r'''package cafe.s18_streams;

public record Sale(String item, String category, int price, int hour) {
}
''',
    "SalesReport.java": r'''package cafe.s18_streams;

import java.util.List;
import java.util.Map;
import java.util.Optional;

// for 文を使わず、Stream で書く
public class SalesReport {
    private final List<Sale> sales;

    public SalesReport(List<Sale> sales) {
        this.sales = sales;
    }

    // 売上合計
    public int total() {
        // TODO
        return 0;
    }

    // price 円以上で売れた品の名前(重複なし、最初に出てきた順)
    public List<String> itemsAtLeast(int price) {
        // TODO
        return List.of();
    }

    // カテゴリごとの売上合計
    public Map<String, Integer> totalByCategory() {
        // TODO
        return Map.of();
    }

    // 品ごとの販売数
    public Map<String, Long> countByItem() {
        // TODO
        return Map.of();
    }

    // 最も多く売れた品の名前(売上が0件なら空)
    public Optional<String> bestSeller() {
        // TODO
        return Optional.empty();
    }
}
'''}, answer={"SalesReport.java": r'''package cafe.s18_streams;

import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.stream.Collectors;

public class SalesReport {
    private final List<Sale> sales;

    public SalesReport(List<Sale> sales) {
        this.sales = sales;
    }

    public int total() {
        return sales.stream().mapToInt(Sale::price).sum();
    }

    public List<String> itemsAtLeast(int price) {
        return sales.stream()
            .filter(s -> s.price() >= price)
            .map(Sale::item)
            .distinct()
            .toList();
    }

    public Map<String, Integer> totalByCategory() {
        return sales.stream()
            .collect(Collectors.groupingBy(Sale::category, Collectors.summingInt(Sale::price)));
    }

    public Map<String, Long> countByItem() {
        return sales.stream()
            .collect(Collectors.groupingBy(Sale::item, Collectors.counting()));
    }

    public Optional<String> bestSeller() {
        return countByItem().entrySet().stream()
            .max(Map.Entry.comparingByValue())
            .map(Map.Entry::getKey);
    }
}
'''}, test={"StreamsTest.java": r'''package cafe.s18_streams;

import static org.junit.jupiter.api.Assertions.assertEquals;

import java.util.List;
import java.util.Map;
import java.util.Optional;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

class StreamsTest {
    private final List<Sale> sales = List.of(
        new Sale("カフェラテ", "ドリンク", 520, 9),
        new Sale("チーズケーキ", "フード", 450, 10),
        new Sale("ブレンドコーヒー", "ドリンク", 480, 10),
        new Sale("カフェラテ", "ドリンク", 520, 13),
        new Sale("ホットサンド", "フード", 650, 12),
        new Sale("カフェラテ", "ドリンク", 520, 15)
    );
    private final SalesReport report = new SalesReport(sales);

    @Test
    @DisplayName("total: 売上合計")
    void total() {
        assertEquals(3140, report.total());
    }

    @Test
    @DisplayName("itemsAtLeast: 重複なし・最初に出てきた順")
    void itemsAtLeast() {
        assertEquals(List.of("カフェラテ", "ホットサンド"), report.itemsAtLeast(500));
        assertEquals(List.of("カフェラテ", "ブレンドコーヒー", "ホットサンド"), report.itemsAtLeast(480));
    }

    @Test
    @DisplayName("totalByCategory: カテゴリごとの売上合計")
    void totalByCategory() {
        assertEquals(Map.of("ドリンク", 2040, "フード", 1100), report.totalByCategory());
    }

    @Test
    @DisplayName("countByItem: 品ごとの販売数")
    void countByItem() {
        assertEquals(Map.of("カフェラテ", 3L, "チーズケーキ", 1L, "ブレンドコーヒー", 1L, "ホットサンド", 1L), report.countByItem());
    }

    @Test
    @DisplayName("bestSeller: 最も多く売れた品。売上0件なら空")
    void bestSeller() {
        assertEquals(Optional.of("カフェラテ"), report.bestSeller());
        assertEquals(Optional.empty(), new SalesReport(List.of()).bestSeller());
    }
}
'''}))

# ---------- s19 ----------
S19_BUGGY = r'''package cafe.s19_testing;

// ポイントカード。どこかにバグがある。テストを書いて見つけ、直そう
public class PointCard {
    private int points;

    // 100円ごとに1ポイント(端数は切り捨て)
    public void earn(int amount) {
        points += amount / 100;
    }

    // ポイントを使う。0以下や、持っているより多いポイントは IllegalArgumentException
    public void use(int usePoints) {
        if (usePoints <= 0 || usePoints >= points) {
            throw new IllegalArgumentException("使えるポイントは1〜" + points + "です");
        }
        points -= usePoints;
    }

    public int getPoints() {
        return points;
    }
}
'''
EX.append(dict(pkg="s19_testing", start={"PointCard.java": S19_BUGGY}, answer={"PointCard.java": S19_BUGGY.replace(
    "// ポイントカード。どこかにバグがある。テストを書いて見つけ、直そう\n", "").replace("usePoints >= points", "usePoints > points")},
    test={
    "PointCardTest.java": r'''package cafe.s19_testing;

import static org.junit.jupiter.api.Assertions.assertEquals;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

// あなたが書くテスト。例を1つ書いておいたので、まねして増やそう
class PointCardTest {
    @Test
    @DisplayName("1050円の買い物で10ポイントたまる")
    void earn() {
        // 準備
        PointCard card = new PointCard();
        // 実行
        card.earn(1050);
        // 確認
        assertEquals(10, card.getPoints());
    }

    // TODO: 「ためたポイントの一部を使うと、その分減る」テストを書く

    // TODO: 「持っているポイントをちょうど全部使える」テストを書く

    // TODO: 「持っているより多いポイントを使うと IllegalArgumentException」のテストを書く(assertThrows を使う)
}
''',
    "PointCardSpecTest.java": r'''package cafe.s19_testing;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

// 採点用のテスト(このファイルは書き換えない)
class PointCardSpecTest {
    @Test
    @DisplayName("100円ごとに1ポイント(端数切り捨て)")
    void earn() {
        PointCard card = new PointCard();
        card.earn(1050);
        card.earn(99);
        assertEquals(10, card.getPoints());
    }

    @Test
    @DisplayName("一部を使うとその分減る")
    void usePart() {
        PointCard card = new PointCard();
        card.earn(1000);
        card.use(3);
        assertEquals(7, card.getPoints());
    }

    @Test
    @DisplayName("持っているポイントをちょうど全部使える")
    void useAll() {
        PointCard card = new PointCard();
        card.earn(500);
        card.use(5);
        assertEquals(0, card.getPoints());
    }

    @Test
    @DisplayName("持っているより多い・0以下のポイントは使えない")
    void useInvalid() {
        PointCard card = new PointCard();
        card.earn(500);
        assertThrows(IllegalArgumentException.class, () -> card.use(6));
        assertThrows(IllegalArgumentException.class, () -> card.use(0));
        assertEquals(5, card.getPoints());
    }
}
'''},
    answer_test={"PointCardTest.java": r'''package cafe.s19_testing;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

class PointCardTest {
    @Test
    @DisplayName("1050円の買い物で10ポイントたまる")
    void earn() {
        PointCard card = new PointCard();
        card.earn(1050);
        assertEquals(10, card.getPoints());
    }

    @Test
    @DisplayName("ためたポイントの一部を使うと、その分減る")
    void usePart() {
        PointCard card = new PointCard();
        card.earn(1000);
        card.use(3);
        assertEquals(7, card.getPoints());
    }

    @Test
    @DisplayName("持っているポイントをちょうど全部使える")
    void useAll() {
        PointCard card = new PointCard();
        card.earn(500);
        card.use(5);
        assertEquals(0, card.getPoints());
    }

    @Test
    @DisplayName("持っているより多いポイントを使うと IllegalArgumentException")
    void useTooMany() {
        PointCard card = new PointCard();
        card.earn(500);
        assertThrows(IllegalArgumentException.class, () -> card.use(6));
    }
}
'''}))


def write(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)


for ex in EX:
    pkg = ex["pkg"]
    base = os.path.join(ROOT, "basics", "src")
    ans = os.path.join(ROOT, "answers", "basics", "src")
    for name, content in ex["start"].items():
        write(os.path.join(base, "main", "java", "cafe", pkg, name), content)
    merged = dict(ex["start"])
    merged.update(ex["answer"])
    for name, content in merged.items():
        write(os.path.join(ans, "main", "java", "cafe", pkg, name), content)
    for name, content in ex["test"].items():
        write(os.path.join(base, "test", "java", "cafe", pkg, name), content)
    for name, content in ex.get("answer_test", {}).items():
        write(os.path.join(ans, "test", "java", "cafe", pkg, name), content)
    print("wrote", pkg)
