package com.hug.pharmacy.repository;

import com.hug.pharmacy.entity.PurchaseOrder;
import com.hug.pharmacy.entity.PurchaseOrderStatus;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;
import java.util.Optional;

public interface PurchaseOrderRepository extends JpaRepository<PurchaseOrder, Long> {
    Optional<PurchaseOrder> findByOrderNumber(String orderNumber);
    List<PurchaseOrder> findByStatusOrderByCreatedAtDesc(PurchaseOrderStatus status);
    List<PurchaseOrder> findTop20ByOrderByCreatedAtDesc();
}
