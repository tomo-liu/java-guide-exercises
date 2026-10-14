package cafe.s11_inheritance;

public class Food extends MenuItem {
    // TODO: 温めるかどうか(boolean)を持つ private final なフィールドを追加する

    public Food(String name, int price, boolean warm) {
        super(name, price);
        // TODO: 温めるかどうかをフィールドに入れる
    }

    // TODO: describe() をオーバーライドし、温める場合は親の説明の後ろに「(温め)」を付ける
}
