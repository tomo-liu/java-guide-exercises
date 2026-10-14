package cafe.s12_polymorphism;

public class Drink extends MenuItem {
    private final String size;

    public Drink(String name, int price, String size) {
        super(name, price);
        this.size = size;
    }

    public String getSize() {
        return size;
    }

    @Override
    public int getPrice() {
        int extra = switch (size) {
            case "M" -> 50;
            case "L" -> 100;
            default -> 0;
        };
        return super.getPrice() + extra;
    }
}
