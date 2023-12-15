# src/crawler/crawl.py
import requests
import logging, re
import psycopg2

from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import urlparse

from ..config import CONNECTION_STRING

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Global variable for mode (Testing or Production)
MODE = "Testing"  # Change this value as needed

def crawl_and_save_data():
    # Implement web scraping logic to extract product price data from websites
    # Use BeautifulSoup, requests, or your preferred web scraping library

    # Placeholder: Sample data for demonstration purposes
    product_data = [
        {"name": "Product1", "price": 10.99, "platform": "Website1"},
        {"name": "Product2", "price": 20.49, "platform": "Website2"},
        # Add more data as needed
    ]

    # Connect to the database
    conn = psycopg2.connect(CONNECTION_STRING)
    cursor = conn.cursor()

    # Save the crawled data to the database
    for product in product_data:
        cursor.execute(
            "INSERT INTO product (name, price, platform, createdat) VALUES (%s, %s, %s, %s);",
            (product["name"], product["price"], product["platform"], datetime.now()),
        )

    # Commit changes and close the connection
    conn.commit()
    cursor.close()
    conn.close()

def crawl_and_save_data(url):
    # Implement web scraping logic to extract product price data from websites
    # Use BeautifulSoup, requests, or your preferred web scraping library

    # Placeholder: Sample data for demonstration purposes
    product_data = scrape_product_prices(url)

    # Connect to the database
    conn = psycopg2.connect(CONNECTION_STRING)
    cursor = conn.cursor()

    # Save the crawled data to the database
    for product in product_data:
        cursor.execute(
            "INSERT INTO product (name, price, platform, createdat) VALUES (%s, %s, %s, %s);",
            (product["name"], product["price"], product["platform"], datetime.now()),
        )

    # Commit changes and close the connection
    conn.commit()
    cursor.close()
    conn.close()

def parse_and_save_data(product_data):
    try:
        # Connect to the database
        conn = psycopg2.connect(CONNECTION_STRING)
        cursor = conn.cursor()

        # Save the crawled data to the database
        for product in product_data:
            cursor.execute("Select id from product_master where name = %s", (product["name"],))
            result = cursor.fetchone()

            if result:
                product_master_id = result[0]
            else:
                cursor.execute(
                    "INSERT INTO product_master (name, detail, type) VALUES (%s, %s, %s) RETURNING id;",
                    (
                        product.get("name", ""), 
                        product.get("detail", ""), 
                        "Unilever"
                    ),
                )
                product_master_id = cursor.fetchone()[0]


            cursor.execute(
                "INSERT INTO product (name, price, original_price, discount_percentage, detail, platform, create_date, product_master_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);",
                (
                    product.get("name", ""), 
                    product.get("price", None), 
                    product.get("original_price", None), 
                    product.get("discount_percentage", None), 
                    product.get("detail", ""), 
                    product.get("platform", ""), 
                    product.get("create_date", datetime.now()),
                    product_master_id
                ),
            )

        # Commit changes and close the connection
        conn.commit()
        cursor.close()
        conn.close()

    except psycopg2.Error as e:
        logging.error(f"Error connecting to the database: {e}")
        # Optionally, you can re-raise the exception to propagate it further
        raise e

    except Exception as e:
        logging.exception(f"An unexpected error occurred while parsing and saving data: {e}")
        raise e
    
def scrape_product_prices(url):
    # Send a GET request to the URL
    # return f"The requested URL is: {url}"
    response = requests.get(url)
    
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, "html.parser")

        # Find the elements containing product information (modify as needed)
        product_elements = soup.find_all("div", class_="each-item")

        product_list = []
        # Extract and print product details (modify as needed)
        for product in product_elements:
            product_name = product.find("div", class_="title")
            product_price = product.find("span", class_="normal price-value")

            product_name = product_name.text.strip() if product_name else None
            product_price = int(product_price.text.strip().replace("Rp ", "").replace(".", "")) if product_price else None

            if (product_name):
                product_data = {
                    "name": product_name,
                    "price": product_price,
                    "platform": url
                }

                product_list.append(product_data)
        
        return product_list

    else:
        return []
    
def scrape_product_info_klikindomaret2(url):
    try:
        logging.info(f"Attempting to fetch HTML content from: {url}")
        response = requests.get(url, timeout=300)

        if response.status_code == 200:
            logging.info(f"Successfully fetched HTML content from: {url}")
            soup = BeautifulSoup(response.text, "html.parser")

            # Use a selector that captures both product names and prices
            product_info_elements = soup.select(".item", limit=100)  # Adjust this selector based on the actual HTML
            # logging.info(product_info_elements)

            # Extract product names and prices
            product_data = []
            for element in product_info_elements:
                e = element.select_one(".title")
                product_name = e.text.strip() if e else None
                e = element.select_one(".disc-price")
                original_price = e.text.strip() if e else None
                e = element.select_one(".discount")
                discount = e.text.strip() if e else None
                e = element.select_one(".price-value")
                price = e.text.strip() if e else None

                if product_name and price:
                    description = ""
                    e = element.select_one("[href]")
                    if e and e.get("href") != "":
                        urlDesc = f"https://{urlparse(url).netloc}{e.get('href')}"
                        responseDesc = requests.get(urlDesc)

                        if responseDesc.status_code == 200:
                            soupDesc = BeautifulSoup(responseDesc.text, "html.parser")
                            elDesc = soupDesc.find(string=re.compile("Deskripsi"))
                            if elDesc:
                                description = elDesc.findNext().text.strip() if elDesc.findNext() else None
                        else:
                            logging.info(f"Failed to fetch url: {urlDesc}. Status code: {response.status_code}")

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
                        "platform": url, 
                        "create_date": datetime.now()
                        })

            return product_data

        else:
            logging.info(f"Failed to fetch data. Status code: {response.status_code}")
            return []

    except requests.exceptions.RequestException as e:
        logging.error(f"Request failed for URL: {url}. Error: {e}")
        raise e

    except Exception as e:
        logging.exception(f"An unexpected error occurred for URL: {url}. Error: {e}")
        raise e   

def scrape_product_info_blibli2(url):
    try:
        logging.info(f"Attempting to fetch HTML content from: {url}")

        # Set up Firefox options
        firefox_options = webdriver.FirefoxOptions()
        firefox_options.add_argument("--headless")  # Run in headless mode (no GUI)

        # Set up the Firefox driver
        executable_path = "./.venv/Scripts/geckodriver.exe"
        # driver = webdriver.Firefox(executable_path=executable_path, options=firefox_options)
        firefox_service_obj = Service(executable_path)
        driver = webdriver.Firefox(service=firefox_service_obj, options=firefox_options)

        # Navigate to the URL
        driver.get(url)

        # Wait for elements to load (adjust as needed)
        wait = WebDriverWait(driver, 300)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".product__container")))

        # Extract product information using appropriate selectors
        product_info_elements = driver.find_elements(By.CSS_SELECTOR, ".product__container")  # Limit to the first product

        # Extracted product data
        product_data = []

        for element in product_info_elements:
            product_name = element.find_element(By.CSS_SELECTOR, ".blu-product__name").text.strip()
            original_price = element.find_element(By.CSS_SELECTOR, ".blu-product__price-before").text.strip()
            discount = element.find_element(By.CSS_SELECTOR, ".blu-product__price-discount").text.strip()
            price = element.find_element(By.CSS_SELECTOR, ".blu-product__price-after").text.strip()

            if product_name and price:
                description = ""

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
                    "platform": url,
                    "create_date": datetime.now()
                })
                break

        driver.quit()

        return product_data

    except Exception as e:
        logging.error(f"An unexpected error occurred for URL: {url}. Error: {e}")
        raise e 
    
def scrape_product_info(url):
    try:
        logging.info(f"Attempting to fetch HTML content from: {url}")
        response = requests.get(url)

        if response.status_code == 200:
            logging.info(f"Successfully fetched HTML content from: {url}")
            soup = BeautifulSoup(response.text, "html.parser")

            # Use a selector that captures both product names and prices
            # product_info_elements = soup.find_all(attrs=re.compile("item"))  # Adjust this selector based on the actual HTML
            # product_info_elements = soup.find_all("div", ["item", "info"])  # Adjust this selector based on the actual HTML
            product_info_elements = soup.find_all(class_=soup_div_has_item)  # Adjust this selector based on the actual HTML
            logging.info(product_info_elements)

            # Extract product names and prices
            product_data = []
            for element in product_info_elements:
                # e = element.find("div", "title")
                e = element.find(class_=soup_has_title)
                product_name = e.text.strip() if e else None
                e = element.select_one("[class*='disc']")
                product_price_before = e.text.strip() if e else None
                e = element.select_one(".discount")
                discount = e.text.strip() if e else None
                e = element.find("span", "price-value")
                product_price_after = e.text.strip() if e else None

                if product_price_before and discount:
                    product_price_before = product_price_before.replace(discount, "").replace("\n", "")

                if product_name and product_price_after:
                    product_data.append({
                        "name": product_name, 
                        "original_price": product_price_before, 
                        "price": product_price_after, 
                        "discount_percentage": discount, 
                        "detail": None, 
                        "platform": url, 
                        "create_date": datetime.now()
                        })

            return product_data

        else:
            logging.info(f"Failed to fetch data. Status code: {response.status_code}")
            return None

    except requests.exceptions.RequestException as e:
        logging.error(f"Request failed for URL: {url}. Error: {e}")
        return None

    except Exception as e:
        logging.exception(f"An unexpected error occurred for URL: {url}. Error: {e}")
        return None
    
def soup_div_has_item(css_class):
    return css_class and re.compile("item").search(css_class)
    
def soup_has_title(css_class):
    return css_class and re.compile("title").search(css_class)
    
def soup_has_current_price(css_class):
    return css_class and re.compile("price").search(css_class)

    
def web_source_html(url):
    try:
        logging.info(f"Attempting to fetch HTML content from: {url}")

        # Set a timeout to prevent the request from taking too long
        response = requests.get(url, timeout=60)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            logging.info(f"Successfully fetched HTML content from: {url}")
            return BeautifulSoup(response.text, "html.parser")
        else:
            logging.error(f"Failed to fetch HTML content. Status code: {response.status_code}")
            return None

    except requests.exceptions.RequestException as e:
        logging.error(f"Request failed for URL: {url}. Error: {e}")
        return None

    except Exception as e:
        logging.exception(f"An unexpected error occurred for URL: {url}. Error: {e}")
        return None
    
def web_tag_html(url):
    try:
        logging.info(f"Attempting to fetch HTML content from: {url}")

        # Set a timeout to prevent the request from taking too long
        response = requests.get(url, timeout=60)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            logging.info(f"Successfully fetched HTML content from: {url}")
            soup = BeautifulSoup(response.text, "html.parser")
            tag_list = []
            tag_existing = []
            for tag in soup.find_all(True):
                # if not tag.name in tag_existing:
                #     tag_existing.append(tag.name)
                #     tag_list.append(tag.name)
                
                tag_list.append(tag.attr)
            return tag_list
        else:
            logging.error(f"Failed to fetch HTML content. Status code: {response.status_code}")
            return None

    except requests.exceptions.RequestException as e:
        logging.error(f"Request failed for URL: {url}. Error: {e}")
        return None

    except Exception as e:
        logging.exception(f"An unexpected error occurred for URL: {url}. Error: {e}")
        return None
    
def get_html_content(url):
    # Function to get HTML content based on mode
    if MODE == "Testing":
        html_file_path = "test/klikindomart.html"
        try:
            with open(html_file_path, "r", encoding="utf-8") as html_file:
                return html_file.read()
        except FileNotFoundError:
            logging.error(f"HTML file not found at {html_file_path}")
            return None
    else:
        # Use Selenium to fetch HTML content
        try:
            logging.info(f"Attempting to fetch HTML content from: {url}")
            firefox_options = webdriver.FirefoxOptions()
            firefox_options.add_argument("--headless")
            executable_path = "./.venv/Scripts/geckodriver.exe"
            firefox_service_obj = FirefoxService(executable_path)
            driver = webdriver.Firefox(service=firefox_service_obj, options=firefox_options)
            driver.get(url)
            wait = WebDriverWait(driver, 300)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".item")))
            html_content = driver.page_source
            driver.quit()
            return html_content
        except Exception as e:
            logging.error(f"Failed to fetch HTML content. Error: {e}")
            return None

def scrape_product_info_klikindomaret(url):
    try:
        logging.info(f"Attempting to fetch HTML content from: {url}")

        # Set up Firefox options
        firefox_options = webdriver.FirefoxOptions()
        firefox_options.add_argument("--headless")  # Run in headless mode (no GUI)

        # Set up the Firefox driver
        executable_path = "./.venv/Scripts/geckodriver.exe"
        # driver = webdriver.Firefox(executable_path=executable_path, options=firefox_options)
        firefox_service_obj = Service(executable_path)
        driver = webdriver.Firefox(service=firefox_service_obj, options=firefox_options)

        # Navigate to the URL
        driver.get(url)

        # Wait for elements to load (adjust as needed)
        wait = WebDriverWait(driver, 300)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".item")))

        # Extract product information using appropriate selectors
        product_info_elements = driver.find_elements(By.CSS_SELECTOR, ".item")  # Limit to the first product

        # Extracted product data
        product_data = []
        urlDomain = urlparse(url).netloc

        for element in product_info_elements:
            product = filter_and_parse_element_klikindomart(urlDomain, element)

            if product:
                # Get the href link
                href_element = element.find_element(By.CSS_SELECTOR, "a[href]")
                href = href_element.get_attribute("href")
                logging.info(f"href: {href}")
                # Open the href link
                driver.execute_script("window.open();")
                driver.switch_to.window(driver.window_handles[1])
                driver.get(href)

                # Wait for the description element to load (adjust as needed)
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#desc-product")))

                # Extract product description using appropriate selector
                description_element = driver.find_element(By.CSS_SELECTOR, "#desc-product")
                description = description_element.text.strip()

                product["description"] = description
                product_data.append(product)

                # Close the newly opened tab
                driver.close()
                driver.switch_to.window(driver.window_handles[0])

        driver.quit()

        return product_data

    except Exception as e:
        logging.error(f"An unexpected error occurred for URL: {url}. Error: {e}")
        raise e

def scrape_product_info_blibli(url):
    try:
        logging.info(f"Attempting to fetch HTML content from: {url}")

        # Set up Firefox options
        firefox_options = webdriver.FirefoxOptions()
        firefox_options.add_argument("--headless")  # Run in headless mode (no GUI)

        # Set up the Firefox driver
        executable_path = "./.venv/Scripts/geckodriver.exe"
        # driver = webdriver.Firefox(executable_path=executable_path, options=firefox_options)
        firefox_service_obj = Service(executable_path)
        driver = webdriver.Firefox(service=firefox_service_obj, options=firefox_options)

        # Navigate to the URL
        driver.get(url)

        # Wait for elements to load (adjust as needed)
        wait = WebDriverWait(driver, 300)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".product__container")))

        # Extract product information using appropriate selectors
        product_info_elements = driver.find_elements(By.CSS_SELECTOR, ".product__container")  # Limit to the first product

        # Extracted product data
        product_data = []
        urlDomain = urlparse(url).netloc
        logging.info(f"urlDomain : {urlDomain}")

        for element in product_info_elements:
            product = filter_and_parse_element_klikindomart(urlDomain, element)

            if product:
                # Get the href link
                href_element = element.find_element(By.CSS_SELECTOR, "a[href]")
                href = href_element.get_attribute("href")
                logging.info(f"href: {href}")
                # Open the href link
                driver.execute_script("window.open();")
                driver.switch_to.window(driver.window_handles[1])
                driver.get(href)

                # Wait for the description element to load (adjust as needed)
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#desc-product")))

                # Extract product description using appropriate selector
                description_element = driver.find_element(By.CSS_SELECTOR, "#desc-product")
                description = description_element.text.strip()

                product["description"] = description
                product_data.append(product)
                break

        driver.quit()

        return product_data

    except Exception as e:
        logging.error(f"An unexpected error occurred for URL: {url}. Error: {e}")
        raise e
    
def filter_and_parse_element_klikindomart(url, element):
    product_data = {}
    result = {}
    selectors_klikindomart = (".title", ".disc-price", ".discount", ".price-value")
    
    result = find_elements_by_css(element, selectors_klikindomart)

    if result:
        product_name = result["product_name"]
        price = result["price"]
        original_price = result["original_price"]
        discount = result["discount"]

        description = ""

        if original_price and discount:
            original_price = original_price.replace(discount, "").replace("\n", "")

        price = float(price.replace("Rp", "").replace(".", "").strip()) if price else None
        original_price = float(original_price.replace("Rp", "").replace(".", "").strip()) if original_price else None
        discount = float(discount.replace("%", "").strip()) if discount else None

        product_data = {
            "name": product_name,
            "original_price": original_price,
            "price": price,
            "discount_percentage": discount,
            "detail": description,
            "platform": url,
            "create_date": datetime.now()
        }
    
    return product_data
    
def filter_and_parse_element_blibli(url, element):
    product_data = {}
    result = {}
    selectors_blibli = (".blu-product__name", ".blu-product__price-before", ".blu-product__price-discount", ".blu-product__price-after")

    try:
        result = find_elements_by_css(element, selectors_blibli)
    except:
        result = None

    if result:
        product_name = result["product_name"]
        price = result["price"]
        original_price = result["original_price"]
        discount = result["discount"]

        description = ""

        if original_price and discount:
            original_price = original_price.replace(discount, "").replace("\n", "")

        price = float(price.replace("Rp", "").replace(".", "").strip()) if price else None
        original_price = float(original_price.replace("Rp", "").replace(".", "").strip()) if original_price else None
        discount = float(discount.replace("%", "").strip()) if discount else None

        product_data = {
            "name": product_name,
            "original_price": original_price,
            "price": price,
            "discount_percentage": discount,
            "detail": description,
            "platform": url,
            "create_date": datetime.now()
        }
    
    return product_data
    
def find_elements_by_css(element, selectors):
    el_dict = {}
    product_name_selector, original_price_selector, discount_selector, price_selector = selectors

    try:
        product_name = element.find_element(By.CSS_SELECTOR, product_name_selector).text.strip()
    except:
        product_name = None
    try:
        original_price = element.find_element(By.CSS_SELECTOR, original_price_selector).text.strip()
    except:
        original_price = None
    try:
        discount = element.find_element(By.CSS_SELECTOR, discount_selector).text.strip()
    except:
        discount = None
    try:
        price = element.find_element(By.CSS_SELECTOR, price_selector).text.strip()
    except:
        price = None
    try:
        urlDesc = element.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
    except:
        urlDesc = None

    if product_name and price:
        el_dict = {
            "product_name": product_name,
            "original_price": original_price,
            "discount": discount,
            "price": price,
            "urlDesc": urlDesc
        }

    return el_dict

# if __name__ == "__main__":
#     crawl_and_save_data()
