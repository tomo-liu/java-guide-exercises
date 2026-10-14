package cafe.s11_inheritance;

public class Food extends MenuItem {
    private final boolean warm;

    public Food(String name, int price, boolean warm) {
        super(name, price);
        this.warm = warm;
    }

    @Override
    public String describe() {
        return warm ? super.describe() + "(温め)" : super.describe();
    }
}
