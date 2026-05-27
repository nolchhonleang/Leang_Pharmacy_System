package com.hug.pharmacy.controller;

import com.hug.pharmacy.service.DashboardService;
import com.hug.pharmacy.service.SaleService;
import com.hug.pharmacy.service.StockService;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;

@Controller
@RequestMapping("/reports")
@RequiredArgsConstructor
public class ReportController {

    private final DashboardService dashboardService;
    private final SaleService saleService;
    private final StockService stockService;

    @GetMapping
    public String reports(Model model) {
        model.addAttribute("stats", dashboardService.getStats());
        model.addAttribute("sales", saleService.recentSales());
        model.addAttribute("stock", stockService.stockOverview());
        model.addAttribute("pageTitle", "Reports");
        return "reports/index";
    }
}
