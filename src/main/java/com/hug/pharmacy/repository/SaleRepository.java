package com.hug.pharmacy.repository;

import com.hug.pharmacy.entity.Sale;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;

import java.math.BigDecimal;
import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;

public interface SaleRepository extends JpaRepository<Sale, Long> {

    Optional<Sale> findByInvoiceNumber(String invoiceNumber);

    @Query("SELECT s FROM Sale s LEFT JOIN FETCH s.customer LEFT JOIN FETCH s.cashier ORDER BY s.soldAt DESC")
    Page<Sale> findAllPaged(Pageable pageable);

    @Query("SELECT s FROM Sale s LEFT JOIN FETCH s.customer LEFT JOIN FETCH s.cashier ORDER BY s.soldAt DESC")
    List<Sale> findRecent(Pageable pageable);

    @Query("SELECT COALESCE(SUM(s.total), 0) FROM Sale s WHERE s.soldAt >= :from")
    BigDecimal sumTotalSince(LocalDateTime from);

    @Query("SELECT DISTINCT s FROM Sale s " +
           "LEFT JOIN FETCH s.customer LEFT JOIN FETCH s.cashier " +
           "LEFT JOIN FETCH s.items i LEFT JOIN FETCH i.medicine WHERE s.id = :id")
    Optional<Sale> findByIdWithDetails(Long id);
}
