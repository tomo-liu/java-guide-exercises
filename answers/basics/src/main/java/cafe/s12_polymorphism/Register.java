package cafe.s12_polymorphism;

public class Register {
    public static int total(MenuItem[] order) {
        int sum = 0;
        for (MenuItem item : order) {
            sum += item.getPrice();
        }
        return sum;
    }

    public static int countDrinks(MenuItem[] order) {
        int count = 0;
        for (MenuItem item : order) {
            if (item instanceof Drink) {
                count++;
            }
        }
        return count;
    }

    public static String label(MenuItem item) {
        return switch (item) {
            case Drink d -> d.getName() + "(" + d.getSize() + ")";
            case Food f when f.isWarm() -> f.getName() + "(温め)";
            default -> item.getName();
        };
    }
}
