package cafe.s09_references;

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
