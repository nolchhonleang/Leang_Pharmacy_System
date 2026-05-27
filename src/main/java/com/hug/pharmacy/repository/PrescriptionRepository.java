package com.hug.pharmacy.repository;

import com.hug.pharmacy.entity.Prescription;
import com.hug.pharmacy.entity.PrescriptionStatus;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;

import java.util.List;

public interface PrescriptionRepository extends JpaRepository<Prescription, Long> {

    long countByStatus(PrescriptionStatus status);

    @Query("SELECT p FROM Prescription p JOIN FETCH p.customer ORDER BY p.createdAt DESC")
    List<Prescription> findAllWithCustomer();

    List<Prescription> findByStatusOrderByCreatedAtDesc(PrescriptionStatus status);
}
