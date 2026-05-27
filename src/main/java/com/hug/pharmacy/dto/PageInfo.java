package com.hug.pharmacy.dto;

import lombok.Builder;
import lombok.Data;
import org.springframework.data.domain.Page;

@Data
@Builder
public class PageInfo {
    private int number;
    private int totalPages;
    private long totalElements;
    private boolean hasPrev;
    private boolean hasNext;
    private int prev;
    private int next;

    public static PageInfo from(Page<?> page) {
        int n = page.getNumber();
        return PageInfo.builder()
                .number(n)
                .totalPages(page.getTotalPages())
                .totalElements(page.getTotalElements())
                .hasPrev(page.hasPrevious())
                .hasNext(page.hasNext())
                .prev(Math.max(0, n - 1))
                .next(n + 1)
                .build();
    }
}
