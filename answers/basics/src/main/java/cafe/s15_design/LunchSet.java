package cafe.s15_design;

public class LunchSet implements Priced {
    private final Priced drink;
    private final Priced food;

    public LunchSet(Priced drink, Priced food) {
        this.drink = drink;
        this.food = food;
    }

    @Override
    public String getName() {
        return drink.getName() + "と" + food.getName() + "のセット";
    }

    @Override
    public int getPrice() {
        return drink.getPrice() + food.getPrice() - 100;
    }
}
