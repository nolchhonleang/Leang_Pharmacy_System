package com.hug.pharmacy.api;

import com.hug.pharmacy.dto.MedicineStockView;
import com.hug.pharmacy.service.StockService;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequestMapping("/api/v1/stock")
@RequiredArgsConstructor
public class StockApiController {

    private final StockService stockService;

    @GetMapping("/overview")
    public List<MedicineStockView> overview() {
        return stockService.stockOverview();
    }
}
