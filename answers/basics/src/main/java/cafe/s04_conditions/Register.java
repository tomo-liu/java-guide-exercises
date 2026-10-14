package cafe.s04_conditions;

public class Register {
    public static int taxRate(boolean takeout) {
        return takeout ? 8 : 10;
    }

    public static int discount(int total) {
        if (total >= 2000) {
            return 200;
        } else if (total >= 1000) {
            return 100;
        } else {
            return 0;
        }
    }

    public static int priceOf(String name) {
        return switch (name) {
            case "ブレンドコーヒー" -> 480;
            case "カフェラテ" -> 520;
            case "抹茶ラテ" -> 560;
            case "チーズケーキ" -> 450;
            case "ホットサンド" -> 650;
            case "クロワッサン" -> 320;
            default -> -1;
        };
    }
}
