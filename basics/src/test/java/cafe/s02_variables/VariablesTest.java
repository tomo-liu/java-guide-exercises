package cafe.s02_variables;

import static org.junit.jupiter.api.Assertions.assertEquals;

import java.io.ByteArrayOutputStream;
import java.io.PrintStream;
import java.nio.charset.StandardCharsets;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

class VariablesTest {
    @Test
    @DisplayName("店名・2品の価格・税率の4行を出力する")
    void printsMenu() {
        assertEquals("ひだまりカフェ\nブレンドコーヒー: 480円\nチーズケーキ: 450円\n消費税率: 10%\n", run());
    }

    private static String run() {
        PrintStream original = System.out;
        ByteArrayOutputStream buffer = new ByteArrayOutputStream();
        System.setOut(new PrintStream(buffer, true, StandardCharsets.UTF_8));
        try {
            Main.main(new String[0]);
        } finally {
            System.setOut(original);
        }
        return buffer.toString(StandardCharsets.UTF_8).replace("\r\n", "\n");
    }
}
