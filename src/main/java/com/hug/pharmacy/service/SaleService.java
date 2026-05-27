package com.hug.pharmacy.service;

import com.hug.pharmacy.dto.PosCheckoutRequest;
import com.hug.pharmacy.dto.PosLineDto;
import com.hug.pharmacy.entity.*;
import com.hug.pharmacy.repository.CustomerRepository;
import com.hug.pharmacy.repository.MedicineRepository;
import com.hug.pharmacy.repository.SaleRepository;
import com.hug.pharmacy.repository.UserRepository;
import com.hug.pharmacy.config.CacheNames;
import lombok.RequiredArgsConstructor;
import org.springframework.cache.annotation.CacheEvict;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;
import java.time.LocalDateTime;
import java.util.List;
import java.util.UUID;

@Service
@RequiredArgsConstructor
public class SaleService {

    private final SaleRepository saleRepository;
    private final MedicineRepository medicineRepository;
    private final CustomerRepository customerRepository;
    private final UserRepository userRepository;
    private final StockService stockService;
    private final AuditService auditService;

    public List<Sale> recentSales() {
        return saleRepository.findRecent(PageRequest.of(0, 20));
    }

    public Page<Sale> salesPage(Pageable pageable) {
        return saleRepository.findAllPaged(pageable);
    }

    public Sale findById(Long id) {
        return saleRepository.findByIdWithDetails(id)
                .orElseThrow(() -> new IllegalArgumentException("Sale not found"));
    }

    @CacheEvict(value = {CacheNames.DASHBOARD, CacheNames.STOCK}, allEntries = true)
    @Transactional
    public Sale checkout(PosCheckoutRequest req, String username) {
        User cashier = userRepository.findByUsername(username)
                .orElseThrow(() -> new IllegalStateException("User not found"));
        if (req.getLines() == null || req.getLines().isEmpty()) {
            throw new IllegalArgumentException("Cart is empty");
        }

        BigDecimal subtotal = BigDecimal.ZERO;
        Sale sale = Sale.builder()
                .invoiceNumber("INV-" + UUID.randomUUID().toString().substring(0, 8).toUpperCase())
                .cashier(cashier)
                .paymentMethod(req.getPaymentMethod())
                .discount(req.getDiscount() != null ? req.getDiscount() : BigDecimal.ZERO)
                .build();

        if (req.getCustomerId() != null) {
            sale.setCustomer(customerRepository.findById(req.getCustomerId()).orElse(null));
        }

        for (PosLineDto line : req.getLines()) {
            Medicine med = medicineRepository.findById(line.getMedicineId())
                    .orElseThrow(() -> new IllegalArgumentException("Invalid medicine: " + line.getMedicineId()));
            stockService.deductStock(med.getId(), line.getQuantity());
            BigDecimal lineTotal = med.getUnitPrice().multiply(BigDecimal.valueOf(line.getQuantity()));
            subtotal = subtotal.add(lineTotal);
            SaleItem item = SaleItem.builder()
                    .sale(sale)
                    .medicine(med)
                    .quantity(line.getQuantity())
                    .unitPrice(med.getUnitPrice())
                    .lineTotal(lineTotal)
                    .build();
            sale.getItems().add(item);
        }

        sale.setSubtotal(subtotal);
        sale.setTotal(subtotal.subtract(sale.getDiscount()).max(BigDecimal.ZERO));
        saleRepository.save(sale);
        auditService.log("SALE", "Sale", sale.getInvoiceNumber() + " total=" + sale.getTotal());
        return sale;
    }

    public BigDecimal salesSince(LocalDateTime from) {
        return saleRepository.sumTotalSince(from);
    }
}
