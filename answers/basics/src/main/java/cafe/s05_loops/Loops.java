package cafe.s05_loops;

public class Loops {
    public static String stampCard(int stamps) {
        String card = "";
        for (int i = 0; i < 10; i++) {
            if (i < stamps) {
                card += "●";
            } else {
                card += "○";
            }
        }
        return card;
    }

    public static int cupsToReach(int goal) {
        int sales = 0;
        int cups = 0;
        while (sales < goal) {
            sales += 480;
            cups++;
        }
        return cups;
    }

    public static int total(int[] prices) {
        int sum = 0;
        for (int price : prices) {
            sum += price;
        }
        return sum;
    }
}
