package com.hug.pharmacy.controller;

import com.hug.pharmacy.entity.Role;
import com.hug.pharmacy.entity.User;
import com.hug.pharmacy.service.UserService;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.servlet.mvc.support.RedirectAttributes;

@Controller
@RequestMapping("/users")
@RequiredArgsConstructor
public class UserController {

    private final UserService userService;

    @GetMapping
    public String list(Model model) {
        model.addAttribute("users", userService.findAll());
        model.addAttribute("roles", Role.values());
        model.addAttribute("pageTitle", "User Management");
        return "users/list";
    }

    @GetMapping("/new")
    public String form(Model model) {
        model.addAttribute("user", new User());
        model.addAttribute("roles", Role.values());
        model.addAttribute("pageTitle", "Add User");
        return "users/form";
    }

    @GetMapping("/{id}/edit")
    public String edit(@PathVariable Long id, Model model) {
        model.addAttribute("user", userService.findById(id));
        model.addAttribute("roles", Role.values());
        model.addAttribute("pageTitle", "Edit User");
        return "users/form";
    }

    @PostMapping("/save")
    public String save(@ModelAttribute User user,
                       @RequestParam String password,
                       @RequestParam(required = false) Long id,
                       RedirectAttributes ra) {
        try {
            if (id == null) {
                userService.create(user, password);
            } else {
                user.setId(id);
                userService.update(id, user, password.isBlank() ? null : password);
            }
            ra.addFlashAttribute("success", "User saved");
        } catch (Exception e) {
            ra.addFlashAttribute("error", e.getMessage());
        }
        return "redirect:/users";
    }
}
