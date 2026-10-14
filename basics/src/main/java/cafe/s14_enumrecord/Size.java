package cafe.s14_enumrecord;

public enum Size {
    // TODO: 追加料金(0・50・100円)とラベル("S"・"M"・"L")を持たせる
    SMALL, MEDIUM, LARGE;

    // 追加料金
    public int extra() {
        // TODO
        return -1;
    }

    // 「S」「M」「L」
    public String label() {
        // TODO
        return "";
    }
}
