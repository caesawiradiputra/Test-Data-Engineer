# src/machine_learning/dummy_model.py
import psycopg2
import random
from datetime import datetime
import logging

from ..config import CONNECTION_STRING

def calculate_new_discount():
    try:
        # Connect to the database
        conn = psycopg2.connect(CONNECTION_STRING)
        cursor = conn.cursor()

        # Placeholder: Implement data cleaning and preprocessing logic
        cursor.execute("TRUNCATE TABLE price_recommendation;")
        # For example, you can calculate discounted prices, handle missing values, etc.

        # Placeholder: Sample query to retrieve data for processing
        cursor.execute("SELECT id, name, price, COALESCE(original_price, price) original_price, platform, product_master_id FROM product;")
        products = cursor.fetchall()

        # Placeholder: Perform data processing operations
        for product in products:
            if random.choice([True, False]):
                recommendation_percentage = round(random.uniform(0.02, 0.2) * 100)                
                recommended_price = round(float(product[2]) * float(1-recommendation_percentage/100), 0)  
                
            else:
                recommended_price = None

            if recommended_price:
                cursor.execute(
                    "INSERT INTO price_recommendation (product_master_id, price, discount, original_price, date) VALUES (%s, %s, %s, %s, %s);",
                    (product[5], recommended_price, recommendation_percentage, product[3], datetime.now())  
                )

        # # Update the processed data in the database if needed
        # cursor.execute(
        #     '''
        #     update product_2 p2
        #     set original_price = coalesce(p.original_price, p.price), 
        #         discount_percentage = pr.discount,
        #         price = coalesce(p.original_price, p.price)
        #     FROM product_2 p
        #     LEFT JOIN price_recommendation pr ON pr.product_master_id = p.product_master_id
        #     where p.id = p2.id;
        #     '''
        # )

        # Commit changes and close the connection
        conn.commit()

    except psycopg2.Error as e:
        # Log the error
        logging.error(f"Error in data processing: {e}")

    finally:
        # Close the cursor and connection in the finally block to ensure it happens even if an exception occurs
        if cursor:
            cursor.close()
        if conn:
            conn.close()            

# if __name__ == "__main__":
#     generate_price_recommendations()
