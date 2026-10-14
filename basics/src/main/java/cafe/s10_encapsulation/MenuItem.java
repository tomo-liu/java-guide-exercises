package cafe.s10_encapsulation;

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
