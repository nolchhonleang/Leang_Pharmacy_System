package com.hug.pharmacy.entity;

import jakarta.persistence.*;
import lombok.*;

import java.math.BigDecimal;

@Entity
@Table(name = "medicines", indexes = {
        @Index(name = "idx_medicine_active_name", columnList = "active, name"),
        @Index(name = "idx_medicine_sku", columnList = "sku")
})
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class Medicine {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, unique = true, length = 40)
    private String sku;

    @Column(nullable = false, length = 150)
    private String name;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "category_id")
    private Category category;

    @Column(length = 500)
    private String description;

    private String manufacturer;
    private String dosageForm;

    @Column(nullable = false, precision = 12, scale = 2)
    private BigDecimal unitPrice;

    @Column(nullable = false, precision = 12, scale = 2)
    private BigDecimal costPrice;

    @Builder.Default
    private int reorderLevel = 10;

    @Builder.Default
    private boolean requiresPrescription = false;

    @Builder.Default
    private boolean active = true;
}
