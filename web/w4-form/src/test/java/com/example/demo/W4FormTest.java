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

// Day8:フォーム → Controller → Model → HTML の流れを確かめる
@SpringBootTest
@AutoConfigureMockMvc
class W4FormTest {
    @Autowired
    MockMvc mockMvc;

    @Test
    @DisplayName("GET /form:入力画面が表示される")
    void form() throws Exception {
        mockMvc.perform(get("/form"))
            .andExpect(status().isOk())
            .andExpect(view().name("form"))
            .andExpect(content().string(containsString("name=\"name\"")));
    }

    @Test
    @DisplayName("POST /form:正しく入力すると、結果の画面に表示される")
    void submit() throws Exception {
        mockMvc.perform(post("/form").param("name", "田中").param("age", "20"))
            .andExpect(status().isOk())
            .andExpect(view().name("result"))
            .andExpect(content().string(containsString("田中さん(20歳)を受け付けました")));
    }

    @Test
    @DisplayName("POST /form:名前が空なら入力画面に戻り、メッセージが出る")
    void nameBlank() throws Exception {
        mockMvc.perform(post("/form").param("name", "").param("age", "20"))
            .andExpect(view().name("form"))
            .andExpect(content().string(containsString("名前を入力してください")));
    }

    @Test
    @DisplayName("POST /form:年齢が範囲外なら入力画面に戻り、メッセージが出る")
    void ageOutOfRange() throws Exception {
        mockMvc.perform(post("/form").param("name", "田中").param("age", "200"))
            .andExpect(view().name("form"))
            .andExpect(content().string(containsString("年齢は150以下にしてください")));
        mockMvc.perform(post("/form").param("name", "田中").param("age", ""))
            .andExpect(view().name("form"))
            .andExpect(content().string(containsString("年齢を入力してください")));
    }
}
