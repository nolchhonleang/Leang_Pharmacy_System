package com.hug.pharmacy.dto;

import lombok.Data;

import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.List;

@Data
public class PosCheckoutRequest {
    private Long customerId;
    private String paymentMethod = "CASH";
    private BigDecimal discount = BigDecimal.ZERO;
    private List<PosLineDto> lines = new ArrayList<>();
}
