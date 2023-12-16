# src/data_processing/data_processing.py
import psycopg2
from datetime import datetime
import logging, time

from ..config import CONNECTION_STRING

def clean_data():
    try:
        # Connect to the database
        conn = psycopg2.connect(CONNECTION_STRING)
        cursor = conn.cursor()

        # cursor.execute("TRUNCATE TABLE price_recommendation;")
        # cursor.execute("TRUNCATE TABLE product;")
        # cursor.execute("TRUNCATE TABLE product_master;")
        cursor.execute("DELETE FROM price_recommendation;")
        cursor.execute("DELETE FROM product;")
        cursor.execute("DELETE FROM product_master;")

        # Commit changes and close the connection
        conn.commit()
        cursor.close()
        conn.close()

    except psycopg2.Error as e:
        # Log the error
        logging.error(f"Error in data processing: {e}")

    finally:
        # Close the cursor and connection in the finally block to ensure it happens even if an exception occurs
        if cursor:
            cursor.close()
        if conn:
            conn.close()            

def parse_and_save_data(product_data):
    try:
        start_time = time.time()
        logging.info(f"Attempting to parse and save data")
        # Connect to the database
        conn = psycopg2.connect(CONNECTION_STRING)
        cursor = conn.cursor()

        # Save the crawled data to the database
        for product in product_data:
            cursor.execute("Select id, detail, type from product_master where name = %s", (product["name"],))
            result = cursor.fetchone()

            if result:
                product_master_id = result[0]
                # if product.get("detail", "") != "" and product.get("detail", "") != result[1]:
                #     cursor.execute(
                #         """
                #         UPDATE product_master
                #             SET detail = %s
                #                 ,type = %s
                #         WHERE id = %s"
                #         """, product.get("detail", ""), product.get("category", ""), result[0]
                #     )
            else:
                cursor.execute(
                    "INSERT INTO product_master (name, detail, type) VALUES (%s, %s, %s) RETURNING id;",
                    (
                        product.get("name", ""), 
                        product.get("detail", ""), 
                        product.get("category", "")
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

        execution_time = time.time() - start_time
        logging.info(f"Successfully parse and save data, in: {execution_time} seconds")

    except psycopg2.Error as e:
        logging.error(f"Error connecting to the database: {e}")
        # Optionally, you can re-raise the exception to propagate it further
        raise e

    except Exception as e:
        logging.exception(f"An unexpected error occurred while parsing and saving data: {e}")
        raise e

    finally:
        # Close the cursor and connection in the finally block to ensure it happens even if an exception occurs
        if cursor:
            cursor.close()
        if conn:
            conn.close()  

def list_product_data():
    # Connect to the database
    conn = psycopg2.connect(CONNECTION_STRING)
    cursor = conn.cursor()

    # Placeholder: Sample query to retrieve product data
    cursor.execute("SELECT id, name, price, platform FROM product;")
    products = cursor.fetchall()

    # Convert the result to a list of dictionaries
    product_list = [{"id": row[0], "name": row[1], "price": row[2], "platform": row[3]} for row in products]

    # Close the database connection
    cursor.close()
    conn.close()

    return product_list

def list_price_recomendation():
    # Connect to the database
    conn = psycopg2.connect(CONNECTION_STRING)
    cursor = conn.cursor()

    # Placeholder: Sample query to retrieve product data
    cursor.execute("""
                    select pr.product_master_id, pm.name, pr.price, pr.discount, pr.original_price 
                    from price_recommendation pr
                    join product_master pm on pm.id = pr.product_master_id;
                    """)
    price_recommendations = cursor.fetchall()

    # Convert the result to a list of dictionaries
    price_recommendations_list = [{"product_master_id": row[0], "name": row[1], "price": row[2], "discount": f"{row[3]}%", "original_price": row[4]} for row in price_recommendations]

    # Close the database connection
    cursor.close()
    conn.close()

    return price_recommendations_list

# if __name__ == "__main__":
#     clean_and_process_data()
