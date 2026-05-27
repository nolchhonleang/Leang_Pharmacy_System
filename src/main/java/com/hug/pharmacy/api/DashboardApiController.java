package com.hug.pharmacy.api;

import com.hug.pharmacy.dto.DashboardStats;
import com.hug.pharmacy.service.DashboardService;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/v1/dashboard")
@RequiredArgsConstructor
public class DashboardApiController {

    private final DashboardService dashboardService;

    @GetMapping("/stats")
    public DashboardStats stats() {
        return dashboardService.getStats();
    }
}
