# Multi-Website E-commerce Scraper


## Project Overview
This project is a Python-based scraper for collecting product data from multiple e-commerce websites. It scrapes real book listings from https://books.toscrape.com using BeautifulSoup and demonstrates a complete scraping pipeline including extraction, cleaning, storage, and export.

## Example Output

Below is an example of scraped product data exported to CSV and opened in Excel.

![Scraper Output](assets/output.png)

## Features
- Scrapes product name, price, rating, URL, and timestamp
- Supports multiple websites with modular scraper design
- Asynchronous scraping with aiohttp
- Rotating user agents to avoid detection
- Retry logic with exponential backoff using tenacity
- Proxy support
- Redis caching for scraped data
- Elasticsearch indexing for search
- Pagination support for multi-page scraping
- Data cleaning and deduplication
- Saves data to SQLite database
- Exports data to CSV
- Comprehensive logging with file and console output
- Docker support for containerization

## Technologies Used
- Python
- aiohttp for asynchronous HTTP requests
- tenacity for retry logic
- fake-useragent for rotating user agents
- redis for caching
- elasticsearch for indexing
- SQLAlchemy for database operations
- Pandas for data manipulation
- BeautifulSoup for HTML parsing
- Logging for error tracking
- Docker for containerization

## Installation

1. Clone the repository
>>>>>>> 69eea01736ad8dc09dbd76c570b5b7a92d285915
