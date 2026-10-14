package cafe.s12_polymorphism;

public class Food extends MenuItem {
    private final boolean warm;

    public Food(String name, int price, boolean warm) {
        super(name, price);
        this.warm = warm;
    }

    public boolean isWarm() {
        return warm;
    }
}
