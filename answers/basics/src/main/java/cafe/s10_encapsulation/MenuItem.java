package cafe.s10_encapsulation;

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
