package com.example.library;

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

// 演習2の採点テスト(HTTP のリクエストだけで確かめる)
@SpringBootTest
@AutoConfigureMockMvc
@Transactional
class E2BookDbApiTest {
    @Autowired
    MockMvc mockMvc;

    @Test
    @DisplayName("一覧:data.sql の2冊")
    void list() throws Exception {
        mockMvc.perform(get("/api/books")).andExpect(status().isOk()).andExpect(jsonPath("$.length()").value(2));
    }

    @Test
    @DisplayName("1件:200、ない id は 404")
    void getOne() throws Exception {
        mockMvc.perform(get("/api/books/1")).andExpect(status().isOk()).andExpect(jsonPath("$.title").value("Java入門"));
        mockMvc.perform(get("/api/books/99")).andExpect(status().isNotFound());
    }

    @Test
    @DisplayName("登録:201 と id=3、title が空なら 400")
    void create() throws Exception {
        mockMvc.perform(post("/api/books")
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"title\": \"Spring Boot入門\", \"author\": \"鈴木 一郎\"}"))
            .andExpect(status().isCreated())
            .andExpect(jsonPath("$.id").value(3));
        mockMvc.perform(post("/api/books")
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"title\": \"\", \"author\": \"鈴木 一郎\"}"))
            .andExpect(status().isBadRequest());
        mockMvc.perform(get("/api/books")).andExpect(jsonPath("$.length()").value(3));
    }

    @Test
    @DisplayName("更新:200、ない id は 404")
    void update() throws Exception {
        mockMvc.perform(put("/api/books/2")
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"title\": \"SQLの基本 第2版\", \"author\": \"佐藤 花子\"}"))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.title").value("SQLの基本 第2版"));
        mockMvc.perform(get("/api/books/2")).andExpect(jsonPath("$.title").value("SQLの基本 第2版"));
        mockMvc.perform(put("/api/books/99")
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"title\": \"だれか\", \"author\": \"だれか\"}"))
            .andExpect(status().isNotFound());
    }

    @Test
    @DisplayName("削除:204、ない id は 404")
    void deleteBook() throws Exception {
        mockMvc.perform(delete("/api/books/1")).andExpect(status().isNoContent());
        mockMvc.perform(get("/api/books/1")).andExpect(status().isNotFound());
        mockMvc.perform(delete("/api/books/1")).andExpect(status().isNotFound());
    }
}
