package com.hug.pharmacy.service;

import com.hug.pharmacy.config.CacheNames;
import com.hug.pharmacy.dto.MedicineStockView;
import com.hug.pharmacy.dto.PosMedicineDto;
import com.hug.pharmacy.entity.Medicine;
import com.hug.pharmacy.entity.StockBatch;
import com.hug.pharmacy.entity.Supplier;
import com.hug.pharmacy.repository.MedicineRepository;
import com.hug.pharmacy.repository.StockBatchRepository;
import com.hug.pharmacy.repository.SupplierRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.cache.annotation.CacheEvict;
import org.springframework.cache.annotation.Cacheable;
import org.springframework.data.domain.PageRequest;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDate;
import java.util.Comparator;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
public class StockService {

    private final StockBatchRepository stockBatchRepository;
    private final MedicineRepository medicineRepository;
    private final SupplierRepository supplierRepository;
    private final AuditService auditService;

    @Value("${pharmacy.expiry-warning-days:90}")
    private int expiryWarningDays;

    @Cacheable(CacheNames.STOCK)
    public List<MedicineStockView> stockOverview() {
        return medicineRepository.findStockOverview();
    }

    public Map<Long, MedicineStockView> stockByMedicineId() {
        return stockOverview().stream()
                .collect(Collectors.toMap(MedicineStockView::getId, v -> v, (a, b) -> a));
    }

    public List<PosMedicineDto> searchForPos(String q, int limit) {
        String term = q == null ? "" : q.trim();
        if (term.length() < 1) {
            return List.of();
        }
        return medicineRepository.searchForPos(term, PageRequest.of(0, Math.min(limit, 30)));
    }

    public List<StockBatch> allBatches() {
        return stockBatchRepository.findAllInStock();
    }

    public List<StockBatch> recentBatches(int limit) {
        return stockBatchRepository.findRecentBatches(PageRequest.of(0, limit));
    }

    public List<StockBatch> expiringSoon() {
        return stockBatchRepository.findExpiringBefore(LocalDate.now().plusDays(expiryWarningDays));
    }

    public long countExpiringSoon() {
        return stockBatchRepository.countExpiringBefore(LocalDate.now().plusDays(expiryWarningDays));
    }

    public long countLowStock() {
        return medicineRepository.countLowStock();
    }

    @CacheEvict(value = {CacheNames.STOCK, CacheNames.DASHBOARD}, allEntries = true)
    @Transactional
    public StockBatch addBatch(Long medicineId, String batchNumber, int quantity,
                             LocalDate expiryDate, Long supplierId) {
        Medicine medicine = medicineRepository.findById(medicineId)
                .orElseThrow(() -> new IllegalArgumentException("Medicine not found"));
        Supplier supplier = supplierId != null
                ? supplierRepository.findById(supplierId).orElse(null) : null;
        StockBatch batch = StockBatch.builder()
                .medicine(medicine)
                .batchNumber(batchNumber)
                .quantity(quantity)
                .expiryDate(expiryDate)
                .supplier(supplier)
                .receivedDate(LocalDate.now())
                .build();
        stockBatchRepository.save(batch);
        auditService.log("STOCK_IN", "StockBatch", medicine.getSku() + " +" + quantity);
        return batch;
    }

    @CacheEvict(value = CacheNames.STOCK, allEntries = true)
    @Transactional
    public void deductStock(Long medicineId, int quantity) {
        List<StockBatch> batches = stockBatchRepository
                .findByMedicineIdAndQuantityGreaterThan(medicineId, 0);
        batches.sort(Comparator.comparing(StockBatch::getExpiryDate, Comparator.nullsLast(Comparator.naturalOrder())));
        int remaining = quantity;
        for (StockBatch b : batches) {
            if (remaining <= 0) break;
            int take = Math.min(b.getQuantity(), remaining);
            b.setQuantity(b.getQuantity() - take);
            remaining -= take;
        }
        if (remaining > 0) {
            throw new IllegalStateException("Insufficient stock for medicine id " + medicineId);
        }
    }
}
