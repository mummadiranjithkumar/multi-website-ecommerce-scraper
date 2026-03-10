# Multi-Website E-commerce Scraper

## Project Overview
This project is a Python-based scraper for collecting product data from multiple e-commerce websites. It now scrapes real book listings from https://books.toscrape.com using BeautifulSoup.

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

## Installation
1. Clone or download the project.
2. Navigate to the ecommerce_scraper directory.
3. Install dependencies: `pip install -r requirements.txt`

## Configuration
Create a `.env` file in the root directory with the following variables (optional):
- `DATABASE_URL`: Database URL (default: sqlite:///products.db)
- `PROXIES`: Comma-separated list of proxy URLs
- `USE_REDIS`: Whether to use Redis for caching (default: **False**). Set to `True` in `.env` to enable caching, or leave unset to disable.
- `REDIS_HOST`: Redis host (default: localhost)
- `REDIS_PORT`: Redis port (default: 6379)
- `REDIS_DB`: Redis database (default: 0)

> Redis connection is attempted only if `USE_REDIS` is true. If a connection fails, the scraper logs a warning and continues without caching.
- `USE_ELASTICSEARCH`: Whether to index into Elasticsearch (default: **False**). Set to `True` to enable.
- `ELASTICSEARCH_HOST`: Elasticsearch host (default: localhost)
- `ELASTICSEARCH_PORT`: Elasticsearch port (default: 9200)
- `ELASTICSEARCH_INDEX`: Elasticsearch index name (default: products)

> Elasticsearch connection is only attempted if `USE_ELASTICSEARCH` is true. Failures are logged and do not stop execution.

## How to Run
### Local
Run the main script: `python main.py`

This will scrape data from the configured websites (now using https://books.toscrape.com), clean it, save to database, index to Elasticsearch (if available), and export to CSV.

> **Note:** Redis and Elasticsearch are optional services. If Redis is not running, caching will be disabled and the scraper continues normally. Elasticsearch errors are logged but do not stop execution.

### Docker
1. Ensure Docker and Docker Compose are installed.
2. Run: `docker-compose up --build`

This will start the app along with Redis and Elasticsearch services.

## Project Structure
- `main.py`: Entry point
- `scraper/`: Scraper modules
- `database/`: Database operations and Elasticsearch indexing
- `utils/`: Utilities for cleaning and logging
- `config/`: Configuration settings
- `data/`: Output CSV file
- `Dockerfile`: Docker image definition
- `docker-compose.yml`: Docker Compose configuration