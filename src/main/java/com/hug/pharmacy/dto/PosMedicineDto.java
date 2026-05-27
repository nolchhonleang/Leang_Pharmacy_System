package com.hug.pharmacy.dto;

import lombok.Builder;
import lombok.Data;

import java.math.BigDecimal;

@Data
@Builder
public class PosMedicineDto {
    private Long id;
    private String sku;
    private String name;
    private BigDecimal unitPrice;
    private Long available;
    private boolean requiresPrescription;

    public PosMedicineDto(Long id, String sku, String name, BigDecimal unitPrice,
                          Long available, boolean requiresPrescription) {
        this.id = id;
        this.sku = sku;
        this.name = name;
        this.unitPrice = unitPrice;
        this.available = available != null ? available : 0L;
        this.requiresPrescription = requiresPrescription;
    }
}
