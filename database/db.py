from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config.settings import DATABASE_URL
from datetime import datetime, UTC
from utils.logger import logger

# Elasticsearch import and settings are optional
from config.settings import ELASTICSEARCH_HOST, ELASTICSEARCH_PORT, ELASTICSEARCH_INDEX, USE_ELASTICSEARCH

try:
    from elasticsearch import Elasticsearch
except ImportError:
    Elasticsearch = None

Base = declarative_base()

class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    product_name = Column(String)
    price = Column(Float)
    rating = Column(Float)
    url = Column(String)
    scraped_at = Column(DateTime, default=lambda: datetime.now(UTC))

engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)

# initialize Elasticsearch client only if configured and available
es = None
if USE_ELASTICSEARCH and Elasticsearch is not None:
    try:
        es = Elasticsearch([f'http://{ELASTICSEARCH_HOST}:{ELASTICSEARCH_PORT}'])
    except Exception as e:
        logger.warning(f"Elasticsearch initialization failed, indexing disabled: {e}")
        es = None

def save_products(products):
    session = Session()
    try:
        for product in products:
            prod = Product(
                product_name=product['product_name'],
                price=product['price'],
                rating=product['rating'],
                url=product['url'],
                scraped_at=datetime.fromisoformat(product['scraped_at']) if isinstance(product['scraped_at'], str) else product['scraped_at']
            )
            session.add(prod)
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

def index_products(products):
    if not USE_ELASTICSEARCH or es is None:
        logger.info("Elasticsearch indexing skipped")
        return
    try:
        for product in products:
            es.index(index=ELASTICSEARCH_INDEX, body=product, id=product['url'])
        logger.info("Products indexed in Elasticsearch")
    except Exception as e:
        logger.warning(f"Error indexing to Elasticsearch: {e}")