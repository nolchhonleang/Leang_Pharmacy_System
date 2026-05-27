package com.hug.pharmacy.controller;

import com.hug.pharmacy.entity.*;
import com.hug.pharmacy.repository.CustomerRepository;
import com.hug.pharmacy.repository.MedicineRepository;
import com.hug.pharmacy.repository.PrescriptionRepository;
import com.hug.pharmacy.service.AuditService;
import lombok.RequiredArgsConstructor;
import org.springframework.format.annotation.DateTimeFormat;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.servlet.mvc.support.RedirectAttributes;

import java.time.LocalDate;
import java.util.List;

@Controller
@RequestMapping("/prescriptions")
@RequiredArgsConstructor
public class PrescriptionController {

    private final PrescriptionRepository prescriptionRepository;
    private final CustomerRepository customerRepository;
    private final MedicineRepository medicineRepository;
    private final AuditService auditService;

    @GetMapping
    public String list(Model model) {
        model.addAttribute("prescriptions", prescriptionRepository.findAllWithCustomer());
        model.addAttribute("pageTitle", "Prescriptions");
        return "prescriptions/list";
    }

    @GetMapping("/new")
    public String form(Model model) {
        model.addAttribute("customers", customerRepository.findAll());
        model.addAttribute("medicines", medicineRepository.findByActiveTrueOrderByNameAsc());
        model.addAttribute("pageTitle", "New Prescription");
        return "prescriptions/form";
    }

    @PostMapping("/save")
    public String save(@RequestParam Long customerId,
                       @RequestParam String doctorName,
                       @RequestParam @DateTimeFormat(iso = DateTimeFormat.ISO.DATE) LocalDate prescribedDate,
                       @RequestParam(required = false) String notes,
                       @RequestParam(required = false) List<Long> medicineId,
                       @RequestParam(required = false) List<Integer> quantity,
                       RedirectAttributes ra) {
        Customer customer = customerRepository.findById(customerId).orElseThrow();
        Prescription rx = Prescription.builder()
                .customer(customer)
                .doctorName(doctorName)
                .prescribedDate(prescribedDate)
                .notes(notes)
                .status(PrescriptionStatus.PENDING)
                .build();
        if (medicineId != null) {
            for (int i = 0; i < medicineId.size(); i++) {
                if (quantity != null && i < quantity.size() && quantity.get(i) > 0) {
                    Medicine med = medicineRepository.findById(medicineId.get(i)).orElseThrow();
                    rx.getItems().add(PrescriptionItem.builder()
                            .prescription(rx)
                            .medicine(med)
                            .quantity(quantity.get(i))
                            .build());
                }
            }
        }
        prescriptionRepository.save(rx);
        auditService.log("CREATE", "Prescription", "RX#" + rx.getId());
        ra.addFlashAttribute("success", "Prescription created");
        return "redirect:/prescriptions";
    }

    @PostMapping("/{id}/dispense")
    public String dispense(@PathVariable Long id, RedirectAttributes ra) {
        Prescription rx = prescriptionRepository.findById(id).orElseThrow();
        rx.setStatus(PrescriptionStatus.DISPENSED);
        prescriptionRepository.save(rx);
        auditService.log("DISPENSE", "Prescription", "RX#" + id);
        ra.addFlashAttribute("success", "Marked as dispensed");
        return "redirect:/prescriptions";
    }
}
