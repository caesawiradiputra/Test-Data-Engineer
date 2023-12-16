from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urljoin, urlparse
import requests, logging, time
from datetime import datetime
import platform

from ..config import MODE, SELECTORS
from ..data_processing import data_processing

def get_html_content(url, selector, blnScroll=False):
    parsed_url = urlparse(url).netloc
    domain = parsed_url.split('.')[1]
    logging.debug(f"url : {url}")
    logging.debug(f"parsed_url : {parsed_url}")
    logging.debug(f"domain : {domain}")
    logging.debug(f"MODE : {MODE}")
    # Function to get HTML content based on mode
    start_time = time.time()
    if MODE == "Testing":
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
            wait = WebDriverWait(driver, 30)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
            if blnScroll:
                logging.info(f"Scrolling until the end of web : {url}")
                for i in range(3):
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(1)
            html_content = driver.page_source
            driver.quit()

            execution_time = time.time() - start_time
            logging.info(f"Successfully fetched HTML content from: {url}, in: {execution_time} seconds")
            return html_content
        except Exception as e:
            if start_time: execution_time = time.time() - start_time
            logging.exception(f"Failed to fetch HTML content. Error: {e}, after: {execution_time} seconds")
            raise e        

def scrape_product_info(selectors):
    try:
        # product_selector, product_name_selector, original_price_selector, discount_selector, price_selector, detail_href_selector, description_selector, category_selector = selectors

        url = selectors["url"]
        html_content = get_html_content(url, selectors["web_selector"], True)    
        # html_content = get_html_content(url, "*", True)       
        logging.info(f"Attempting to scrape HTML content from: {url}")
        start_time = time.time()

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
                category = url.split(".")[1]
                urlDesc = None
                e = element.select_one(selectors["detail_href_selector"])
                if e and e.get("href") != "":
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

        execution_time = time.time() - start_time
        logging.info(f"Successfully scrape HTML content from: {url}, in: {execution_time} seconds")
        return product_data

    except Exception as e:
        if html_content: logging.error(f"Error processing html_content: {html_content}")
        if start_time: execution_time = time.time() - start_time
        logging.exception(f"An unexpected error occurred for URL: {url}. Error: {e}, after: {execution_time} seconds")
        raise e
    
def get_product_description2(product_data, selectors):
    try:
        start_time = time.time()
        logging.info(f"Attempting to get product description from: {selectors['url']}")
        for product in product_data:
            try:
                if product["urlDesc"]:
                    logging.debug(f"Attempting to get product description from: {product['urlDesc']}")
                    responseDesc = requests.get(product["urlDesc"], timeout=5)

                    if responseDesc.status_code == 200:
                        logging.debug(f"Desc html_content: {responseDesc.text}")
                        soupDesc = BeautifulSoup(responseDesc.text, "html.parser")

                        el = soupDesc.select_one(selectors["description_selector"])
                        logging.debug(f"Desc description selectors: {selectors['description_selector']}")
                        logging.debug(f"Desc description el: {el}")
                        description = el.text.strip() if el else None
                        logging.debug(f"Desc description: {description}")
                        el = soupDesc.select_one(selectors["category_selector"])
                        logging.debug(f"Desc description selectors: {selectors['category_selector']}")
                        logging.debug(f"Desc category el: {el}")
                        category = el.text.strip() if el else None
                        logging.debug(f"Desc category: {category}")

                        product["detail"] = description
                        product["category"] = category
                    else:
                        logging.error(f"Failed to fetch url: {product['urlDesc']}.")

            except Exception as e:
                if responseDesc.text: logging.debug(f"Desc html_content: {responseDesc.text}")
                logging.error(f"An unexpected error when get product description from: {product['urlDesc']}, error: {e}")

        execution_time = time.time() - start_time
        logging.info(f"Successfully get product description from: {selectors['url']}, in: {execution_time} seconds")
        return product_data
    except Exception as e:
        if start_time: execution_time = time.time() - start_time
        logging.exception(f"An unexpected error occurred for URL: {selectors['url']}. Error: {e}, after: {execution_time} seconds")
        return product_data
    
def get_product_description(product_data, selectors):
    try:
        start_time = time.time()
        logging.info(f"Attempting to get product description from: {selectors['url']}")
        for product in product_data:
            try:
                if product["urlDesc"]:
                    logging.debug(f"Attempting to get product description from: {product['urlDesc']}")
                    html_content = get_html_content(product["urlDesc"], selectors["description_selector"])
                    # logging.debug(f"Desc html_content: {html_content}")

                    if html_content:
                        soupDesc = BeautifulSoup(html_content, "html.parser")

                        el = soupDesc.select_one(selectors["description_selector"])
                        logging.debug(f"Desc description selectors: {selectors['description_selector']}")
                        logging.debug(f"Desc description el: {el}")
                        description = el.text.strip() if el else None
                        logging.debug(f"Desc description: {description}")
                        el = soupDesc.select_one(selectors["category_selector"])
                        logging.debug(f"Desc description selectors: {selectors['category_selector']}")
                        logging.debug(f"Desc category el: {el}")
                        category = el.text.strip() if el else None
                        logging.debug(f"Desc category: {category}")

                        product["detail"] = description
                        product["category"] = category
                    else:
                        logging.error(f"Failed to fetch url: {product['urlDesc']}.")

            except Exception as e:
                if html_content: logging.debug(f"Desc html_content: {html_content}")
                logging.error(f"An unexpected error when get product description from: {product['urlDesc']}, error: {e}")

        execution_time = time.time() - start_time
        logging.info(f"Successfully get product description from: {selectors['url']}, in: {execution_time} seconds")
        return product_data
    except Exception as e:
        if start_time: execution_time = time.time() - start_time
        logging.exception(f"An unexpected error occurred for URL: {selectors['url']}. Error: {e}, after: {execution_time} seconds")
        return product_data

    
def list_element_hierarchy(selectors):

    try:
        logging.info(f"Attempting to get list of element from: {selectors['check_element_url']}")
        html_content = get_html_content(selectors["check_element_url"], selectors["check_element_selector"], True)

        soup = BeautifulSoup(html_content, "html.parser")

        # Extract prices
        parent_tags = []
        target_element = soup.select_one(selectors["check_element_selector"])
        
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

            parent_tags.append({selectors["check_element_selector"] : parent_tag})
        else:
            logging.debug(f"html_content: {html_content}")

        return parent_tags

    except Exception as e:
        logging.exception(f"An unexpected error occurred for list_elements. Error: {e}")
        raise e
    
def populate_data_all():   
    try:
        selectors = SELECTORS["klikindomaret_selector"]
        product_data = scrape_product_info(selectors)
        # product_data = get_product_description(product_data, selectors)
        data_processing.parse_and_save_data(product_data)    
    except Exception as e:
        logging.exception(f"An unexpected error occurred while processing URL {selectors['url']}, error: {e}")
        raise e

    try:
        selectors = SELECTORS["blibli_selector"]
        product_data = scrape_product_info(selectors)
        # product_data = get_product_description(product_data, selectors)
        data_processing.parse_and_save_data(product_data)
    except Exception as e:
        logging.exception(f"An unexpected error occurred while processing URL {selectors['url']}, error: {e}")
        raise e

    try:
        selectors = SELECTORS["blibli_tokopedia"]
        product_data = scrape_product_info(selectors)
        # product_data = get_product_description(product_data, selectors)
        data_processing.parse_and_save_data(product_data)
    except Exception as e:
        logging.exception(f"An unexpected error occurred while processing URL {selectors['url']}, error: {e}")
        raise e
    
def repopulate_all_data():
    try:
        data_processing.clean_data()
        populate_data_all()
    
    except Exception as e:
        logging.exception(f"An unexpected error occurred while processing data: {e}")
        raise e
