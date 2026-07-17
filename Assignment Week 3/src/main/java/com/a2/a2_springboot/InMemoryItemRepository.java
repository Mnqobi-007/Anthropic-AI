// src/main/java/com/a2/a2_springboot/InMemoryItemRepository.java
package com.a2.a2_springboot;

import org.springframework.stereotype.Repository;
import java.util.*;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.atomic.AtomicLong;

@Repository
public class InMemoryItemRepository implements ItemMemRepository {
    private final Map<Long, Item> store = new ConcurrentHashMap<>();
    private final AtomicLong idGenerator = new AtomicLong(1);
    
    @Override
    public List<Item> findAll() {
        return new ArrayList<>(store.values());
    }
    
    @Override
    public Optional<Item> findById(Long id) {
        return Optional.ofNullable(store.get(id));
    }
    
    @Override
    public Item save(Item item) {
        if (item.getId() == null) {
            item.setId(idGenerator.getAndIncrement());
        }
        store.put(item.getId(), item);
        return item;
    }
    
    @Override
    public void deleteById(Long id) {
        store.remove(id);
    }
    
    @Override
    public boolean existsById(Long id) {
        return store.containsKey(id);
    }
}