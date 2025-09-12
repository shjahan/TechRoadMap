# Section 2 – SQL and Data Types

## 2.1 PostgreSQL SQL Dialect

PostgreSQL implements a comprehensive SQL dialect that extends the SQL standard with advanced features and PostgreSQL-specific capabilities.

### SQL Standard Compliance:
- **SQL:2016**: Core standard compliance
- **SQL:2011**: Window functions, common table expressions
- **SQL:2008**: MERGE, TRUNCATE, enhanced data types
- **SQL:2003**: XML support, window functions
- **PostgreSQL Extensions**: Custom operators, data types, functions

### Key Features:
- **Advanced Queries**: Window functions, CTEs, recursive queries
- **Data Types**: Rich set of built-in and extensible types
- **Operators**: Custom operators for complex data types
- **Functions**: Extensive built-in function library
- **Procedural Languages**: Multiple languages for stored procedures

### Real-World Analogy:
PostgreSQL SQL dialect is like a comprehensive language:
- **SQL Standard** = Grammar rules and vocabulary
- **PostgreSQL Extensions** = Regional dialects and slang
- **Advanced Queries** = Complex sentence structures
- **Data Types** = Different types of words (nouns, verbs, adjectives)
- **Functions** = Idioms and expressions

### SQL Example - PostgreSQL SQL Features:
```sql
-- Window functions (SQL:2003)
SELECT 
    name,
    salary,
    department,
    ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary DESC) as rank,
    AVG(salary) OVER (PARTITION BY department) as dept_avg
FROM employees;

-- Common Table Expressions (CTEs)
WITH RECURSIVE employee_hierarchy AS (
    SELECT id, name, manager_id, 1 as level
    FROM employees 
    WHERE manager_id IS NULL
    
    UNION ALL
    
    SELECT e.id, e.name, e.manager_id, eh.level + 1
    FROM employees e
    JOIN employee_hierarchy eh ON e.manager_id = eh.id
)
SELECT * FROM employee_hierarchy ORDER BY level, name;

-- Array operations (PostgreSQL specific)
SELECT 
    name,
    skills,
    array_length(skills, 1) as skill_count,
    unnest(skills) as individual_skill
FROM developers;
```

## 2.2 Data Types Overview

PostgreSQL provides a rich set of data types covering numeric, character, date/time, boolean, and specialized types.

### Data Type Categories:
- **Numeric**: INTEGER, BIGINT, NUMERIC, REAL, DOUBLE PRECISION
- **Character**: CHAR, VARCHAR, TEXT
- **Date/Time**: DATE, TIME, TIMESTAMP, INTERVAL
- **Boolean**: BOOLEAN
- **Binary**: BYTEA
- **Geometric**: POINT, LINE, POLYGON
- **Network**: INET, CIDR, MACADDR
- **JSON**: JSON, JSONB

### Real-World Analogy:
Data types are like different containers for different purposes:
- **Numeric** = Measuring cups (precise quantities)
- **Character** = Text boxes (words and sentences)
- **Date/Time** = Calendars and clocks (temporal data)
- **Boolean** = Light switches (on/off states)
- **Binary** = Storage boxes (raw data)
- **Geometric** = Maps and blueprints (spatial data)
- **Network** = Address books (network information)
- **JSON** = Flexible containers (structured data)

### SQL Example - Data Type Usage:
```sql
-- Create table with various data types
CREATE TABLE product_catalog (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    price NUMERIC(10,2),
    quantity INTEGER,
    in_stock BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    tags TEXT[],
    metadata JSONB,
    image_data BYTEA
);

-- Insert data with different types
INSERT INTO product_catalog (name, description, price, quantity, tags, metadata)
VALUES (
    'Laptop Pro',
    'High-performance laptop for professionals',
    1299.99,
    50,
    ARRAY['electronics', 'computers', 'laptops'],
    '{"brand": "TechCorp", "warranty": "2 years", "specs": {"ram": "16GB", "storage": "512GB"}}'
);

-- Query with type-specific operations
SELECT 
    name,
    price,
    CASE WHEN quantity > 0 THEN 'In Stock' ELSE 'Out of Stock' END as availability,
    array_to_string(tags, ', ') as tag_list,
    metadata->>'brand' as brand
FROM product_catalog;
```

## 2.3 Numeric Data Types

PostgreSQL offers precise numeric types for different precision and scale requirements.

### Numeric Type Hierarchy:
- **SMALLINT**: 2 bytes, -32,768 to 32,767
- **INTEGER**: 4 bytes, -2,147,483,648 to 2,147,483,647
- **BIGINT**: 8 bytes, -9,223,372,036,854,775,808 to 9,223,372,036,854,775,807
- **DECIMAL/NUMERIC**: Variable precision, exact decimal arithmetic
- **REAL**: 4 bytes, single precision floating point
- **DOUBLE PRECISION**: 8 bytes, double precision floating point

### Real-World Analogy:
Numeric types are like different measuring instruments:
- **SMALLINT** = Small ruler (limited range, precise)
- **INTEGER** = Standard ruler (common range, precise)
- **BIGINT** = Long measuring tape (large range, precise)
- **DECIMAL/NUMERIC** = Precision caliper (exact decimal places)
- **REAL** = Approximate scale (fast, some precision loss)
- **DOUBLE PRECISION** = High-precision scale (more accurate than REAL)

### SQL Example - Numeric Operations:
```sql
-- Create table with numeric types
CREATE TABLE financial_data (
    id SERIAL PRIMARY KEY,
    account_id INTEGER,
    transaction_amount NUMERIC(15,2),
    interest_rate REAL,
    balance DOUBLE PRECISION,
    transaction_count SMALLINT
);

-- Insert sample data
INSERT INTO financial_data (account_id, transaction_amount, interest_rate, balance, transaction_count)
VALUES 
    (1001, 1500.75, 3.5, 25000.50, 15),
    (1002, -200.00, 2.8, 5000.25, 8),
    (1003, 5000.00, 4.2, 75000.00, 3);

-- Numeric calculations
SELECT 
    account_id,
    transaction_amount,
    balance,
    balance * (interest_rate / 100) as annual_interest,
    ROUND(balance * (interest_rate / 100), 2) as rounded_interest,
    transaction_amount::INTEGER as amount_as_integer
FROM financial_data;

-- Numeric functions
SELECT 
    MIN(transaction_amount) as min_transaction,
    MAX(transaction_amount) as max_transaction,
    AVG(transaction_amount) as avg_transaction,
    SUM(transaction_amount) as total_transactions,
    STDDEV(transaction_amount) as std_deviation
FROM financial_data;
```

## 2.4 Character Data Types

PostgreSQL provides flexible character types for storing text data of varying lengths and formats.

### Character Type Options:
- **CHAR(n)**: Fixed-length character string, padded with spaces
- **VARCHAR(n)**: Variable-length character string with length limit
- **TEXT**: Variable-length character string without length limit
- **CHARACTER VARYING**: Alias for VARCHAR
- **CHARACTER**: Alias for CHAR

### Real-World Analogy:
Character types are like different text containers:
- **CHAR(n)** = Fixed-size text boxes (always same size)
- **VARCHAR(n)** = Expandable text boxes (up to maximum size)
- **TEXT** = Unlimited text area (no size restrictions)

### SQL Example - Character Operations:
```sql
-- Create table with character types
CREATE TABLE user_profiles (
    id SERIAL PRIMARY KEY,
    username CHAR(20),
    full_name VARCHAR(100),
    bio TEXT,
    email VARCHAR(255),
    phone CHAR(15)
);

-- Insert sample data
INSERT INTO user_profiles (username, full_name, bio, email, phone)
VALUES 
    ('jdoe', 'John Doe', 'Software engineer with 10 years experience in web development', 'john.doe@example.com', '555-123-4567'),
    ('asmith', 'Alice Smith', 'Data scientist passionate about machine learning and AI', 'alice.smith@example.com', '555-987-6543');

-- Character string functions
SELECT 
    username,
    full_name,
    LENGTH(full_name) as name_length,
    UPPER(username) as username_upper,
    LOWER(email) as email_lower,
    SUBSTRING(bio, 1, 50) || '...' as bio_preview,
    POSITION('@' IN email) as at_position
FROM user_profiles;

-- Pattern matching
SELECT 
    full_name,
    email
FROM user_profiles 
WHERE full_name LIKE 'J%'  -- Names starting with J
   OR email LIKE '%@gmail.com';  -- Gmail addresses

-- String concatenation
SELECT 
    username || ' (' || full_name || ')' as display_name,
    'Contact: ' || email || ' | ' || phone as contact_info
FROM user_profiles;
```

## 2.5 Date and Time Types

PostgreSQL provides comprehensive date and time types with extensive functionality for temporal data handling.

### Date/Time Types:
- **DATE**: Date only (year, month, day)
- **TIME**: Time only (hour, minute, second, microsecond)
- **TIMESTAMP**: Date and time without timezone
- **TIMESTAMPTZ**: Date and time with timezone
- **INTERVAL**: Time intervals and durations
- **TIME WITH TIME ZONE**: Time with timezone information

### Real-World Analogy:
Date/time types are like different timekeeping devices:
- **DATE** = Calendar (shows dates)
- **TIME** = Clock (shows time)
- **TIMESTAMP** = Digital clock (date and time)
- **TIMESTAMPTZ** = World clock (date, time, and timezone)
- **INTERVAL** = Stopwatch (measures duration)

### SQL Example - Date/Time Operations:
```sql
-- Create table with date/time types
CREATE TABLE events (
    id SERIAL PRIMARY KEY,
    event_name VARCHAR(100),
    event_date DATE,
    start_time TIME,
    end_time TIME,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    duration INTERVAL
);

-- Insert sample data
INSERT INTO events (event_name, event_date, start_time, end_time, duration)
VALUES 
    ('Conference 2024', '2024-06-15', '09:00:00', '17:00:00', '8 hours'),
    ('Workshop', '2024-06-16', '14:30:00', '16:30:00', '2 hours'),
    ('Meeting', CURRENT_DATE, '10:00:00', '11:00:00', '1 hour');

-- Date/time functions
SELECT 
    event_name,
    event_date,
    start_time,
    end_time,
    EXTRACT(YEAR FROM event_date) as event_year,
    EXTRACT(MONTH FROM event_date) as event_month,
    EXTRACT(DAY FROM event_date) as event_day,
    AGE(event_date) as days_ago,
    event_date + INTERVAL '1 day' as next_day
FROM events;

-- Time calculations
SELECT 
    event_name,
    start_time,
    end_time,
    end_time - start_time as calculated_duration,
    duration,
    start_time + duration as calculated_end_time
FROM events;

-- Date filtering
SELECT *
FROM events 
WHERE event_date >= CURRENT_DATE 
  AND event_date <= CURRENT_DATE + INTERVAL '30 days'
ORDER BY event_date, start_time;
```

## 2.6 Boolean and Enum Types

PostgreSQL supports boolean values and enumerated types for representing fixed sets of values.

### Boolean Type:
- **BOOLEAN**: True, False, or NULL
- **Input values**: true, false, 't', 'f', 'yes', 'no', '1', '0'
- **Output values**: t, f, or NULL

### Enum Type:
- **ENUM**: User-defined enumerated type
- **Fixed set of values**: Cannot be modified after creation
- **Ordered**: Values have implicit ordering
- **Case-sensitive**: Values are case-sensitive

### Real-World Analogy:
Boolean and enum types are like switches and selectors:
- **BOOLEAN** = Light switch (on/off)
- **ENUM** = Multi-position selector switch (fixed options)

### SQL Example - Boolean and Enum Usage:
```sql
-- Create enum type
CREATE TYPE order_status AS ENUM ('pending', 'processing', 'shipped', 'delivered', 'cancelled');
CREATE TYPE priority_level AS ENUM ('low', 'medium', 'high', 'urgent');

-- Create table with boolean and enum types
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    customer_name VARCHAR(100),
    order_status order_status DEFAULT 'pending',
    priority priority_level DEFAULT 'medium',
    is_urgent BOOLEAN DEFAULT false,
    is_paid BOOLEAN DEFAULT false,
    requires_shipping BOOLEAN DEFAULT true
);

-- Insert sample data
INSERT INTO orders (customer_name, order_status, priority, is_urgent, is_paid, requires_shipping)
VALUES 
    ('John Smith', 'pending', 'high', true, false, true),
    ('Alice Johnson', 'shipped', 'medium', false, true, true),
    ('Bob Wilson', 'delivered', 'low', false, true, false);

-- Boolean operations
SELECT 
    customer_name,
    order_status,
    priority,
    is_urgent,
    is_paid,
    requires_shipping,
    is_urgent AND NOT is_paid as needs_immediate_attention,
    CASE 
        WHEN is_paid THEN 'Payment Complete'
        ELSE 'Payment Pending'
    END as payment_status
FROM orders;

-- Enum operations
SELECT 
    customer_name,
    order_status,
    priority,
    order_status > 'processing' as is_advanced,
    priority = 'urgent' as is_urgent_priority
FROM orders
WHERE order_status IN ('shipped', 'delivered')
ORDER BY priority DESC, order_status;
```

## 2.7 Array Data Types

PostgreSQL supports arrays of any data type, providing powerful capabilities for storing and querying multiple values.

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
INSERT INTO products (name, tags, prices, dimensions, categories)
VALUES 
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

## 2.8 JSON and JSONB Data Types

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
INSERT INTO user_profiles (username, profile_data, settings, metadata)
VALUES 
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

## 2.9 UUID and Network Types

PostgreSQL provides specialized types for UUIDs and network addresses.

### UUID Type:
- **UUID**: Universally Unique Identifier (128-bit)
- **Format**: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
- **Generation**: Built-in functions for UUID generation
- **Indexing**: Efficient B-tree and hash indexing

### Network Types:
- **INET**: IPv4 and IPv6 addresses
- **CIDR**: Network addresses with subnet masks
- **MACADDR**: MAC addresses (hardware addresses)

### Real-World Analogy:
UUID and network types are like identification systems:
- **UUID** = Social Security Number (unique identifier)
- **INET** = Street address (network location)
- **CIDR** = Neighborhood (network range)
- **MACADDR** = License plate (hardware identifier)

### SQL Example - UUID and Network Operations:
```sql
-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create table with UUID and network types
CREATE TABLE network_devices (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    device_name VARCHAR(100),
    ip_address INET,
    network_range CIDR,
    mac_address MACADDR,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert sample data
INSERT INTO network_devices (device_name, ip_address, network_range, mac_address)
VALUES 
    ('Web Server', '192.168.1.10', '192.168.1.0/24', '00:1B:44:11:3A:B7'),
    ('Database Server', '192.168.1.20', '192.168.1.0/24', '00:1B:44:11:3A:B8'),
    ('Router', '192.168.1.1', '192.168.1.0/24', '00:1B:44:11:3A:B9');

-- UUID operations
SELECT 
    id,
    device_name,
    uuid_generate_v4() as new_uuid,
    uuid_generate_v1() as time_based_uuid
FROM network_devices;

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
```

## 2.10 Custom Data Types

PostgreSQL allows creation of custom data types using various methods.

### Custom Type Methods:
- **Composite Types**: User-defined structured types
- **Domain Types**: Constrained base types
- **Enum Types**: Enumerated value types
- **Range Types**: Range value types
- **Base Types**: Low-level C types (advanced)

### Real-World Analogy:
Custom data types are like creating specialized containers:
- **Composite Types** = Custom boxes with specific compartments
- **Domain Types** = Standard boxes with custom labels and rules
- **Enum Types** = Predefined selection lists
- **Range Types** = Measuring tools with specific ranges

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
INSERT INTO customers (name, email, billing_address, temp_range)
VALUES 
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
```