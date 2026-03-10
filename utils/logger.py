import logging
import sys
from datetime import datetime

def setup_logger():
    logger = logging.getLogger('ecommerce_scraper')
    logger.setLevel(logging.DEBUG)

    # Create handlers with UTF-8 encoding for file
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)

    file_handler = logging.FileHandler('scraper.log', encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)

    # Create formatters and add to handlers
    console_format = logging.Formatter('%(levelname)s - %(message)s')
    file_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    console_handler.setFormatter(console_format)
    file_handler.setFormatter(file_format)

    # Add handlers to logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger

logger = setup_logger()