# src/api/app.py
from flask import Flask, jsonify, make_response, render_template, redirect, url_for
import logging, os

from ..config import SELECTORS
from ..crawler import crawl
from ..data_processing import data_processing
from ..machine_learning import dummy_model

# app = Flask(__name__)
app = Flask(__name__, template_folder=os.path.abspath(os.path.dirname(__file__)))

@app.route('/')
def home():
    return jsonify({"message": "Hello, welcome to the API!"})

@app.route("/api/get_product_data", methods=["GET"])
def get_product_data():
    return jsonify({"products": data_processing.list_product_data()})

@app.route("/api/get_price_recommendation", methods=["GET"])
def get_price_recommendation():
    return jsonify({"products": data_processing.list_price_recomendation()})
    
@app.route("/api/process/populate_data/all", methods=["GET"])
def get_populate_data_all():   
    try:
        crawl.populate_data_all()

        return make_response(jsonify({"response": "success"}), 200)
    
    except Exception as e:
        logging.exception(f"An unexpected error occurred while processing data: {e}")
        return make_response(jsonify(e), 500)
    
@app.route("/api/process/populate_data/1", methods=["GET"])
def get_populate_data_1():   
    try:
        selectors = SELECTORS["klikindomaret_selector"]
        product_data = crawl.scrape_product_info(selectors)
        # product_data = crawl.get_product_description(product_data, selectors)
        data_processing.parse_and_save_data(product_data) 

        return make_response(jsonify({"response": "success"}), 200)
    
    except Exception as e:
        logging.exception(f"An unexpected error occurred while processing data: {e}")
        return make_response(jsonify(e), 500)
    
@app.route("/api/process/populate_data/1/detail", methods=["GET"])
def get_populate_data_1_detail():   
    try:
        selectors = SELECTORS["klikindomaret_selector"]
        product_data = crawl.scrape_product_info(selectors)
        product_data = crawl.get_product_description(product_data, selectors)
        data_processing.parse_and_save_data(product_data) 

        return make_response(jsonify({"response": "success"}), 200)
    
    except Exception as e:
        logging.exception(f"An unexpected error occurred while processing data: {e}")
        return make_response(jsonify(e), 500)
    
@app.route("/api/process/populate_data/2", methods=["GET"])
def get_populate_data_2():   
    try:
        selectors = SELECTORS["blibli_selector"]
        product_data = crawl.scrape_product_info(selectors)
        # product_data = crawl.get_product_description(product_data, selectors)
        data_processing.parse_and_save_data(product_data) 

        return make_response(jsonify({"response": "success"}), 200)
    
    except Exception as e:
        logging.exception(f"An unexpected error occurred while processing data: {e}")
        return make_response(jsonify(e), 500)
    
@app.route("/api/process/populate_data/2/detail", methods=["GET"])
def get_populate_data_2_detail():   
    try:
        selectors = SELECTORS["blibli_selector"]
        product_data = crawl.scrape_product_info(selectors)
        product_data = crawl.get_product_description(product_data, selectors)
        data_processing.parse_and_save_data(product_data) 

        return make_response(jsonify({"response": "success"}), 200)
    
    except Exception as e:
        logging.exception(f"An unexpected error occurred while processing data: {e}")
        return make_response(jsonify(e), 500)
    
@app.route("/api/process/populate_data/3", methods=["GET"])
def get_populate_data_3():   
    try:
        selectors = SELECTORS["tokopedia_selector"]
        product_data = crawl.scrape_product_info(selectors)
        # product_data = crawl.get_product_description(product_data, selectors)
        data_processing.parse_and_save_data(product_data) 

        return make_response(jsonify({"response": "success"}), 200)
    
    except Exception as e:
        logging.exception(f"An unexpected error occurred while processing data: {e}")
        return make_response(jsonify(e), 500)
    
@app.route("/api/process/populate_data/3/detail", methods=["GET"])
def get_populate_data_3_detail():   
    try:
        selectors = SELECTORS["tokopedia_selector"]
        product_data = crawl.scrape_product_info(selectors)
        product_data = crawl.get_product_description(product_data, selectors)
        data_processing.parse_and_save_data(product_data) 

        return make_response(jsonify({"response": "success"}), 200)
    
    except Exception as e:
        logging.exception(f"An unexpected error occurred while processing data: {e}")
        return make_response(jsonify(e), 500)
    
@app.route("/api/process/repopulate_data/all/{}", methods=["GET"])
def get_repopulate_all_data():   
    try:
        crawl.repopulate_all_data()

        return make_response(jsonify({"response": "success"}), 200)
    
    except Exception as e:
        logging.exception(f"An unexpected error occurred while processing data: {e}")
        return make_response(jsonify(e), 500)
    
@app.route("/api/process/repopulate_data/1", methods=["GET"])
def get_repopulate_data_1():   
    try:
        data_processing.clean_data()
        selectors = SELECTORS["klikindomaret_selector"]
        product_data = crawl.scrape_product_info(selectors)
        # product_data = crawl.get_product_description(product_data, selectors)
        data_processing.parse_and_save_data(product_data) 

        return make_response(jsonify({"response": "success"}), 200)
    
    except Exception as e:
        logging.exception(f"An unexpected error occurred while processing data: {e}")
        return make_response(jsonify(e), 500)
    
@app.route("/api/process/repopulate_data/1/detail", methods=["GET"])
def get_repopulate_data_1_detail():   
    try:
        data_processing.clean_data()
        selectors = SELECTORS["klikindomaret_selector"]
        product_data = crawl.scrape_product_info(selectors)
        product_data = crawl.get_product_description(product_data, selectors)
        data_processing.parse_and_save_data(product_data) 

        return make_response(jsonify({"response": "success"}), 200)
    
    except Exception as e:
        logging.exception(f"An unexpected error occurred while processing data: {e}")
        return make_response(jsonify(e), 500)
    
@app.route("/api/process/repopulate_data/2", methods=["GET"])
def get_repopulate_data_2():   
    try:
        data_processing.clean_data()
        selectors = SELECTORS["blibli_selector"]
        product_data = crawl.scrape_product_info(selectors)
        # product_data = crawl.get_product_description(product_data, selectors)
        data_processing.parse_and_save_data(product_data) 

        return make_response(jsonify({"response": "success"}), 200)
    
    except Exception as e:
        logging.exception(f"An unexpected error occurred while processing data: {e}")
        return make_response(jsonify(e), 500)
    
@app.route("/api/process/repopulate_data/2/detail", methods=["GET"])
def get_repopulate_data_2_detail():   
    try:
        data_processing.clean_data()
        selectors = SELECTORS["blibli_selector"]
        product_data = crawl.scrape_product_info(selectors)
        product_data = crawl.get_product_description(product_data, selectors)
        data_processing.parse_and_save_data(product_data) 

        return make_response(jsonify({"response": "success"}), 200)
    
    except Exception as e:
        logging.exception(f"An unexpected error occurred while processing data: {e}")
        return make_response(jsonify(e), 500)
    
@app.route("/api/process/repopulate_data/3", methods=["GET"])
def get_repopulate_data_3():   
    try:
        data_processing.clean_data()
        selectors = SELECTORS["tokopedia_selector"]
        product_data = crawl.scrape_product_info(selectors)
        # product_data = crawl.get_product_description(product_data, selectors)
        data_processing.parse_and_save_data(product_data) 

        return make_response(jsonify({"response": "success"}), 200)
    
    except Exception as e:
        logging.exception(f"An unexpected error occurred while processing data: {e}")
        return make_response(jsonify(e), 500)
    
@app.route("/api/process/repopulate_data/3/detail", methods=["GET"])
def get_repopulate_data_3_detail():   
    try:
        data_processing.clean_data()
        selectors = SELECTORS["tokopedia_selector"]
        product_data = crawl.scrape_product_info(selectors)
        product_data = crawl.get_product_description(product_data, selectors)
        data_processing.parse_and_save_data(product_data) 

        return make_response(jsonify({"response": "success"}), 200)
    
    except Exception as e:
        logging.exception(f"An unexpected error occurred while processing data: {e}")
        return make_response(jsonify(e), 500)
    
@app.route("/api/process/clean_data", methods=["GET"])
def get_clean_data():   
    try:
        data_processing.clean_data()

        return make_response(jsonify({"response": "success"}), 200)
    
    except Exception as e:
        logging.exception(f"An unexpected error occurred while processing data: {e}")
        return make_response(jsonify(e), 500)
    
@app.route("/api/process/calculate_new_discount", methods=["GET"])
def get_calculate_new_discount():   
    try:
        dummy_model.calculate_new_discount()

        return redirect(url_for('get_price_recommendation'))
    
    except Exception as e:
        logging.exception(f"An unexpected error occurred while processing data: {e}")
        return make_response(jsonify(e), 500)
    
@app.route("/api/process/calculate_new_price/1", methods=["GET"])
def get_calculate_new_price_1():   
    try:
        dummy_model.calculate_new_price_history()

        return redirect(url_for('get_price_recommendation'))
    
    except Exception as e:
        logging.exception(f"An unexpected error occurred while processing data: {e}")
        return make_response(jsonify(e), 500)
    
@app.route("/api/process/calculate_new_price/2", methods=["GET"])
def get_calculate_new_price_2():   
    try:
        dummy_model.calculate_new_price_history2()

        return redirect(url_for('get_price_recommendation'))
    
    except Exception as e:
        logging.exception(f"An unexpected error occurred while processing data: {e}")
        return make_response(jsonify(e), 500)
    
@app.route("/api/test/crawl_web/1", methods=["GET"])
def get_crawl_web_1():       
    try:
        selectors = SELECTORS["klikindomaret_selector"]
        product_data = crawl.scrape_product_info(selectors)
        return make_response(jsonify({"product_data": product_data}), 200)
        # data_processing.parse_and_save_data(product_data)
        # return make_response(jsonify({"response": "success"}), 200)
    
    except Exception as e:
        logging.exception(f"An unexpected error occurred while crawling web : {url}, error: {e}")
        return make_response(jsonify(e), 500)
    
@app.route("/api/test/crawl_web/2", methods=["GET"])
def get_crawl_web_2():       
    try:
        selectors = SELECTORS["blibli_selector"]
        product_data = crawl.scrape_product_info(selectors)
        return make_response(jsonify({"product_data": product_data}), 200)
        # data_processing.parse_and_save_data(product_data)
        # return make_response(jsonify({"response": "success"}), 200)
    
    except Exception as e:
        logging.exception(f"An unexpected error occurred while crawling web : {url}, error: {e}")
        return make_response(jsonify(e), 500)
    
@app.route("/api/test/crawl_web/3", methods=["GET"])
def get_crawl_web_3():       
    try:        
        selectors = SELECTORS["tokopedia_selector"]
        product_data = crawl.scrape_product_info(selectors)
        return make_response(jsonify({"product_data": product_data}), 200)
        # data_processing.parse_and_save_data(product_data)
        # return make_response(jsonify({"response": "success"}), 200)
    
    except Exception as e:
        logging.exception(f"An unexpected error occurred while crawling web : {url}, error: {e}")
        return make_response(jsonify(e), 500)
    
@app.route("/api/test/list_element/1", methods=["GET"])
def list_element_1():       
    try:
        selectors = SELECTORS["klikindomaret_selector"]

        elements = crawl.list_element_hierarchy(selectors)
        return make_response(jsonify({"elements": elements}), 200)
    
    except Exception as e:
        logging.exception(f"An unexpected error occurred while list_element data: {e}")
        return make_response(jsonify(e), 500)
    
@app.route("/api/test/list_element/2", methods=["GET"])
def list_element_2():       
    try:
        selectors = SELECTORS["blibli_selector"]

        elements = crawl.list_element_hierarchy(selectors)
        return make_response(jsonify({"elements": elements}), 200)
    
    except Exception as e:
        logging.exception(f"An unexpected error occurred while list_element data: {e}")
        return make_response(jsonify(e), 500)
    
@app.route("/api/test/list_element/3", methods=["GET"])
def list_element_3():       
    try:
        selectors = SELECTORS["tokopedia_selector"]

        elements = crawl.list_element_hierarchy(selectors)
        return make_response(jsonify({"elements": elements}), 200)
    
    except Exception as e:
        logging.exception(f"An unexpected error occurred while list_element data: {e}")
        return make_response(jsonify(e), 500)
    
@app.route('/api/log')
def show_log():
    try:
        with open('log/app.log', 'r') as log_file:
            log_content = log_file.read()
    except Exception as e:
        log_content = f"Error reading log file: {str(e)}"

    return render_template('./log_template.html', log_content=log_content)

@app.route('/api/log/clean_log', methods=['GET'])
def clean_log_and_redirect():
    log_path = 'log/app.log'
    
    # Clear the log file content
    try:
        with open(log_path, 'w'):
            pass
    except FileNotFoundError:
        return jsonify({'error': 'Log file not found'}), 404

    # Redirect to another endpoint (change 'api/log' to your desired endpoint)
    return redirect(url_for('show_log'))

# Error handler for 404 Not Found
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({"error": "Not Found"}), 404)

# Error handler for 500 Internal Server Error
@app.errorhandler(500)
def internal_server_error(error):
    return make_response(jsonify({"error": "Internal Server Error"}), 500)

# if __name__ == "__main__":
#     app.run(debug=True)
