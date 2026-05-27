package com.hug.pharmacy.controller;

import com.hug.pharmacy.entity.Category;
import com.hug.pharmacy.repository.CategoryRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.servlet.mvc.support.RedirectAttributes;

@Controller
@RequestMapping("/categories")
@RequiredArgsConstructor
public class CategoryController {

    private final CategoryRepository categoryRepository;

    @GetMapping
    public String list(Model model) {
        model.addAttribute("categories", categoryRepository.findAll());
        model.addAttribute("pageTitle", "Categories");
        return "categories/list";
    }

    @PostMapping("/save")
    public String save(@RequestParam(required = false) Long id,
                       @RequestParam String name,
                       @RequestParam(required = false) String description,
                       RedirectAttributes ra) {
        Category c = id != null ? categoryRepository.findById(id).orElse(new Category()) : new Category();
        c.setName(name);
        c.setDescription(description);
        categoryRepository.save(c);
        ra.addFlashAttribute("success", "Category saved");
        return "redirect:/categories";
    }
}
