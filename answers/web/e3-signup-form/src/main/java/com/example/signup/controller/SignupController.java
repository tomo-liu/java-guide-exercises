package com.example.signup.controller;

import com.example.signup.form.SignupForm;
import jakarta.validation.Valid;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.validation.BindingResult;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.PostMapping;

@Controller
public class SignupController {
    @GetMapping("/signup")
    public String form(Model model) {
        model.addAttribute("signupForm", new SignupForm());
        return "signup";
    }

    @PostMapping("/signup")
    public String submit(@Valid @ModelAttribute SignupForm signupForm, BindingResult result, Model model) {
        if (result.hasErrors()) {
            return "signup";
        }
        model.addAttribute("name", signupForm.getName());
        return "signup-complete";
    }
}
