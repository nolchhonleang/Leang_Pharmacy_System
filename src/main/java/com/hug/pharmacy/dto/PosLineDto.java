package com.hug.pharmacy.dto;

import lombok.Data;

@Data
public class PosLineDto {
    private Long medicineId;
    private int quantity;
}
