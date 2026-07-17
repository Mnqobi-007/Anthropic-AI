package com.workshop.web_scraper;

import java.io.File;
import java.util.ArrayList;
import java.util.List;

import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Component;

@Component
public class Scrapper {
    private static final Logger log = LoggerFactory.getLogger(Scrapper.class);

    // Scrape from URL
    public List<Book> scrapeBooks(String url) throws Exception {
        log.info("🌐 Starting scrape of: {}", url);
        
        // FETCH + PARSE
        Document doc = Jsoup.connect(url)
                .userAgent("WorkshopBot/1.0 (Educational)")
                .timeout(10000)
                .get();
        
        log.info("📄 Page fetched successfully");
        return processDocument(doc, url);
    }

    // Scrape from local file
    public List<Book> scrapeBooksFromFile(String filePath) throws Exception {
        log.info("📂 Reading from local file: {}", filePath);
        
        File input = new File(filePath);
        if (!input.exists()) {
            throw new IllegalArgumentException("File not found: " + filePath);
        }
        
        // PARSE: Load HTML from file
        Document doc = Jsoup.parse(input, "UTF-8", "file://" + filePath);
        log.info("📄 File loaded successfully");
        
        return processDocument(doc, filePath);
    }

    // Process document
    private List<Book> processDocument(Document doc, String source) {
        // EXTRACT: Get all book cards
        Elements bookCards = doc.select(".book-card");
        log.info("📚 Found {} book cards", bookCards.size());
        
        List<Book> books = new ArrayList<>();
        
        // Process each card
        for (Element card : bookCards) {
            try {
                // EXTRACTION
                String title = card.select(".book-title").text();
                String author = card.select(".book-author span").text();
                String description = card.select(".book-description").text();
                String priceText = card.select(".book-price").text();
                String ratingText = card.select(".book-rating").text();
                String stockText = card.select(".book-stock").text();
                String category = card.select(".book-category").text();
                
                // CLEAN
                title = cleanTitle(title);
                author = cleanAuthor(author);
                description = cleanDescription(description);
                Double price = cleanPrice(priceText);
                Double rating = cleanRating(ratingText);
                boolean inStock = stockText.contains("In Stock");
                category = cleanCategory(category);
                
                // STRUCTURE
                Book book = new Book(title, author, description, price, rating, inStock, category);
                books.add(book);
                
                log.debug("✅ Extracted: {}", book);
                
            } catch (Exception e) {
                log.warn("⚠️ Failed to parse a book card: {}", e.getMessage());
            }
        }
        
        log.info("✅ Successfully scraped {} books from {}", books.size(), source);
        return books;
    }

    // CLEANING METHODS
    private String cleanTitle(String title) {
        if (title == null) return "";
        return title.trim().replaceAll("\\s+", " ");
    }

    private String cleanAuthor(String author) {
        if (author == null) return "";
        return author.trim().replaceAll("\\s+", " ");
    }

    private String cleanDescription(String description) {
        if (description == null) return "";
        return description.trim().replaceAll("\\s+", " ");
    }

    private Double cleanPrice(String priceText) {
        if (priceText == null || priceText.isEmpty()) return null;
        // Remove currency symbols, commas, spaces
        String cleaned = priceText.replaceAll("[^\\d.]", "");
        try {
            return Double.parseDouble(cleaned);
        } catch (NumberFormatException e) {
            log.debug("Could not parse price: '{}'", priceText);
            return null;
        }
    }

    private Double cleanRating(String ratingText) {
        if (ratingText == null || ratingText.isEmpty()) return null;
        // Extract stars from "★★★★☆ (342)"
        String stars = ratingText.replaceAll("\\s*\\(.*\\)", "");
        int filledStars = 0;
        for (char c : stars.toCharArray()) {
            if (c == '★') filledStars++;
        }
        return (double) filledStars;
    }

    private String cleanCategory(String category) {
        if (category == null) return "Uncategorized";
        return category.trim();
    }
}