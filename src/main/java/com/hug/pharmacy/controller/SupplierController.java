package com.hug.pharmacy.controller;

import com.hug.pharmacy.entity.Supplier;
import com.hug.pharmacy.repository.SupplierRepository;
import com.hug.pharmacy.service.AuditService;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.servlet.mvc.support.RedirectAttributes;

@Controller
@RequestMapping("/suppliers")
@RequiredArgsConstructor
public class SupplierController {

    private final SupplierRepository supplierRepository;
    private final AuditService auditService;

    @GetMapping
    public String list(Model model) {
        model.addAttribute("suppliers", supplierRepository.findAll());
        model.addAttribute("pageTitle", "Suppliers");
        return "suppliers/list";
    }

    @GetMapping("/new")
    public String form(Model model) {
        model.addAttribute("supplier", new Supplier());
        model.addAttribute("pageTitle", "Add Supplier");
        return "suppliers/form";
    }

    @GetMapping("/{id}/edit")
    public String edit(@PathVariable Long id, Model model) {
        model.addAttribute("supplier", supplierRepository.findById(id).orElseThrow());
        model.addAttribute("pageTitle", "Edit Supplier");
        return "suppliers/form";
    }

    @PostMapping("/save")
    public String save(@ModelAttribute Supplier supplier, RedirectAttributes ra) {
        supplierRepository.save(supplier);
        auditService.log("SAVE", "Supplier", supplier.getName());
        ra.addFlashAttribute("success", "Supplier saved");
        return "redirect:/suppliers";
    }
}
