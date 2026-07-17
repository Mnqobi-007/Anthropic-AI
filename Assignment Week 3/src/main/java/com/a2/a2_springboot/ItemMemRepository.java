package com.a2.a2_springboot;

import java.util.List;
import java.util.Optional;

public interface ItemMemRepository {
    List<Item> findAll();
    Optional<Item> findById(Long id);
    Item save(Item item);
    void deleteById(Long id);
    boolean existsById(Long id);
}