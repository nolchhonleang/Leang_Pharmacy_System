package com.hug.pharmacy.dto;

import lombok.Builder;
import lombok.Data;

import java.math.BigDecimal;

@Data
@Builder
public class DashboardStats {
    private long medicineCount;
    private long lowStockCount;
    private long expiringSoonCount;
    private long pendingPrescriptions;
    private BigDecimal todaySales;
    private BigDecimal monthSales;
    private long customerCount;
    private long activeSuppliers;
}
