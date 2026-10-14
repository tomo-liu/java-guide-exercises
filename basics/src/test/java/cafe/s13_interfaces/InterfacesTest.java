package cafe.s13_interfaces;

import static org.junit.jupiter.api.Assertions.assertEquals;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

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
