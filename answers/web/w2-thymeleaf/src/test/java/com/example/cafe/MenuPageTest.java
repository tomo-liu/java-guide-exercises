package com.example.cafe;

import static org.hamcrest.Matchers.containsString;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.content;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.view;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.webmvc.test.autoconfigure.AutoConfigureMockMvc;
import org.springframework.test.web.servlet.MockMvc;

// w2: 画面(Thymeleaf)とフォームの入力チェックを確かめる
@SpringBootTest
@AutoConfigureMockMvc
class MenuPageTest {
    @Autowired
    MockMvc mockMvc;

    @Test
    @DisplayName("GET /menu: 店名とメニューが表示される")
    void menuPage() throws Exception {
        mockMvc.perform(get("/menu"))
            .andExpect(status().isOk())
            .andExpect(view().name("menu"))
            .andExpect(content().string(containsString("ひだまりカフェ")))
            .andExpect(content().string(containsString("カフェラテ")))
            .andExpect(content().string(containsString("520円")));
    }

    @Test
    @DisplayName("GET /order: 注文フォームが表示される")
    void orderForm() throws Exception {
        mockMvc.perform(get("/order"))
            .andExpect(status().isOk())
            .andExpect(view().name("order"))
            .andExpect(content().string(containsString("チーズケーキ")));
    }

    @Test
    @DisplayName("POST /order: 正しい注文なら、割引後の金額を表示する")
    void orderOk() throws Exception {
        mockMvc.perform(post("/order").param("name", "カフェラテ").param("quantity", "2"))
            .andExpect(status().isOk())
            .andExpect(view().name("order-complete"))
            .andExpect(content().string(containsString("940円")));
    }

    @Test
    @DisplayName("POST /order: 個数が0ならフォームに戻り、メッセージが出る")
    void orderInvalid() throws Exception {
        mockMvc.perform(post("/order").param("name", "カフェラテ").param("quantity", "0"))
            .andExpect(status().isOk())
            .andExpect(view().name("order"))
            .andExpect(content().string(containsString("個数は1以上にしてください")));
    }

    @Test
    @DisplayName("POST /order: 品を選ばないとフォームに戻る")
    void orderNoItem() throws Exception {
        mockMvc.perform(post("/order").param("name", "").param("quantity", "1"))
            .andExpect(view().name("order"))
            .andExpect(content().string(containsString("品を選んでください")));
    }
}
