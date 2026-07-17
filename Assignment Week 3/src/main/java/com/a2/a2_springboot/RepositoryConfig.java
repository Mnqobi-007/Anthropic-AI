package com.a2.a2_springboot;

import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Primary;

@Configuration
public class RepositoryConfig {
    
    @Bean
    @ConditionalOnProperty(name = "app.storage.type", havingValue = "memory", matchIfMissing = true)
    public ItemMemRepository inMemoryItemRepository() {
        return new InMemoryItemRepository();
    }
    
    @Bean
    @Primary
    @ConditionalOnProperty(name = "app.storage.type", havingValue = "postgres")
    public ItemMemRepository jpaItemRepository(ItemRepository jpaRepo) {
        return jpaRepo;
    }
}