package cafe.s07_methods;

public class Register {
    public static int withTax(int price, boolean takeout) {
        int rate = takeout ? 8 : 10;
        return price * (100 + rate) / 100;
    }

    public static int subtotal(int[] prices, int[] quantities) {
        int sum = 0;
        for (int i = 0; i < prices.length; i++) {
            sum += prices[i] * quantities[i];
        }
        return sum;
    }

    public static int total(int[] prices, int[] quantities, boolean takeout) {
        return withTax(subtotal(prices, quantities), takeout);
    }

    public static int total(int[] prices, int[] quantities) {
        return total(prices, quantities, false);
    }
}
