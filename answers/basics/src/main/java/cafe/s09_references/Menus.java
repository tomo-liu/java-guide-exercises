package cafe.s09_references;

public class Menus {
    public static MenuItem findByName(MenuItem[] menu, String name) {
        for (MenuItem item : menu) {
            if (item.name.equals(name)) {
                return item;
            }
        }
        return null;
    }

    public static void raiseAll(MenuItem[] menu, int amount) {
        for (MenuItem item : menu) {
            item.price += amount;
        }
    }

    public static MenuItem copyOf(MenuItem item) {
        return new MenuItem(item.name, item.price);
    }
}
