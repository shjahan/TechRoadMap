# Section 6 – Query Optimization

## 6.1 Query Planning and Execution

Query planning and execution is the process by which PostgreSQL determines the most efficient way to execute a SQL query.

### Query Planning Process:
1. **Parsing**: Convert SQL text to parse tree
2. **Analysis**: Resolve names and types
3. **Rewriting**: Apply rules and transformations
4. **Planning**: Generate execution plan
5. **Execution**: Execute the plan

### Execution Plan Components:
- **Node Types**: Seq Scan, Index Scan, Hash Join, etc.
- **Cost Estimation**: CPU and I/O costs
- **Row Estimation**: Expected number of rows
- **Join Order**: Order of table joins
- **Index Usage**: Which indexes to use

### Real-World Analogy:
Query planning is like planning a trip:
- **Parsing** = Understanding the destination request
- **Analysis** = Checking what's available and valid
- **Rewriting** = Finding alternative routes
- **Planning** = Choosing the best route
- **Execution** = Actually taking the trip

### SQL Example - Query Planning:
```sql
-- Create sample tables
CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    city VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    customer_id INTEGER REFERENCES customers(customer_id),
    order_date DATE,
    total_amount NUMERIC(10,2),
    status VARCHAR(20)
);

CREATE TABLE order_items (
    item_id SERIAL PRIMARY KEY,
    order_id INTEGER REFERENCES orders(order_id),
    product_name VARCHAR(100),
    quantity INTEGER,
    unit_price NUMERIC(10,2)
);

-- Insert sample data
INSERT INTO customers (name, email, city) VALUES
    ('John Doe', 'john@example.com', 'New York'),
    ('Alice Smith', 'alice@example.com', 'San Francisco'),
    ('Bob Wilson', 'bob@example.com', 'Chicago'),
    ('Carol Brown', 'carol@example.com', 'New York');

INSERT INTO orders (customer_id, order_date, total_amount, status) VALUES
    (1, '2024-01-15', 150.00, 'completed'),
    (2, '2024-01-16', 299.99, 'pending'),
    (3, '2024-01-17', 75.50, 'completed'),
    (1, '2024-01-18', 200.00, 'shipped');

INSERT INTO order_items (order_id, product_name, quantity, unit_price) VALUES
    (1, 'Laptop', 1, 1200.00),
    (1, 'Mouse', 2, 25.00),
    (2, 'Gaming Laptop', 1, 1299.99),
    (3, 'Book', 1, 30.00),
    (4, 'Keyboard', 1, 89.99);

-- Basic query planning
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
SELECT c.name, o.order_date, o.total_amount
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
WHERE c.city = 'New York'
ORDER BY o.order_date;

-- Complex query planning
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
SELECT 
    c.name,
    c.city,
    COUNT(o.order_id) as order_count,
    SUM(o.total_amount) as total_spent
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
WHERE c.created_at >= '2024-01-01'
GROUP BY c.customer_id, c.name, c.city
HAVING COUNT(o.order_id) > 0
ORDER BY total_spent DESC;
```

## 6.2 EXPLAIN and EXPLAIN ANALYZE

EXPLAIN and EXPLAIN ANALYZE are tools for understanding how PostgreSQL executes queries.

### EXPLAIN Options:
- **ANALYZE**: Actually execute the query and show real timing
- **BUFFERS**: Show buffer usage statistics
- **FORMAT**: Output format (TEXT, XML, JSON, YAML)
- **VERBOSE**: Show additional information
- **COSTS**: Show cost estimates
- **TIMING**: Show timing information

### Plan Node Types:
- **Seq Scan**: Sequential table scan
- **Index Scan**: Index-based scan
- **Index Only Scan**: Scan using index only
- **Bitmap Heap Scan**: Bitmap index scan
- **Hash Join**: Hash-based join
- **Nested Loop**: Nested loop join
- **Sort**: Sorting operation
- **Aggregate**: Aggregation operation

### Real-World Analogy:
EXPLAIN is like a detailed itinerary for a trip:
- **ANALYZE** = Actually taking the trip and timing it
- **BUFFERS** = Showing how much fuel was used
- **FORMAT** = Different ways to present the itinerary
- **VERBOSE** = Including every detail
- **COSTS** = Showing estimated costs
- **TIMING** = Showing actual time taken

### SQL Example - EXPLAIN Usage:
```sql
-- Simple EXPLAIN
EXPLAIN
SELECT * FROM customers WHERE city = 'New York';

-- EXPLAIN with costs
EXPLAIN (COSTS ON)
SELECT * FROM customers WHERE city = 'New York';

-- EXPLAIN ANALYZE with timing
EXPLAIN (ANALYZE, TIMING ON)
SELECT * FROM customers WHERE city = 'New York';

-- EXPLAIN with buffers
EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM customers WHERE city = 'New York';

-- EXPLAIN with verbose output
EXPLAIN (ANALYZE, VERBOSE, BUFFERS)
SELECT c.name, o.order_date, o.total_amount
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
WHERE c.city = 'New York';

-- EXPLAIN in JSON format
EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON)
SELECT 
    c.name,
    COUNT(o.order_id) as order_count,
    SUM(o.total_amount) as total_spent
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name
ORDER BY total_spent DESC;

-- Compare different query plans
EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM customers WHERE name = 'John Doe';

EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM customers WHERE customer_id = 1;
```

## 6.3 Query Planner Statistics

Query planner statistics help PostgreSQL make informed decisions about query execution plans.

### Statistics Types:
- **Table Statistics**: Row counts, page counts, tuple statistics
- **Column Statistics**: Distinct values, most common values, histogram
- **Index Statistics**: Index usage, size, bloat
- **System Statistics**: I/O costs, CPU costs, random page costs

### Statistics Collection:
- **ANALYZE**: Manual statistics collection
- **Autovacuum**: Automatic statistics collection
- **Statistics Targets**: Control statistics accuracy
- **Statistics Views**: pg_stat_* views for monitoring

### Real-World Analogy:
Query planner statistics are like market research data:
- **Table Statistics** = General market information
- **Column Statistics** = Specific product information
- **Index Statistics** = Performance metrics
- **System Statistics** = Infrastructure costs

### SQL Example - Statistics Management:
```sql
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
WHERE tablename = 'customers';

-- Check column statistics
SELECT 
    schemaname,
    tablename,
    attname,
    n_distinct,
    most_common_vals,
    most_common_freqs,
    histogram_bounds
FROM pg_stats 
WHERE tablename = 'customers'
ORDER BY attname;

-- Update statistics manually
ANALYZE customers;
ANALYZE orders;
ANALYZE order_items;

-- Check statistics targets
SELECT 
    schemaname,
    tablename,
    attname,
    n_distinct,
    correlation
FROM pg_stats 
WHERE tablename = 'customers'
ORDER BY attname;

-- Set statistics target for specific column
ALTER TABLE customers ALTER COLUMN city SET STATISTICS 1000;

-- Re-analyze to update statistics
ANALYZE customers;

-- Check updated statistics
SELECT 
    schemaname,
    tablename,
    attname,
    n_distinct,
    most_common_vals,
    most_common_freqs
FROM pg_stats 
WHERE tablename = 'customers' 
AND attname = 'city';

-- Check system statistics
SELECT 
    name,
    setting,
    unit,
    context
FROM pg_settings 
WHERE name IN (
    'random_page_cost',
    'seq_page_cost',
    'cpu_tuple_cost',
    'cpu_index_tuple_cost',
    'cpu_operator_cost'
);
```

## 6.4 Cost-Based Optimization

Cost-based optimization uses statistics and cost models to choose the most efficient execution plan.

### Cost Components:
- **CPU Costs**: Tuple processing, operator execution
- **I/O Costs**: Disk reads and writes
- **Memory Costs**: Buffer usage, sorting, hashing
- **Network Costs**: Distributed query costs
- **Random vs Sequential**: Different costs for different access patterns

### Cost Parameters:
- **seq_page_cost**: Cost of sequential page read
- **random_page_cost**: Cost of random page read
- **cpu_tuple_cost**: Cost of processing a tuple
- **cpu_index_tuple_cost**: Cost of processing an index tuple
- **cpu_operator_cost**: Cost of executing an operator

### Real-World Analogy:
Cost-based optimization is like choosing the most cost-effective travel route:
- **CPU Costs** = Time spent driving
- **I/O Costs** = Fuel costs
- **Memory Costs** = Vehicle maintenance
- **Network Costs** = Toll fees
- **Random vs Sequential** = Highway vs city driving

### SQL Example - Cost-Based Optimization:
```sql
-- Check current cost parameters
SELECT 
    name,
    setting,
    unit,
    context,
    short_desc
FROM pg_settings 
WHERE name IN (
    'seq_page_cost',
    'random_page_cost',
    'cpu_tuple_cost',
    'cpu_index_tuple_cost',
    'cpu_operator_cost'
);

-- Create indexes to demonstrate cost differences
CREATE INDEX idx_customers_city ON customers(city);
CREATE INDEX idx_orders_customer ON orders(customer_id);
CREATE INDEX idx_orders_date ON orders(order_date);

-- Query with different cost scenarios
EXPLAIN (ANALYZE, BUFFERS, COSTS)
SELECT c.name, o.order_date, o.total_amount
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
WHERE c.city = 'New York'
ORDER BY o.order_date;

-- Adjust cost parameters
SET random_page_cost = 1.0;  -- Lower random page cost
SET seq_page_cost = 1.0;     -- Lower sequential page cost

-- Re-explain the same query
EXPLAIN (ANALYZE, BUFFERS, COSTS)
SELECT c.name, o.order_date, o.total_amount
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
WHERE c.city = 'New York'
ORDER BY o.order_date;

-- Reset cost parameters
RESET random_page_cost;
RESET seq_page_cost;

-- Query with different join types
EXPLAIN (ANALYZE, BUFFERS, COSTS)
SELECT c.name, o.order_date, o.total_amount
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
WHERE c.city = 'New York'
AND o.order_date >= '2024-01-01';

-- Force different join algorithms
SET enable_hashjoin = off;
EXPLAIN (ANALYZE, BUFFERS, COSTS)
SELECT c.name, o.order_date, o.total_amount
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
WHERE c.city = 'New York';

SET enable_hashjoin = on;
SET enable_nestloop = off;
EXPLAIN (ANALYZE, BUFFERS, COSTS)
SELECT c.name, o.order_date, o.total_amount
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
WHERE c.city = 'New York';

-- Reset join algorithms
SET enable_nestloop = on;
```

## 6.5 Join Algorithms

PostgreSQL supports different join algorithms, each optimized for different scenarios.

### Join Algorithm Types:
- **Nested Loop Join**: For small tables or when one table has an index
- **Hash Join**: For larger tables when memory is available
- **Merge Join**: For pre-sorted data or when sorting is needed
- **Bitmap Heap Scan**: For complex index conditions

### Join Algorithm Selection:
- **Table Sizes**: Relative sizes of joined tables
- **Available Memory**: Hash join memory requirements
- **Index Availability**: Presence of useful indexes
- **Data Distribution**: How data is distributed
- **Query Characteristics**: Specific query patterns

### Real-World Analogy:
Join algorithms are like different ways to match two lists:
- **Nested Loop** = Checking each item in one list against each item in another
- **Hash Join** = Creating a lookup table for fast matching
- **Merge Join** = Merging two sorted lists
- **Bitmap Heap Scan** = Using a bitmap to mark relevant items

### SQL Example - Join Algorithms:
```sql
-- Create larger tables for join demonstration
CREATE TABLE large_customers (
    customer_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    city VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE large_orders (
    order_id SERIAL PRIMARY KEY,
    customer_id INTEGER,
    order_date DATE,
    total_amount NUMERIC(10,2),
    status VARCHAR(20)
);

-- Insert more data
INSERT INTO large_customers (name, email, city)
SELECT 
    'Customer ' || i,
    'customer' || i || '@example.com',
    CASE (i % 10)
        WHEN 0 THEN 'New York'
        WHEN 1 THEN 'San Francisco'
        WHEN 2 THEN 'Chicago'
        WHEN 3 THEN 'Los Angeles'
        WHEN 4 THEN 'Boston'
        WHEN 5 THEN 'Seattle'
        WHEN 6 THEN 'Miami'
        WHEN 7 THEN 'Denver'
        WHEN 8 THEN 'Austin'
        ELSE 'Portland'
    END
FROM generate_series(1, 10000) i;

INSERT INTO large_orders (customer_id, order_date, total_amount, status)
SELECT 
    (random() * 10000)::INTEGER + 1,
    '2024-01-01'::DATE + (random() * 365)::INTEGER,
    (random() * 1000 + 10)::NUMERIC(10,2),
    CASE (random() * 4)::INTEGER
        WHEN 0 THEN 'completed'
        WHEN 1 THEN 'pending'
        WHEN 2 THEN 'shipped'
        ELSE 'cancelled'
    END
FROM generate_series(1, 50000) i;

-- Create indexes
CREATE INDEX idx_large_customers_city ON large_customers(city);
CREATE INDEX idx_large_orders_customer ON large_orders(customer_id);
CREATE INDEX idx_large_orders_date ON large_orders(order_date);

-- Analyze tables
ANALYZE large_customers;
ANALYZE large_orders;

-- Nested Loop Join
EXPLAIN (ANALYZE, BUFFERS, COSTS)
SELECT c.name, o.order_date, o.total_amount
FROM large_customers c
JOIN large_orders o ON c.customer_id = o.customer_id
WHERE c.city = 'New York'
LIMIT 100;

-- Hash Join
EXPLAIN (ANALYZE, BUFFERS, COSTS)
SELECT c.name, COUNT(o.order_id) as order_count
FROM large_customers c
JOIN large_orders o ON c.customer_id = o.customer_id
WHERE c.city = 'New York'
GROUP BY c.customer_id, c.name
ORDER BY order_count DESC
LIMIT 100;

-- Merge Join (requires sorted data)
EXPLAIN (ANALYZE, BUFFERS, COSTS)
SELECT c.name, o.order_date, o.total_amount
FROM large_customers c
JOIN large_orders o ON c.customer_id = o.customer_id
WHERE c.city = 'New York'
ORDER BY c.customer_id, o.order_date
LIMIT 100;

-- Force specific join algorithms
SET enable_hashjoin = off;
SET enable_mergejoin = off;
EXPLAIN (ANALYZE, BUFFERS, COSTS)
SELECT c.name, o.order_date, o.total_amount
FROM large_customers c
JOIN large_orders o ON c.customer_id = o.customer_id
WHERE c.city = 'New York'
LIMIT 100;

-- Reset join algorithms
SET enable_hashjoin = on;
SET enable_mergejoin = on;
```

## 6.6 Sort and Hash Operations

Sort and hash operations are fundamental to many query execution plans.

### Sort Operations:
- **External Sort**: Sorting data that doesn't fit in memory
- **In-Memory Sort**: Sorting data that fits in memory
- **Sort Keys**: Columns used for sorting
- **Sort Methods**: Different sorting algorithms
- **Sort Memory**: Memory allocation for sorting

### Hash Operations:
- **Hash Tables**: Data structures for fast lookups
- **Hash Functions**: Functions to compute hash values
- **Hash Joins**: Using hash tables for joins
- **Hash Aggregates**: Using hash tables for grouping
- **Hash Memory**: Memory allocation for hash operations

### Real-World Analogy:
Sort and hash operations are like organizing information:
- **Sort Operations** = Alphabetizing a list
- **Hash Operations** = Creating a phone book index
- **Sort Keys** = What to sort by
- **Hash Tables** = Quick lookup directories
- **Memory Allocation** = How much space to use

### SQL Example - Sort and Hash Operations:
```sql
-- Sort operations
EXPLAIN (ANALYZE, BUFFERS, COSTS)
SELECT name, city, created_at
FROM large_customers
ORDER BY city, name
LIMIT 1000;

-- Sort with different memory settings
SET work_mem = '1MB';
EXPLAIN (ANALYZE, BUFFERS, COSTS)
SELECT name, city, created_at
FROM large_customers
ORDER BY city, name
LIMIT 1000;

SET work_mem = '100MB';
EXPLAIN (ANALYZE, BUFFERS, COSTS)
SELECT name, city, created_at
FROM large_customers
ORDER BY city, name
LIMIT 1000;

-- Hash operations
EXPLAIN (ANALYZE, BUFFERS, COSTS)
SELECT city, COUNT(*) as customer_count
FROM large_customers
GROUP BY city
ORDER BY customer_count DESC;

-- Hash join
EXPLAIN (ANALYZE, BUFFERS, COSTS)
SELECT c.city, COUNT(o.order_id) as order_count
FROM large_customers c
JOIN large_orders o ON c.customer_id = o.customer_id
GROUP BY c.city
ORDER BY order_count DESC;

-- Hash aggregate with different memory
SET hash_mem_multiplier = 1.0;
EXPLAIN (ANALYZE, BUFFERS, COSTS)
SELECT city, COUNT(*) as customer_count
FROM large_customers
GROUP BY city
ORDER BY customer_count DESC;

SET hash_mem_multiplier = 2.0;
EXPLAIN (ANALYZE, BUFFERS, COSTS)
SELECT city, COUNT(*) as customer_count
FROM large_customers
GROUP BY city
ORDER BY customer_count DESC;

-- Reset memory settings
RESET work_mem;
RESET hash_mem_multiplier;
```

## 6.7 Query Hints and Directives

PostgreSQL provides limited query hints and directives to influence query execution.

### Available Hints:
- **SET Commands**: Global session settings
- **Table Hints**: Limited table-level hints
- **Index Hints**: Force specific index usage
- **Join Hints**: Control join algorithms
- **Scan Hints**: Control scan methods

### Hint Limitations:
- **Limited Support**: PostgreSQL has fewer hints than other databases
- **Global Settings**: Most hints are session-wide
- **Index Hints**: Limited index hint support
- **Join Hints**: Limited join algorithm control
- **Scan Hints**: Limited scan method control

### Real-World Analogy:
Query hints are like giving directions to a driver:
- **SET Commands** = General driving preferences
- **Table Hints** = Specific route instructions
- **Index Hints** = Which roads to use
- **Join Hints** = How to combine different routes
- **Scan Hints** = Which search method to use

### SQL Example - Query Hints:
```sql
-- Global session settings
SET enable_seqscan = off;
SET enable_indexscan = on;
SET enable_bitmapscan = on;

-- Query with forced index scan
EXPLAIN (ANALYZE, BUFFERS, COSTS)
SELECT * FROM large_customers 
WHERE city = 'New York'
LIMIT 100;

-- Force specific join algorithms
SET enable_hashjoin = off;
SET enable_mergejoin = off;
SET enable_nestloop = on;

EXPLAIN (ANALYZE, BUFFERS, COSTS)
SELECT c.name, o.order_date, o.total_amount
FROM large_customers c
JOIN large_orders o ON c.customer_id = o.customer_id
WHERE c.city = 'New York'
LIMIT 100;

-- Control sort operations
SET enable_sort = off;
EXPLAIN (ANALYZE, BUFFERS, COSTS)
SELECT name, city
FROM large_customers
ORDER BY city, name
LIMIT 100;

-- Control aggregate operations
SET enable_hashagg = off;
SET enable_sortagg = on;

EXPLAIN (ANALYZE, BUFFERS, COSTS)
SELECT city, COUNT(*) as customer_count
FROM large_customers
GROUP BY city
ORDER BY customer_count DESC;

-- Memory settings
SET work_mem = '256MB';
SET hash_mem_multiplier = 2.0;

EXPLAIN (ANALYZE, BUFFERS, COSTS)
SELECT c.city, COUNT(o.order_id) as order_count
FROM large_customers c
JOIN large_orders o ON c.customer_id = o.customer_id
GROUP BY c.city
ORDER BY order_count DESC;

-- Reset all settings
RESET enable_seqscan;
RESET enable_indexscan;
RESET enable_bitmapscan;
RESET enable_hashjoin;
RESET enable_mergejoin;
RESET enable_nestloop;
RESET enable_sort;
RESET enable_hashagg;
RESET enable_sortagg;
RESET work_mem;
RESET hash_mem_multiplier;
```

## 6.8 Performance Tuning Best Practices

Performance tuning involves optimizing queries, indexes, and database configuration for better performance.

### Tuning Areas:
- **Query Optimization**: Rewriting queries for better performance
- **Index Optimization**: Creating and maintaining appropriate indexes
- **Configuration Tuning**: Adjusting PostgreSQL parameters
- **Schema Design**: Optimizing table and column design
- **Hardware Optimization**: Using appropriate hardware resources

### Best Practices:
- **Profile First**: Identify performance bottlenecks
- **Index Strategically**: Create indexes for common query patterns
- **Optimize Queries**: Rewrite queries for better performance
- **Monitor Performance**: Track performance metrics over time
- **Test Changes**: Validate performance improvements

### Real-World Analogy:
Performance tuning is like optimizing a car:
- **Query Optimization** = Improving driving technique
- **Index Optimization** = Upgrading engine and transmission
- **Configuration Tuning** = Adjusting car settings
- **Schema Design** = Choosing the right car model
- **Hardware Optimization** = Using better fuel and parts

### SQL Example - Performance Tuning:
```sql
-- Identify slow queries
SELECT 
    query,
    calls,
    total_time,
    mean_time,
    rows,
    100.0 * shared_blks_hit / nullif(shared_blks_hit + shared_blks_read, 0) AS hit_percent
FROM pg_stat_statements 
ORDER BY total_time DESC 
LIMIT 10;

-- Check index usage
SELECT 
    schemaname,
    tablename,
    indexname,
    idx_scan,
    idx_tup_read,
    idx_tup_fetch
FROM pg_stat_user_indexes 
ORDER BY idx_scan DESC;

-- Find unused indexes
SELECT 
    schemaname,
    tablename,
    indexname,
    pg_size_pretty(pg_relation_size(indexname::regclass)) as index_size
FROM pg_stat_user_indexes 
WHERE idx_scan = 0
ORDER BY pg_relation_size(indexname::regclass) DESC;

-- Check table bloat
SELECT 
    schemaname,
    tablename,
    n_dead_tup,
    n_live_tup,
    n_dead_tup::float / n_live_tup::float * 100 as bloat_percent
FROM pg_stat_user_tables 
WHERE n_live_tup > 0
ORDER BY bloat_percent DESC;

-- Optimize queries
-- Before: Sequential scan
EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM large_customers 
WHERE city = 'New York' 
AND created_at >= '2024-01-01';

-- After: Create index and re-query
CREATE INDEX idx_large_customers_city_date ON large_customers(city, created_at);

EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM large_customers 
WHERE city = 'New York' 
AND created_at >= '2024-01-01';

-- Optimize joins
-- Before: Nested loop join
EXPLAIN (ANALYZE, BUFFERS)
SELECT c.name, o.order_date, o.total_amount
FROM large_customers c
JOIN large_orders o ON c.customer_id = o.customer_id
WHERE c.city = 'New York'
LIMIT 100;

-- After: Create index and re-query
CREATE INDEX idx_large_orders_customer_date ON large_orders(customer_id, order_date);

EXPLAIN (ANALYZE, BUFFERS)
SELECT c.name, o.order_date, o.total_amount
FROM large_customers c
JOIN large_orders o ON c.customer_id = o.customer_id
WHERE c.city = 'New York'
LIMIT 100;

-- Optimize aggregations
-- Before: Hash aggregate
EXPLAIN (ANALYZE, BUFFERS)
SELECT city, COUNT(*) as customer_count
FROM large_customers
GROUP BY city
ORDER BY customer_count DESC;

-- After: Create index and re-query
CREATE INDEX idx_large_customers_city_count ON large_customers(city);

EXPLAIN (ANALYZE, BUFFERS)
SELECT city, COUNT(*) as customer_count
FROM large_customers
GROUP BY city
ORDER BY customer_count DESC;
```

## 6.9 Monitoring Query Performance

Monitoring query performance involves tracking and analyzing query execution metrics.

### Performance Metrics:
- **Execution Time**: How long queries take to run
- **Resource Usage**: CPU, memory, and I/O usage
- **Row Counts**: Number of rows processed
- **Buffer Usage**: Buffer hit ratios
- **Index Usage**: Which indexes are being used

### Monitoring Tools:
- **pg_stat_statements**: Query execution statistics
- **pg_stat_user_tables**: Table-level statistics
- **pg_stat_user_indexes**: Index usage statistics
- **EXPLAIN ANALYZE**: Detailed execution plans
- **System Views**: Various system statistics views

### Real-World Analogy:
Monitoring query performance is like monitoring car performance:
- **Execution Time** = Trip duration
- **Resource Usage** = Fuel consumption
- **Row Counts** = Distance traveled
- **Buffer Usage** = Engine efficiency
- **Index Usage** = Route optimization

### SQL Example - Performance Monitoring:
```sql
-- Enable pg_stat_statements extension
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;

-- Check query performance
SELECT 
    query,
    calls,
    total_time,
    mean_time,
    stddev_time,
    rows,
    100.0 * shared_blks_hit / nullif(shared_blks_hit + shared_blks_read, 0) AS hit_percent
FROM pg_stat_statements 
ORDER BY total_time DESC 
LIMIT 10;

-- Check table performance
SELECT 
    schemaname,
    tablename,
    seq_scan,
    seq_tup_read,
    idx_scan,
    idx_tup_fetch,
    n_tup_ins,
    n_tup_upd,
    n_tup_del
FROM pg_stat_user_tables 
ORDER BY seq_tup_read DESC;

-- Check index performance
SELECT 
    schemaname,
    tablename,
    indexname,
    idx_scan,
    idx_tup_read,
    idx_tup_fetch
FROM pg_stat_user_indexes 
ORDER BY idx_scan DESC;

-- Check database performance
SELECT 
    datname,
    numbackends,
    xact_commit,
    xact_rollback,
    blks_read,
    blks_hit,
    100.0 * blks_hit / (blks_hit + blks_read) AS hit_percent
FROM pg_stat_database 
WHERE datname = current_database();

-- Check connection performance
SELECT 
    state,
    COUNT(*) as connection_count
FROM pg_stat_activity 
GROUP BY state
ORDER BY connection_count DESC;

-- Check lock performance
SELECT 
    mode,
    COUNT(*) as lock_count
FROM pg_locks 
GROUP BY mode
ORDER BY lock_count DESC;

-- Check I/O performance
SELECT 
    schemaname,
    tablename,
    heap_blks_read,
    heap_blks_hit,
    100.0 * heap_blks_hit / (heap_blks_hit + heap_blks_read) AS hit_percent
FROM pg_statio_user_tables 
ORDER BY heap_blks_read DESC;
```

## 6.10 Query Rewriting Techniques

Query rewriting involves modifying queries to improve performance while maintaining the same results.

### Rewriting Techniques:
- **Subquery to JOIN**: Convert subqueries to joins
- **UNION to UNION ALL**: Use UNION ALL when duplicates don't matter
- **EXISTS vs IN**: Choose appropriate existence checks
- **Index Hints**: Use appropriate indexes
- **Predicate Pushdown**: Move conditions closer to data source

### Common Patterns:
- **Correlated Subqueries**: Often can be converted to joins
- **Multiple OR Conditions**: Can be optimized with indexes
- **String Operations**: Can be optimized with expression indexes
- **Date Operations**: Can be optimized with proper indexing
- **Aggregation**: Can be optimized with proper grouping

### Real-World Analogy:
Query rewriting is like finding a better route:
- **Subquery to JOIN** = Taking a direct route instead of detours
- **UNION to UNION ALL** = Using a faster highway
- **EXISTS vs IN** = Choosing the right type of road
- **Index Hints** = Using GPS for optimal routing
- **Predicate Pushdown** = Avoiding unnecessary stops

### SQL Example - Query Rewriting:
```sql
-- Original query with subquery
EXPLAIN (ANALYZE, BUFFERS)
SELECT c.name, c.city
FROM large_customers c
WHERE c.customer_id IN (
    SELECT customer_id 
    FROM large_orders 
    WHERE total_amount > 500
);

-- Rewritten query with JOIN
EXPLAIN (ANALYZE, BUFFERS)
SELECT DISTINCT c.name, c.city
FROM large_customers c
JOIN large_orders o ON c.customer_id = o.customer_id
WHERE o.total_amount > 500;

-- Original query with EXISTS
EXPLAIN (ANALYZE, BUFFERS)
SELECT c.name, c.city
FROM large_customers c
WHERE EXISTS (
    SELECT 1 
    FROM large_orders o 
    WHERE o.customer_id = c.customer_id 
    AND o.total_amount > 500
);

-- Rewritten query with JOIN
EXPLAIN (ANALYZE, BUFFERS)
SELECT DISTINCT c.name, c.city
FROM large_customers c
JOIN large_orders o ON c.customer_id = o.customer_id
WHERE o.total_amount > 500;

-- Original query with multiple OR conditions
EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM large_customers 
WHERE city = 'New York' 
   OR city = 'San Francisco' 
   OR city = 'Chicago'
   OR city = 'Los Angeles';

-- Rewritten query with IN
EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM large_customers 
WHERE city IN ('New York', 'San Francisco', 'Chicago', 'Los Angeles');

-- Original query with string operations
EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM large_customers 
WHERE UPPER(city) = 'NEW YORK';

-- Rewritten query with expression index
CREATE INDEX idx_large_customers_city_upper ON large_customers(UPPER(city));

EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM large_customers 
WHERE UPPER(city) = 'NEW YORK';

-- Original query with date operations
EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM large_orders 
WHERE EXTRACT(YEAR FROM order_date) = 2024;

-- Rewritten query with range
EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM large_orders 
WHERE order_date >= '2024-01-01' 
AND order_date < '2025-01-01';

-- Original query with complex aggregation
EXPLAIN (ANALYZE, BUFFERS)
SELECT 
    c.city,
    COUNT(*) as customer_count,
    AVG(o.total_amount) as avg_order_amount
FROM large_customers c
LEFT JOIN large_orders o ON c.customer_id = o.customer_id
GROUP BY c.city
ORDER BY customer_count DESC;

-- Rewritten query with pre-aggregation
EXPLAIN (ANALYZE, BUFFERS)
SELECT 
    c.city,
    c.customer_count,
    COALESCE(o.avg_order_amount, 0) as avg_order_amount
FROM (
    SELECT city, COUNT(*) as customer_count
    FROM large_customers
    GROUP BY city
) c
LEFT JOIN (
    SELECT 
        c.city,
        AVG(o.total_amount) as avg_order_amount
    FROM large_customers c
    JOIN large_orders o ON c.customer_id = o.customer_id
    GROUP BY c.city
) o ON c.city = o.city
ORDER BY c.customer_count DESC;
```