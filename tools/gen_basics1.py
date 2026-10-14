# 課題リポジトリ basics の s01〜s10 を生成する。
# START: 読者が受け取る開始コード / ANSWER: 解答(START を上書きするファイルだけ) / TEST: 採点テスト
import os, sys

ROOT = sys.argv[1]

CAPTURE = r'''
    private static String run() {
        PrintStream original = System.out;
        ByteArrayOutputStream buffer = new ByteArrayOutputStream();
        System.setOut(new PrintStream(buffer, true, StandardCharsets.UTF_8));
        try {
            Main.main(new String[0]);
        } finally {
            System.setOut(original);
        }
        return buffer.toString(StandardCharsets.UTF_8).replace("\r\n", "\n");
    }
'''

CAPTURE_IMPORTS = r'''import static org.junit.jupiter.api.Assertions.assertEquals;

import java.io.ByteArrayOutputStream;
import java.io.PrintStream;
import java.nio.charset.StandardCharsets;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
'''

EX = []

# ---------- s01 ----------
EX.append(dict(pkg="s01_hello", start={"Main.java": r'''package cafe.s01_hello;

public class Main {
    public static void main(String[] args) {
        // TODO: 「ひだまりカフェ、開店です!」と「営業時間 8:00-20:00」の2行を出力する
    }
}
'''}, answer={"Main.java": r'''package cafe.s01_hello;

public class Main {
    public static void main(String[] args) {
        System.out.println("ひだまりカフェ、開店です!");
        System.out.println("営業時間 8:00-20:00");
    }
}
'''}, test={"HelloTest.java": r'''package cafe.s01_hello;

''' + CAPTURE_IMPORTS + r'''
class HelloTest {
    @Test
    @DisplayName("開店のあいさつと営業時間の2行を出力する")
    void printsGreeting() {
        assertEquals("ひだまりカフェ、開店です!\n営業時間 8:00-20:00\n", run());
    }
''' + CAPTURE + r'''}
'''}))

# ---------- s02 ----------
EX.append(dict(pkg="s02_variables", start={"Main.java": r'''package cafe.s02_variables;

public class Main {
    public static void main(String[] args) {
        // TODO: shopName(String)・coffeePrice(int)・cakePrice(int)・TAX_RATE(final int)を宣言する

        // TODO: 変数を使って、次の4行を出力する
        // ひだまりカフェ
        // ブレンドコーヒー: 480円
        // チーズケーキ: 450円
        // 消費税率: 10%
    }
}
'''}, answer={"Main.java": r'''package cafe.s02_variables;

public class Main {
    public static void main(String[] args) {
        String shopName = "ひだまりカフェ";
        int coffeePrice = 480;
        int cakePrice = 450;
        final int TAX_RATE = 10;

        System.out.println(shopName);
        System.out.println("ブレンドコーヒー: " + coffeePrice + "円");
        System.out.println("チーズケーキ: " + cakePrice + "円");
        System.out.println("消費税率: " + TAX_RATE + "%");
    }
}
'''}, test={"VariablesTest.java": r'''package cafe.s02_variables;

''' + CAPTURE_IMPORTS + r'''
class VariablesTest {
    @Test
    @DisplayName("店名・2品の価格・税率の4行を出力する")
    void printsMenu() {
        assertEquals("ひだまりカフェ\nブレンドコーヒー: 480円\nチーズケーキ: 450円\n消費税率: 10%\n", run());
    }
''' + CAPTURE + r'''}
'''}))

# ---------- s03 ----------
EX.append(dict(pkg="s03_operators", start={"Main.java": r'''package cafe.s03_operators;

public class Main {
    public static void main(String[] args) {
        int coffeePrice = 480;
        int coffeeCount = 2;
        int cakePrice = 450;
        int cakeCount = 1;
        int taxRate = 10;
        int people = 2;

        // TODO: 小計・税込(1円未満切り捨て)・1人あたり(切り捨て)を計算して、次の3行を出力する
        // 小計: 1410円
        // 税込: 1551円
        // 1人あたり: 775円
    }
}
'''}, answer={"Main.java": r'''package cafe.s03_operators;

public class Main {
    public static void main(String[] args) {
        int coffeePrice = 480;
        int coffeeCount = 2;
        int cakePrice = 450;
        int cakeCount = 1;
        int taxRate = 10;
        int people = 2;

        int subtotal = coffeePrice * coffeeCount + cakePrice * cakeCount;
        int total = subtotal * (100 + taxRate) / 100;
        int perPerson = total / people;

        System.out.println("小計: " + subtotal + "円");
        System.out.println("税込: " + total + "円");
        System.out.println("1人あたり: " + perPerson + "円");
    }
}
'''}, test={"OperatorsTest.java": r'''package cafe.s03_operators;

''' + CAPTURE_IMPORTS + r'''
class OperatorsTest {
    @Test
    @DisplayName("小計・税込・1人あたりの3行を出力する")
    void printsReceipt() {
        assertEquals("小計: 1410円\n税込: 1551円\n1人あたり: 775円\n", run());
    }
''' + CAPTURE + r'''}
'''}))

# ---------- s04 ----------
EX.append(dict(pkg="s04_conditions", start={"Register.java": r'''package cafe.s04_conditions;

public class Register {
    // 持ち帰りなら 8、店内なら 10 を返す
    public static int taxRate(boolean takeout) {
        // TODO
        return 0;
    }

    // 2000円以上なら 200、1000円以上なら 100、それ以外は 0 を返す
    public static int discount(int total) {
        // TODO
        return 0;
    }

    // switch を使い、メニュー6品の税抜価格を返す。メニューにない名前なら -1
    public static int priceOf(String name) {
        // TODO
        return 0;
    }
}
'''}, answer={"Register.java": r'''package cafe.s04_conditions;

public class Register {
    public static int taxRate(boolean takeout) {
        return takeout ? 8 : 10;
    }

    public static int discount(int total) {
        if (total >= 2000) {
            return 200;
        } else if (total >= 1000) {
            return 100;
        } else {
            return 0;
        }
    }

    public static int priceOf(String name) {
        return switch (name) {
            case "ブレンドコーヒー" -> 480;
            case "カフェラテ" -> 520;
            case "抹茶ラテ" -> 560;
            case "チーズケーキ" -> 450;
            case "ホットサンド" -> 650;
            case "クロワッサン" -> 320;
            default -> -1;
        };
    }
}
'''}, test={"ConditionsTest.java": r'''package cafe.s04_conditions;

import static org.junit.jupiter.api.Assertions.assertEquals;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

class ConditionsTest {
    @Test
    @DisplayName("taxRate: 持ち帰りは8、店内は10")
    void taxRate() {
        assertEquals(8, Register.taxRate(true));
        assertEquals(10, Register.taxRate(false));
    }

    @Test
    @DisplayName("discount: 2000円以上は200、1000円以上は100、それ以外は0")
    void discount() {
        assertEquals(200, Register.discount(2500), "2500円のとき");
        assertEquals(200, Register.discount(2000), "ちょうど2000円のとき");
        assertEquals(100, Register.discount(1999), "1999円のとき");
        assertEquals(100, Register.discount(1000), "ちょうど1000円のとき");
        assertEquals(0, Register.discount(999), "999円のとき");
        assertEquals(0, Register.discount(0), "0円のとき");
    }

    @Test
    @DisplayName("priceOf: メニュー6品の価格と、ない名前は-1")
    void priceOf() {
        assertEquals(480, Register.priceOf("ブレンドコーヒー"));
        assertEquals(520, Register.priceOf("カフェラテ"));
        assertEquals(560, Register.priceOf("抹茶ラテ"));
        assertEquals(450, Register.priceOf("チーズケーキ"));
        assertEquals(650, Register.priceOf("ホットサンド"));
        assertEquals(320, Register.priceOf("クロワッサン"));
        assertEquals(-1, Register.priceOf("カフェモカ"));
    }
}
'''}))

# ---------- s05 ----------
EX.append(dict(pkg="s05_loops", start={"Loops.java": r'''package cafe.s05_loops;

public class Loops {
    // 10枠のスタンプカード。押した数だけ「●」、残りは「○」(例:3 なら「●●●○○○○○○○」)
    public static String stampCard(int stamps) {
        // TODO
        return "";
    }

    // 1杯480円のコーヒーで、売上が goal 円以上になるまでに必要な杯数(while を使う)
    public static int cupsToReach(int goal) {
        // TODO
        return 0;
    }

    // 拡張forで価格をすべて足した合計
    public static int total(int[] prices) {
        // TODO
        return 0;
    }
}
'''}, answer={"Loops.java": r'''package cafe.s05_loops;

public class Loops {
    public static String stampCard(int stamps) {
        String card = "";
        for (int i = 0; i < 10; i++) {
            if (i < stamps) {
                card += "●";
            } else {
                card += "○";
            }
        }
        return card;
    }

    public static int cupsToReach(int goal) {
        int sales = 0;
        int cups = 0;
        while (sales < goal) {
            sales += 480;
            cups++;
        }
        return cups;
    }

    public static int total(int[] prices) {
        int sum = 0;
        for (int price : prices) {
            sum += price;
        }
        return sum;
    }
}
'''}, test={"LoopsTest.java": r'''package cafe.s05_loops;

import static org.junit.jupiter.api.Assertions.assertEquals;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

class LoopsTest {
    @Test
    @DisplayName("stampCard: 押した数だけ●、残りは○の10文字")
    void stampCard() {
        assertEquals("●●●○○○○○○○", Loops.stampCard(3));
        assertEquals("○○○○○○○○○○", Loops.stampCard(0));
        assertEquals("●●●●●●●●●●", Loops.stampCard(10));
    }

    @Test
    @DisplayName("cupsToReach: 売上が目標に届くまでの杯数")
    void cupsToReach() {
        assertEquals(11, Loops.cupsToReach(5000), "5000円のとき(11杯で5280円)");
        assertEquals(1, Loops.cupsToReach(480), "ちょうど1杯分のとき");
        assertEquals(2, Loops.cupsToReach(481), "1杯分を1円超えるとき");
        assertEquals(0, Loops.cupsToReach(0), "目標0円のとき");
    }

    @Test
    @DisplayName("total: 全部の価格の合計")
    void total() {
        assertEquals(1450, Loops.total(new int[] {480, 520, 450}));
        assertEquals(0, Loops.total(new int[] {}));
    }
}
'''}))

# ---------- s06 ----------
EX.append(dict(pkg="s06_arrays", start={"Order.java": r'''package cafe.s06_arrays;

public class Order {
    // 合計
    public static int total(int[] prices) {
        // TODO
        return 0;
    }

    // 最大値(配列は1個以上ある前提でよい)
    public static int max(int[] prices) {
        // TODO
        return 0;
    }

    // threshold 円以上の品の数
    public static int countAtLeast(int[] prices, int threshold) {
        // TODO
        return 0;
    }

    // name と同じ名前が何番目にあるか。なければ -1
    public static int indexOf(String[] names, String name) {
        // TODO
        return 0;
    }
}
'''}, answer={"Order.java": r'''package cafe.s06_arrays;

public class Order {
    public static int total(int[] prices) {
        int sum = 0;
        for (int i = 0; i < prices.length; i++) {
            sum += prices[i];
        }
        return sum;
    }

    public static int max(int[] prices) {
        int max = prices[0];
        for (int i = 1; i < prices.length; i++) {
            if (prices[i] > max) {
                max = prices[i];
            }
        }
        return max;
    }

    public static int countAtLeast(int[] prices, int threshold) {
        int count = 0;
        for (int i = 0; i < prices.length; i++) {
            if (prices[i] >= threshold) {
                count++;
            }
        }
        return count;
    }

    public static int indexOf(String[] names, String name) {
        for (int i = 0; i < names.length; i++) {
            if (names[i].equals(name)) {
                return i;
            }
        }
        return -1;
    }
}
'''}, test={"ArraysTest.java": r'''package cafe.s06_arrays;

import static org.junit.jupiter.api.Assertions.assertEquals;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

class ArraysTest {
    private final int[] prices = {480, 520, 560, 450, 650, 320};
    private final String[] names = {"ブレンドコーヒー", "カフェラテ", "抹茶ラテ", "チーズケーキ", "ホットサンド", "クロワッサン"};

    @Test
    @DisplayName("total: 6品の合計")
    void total() {
        assertEquals(2980, Order.total(prices));
    }

    @Test
    @DisplayName("max: 最高値")
    void max() {
        assertEquals(650, Order.max(prices));
        assertEquals(320, Order.max(new int[] {320}), "1品だけのとき");
        assertEquals(480, Order.max(new int[] {480, 320}), "先頭が最大のとき");
    }

    @Test
    @DisplayName("countAtLeast: しきい値以上の数(ちょうども含む)")
    void countAtLeast() {
        assertEquals(3, Order.countAtLeast(prices, 500));
        assertEquals(4, Order.countAtLeast(prices, 480), "480円ちょうども数える");
        assertEquals(0, Order.countAtLeast(prices, 1000));
    }

    @Test
    @DisplayName("indexOf: 名前の位置。なければ-1")
    void indexOf() {
        assertEquals(0, Order.indexOf(names, "ブレンドコーヒー"));
        assertEquals(3, Order.indexOf(names, "チーズケーキ"));
        assertEquals(-1, Order.indexOf(names, "カフェモカ"));
        // == で比べると見つからない、実行中に作った文字列でも探せること
        String latte = "カフェ" + "ラテ".repeat(1);
        assertEquals(1, Order.indexOf(names, latte), "文字列は equals で比べる");
    }
}
'''}))

# ---------- s07 ----------
EX.append(dict(pkg="s07_methods", start={"Register.java": r'''package cafe.s07_methods;

public class Register {
    // TODO: 次の4つの static メソッドを、自分で定義する(public static で)
    //   withTax(int price, boolean takeout)                       … 税込価格(持ち帰り8%・店内10%、切り捨て)
    //   subtotal(int[] prices, int[] quantities)                  … 価格 × 個数 の合計(税抜)
    //   total(int[] prices, int[] quantities, boolean takeout)    … 小計に税を加えた支払額
    //   total(int[] prices, int[] quantities)                     … 店内として計算するオーバーロード
}
'''}, answer={"Register.java": r'''package cafe.s07_methods;

public class Register {
    public static int withTax(int price, boolean takeout) {
        int rate = takeout ? 8 : 10;
        return price * (100 + rate) / 100;
    }

    public static int subtotal(int[] prices, int[] quantities) {
        int sum = 0;
        for (int i = 0; i < prices.length; i++) {
            sum += prices[i] * quantities[i];
        }
        return sum;
    }

    public static int total(int[] prices, int[] quantities, boolean takeout) {
        return withTax(subtotal(prices, quantities), takeout);
    }

    public static int total(int[] prices, int[] quantities) {
        return total(prices, quantities, false);
    }
}
'''}, test={"MethodsTest.java": r'''package cafe.s07_methods;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.junit.jupiter.api.Assertions.fail;

import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.lang.reflect.Modifier;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

// この課題ではメソッドを自分で定義するので、テストは名前と引数の型からメソッドを探して呼び出す
// (まだ定義していなくても、他の課題のテストがコンパイルできるようにするため)。
class MethodsTest {
    private static Object call(String name, Class<?>[] types, Object... args) {
        try {
            Method m = Register.class.getDeclaredMethod(name, types);
            assertTrue(Modifier.isStatic(m.getModifiers()), name + " は static にする");
            m.setAccessible(true);
            return m.invoke(null, args);
        } catch (NoSuchMethodException e) {
            fail("メソッド " + name + " が見つかりません。名前と引数の型を確かめよう");
        } catch (IllegalAccessException | InvocationTargetException e) {
            fail(name + " の呼び出しで問題が起きました: " + e.getCause());
        }
        return null;
    }

    private final int[] prices = {480, 450};
    private final int[] quantities = {2, 1};

    @Test
    @DisplayName("withTax: 持ち帰り8%・店内10%")
    void withTax() {
        assertEquals(518, call("withTax", new Class<?>[] {int.class, boolean.class}, 480, true));
        assertEquals(528, call("withTax", new Class<?>[] {int.class, boolean.class}, 480, false));
    }

    @Test
    @DisplayName("subtotal: 価格 × 個数 の合計")
    void subtotal() {
        assertEquals(1410, call("subtotal", new Class<?>[] {int[].class, int[].class}, prices, quantities));
    }

    @Test
    @DisplayName("total(3引数): 小計に税を加える")
    void total() {
        Class<?>[] types = {int[].class, int[].class, boolean.class};
        assertEquals(1551, call("total", types, prices, quantities, false));
        assertEquals(1522, call("total", types, prices, quantities, true));
    }

    @Test
    @DisplayName("total(2引数): 店内として計算するオーバーロード")
    void totalEatIn() {
        assertEquals(1551, call("total", new Class<?>[] {int[].class, int[].class}, prices, quantities));
    }
}
'''}))

# ---------- s08 ----------
EX.append(dict(pkg="s08_classes", start={"MenuItem.java": r'''package cafe.s08_classes;

public class MenuItem {
    // TODO: フィールド name(String)と price(int)を追加する

    public MenuItem(String name, int price) {
        // TODO: this を使って、引数をフィールドに入れる
    }

    // この品の税込価格(持ち帰り8%・店内10%、切り捨て)
    public int priceWithTax(boolean takeout) {
        // TODO
        return 0;
    }

    // 「カフェラテ(520円)」の形の文字列
    @Override
    public String toString() {
        // TODO
        return "";
    }
}
'''}, answer={"MenuItem.java": r'''package cafe.s08_classes;

public class MenuItem {
    String name;
    int price;

    public MenuItem(String name, int price) {
        this.name = name;
        this.price = price;
    }

    public int priceWithTax(boolean takeout) {
        int rate = takeout ? 8 : 10;
        return price * (100 + rate) / 100;
    }

    @Override
    public String toString() {
        return name + "(" + price + "円)";
    }
}
'''}, test={"MenuItemTest.java": r'''package cafe.s08_classes;

import static org.junit.jupiter.api.Assertions.assertEquals;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

class MenuItemTest {
    @Test
    @DisplayName("toString: 「名前(価格円)」の形")
    void toStringFormat() {
        assertEquals("カフェラテ(520円)", new MenuItem("カフェラテ", 520).toString());
        assertEquals("クロワッサン(320円)", new MenuItem("クロワッサン", 320).toString());
    }

    @Test
    @DisplayName("priceWithTax: その品の税込価格")
    void priceWithTax() {
        MenuItem coffee = new MenuItem("ブレンドコーヒー", 480);
        assertEquals(518, coffee.priceWithTax(true));
        assertEquals(528, coffee.priceWithTax(false));
    }

    @Test
    @DisplayName("オブジェクトごとに別々の値を持つ")
    void eachObjectHasOwnValues() {
        MenuItem a = new MenuItem("カフェラテ", 520);
        MenuItem b = new MenuItem("抹茶ラテ", 560);
        assertEquals("カフェラテ(520円)", a.toString());
        assertEquals("抹茶ラテ(560円)", b.toString());
        assertEquals(616, b.priceWithTax(false));
    }
}
'''}))

# ---------- s09 ----------
S09_MENU_ITEM = r'''package cafe.s09_references;

public class MenuItem {
    String name;
    int price;

    public MenuItem(String name, int price) {
        this.name = name;
        this.price = price;
    }

    @Override
    public String toString() {
        return name + "(" + price + "円)";
    }
}
'''
EX.append(dict(pkg="s09_references", start={"MenuItem.java": S09_MENU_ITEM, "Menus.java": r'''package cafe.s09_references;

public class Menus {
    // 名前が一致する品を返す。なければ null
    public static MenuItem findByName(MenuItem[] menu, String name) {
        // TODO
        return null;
    }

    // 全品の価格を amount 円上げる(渡された品そのものを書き換える)
    public static void raiseAll(MenuItem[] menu, int amount) {
        // TODO
    }

    // 同じ名前・価格の「別のオブジェクト」を返す
    public static MenuItem copyOf(MenuItem item) {
        // TODO
        return item;
    }
}
'''}, answer={"Menus.java": r'''package cafe.s09_references;

public class Menus {
    public static MenuItem findByName(MenuItem[] menu, String name) {
        for (MenuItem item : menu) {
            if (item.name.equals(name)) {
                return item;
            }
        }
        return null;
    }

    public static void raiseAll(MenuItem[] menu, int amount) {
        for (MenuItem item : menu) {
            item.price += amount;
        }
    }

    public static MenuItem copyOf(MenuItem item) {
        return new MenuItem(item.name, item.price);
    }
}
'''}, test={"MenusTest.java": r'''package cafe.s09_references;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotSame;
import static org.junit.jupiter.api.Assertions.assertNull;
import static org.junit.jupiter.api.Assertions.assertSame;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

class MenusTest {
    private MenuItem[] menu() {
        return new MenuItem[] {
            new MenuItem("ブレンドコーヒー", 480),
            new MenuItem("カフェラテ", 520),
        };
    }

    @Test
    @DisplayName("findByName: 見つかった品そのものを返し、なければ null")
    void findByName() {
        MenuItem[] menu = menu();
        assertSame(menu[1], Menus.findByName(menu, "カフェラテ"), "配列に入っている品そのものを返す");
        assertNull(Menus.findByName(menu, "カフェモカ"));
        String name = "ブレンド" + "コーヒー".repeat(1);
        assertSame(menu[0], Menus.findByName(menu, name), "文字列は equals で比べる");
    }

    @Test
    @DisplayName("raiseAll: 渡された品そのものが値上がりする")
    void raiseAll() {
        MenuItem[] menu = menu();
        MenuItem latte = menu[1];
        Menus.raiseAll(menu, 20);
        assertEquals(500, menu[0].price);
        assertEquals(540, latte.price, "同じオブジェクトを指す別の変数からも値上がりが見える");
    }

    @Test
    @DisplayName("copyOf: 中身が同じ別のオブジェクトを返し、コピーを変えても元は変わらない")
    void copyOf() {
        MenuItem original = new MenuItem("カフェラテ", 520);
        MenuItem copy = Menus.copyOf(original);
        assertNotSame(original, copy, "同じオブジェクトではなく、new で作り直す");
        assertEquals("カフェラテ", copy.name);
        assertEquals(520, copy.price);
        copy.price = 999;
        assertEquals(520, original.price, "コピーを変えても元は変わらない");
    }
}
'''}))

# ---------- s10 ----------
EX.append(dict(pkg="s10_encapsulation", start={"MenuItem.java": r'''package cafe.s10_encapsulation;

public class MenuItem {
    // TODO: フィールドを private にする
    String name;
    int price;

    public MenuItem(String name, int price) {
        this.name = name;
        this.price = price;
    }

    public String getName() {
        // TODO
        return null;
    }

    public int getPrice() {
        // TODO
        return 0;
    }

    // この品の税込価格(持ち帰り8%・店内10%、切り捨て)
    public int priceWithTax(boolean takeout) {
        // TODO
        return 0;
    }

    // 0以下なら変更せず false、変更したら true
    public boolean changePrice(int newPrice) {
        // TODO
        return false;
    }
}
''', "StampCard.java": r'''package cafe.s10_encapsulation;

public class StampCard {
    // TODO: スタンプ数と無料券の枚数を private なフィールドで持つ

    // スタンプを1つ押す。10個たまったら0に戻して、無料券を1枚増やす
    public void addStamp() {
        // TODO
    }

    public int getStamps() {
        // TODO
        return 0;
    }

    public int getFreeDrinks() {
        // TODO
        return 0;
    }
}
'''}, answer={"MenuItem.java": r'''package cafe.s10_encapsulation;

public class MenuItem {
    private final String name;
    private int price;

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

    public int priceWithTax(boolean takeout) {
        int rate = takeout ? 8 : 10;
        return price * (100 + rate) / 100;
    }

    public boolean changePrice(int newPrice) {
        if (newPrice <= 0) {
            return false;
        }
        price = newPrice;
        return true;
    }
}
''', "StampCard.java": r'''package cafe.s10_encapsulation;

public class StampCard {
    private int stamps;
    private int freeDrinks;

    public void addStamp() {
        stamps++;
        if (stamps == 10) {
            stamps = 0;
            freeDrinks++;
        }
    }

    public int getStamps() {
        return stamps;
    }

    public int getFreeDrinks() {
        return freeDrinks;
    }
}
'''}, test={"EncapsulationTest.java": r'''package cafe.s10_encapsulation;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.lang.reflect.Field;
import java.lang.reflect.Modifier;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

class EncapsulationTest {
    private static void assertAllFieldsPrivate(Class<?> type) {
        Field[] fields = type.getDeclaredFields();
        assertTrue(fields.length > 0, type.getSimpleName() + " にフィールドを用意する");
        for (Field field : fields) {
            assertTrue(Modifier.isPrivate(field.getModifiers()),
                type.getSimpleName() + " のフィールド " + field.getName() + " を private にする");
        }
    }

    @Test
    @DisplayName("MenuItem: フィールドがすべて private")
    void menuItemFieldsArePrivate() {
        assertAllFieldsPrivate(MenuItem.class);
    }

    @Test
    @DisplayName("MenuItem: getter と税込価格")
    void menuItemGetters() {
        MenuItem latte = new MenuItem("カフェラテ", 520);
        assertEquals("カフェラテ", latte.getName());
        assertEquals(520, latte.getPrice());
        assertEquals(561, latte.priceWithTax(true));
        assertEquals(572, latte.priceWithTax(false));
    }

    @Test
    @DisplayName("MenuItem: changePrice は0以下を受け付けない")
    void changePrice() {
        MenuItem latte = new MenuItem("カフェラテ", 520);
        assertFalse(latte.changePrice(-100));
        assertFalse(latte.changePrice(0));
        assertEquals(520, latte.getPrice(), "不正な値では価格は変わらない");
        assertTrue(latte.changePrice(540));
        assertEquals(540, latte.getPrice());
    }

    @Test
    @DisplayName("StampCard: フィールドがすべて private")
    void stampCardFieldsArePrivate() {
        assertAllFieldsPrivate(StampCard.class);
    }

    @Test
    @DisplayName("StampCard: 10個で無料券になり、スタンプは0に戻る")
    void stampCard() {
        StampCard card = new StampCard();
        for (int i = 0; i < 9; i++) {
            card.addStamp();
        }
        assertEquals(9, card.getStamps());
        assertEquals(0, card.getFreeDrinks());
        card.addStamp();
        assertEquals(0, card.getStamps(), "10個目で0に戻る");
        assertEquals(1, card.getFreeDrinks());
        for (int i = 0; i < 12; i++) {
            card.addStamp();
        }
        assertEquals(2, card.getStamps());
        assertEquals(2, card.getFreeDrinks());
    }
}
'''}))


def write(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)


for ex in EX:
    pkg = ex["pkg"]
    main_dir = os.path.join(ROOT, "basics", "src", "main", "java", "cafe", pkg)
    test_dir = os.path.join(ROOT, "basics", "src", "test", "java", "cafe", pkg)
    ans_dir = os.path.join(ROOT, "answers", "basics", "src", "main", "java", "cafe", pkg)
    for name, content in ex["start"].items():
        write(os.path.join(main_dir, name), content)
    merged = dict(ex["start"])
    merged.update(ex["answer"])
    for name, content in merged.items():
        write(os.path.join(ans_dir, name), content)
    for name, content in ex["test"].items():
        write(os.path.join(test_dir, name), content)
    print("wrote", pkg)
