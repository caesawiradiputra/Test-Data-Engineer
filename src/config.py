import os
from dotenv import load_dotenv

# Load environment variables from .env file
ENVIRONMENT = os.environ.get("ENVIRONMENT", "dev")
load_dotenv(f".env.{ENVIRONMENT}", override=True)

# Get environment variables or use default values
DATABASE_NAME = os.getenv("DATABASE_NAME", "postgres")
DATABASE_USER = os.getenv("DATABASE_USER", "postgres")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD", "admin123")
DATABASE_HOST = os.getenv("DATABASE_HOST", "localhost")
DATABASE_PORT = os.getenv("DATABASE_PORT", "5432")

# Construct the connection string
CONNECTION_STRING = f"dbname={DATABASE_NAME} user={DATABASE_USER} password={DATABASE_PASSWORD} host={DATABASE_HOST} port={DATABASE_PORT}"

MODE = os.getenv("MODE", "Development")
DEBUG = os.getenv("DEBUG", True)

SELECTORS = {
    "klikindomaret_selector": {
        "url": "https://www.klikindomaret.com/page/unilever-officialstore",
        "product_selector" : ".item", 
        "product_name_selector": ".title", 
        "original_price_selector": ".disc-price", 
        "discount_selector": ".discount", 
        "price_selector": ".price-value", 
        "detail_href_selector": "a:first-of-type", 
        "description_selector": "#desc-product", 
        "category_selector": ".breadcrumb a:last-of-type"
    },
    "blibli_selector": {
        "url": "https://www.blibli.com/cari/unilever%20indonesia%20official?seller=Official%20Store",
        "product_selector" : ".product__container", 
        "product_name_selector": ".blu-product__name", 
        "original_price_selector": ".blu-product__price-before", 
        "discount_selector": ".blu-product__price-discount", 
        "price_selector": ".blu-product__price-after", 
        "detail_href_selector": "a:first-of-type", 
        "description_selector": ".product-features", 
        "category_selector": "span.value[data-testid='descriptionInfoCategory']"
    },
    "tokopedia_selector": {
        "url": "https://www.tokopedia.com/unilever/product",
        "product_selector": ".prd_container-card",
        "product_name_selector": ".prd_link-product-name",
        "original_price_selector": ".prd_label-product-slash-price",
        "discount_selector": ".prd_badge-product-discount",
        "price_selector": ".prd_link-product-price",
        "detail_href_selector": "a:first-of-type",
        "description_selector": ".product-features",
        "category_selector": ".breadcrumb li:nth-last-child(2)"
    }
}