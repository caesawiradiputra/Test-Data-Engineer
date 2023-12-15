# src/machine_learning/dummy_model.py
import psycopg2
from psycopg2.extras import execute_values
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

def calculate_new_price_history():
    try:
        # Connect to the database
        conn = psycopg2.connect(CONNECTION_STRING)
        cursor = conn.cursor()

        # Placeholder: Implement data cleaning and preprocessing logic
        cursor.execute("TRUNCATE TABLE price_recommendation;")

        # Placeholder: Sample query to retrieve data for processing
        cursor.execute("SELECT id, name FROM product_master;")
        product_masters = cursor.fetchall()

        # Placeholder: Perform data processing operations
        for product_master in product_masters:
            cursor.execute(
                "SELECT COUNT(1) count_history, "
                "SUM(price) sum_price, "
                "MAX(COALESCE(original_price, price)) original_price, "
                "SUM(discount) sum_discount "
                "FROM product_master "
                "WHERE product_master_id = %s;",
                (product_master[0],)
            )
            avg_products = cursor.fetchone()

            if avg_products[0] > 1:
                avg_price = avg_products[1] / avg_products[0]
                avg_discount = avg_products[3] / avg_products[0]
                max_original_price = avg_products[2]

                if avg_price > max_original_price and avg_discount > 0:
                    new_discount = avg_discount
                else:
                    new_discount = round(random.uniform(0.02, 0.2) * 100)

                recommended_price = round(max_original_price * (1 - new_discount / 100), 0)

                # Use execute_values to insert multiple rows in a single query
                execute_values(
                    cursor,
                    "INSERT INTO price_recommendation (product_master_id, price, discount, original_price, date) VALUES %s;",
                    [(product_master[0], recommended_price, new_discount, product_master[3], datetime.now())],
                )

        # Commit changes
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

def calculate_new_price_history2():
    try:
        # Connect to the database
        conn = psycopg2.connect(CONNECTION_STRING)
        cursor = conn.cursor()

        # Placeholder: Implement data cleaning and preprocessing logic
        cursor.execute("TRUNCATE TABLE price_recommendation;")

        # Placeholder: Sample query to retrieve data for processing
        cursor.execute("SELECT id, name FROM product_master;")
        product_masters = cursor.fetchall()

        # Placeholder: Perform data processing operations
        for product_master in product_masters:
            weighted_sum_price = 0
            weighted_sum_discount = 0
            total_weight = 0

            cursor.execute(
                "SELECT price, discount, date FROM product_master "
                "WHERE product_master_id = %s ORDER BY date DESC LIMIT 5;",  # Adjust the limit as needed
                (product_master[0],)
            )
            recent_records = cursor.fetchall()

            for idx, record in enumerate(recent_records):
                weight = 1 / (idx + 1)  # Weight based on recency
                total_weight += weight
                weighted_sum_price += weight * record[0]
                weighted_sum_discount += weight * record[1]

            # Calculate weighted averages
            if total_weight > 0:
                weighted_avg_price = weighted_sum_price / total_weight
                weighted_avg_discount = weighted_sum_discount / total_weight

            # Adjust the new price based on the weighted average and apply a discount threshold
            recommended_price = round(weighted_avg_price * (1 - min(weighted_avg_discount, 0.2)), 0)

            # Use execute_values to insert multiple rows in a single query
            execute_values(
                cursor,
                "INSERT INTO price_recommendation (product_master_id, price, discount, original_price, date) VALUES %s;",
                [(product_master[0], recommended_price, weighted_avg_discount, product_master[3], datetime.now())],
            )

        # Commit changes
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
