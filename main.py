from scraper.amazon_scraper import AmazonScraper
from scraper.flipkart_scraper import FlipkartScraper
from utils.cleaner import clean_data
from database.db import save_products, index_products
from config.settings import USE_ELASTICSEARCH
from utils.logger import logger
import pandas as pd
import asyncio

async def main():
    logger.info("Scraping started")

    # Scrape from websites asynchronously
    async with AmazonScraper() as amazon_scraper, FlipkartScraper() as flipkart_scraper:
        try:
            amazon_products, flipkart_products = await asyncio.gather(
                amazon_scraper.scrape(),
                flipkart_scraper.scrape()
            )
        except Exception as e:
            logger.warning(f"Error during scraping: {e}")
            # fall back to empty lists to allow pipeline to continue
            amazon_products, flipkart_products = [], []

    all_products = amazon_products + flipkart_products

    logger.info(f"Scraped {len(all_products)} products")

    # Convert to DataFrame
    df = pd.DataFrame(all_products)

    # Clean data
    df_clean = clean_data(df)

    # Save to database
    try:
        save_products(df_clean.to_dict('records'))
        logger.info("Data saved to database")
    except Exception as e:
        logger.error(f"Error saving to database: {e}")

    # Index to Elasticsearch (only if enabled)
    if USE_ELASTICSEARCH:
        try:
            index_products(df_clean.to_dict('records'))
        except Exception as e:
            logger.warning(f"Error indexing to Elasticsearch: {e}")
    else:
        logger.info("Elasticsearch disabled; skipping indexing")

    # Export to CSV with retry and cleanup of old timestamped files
    import os
    import glob
    import time
    from datetime import datetime, UTC

    csv_path = 'data/products.csv'
    
    def cleanup_old_csv_files(max_keep=5):
        """Remove old timestamped CSV files, keeping only the most recent max_keep files."""
        try:
            pattern = 'data/products_*.csv'
            files = sorted(glob.glob(pattern), reverse=True)
            if len(files) > max_keep:
                for old_file in files[max_keep:]:
                    try:
                        os.remove(old_file)
                    except Exception:
                        pass
        except Exception:
            pass

    try:
        # Attempt 1: Direct write
        df_clean.to_csv(csv_path, index=False)
        logger.info("CSV exported successfully")
    except PermissionError:
        # File is locked; attempt to write with retry
        retry_count = 0
        max_retries = 2
        while retry_count < max_retries:
            try:
                time.sleep(0.5)  # brief delay to allow other process to release handle
                df_clean.to_csv(csv_path, index=False)
                logger.info("CSV exported successfully")
                break
            except PermissionError:
                retry_count += 1
                if retry_count >= max_retries:
                    # fallback to timestamped file
                    timestamp = datetime.now(UTC).strftime('%Y%m%d_%H%M%S')
                    fallback = f'data/products_{timestamp}.csv'
                    try:
                        df_clean.to_csv(fallback, index=False)
                        logger.info(f"CSV exported to {fallback}")
                        cleanup_old_csv_files(max_keep=5)
                    except Exception as e:
                        logger.error(f"Failed to export CSV: {e}")
    except Exception as e:
        logger.error(f"Failed to export CSV: {e}")

if __name__ == "__main__":
    asyncio.run(main())

##hello updated code