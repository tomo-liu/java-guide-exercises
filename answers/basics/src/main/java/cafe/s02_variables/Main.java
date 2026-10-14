package cafe.s02_variables;

public class Main {
    public static void main(String[] args) {
        String shopName = "ひだまりカフェ";
        int coffeePrice = 480;
        int cakePrice = 450;
        final int TAX_RATE = 10;

        System.out.println(shopName);
        System.out.println("ブレンドコーヒー: " + coffeePrice + "円");
        System.out.println("チーズケーキ: " + cakePrice + "円");
        System.out.println("消費税率: " + TAX_RATE + "%");
    }
}
