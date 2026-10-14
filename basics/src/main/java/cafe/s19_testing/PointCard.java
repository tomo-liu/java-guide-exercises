package cafe.s19_testing;

// ポイントカード。どこかにバグがある。テストを書いて見つけ、直そう
public class PointCard {
    private int points;

    // 100円ごとに1ポイント(端数は切り捨て)
    public void earn(int amount) {
        points += amount / 100;
    }

    // ポイントを使う。0以下や、持っているより多いポイントは IllegalArgumentException
    public void use(int usePoints) {
        if (usePoints <= 0 || usePoints >= points) {
            throw new IllegalArgumentException("使えるポイントは1〜" + points + "です");
        }
        points -= usePoints;
    }

    public int getPoints() {
        return points;
    }
}
