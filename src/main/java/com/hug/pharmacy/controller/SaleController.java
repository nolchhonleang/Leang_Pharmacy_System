package com.hug.pharmacy.controller;

import com.hug.pharmacy.dto.PageInfo;
import com.hug.pharmacy.dto.PosCheckoutRequest;
import com.hug.pharmacy.dto.PosLineDto;
import com.hug.pharmacy.repository.CustomerRepository;
import com.hug.pharmacy.service.SaleService;
import lombok.RequiredArgsConstructor;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Sort;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.servlet.mvc.support.RedirectAttributes;

import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.List;

@Controller
@RequestMapping("/pos")
@RequiredArgsConstructor
public class SaleController {

    private final SaleService saleService;
    private final CustomerRepository customerRepository;

    @Value("${pharmacy.page-size:15}")
    private int pageSize;

    @GetMapping
    public String pos(Model model) {
        model.addAttribute("customers", customerRepository.findAll());
        model.addAttribute("pageTitle", "Point of Sale");
        return "pos/index";
    }

    @GetMapping("/history")
    public String history(@RequestParam(defaultValue = "0") int page, Model model) {
        var sales = saleService.salesPage(PageRequest.of(page, pageSize, Sort.by(Sort.Direction.DESC, "soldAt")));
        model.addAttribute("sales", sales.getContent());
        model.addAttribute("page", PageInfo.from(sales));
        model.addAttribute("pageTitle", "Sales History");
        return "pos/history";
    }

    @GetMapping("/receipt/{id}")
    public String receipt(@PathVariable Long id, Model model) {
        model.addAttribute("sale", saleService.findById(id));
        model.addAttribute("pageTitle", "Receipt");
        return "pos/receipt";
    }

    @PostMapping("/checkout")
    public String checkout(@RequestParam(required = false) Long customerId,
                           @RequestParam String paymentMethod,
                           @RequestParam(defaultValue = "0") BigDecimal discount,
                           @RequestParam List<Long> medicineId,
                           @RequestParam List<Integer> quantity,
                           @AuthenticationPrincipal UserDetails user,
                           RedirectAttributes ra) {
        try {
            PosCheckoutRequest req = new PosCheckoutRequest();
            req.setCustomerId(customerId);
            req.setPaymentMethod(paymentMethod);
            req.setDiscount(discount);
            List<PosLineDto> lines = new ArrayList<>();
            for (int i = 0; i < medicineId.size(); i++) {
                if (i < quantity.size() && quantity.get(i) > 0) {
                    PosLineDto line = new PosLineDto();
                    line.setMedicineId(medicineId.get(i));
                    line.setQuantity(quantity.get(i));
                    lines.add(line);
                }
            }
            req.setLines(lines);
            var sale = saleService.checkout(req, user.getUsername());
            ra.addFlashAttribute("success", "Sale complete: " + sale.getInvoiceNumber());
            return "redirect:/pos/receipt/" + sale.getId();
        } catch (Exception e) {
            ra.addFlashAttribute("error", e.getMessage());
            return "redirect:/pos";
        }
    }
}
