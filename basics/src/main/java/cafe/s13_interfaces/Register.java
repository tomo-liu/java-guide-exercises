package cafe.s13_interfaces;

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
