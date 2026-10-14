package cafe.s15_design;

public class ReceiptPrinter {
    public String print(Order order) {
        String text = "";
        for (Priced item : order.getItems()) {
            text += item.getName() + " " + item.getPrice() + "円\n";
        }
        text += "合計 " + order.total() + "円";
        return text;
    }
}
