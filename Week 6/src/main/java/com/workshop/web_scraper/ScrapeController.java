package com.workshop.web_scraper;

import java.util.List;
import java.util.Map;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api")
public class ScrapeController {
	@Autowired
	private Scrapper scrapper;
	
	@GetMapping("/start")
    public ResponseEntity<?> startScrape() {
        try {
            // Default path to practice-site.html
            String filePath = "src/main/resources/practice-site.html";
            List<Book> books = scrapper.scrapeBooksFromFile(filePath);
            
            return ResponseEntity.ok(Map.of(
                "status", "success",
                "message", "Scraped " + books.size() + " books from local file",
                "books", books
            ));
        } catch (Exception e) {
            return ResponseEntity.internalServerError().body(Map.of(
                "status", "error",
                "message", e.getMessage()
            ));
        }
    }
}
