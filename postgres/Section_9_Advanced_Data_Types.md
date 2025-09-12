# Section 9 – Advanced Data Types

## 9.1 JSON and JSONB Operations

PostgreSQL provides native JSON support with two data types: JSON (text-based) and JSONB (binary).

### JSON vs JSONB:
- **JSON**: Stored as text, preserves formatting, slower queries
- **JSONB**: Stored as binary, removes whitespace, faster queries
- **JSONB advantages**: Indexing, better performance, more operators
- **JSON advantages**: Preserves exact formatting, smaller storage

### Real-World Analogy:
JSON types are like different document formats:
- **JSON** = Handwritten document (preserves exact formatting)
- **JSONB** = Typed document (optimized for reading and searching)

### SQL Example - JSON Operations:
```sql
-- Create table with JSON columns
CREATE TABLE user_profiles (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50),
    profile_data JSON,
    settings JSONB,
    metadata JSONB
);

-- Insert sample data
INSERT INTO user_profiles (username, profile_data, settings, metadata) VALUES
    ('jdoe', 
     '{"name": "John Doe", "age": 30, "location": "New York", "hobbies": ["reading", "gaming"]}',
     '{"theme": "dark", "notifications": true, "language": "en"}',
     '{"created_at": "2024-01-15", "last_login": "2024-01-20", "login_count": 42}'),
    ('asmith',
     '{"name": "Alice Smith", "age": 25, "location": "San Francisco", "hobbies": ["cooking", "travel"]}',
     '{"theme": "light", "notifications": false, "language": "en"}',
     '{"created_at": "2024-01-10", "last_login": "2024-01-19", "login_count": 28}');

-- JSON querying
SELECT 
    username,
    profile_data->>'name' as full_name,
    profile_data->>'age' as age,
    profile_data->'hobbies' as hobbies,
    settings->>'theme' as theme,
    metadata->>'last_login' as last_login
FROM user_profiles;

-- JSONB operations
SELECT 
    username,
    settings,
    settings ? 'theme' as has_theme,
    settings ?& ARRAY['theme', 'notifications'] as has_all_settings,
    settings ?| ARRAY['theme', 'language'] as has_any_setting
FROM user_profiles;

-- JSON functions
SELECT 
    username,
    jsonb_pretty(settings) as formatted_settings,
    jsonb_object_keys(settings) as setting_keys,
    jsonb_array_length(profile_data->'hobbies') as hobby_count
FROM user_profiles;

-- JSON aggregation
SELECT 
    jsonb_agg(
        jsonb_build_object(
            'username', username,
            'name', profile_data->>'name',
            'age', (profile_data->>'age')::integer
        )
    ) as all_users
FROM user_profiles;
```

## 9.2 Array Operations and Functions

PostgreSQL supports arrays of any data type with comprehensive operations and functions.

### Array Features:
- **Any data type**: Arrays of any PostgreSQL data type
- **Multi-dimensional**: Support for multi-dimensional arrays
- **Variable length**: Arrays can have different lengths
- **Rich operators**: Extensive set of array operators
- **Functions**: Comprehensive array function library

### Real-World Analogy:
Arrays are like containers with multiple compartments:
- **Single-dimensional** = Simple list or row of items
- **Multi-dimensional** = Table or grid of items
- **Variable length** = Expandable containers
- **Operators** = Tools for manipulating the containers

### SQL Example - Array Operations:
```sql
-- Create table with array columns
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    tags TEXT[],
    prices NUMERIC[],
    dimensions INTEGER[][],
    categories VARCHAR(50)[]
);

-- Insert sample data
INSERT INTO products (name, tags, prices, dimensions, categories) VALUES
    ('Laptop', ARRAY['electronics', 'computers', 'portable'], ARRAY[999.99, 1299.99], ARRAY[[15, 10, 1]], ARRAY['Electronics', 'Computers']),
    ('Phone', ARRAY['electronics', 'mobile', 'communication'], ARRAY[699.99, 899.99], ARRAY[[6, 3, 0.5]], ARRAY['Electronics', 'Mobile']),
    ('Book', ARRAY['education', 'reading', 'paperback'], ARRAY[19.99, 29.99], ARRAY[[8, 5, 1]], ARRAY['Education', 'Books']);

-- Array operations
SELECT 
    name,
    tags,
    array_length(tags, 1) as tag_count,
    tags[1] as primary_tag,
    array_to_string(tags, ', ') as tag_string
FROM products;

-- Array functions
SELECT 
    name,
    prices,
    array_min(prices) as min_price,
    array_max(prices) as max_price,
    array_avg(prices) as avg_price,
    array_sum(prices) as total_price
FROM products;

-- Array searching
SELECT 
    name,
    tags
FROM products 
WHERE 'electronics' = ANY(tags)
   OR 'education' = ANY(tags);

-- Array containment
SELECT 
    name,
    tags
FROM products 
WHERE tags @> ARRAY['electronics']
   AND tags @> ARRAY['portable'];

-- Unnest arrays
SELECT 
    name,
    unnest(tags) as individual_tag
FROM products 
ORDER BY name, individual_tag;
```

## 9.3 Range Types

Range types represent ranges of values with comprehensive operations and functions.

### Range Type Features:
- **Built-in Types**: int4range, int8range, numrange, tsrange, tstzrange, daterange
- **Custom Types**: User-defined range types
- **Operators**: Overlap, contains, contained by, adjacent
- **Functions**: Range construction, manipulation, and querying
- **Indexing**: GiST indexes for range operations

### Real-World Analogy:
Range types are like measuring tools:
- **Built-in Types** = Standard measuring instruments
- **Custom Types** = Specialized measuring tools
- **Operators** = Different ways to compare measurements
- **Functions** = Tools for working with measurements
- **Indexing** = Quick lookup of measurements

### SQL Example - Range Types:
```sql
-- Create table with range types
CREATE TABLE events (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    duration TSRANGE,
    price_range NUMRANGE,
    age_range INT4RANGE
);

-- Insert sample data
INSERT INTO events (name, duration, price_range, age_range) VALUES
    ('Conference', '[2024-01-15 09:00, 2024-01-15 17:00]', '[100, 500]', '[18, 65]'),
    ('Workshop', '[2024-01-16 14:00, 2024-01-16 16:00]', '[50, 200]', '[21, 50]'),
    ('Meeting', '[2024-01-17 10:00, 2024-01-17 11:00]', '[0, 0]', '[25, 40]');

-- Range operations
SELECT 
    name,
    duration,
    lower(duration) as start_time,
    upper(duration) as end_time,
    duration @> TIMESTAMP '2024-01-15 10:00' as contains_time,
    duration && TSRANGE('[2024-01-15 08:00, 2024-01-15 12:00]') as overlaps_morning
FROM events;

-- Range functions
SELECT 
    name,
    price_range,
    lower(price_range) as min_price,
    upper(price_range) as max_price,
    price_range @> 150 as contains_price,
    price_range && NUMRANGE('[100, 300]') as overlaps_range
FROM events;

-- Range aggregation
SELECT 
    name,
    duration,
    age_range,
    CASE 
        WHEN age_range @> 30 THEN 'Includes 30s'
        ELSE 'Excludes 30s'
    END as age_30_status
FROM events
WHERE duration @> TIMESTAMP '2024-01-15 10:00';
```

## 9.4 Composite Types

Composite types allow creating structured data types with multiple fields.

### Composite Type Features:
- **Field Access**: Access individual fields with dot notation
- **Construction**: Build composite values with ROW constructor
- **Comparison**: Compare composite values
- **Functions**: Built-in functions for composite types
- **Indexing**: Index on composite type fields

### Real-World Analogy:
Composite types are like structured forms:
- **Field Access** = Reading specific form fields
- **Construction** = Filling out the form
- **Comparison** = Comparing completed forms
- **Functions** = Tools for working with forms
- **Indexing** = Organizing forms by specific fields

### SQL Example - Composite Types:
```sql
-- Create composite type
CREATE TYPE address AS (
    street VARCHAR(100),
    city VARCHAR(50),
    state VARCHAR(2),
    zip_code VARCHAR(10)
);

-- Create table using composite type
CREATE TABLE customers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    billing_address address,
    shipping_address address
);

-- Insert sample data
INSERT INTO customers (name, billing_address, shipping_address) VALUES
    ('John Doe', 
     ROW('123 Main St', 'New York', 'NY', '10001'),
     ROW('123 Main St', 'New York', 'NY', '10001')),
    ('Alice Smith',
     ROW('456 Oak Ave', 'San Francisco', 'CA', '94102'),
     ROW('789 Pine St', 'San Francisco', 'CA', '94103'));

-- Access composite type fields
SELECT 
    name,
    (billing_address).street as billing_street,
    (billing_address).city as billing_city,
    (shipping_address).street as shipping_street,
    (shipping_address).city as shipping_city
FROM customers;

-- Compare composite types
SELECT 
    name,
    billing_address,
    shipping_address,
    billing_address = shipping_address as same_address
FROM customers;

-- Composite type functions
SELECT 
    name,
    billing_address,
    (billing_address).street || ', ' || (billing_address).city as full_address
FROM customers;

-- Update composite type
UPDATE customers 
SET billing_address = ROW('999 New St', 'Boston', 'MA', '02101')
WHERE name = 'John Doe';
```

## 9.5 Domain Types

Domain types are constrained base types with validation rules.

### Domain Type Features:
- **Base Type**: Built on existing PostgreSQL types
- **Constraints**: Check constraints for validation
- **Default Values**: Default values for domain types
- **Inheritance**: Domain types inherit base type properties
- **Validation**: Automatic validation of values

### Real-World Analogy:
Domain types are like specialized containers:
- **Base Type** = Basic container type
- **Constraints** = Rules for what can go in container
- **Default Values** = Pre-filled container contents
- **Inheritance** = Container inherits basic properties
- **Validation** = Automatic checking of contents

### SQL Example - Domain Types:
```sql
-- Create domain types
CREATE DOMAIN email_address AS VARCHAR(255)
CHECK (VALUE ~ '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$');

CREATE DOMAIN phone_number AS VARCHAR(20)
CHECK (VALUE ~ '^\+?[1-9]\d{1,14}$');

CREATE DOMAIN positive_amount AS NUMERIC(10,2)
CHECK (VALUE > 0);

CREATE DOMAIN age AS INTEGER
CHECK (VALUE >= 0 AND VALUE <= 150);

-- Create table using domain types
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    email email_address,
    phone phone_number,
    age age,
    balance positive_amount DEFAULT 0.00
);

-- Insert valid data
INSERT INTO users (name, email, phone, age, balance) VALUES
    ('John Doe', 'john@example.com', '+1234567890', 30, 1000.00),
    ('Alice Smith', 'alice@example.com', '555-123-4567', 25, 500.50);

-- Try to insert invalid data (will fail)
INSERT INTO users (name, email, phone, age, balance) VALUES
    ('Invalid User', 'invalid-email', 'invalid-phone', 200, -100.00);

-- Check domain constraints
SELECT 
    domain_name,
    data_type,
    character_maximum_length,
    domain_default,
    check_clause
FROM information_schema.domains
WHERE domain_schema = 'public';

-- Use domain types in functions
CREATE OR REPLACE FUNCTION create_user(
    p_name VARCHAR,
    p_email email_address,
    p_phone phone_number,
    p_age age
) RETURNS INTEGER AS $$
DECLARE
    user_id INTEGER;
BEGIN
    INSERT INTO users (name, email, phone, age)
    VALUES (p_name, p_email, p_phone, p_age)
    RETURNING id INTO user_id;
    
    RETURN user_id;
END;
$$ LANGUAGE plpgsql;
```

## 9.6 Enumerated Types

Enumerated types define a fixed set of values with ordering.

### Enum Type Features:
- **Fixed Values**: Cannot be modified after creation
- **Ordering**: Values have implicit ordering
- **Case-Sensitive**: Values are case-sensitive
- **Comparison**: Can compare enum values
- **Functions**: Built-in functions for enum types

### Real-World Analogy:
Enum types are like predefined options:
- **Fixed Values** = Limited set of choices
- **Ordering** = Options have a specific order
- **Case-Sensitive** = Exact spelling matters
- **Comparison** = Can compare options
- **Functions** = Tools for working with options

### SQL Example - Enumerated Types:
```sql
-- Create enum types
CREATE TYPE order_status AS ENUM ('pending', 'processing', 'shipped', 'delivered', 'cancelled');
CREATE TYPE priority_level AS ENUM ('low', 'medium', 'high', 'urgent');
CREATE TYPE user_role AS ENUM ('admin', 'user', 'guest');

-- Create table using enum types
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    customer_name VARCHAR(100),
    status order_status DEFAULT 'pending',
    priority priority_level DEFAULT 'medium',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert sample data
INSERT INTO orders (customer_name, status, priority) VALUES
    ('John Doe', 'pending', 'high'),
    ('Alice Smith', 'shipped', 'medium'),
    ('Bob Wilson', 'delivered', 'low'),
    ('Carol Brown', 'cancelled', 'urgent');

-- Enum operations
SELECT 
    customer_name,
    status,
    priority,
    status > 'processing' as is_advanced,
    priority = 'urgent' as is_urgent
FROM orders
ORDER BY status, priority;

-- Enum functions
SELECT 
    customer_name,
    status,
    priority,
    enumlabel as status_label
FROM orders
JOIN pg_enum ON orders.status::text = enumlabel
WHERE enumtypid = 'order_status'::regtype
ORDER BY enumsortorder;

-- Check enum values
SELECT 
    enumlabel,
    enumsortorder
FROM pg_enum
WHERE enumtypid = 'order_status'::regtype
ORDER BY enumsortorder;

-- Compare enum values
SELECT 
    customer_name,
    status,
    CASE 
        WHEN status = 'delivered' THEN 'Order completed'
        WHEN status = 'cancelled' THEN 'Order cancelled'
        ELSE 'Order in progress'
    END as status_description
FROM orders;
```

## 9.7 Network Address Types

PostgreSQL provides specialized types for network addresses and ranges.

### Network Address Types:
- **INET**: IPv4 and IPv6 addresses
- **CIDR**: Network addresses with subnet masks
- **MACADDR**: MAC addresses (hardware addresses)
- **Operators**: Network containment and comparison
- **Functions**: Network address manipulation

### Real-World Analogy:
Network address types are like address systems:
- **INET** = Street addresses (network locations)
- **CIDR** = Neighborhoods (network ranges)
- **MACADDR** = License plates (hardware identifiers)
- **Operators** = Different ways to compare addresses
- **Functions** = Tools for working with addresses

### SQL Example - Network Address Types:
```sql
-- Create table with network types
CREATE TABLE network_devices (
    id SERIAL PRIMARY KEY,
    device_name VARCHAR(100),
    ip_address INET,
    network_range CIDR,
    mac_address MACADDR,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert sample data
INSERT INTO network_devices (device_name, ip_address, network_range, mac_address) VALUES
    ('Web Server', '192.168.1.10', '192.168.1.0/24', '00:1B:44:11:3A:B7'),
    ('Database Server', '192.168.1.20', '192.168.1.0/24', '00:1B:44:11:3A:B8'),
    ('Router', '192.168.1.1', '192.168.1.0/24', '00:1B:44:11:3A:B9'),
    ('External Server', '203.0.113.5', '203.0.113.0/24', '00:1B:44:11:3A:BA');

-- Network operations
SELECT 
    device_name,
    ip_address,
    network_range,
    mac_address,
    family(ip_address) as ip_version,
    host(ip_address) as host_address,
    masklen(network_range) as subnet_mask_length
FROM network_devices;

-- Network containment
SELECT 
    device_name,
    ip_address,
    network_range
FROM network_devices 
WHERE ip_address << network_range;

-- Network functions
SELECT 
    device_name,
    ip_address,
    set_masklen(ip_address, 24) as ip_with_mask,
    broadcast(ip_address) as broadcast_address,
    network(ip_address) as network_address
FROM network_devices;

-- MAC address operations
SELECT 
    device_name,
    mac_address,
    mac_address::TEXT as mac_string
FROM network_devices
ORDER BY mac_address;
```

## 9.8 Geometric Types

PostgreSQL provides geometric types for spatial data operations.

### Geometric Types:
- **POINT**: Single point in 2D space
- **LINE**: Infinite line in 2D space
- **LSEG**: Line segment in 2D space
- **BOX**: Rectangular box in 2D space
- **PATH**: Connected line segments
- **POLYGON**: Closed path forming a polygon
- **CIRCLE**: Circle in 2D space

### Real-World Analogy:
Geometric types are like drawing tools:
- **POINT** = Single dot
- **LINE** = Infinite line
- **LSEG** = Line segment
- **BOX** = Rectangle
- **PATH** = Connected lines
- **POLYGON** = Closed shape
- **CIRCLE** = Circle

### SQL Example - Geometric Types:
```sql
-- Create table with geometric types
CREATE TABLE locations (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    point POINT,
    polygon POLYGON,
    circle CIRCLE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert sample data
INSERT INTO locations (name, point, polygon, circle) VALUES
    ('Central Park', 
     POINT(-73.965355, 40.782865), 
     POLYGON((-73.973, 40.764, -73.973, 40.800, -73.958, 40.800, -73.958, 40.764, -73.973, 40.764)),
     CIRCLE(POINT(-73.965355, 40.782865), 1000)),
    ('Times Square', 
     POINT(-73.985130, 40.758896), 
     POLYGON((-73.990, 40.755, -73.990, 40.762, -73.980, 40.762, -73.980, 40.755, -73.990, 40.755)),
     CIRCLE(POINT(-73.985130, 40.758896), 500));

-- Geometric operations
SELECT 
    name,
    point,
    polygon,
    circle,
    area(polygon) as polygon_area,
    radius(circle) as circle_radius
FROM locations;

-- Geometric containment
SELECT 
    name,
    point,
    polygon
FROM locations 
WHERE polygon @> point;

-- Geometric intersection
SELECT 
    name,
    polygon
FROM locations 
WHERE polygon && POLYGON((-74.000, 40.700, -74.000, 40.800, -73.950, 40.800, -73.950, 40.700, -74.000, 40.700));

-- Distance calculations
SELECT 
    name,
    point,
    distance(point, POINT(-73.985130, 40.758896)) as distance_to_times_square
FROM locations
ORDER BY distance_to_times_square;
```

## 9.9 Text Search Types

PostgreSQL provides specialized types for full-text search operations.

### Text Search Types:
- **tsvector**: Normalized text for searching
- **tsquery**: Search query with operators
- **tsconfig**: Text search configuration
- **Operators**: Text search operators
- **Functions**: Text search functions

### Real-World Analogy:
Text search types are like search tools:
- **tsvector** = Index of searchable text
- **tsquery** = Search request
- **tsconfig** = Search configuration
- **Operators** = Different search methods
- **Functions** = Tools for searching

### SQL Example - Text Search Types:
```sql
-- Create table with text search
CREATE TABLE documents (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200),
    content TEXT,
    search_vector tsvector,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert sample data
INSERT INTO documents (title, content, search_vector) VALUES
    ('PostgreSQL Guide', 'PostgreSQL is a powerful database system', 
     to_tsvector('english', 'PostgreSQL is a powerful database system')),
    ('SQL Tutorial', 'Learn SQL with practical examples', 
     to_tsvector('english', 'Learn SQL with practical examples')),
    ('Database Design', 'Designing efficient database schemas', 
     to_tsvector('english', 'Designing efficient database schemas'));

-- Text search operations
SELECT 
    title,
    content,
    search_vector,
    search_vector @@ to_tsquery('english', 'database') as contains_database,
    search_vector @@ to_tsquery('english', 'PostgreSQL & powerful') as contains_postgresql_powerful
FROM documents;

-- Text search functions
SELECT 
    title,
    ts_rank(search_vector, to_tsquery('english', 'database')) as rank,
    ts_headline('english', content, to_tsquery('english', 'database')) as headline
FROM documents
WHERE search_vector @@ to_tsquery('english', 'database')
ORDER BY rank DESC;

-- Text search configuration
SELECT 
    cfgname,
    cfgowner,
    cfgparser
FROM pg_ts_config
WHERE cfgname = 'english';

-- Text search operators
SELECT 
    title,
    content
FROM documents
WHERE search_vector @@ to_tsquery('english', 'database | sql')
ORDER BY title;
```

## 9.10 Custom Type Creation

PostgreSQL allows creation of custom data types using various methods.

### Custom Type Methods:
- **Composite Types**: User-defined structured types
- **Domain Types**: Constrained base types
- **Enum Types**: Enumerated value types
- **Range Types**: Range value types
- **Base Types**: Low-level C types (advanced)

### Real-World Analogy:
Custom type creation is like creating specialized tools:
- **Composite Types** = Custom multi-part tools
- **Domain Types** = Specialized versions of basic tools
- **Enum Types** = Tools with predefined options
- **Range Types** = Tools for measuring ranges
- **Base Types** = Creating entirely new tools

### SQL Example - Custom Type Creation:
```sql
-- Create composite type
CREATE TYPE address AS (
    street VARCHAR(100),
    city VARCHAR(50),
    state VARCHAR(2),
    zip_code VARCHAR(10)
);

-- Create domain type
CREATE DOMAIN email_address AS VARCHAR(255)
CHECK (VALUE ~ '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$');

-- Create enum type
CREATE TYPE order_status AS ENUM ('pending', 'processing', 'shipped', 'delivered', 'cancelled');

-- Create range type
CREATE TYPE temperature_range AS RANGE (
    SUBTYPE = NUMERIC
);

-- Create table using custom types
CREATE TABLE customers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    email email_address,
    billing_address address,
    temp_range temperature_range,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert sample data
INSERT INTO customers (name, email, billing_address, temp_range) VALUES
    ('John Doe', 'john@example.com', 
     ROW('123 Main St', 'New York', 'NY', '10001'),
     '[20.0, 25.0]'),
    ('Alice Smith', 'alice@example.com',
     ROW('456 Oak Ave', 'San Francisco', 'CA', '94102'),
     '[15.0, 30.0]');

-- Query custom types
SELECT 
    name,
    email,
    (billing_address).street as street,
    (billing_address).city as city,
    (billing_address).state as state,
    temp_range,
    lower(temp_range) as min_temp,
    upper(temp_range) as max_temp
FROM customers;

-- Custom type functions
SELECT 
    name,
    email,
    billing_address,
    temp_range,
    temp_range @> 22.5 as contains_22_5,
    temp_range && '[18.0, 28.0]' as overlaps_range
FROM customers;

-- Check custom types
SELECT 
    typname,
    typtype,
    typcategory,
    typinput,
    typoutput
FROM pg_type
WHERE typname IN ('address', 'email_address', 'order_status', 'temperature_range')
ORDER BY typname;
```