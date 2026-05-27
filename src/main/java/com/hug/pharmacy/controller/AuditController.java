package com.hug.pharmacy.controller;

import com.hug.pharmacy.dto.PageInfo;
import com.hug.pharmacy.service.AuditService;
import lombok.RequiredArgsConstructor;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.data.domain.PageRequest;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;

@Controller
@RequestMapping("/audit")
@RequiredArgsConstructor
public class AuditController {

    private final AuditService auditService;

    @Value("${pharmacy.page-size:15}")
    private int pageSize;

    @GetMapping
    public String list(@RequestParam(defaultValue = "0") int page, Model model) {
        var logs = auditService.findPaged(PageRequest.of(page, pageSize));
        model.addAttribute("logs", logs.getContent());
        model.addAttribute("page", PageInfo.from(logs));
        model.addAttribute("pageTitle", "Audit Log");
        return "audit/list";
    }
}
