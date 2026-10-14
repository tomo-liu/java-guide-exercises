package cafe.s03_operators;

public class Main {
    public static void main(String[] args) {
        int coffeePrice = 480;
        int coffeeCount = 2;
        int cakePrice = 450;
        int cakeCount = 1;
        int taxRate = 10;
        int people = 2;

        int subtotal = coffeePrice * coffeeCount + cakePrice * cakeCount;
        int total = subtotal * (100 + taxRate) / 100;
        int perPerson = total / people;

        System.out.println("小計: " + subtotal + "円");
        System.out.println("税込: " + total + "円");
        System.out.println("1人あたり: " + perPerson + "円");
    }
}
