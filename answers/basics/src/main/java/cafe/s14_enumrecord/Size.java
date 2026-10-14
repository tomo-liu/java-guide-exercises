package cafe.s14_enumrecord;

public enum Size {
    SMALL(0, "S"), MEDIUM(50, "M"), LARGE(100, "L");

    private final int extra;
    private final String label;

    Size(int extra, String label) {
        this.extra = extra;
        this.label = label;
    }

    public int extra() {
        return extra;
    }

    public String label() {
        return label;
    }
}
