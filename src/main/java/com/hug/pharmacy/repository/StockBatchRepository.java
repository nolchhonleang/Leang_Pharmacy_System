package com.hug.pharmacy.repository;

import com.hug.pharmacy.entity.StockBatch;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;

import java.time.LocalDate;
import java.util.List;

public interface StockBatchRepository extends JpaRepository<StockBatch, Long> {

    List<StockBatch> findByMedicineIdAndQuantityGreaterThan(Long medicineId, int min);

    @Query("SELECT sb FROM StockBatch sb JOIN FETCH sb.medicine m WHERE sb.quantity > 0 ORDER BY sb.expiryDate ASC")
    List<StockBatch> findAllInStock();

    @Query("SELECT sb FROM StockBatch sb JOIN FETCH sb.medicine m WHERE sb.expiryDate <= :before AND sb.quantity > 0 ORDER BY sb.expiryDate ASC")
    List<StockBatch> findExpiringBefore(LocalDate before);

    @Query("SELECT COUNT(sb) FROM StockBatch sb WHERE sb.expiryDate <= :before AND sb.quantity > 0")
    long countExpiringBefore(LocalDate before);

    @Query("SELECT sb FROM StockBatch sb JOIN FETCH sb.medicine WHERE sb.quantity > 0 ORDER BY sb.receivedDate DESC")
    List<StockBatch> findRecentBatches(Pageable pageable);
}
