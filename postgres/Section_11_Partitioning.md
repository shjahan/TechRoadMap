# Section 11 – Partitioning

## 11.1 Table Partitioning Concepts

Table partitioning divides large tables into smaller, manageable pieces called partitions.

### Partitioning Benefits:
- **Performance**: Faster queries on smaller partitions
- **Maintenance**: Easier maintenance of individual partitions
- **Scalability**: Better performance as data grows
- **Storage**: Efficient storage management
- **Parallelism**: Parallel operations on partitions

### Real-World Analogy:
Table partitioning is like organizing a large library:
- **Performance** = Faster book finding in smaller sections
- **Maintenance** = Easier to maintain individual sections
- **Scalability** = Better organization as library grows
- **Storage** = Efficient use of shelf space
- **Parallelism** = Multiple librarians can work simultaneously

### SQL Example - Partitioning Concepts:
```sql
-- Create partitioned table
CREATE TABLE sales (
    id SERIAL,
    sale_date DATE,
    product_id INTEGER,
    amount NUMERIC(10,2),
    region VARCHAR(50)
) PARTITION BY RANGE (sale_date);

-- Create partitions
CREATE TABLE sales_2024_q1 PARTITION OF sales
    FOR VALUES FROM ('2024-01-01') TO ('2024-04-01');

CREATE TABLE sales_2024_q2 PARTITION OF sales
    FOR VALUES FROM ('2024-04-01') TO ('2024-07-01');

CREATE TABLE sales_2024_q3 PARTITION OF sales
    FOR VALUES FROM ('2024-07-01') TO ('2024-10-01');

CREATE TABLE sales_2024_q4 PARTITION OF sales
    FOR VALUES FROM ('2024-10-01') TO ('2025-01-01');

-- Insert sample data
INSERT INTO sales (sale_date, product_id, amount, region) VALUES
    ('2024-01-15', 1, 100.00, 'North'),
    ('2024-02-20', 2, 200.00, 'South'),
    ('2024-05-10', 3, 150.00, 'East'),
    ('2024-08-25', 4, 300.00, 'West');

-- Query partitioned table
SELECT * FROM sales WHERE sale_date >= '2024-01-01' AND sale_date < '2024-04-01';

-- Check partition information
SELECT 
    schemaname,
    tablename,
    partitionname,
    partitionbounddef
FROM pg_partitions
WHERE tablename = 'sales'
ORDER BY partitionname;
```

## 11.2 Range Partitioning

Range partitioning divides data based on ranges of values.

### Range Partitioning Features:
- **Range Boundaries**: Define start and end values
- **Overlapping**: Ranges cannot overlap
- **Gaps**: Gaps between ranges are allowed
- **Default Partition**: Handle values outside ranges
- **Automatic Partitioning**: Create partitions automatically

### Real-World Analogy:
Range partitioning is like organizing books by publication year:
- **Range Boundaries** = Year ranges (2020-2025)
- **Overlapping** = No year can be in multiple ranges
- **Gaps** = Missing years are allowed
- **Default Partition** = Books with unknown years
- **Automatic Partitioning** = Auto-creating new year sections

### SQL Example - Range Partitioning:
```sql
-- Create range partitioned table
CREATE TABLE orders (
    order_id SERIAL,
    order_date DATE,
    customer_id INTEGER,
    total_amount NUMERIC(10,2),
    status VARCHAR(20)
) PARTITION BY RANGE (order_date);

-- Create monthly partitions
CREATE TABLE orders_2024_01 PARTITION OF orders
    FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');

CREATE TABLE orders_2024_02 PARTITION OF orders
    FOR VALUES FROM ('2024-02-01') TO ('2024-03-01');

CREATE TABLE orders_2024_03 PARTITION OF orders
    FOR VALUES FROM ('2024-03-01') TO ('2024-04-01');

-- Create default partition
CREATE TABLE orders_default PARTITION OF orders DEFAULT;

-- Insert sample data
INSERT INTO orders (order_date, customer_id, total_amount, status) VALUES
    ('2024-01-15', 1, 150.00, 'completed'),
    ('2024-02-20', 2, 200.00, 'pending'),
    ('2024-03-10', 3, 175.00, 'shipped'),
    ('2024-12-25', 4, 300.00, 'completed');

-- Query specific partition
SELECT * FROM orders_2024_01;

-- Query across partitions
SELECT 
    order_date,
    COUNT(*) as order_count,
    SUM(total_amount) as total_amount
FROM orders
WHERE order_date >= '2024-01-01' AND order_date < '2024-04-01'
GROUP BY order_date
ORDER BY order_date;

-- Check partition pruning
EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM orders WHERE order_date = '2024-01-15';
```

## 11.3 List Partitioning

List partitioning divides data based on specific values.

### List Partitioning Features:
- **Value Lists**: Define specific values for each partition
- **No Overlap**: Values cannot appear in multiple partitions
- **Default Partition**: Handle values not in any list
- **Multiple Columns**: Partition by multiple columns
- **Flexible Values**: Any data type can be used

### Real-World Analogy:
List partitioning is like organizing books by genre:
- **Value Lists** = Specific genres (Fiction, Non-fiction, Science)
- **No Overlap** = Each book belongs to one genre
- **Default Partition** = Books with unknown genres
- **Multiple Columns** = Genre and subgenre
- **Flexible Values** = Any genre name

### SQL Example - List Partitioning:
```sql
-- Create list partitioned table
CREATE TABLE products (
    product_id SERIAL,
    name VARCHAR(100),
    category VARCHAR(50),
    price NUMERIC(10,2),
    region VARCHAR(50)
) PARTITION BY LIST (category);

-- Create category partitions
CREATE TABLE products_electronics PARTITION OF products
    FOR VALUES IN ('Electronics', 'Computers', 'Mobile');

CREATE TABLE products_books PARTITION OF products
    FOR VALUES IN ('Books', 'Education', 'Reference');

CREATE TABLE products_clothing PARTITION OF products
    FOR VALUES IN ('Clothing', 'Shoes', 'Accessories');

-- Create default partition
CREATE TABLE products_default PARTITION OF products DEFAULT;

-- Insert sample data
INSERT INTO products (name, category, price, region) VALUES
    ('Laptop', 'Electronics', 999.99, 'North'),
    ('Programming Book', 'Books', 49.99, 'South'),
    ('T-Shirt', 'Clothing', 19.99, 'East'),
    ('Unknown Item', 'Unknown', 10.00, 'West');

-- Query specific partition
SELECT * FROM products_electronics;

-- Query across partitions
SELECT 
    category,
    COUNT(*) as product_count,
    AVG(price) as avg_price
FROM products
GROUP BY category
ORDER BY category;

-- Check partition pruning
EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM products WHERE category = 'Electronics';
```

## 11.4 Hash Partitioning

Hash partitioning divides data based on hash values of the partition key.

### Hash Partitioning Features:
- **Hash Function**: Uses hash function to distribute data
- **Even Distribution**: Data is evenly distributed across partitions
- **No Gaps**: All hash values are covered
- **Fixed Partitions**: Number of partitions is fixed
- **Random Distribution**: Data distribution is random

### Real-World Analogy:
Hash partitioning is like randomly distributing books across shelves:
- **Hash Function** = Random distribution algorithm
- **Even Distribution** = Equal number of books per shelf
- **No Gaps** = All shelves are used
- **Fixed Partitions** = Fixed number of shelves
- **Random Distribution** = Books are randomly placed

### SQL Example - Hash Partitioning:
```sql
-- Create hash partitioned table
CREATE TABLE users (
    user_id SERIAL,
    username VARCHAR(50),
    email VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) PARTITION BY HASH (user_id);

-- Create hash partitions
CREATE TABLE users_0 PARTITION OF users
    FOR VALUES WITH (modulus 4, remainder 0);

CREATE TABLE users_1 PARTITION OF users
    FOR VALUES WITH (modulus 4, remainder 1);

CREATE TABLE users_2 PARTITION OF users
    FOR VALUES WITH (modulus 4, remainder 2);

CREATE TABLE users_3 PARTITION OF users
    FOR VALUES WITH (modulus 4, remainder 3);

-- Insert sample data
INSERT INTO users (username, email) VALUES
    ('user1', 'user1@example.com'),
    ('user2', 'user2@example.com'),
    ('user3', 'user3@example.com'),
    ('user4', 'user4@example.com'),
    ('user5', 'user5@example.com');

-- Query specific partition
SELECT * FROM users_0;

-- Query across partitions
SELECT 
    COUNT(*) as total_users,
    COUNT(*) FILTER (WHERE username LIKE 'user%') as user_count
FROM users;

-- Check data distribution
SELECT 
    'users_0' as partition,
    COUNT(*) as row_count
FROM users_0
UNION ALL
SELECT 
    'users_1',
    COUNT(*)
FROM users_1
UNION ALL
SELECT 
    'users_2',
    COUNT(*)
FROM users_2
UNION ALL
SELECT 
    'users_3',
    COUNT(*)
FROM users_3;
```

## 11.5 Composite Partitioning

Composite partitioning combines multiple partitioning methods.

### Composite Partitioning Features:
- **Multiple Levels**: Partition by multiple criteria
- **Flexible Combinations**: Any combination of partitioning methods
- **Hierarchical Structure**: Tree-like partition structure
- **Complex Queries**: Support for complex query patterns
- **Performance**: Optimized for specific access patterns

### Real-World Analogy:
Composite partitioning is like organizing a library by multiple criteria:
- **Multiple Levels** = First by genre, then by year
- **Flexible Combinations** = Any combination of criteria
- **Hierarchical Structure** = Tree-like organization
- **Complex Queries** = Finding books by multiple criteria
- **Performance** = Optimized for specific searches

### SQL Example - Composite Partitioning:
```sql
-- Create composite partitioned table
CREATE TABLE sales_composite (
    id SERIAL,
    sale_date DATE,
    region VARCHAR(50),
    product_id INTEGER,
    amount NUMERIC(10,2)
) PARTITION BY RANGE (sale_date);

-- Create range partitions
CREATE TABLE sales_2024 PARTITION OF sales_composite
    FOR VALUES FROM ('2024-01-01') TO ('2025-01-01')
    PARTITION BY LIST (region);

CREATE TABLE sales_2025 PARTITION OF sales_composite
    FOR VALUES FROM ('2025-01-01') TO ('2026-01-01')
    PARTITION BY LIST (region);

-- Create list partitions for 2024
CREATE TABLE sales_2024_north PARTITION OF sales_2024
    FOR VALUES IN ('North', 'Northeast');

CREATE TABLE sales_2024_south PARTITION OF sales_2024
    FOR VALUES IN ('South', 'Southeast');

CREATE TABLE sales_2024_west PARTITION OF sales_2024
    FOR VALUES IN ('West', 'Southwest');

-- Create list partitions for 2025
CREATE TABLE sales_2025_north PARTITION OF sales_2025
    FOR VALUES IN ('North', 'Northeast');

CREATE TABLE sales_2025_south PARTITION OF sales_2025
    FOR VALUES IN ('South', 'Southeast');

CREATE TABLE sales_2025_west PARTITION OF sales_2025
    FOR VALUES IN ('West', 'Southwest');

-- Insert sample data
INSERT INTO sales_composite (sale_date, region, product_id, amount) VALUES
    ('2024-01-15', 'North', 1, 100.00),
    ('2024-02-20', 'South', 2, 200.00),
    ('2024-03-10', 'West', 3, 150.00),
    ('2025-01-15', 'North', 4, 300.00);

-- Query specific partition
SELECT * FROM sales_2024_north;

-- Query across partitions
SELECT 
    region,
    COUNT(*) as sale_count,
    SUM(amount) as total_amount
FROM sales_composite
WHERE sale_date >= '2024-01-01' AND sale_date < '2025-01-01'
GROUP BY region
ORDER BY region;

-- Check partition hierarchy
SELECT 
    schemaname,
    tablename,
    partitionname,
    partitionbounddef
FROM pg_partitions
WHERE tablename = 'sales_composite'
ORDER BY partitionname;
```

## 11.6 Partition Pruning

Partition pruning automatically eliminates partitions that cannot contain matching rows.

### Partition Pruning Features:
- **Automatic**: Happens automatically during query planning
- **Predicate Analysis**: Analyzes WHERE clauses
- **Index Usage**: Uses partition indexes
- **Statistics**: Uses partition statistics
- **Performance**: Significantly improves query performance

### Real-World Analogy:
Partition pruning is like a smart librarian:
- **Automatic** = Automatically skips irrelevant sections
- **Predicate Analysis** = Understands what you're looking for
- **Index Usage** = Uses section indexes
- **Statistics** = Knows what's in each section
- **Performance** = Much faster book finding

### SQL Example - Partition Pruning:
```sql
-- Create partitioned table with indexes
CREATE TABLE orders_pruning (
    order_id SERIAL,
    order_date DATE,
    customer_id INTEGER,
    total_amount NUMERIC(10,2),
    status VARCHAR(20)
) PARTITION BY RANGE (order_date);

-- Create partitions
CREATE TABLE orders_2024_q1 PARTITION OF orders_pruning
    FOR VALUES FROM ('2024-01-01') TO ('2024-04-01');

CREATE TABLE orders_2024_q2 PARTITION OF orders_pruning
    FOR VALUES FROM ('2024-04-01') TO ('2024-07-01');

CREATE TABLE orders_2024_q3 PARTITION OF orders_pruning
    FOR VALUES FROM ('2024-07-01') TO ('2024-10-01');

CREATE TABLE orders_2024_q4 PARTITION OF orders_pruning
    FOR VALUES FROM ('2024-10-01') TO ('2025-01-01');

-- Create indexes on partitions
CREATE INDEX idx_orders_2024_q1_date ON orders_2024_q1 (order_date);
CREATE INDEX idx_orders_2024_q2_date ON orders_2024_q2 (order_date);
CREATE INDEX idx_orders_2024_q3_date ON orders_2024_q3 (order_date);
CREATE INDEX idx_orders_2024_q4_date ON orders_2024_q4 (order_date);

-- Insert sample data
INSERT INTO orders_pruning (order_date, customer_id, total_amount, status) VALUES
    ('2024-01-15', 1, 150.00, 'completed'),
    ('2024-02-20', 2, 200.00, 'pending'),
    ('2024-05-10', 3, 175.00, 'shipped'),
    ('2024-08-25', 4, 300.00, 'completed');

-- Check partition pruning
EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM orders_pruning WHERE order_date = '2024-01-15';

-- Check partition pruning with range
EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM orders_pruning 
WHERE order_date >= '2024-01-01' AND order_date < '2024-04-01';

-- Check partition pruning with multiple conditions
EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM orders_pruning 
WHERE order_date >= '2024-01-01' 
AND order_date < '2024-04-01'
AND status = 'completed';

-- Check partition pruning statistics
SELECT 
    schemaname,
    tablename,
    partitionname,
    n_tup_ins,
    n_tup_upd,
    n_tup_del,
    n_live_tup,
    n_dead_tup
FROM pg_stat_user_tables
WHERE tablename LIKE 'orders_2024_%'
ORDER BY partitionname;
```

## 11.7 Partition-wise Joins

Partition-wise joins optimize joins between partitioned tables.

### Partition-wise Join Features:
- **Automatic**: Happens automatically when possible
- **Parallel Execution**: Joins partitions in parallel
- **Memory Efficiency**: Reduces memory usage
- **Performance**: Significantly improves join performance
- **Compatibility**: Works with different partitioning methods

### Real-World Analogy:
Partition-wise joins are like having multiple librarians work in parallel:
- **Automatic** = Automatically assigns work to librarians
- **Parallel Execution** = Multiple librarians work simultaneously
- **Memory Efficiency** = Each librarian works with smaller sections
- **Performance** = Much faster book finding
- **Compatibility** = Works with different organization methods

### SQL Example - Partition-wise Joins:
```sql
-- Create partitioned tables
CREATE TABLE orders_partitioned (
    order_id SERIAL,
    order_date DATE,
    customer_id INTEGER,
    total_amount NUMERIC(10,2)
) PARTITION BY RANGE (order_date);

CREATE TABLE order_items_partitioned (
    item_id SERIAL,
    order_id INTEGER,
    product_id INTEGER,
    quantity INTEGER,
    unit_price NUMERIC(10,2)
) PARTITION BY RANGE (order_id);

-- Create partitions for orders
CREATE TABLE orders_2024_q1 PARTITION OF orders_partitioned
    FOR VALUES FROM ('2024-01-01') TO ('2024-04-01');

CREATE TABLE orders_2024_q2 PARTITION OF orders_partitioned
    FOR VALUES FROM ('2024-04-01') TO ('2024-07-01');

-- Create partitions for order items
CREATE TABLE order_items_1_1000 PARTITION OF order_items_partitioned
    FOR VALUES FROM (1) TO (1000);

CREATE TABLE order_items_1000_2000 PARTITION OF order_items_partitioned
    FOR VALUES FROM (1000) TO (2000);

-- Insert sample data
INSERT INTO orders_partitioned (order_date, customer_id, total_amount) VALUES
    ('2024-01-15', 1, 150.00),
    ('2024-02-20', 2, 200.00),
    ('2024-05-10', 3, 175.00);

INSERT INTO order_items_partitioned (order_id, product_id, quantity, unit_price) VALUES
    (1, 101, 2, 75.00),
    (2, 102, 1, 200.00),
    (3, 103, 3, 58.33);

-- Check partition-wise join
EXPLAIN (ANALYZE, BUFFERS)
SELECT 
    o.order_id,
    o.order_date,
    o.total_amount,
    oi.product_id,
    oi.quantity,
    oi.unit_price
FROM orders_partitioned o
JOIN order_items_partitioned oi ON o.order_id = oi.order_id
WHERE o.order_date >= '2024-01-01' AND o.order_date < '2024-04-01';

-- Check partition-wise join with aggregation
EXPLAIN (ANALYZE, BUFFERS)
SELECT 
    o.order_date,
    COUNT(oi.item_id) as item_count,
    SUM(oi.quantity * oi.unit_price) as total_amount
FROM orders_partitioned o
JOIN order_items_partitioned oi ON o.order_id = oi.order_id
WHERE o.order_date >= '2024-01-01' AND o.order_date < '2024-07-01'
GROUP BY o.order_date
ORDER BY o.order_date;
```

## 11.8 Partition Maintenance

Partition maintenance involves managing partitions over time.

### Maintenance Tasks:
- **Adding Partitions**: Create new partitions
- **Removing Partitions**: Drop old partitions
- **Splitting Partitions**: Divide large partitions
- **Merging Partitions**: Combine small partitions
- **Updating Statistics**: Keep statistics current

### Real-World Analogy:
Partition maintenance is like library maintenance:
- **Adding Partitions** = Adding new sections
- **Removing Partitions** = Removing old sections
- **Splitting Partitions** = Dividing overcrowded sections
- **Merging Partitions** = Combining underused sections
- **Updating Statistics** = Keeping catalog current

### SQL Example - Partition Maintenance:
```sql
-- Create partitioned table
CREATE TABLE logs (
    log_id SERIAL,
    log_date DATE,
    level VARCHAR(20),
    message TEXT
) PARTITION BY RANGE (log_date);

-- Create initial partitions
CREATE TABLE logs_2024_01 PARTITION OF logs
    FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');

CREATE TABLE logs_2024_02 PARTITION OF logs
    FOR VALUES FROM ('2024-02-01') TO ('2024-03-01');

-- Add new partition
CREATE TABLE logs_2024_03 PARTITION OF logs
    FOR VALUES FROM ('2024-03-01') TO ('2024-04-01');

-- Insert sample data
INSERT INTO logs (log_date, level, message) VALUES
    ('2024-01-15', 'INFO', 'Application started'),
    ('2024-02-20', 'ERROR', 'Database connection failed'),
    ('2024-03-10', 'WARN', 'Memory usage high');

-- Check partition information
SELECT 
    schemaname,
    tablename,
    partitionname,
    partitionbounddef
FROM pg_partitions
WHERE tablename = 'logs'
ORDER BY partitionname;

-- Split partition (PostgreSQL 11+)
-- Note: This is a conceptual example as splitting requires specific syntax
-- ALTER TABLE logs_2024_01 SPLIT PARTITION FOR VALUES FROM ('2024-01-01') TO ('2024-02-01')
-- INTO (PARTITION logs_2024_01a FOR VALUES FROM ('2024-01-01') TO ('2024-01-15'),
--       PARTITION logs_2024_01b FOR VALUES FROM ('2024-01-15') TO ('2024-02-01'));

-- Drop old partition
DROP TABLE logs_2024_01;

-- Update statistics
ANALYZE logs;

-- Check partition statistics
SELECT 
    schemaname,
    tablename,
    partitionname,
    n_tup_ins,
    n_tup_upd,
    n_tup_del,
    n_live_tup,
    n_dead_tup
FROM pg_stat_user_tables
WHERE tablename LIKE 'logs_2024_%'
ORDER BY partitionname;
```

## 11.9 Partitioning Strategies

Choosing the right partitioning strategy depends on data characteristics and query patterns.

### Strategy Considerations:
- **Data Distribution**: How data is distributed
- **Query Patterns**: Common query patterns
- **Growth Patterns**: How data grows over time
- **Maintenance Requirements**: Maintenance frequency
- **Performance Requirements**: Performance goals

### Real-World Analogy:
Partitioning strategies are like choosing library organization methods:
- **Data Distribution** = How books are distributed
- **Query Patterns** = How people search for books
- **Growth Patterns** = How the library grows
- **Maintenance Requirements** = How often sections need updating
- **Performance Requirements** = How fast books need to be found

### SQL Example - Partitioning Strategies:
```sql
-- Strategy 1: Time-based partitioning (for time-series data)
CREATE TABLE time_series_data (
    id SERIAL,
    timestamp TIMESTAMP,
    value NUMERIC(10,2),
    metric_name VARCHAR(50)
) PARTITION BY RANGE (timestamp);

-- Create monthly partitions
CREATE TABLE time_series_2024_01 PARTITION OF time_series_data
    FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');

CREATE TABLE time_series_2024_02 PARTITION OF time_series_data
    FOR VALUES FROM ('2024-02-01') TO ('2024-03-01');

-- Strategy 2: Hash partitioning (for even distribution)
CREATE TABLE user_sessions (
    session_id SERIAL,
    user_id INTEGER,
    start_time TIMESTAMP,
    end_time TIMESTAMP
) PARTITION BY HASH (user_id);

-- Create hash partitions
CREATE TABLE user_sessions_0 PARTITION OF user_sessions
    FOR VALUES WITH (modulus 4, remainder 0);

CREATE TABLE user_sessions_1 PARTITION OF user_sessions
    FOR VALUES WITH (modulus 4, remainder 1);

CREATE TABLE user_sessions_2 PARTITION OF user_sessions
    FOR VALUES WITH (modulus 4, remainder 2);

CREATE TABLE user_sessions_3 PARTITION OF user_sessions
    FOR VALUES WITH (modulus 4, remainder 3);

-- Strategy 3: List partitioning (for categorical data)
CREATE TABLE events (
    event_id SERIAL,
    event_type VARCHAR(50),
    event_date DATE,
    description TEXT
) PARTITION BY LIST (event_type);

-- Create event type partitions
CREATE TABLE events_login PARTITION OF events
    FOR VALUES IN ('login', 'logout', 'session_start', 'session_end');

CREATE TABLE events_purchase PARTITION OF events
    FOR VALUES IN ('purchase', 'refund', 'cancellation');

CREATE TABLE events_system PARTITION OF events
    FOR VALUES IN ('error', 'warning', 'info', 'debug');

-- Strategy 4: Composite partitioning (for complex scenarios)
CREATE TABLE sales_composite (
    id SERIAL,
    sale_date DATE,
    region VARCHAR(50),
    product_category VARCHAR(50),
    amount NUMERIC(10,2)
) PARTITION BY RANGE (sale_date);

-- Create range partitions
CREATE TABLE sales_2024 PARTITION OF sales_composite
    FOR VALUES FROM ('2024-01-01') TO ('2025-01-01')
    PARTITION BY LIST (region);

-- Create list partitions within range
CREATE TABLE sales_2024_north PARTITION OF sales_2024
    FOR VALUES IN ('North', 'Northeast');

CREATE TABLE sales_2024_south PARTITION OF sales_2024
    FOR VALUES IN ('South', 'Southeast');

-- Check partitioning strategy effectiveness
SELECT 
    schemaname,
    tablename,
    partitionname,
    n_live_tup,
    pg_size_pretty(pg_relation_size(partitionname::regclass)) as size
FROM pg_stat_user_tables
WHERE tablename IN ('time_series_data', 'user_sessions', 'events', 'sales_composite')
ORDER BY tablename, partitionname;
```

## 11.10 Performance Considerations

Partitioning performance depends on proper design and maintenance.

### Performance Factors:
- **Partition Size**: Optimal partition sizes
- **Index Design**: Proper indexing strategy
- **Query Patterns**: Matching queries to partitions
- **Statistics**: Keeping statistics current
- **Maintenance**: Regular maintenance tasks

### Real-World Analogy:
Partitioning performance is like library efficiency:
- **Partition Size** = Optimal section sizes
- **Index Design** = Proper catalog organization
- **Query Patterns** = Matching searches to sections
- **Statistics** = Keeping usage data current
- **Maintenance** = Regular section updates

### SQL Example - Performance Considerations:
```sql
-- Create optimized partitioned table
CREATE TABLE performance_test (
    id SERIAL,
    created_at TIMESTAMP,
    category VARCHAR(50),
    value NUMERIC(10,2),
    status VARCHAR(20)
) PARTITION BY RANGE (created_at);

-- Create partitions with optimal sizes
CREATE TABLE performance_2024_q1 PARTITION OF performance_test
    FOR VALUES FROM ('2024-01-01') TO ('2024-04-01');

CREATE TABLE performance_2024_q2 PARTITION OF performance_test
    FOR VALUES FROM ('2024-04-01') TO ('2024-07-01');

-- Create indexes on partitions
CREATE INDEX idx_performance_2024_q1_created ON performance_2024_q1 (created_at);
CREATE INDEX idx_performance_2024_q1_category ON performance_2024_q1 (category);
CREATE INDEX idx_performance_2024_q1_status ON performance_2024_q1 (status);

CREATE INDEX idx_performance_2024_q2_created ON performance_2024_q2 (created_at);
CREATE INDEX idx_performance_2024_q2_category ON performance_2024_q2 (category);
CREATE INDEX idx_performance_2024_q2_status ON performance_2024_q2 (status);

-- Insert sample data
INSERT INTO performance_test (created_at, category, value, status) VALUES
    ('2024-01-15', 'A', 100.00, 'active'),
    ('2024-02-20', 'B', 200.00, 'inactive'),
    ('2024-05-10', 'A', 150.00, 'active'),
    ('2024-06-25', 'C', 300.00, 'pending');

-- Check partition pruning
EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM performance_test 
WHERE created_at >= '2024-01-01' AND created_at < '2024-04-01';

-- Check index usage
EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM performance_test 
WHERE created_at >= '2024-01-01' AND created_at < '2024-04-01'
AND category = 'A';

-- Check partition statistics
SELECT 
    schemaname,
    tablename,
    partitionname,
    n_live_tup,
    n_dead_tup,
    last_vacuum,
    last_autovacuum,
    last_analyze,
    last_autoanalyze
FROM pg_stat_user_tables
WHERE tablename LIKE 'performance_2024_%'
ORDER BY partitionname;

-- Check partition sizes
SELECT 
    schemaname,
    tablename,
    partitionname,
    pg_size_pretty(pg_relation_size(partitionname::regclass)) as size
FROM pg_indexes
WHERE tablename LIKE 'performance_2024_%'
ORDER BY partitionname;
```