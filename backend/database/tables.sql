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

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    clerk_id VARCHAR(255) UNIQUE NOT NULL,
    full_name VARCHAR(255),
    email VARCHAR(255),
    role VARCHAR(50) DEFAULT 'customer',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE user_devices (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,

    push_token TEXT NOT NULL,
    
    device_id VARCHAR(255),        -- optional (unique device fingerprint)
    platform VARCHAR(50),          -- ios | android | web
    device_name VARCHAR(100),      -- "iPhone 14", "Samsung S21"

    lat DOUBLE PRECISION,
    lng DOUBLE PRECISION,

    last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE campuses (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    campus VARCHAR(255) NOT NULL, -- e.g. "Main Campus", "City Campus"
    color VARCHAR(50) NOT NULL,
    initials VARCHAR(10) NOT NULL,
    coordinates JSONB NOT NULL,  -- {"lat": 1.234, "lng": 2.345}
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE rooms(
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    campus_id INTEGER REFERENCES campuses(id) ON DELETE SET NULL,
    is_available BOOLEAN DEFAULT TRUE,
    room_type VARCHAR(100),
    distance VARCHAR(50),
    price DECIMAL(10, 2),
    room_description VARCHAR(255),
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE amenities(
    id SERIAL PRIMARY KEY,
    amenity_key VARCHAR(255) UNIQUE NOT NULL,
    label VARCHAR(255) NOT NULL
);

CREATE TABLE room_amenities (
    id SERIAL PRIMARY KEY,
    room_id INTEGER REFERENCES rooms(id) ON DELETE CASCADE,
    amenity_id INTEGER REFERENCES amenities(id) ON DELETE CASCADE
);

CREATE TABLE accomodatives (
     id SERIAL PRIMARY KEY,
     room_id INTEGER REFERENCES rooms(id) ON DELETE CASCADE,
     beds INTEGER DEFAULT 1,
     baths INTEGER DEFAULT 1,
     wifi BOOLEAN DEFAULT FALSE,
     furnished BOOLEAN DEFAULT FALSE,
     self_contained BOOLEAN DEFAULT FALSE
);

CREATE TABLE images (
    id SERIAL PRIMARY KEY,
    room_id INTEGER REFERENCES rooms(id) ON DELETE CASCADE,
    image_url VARCHAR(255) NOT NULL,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE location_data (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) REFERENCES users(clerk_id) ON DELETE CASCADE NULL,
    room_id INTEGER REFERENCES rooms(id) ON DELETE CASCADE NULL,
    coordinates JSONB NOT NULL,  -- {"lat": 1.234, "lng": 2.345}
    address VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- INSERT INTO campuses (name, campus, color, initials, coordinates)
-- VALUES (
--     'KCA',
--     'Main Campus',
--     'yellow',
--     'KCA',
--     '{"lat": -1.2532105175525106, "lng": 36.859377575781984}'::jsonb
-- );

INSERT INTO amenities (amenity_key, label) VALUES
('wifi', 'Wi-Fi'),
('fibre', 'Fibre Internet'),
('borehole', 'Borehole Water'),
('city_water', 'City Water'),
('prepaid_power', 'Prepaid Electricity'),
('backup_power', 'Backup Power'),
('solar_hot_water', 'Solar Hot Water'),
('water_tank', 'Water Tank'),
('security', '24/7 Security'),
('cctv', 'CCTV'),
('gated', 'Gated Compound'),
('electric_fence', 'Electric Fence'),
('controlled_access', 'Controlled Access'),
('parking', 'Parking'),
('private_parking', 'Private Parking'),
('motorbike_parking', 'Motorbike Parking'),
('furnished', 'Furnished'),
('semi_furnished', 'Semi-Furnished'),
('wardrobe', 'Built-in Wardrobes'),
('balcony', 'Balcony'),
('tiled_floor', 'Tiled Floor'),
('wood_floor', 'Wooden Floor'),
('open_kitchen', 'Open Kitchen'),
('kitchen_cabinets', 'Kitchen Cabinets'),
('pantry', 'Pantry'),
('hot_shower', 'Hot Shower'),
('bathtub', 'Bathtub'),
('instant_shower', 'Instant Shower'),
('separate_toilet', 'Separate Toilet'),
('laundry_area', 'Laundry Area'),
('drying_area', 'Drying Area'),
('elevator', 'Elevator'),
('caretaker', 'Caretaker On Site'),
('garbage', 'Garbage Collection'),
('garden', 'Garden'),
('rooftop', 'Rooftop Access'),
('shared_kitchen', 'Shared Kitchen'),
('shared_bathroom', 'Shared Bathroom'),
('study_area', 'Study Area'),
('common_room', 'Common Room'),
('warden', 'On-site Warden'),
('pets_allowed', 'Pets Allowed'),
('no_smoking', 'No Smoking');