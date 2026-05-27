package com.hug.pharmacy.api;

import com.hug.pharmacy.dto.PosMedicineDto;
import com.hug.pharmacy.service.StockService;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequestMapping("/api/v1/pos")
@RequiredArgsConstructor
public class PosApiController {

    private final StockService stockService;

    @GetMapping("/search")
    public List<PosMedicineDto> search(@RequestParam(defaultValue = "") String q,
                                       @RequestParam(defaultValue = "20") int limit) {
        return stockService.searchForPos(q, limit);
    }
}
