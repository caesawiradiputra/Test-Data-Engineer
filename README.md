# Running the Application on Windows
## Prerequisites
* Install [Python](https://www.python.org/downloads/) on your system.
* Install [Git](https://git-scm.com/downloads) on your system.
* Install PostgreSQL on your system.

## Clone the Repository
```
git clone https://github.com/caesawiradiputra/Test-Data-Engineer.git
cd your-repository
```

## Set Up Virtual Environment
>**Navigate to the project root directory**
>
```
cd "Test-Data-Engineer"
```
>
>**Create a virtual environment**
```
python -m venv .venv
```
>**Activate the virtual environment**
```
.venv\Scripts\activate
```

## Install Dependencies
> **Install Python dependencies**
```
pip install -r requirements.txt
```

## Download and Set Up Geckodriver
Download the appropriate geckodriver for your system and save it as geckodriver.exe.

Move the geckodriver.exe to the .venv\Scripts directory.

## Run the Application
> **Run the application**
```
python -m main
```

## Access the Application
Open a web browser and go to **http://localhost:5000** to access your application.

## Test the API
Open Postman and navigate to http://localhost:5000/{path_api} to test the application.

## Stopping the Application
To stop the application, press Ctrl + C in the terminal where the application is running.

## Deactivate Virtual Environment
> **Deactivate the virtual environment**
```
deactivate
```

# Running the Application with Docker
## Prerequisites
* Install [Docker](https://www.docker.com/get-started) on your system.

## Build Docker Image
```
docker-compose up --build
```

## Access the Application
Open a web browser and go to **http://localhost:5000** to access your application.

## Test the API
Open Postman and navigate to http://localhost:5000/{path_api} to test the application.

# API Documentation
## Get Product Data
* Endpoint: /api/get_product_data
* Method: GET
* Description: Retrieve a list of product data.
* Response:
```
{
  "products": [
    {
      "product_id": 1,
      "name": "Product Name 1",
      "price": 20.5,
      "category": "Category 1"
    },
    // ... (more products)
  ]
}
```

## Get Price Recommendation
* Endpoint: /api/get_price_recommendation
* Method: GET
* Description: Retrieve a list of price recommendations.
* Response:
```
{
  "products": [
    {
      "discount": "11%",
      "name": "Molto Pelembut & Pewangi Pakaian Himalayan Honeysuckle 650mL",
      "original_price": "23000.0",
      "price": "20470.0",
      "product_master_id": 615
    },
    // ... (more products)
  ]
}
```

## Populate Data (All Sites)
* Endpoint: /api/process/populate_data/all
* Method: GET
* Description: Populate data from all three sources (KlikUndomaret, Blibli, Tokopedia).
* Response:
```
{
  "response": "success"
}
```

## Populate Data (KlikIndomaret)
* Endpoint: /api/process/populate_data/1
  * Detail Endpoint: /api/process/populate_data/1/detail (Includes opening each product link to retrieve description and category)
* Method: GET
* Description: Populate data from KlikIndomaret.
* Response:
```
{
  "response": "success"
}
```

## Populate Data (Blibli)
* Endpoint: /api/process/populate_data/2
  * Detail Endpoint: /api/process/populate_data/2/detail (Includes opening each product link to retrieve description and category)
* Method: GET
* Description: Populate data from Blibli.
* Response:
```
{
  "response": "success"
}
```

## Populate Data (Tokopedia)
* Endpoint: /api/process/populate_data/3
  * Detail Endpoint: /api/process/populate_data/3/detail (Includes opening each product link to retrieve description and category)
* Method: GET
* Description: Populate data from Tokopedia.
* Response:
```
{
  "response": "success"
}
```

## Repopulate Data (All Sites)
* Endpoint: /api/process/repopulate_data/all
* Method: GET
* Description: Clean and repopulate data from all three sources (KlikUndomaret, Blibli, Tokopedia).
* Response:
```
{
  "response": "success"
}
```

## Repopulate Data (KlikIndomaret)
* Endpoint: /api/process/repopulate_data/1
  * Detail Endpoint: /api/process/repopulate_data/1/detail (Includes opening each product link to retrieve description and category)
* Method: GET
* Description: Clean and repopulate data from KlikIndomaret.
* Response:
```
{
  "response": "success"
}
```

## Repopulate Data (Blibli)
* Endpoint: /api/process/repopulate_data/2
  * Detail Endpoint: /api/process/repopulate_data/2/detail (Includes opening each product link to retrieve description and category)
* Method: GET
* Description: Clean and repopulate data from Blibli.
* Response:
```
{
  "response": "success"
}
```

## Repopulate Data (Tokopedia)
* Endpoint: /api/process/repopulate_data/3
  * Detail Endpoint: /api/process/repopulate_data/3/detail (Includes opening each product link to retrieve description and category)
* Method: GET
* Description: Clean and repopulate data from Tokopedia.
* Response:
```
{
  "response": "success"
}
```

## Clean Data
* Endpoint: /api/process/clean_data
* Method: GET
* Description: Clean existing data.
* Response:
```
{
  "response": "success"
}
```

## Calculate New Discount
* Endpoint: /api/process/calculate_new_discount
* Method: GET
* Description: Calculate new discount using a dummy model.
* Response:
  * Redirects to /api/get_price_recommendation

## Calculate New Price (Based on History)
* Endpoint: /api/process/calculate_new_price/1
* Method: GET
* Description: Calculate new price based on historical data.
* Response:
  * Redirects to /api/get_price_recommendation

## Calculate New Price (Based on Weight)
* Endpoint: /api/process/calculate_new_price/2
* Method: GET
* Description: Calculate new price based on Weight data.
* Response:
  * Redirects to /api/get_price_recommendation

## Crawl Web Data (KlikIndomaret)
* Endpoint: /api/test/crawl_web/1
* Method: GET
* Description: Crawl web data from KlikIndomaret.
* Response:
```
{
  "product_data": [
    {
      "category": "klikindomaret",
      "create_date": "Fri, 15 Dec 2023 19:20:09 GMT",
      "detail": "",
      "discount_percentage": null,
      "name": "Molto Pelembut & Pewangi Pakaian Himalayan Honeysuckle 650mL",
      "original_price": null,
      "platform": "www.klikindomaret.com",
      "price": 23000.0
    },
    // ... (more products)
  ]
}
```

## Crawl Web Data (Blibli)
* Endpoint: /api/test/crawl_web/2
* Method: GET
* Description: Crawl web data from Blibli.
* Response:
```
{
  "product_data": [
    {
      "category": "blibli",
      "create_date": "Fri, 15 Dec 2023 19:20:09 GMT",
      "detail": "",
      "discount_percentage": null,
      "name": "Molto Pelembut & Pewangi Pakaian Himalayan Honeysuckle 650mL",
      "original_price": null,
      "platform": "www.klikindomaret.com",
      "price": 23000.0
    },
    // ... (more products)
  ]
}
```

## Crawl Web Data (Tokopedia)
* Endpoint: /api/test/crawl_web/3
* Method: GET
* Description: Crawl web data from Tokopedia.
* Response:
```
{
  "product_data": [
    {
      "category": "tokopedia",
      "create_date": "Fri, 15 Dec 2023 19:20:09 GMT",
      "detail": "",
      "discount_percentage": null,
      "name": "Molto Pelembut & Pewangi Pakaian Himalayan Honeysuckle 650mL",
      "original_price": null,
      "platform": "www.klikindomaret.com",
      "price": 23000.0
    },
    // ... (more products)
  ]
}
```

## List Element Hierarchy (KlikIndomaret)
* Endpoint: /api/test/list_element/1
* Method: GET
* Description: List the hierarchy of HTML elements from KlikIndomaret.
* Response:
```
{
  "elements": [
    ".price-value": "[document] > html > body.['isPromo'] > div.['new-nav'] #site-content > div.['wrp-container-promosi', 'officialStore-template', 'filterPromoPage'] > div.['produk', 'produk-level'] > div.['container', 'nopadding'] > div.['floatL', 'rightside'] #productOfficial > div.['tab-content', 'content-menu-tab', 'clearfix'] > div.['tab-pane', 'active'] #productPromo > div.['wrp-produk-list', 'bg-white'] > div.['clearfix'] > div.['product-collection', 'list-product', 'clearfix'] > div.['item'] #pageFilterProduct-2ad8dea9-3222-4917-bcc1-e62d91660228 > a > div.['each-item'] > div.['wrp-content'] > div.['wrp-price'] > div.['vmiddle'] > div.['price'] > span.['normal', 'price-value']"
  ]
}
```

## List Element Hierarchy (Blibli)
* Endpoint: /api/test/list_element/2
* Method: GET
* Description: List the hierarchy of HTML elements from Blibli.
* Response:
```
{
  "elements": [
    ".blu-product__price-after": "[document] > html > body > div #app > div > div.['collabs-wrapper', 'full-width'] #main-ui-wrapper > span > div > div > div.['container', 'container__desktop'] > div.['content-wrapper', 'content-wrapper-overflow'] #blibli-main-ctrl > section.['content-section'] > div.['row'] #catalogProductListDiv > div.['product-listing'] #productListingAgeRestrictedFilter > div.['large-16', 'medium-16', 'small-16'] > div.['product-listing__right-section', 'large-13', 'medium-13', 'small-16', 'column', 'large-13__full-width', 'medium-13__full-width'] #catalogProductListContentDiv > div #productContentDiv > div > div.['product', 'columns', 'product__container__side'] > div.['product__card', 'product__card__five'] > div.['product__container'] > a > div.['blu-product', 'product__card'] > div.['blu-product__btm'] > div.['blu-product__info'] > div.['blu-product__price'] > div.['blu-product__price-after']"
  ]
}
```

## List Element Hierarchy (Tokopedia)
* Endpoint: /api/test/list_element/3
* Method: GET
* Description: List the hierarchy of HTML elements from Tokopedia.
* Response:
```
{
  "elements": [
    ".prd_link-product-price": "[document] > html > body > div #zeus-root > div.['css-8atqhb'] > div > div.['css-1s3ezns'] > div.['css-1kn5b1o'] > div.['css-1v9ovqz'] > div.['css-8atqhb'] > div.['css-tjjb18'] > div.['css-1sn1xa2'] > div.['css-54k5sq'] > div.['css-uwyh54'] > div.['css-qa82pd'] > div.['prd_container-card', 'css-126fhq2'] > div.['pcv3__container', 'css-1izdl9e'] > div.['css-1asz3by'] > a.['pcv3__info-content', 'css-gwkf0u'] > div > div > div.['prd_link-product-price', 'css-h66vau']"
  ]
}
```

## Show Log
* Endpoint: /api/log
* Method: GET
* Description: Show the contents of the log file.
* Response:
 * Renders the log content.

## Clean Log
* Endpoint: /api/log/clean_log
* Method: GET
* Description: Clean the log file and redirect to /api/log.
* Response
  * Redirects to /api/log
 
## Error Handling
* 200 Success:
```
{
    "response": "success"
}
```
* 404 Not Found:
```
{
  "error": "Not Found"
}
```
* 500 Internal Server Error:
```
{
  "error": "Internal Server Error"
}
```
