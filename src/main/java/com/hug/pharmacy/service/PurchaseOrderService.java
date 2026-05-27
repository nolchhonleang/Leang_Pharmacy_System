package com.hug.pharmacy.service;

import com.hug.pharmacy.entity.*;
import com.hug.pharmacy.repository.MedicineRepository;
import com.hug.pharmacy.repository.PurchaseOrderRepository;
import com.hug.pharmacy.repository.SupplierRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.List;
import java.util.UUID;

@Service
@RequiredArgsConstructor
public class PurchaseOrderService {

    private final PurchaseOrderRepository purchaseOrderRepository;
    private final SupplierRepository supplierRepository;
    private final MedicineRepository medicineRepository;
    private final StockService stockService;
    private final AuditService auditService;

    public List<PurchaseOrder> findAll() {
        return purchaseOrderRepository.findTop20ByOrderByCreatedAtDesc();
    }

    @Transactional
    public PurchaseOrder create(Long supplierId, LocalDate expectedDate) {
        Supplier supplier = supplierRepository.findById(supplierId)
                .orElseThrow(() -> new IllegalArgumentException("Supplier not found"));
        PurchaseOrder po = PurchaseOrder.builder()
                .orderNumber("PO-" + UUID.randomUUID().toString().substring(0, 8).toUpperCase())
                .supplier(supplier)
                .expectedDate(expectedDate)
                .status(PurchaseOrderStatus.DRAFT)
                .totalAmount(BigDecimal.ZERO)
                .build();
        return purchaseOrderRepository.save(po);
    }

    @Transactional
    public PurchaseOrder addItem(Long poId, Long medicineId, int qty, BigDecimal unitCost) {
        PurchaseOrder po = purchaseOrderRepository.findById(poId).orElseThrow();
        Medicine med = medicineRepository.findById(medicineId).orElseThrow();
        PurchaseOrderItem item = PurchaseOrderItem.builder()
                .purchaseOrder(po)
                .medicine(med)
                .quantity(qty)
                .unitCost(unitCost)
                .build();
        po.getItems().add(item);
        recalcTotal(po);
        return purchaseOrderRepository.save(po);
    }

    @Transactional
    public PurchaseOrder receive(Long poId) {
        PurchaseOrder po = purchaseOrderRepository.findById(poId).orElseThrow();
        if (po.getStatus() == PurchaseOrderStatus.RECEIVED) {
            throw new IllegalStateException("Already received");
        }
        for (PurchaseOrderItem item : po.getItems()) {
            String batchNum = "PO-" + po.getOrderNumber() + "-" + item.getMedicine().getSku();
            stockService.addBatch(
                    item.getMedicine().getId(),
                    batchNum,
                    item.getQuantity(),
                    LocalDate.now().plusYears(2),
                    po.getSupplier().getId()
            );
        }
        po.setStatus(PurchaseOrderStatus.RECEIVED);
        auditService.log("PO_RECEIVE", "PurchaseOrder", po.getOrderNumber());
        return purchaseOrderRepository.save(po);
    }

    private void recalcTotal(PurchaseOrder po) {
        BigDecimal total = po.getItems().stream()
                .map(i -> i.getUnitCost().multiply(BigDecimal.valueOf(i.getQuantity())))
                .reduce(BigDecimal.ZERO, BigDecimal::add);
        po.setTotalAmount(total);
    }
}
