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

import static org.junit.jupiter.api.Assertions.assertEquals;

import com.example.demo.service.GreetingService;

// Day4:Controller と DI を確かめる
@SpringBootTest
@AutoConfigureMockMvc
class W1ControllerTest {
    @Autowired
    MockMvc mockMvc;

    @Autowired
    GreetingService greetingService;

    @Test
    @DisplayName("GreetingService:Spring が GreetingServiceImpl を渡してくれる")
    void greetingService() {
        assertEquals("GreetingServiceImpl", greetingService.getClass().getSimpleName());
        assertEquals("こんにちは、田中さん", greetingService.greet("田中"));
    }

    @Test
    @DisplayName("GET /hello:文字をそのまま返す")
    void hello() throws Exception {
        mockMvc.perform(get("/hello"))
            .andExpect(status().isOk())
            .andExpect(content().string("Hello, Spring Boot!"));
    }

    @Test
    @DisplayName("GET /hello/{name}:URL の一部を受け取って、あいさつを返す")
    void helloName() throws Exception {
        mockMvc.perform(get("/hello/{name}", "田中"))
            .andExpect(status().isOk())
            .andExpect(content().string("こんにちは、田中さん"));
    }

    @Test
    @DisplayName("GET /welcome:Model に入れたメッセージが HTML に表示される")
    void welcome() throws Exception {
        mockMvc.perform(get("/welcome"))
            .andExpect(status().isOk())
            .andExpect(view().name("welcome"))
            .andExpect(content().string(containsString("こんにちは、ゲストさん")));
    }
}
