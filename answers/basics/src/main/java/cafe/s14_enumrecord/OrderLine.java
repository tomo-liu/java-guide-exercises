package cafe.s14_enumrecord;

public record OrderLine(String name, int unitPrice, Size size, int quantity) {
    public int subtotal() {
        return (unitPrice + size.extra()) * quantity;
    }
}
