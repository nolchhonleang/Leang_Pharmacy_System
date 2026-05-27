package com.hug.pharmacy.controller;

import com.hug.pharmacy.dto.PageInfo;
import com.hug.pharmacy.entity.Medicine;
import com.hug.pharmacy.repository.CategoryRepository;
import com.hug.pharmacy.repository.MedicineRepository;
import com.hug.pharmacy.service.AuditService;
import com.hug.pharmacy.service.StockService;
import lombok.RequiredArgsConstructor;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Sort;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.servlet.mvc.support.RedirectAttributes;

import java.math.BigDecimal;
import java.util.Map;
import java.util.stream.Collectors;

@Controller
@RequestMapping("/medicines")
@RequiredArgsConstructor
public class MedicineController {

    private final MedicineRepository medicineRepository;
    private final CategoryRepository categoryRepository;
    private final StockService stockService;
    private final AuditService auditService;

    @Value("${pharmacy.page-size:15}")
    private int pageSize;

    @GetMapping
    public String list(@RequestParam(required = false) String q,
                       @RequestParam(defaultValue = "0") int page,
                       Model model) {
        PageRequest pageable = PageRequest.of(page, pageSize, Sort.by("name"));
        Page<Medicine> medicines = (q != null && !q.isBlank())
                ? medicineRepository.searchActive(q.trim(), pageable)
                : medicineRepository.findActivePaged(pageable);

        var stockById = stockService.stockByMedicineId();
        model.addAttribute("medicines", medicines.getContent());
        model.addAttribute("stockMap", stockById.entrySet().stream()
                .collect(Collectors.toMap(Map.Entry::getKey, e -> e.getValue().getTotalStock())));
        model.addAttribute("lowMap", stockById.entrySet().stream()
                .collect(Collectors.toMap(Map.Entry::getKey, e -> e.getValue().isLowStock())));
        model.addAttribute("page", PageInfo.from(medicines));
        model.addAttribute("q", q);
        model.addAttribute("pageTitle", "Medicines");
        return "medicines/list";
    }

    @GetMapping("/new")
    public String createForm(Model model) {
        model.addAttribute("medicine", new Medicine());
        model.addAttribute("categories", categoryRepository.findAll());
        model.addAttribute("pageTitle", "Add Medicine");
        return "medicines/form";
    }

    @GetMapping("/{id}/edit")
    public String editForm(@PathVariable Long id, Model model) {
        model.addAttribute("medicine", medicineRepository.findById(id).orElseThrow());
        model.addAttribute("categories", categoryRepository.findAll());
        model.addAttribute("pageTitle", "Edit Medicine");
        return "medicines/form";
    }

    @PostMapping("/save")
    public String save(@ModelAttribute Medicine medicine,
                       @RequestParam(required = false) Long categoryId,
                       RedirectAttributes ra) {
        if (categoryId != null) {
            medicine.setCategory(categoryRepository.findById(categoryId).orElse(null));
        }
        if (medicine.getUnitPrice() == null) medicine.setUnitPrice(BigDecimal.ZERO);
        if (medicine.getCostPrice() == null) medicine.setCostPrice(BigDecimal.ZERO);
        medicineRepository.save(medicine);
        auditService.log("SAVE", "Medicine", medicine.getSku());
        ra.addFlashAttribute("success", "Medicine saved");
        return "redirect:/medicines";
    }

    @PostMapping("/{id}/delete")
    public String delete(@PathVariable Long id, RedirectAttributes ra) {
        medicineRepository.findById(id).ifPresent(m -> {
            m.setActive(false);
            medicineRepository.save(m);
            auditService.log("DEACTIVATE", "Medicine", m.getSku());
        });
        ra.addFlashAttribute("success", "Medicine deactivated");
        return "redirect:/medicines";
    }
}
