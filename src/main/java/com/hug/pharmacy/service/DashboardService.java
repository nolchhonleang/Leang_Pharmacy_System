package com.hug.pharmacy.service;

import com.hug.pharmacy.config.CacheNames;
import com.hug.pharmacy.dto.DashboardStats;
import com.hug.pharmacy.entity.PrescriptionStatus;
import com.hug.pharmacy.repository.CustomerRepository;
import com.hug.pharmacy.repository.MedicineRepository;
import com.hug.pharmacy.repository.PrescriptionRepository;
import com.hug.pharmacy.repository.SupplierRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.cache.annotation.Cacheable;
import org.springframework.stereotype.Service;

import java.time.LocalDate;
import java.time.LocalDateTime;

@Service
@RequiredArgsConstructor
public class DashboardService {

    private final MedicineRepository medicineRepository;
    private final StockService stockService;
    private final SaleService saleService;
    private final PrescriptionRepository prescriptionRepository;
    private final CustomerRepository customerRepository;
    private final SupplierRepository supplierRepository;

    @Cacheable(CacheNames.DASHBOARD)
    public DashboardStats getStats() {
        LocalDateTime startOfDay = LocalDate.now().atStartOfDay();
        LocalDateTime startOfMonth = LocalDate.now().withDayOfMonth(1).atStartOfDay();
        return DashboardStats.builder()
                .medicineCount(medicineRepository.countByActiveTrue())
                .lowStockCount(stockService.countLowStock())
                .expiringSoonCount(stockService.countExpiringSoon())
                .pendingPrescriptions(prescriptionRepository.countByStatus(PrescriptionStatus.PENDING))
                .todaySales(saleService.salesSince(startOfDay))
                .monthSales(saleService.salesSince(startOfMonth))
                .customerCount(customerRepository.count())
                .activeSuppliers(supplierRepository.findByActiveTrue().size())
                .build();
    }
}
