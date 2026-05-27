package com.hug.pharmacy.service;

import com.hug.pharmacy.entity.Role;
import com.hug.pharmacy.entity.User;
import com.hug.pharmacy.repository.UserRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

@Service
@RequiredArgsConstructor
public class UserService {

    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;
    private final AuditService auditService;

    public List<User> findAll() {
        return userRepository.findAll();
    }

    public User findById(Long id) {
        return userRepository.findById(id).orElseThrow();
    }

    @Transactional
    public User create(User user, String rawPassword) {
        if (userRepository.existsByUsername(user.getUsername())) {
            throw new IllegalArgumentException("Username already exists");
        }
        user.setPassword(passwordEncoder.encode(rawPassword));
        user.setActive(true);
        User saved = userRepository.save(user);
        auditService.log("CREATE", "User", saved.getUsername());
        return saved;
    }

    @Transactional
    public User update(Long id, User updated, String newPassword) {
        User user = userRepository.findById(id).orElseThrow();
        user.setFullName(updated.getFullName());
        user.setEmail(updated.getEmail());
        user.setRole(updated.getRole());
        user.setActive(updated.isActive());
        if (newPassword != null && !newPassword.isBlank()) {
            user.setPassword(passwordEncoder.encode(newPassword));
        }
        return userRepository.save(user);
    }
}
