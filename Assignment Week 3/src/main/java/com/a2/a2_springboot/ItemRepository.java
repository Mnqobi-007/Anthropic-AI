package com.a2.a2_springboot;

import java.util.Optional;

import org.springframework.data.jpa.repository.JpaRepository;

public interface ItemRepository extends JpaRepository<Item, Long>, ItemMemRepository {
	Optional<Item> findById(Long id);
	Optional<Item> findByName(String name);
}
