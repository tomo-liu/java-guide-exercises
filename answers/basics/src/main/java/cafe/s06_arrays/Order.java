package cafe.s06_arrays;

public class Order {
    public static int total(int[] prices) {
        int sum = 0;
        for (int i = 0; i < prices.length; i++) {
            sum += prices[i];
        }
        return sum;
    }

    public static int max(int[] prices) {
        int max = prices[0];
        for (int i = 1; i < prices.length; i++) {
            if (prices[i] > max) {
                max = prices[i];
            }
        }
        return max;
    }

    public static int countAtLeast(int[] prices, int threshold) {
        int count = 0;
        for (int i = 0; i < prices.length; i++) {
            if (prices[i] >= threshold) {
                count++;
            }
        }
        return count;
    }

    public static int indexOf(String[] names, String name) {
        for (int i = 0; i < names.length; i++) {
            if (names[i].equals(name)) {
                return i;
            }
        }
        return -1;
    }
}
