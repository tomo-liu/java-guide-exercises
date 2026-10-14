package cafe.s07_methods;

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
