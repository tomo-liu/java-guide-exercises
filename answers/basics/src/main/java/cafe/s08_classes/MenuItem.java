package cafe.s08_classes;

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
