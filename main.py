from dotenv import load_dotenv
import os

from src.api.app import app
import logging

if __name__ == "__main__":
    ENVIRONMENT = os.environ.get("ENVIRONMENT", "dev")
    load_dotenv(f".env.{ENVIRONMENT}", override=True)

    DEBUG = os.getenv("DEBUG", True).lower() == "true"
    print(f"ENVIRONMENT: {ENVIRONMENT}")
    print(f"DEBUG: {DEBUG}")
    if DEBUG:
        logging.basicConfig(filename='log/app.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)7s - [%(filename)20s:%(lineno)5s - %(funcName)20s() ] - %(message)s')
    else:
        logging.basicConfig(filename='log/app.log', level=logging.INFO, format='%(asctime)s - %(levelname)7s - [%(filename)20s:%(lineno)5s - %(funcName)20s() ] - %(message)s')

    app.run(host=os.getenv("HOST", "0.0.0.0"), port=os.getenv("PORT", 5000), debug=DEBUG)