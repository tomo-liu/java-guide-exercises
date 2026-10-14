package cafe.s10_encapsulation;

public class StampCard {
    private int stamps;
    private int freeDrinks;

    public void addStamp() {
        stamps++;
        if (stamps == 10) {
            stamps = 0;
            freeDrinks++;
        }
    }

    public int getStamps() {
        return stamps;
    }

    public int getFreeDrinks() {
        return freeDrinks;
    }
}
