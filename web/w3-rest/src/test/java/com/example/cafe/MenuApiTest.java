package com.example.cafe;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.webmvc.test.autoconfigure.AutoConfigureMockMvc;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;

// w3: REST API(JSON の入出力・ステータスコード・エラー処理)を確かめる
@SpringBootTest
@AutoConfigureMockMvc
class MenuApiTest {
    @Autowired
    MockMvc mockMvc;

    @Test
    @DisplayName("GET /api/menu: 6品のJSON配列")
    void menu() throws Exception {
        mockMvc.perform(get("/api/menu"))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.length()").value(6))
            .andExpect(jsonPath("$[1].name").value("カフェラテ"))
            .andExpect(jsonPath("$[1].price").value(520));
    }

    @Test
    @DisplayName("GET /api/menu/{name}: 1品のJSON")
    void item() throws Exception {
        mockMvc.perform(get("/api/menu/{name}", "抹茶ラテ"))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.price").value(560))
            .andExpect(jsonPath("$.category").value("ドリンク"));
    }

    @Test
    @DisplayName("GET /api/menu/{name}: ない品は 404 とエラーメッセージ")
    void itemNotFound() throws Exception {
        mockMvc.perform(get("/api/menu/{name}", "カフェモカ"))
            .andExpect(status().isNotFound())
            .andExpect(jsonPath("$.message").value("カフェモカ はメニューにありません"));
    }

    @Test
    @DisplayName("POST /api/orders: 201 Created と割引後の金額")
    void order() throws Exception {
        mockMvc.perform(post("/api/orders")
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"name\": \"カフェラテ\", \"quantity\": 2}"))
            .andExpect(status().isCreated())
            .andExpect(jsonPath("$.name").value("カフェラテ"))
            .andExpect(jsonPath("$.quantity").value(2))
            .andExpect(jsonPath("$.total").value(940));
    }

    @Test
    @DisplayName("POST /api/orders: 個数が0なら 400 とエラーメッセージ")
    void orderInvalid() throws Exception {
        mockMvc.perform(post("/api/orders")
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"name\": \"カフェラテ\", \"quantity\": 0}"))
            .andExpect(status().isBadRequest())
            .andExpect(jsonPath("$.message").value("個数は1以上にしてください"));
    }
}
