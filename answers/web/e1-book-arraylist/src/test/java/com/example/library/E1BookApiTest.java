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

import org.springframework.test.annotation.DirtiesContext;

// 演習1の採点テスト(HTTP のリクエストだけで確かめる。各テストの前にアプリを作り直すので、ArrayList は毎回空から始まる)
@SpringBootTest
@AutoConfigureMockMvc
@DirtiesContext(classMode = DirtiesContext.ClassMode.BEFORE_EACH_TEST_METHOD)
class E1BookApiTest {
    @Autowired
    MockMvc mockMvc;

    private void register(String title, String author) throws Exception {
        mockMvc.perform(post("/api/books")
            .contentType(MediaType.APPLICATION_JSON)
            .content("{\"title\": \"" + title + "\", \"author\": \"" + author + "\"}"));
    }

    @Test
    @DisplayName("一覧:最初は空の配列")
    void emptyAtFirst() throws Exception {
        mockMvc.perform(get("/api/books")).andExpect(status().isOk()).andExpect(jsonPath("$.length()").value(0));
    }

    @Test
    @DisplayName("登録:201 と、id=1 の振られた本")
    void create() throws Exception {
        mockMvc.perform(post("/api/books")
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"title\": \"Java入門\", \"author\": \"山田 太郎\"}"))
            .andExpect(status().isCreated())
            .andExpect(jsonPath("$.id").value(1))
            .andExpect(jsonPath("$.title").value("Java入門"));
    }

    @Test
    @DisplayName("登録して一覧・1件取得:id は 1, 2 と振られる。ない id は 404")
    void listAndGet() throws Exception {
        register("Java入門", "山田 太郎");
        register("SQLの基本", "佐藤 花子");
        mockMvc.perform(get("/api/books")).andExpect(jsonPath("$.length()").value(2));
        mockMvc.perform(get("/api/books/2")).andExpect(status().isOk()).andExpect(jsonPath("$.author").value("佐藤 花子"));
        mockMvc.perform(get("/api/books/99")).andExpect(status().isNotFound());
    }

    @Test
    @DisplayName("登録:title が空なら 400")
    void createInvalid() throws Exception {
        mockMvc.perform(post("/api/books")
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"title\": \"\", \"author\": \"山田 太郎\"}"))
            .andExpect(status().isBadRequest());
    }
}
