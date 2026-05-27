package com.hug.pharmacy.repository;

import com.hug.pharmacy.dto.MedicineStockView;
import com.hug.pharmacy.dto.PosMedicineDto;
import com.hug.pharmacy.entity.Medicine;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.util.List;
import java.util.Optional;

public interface MedicineRepository extends JpaRepository<Medicine, Long> {

    Optional<Medicine> findBySku(String sku);

    long countByActiveTrue();

    java.util.List<Medicine> findByActiveTrueOrderByNameAsc();

    @Query(value = "SELECT m FROM Medicine m LEFT JOIN FETCH m.category WHERE m.active = true",
           countQuery = "SELECT COUNT(m) FROM Medicine m WHERE m.active = true")
    Page<Medicine> findActivePaged(Pageable pageable);

    @Query(value = "SELECT m FROM Medicine m LEFT JOIN FETCH m.category WHERE m.active = true AND " +
           "(LOWER(m.name) LIKE LOWER(CONCAT('%', :q, '%')) OR LOWER(m.sku) LIKE LOWER(CONCAT('%', :q, '%')))",
           countQuery = "SELECT COUNT(m) FROM Medicine m WHERE m.active = true AND " +
           "(LOWER(m.name) LIKE LOWER(CONCAT('%', :q, '%')) OR LOWER(m.sku) LIKE LOWER(CONCAT('%', :q, '%')))")
    Page<Medicine> searchActive(@Param("q") String q, Pageable pageable);

    @Query("""
            SELECT new com.hug.pharmacy.dto.MedicineStockView(
              m.id, m.sku, m.name, COALESCE(c.name, '-'),
              COALESCE(SUM(CASE WHEN sb.quantity > 0 THEN sb.quantity ELSE 0 END), 0L),
              m.reorderLevel,
              COALESCE(SUM(CASE WHEN sb.quantity > 0 THEN sb.quantity ELSE 0 END), 0L) <= m.reorderLevel,
              m.unitPrice
            )
            FROM Medicine m
            LEFT JOIN m.category c
            LEFT JOIN StockBatch sb ON sb.medicine = m
            WHERE m.active = true
            GROUP BY m.id, m.sku, m.name, c.id, c.name, m.reorderLevel, m.unitPrice
            ORDER BY m.name ASC
            """)
    List<MedicineStockView> findStockOverview();

    @Query("""
            SELECT COUNT(m) FROM Medicine m
            WHERE m.active = true AND
            COALESCE((SELECT SUM(sb.quantity) FROM StockBatch sb WHERE sb.medicine = m AND sb.quantity > 0), 0L) <= m.reorderLevel
            """)
    long countLowStock();

    @Query("""
            SELECT new com.hug.pharmacy.dto.PosMedicineDto(
              m.id, m.sku, m.name, m.unitPrice,
              COALESCE((SELECT SUM(sb.quantity) FROM StockBatch sb WHERE sb.medicine = m AND sb.quantity > 0), 0L),
              m.requiresPrescription
            )
            FROM Medicine m
            WHERE m.active = true AND
            (LOWER(m.name) LIKE LOWER(CONCAT('%', :q, '%')) OR LOWER(m.sku) LIKE LOWER(CONCAT('%', :q, '%')))
            ORDER BY m.name ASC
            """)
    List<PosMedicineDto> searchForPos(@Param("q") String q, Pageable pageable);
}
