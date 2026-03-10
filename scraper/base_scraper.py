from abc import ABC, abstractmethod
from datetime import datetime, UTC
import asyncio
import aiohttp
from tenacity import retry, stop_after_attempt, wait_exponential
from fake_useragent import UserAgent
import redis
import random
from config.settings import PROXIES, REDIS_HOST, REDIS_PORT, REDIS_DB, USE_REDIS
from utils.logger import logger

class BaseScraper(ABC):
    def __init__(self, base_url):
        self.base_url = base_url
        self.ua = UserAgent()
        self.session = None
        self.logger = logger

        # Initialize Redis only if enabled via configuration
        self.redis_client = None
        if USE_REDIS:
            try:
                client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
                client.ping()  # verify connection
                self.redis_client = client
            except Exception as e:
                self.logger.warning(f"Redis connection failed, caching disabled: {e}")
                self.redis_client = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()

    def get_user_agent(self):
        return self.ua.random

    def get_proxy(self):
        if PROXIES:
            return random.choice(PROXIES)
        return None

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    async def make_request(self, url):
        headers = {'User-Agent': self.get_user_agent()}
        proxy = self.get_proxy()
        async with self.session.get(url, headers=headers, proxy=proxy) as response:
            return await response.text()

    def check_cache(self, key):
        if not self.redis_client:
            return None
        try:
            return self.redis_client.get(key)
        except Exception as e:
            self.logger.warning(f"Failed to read from Redis cache: {e}")
            return None

    def set_cache(self, key, value, ttl=3600):
        if not self.redis_client:
            return
        try:
            self.redis_client.setex(key, ttl, value)
        except Exception as e:
            self.logger.warning(f"Failed to write to Redis cache: {e}")



    def get_timestamp(self):
        # return timezone-aware UTC datetime
        return datetime.now(UTC)