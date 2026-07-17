package com.a2.a2_springboot;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import jakarta.transaction.Transactional;

@Service
public class ItemService {
private final ItemRepository itemRepository;
    
    @Autowired
    public ItemService(ItemRepository itemRepository) {
        this.itemRepository = itemRepository;
    }
	
	@Transactional
	public Item saveItem(Item item) {
		if(item.getName().isEmpty()) {
			throw new IllegalArgumentException("Item name cannot be empty");
		}
		return itemRepository.save(item);
	}
	
	public List<Item> getAllItems(){
		return itemRepository.findAll();
	}
	
	public Item getItemById(Long id) {
        return itemRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Item not found with id: " + id));
    }
	
	@Transactional
    public Item updateItem(Long id, Item itemDetails) {
        Item existingItem = getItemById(id);
        existingItem.setName(itemDetails.getName());
        existingItem.setDescription(itemDetails.getDescription());
        return itemRepository.save(existingItem);
    }
    
    @Transactional
    public void deleteItem(Long id) {
        if (!itemRepository.existsById(id)) {
            throw new RuntimeException("Item not found with id: " + id);
        }
        itemRepository.deleteById(id);
    }
}
