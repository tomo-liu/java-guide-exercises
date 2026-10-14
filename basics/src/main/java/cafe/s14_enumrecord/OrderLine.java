package cafe.s14_enumrecord;

public record OrderLine(String name, int unitPrice, Size size, int quantity) {
    // (単価 + 追加料金)× 個数
    public int subtotal() {
        // TODO
        return 0;
    }
}
