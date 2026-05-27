package com.hug.pharmacy.controller;

import com.hug.pharmacy.service.DashboardService;
import com.hug.pharmacy.service.SaleService;
import com.hug.pharmacy.service.StockService;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;

@Controller
@RequiredArgsConstructor
public class DashboardController {

    private final DashboardService dashboardService;
    private final SaleService saleService;
    private final StockService stockService;

    @GetMapping("/dashboard")
    public String dashboard(Model model) {
        model.addAttribute("stats", dashboardService.getStats());
        model.addAttribute("recentSales", saleService.recentSales());
        model.addAttribute("lowStock", stockService.stockOverview().stream()
                .filter(s -> s.isLowStock()).limit(8).toList());
        model.addAttribute("expiring", stockService.expiringSoon().stream().limit(8).toList());
        model.addAttribute("pageTitle", "Dashboard");
        return "dashboard";
    }
}
