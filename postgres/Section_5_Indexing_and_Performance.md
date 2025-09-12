# Section 5 – Indexing and Performance

## 5.1 Index Fundamentals

Indexes are database objects that improve query performance by providing fast access to data without scanning entire tables.

### Index Concepts:
- **Purpose**: Speed up data retrieval operations
- **Trade-offs**: Faster reads vs slower writes and storage overhead
- **Types**: B-tree, Hash, GIN, GiST, SP-GiST, BRIN
- **Maintenance**: Automatic updates, but require maintenance
- **Statistics**: Query planner uses index statistics for optimization

### Real-World Analogy:
Indexes are like book indexes or library catalogs:
- **Purpose** = Quick way to find information without reading entire book
- **Trade-offs** = Faster lookup vs extra space and maintenance
- **Types** = Different catalog systems (alphabetical, subject, author)
- **Maintenance** = Keeping the catalog up to date
- **Statistics** = Librarian's knowledge about what's available

### SQL Example - Index Fundamentals:
```sql
-- Create sample table
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    category VARCHAR(50),
    price NUMERIC(10,2),
    stock_quantity INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO products (name, category, price, stock_quantity) VALUES
    ('Laptop Pro', 'Electronics', 1299.99, 50),
    ('Gaming Mouse', 'Electronics', 79.99, 100),
    ('Programming Book', 'Books', 49.99, 200),
    ('Office Chair', 'Furniture', 299.99, 25),
    ('Wireless Keyboard', 'Electronics', 89.99, 75);

-- Create basic B-tree index
CREATE INDEX idx_products_name ON products(name);

-- Create composite index
CREATE INDEX idx_products_category_price ON products(category, price);

-- Create partial index (only for active products)
CREATE INDEX idx_products_active ON products(name) 
WHERE stock_quantity > 0;

-- Check index usage
EXPLAIN (ANALYZE, BUFFERS) 
SELECT * FROM products WHERE name = 'Laptop Pro';

-- List all indexes on table
SELECT 
    indexname,
    indexdef
FROM pg_indexes 
WHERE tablename = 'products';

-- Check index size
SELECT 
    schemaname,
    tablename,
    indexname,
    pg_size_pretty(pg_relation_size(indexname::regclass)) as index_size
FROM pg_indexes 
WHERE tablename = 'products';
```

## 5.2 B-Tree Indexes

B-tree indexes are the most common type in PostgreSQL, providing efficient range queries and equality searches.

### B-Tree Features:
- **Balanced Tree**: Self-balancing tree structure
- **Range Queries**: Efficient for <, >, <=, >=, BETWEEN
- **Equality**: Fast for = and IN operations
- **Sorting**: Results are returned in sorted order
- **NULL Handling**: Supports NULL values

### B-Tree Use Cases:
- **Primary Keys**: Automatic B-tree index
- **Foreign Keys**: Often benefit from B-tree indexes
- **Frequently Queried Columns**: Columns in WHERE clauses
- **Sorting**: Columns in ORDER BY clauses
- **Range Queries**: Date ranges, numeric ranges

### Real-World Analogy:
B-tree indexes are like organized filing cabinets:
- **Balanced Tree** = Equal-sized drawers for easy access
- **Range Queries** = Finding all files between two dates
- **Equality** = Finding a specific file by exact name
- **Sorting** = Files are already in order
- **NULL Handling** = Special drawer for unknown items

### SQL Example - B-Tree Indexes:
```sql
-- Create table with various data types
CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    customer_id INTEGER,
    order_date DATE,
    total_amount NUMERIC(10,2),
    status VARCHAR(20),
    region VARCHAR(50)
);

INSERT INTO orders (customer_id, order_date, total_amount, status, region) VALUES
    (1, '2024-01-15', 150.00, 'completed', 'North'),
    (2, '2024-01-16', 299.99, 'pending', 'South'),
    (3, '2024-01-17', 75.50, 'completed', 'East'),
    (4, '2024-01-18', 200.00, 'shipped', 'West'),
    (5, '2024-01-19', 450.00, 'completed', 'North');

-- Create B-tree indexes
CREATE INDEX idx_orders_customer ON orders(customer_id);
CREATE INDEX idx_orders_date ON orders(order_date);
CREATE INDEX idx_orders_amount ON orders(total_amount);
CREATE INDEX idx_orders_status ON orders(status);

-- Range queries using B-tree indexes
EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM orders 
WHERE order_date BETWEEN '2024-01-16' AND '2024-01-18';

-- Equality queries
EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM orders 
WHERE status = 'completed';

-- Sorting with B-tree index
EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM orders 
ORDER BY total_amount DESC;

-- Composite B-tree index
CREATE INDEX idx_orders_region_status ON orders(region, status);

-- Query using composite index
EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM orders 
WHERE region = 'North' AND status = 'completed';

-- Partial B-tree index
CREATE INDEX idx_orders_high_value ON orders(total_amount) 
WHERE total_amount > 200;

-- Query using partial index
EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM orders 
WHERE total_amount > 200;
```

## 5.3 Hash Indexes

Hash indexes provide very fast equality lookups but don't support range queries or sorting.

### Hash Index Features:
- **Fast Equality**: O(1) average case for = operations
- **No Range Queries**: Cannot use <, >, BETWEEN
- **No Sorting**: Results not in sorted order
- **Memory Usage**: Can be memory-intensive
- **Collision Handling**: Uses chaining for hash collisions

### Hash Index Use Cases:
- **Exact Matches**: Primary key lookups
- **Lookup Tables**: Reference data lookups
- **High-Cardinality**: Columns with many unique values
- **Frequent Equality**: Columns frequently used with = operator

### Real-World Analogy:
Hash indexes are like a hash table or dictionary:
- **Fast Equality** = Instant word lookup in dictionary
- **No Range Queries** = Cannot find words between two letters
- **No Sorting** = Words not in alphabetical order
- **Memory Usage** = Requires space for hash table
- **Collision Handling** = Multiple words with same hash

### SQL Example - Hash Indexes:
```sql
-- Create table for hash index demonstration
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE,
    email VARCHAR(100) UNIQUE,
    phone VARCHAR(20),
    status VARCHAR(20) DEFAULT 'active'
);

INSERT INTO users (username, email, phone, status) VALUES
    ('jdoe', 'john.doe@example.com', '+1234567890', 'active'),
    ('asmith', 'alice.smith@example.com', '+1987654321', 'active'),
    ('bwilson', 'bob.wilson@example.com', '+1555123456', 'inactive'),
    ('cbrown', 'carol.brown@example.com', '+1555987654', 'active');

-- Create hash index on username
CREATE INDEX idx_users_username_hash ON users USING HASH (username);

-- Create hash index on email
CREATE INDEX idx_users_email_hash ON users USING HASH (email);

-- Equality queries using hash indexes
EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM users 
WHERE username = 'jdoe';

EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM users 
WHERE email = 'alice.smith@example.com';

-- Hash index cannot be used for range queries
EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM users 
WHERE username > 'jdoe';

-- Hash index cannot be used for sorting
EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM users 
ORDER BY username;

-- Compare hash vs B-tree for equality
CREATE INDEX idx_users_username_btree ON users(username);

-- Test both index types
EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM users 
WHERE username = 'jdoe';

-- Drop B-tree index to test hash only
DROP INDEX idx_users_username_btree;

EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM users 
WHERE username = 'jdoe';
```

## 5.4 GIN (Generalized Inverted Index)

GIN indexes are designed for complex data types like arrays, JSON, and full-text search.

### GIN Index Features:
- **Complex Data Types**: Arrays, JSON, text search vectors
- **Multiple Values**: Each row can have multiple index entries
- **Full-Text Search**: Optimized for text search operations
- **JSON Queries**: Efficient JSON path queries
- **Array Operations**: Fast array containment queries

### GIN Use Cases:
- **Full-Text Search**: Text search vectors
- **JSON Data**: JSONB columns with path queries
- **Array Columns**: Array containment and overlap
- **Composite Types**: Complex data type queries
- **Custom Operators**: User-defined operators

### Real-World Analogy:
GIN indexes are like a comprehensive subject index:
- **Complex Data Types** = Indexing different types of content
- **Multiple Values** = One book can be in multiple categories
- **Full-Text Search** = Finding books by content, not just title
- **JSON Queries** = Finding books by specific metadata
- **Array Operations** = Finding books with specific tags

### SQL Example - GIN Indexes:
```sql
-- Create table with complex data types
CREATE TABLE documents (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200),
    content TEXT,
    tags TEXT[],
    metadata JSONB,
    search_vector tsvector
);

INSERT INTO documents (title, content, tags, metadata, search_vector) VALUES
    ('PostgreSQL Guide', 'PostgreSQL is a powerful database system', 
     ARRAY['database', 'postgresql', 'sql'], 
     '{"author": "John Doe", "version": "1.0", "category": "technical"}',
     to_tsvector('english', 'PostgreSQL is a powerful database system')),
    ('SQL Tutorial', 'Learn SQL with practical examples', 
     ARRAY['sql', 'tutorial', 'learning'], 
     '{"author": "Alice Smith", "version": "2.0", "category": "educational"}',
     to_tsvector('english', 'Learn SQL with practical examples')),
    ('Database Design', 'Designing efficient database schemas', 
     ARRAY['database', 'design', 'schema'], 
     '{"author": "Bob Wilson", "version": "1.5", "category": "technical"}',
     to_tsvector('english', 'Designing efficient database schemas'));

-- Create GIN index on array column
CREATE INDEX idx_documents_tags_gin ON documents USING GIN (tags);

-- Create GIN index on JSONB column
CREATE INDEX idx_documents_metadata_gin ON documents USING GIN (metadata);

-- Create GIN index on text search vector
CREATE INDEX idx_documents_search_gin ON documents USING GIN (search_vector);

-- Array containment queries
EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM documents 
WHERE tags @> ARRAY['database'];

-- Array overlap queries
EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM documents 
WHERE tags && ARRAY['sql', 'tutorial'];

-- JSON path queries
EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM documents 
WHERE metadata @> '{"category": "technical"}';

-- JSON key existence
EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM documents 
WHERE metadata ? 'author';

-- Full-text search
EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM documents 
WHERE search_vector @@ to_tsquery('english', 'database & design');

-- Complex JSON queries
EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM documents 
WHERE metadata @> '{"author": "John Doe"}' 
AND tags @> ARRAY['database'];
```

## 5.5 GiST (Generalized Search Tree)

GiST indexes are designed for geometric data and custom data types that don't fit well into B-tree or hash indexes.

### GiST Index Features:
- **Geometric Data**: Points, lines, polygons, circles
- **Custom Data Types**: User-defined types with custom operators
- **Spatial Queries**: Distance, containment, intersection
- **Extensible**: Can be extended for new data types
- **Balanced Tree**: Self-balancing tree structure

### GiST Use Cases:
- **Geometric Data**: PostGIS spatial data
- **Range Types**: Date ranges, numeric ranges
- **Custom Types**: User-defined data types
- **Spatial Queries**: Geographic information systems
- **Text Search**: Some text search operations

### Real-World Analogy:
GiST indexes are like a spatial map system:
- **Geometric Data** = Locations on a map
- **Custom Data Types** = Different types of map features
- **Spatial Queries** = Finding nearby locations
- **Extensible** = Can add new types of map features
- **Balanced Tree** = Organized map sections

### SQL Example - GiST Indexes:
```sql
-- Enable PostGIS extension (if available)
-- CREATE EXTENSION IF NOT EXISTS postgis;

-- Create table with geometric data
CREATE TABLE locations (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    point POINT,
    polygon POLYGON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert sample geometric data
INSERT INTO locations (name, point, polygon) VALUES
    ('Central Park', POINT(-73.965355, 40.782865), 
     POLYGON((-73.973, 40.764, -73.973, 40.800, -73.958, 40.800, -73.958, 40.764, -73.973, 40.764))),
    ('Times Square', POINT(-73.985130, 40.758896), 
     POLYGON((-73.990, 40.755, -73.990, 40.762, -73.980, 40.762, -73.980, 40.755, -73.990, 40.755))),
    ('Brooklyn Bridge', POINT(-73.996315, 40.706086), 
     POLYGON((-74.000, 40.704, -74.000, 40.708, -73.993, 40.708, -73.993, 40.704, -74.000, 40.704)));

-- Create GiST index on point column
CREATE INDEX idx_locations_point_gist ON locations USING GIST (point);

-- Create GiST index on polygon column
CREATE INDEX idx_locations_polygon_gist ON locations USING GIST (polygon);

-- Spatial queries using GiST indexes
EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM locations 
WHERE point <-> POINT(-73.985130, 40.758896) < 0.01;

-- Containment queries
EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM locations 
WHERE polygon @> POINT(-73.985130, 40.758896);

-- Intersection queries
EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM locations 
WHERE polygon && POLYGON((-74.000, 40.700, -74.000, 40.800, -73.950, 40.800, -73.950, 40.700, -74.000, 40.700));

-- Range type example
CREATE TABLE events (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    duration TSRANGE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO events (name, duration) VALUES
    ('Meeting', '[2024-01-15 09:00, 2024-01-15 10:00]'),
    ('Lunch', '[2024-01-15 12:00, 2024-01-15 13:00]'),
    ('Conference', '[2024-01-15 14:00, 2024-01-15 17:00]');

-- Create GiST index on range type
CREATE INDEX idx_events_duration_gist ON events USING GIST (duration);

-- Range queries
EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM events 
WHERE duration @> TIMESTAMP '2024-01-15 09:30';

-- Range overlap
EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM events 
WHERE duration && TSRANGE('[2024-01-15 08:00, 2024-01-15 11:00]');
```

## 5.6 SP-GiST (Space-Partitioned GiST)

SP-GiST indexes are designed for data that can be partitioned into non-overlapping regions.

### SP-GiST Features:
- **Space Partitioning**: Non-overlapping regions
- **Balanced Tree**: Self-balancing structure
- **Custom Partitioning**: User-defined partitioning schemes
- **Efficient Lookups**: Fast point and range queries
- **Extensible**: Can be extended for new data types

### SP-GiST Use Cases:
- **Quad Trees**: 2D spatial partitioning
- **KD Trees**: Multi-dimensional data
- **Tries**: String prefix trees
- **Custom Types**: User-defined partitioning
- **Spatial Data**: Some geometric operations

### Real-World Analogy:
SP-GiST indexes are like a hierarchical map system:
- **Space Partitioning** = Dividing map into non-overlapping regions
- **Balanced Tree** = Equal-sized map sections
- **Custom Partitioning** = Different ways to divide the map
- **Efficient Lookups** = Quick navigation to specific areas
- **Extensible** = Can add new types of map divisions

### SQL Example - SP-GiST Indexes:
```sql
-- Create table with data suitable for SP-GiST
CREATE TABLE spatial_data (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    point POINT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO spatial_data (name, point) VALUES
    ('Location 1', POINT(0.1, 0.1)),
    ('Location 2', POINT(0.3, 0.3)),
    ('Location 3', POINT(0.7, 0.7)),
    ('Location 4', POINT(0.9, 0.9)),
    ('Location 5', POINT(0.5, 0.5));

-- Create SP-GiST index on point column
CREATE INDEX idx_spatial_data_point_spgist ON spatial_data USING SPGIST (point);

-- Point queries using SP-GiST
EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM spatial_data 
WHERE point <-> POINT(0.5, 0.5) < 0.1;

-- Range queries
EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM spatial_data 
WHERE point <@ BOX(POINT(0.0, 0.0), POINT(0.5, 0.5));

-- Text data with SP-GiST (using text_ops)
CREATE TABLE text_data (
    id SERIAL PRIMARY KEY,
    text_value VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO text_data (text_value) VALUES
    ('apple'),
    ('application'),
    ('apply'),
    ('banana'),
    ('band'),
    ('bandana');

-- Create SP-GiST index on text column
CREATE INDEX idx_text_data_text_spgist ON text_data USING SPGIST (text_value text_ops);

-- Prefix queries
EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM text_data 
WHERE text_value LIKE 'app%';

-- Pattern queries
EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM text_data 
WHERE text_value ~ '^ban.*';
```

## 5.7 BRIN (Block Range Indexes)

BRIN indexes are designed for very large tables where traditional indexes would be too large.

### BRIN Features:
- **Block-Level**: Indexes at the block level, not row level
- **Small Size**: Much smaller than traditional indexes
- **Large Tables**: Designed for tables with millions/billions of rows
- **Correlated Data**: Works best with naturally ordered data
- **Maintenance**: Requires periodic maintenance

### BRIN Use Cases:
- **Time Series Data**: Logs, metrics, sensor data
- **Large Tables**: Tables too large for traditional indexes
- **Correlated Data**: Data that's naturally ordered
- **Append-Only**: Tables that are mostly append-only
- **Storage Constraints**: When index size is a concern

### Real-World Analogy:
BRIN indexes are like a table of contents for a very large book:
- **Block-Level** = Indexing chapters, not individual pages
- **Small Size** = Much smaller than a full index
- **Large Tables** = Designed for very large books
- **Correlated Data** = Works best with organized content
- **Maintenance** = Needs periodic updates

### SQL Example - BRIN Indexes:
```sql
-- Create large table with time series data
CREATE TABLE sensor_readings (
    id BIGSERIAL PRIMARY KEY,
    sensor_id INTEGER,
    reading_time TIMESTAMP,
    temperature NUMERIC(5,2),
    humidity NUMERIC(5,2),
    pressure NUMERIC(8,2)
);

-- Insert sample time series data
INSERT INTO sensor_readings (sensor_id, reading_time, temperature, humidity, pressure)
SELECT 
    (random() * 100)::INTEGER,
    '2024-01-01'::TIMESTAMP + (i * INTERVAL '1 minute'),
    (random() * 40 + 10)::NUMERIC(5,2),
    (random() * 100)::NUMERIC(5,2),
    (random() * 1000 + 900)::NUMERIC(8,2)
FROM generate_series(1, 10000) i;

-- Create BRIN index on time column
CREATE INDEX idx_sensor_readings_time_brin ON sensor_readings USING BRIN (reading_time);

-- Create BRIN index on sensor_id column
CREATE INDEX idx_sensor_readings_sensor_brin ON sensor_readings USING BRIN (sensor_id);

-- Time range queries using BRIN
EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM sensor_readings 
WHERE reading_time BETWEEN '2024-01-01 10:00:00' AND '2024-01-01 11:00:00';

-- Sensor queries
EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM sensor_readings 
WHERE sensor_id = 50;

-- BRIN with custom pages_per_range
CREATE INDEX idx_sensor_readings_temp_brin ON sensor_readings USING BRIN (temperature) 
WITH (pages_per_range = 4);

-- Temperature range queries
EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM sensor_readings 
WHERE temperature BETWEEN 20.0 AND 30.0;

-- Check BRIN index statistics
SELECT 
    schemaname,
    tablename,
    indexname,
    pages_per_range,
    relpages,
    reltuples
FROM pg_stat_user_indexes 
JOIN pg_class ON pg_stat_user_indexes.indexrelid = pg_class.oid
WHERE indexname LIKE '%brin%';
```

## 5.8 Partial Indexes

Partial indexes include only a subset of rows from a table, making them smaller and more efficient for specific queries.

### Partial Index Features:
- **Conditional**: Only index rows that meet a condition
- **Smaller Size**: Significantly smaller than full indexes
- **Faster Maintenance**: Less data to maintain
- **Query Optimization**: Only used when condition matches
- **Storage Efficiency**: Saves disk space

### Partial Index Use Cases:
- **Active Records**: Only index active/current records
- **High-Value Data**: Only index important or frequently queried data
- **Filtered Queries**: Queries that always include a condition
- **Sparse Data**: Columns with many NULL values
- **Performance**: Improve performance for specific query patterns

### Real-World Analogy:
Partial indexes are like specialized catalogs:
- **Conditional** = Only cataloging certain types of items
- **Smaller Size** = Much smaller than a complete catalog
- **Faster Maintenance** = Easier to keep up to date
- **Query Optimization** = Only used for specific searches
- **Storage Efficiency** = Takes up less space

### SQL Example - Partial Indexes:
```sql
-- Create table with status column
CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    customer_id INTEGER,
    order_date DATE,
    total_amount NUMERIC(10,2),
    status VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO orders (customer_id, order_date, total_amount, status) VALUES
    (1, '2024-01-15', 150.00, 'completed'),
    (2, '2024-01-16', 299.99, 'pending'),
    (3, '2024-01-17', 75.50, 'completed'),
    (4, '2024-01-18', 200.00, 'shipped'),
    (5, '2024-01-19', 450.00, 'completed'),
    (6, '2024-01-20', 100.00, 'cancelled'),
    (7, '2024-01-21', 300.00, 'pending'),
    (8, '2024-01-22', 250.00, 'completed');

-- Create partial index for active orders only
CREATE INDEX idx_orders_active ON orders(customer_id, order_date) 
WHERE status IN ('pending', 'shipped');

-- Create partial index for high-value orders
CREATE INDEX idx_orders_high_value ON orders(customer_id, total_amount) 
WHERE total_amount > 200;

-- Create partial index for recent orders
CREATE INDEX idx_orders_recent ON orders(customer_id, order_date) 
WHERE order_date >= CURRENT_DATE - INTERVAL '30 days';

-- Queries that can use partial indexes
EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM orders 
WHERE status IN ('pending', 'shipped') 
AND customer_id = 2;

EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM orders 
WHERE total_amount > 200 
AND customer_id = 5;

EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM orders 
WHERE order_date >= CURRENT_DATE - INTERVAL '30 days' 
AND customer_id = 1;

-- Queries that cannot use partial indexes
EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM orders 
WHERE status = 'completed' 
AND customer_id = 1;

-- Check index usage
SELECT 
    schemaname,
    tablename,
    indexname,
    idx_scan,
    idx_tup_read,
    idx_tup_fetch
FROM pg_stat_user_indexes 
WHERE tablename = 'orders';
```

## 5.9 Expression Indexes

Expression indexes are built on expressions rather than just column values, enabling efficient queries on computed values.

### Expression Index Features:
- **Computed Values**: Index on expressions, not just columns
- **Function Results**: Index on function outputs
- **Mathematical Operations**: Index on calculated values
- **String Operations**: Index on string manipulations
- **Performance**: Fast queries on computed values

### Expression Index Use Cases:
- **Computed Columns**: Frequently queried calculated values
- **Function Results**: Queries on function outputs
- **String Operations**: Case-insensitive searches
- **Mathematical Operations**: Range queries on calculations
- **Date Operations**: Queries on date parts

### Real-World Analogy:
Expression indexes are like pre-calculated reference tables:
- **Computed Values** = Pre-calculated results for quick lookup
- **Function Results** = Pre-computed function outputs
- **Mathematical Operations** = Pre-calculated math results
- **String Operations** = Pre-processed text for searching
- **Performance** = Instant lookup instead of calculation

### SQL Example - Expression Indexes:
```sql
-- Create table with data for expression indexes
CREATE TABLE employees (
    emp_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(100),
    salary NUMERIC(10,2),
    hire_date DATE,
    email VARCHAR(100)
);

INSERT INTO employees (first_name, last_name, salary, hire_date, email) VALUES
    ('John', 'Doe', 75000.00, '2020-01-15', 'john.doe@company.com'),
    ('Alice', 'Smith', 80000.00, '2019-06-20', 'alice.smith@company.com'),
    ('Bob', 'Wilson', 70000.00, '2021-03-10', 'bob.wilson@company.com'),
    ('Carol', 'Brown', 85000.00, '2018-11-05', 'carol.brown@company.com'),
    ('David', 'Lee', 72000.00, '2022-02-28', 'david.lee@company.com');

-- Create expression index on full name
CREATE INDEX idx_employees_full_name ON employees((first_name || ' ' || last_name));

-- Create expression index on case-insensitive name
CREATE INDEX idx_employees_name_lower ON employees(LOWER(first_name || ' ' || last_name));

-- Create expression index on salary with tax calculation
CREATE INDEX idx_employees_net_salary ON employees((salary * 0.85));

-- Create expression index on hire year
CREATE INDEX idx_employees_hire_year ON employees(EXTRACT(YEAR FROM hire_date));

-- Create expression index on email domain
CREATE INDEX idx_employees_email_domain ON employees(SUBSTRING(email FROM '@(.*)$'));

-- Queries using expression indexes
EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM employees 
WHERE first_name || ' ' || last_name = 'John Doe';

EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM employees 
WHERE LOWER(first_name || ' ' || last_name) = 'alice smith';

EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM employees 
WHERE salary * 0.85 > 60000;

EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM employees 
WHERE EXTRACT(YEAR FROM hire_date) = 2020;

EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM employees 
WHERE SUBSTRING(email FROM '@(.*)$') = 'company.com';

-- Complex expression index
CREATE INDEX idx_employees_salary_hire ON employees((salary / EXTRACT(YEAR FROM CURRENT_DATE) - EXTRACT(YEAR FROM hire_date)));

-- Query using complex expression
EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM employees 
WHERE (salary / (EXTRACT(YEAR FROM CURRENT_DATE) - EXTRACT(YEAR FROM hire_date))) > 15000;
```

## 5.10 Index Maintenance and Optimization

Index maintenance involves monitoring, analyzing, and optimizing indexes to ensure optimal performance.

### Index Maintenance Tasks:
- **Statistics Updates**: Keep index statistics current
- **Index Rebuilding**: Rebuild fragmented indexes
- **Index Analysis**: Analyze index usage and effectiveness
- **Index Cleanup**: Remove unused or redundant indexes
- **Index Monitoring**: Track index performance metrics

### Maintenance Tools:
- **ANALYZE**: Update table and index statistics
- **REINDEX**: Rebuild indexes
- **pg_stat_user_indexes**: Monitor index usage
- **pg_stat_user_tables**: Monitor table statistics
- **EXPLAIN**: Analyze query execution plans

### Real-World Analogy:
Index maintenance is like maintaining a library catalog:
- **Statistics Updates** = Keeping catalog information current
- **Index Rebuilding** = Reorganizing the catalog for efficiency
- **Index Analysis** = Reviewing which parts of catalog are used
- **Index Cleanup** = Removing outdated catalog entries
- **Index Monitoring** = Tracking catalog usage patterns

### SQL Example - Index Maintenance:
```sql
-- Create table with indexes
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    category VARCHAR(50),
    price NUMERIC(10,2),
    stock_quantity INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create various indexes
CREATE INDEX idx_products_name ON products(name);
CREATE INDEX idx_products_category ON products(category);
CREATE INDEX idx_products_price ON products(price);
CREATE INDEX idx_products_stock ON products(stock_quantity) WHERE stock_quantity > 0;

-- Insert sample data
INSERT INTO products (name, category, price, stock_quantity)
SELECT 
    'Product ' || i,
    CASE (i % 4) 
        WHEN 0 THEN 'Electronics'
        WHEN 1 THEN 'Books'
        WHEN 2 THEN 'Clothing'
        ELSE 'Home'
    END,
    (random() * 1000 + 10)::NUMERIC(10,2),
    (random() * 100)::INTEGER
FROM generate_series(1, 10000) i;

-- Update table statistics
ANALYZE products;

-- Check index statistics
SELECT 
    schemaname,
    tablename,
    indexname,
    idx_scan,
    idx_tup_read,
    idx_tup_fetch,
    idx_blks_read,
    idx_blks_hit
FROM pg_stat_user_indexes 
WHERE tablename = 'products'
ORDER BY idx_scan DESC;

-- Check table statistics
SELECT 
    schemaname,
    tablename,
    n_tup_ins,
    n_tup_upd,
    n_tup_del,
    n_live_tup,
    n_dead_tup,
    last_vacuum,
    last_autovacuum,
    last_analyze,
    last_autoanalyze
FROM pg_stat_user_tables 
WHERE tablename = 'products';

-- Rebuild specific index
REINDEX INDEX idx_products_name;

-- Rebuild all indexes on table
REINDEX TABLE products;

-- Check index size
SELECT 
    schemaname,
    tablename,
    indexname,
    pg_size_pretty(pg_relation_size(indexname::regclass)) as index_size,
    pg_size_pretty(pg_relation_size(tablename::regclass)) as table_size
FROM pg_indexes 
WHERE tablename = 'products'
ORDER BY pg_relation_size(indexname::regclass) DESC;

-- Find unused indexes
SELECT 
    schemaname,
    tablename,
    indexname,
    idx_scan,
    pg_size_pretty(pg_relation_size(indexname::regclass)) as index_size
FROM pg_stat_user_indexes 
WHERE idx_scan = 0
ORDER BY pg_relation_size(indexname::regclass) DESC;

-- Check index bloat
SELECT 
    schemaname,
    tablename,
    indexname,
    pg_size_pretty(pg_relation_size(indexname::regclass)) as index_size,
    pg_size_pretty(pg_stat_get_tuples_fetched(indexname::regclass)) as tuples_fetched
FROM pg_indexes 
WHERE tablename = 'products'
ORDER BY pg_relation_size(indexname::regclass) DESC;
```