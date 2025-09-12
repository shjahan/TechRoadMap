# Section 18 – Performance Tuning

## 18.1 Performance Tuning Fundamentals

Performance tuning is the process of optimizing PostgreSQL database performance by identifying bottlenecks and implementing solutions to improve query execution speed, throughput, and resource utilization.

### Key Performance Areas:
- **Query Performance**: Optimizing individual query execution
- **System Performance**: Overall database system optimization
- **Resource Utilization**: Efficient use of CPU, memory, and I/O
- **Scalability**: Ability to handle increased load

### Real-World Analogy:
Performance tuning is like optimizing a car's engine:
- **Query Performance** = Optimizing individual engine components
- **System Performance** = Overall engine efficiency
- **Resource Utilization** = Fuel and energy efficiency
- **Scalability** = Engine's ability to handle higher speeds

### Example:
```sql
-- Basic performance monitoring queries
-- Check current database activity
SELECT 
    pid,
    usename,
    application_name,
    client_addr,
    state,
    query_start,
    query
FROM pg_stat_activity
WHERE state = 'active'
ORDER BY query_start;

-- Monitor database size and growth
SELECT 
    datname as database_name,
    pg_size_pretty(pg_database_size(datname)) as size,
    pg_database_size(datname) as size_bytes
FROM pg_database
WHERE datistemplate = false
ORDER BY pg_database_size(datname) DESC;

-- Check table sizes
SELECT 
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as total_size,
    pg_size_pretty(pg_relation_size(schemaname||'.'||tablename)) as table_size,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename) - pg_relation_size(schemaname||'.'||tablename)) as index_size
FROM pg_stat_user_tables
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;
```

## 18.2 Configuration Tuning

Configuration tuning involves adjusting PostgreSQL parameters to optimize performance for your specific workload and hardware configuration.

### Key Configuration Areas:
- **Memory Settings**: shared_buffers, effective_cache_size, work_mem
- **WAL Settings**: wal_buffers, checkpoint_segments, checkpoint_completion_target
- **Connection Settings**: max_connections, superuser_reserved_connections
- **Query Planner Settings**: random_page_cost, effective_io_concurrency

### Real-World Analogy:
Configuration tuning is like adjusting a car's settings for different driving conditions:
- **Memory Settings** = Engine tuning for power vs efficiency
- **WAL Settings** = Transmission settings for smooth operation
- **Connection Settings** = Passenger capacity and comfort
- **Query Planner Settings** = Navigation system optimization

### Example:
```sql
-- Check current configuration
SELECT 
    name,
    setting,
    unit,
    context,
    short_desc
FROM pg_settings
WHERE name IN (
    'shared_buffers',
    'effective_cache_size',
    'work_mem',
    'maintenance_work_mem',
    'wal_buffers',
    'checkpoint_completion_target',
    'random_page_cost',
    'effective_io_concurrency'
);

-- Recommended configuration for different scenarios
-- For OLTP workloads (high concurrency, small transactions)
-- shared_buffers = 25% of RAM
-- effective_cache_size = 75% of RAM
-- work_mem = 4MB
-- maintenance_work_mem = 256MB

-- For OLAP workloads (large queries, analytics)
-- shared_buffers = 15% of RAM
-- effective_cache_size = 85% of RAM
-- work_mem = 64MB
-- maintenance_work_mem = 1GB

-- For mixed workloads
-- shared_buffers = 20% of RAM
-- effective_cache_size = 80% of RAM
-- work_mem = 16MB
-- maintenance_work_mem = 512MB
```

## 18.3 Index Optimization

Index optimization involves creating, maintaining, and monitoring indexes to improve query performance while minimizing storage overhead and maintenance costs.

### Index Types and Use Cases:
- **B-tree Indexes**: General purpose, range queries
- **Hash Indexes**: Equality comparisons
- **GIN Indexes**: Full-text search, array operations
- **GiST Indexes**: Geometric data, custom operators
- **BRIN Indexes**: Large tables with natural ordering

### Real-World Analogy:
Index optimization is like organizing a library:
- **B-tree Indexes** = Alphabetical catalog system
- **Hash Indexes** = Direct lookup system
- **GIN Indexes** = Subject-based catalog
- **GiST Indexes** = Geographic organization
- **BRIN Indexes** = Summary catalog for large collections

### Example:
```sql
-- Analyze index usage
SELECT 
    schemaname,
    tablename,
    indexname,
    idx_tup_read,
    idx_tup_fetch,
    idx_scan,
    CASE 
        WHEN idx_scan = 0 THEN 'UNUSED'
        WHEN idx_tup_read = 0 THEN 'NO READS'
        ELSE 'ACTIVE'
    END as status
FROM pg_stat_user_indexes
ORDER BY idx_scan DESC;

-- Find unused indexes
SELECT 
    schemaname,
    tablename,
    indexname,
    pg_size_pretty(pg_relation_size(indexrelid)) as index_size
FROM pg_stat_user_indexes
WHERE idx_scan = 0
ORDER BY pg_relation_size(indexrelid) DESC;

-- Analyze index bloat
SELECT 
    schemaname,
    tablename,
    indexname,
    pg_size_pretty(pg_relation_size(indexrelid)) as index_size,
    pg_size_pretty(pg_relation_size(indexrelid) - pg_relation_size(indexrelid) * (1 - pg_stat_get_tuples_returned(indexrelid)::float / pg_stat_get_tuples_fetched(indexrelid))) as bloat_size
FROM pg_stat_user_indexes
WHERE pg_stat_get_tuples_fetched(indexrelid) > 0;

-- Create optimized indexes
-- Composite index for multi-column queries
CREATE INDEX idx_orders_customer_date ON orders (customer_id, order_date);

-- Partial index for filtered queries
CREATE INDEX idx_orders_active ON orders (order_date) 
WHERE status = 'active';

-- Expression index for computed columns
CREATE INDEX idx_orders_total_amount ON orders ((total_amount * tax_rate));
```

## 18.4 Query Optimization

Query optimization involves analyzing and improving individual queries to reduce execution time and resource consumption.

### Optimization Techniques:
- **Query Analysis**: Using EXPLAIN and EXPLAIN ANALYZE
- **Index Usage**: Ensuring proper index utilization
- **Join Optimization**: Optimizing join strategies
- **Subquery Optimization**: Converting subqueries to joins
- **Function Optimization**: Avoiding expensive function calls

### Real-World Analogy:
Query optimization is like optimizing a delivery route:
- **Query Analysis** = Analyzing the current route
- **Index Usage** = Using efficient navigation tools
- **Join Optimization** = Optimizing multiple stops
- **Subquery Optimization** = Consolidating delivery stops
- **Function Optimization** = Using faster delivery methods

### Example:
```sql
-- Analyze query performance
EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON)
SELECT 
    o.order_id,
    o.order_date,
    c.customer_name,
    SUM(oi.quantity * oi.unit_price) as total_amount
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN order_items oi ON o.order_id = oi.order_id
WHERE o.order_date >= '2024-01-01'
GROUP BY o.order_id, o.order_date, c.customer_name
ORDER BY total_amount DESC
LIMIT 10;

-- Optimize subquery to join
-- Before (subquery)
SELECT 
    customer_id,
    customer_name
FROM customers
WHERE customer_id IN (
    SELECT DISTINCT customer_id 
    FROM orders 
    WHERE order_date >= '2024-01-01'
);

-- After (join)
SELECT DISTINCT
    c.customer_id,
    c.customer_name
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id
WHERE o.order_date >= '2024-01-01';

-- Use window functions instead of correlated subqueries
-- Before (correlated subquery)
SELECT 
    order_id,
    order_date,
    total_amount,
    (SELECT AVG(total_amount) 
     FROM orders o2 
     WHERE o2.customer_id = o1.customer_id) as avg_customer_amount
FROM orders o1;

-- After (window function)
SELECT 
    order_id,
    order_date,
    total_amount,
    AVG(total_amount) OVER (PARTITION BY customer_id) as avg_customer_amount
FROM orders;
```

## 18.5 Memory Management

Memory management involves optimizing PostgreSQL's memory usage to improve performance and avoid memory-related issues.

### Memory Components:
- **shared_buffers**: Shared memory for caching data pages
- **work_mem**: Memory for sorting and hash operations
- **maintenance_work_mem**: Memory for maintenance operations
- **effective_cache_size**: Estimated size of OS cache

### Real-World Analogy:
Memory management is like managing warehouse space:
- **shared_buffers** = Main warehouse storage
- **work_mem** = Workbench space for processing
- **maintenance_work_mem** = Specialized equipment space
- **effective_cache_size** = Total available warehouse space

### Example:
```sql
-- Monitor memory usage
SELECT 
    name,
    setting,
    unit,
    context
FROM pg_settings
WHERE name IN (
    'shared_buffers',
    'work_mem',
    'maintenance_work_mem',
    'effective_cache_size',
    'max_connections'
);

-- Calculate memory requirements
-- Total memory = shared_buffers + (max_connections * work_mem) + maintenance_work_mem
SELECT 
    setting::bigint * 8192 as shared_buffers_bytes,
    (SELECT setting::bigint FROM pg_settings WHERE name = 'max_connections') * 
    (SELECT setting::bigint FROM pg_settings WHERE name = 'work_mem') * 1024 as work_mem_total_bytes,
    (SELECT setting::bigint FROM pg_settings WHERE name = 'maintenance_work_mem') * 1024 as maintenance_work_mem_bytes;

-- Monitor memory usage in real-time
SELECT 
    pid,
    usename,
    application_name,
    state,
    query,
    pg_size_pretty(pg_stat_get_activity_memory_usage(pid)) as memory_usage
FROM pg_stat_activity
WHERE state = 'active'
ORDER BY pg_stat_get_activity_memory_usage(pid) DESC;
```

## 18.6 I/O Optimization

I/O optimization involves reducing disk I/O operations and improving I/O performance through various techniques.

### I/O Optimization Techniques:
- **Index Optimization**: Reducing I/O through better indexing
- **Partitioning**: Reducing I/O through table partitioning
- **VACUUM and ANALYZE**: Maintaining optimal I/O performance
- **Storage Optimization**: Using appropriate storage types

### Real-World Analogy:
I/O optimization is like optimizing a filing system:
- **Index Optimization** = Better filing system organization
- **Partitioning** = Separating files by category
- **VACUUM and ANALYZE** = Regular file cleanup and organization
- **Storage Optimization** = Using appropriate storage methods

### Example:
```sql
-- Monitor I/O statistics
SELECT 
    datname,
    blks_read,
    blks_hit,
    round(blks_hit::float / (blks_hit + blks_read) * 100, 2) as cache_hit_ratio
FROM pg_stat_database
WHERE datname = current_database();

-- Check table I/O statistics
SELECT 
    schemaname,
    tablename,
    heap_blks_read,
    heap_blks_hit,
    idx_blks_read,
    idx_blks_hit,
    round(heap_blks_hit::float / (heap_blks_hit + heap_blks_read) * 100, 2) as heap_hit_ratio,
    round(idx_blks_hit::float / (idx_blks_hit + idx_blks_read) * 100, 2) as idx_hit_ratio
FROM pg_statio_user_tables
ORDER BY heap_blks_read + idx_blks_read DESC;

-- Optimize I/O through partitioning
-- Create partitioned table
CREATE TABLE sales (
    id SERIAL,
    sale_date DATE,
    product_id INTEGER,
    amount DECIMAL(10,2)
) PARTITION BY RANGE (sale_date);

-- Create monthly partitions
CREATE TABLE sales_2024_01 PARTITION OF sales
    FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');

CREATE TABLE sales_2024_02 PARTITION OF sales
    FOR VALUES FROM ('2024-02-01') TO ('2024-03-01');

-- Create indexes on partitions
CREATE INDEX idx_sales_2024_01_date ON sales_2024_01 (sale_date);
CREATE INDEX idx_sales_2024_02_date ON sales_2024_02 (sale_date);
```

## 18.7 Connection Pooling

Connection pooling manages database connections efficiently to reduce connection overhead and improve performance.

### Connection Pooling Benefits:
- **Reduced Overhead**: Reusing existing connections
- **Resource Management**: Limiting concurrent connections
- **Load Distribution**: Distributing load across connections
- **Fault Tolerance**: Handling connection failures

### Real-World Analogy:
Connection pooling is like a taxi dispatch system:
- **Reduced Overhead** = Reusing available taxis
- **Resource Management** = Managing taxi fleet size
- **Load Distribution** = Efficiently dispatching taxis
- **Fault Tolerance** = Handling taxi breakdowns

### Example:
```sql
-- Monitor connection usage
SELECT 
    state,
    count(*) as connection_count,
    round(count(*)::float / (SELECT count(*) FROM pg_stat_activity) * 100, 2) as percentage
FROM pg_stat_activity
GROUP BY state
ORDER BY connection_count DESC;

-- Check connection limits
SELECT 
    setting as max_connections,
    (SELECT count(*) FROM pg_stat_activity) as current_connections,
    (SELECT count(*) FROM pg_stat_activity WHERE state = 'active') as active_connections
FROM pg_settings
WHERE name = 'max_connections';

-- Monitor connection duration
SELECT 
    pid,
    usename,
    application_name,
    state,
    query_start,
    now() - query_start as duration,
    query
FROM pg_stat_activity
WHERE state = 'active'
ORDER BY duration DESC;

-- Connection pooling configuration example (pgBouncer)
-- pgbouncer.ini
[databases]
mydb = host=localhost port=5432 dbname=mydb

[pgbouncer]
listen_port = 6432
listen_addr = 127.0.0.1
auth_type = md5
auth_file = /etc/pgbouncer/userlist.txt
pool_mode = transaction
max_client_conn = 100
default_pool_size = 20
reserve_pool_size = 5
reserve_pool_timeout = 3
```

## 18.8 Monitoring and Profiling

Monitoring and profiling provide insights into database performance and help identify optimization opportunities.

### Monitoring Tools:
- **pg_stat_statements**: Query performance statistics
- **pg_stat_activity**: Current activity monitoring
- **pg_stat_database**: Database-level statistics
- **pg_stat_user_tables**: Table-level statistics

### Real-World Analogy:
Monitoring and profiling are like having a comprehensive dashboard in a car:
- **pg_stat_statements** = Engine performance metrics
- **pg_stat_activity** = Current driving status
- **pg_stat_database** = Overall vehicle performance
- **pg_stat_user_tables** = Individual component performance

### Example:
```sql
-- Enable query statistics
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;

-- Top queries by total time
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

-- Top queries by average time
SELECT 
    query,
    calls,
    total_time,
    mean_time,
    rows
FROM pg_stat_statements
WHERE calls > 100
ORDER BY mean_time DESC
LIMIT 10;

-- Monitor table activity
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

-- Monitor index usage
SELECT 
    schemaname,
    tablename,
    indexname,
    idx_scan,
    idx_tup_read,
    idx_tup_fetch
FROM pg_stat_user_indexes
ORDER BY idx_scan DESC;
```

## 18.9 Performance Testing

Performance testing involves systematically testing database performance under various conditions to identify bottlenecks and validate optimizations.

### Testing Types:
- **Load Testing**: Testing under normal expected load
- **Stress Testing**: Testing under extreme load conditions
- **Volume Testing**: Testing with large amounts of data
- **Concurrency Testing**: Testing with multiple concurrent users

### Real-World Analogy:
Performance testing is like testing a car's performance:
- **Load Testing** = Normal driving conditions
- **Stress Testing** = Extreme driving conditions
- **Volume Testing** = Testing with heavy cargo
- **Concurrency Testing** = Testing with multiple passengers

### Example:
```sql
-- Create test data for performance testing
CREATE TABLE performance_test (
    id SERIAL PRIMARY KEY,
    data TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Generate test data
INSERT INTO performance_test (data)
SELECT 
    'Test data ' || generate_series(1, 1000000) || ' - ' || 
    md5(random()::text)
FROM generate_series(1, 1000000);

-- Create indexes for testing
CREATE INDEX idx_performance_test_created_at ON performance_test (created_at);
CREATE INDEX idx_performance_test_data ON performance_test (data);

-- Test query performance
EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON)
SELECT 
    id,
    data,
    created_at
FROM performance_test
WHERE created_at >= '2024-01-01'
ORDER BY created_at DESC
LIMIT 1000;

-- Test concurrent performance
-- Simulate concurrent inserts
DO $$
DECLARE
    i INTEGER;
BEGIN
    FOR i IN 1..1000 LOOP
        INSERT INTO performance_test (data) 
        VALUES ('Concurrent test ' || i || ' - ' || md5(random()::text));
    END LOOP;
END $$;

-- Monitor performance during testing
SELECT 
    pid,
    usename,
    state,
    query_start,
    now() - query_start as duration,
    query
FROM pg_stat_activity
WHERE query LIKE '%performance_test%'
ORDER BY query_start DESC;
```

## 18.10 Best Practices

Best practices for performance tuning ensure consistent, maintainable, and effective performance optimization.

### Key Practices:
- **Regular Monitoring**: Continuous performance monitoring
- **Baseline Establishment**: Establishing performance baselines
- **Incremental Optimization**: Making small, measurable improvements
- **Documentation**: Documenting performance optimizations
- **Testing**: Validating optimizations through testing

### Real-World Analogy:
Best practices are like maintaining a high-performance vehicle:
- **Regular Monitoring** = Regular maintenance checks
- **Baseline Establishment** = Knowing normal performance levels
- **Incremental Optimization** = Making small improvements over time
- **Documentation** = Keeping maintenance records
- **Testing** = Regular performance testing

### Example:
```sql
-- Create a performance monitoring function
CREATE OR REPLACE FUNCTION monitor_performance()
RETURNS TABLE(
    metric_name TEXT,
    metric_value TEXT,
    recommendation TEXT
) AS $$
BEGIN
    -- Check cache hit ratio
    RETURN QUERY
    SELECT 
        'Cache Hit Ratio'::TEXT,
        round(blks_hit::float / (blks_hit + blks_read) * 100, 2)::TEXT || '%',
        CASE 
            WHEN blks_hit::float / (blks_hit + blks_read) < 0.9 THEN 'Consider increasing shared_buffers'
            ELSE 'Cache hit ratio is good'
        END
    FROM pg_stat_database
    WHERE datname = current_database();
    
    -- Check connection usage
    RETURN QUERY
    SELECT 
        'Connection Usage'::TEXT,
        (SELECT count(*) FROM pg_stat_activity)::TEXT || '/' || 
        (SELECT setting FROM pg_settings WHERE name = 'max_connections')::TEXT,
        CASE 
            WHEN (SELECT count(*) FROM pg_stat_activity)::float / 
                 (SELECT setting::float FROM pg_settings WHERE name = 'max_connections') > 0.8 
            THEN 'Consider connection pooling or increasing max_connections'
            ELSE 'Connection usage is acceptable'
        END;
    
    -- Check for unused indexes
    RETURN QUERY
    SELECT 
        'Unused Indexes'::TEXT,
        count(*)::TEXT,
        CASE 
            WHEN count(*) > 0 THEN 'Consider dropping unused indexes'
            ELSE 'No unused indexes found'
        END
    FROM pg_stat_user_indexes
    WHERE idx_scan = 0;
END;
$$ LANGUAGE plpgsql;

-- Use the monitoring function
SELECT * FROM monitor_performance();
```