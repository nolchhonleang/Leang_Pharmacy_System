package com.hug.pharmacy.service;

import com.hug.pharmacy.entity.AuditLog;
import com.hug.pharmacy.repository.AuditLogRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
@RequiredArgsConstructor
public class AuditService {

    private final AuditLogRepository auditLogRepository;

    @Transactional
    public void log(String action, String entityType, String details) {
        String user = "system";
        var auth = SecurityContextHolder.getContext().getAuthentication();
        if (auth != null && auth.isAuthenticated() && !"anonymousUser".equals(auth.getPrincipal())) {
            user = auth.getName();
        }
        auditLogRepository.save(AuditLog.builder()
                .username(user)
                .action(action)
                .entityType(entityType)
                .details(details)
                .build());
    }

    public Page<AuditLog> findPaged(Pageable pageable) {
        return auditLogRepository.findAllByOrderByCreatedAtDesc(pageable);
    }
}
