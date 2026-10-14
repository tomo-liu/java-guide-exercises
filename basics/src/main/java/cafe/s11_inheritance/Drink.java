package cafe.s11_inheritance;

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
