package com.example.cafe.order;

import org.springframework.data.jpa.repository.JpaRepository;

public interface CafeOrderRepository extends JpaRepository<CafeOrder, Long> {
}
