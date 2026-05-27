package com.hug.pharmacy.controller;

import com.hug.pharmacy.repository.MedicineRepository;
import com.hug.pharmacy.repository.PurchaseOrderRepository;
import com.hug.pharmacy.repository.SupplierRepository;
import com.hug.pharmacy.service.PurchaseOrderService;
import lombok.RequiredArgsConstructor;
import org.springframework.format.annotation.DateTimeFormat;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.servlet.mvc.support.RedirectAttributes;

import java.math.BigDecimal;
import java.time.LocalDate;

@Controller
@RequestMapping("/purchases")
@RequiredArgsConstructor
public class PurchaseOrderController {

    private final PurchaseOrderService purchaseOrderService;
    private final PurchaseOrderRepository purchaseOrderRepository;
    private final SupplierRepository supplierRepository;
    private final MedicineRepository medicineRepository;

    @GetMapping
    public String list(Model model) {
        model.addAttribute("orders", purchaseOrderService.findAll());
        model.addAttribute("pageTitle", "Purchase Orders");
        return "purchases/list";
    }

    @GetMapping("/new")
    public String newOrder(Model model) {
        model.addAttribute("suppliers", supplierRepository.findByActiveTrue());
        model.addAttribute("pageTitle", "New Purchase Order");
        return "purchases/new";
    }

    @PostMapping("/create")
    public String create(@RequestParam Long supplierId,
                         @RequestParam(required = false) @DateTimeFormat(iso = DateTimeFormat.ISO.DATE) LocalDate expectedDate,
                         RedirectAttributes ra) {
        var po = purchaseOrderService.create(supplierId, expectedDate);
        ra.addFlashAttribute("success", "PO created: " + po.getOrderNumber());
        return "redirect:/purchases/" + po.getId();
    }

    @GetMapping("/{id}")
    public String detail(@PathVariable Long id, Model model) {
        model.addAttribute("order", purchaseOrderRepository.findById(id).orElseThrow());
        model.addAttribute("medicines", medicineRepository.findByActiveTrueOrderByNameAsc());
        model.addAttribute("pageTitle", "Purchase Order");
        return "purchases/detail";
    }

    @PostMapping("/{id}/add-item")
    public String addItem(@PathVariable Long id,
                          @RequestParam Long medicineId,
                          @RequestParam int quantity,
                          @RequestParam BigDecimal unitCost,
                          RedirectAttributes ra) {
        purchaseOrderService.addItem(id, medicineId, quantity, unitCost);
        ra.addFlashAttribute("success", "Item added");
        return "redirect:/purchases/" + id;
    }

    @PostMapping("/{id}/receive")
    public String receive(@PathVariable Long id, RedirectAttributes ra) {
        try {
            var po = purchaseOrderService.receive(id);
            ra.addFlashAttribute("success", "Stock received for " + po.getOrderNumber());
        } catch (Exception e) {
            ra.addFlashAttribute("error", e.getMessage());
        }
        return "redirect:/purchases/" + id;
    }
}
