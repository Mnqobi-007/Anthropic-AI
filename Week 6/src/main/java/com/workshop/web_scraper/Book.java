package com.workshop.web_scraper;

public class Book {
	private String author;
	private String title;
	private String description;
	private Double price;
	private Double rating;
	private boolean inStock;
	private String category;
	public Book() {
		super();
	}
	public Book(String title, String author, String description, Double price, Double rating, boolean inStock,
			String category) {
		super();
		this.author = author;
		this.title = title;
		this.description = description;
		this.price = price;
		this.rating = rating;
		this.inStock = inStock;
		this.category = category;
	}
	public String getAuthor() {
		return author;
	}
	public void setAuthor(String author) {
		this.author = author;
	}
	public String getTitle() {
		return title;
	}
	public void setTitle(String title) {
		this.title = title;
	}
	public String getDescription() {
		return description;
	}
	public void setDescription(String description) {
		this.description = description;
	}
	public Double getPrice() {
		return price;
	}
	public void setPrice(Double price) {
		this.price = price;
	}
	public Double getRating() {
		return rating;
	}
	public void setRating(Double rating) {
		this.rating = rating;
	}
	public boolean isInStock() {
		return inStock;
	}
	public void setInStock(boolean inStock) {
		this.inStock = inStock;
	}
	public String getCategory() {
		return category;
	}
	public void setCategory(String category) {
		this.category = category;
	}
	
	@Override
    public String toString() {
        return String.format("Book{title='%s', author='%s', price=%.2f, inStock=%s}", 
                           title, author, price != null ? price : 0.0, inStock);
    }
	
}
