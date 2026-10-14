package cafe.s16_exceptions;

// 在庫切れを表す検査例外
public class OutOfStockException extends Exception {
    // TODO: 品名・注文数・残り数を受け取り、
    //       メッセージを「カフェラテの在庫が足りません(注文2、残り1)」の形にする
    public OutOfStockException(String itemName, int requested, int remaining) {
        super("TODO");
    }
}
