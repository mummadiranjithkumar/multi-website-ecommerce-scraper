import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///products.db')

# Proxy settings
PROXIES = os.getenv('PROXIES', '').split(',') if os.getenv('PROXIES') else []

# Redis settings
# toggle Redis usage; defaults to False (optional service)
USE_REDIS = os.getenv('USE_REDIS', 'False').lower() in ('1', 'true', 'yes')
REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
REDIS_DB = int(os.getenv('REDIS_DB', 0))

# Elasticsearch settings
# toggle Elasticsearch indexing; defaults to False (optional service)
USE_ELASTICSEARCH = os.getenv('USE_ELASTICSEARCH', 'False').lower() in ('1', 'true', 'yes')
ELASTICSEARCH_HOST = os.getenv('ELASTICSEARCH_HOST', 'localhost')
ELASTICSEARCH_PORT = int(os.getenv('ELASTICSEARCH_PORT', 9200))
ELASTICSEARCH_INDEX = os.getenv('ELASTICSEARCH_INDEX', 'products')