package com.hug.pharmacy.config;

import com.hug.pharmacy.entity.*;
import com.hug.pharmacy.repository.*;
import lombok.RequiredArgsConstructor;
import org.springframework.boot.CommandLineRunner;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Component;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.Optional;

@Component
@RequiredArgsConstructor
public class DataInitializer implements CommandLineRunner {

    private final UserRepository userRepository;
    private final CategoryRepository categoryRepository;
    private final SupplierRepository supplierRepository;
    private final MedicineRepository medicineRepository;
    private final StockBatchRepository stockBatchRepository;
    private final CustomerRepository customerRepository;
    private final PasswordEncoder passwordEncoder;

    @Override
    public void run(String... args) {
        upsertDemoUser("admin", "admin123", "System Admin", "admin@leangpharmacy.com", Role.ROLE_ADMIN);
        upsertDemoUser("pharmacist", "pharma123", "Jane Pharmacist", "jane@leangpharmacy.com", Role.ROLE_PHARMACIST);
        upsertDemoUser("cashier", "cash123", "Mike Cashier", "mike@leangpharmacy.com", Role.ROLE_CASHIER);

        if (categoryRepository.count() > 0) return;

        Category pain = categoryRepository.save(Category.builder().name("Pain Relief").description("Analgesics").build());
        Category antibiotic = categoryRepository.save(Category.builder().name("Antibiotics").description("Anti-infectives").build());
        Category vitamin = categoryRepository.save(Category.builder().name("Vitamins").description("Supplements").build());

        Supplier s1 = supplierRepository.save(Supplier.builder().name("MedSupply Co").contactPerson("John").phone("555-0100").email("orders@medsupply.com").active(true).build());

        Medicine m1 = medicineRepository.save(Medicine.builder().sku("MED-001").name("Paracetamol 500mg").category(pain)
                .unitPrice(new BigDecimal("5.99")).costPrice(new BigDecimal("2.50")).reorderLevel(50).dosageForm("Tablet").build());
        Medicine m2 = medicineRepository.save(Medicine.builder().sku("MED-002").name("Amoxicillin 250mg").category(antibiotic)
                .unitPrice(new BigDecimal("12.50")).costPrice(new BigDecimal("6.00")).reorderLevel(30).requiresPrescription(true).dosageForm("Capsule").build());
        Medicine m3 = medicineRepository.save(Medicine.builder().sku("MED-003").name("Vitamin C 1000mg").category(vitamin)
                .unitPrice(new BigDecimal("8.99")).costPrice(new BigDecimal("4.00")).reorderLevel(40).dosageForm("Tablet").build());
        Medicine m4 = medicineRepository.save(Medicine.builder().sku("MED-004").name("Ibuprofen 400mg").category(pain)
                .unitPrice(new BigDecimal("7.49")).costPrice(new BigDecimal("3.20")).reorderLevel(45).dosageForm("Tablet").build());

        stockBatchRepository.save(StockBatch.builder().medicine(m1).batchNumber("B2026-01").quantity(200).expiryDate(LocalDate.of(2027, 6, 1)).supplier(s1).receivedDate(LocalDate.now()).build());
        stockBatchRepository.save(StockBatch.builder().medicine(m2).batchNumber("B2026-02").quantity(80).expiryDate(LocalDate.of(2026, 12, 1)).supplier(s1).receivedDate(LocalDate.now()).build());
        stockBatchRepository.save(StockBatch.builder().medicine(m3).batchNumber("B2026-03").quantity(150).expiryDate(LocalDate.of(2028, 1, 15)).supplier(s1).receivedDate(LocalDate.now()).build());
        stockBatchRepository.save(StockBatch.builder().medicine(m4).batchNumber("B2026-04").quantity(8).expiryDate(LocalDate.of(2027, 3, 20)).supplier(s1).receivedDate(LocalDate.now()).build());

        customerRepository.save(Customer.builder().fullName("Alice Walker").phone("555-2001").email("alice@email.com").build());
    }

    private void upsertDemoUser(String username, String rawPassword, String fullName, String email, Role role) {
        Optional<User> existing = userRepository.findByUsername(username);
        User user = existing.orElseGet(User::new);
        user.setUsername(username);
        user.setPassword(passwordEncoder.encode(rawPassword));
        user.setFullName(fullName);
        user.setEmail(email);
        user.setRole(role);
        user.setActive(true);
        userRepository.save(user);
    }
}
