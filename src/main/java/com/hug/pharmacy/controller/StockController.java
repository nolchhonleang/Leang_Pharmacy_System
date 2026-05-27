package com.hug.pharmacy.controller;

import com.hug.pharmacy.repository.MedicineRepository;
import com.hug.pharmacy.repository.SupplierRepository;
import com.hug.pharmacy.service.StockService;
import lombok.RequiredArgsConstructor;
import org.springframework.format.annotation.DateTimeFormat;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.servlet.mvc.support.RedirectAttributes;

import java.time.LocalDate;

@Controller
@RequestMapping("/stock")
@RequiredArgsConstructor
public class StockController {

    private final StockService stockService;
    private final MedicineRepository medicineRepository;
    private final SupplierRepository supplierRepository;

    @GetMapping
    public String index(Model model) {
        model.addAttribute("overview", stockService.stockOverview());
        model.addAttribute("expiring", stockService.expiringSoon());
        model.addAttribute("batches", stockService.recentBatches(10));
        model.addAttribute("pageTitle", "Stock Management");
        return "stock/index";
    }

    @GetMapping("/add")
    public String addForm(Model model) {
        model.addAttribute("medicines", medicineRepository.findByActiveTrueOrderByNameAsc());
        model.addAttribute("suppliers", supplierRepository.findByActiveTrue());
        model.addAttribute("pageTitle", "Receive Stock");
        return "stock/add";
    }

    @PostMapping("/add")
    public String addBatch(@RequestParam Long medicineId,
                           @RequestParam String batchNumber,
                           @RequestParam int quantity,
                           @RequestParam @DateTimeFormat(iso = DateTimeFormat.ISO.DATE) LocalDate expiryDate,
                           @RequestParam(required = false) Long supplierId,
                           RedirectAttributes ra) {
        stockService.addBatch(medicineId, batchNumber, quantity, expiryDate, supplierId);
        ra.addFlashAttribute("success", "Stock batch added");
        return "redirect:/stock";
    }
}
