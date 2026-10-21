package com.example.demo;

import static org.hamcrest.Matchers.containsString;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.delete;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.put;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.content;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.view;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.webmvc.test.autoconfigure.AutoConfigureMockMvc;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.transaction.annotation.Transactional;

// s5:入力チェック(400)とエラーの JSON、名前での検索
@SpringBootTest
@AutoConfigureMockMvc
@Transactional
class S5ErrorsTest {
    @Autowired
    MockMvc mockMvc;

    @Test
    @DisplayName("GET /api/users:全件(200、最初は3人)")
    void getAll() throws Exception {
        mockMvc.perform(get("/api/users"))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.length()").value(3))
            .andExpect(jsonPath("$[0].name").value("佐藤 花子"));
    }

    @Test
    @DisplayName("GET /api/users/{id}:1件(200)、いなければ 404")
    void getOne() throws Exception {
        mockMvc.perform(get("/api/users/2"))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.name").value("鈴木 一郎"))
            .andExpect(jsonPath("$.age").value(22));
        mockMvc.perform(get("/api/users/99")).andExpect(status().isNotFound());
    }

    @Test
    @DisplayName("GET /api/users/search?keyword=:名前で検索(200)")
    void search() throws Exception {
        mockMvc.perform(get("/api/users/search").param("keyword", "鈴木"))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.length()").value(1))
            .andExpect(jsonPath("$[0].email").value("ichiro@example.com"));
    }

    @Test
    @DisplayName("POST /api/users:名前が空なら 400 とエラーメッセージ(登録されない)")
    void createInvalid() throws Exception {
        mockMvc.perform(post("/api/users")
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"name\": \"\", \"email\": \"x@example.com\", \"age\": 30}"))
            .andExpect(status().isBadRequest())
            .andExpect(jsonPath("$.message").value("名前は必須です"));
        mockMvc.perform(get("/api/users")).andExpect(jsonPath("$.length()").value(3));
    }

    @Test
    @DisplayName("PUT /api/users/{id}:名前が空なら 400")
    void updateInvalid() throws Exception {
        mockMvc.perform(put("/api/users/1")
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"name\": \" \", \"email\": \"x@example.com\", \"age\": 30}"))
            .andExpect(status().isBadRequest())
            .andExpect(jsonPath("$.message").value("名前は必須です"));
    }
}
