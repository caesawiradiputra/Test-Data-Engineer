-- database_setup.sql

CREATE TABLE IF NOT EXISTS product_master (
    id SERIAL PRIMARY KEY,
    type VARCHAR(255),
    name VARCHAR(255),
    detail TEXT
);

CREATE TABLE IF NOT EXISTS product (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    price NUMERIC,
    original_price NUMERIC,
    discount_percentage NUMERIC,
    detail TEXT,
    platform VARCHAR(255),
    product_master_id INTEGER REFERENCES product_master(id),
    create_date TIMESTAMP
);

CREATE TABLE IF NOT EXISTS price_recommendation (
    product_master_id INTEGER REFERENCES product_master(id),
    price NUMERIC,
    discount NUMERIC,
    original_price NUMERIC,
    date DATE
);
