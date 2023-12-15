from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urljoin, urlparse
import requests, logging
from datetime import datetime
import platform

from ..config import MODE
from ..data_processing import data_processing

def get_html_content(url):
    parsed_url = urlparse(url).netloc
    domain = parsed_url.split('.')[1]
    logging.debug(f"url : {url}")
    logging.debug(f"parsed_url : {parsed_url}")
    logging.debug(f"domain : {domain}")
    logging.debug(f"MODE : {MODE}")
    # Function to get HTML content based on mode
    if MODE == "Development":
        html_file_path = f"./test/{domain}.html"
        try:
            with open(html_file_path, "r", encoding="utf-8") as html_file:
                return html_file.read()
        except FileNotFoundError:
            logging.exception(f"HTML file not found at {html_file_path}")
            return None
    else:
        # Use Selenium to fetch HTML content
        try:
            logging.info(f"Attempting to fetch HTML content from: {url}")
            firefox_options = webdriver.FirefoxOptions()
            firefox_options.add_argument("--headless")
            
            if platform.system() == "Windows":
                executable_path = "./.venv/Scripts/geckodriver.exe"
                firefox_service_obj = FirefoxService(executable_path)
                driver = webdriver.Firefox(service=firefox_service_obj, options=firefox_options)
            elif platform.system() == "Linux":
                executable_path = "./.venv/bin/geckodriver"
                firefox_service_obj = FirefoxService(executable_path)
                firefox_binary_path = '/usr/bin/firefox-esr'
                binary = FirefoxBinary(firefox_binary_path)
                # driver = webdriver.Firefox(firefox_binary=binary, service=firefox_service_obj, options=firefox_options)
                driver = webdriver.Firefox(service=firefox_service_obj, options=firefox_options)

            driver.get(url)
            wait = WebDriverWait(driver, 300)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".item")))
            html_content = driver.page_source
            driver.quit()
            return html_content
        except Exception as e:
            logging.exception(f"Failed to fetch HTML content. Error: {e}")
            return None        

def scrape_product_info(selectors):
    try:
        # product_selector, product_name_selector, original_price_selector, discount_selector, price_selector, detail_href_selector, description_selector, category_selector = selectors

        url = selectors["url"]
        html_content = get_html_content(url)        

        soup = BeautifulSoup(html_content, "html.parser")

        # Use a selector that captures both product names and prices
        product_info_elements = soup.select(selectors["product_selector"])  # Adjust this selector based on the actual HTML
        # logging.info(product_info_elements)

        # Extract product names and prices
        product_data = []
        for element in product_info_elements:
            e = element.select_one(selectors["product_name_selector"])
            product_name = e.text.strip() if e else None
            e = element.select_one(selectors["original_price_selector"])
            original_price = e.text.strip() if e else None
            e = element.select_one(selectors["discount_selector"])
            discount = e.text.strip() if e else None
            e = element.select_one(selectors["price_selector"])
            price = e.text.strip() if e else None

            if product_name and price:
                description = ""
                category = ""
                urlDesc = ""
                e = element.select_one(selectors["detail_href_selector"])
                if e and e.get("href") != "" and MODE != "Development":
                    try:
                        logging.debug(f"url: {url}")
                        urlDomain = f"https://{urlparse(url).netloc}"
                        logging.debug(f"url: {urlDomain}")
                        href = e.get('href')
                        logging.debug(f"href: {href}")
                        urlDesc = urljoin(urlDomain, href)
                        logging.debug(f"urlDesc: {urlDesc}")
                        # urlDesc = f"https://{urlparse(url).netloc}{e.get('href')}"
                    except Exception as e:
                        logging.exception(f"An unexpected error occurred for parsing URL: {urlDesc}. Error: {e}")
                        category = url.split(".")[1]
                else:
                    category = url.split(".")[1]

                if original_price and discount:
                    original_price = original_price.replace(discount, "").replace("\n", "")

                price = float(price.replace("Rp", "").replace(".", "").strip()) if price else None
                original_price = float(original_price.replace("Rp", "").replace(".", "").strip()) if original_price else None
                discount = float(discount.replace("%", "").strip()) if discount else None

                product_data.append({
                    "name": product_name, 
                    "original_price": original_price, 
                    "price": price, 
                    "discount_percentage": discount, 
                    "detail": description, 
                    "category": category,
                    "platform": urlparse(url).netloc,
                    "urlDesc": urlDesc,
                    "create_date": datetime.now()
                    })

        return product_data

    except Exception as e:
        logging.exception(f"An unexpected error occurred for URL: {url}. Error: {e}")
        raise e
    
def get_product_description(product_data, selectors):
    
    for product in product_data:
        try:
            responseDesc = requests.get(product["urlDesc"], timeout=1)

            if responseDesc.status_code == 200:
                soupDesc = BeautifulSoup(responseDesc.text, "html.parser")

                el = soupDesc.select_one(selectors["description_selector"])
                description = el.text.strip() if el else None
                last_a_tag = soupDesc.select_one(selectors["category_selector"])
                category = last_a_tag.text.strip() if last_a_tag else None

                product["detail"] = description
                product["category"] = category
            else:
                logging.error(f"Failed to fetch url: {urlDesc}. Status code: {responseDesc.status_code}")

        except Exception as e:
            pass

    return product_data
    
def list_element_hierarchy(selectors):

    try:
        html_content = get_html_content(selectors["url"])

        soup = BeautifulSoup(html_content, "html.parser")

        # Extract prices
        parent_tags = []
        target_element = soup.select_one(selectors["info_selector"])
        
        if target_element:
            if target_element.find_all(recursive=False):
                target_element = target_element.find_all(recursive=False)[-1]

            parents = list(reversed(list(target_element.find_parents())))
                
            parent_tag = ""
            for parent in parents:
                parent_tag += f"{parent.name}"
                if (parent.get('class')):
                    parent_tag += f".{parent.get('class')}"
                if (parent.get('id')):
                    parent_tag += f" #{parent.get('id')}"
                parent_tag += " > "
        
            parent_tag += f"{target_element.name}"
            if (target_element.get('class')):
                parent_tag += f".{target_element.get('class')}"
            if (target_element.get('id')):
                parent_tag += f" #{target_element.get('id')}"

            parent_tags.append({selectors["info_selector"] : parent_tag})

        return parent_tags

    except Exception as target_element:
        logging.exception(f"An unexpected error occurred for list_elements. Error: {target_element}")
        raise target_element
    
def populate_data_all():   
    try:
        selectors = {
            "url": "https://www.klikindomaret.com/page/unilever-officialstore",
            "product_selector" : ".item", 
            "product_name_selector": ".title", 
            "original_price_selector": ".disc-price", 
            "discount_selector": ".discount", 
            "price_selector": ".price-value", 
            "detail_href_selector": "a:first-of-type", 
            "description_selector": "#desc-product", 
            "category_selector": ".breadcrumb a:last-of-type"
        }
        product_data = scrape_product_info(selectors)
        product_data = get_product_description(product_data, selectors)
        data_processing.parse_and_save_data(product_data)    
    except Exception as e:
        logging.exception(f"An unexpected error occurred while processing URL {selectors['url']}, error: {e}")

    try:
        selectors = {
            "url": "https://www.blibli.com/cari/unilever%20indonesia%20official?seller=Official%20Store",
            "product_selector" : ".product__container", 
            "product_name_selector": ".blu-product__name", 
            "original_price_selector": ".blu-product__price-before", 
            "discount_selector": ".blu-product__price-discount", 
            "price_selector": ".blu-product__price-after", 
            "detail_href_selector": "a:first-of-type", 
            "description_selector": ".product-features", 
            "category_selector": "span.value[data-testid='descriptionInfoCategory']"
        }
        product_data = scrape_product_info(selectors)
        product_data = get_product_description(product_data, selectors)
        data_processing.parse_and_save_data(product_data)
    except Exception as e:
        logging.exception(f"An unexpected error occurred while processing URL {selectors['url']}, error: {e}")

    try:
        selectors = {
            "url": "https://www.tokopedia.com/unilever/product",
            "product_selector" : ".prd_container-card", 
            "product_name_selector": ".prd_link-product-name", 
            "original_price_selector": ".prd_label-product-slash-price", 
            "discount_selector": ".prd_badge-product-discount", 
            "price_selector": ".prd_link-product-price", 
            "detail_href_selector": "a:first-of-type", 
            "description_selector": ".product-features", 
            "category_selector": ".breadcrumb li:nth-last-child(2)"
        }
        product_data = scrape_product_info(selectors)
        product_data = get_product_description(product_data, selectors)
        data_processing.parse_and_save_data(product_data)
    except Exception as e:
        logging.exception(f"An unexpected error occurred while processing URL {selectors['url']}, error: {e}")
    
def repopulate_data():
    try:
        data_processing.clean_data()
        populate_data_all()
    
    except Exception as e:
        logging.exception(f"An unexpected error occurred while processing data: {e}")
        raise e
