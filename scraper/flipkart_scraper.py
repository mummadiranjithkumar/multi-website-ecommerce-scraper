from scraper.base_scraper import BaseScraper
import json
import requests
from bs4 import BeautifulSoup
import asyncio
from datetime import datetime, UTC
import re

class FlipkartScraper(BaseScraper):
    def __init__(self):
        # reuse the same books site to simulate a second website
        super().__init__('https://books.toscrape.com')

    async def scrape(self):
        cache_key = 'flipkart_products'
        cached = self.check_cache(cache_key)
        if cached:
            self.logger.info("Using cached data for Flipkart")
            return json.loads(cached)

        products = await asyncio.to_thread(self._fetch_products)
        self.set_cache(cache_key, json.dumps(products))
        return products

    def _fetch_products(self):
        products = []
        # scrape pages 3 and 4 to differentiate from AmazonScraper
        for page in range(3, 5):
            url = f"{self.base_url}/catalogue/page-{page}.html"
            try:
                headers = {'User-Agent': self.get_user_agent()}
                proxy = self.get_proxy()
                resp = requests.get(url, headers=headers, proxies={'http': proxy, 'https': proxy} if proxy else None, timeout=10)
                resp.raise_for_status()
            except Exception as e:
                self.logger.warning(f"Request failed for {url}: {e}")
                break

            soup = BeautifulSoup(resp.text, 'html.parser')
            for article in soup.select('article.product_pod'):
                try:
                    title = article.h3.a['title']
                    price_elem = article.select_one('p.price_color')
                    if price_elem:
                        price_text = price_elem.text.strip()
                        # Clean price: keep only digits and decimal point
                        clean_price = re.sub(r'[^\d.]', '', price_text).strip()
                        if clean_price:
                            try:
                                price = float(clean_price)
                            except ValueError:
                                self.logger.warning(f"Failed to parse price '{price_text}' for product {title}")
                                price = 0.0
                        else:
                            price = 0.0
                    else:
                        self.logger.warning(f"No price found for product {title}")
                        price = 0.0
                    classes = article.p['class']
                    rating_word = classes[1] if len(classes) > 1 else ''
                    rating_map = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}
                    rating = rating_map.get(rating_word, 0)
                    href = article.h3.a['href']
                    product_url = self.base_url + '/' + href
                    products.append({
                        'product_name': title,
                        'price': price,
                        'rating': rating,
                        'url': product_url,
                        'scraped_at': datetime.now(UTC).isoformat()
                    })
                except Exception as e:
                    self.logger.warning(f"Error processing product: {e}")
                    continue
        return products