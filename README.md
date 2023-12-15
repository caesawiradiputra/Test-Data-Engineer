# Known Issues
* Blibli and Tokopedia websites appear to have protections against robots or crawlers, possibly allowing only one crawl per public IP.
  * For development purposes, the HTML content from each website is copied to an HTML file in the /test folder.

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

# API Documentation
## Get Product Data
* URL: /api/get_product_data
* Method: GET
* Description: Retrieve a list of product data.

## Get Price Recommendation
* URL: /api/get_price_recommendation
* Method: GET
* Description: Retrieve a list of price recommendations.

## Get Price Recommendation
* URL: /api/get_price_recommendation
* Method: GET
* Description: Retrieve a list of price recommendations.

## Populate Data (All Sites)
* URL: /api/process/populate_data/all
* Method: GET
* Description: Populate data from all three sources (KlikUndomaret, Blibli, Tokopedia).

## Populate Data (KlikIndomaret)
* URL: /api/process/populate_data/1
* Method: GET
* Description: Populate data from KlikIndomaret.

## Populate Data (Blibli)
* URL: /api/process/populate_data/2
* Method: GET
* Description: Populate data from Blibli.

## Populate Data (Tokopedia)
* URL: /api/process/populate_data/3
* Method: GET
* Description: Populate data from Tokopedia.

## Repopulate Data (All Sites)
* URL: /api/process/populate_data/all
* Method: GET
* Description: Clean and repopulate data from all three sources (KlikUndomaret, Blibli, Tokopedia).

## Repopulate Data (KlikIndomaret)
* URL: /api/process/populate_data/1
* Method: GET
* Description: Clean and repopulate data from KlikIndomaret.

## Repopulate Data (Blibli)
* URL: /api/process/populate_data/2
* Method: GET
* Description: Clean and repopulate data from Blibli.

## Repopulate Data (Tokopedia)
* URL: /api/process/populate_data/3
* Method: GET
* Description: Clean and repopulate data from Tokopedia.

## Clean Data
* URL: /api/process/clean_data
* Method: GET
* Description: Clean existing data.

## Calculate New Discount
* URL: /api/process/calculate_new_discount
* Method: GET
* Description: Calculate new discount using a dummy model.
* Response:
  * Redirects to /api/get_price_recommendation

## Calculate New Price (Based on History)
* URL: /api/process/calculate_new_price/1
* Method: GET
* Description: Calculate new price based on historical data.
* Response:
  * Redirects to /api/get_price_recommendation

## Calculate New Price (Based on Weight)
* URL: /api/process/calculate_new_price/2
* Method: GET
* Description: Calculate new price based on Weight data.
* Response:
  * Redirects to /api/get_price_recommendation

## Crawl Web Data (KlikIndomaret)
* URL: /api/test/crawl_web/1
* Method: GET
* Description: Crawl web data from KlikIndomaret.

## Crawl Web Data (Blibli)
* URL: /api/test/crawl_web/2
* Method: GET
* Description: Crawl web data from Blibli.

## Crawl Web Data (Tokopedia)
* URL: /api/test/crawl_web/3
* Method: GET
* Description: Crawl web data from Tokopedia.

## List Element Hierarchy (KlikIndomaret)
* URL: /api/test/list_element/1
* Method: GET
* Description: List the hierarchy of HTML elements from KlikIndomaret.

## List Element Hierarchy (Blibli)
* URL: /api/test/list_element/2
* Method: GET
* Description: List the hierarchy of HTML elements from KlikIndomaret.

## List Element Hierarchy (Tokopedia)
* URL: /api/test/list_element/3
* Method: GET
* Description: List the hierarchy of HTML elements from KlikIndomaret.

## Show Log
* URL: /api/log
* Method: GET
* Description: Show the contents of the log file.

## Clean Log
* URL: /api/log/clean_log
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
