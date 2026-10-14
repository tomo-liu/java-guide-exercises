package cafe.s15_design;

// ドリンクとフードを「持つ」セット(継承しない)
public class LunchSet implements Priced {
    // TODO: ドリンクとフード(どちらも Priced)をフィールドで持つ

    public LunchSet(Priced drink, Priced food) {
        // TODO
    }

    // 「カフェラテとホットサンドのセット」の形
    @Override
    public String getName() {
        // TODO
        return "";
    }

    // 2つの合計から100円引き
    @Override
    public int getPrice() {
        // TODO
        return 0;
    }
}
