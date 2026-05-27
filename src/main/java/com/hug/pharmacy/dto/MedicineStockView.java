package com.hug.pharmacy.dto;

import lombok.Builder;
import lombok.Data;

import java.math.BigDecimal;

@Data
@Builder
public class MedicineStockView {
    private Long id;
    private String sku;
    private String name;
    private String categoryName;
    private Long totalStock;
    private int reorderLevel;
    private boolean lowStock;
    private BigDecimal unitPrice;

    /** JPQL constructor for aggregated stock query */
    public MedicineStockView(Long id, String sku, String name, String categoryName,
                             Long totalStock, int reorderLevel, boolean lowStock, BigDecimal unitPrice) {
        this.id = id;
        this.sku = sku;
        this.name = name;
        this.categoryName = categoryName;
        this.totalStock = totalStock != null ? totalStock : 0L;
        this.reorderLevel = reorderLevel;
        this.lowStock = lowStock;
        this.unitPrice = unitPrice;
    }
}
