package com.hug.pharmacy.controller;

import com.hug.pharmacy.entity.Customer;
import com.hug.pharmacy.repository.CustomerRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.servlet.mvc.support.RedirectAttributes;

@Controller
@RequestMapping("/customers")
@RequiredArgsConstructor
public class CustomerController {

    private final CustomerRepository customerRepository;

    @GetMapping
    public String list(@RequestParam(required = false) String q, Model model) {
        model.addAttribute("customers", q == null || q.isBlank()
                ? customerRepository.findAll()
                : customerRepository.findByFullNameContainingIgnoreCase(q));
        model.addAttribute("q", q);
        model.addAttribute("pageTitle", "Customers");
        return "customers/list";
    }

    @GetMapping("/new")
    public String form(Model model) {
        model.addAttribute("customer", new Customer());
        model.addAttribute("pageTitle", "Add Customer");
        return "customers/form";
    }

    @PostMapping("/save")
    public String save(@ModelAttribute Customer customer, RedirectAttributes ra) {
        customerRepository.save(customer);
        ra.addFlashAttribute("success", "Customer saved");
        return "redirect:/customers";
    }
}
