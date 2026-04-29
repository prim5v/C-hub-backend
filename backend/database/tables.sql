CREATE TABLE users_new (
    id SERIAL PRIMARY KEY,
    full_name VARCHAR(255),
    clerk_id VARCHAR(255) UNIQUE NOT NULL,
    push_token TEXT,
    email VARCHAR(255),
    role VARCHAR(50) DEFAULT 'customer',
    lat DOUBLE PRECISION,
    lng DOUBLE PRECISION,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    order_id VARCHAR(255) UNIQUE NOT NULL,
    products JSONB NOT NULL,
    delivery_address TEXT NOT NULL,
    total_price DECIMAL(10, 2) NOT NULL,
    status VARCHAR(50) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    payment_method VARCHAR(50) NOT NULL
);
-- {
--     "product_id": "prod_123",
--     "size": "M",
--     "quantity": 2
-- }  single product example for the product JSON field in the orders table.

-- {
--     "products": [
--         {
--             "product_id": "prod_123",
--             "size": "M",
--             "quantity": 2
--         },
--         {
--             "product_id": "prod_456",
--             "size": "L",
--             "quantity": 1
--         }
--     ]
-- }  example of multiple products in the product JSON field in the orders table.


CREATE TABLE mpesa_sessions (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    session_id VARCHAR(255) UNIQUE NOT NULL,
    checkout_request_id VARCHAR(255) UNIQUE,
    mpesa_receipt_code VARCHAR(255) UNIQUE,
    transaction_type VARCHAR(255) NOT NULL,
    order_id VARCHAR(255) NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    status VARCHAR(50) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    product_id VARCHAR(255) UNIQUE NOT NULL,
    product_name VARCHAR(255) NOT NULL, 
    product_description TEXT NOT NULL,
    image_url VARCHAR(255) NOT NULL,
    available_sizes JSONB NOT NULL,
    capacity INTEGER NOT NULL,
    is_popular BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- {"products": [{"size": "M", "quantity": 2, "product_id": "prod_1"}]}

Create TABLE IF NOT EXISTS users_preferences (
    id SERIAL PRIMARY KEY,
    
);