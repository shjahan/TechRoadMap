# Section 19 – Advanced Features

## 19.1 Logical Replication

Logical replication allows you to replicate data changes at the logical level, enabling selective replication of specific tables or databases and supporting different PostgreSQL versions.

### Key Concepts:
- **Publication**: Defines which tables to replicate
- **Subscription**: Connects to a publication and receives changes
- **Logical Decoding**: Extracting changes from WAL in a logical format
- **Replication Slots**: Ensuring WAL retention for subscribers

### Real-World Analogy:
Logical replication is like a newspaper subscription service:
- **Publication** = Different newspaper sections you want
- **Subscription** = Your subscription to specific sections
- **Logical Decoding** = Converting news into readable format
- **Replication Slots** = Ensuring you don't miss any issues

### Example:
```sql
-- Set up logical replication
-- On the publisher (source) database
ALTER SYSTEM SET wal_level = logical;
ALTER SYSTEM SET max_replication_slots = 10;
SELECT pg_reload_conf();

-- Create a publication
CREATE PUBLICATION my_publication FOR TABLE users, orders, products;

-- On the subscriber (target) database
-- Create the same tables
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50),
    email VARCHAR(100),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    total_amount DECIMAL(10,2),
    order_date TIMESTAMP DEFAULT NOW()
);

CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    price DECIMAL(10,2),
    stock_quantity INTEGER
);

-- Create subscription
CREATE SUBSCRIPTION my_subscription
CONNECTION 'host=publisher_host port=5432 dbname=mydb user=replicator password=password'
PUBLICATION my_publication;

-- Monitor replication status
SELECT 
    subname,
    subenabled,
    subslotname,
    subpublications
FROM pg_subscription;

-- Check replication lag
SELECT 
    application_name,
    client_addr,
    state,
    sent_lsn,
    write_lsn,
    flush_lsn,
    replay_lsn
FROM pg_stat_replication;
```

## 19.2 Foreign Data Wrappers

Foreign Data Wrappers (FDW) allow PostgreSQL to access data stored in external systems as if they were local tables, enabling federated queries across different data sources.

### Key Components:
- **Foreign Data Wrapper**: Extension that handles communication with external systems
- **Foreign Server**: Connection to external data source
- **Foreign Table**: Local representation of external data
- **User Mapping**: Authentication for foreign servers

### Real-World Analogy:
Foreign Data Wrappers are like universal translators:
- **Foreign Data Wrapper** = Translation protocol
- **Foreign Server** = Connection to foreign system
- **Foreign Table** = Translated data representation
- **User Mapping** = Authentication credentials

### Example:
```sql
-- Install postgres_fdw extension
CREATE EXTENSION postgres_fdw;

-- Create foreign server
CREATE SERVER remote_server
FOREIGN DATA WRAPPER postgres_fdw
OPTIONS (host 'remote_host', port '5432', dbname 'remote_db');

-- Create user mapping
CREATE USER MAPPING FOR current_user
SERVER remote_server
OPTIONS (user 'remote_user', password 'remote_password');

-- Create foreign table
CREATE FOREIGN TABLE remote_users (
    id INTEGER,
    username VARCHAR(50),
    email VARCHAR(100),
    created_at TIMESTAMP
) SERVER remote_server
OPTIONS (schema_name 'public', table_name 'users');

-- Query foreign table
SELECT 
    id,
    username,
    email,
    created_at
FROM remote_users
WHERE created_at >= '2024-01-01'
ORDER BY created_at DESC;

-- Join local and foreign tables
SELECT 
    l.id as local_id,
    l.name as local_name,
    r.username as remote_username,
    r.email as remote_email
FROM local_customers l
JOIN remote_users r ON l.email = r.email;

-- Create foreign table for CSV file (using file_fdw)
CREATE EXTENSION file_fdw;

CREATE SERVER csv_server
FOREIGN DATA WRAPPER file_fdw;

CREATE FOREIGN TABLE csv_data (
    id INTEGER,
    name VARCHAR(100),
    value DECIMAL(10,2)
) SERVER csv_server
OPTIONS (filename '/path/to/data.csv', format 'csv', header 'true');
```

## 19.3 Parallel Query Processing

Parallel query processing allows PostgreSQL to execute queries using multiple CPU cores simultaneously, significantly improving performance for large data operations.

### Parallel Operations:
- **Parallel Sequential Scans**: Multiple workers scan different parts of a table
- **Parallel Hash Joins**: Parallel execution of hash join operations
- **Parallel Nested Loops**: Parallel nested loop joins
- **Parallel Aggregation**: Parallel execution of aggregate functions

### Real-World Analogy:
Parallel query processing is like having multiple workers on an assembly line:
- **Parallel Sequential Scans** = Multiple workers checking different sections
- **Parallel Hash Joins** = Multiple workers matching parts simultaneously
- **Parallel Nested Loops** = Multiple workers doing repetitive tasks
- **Parallel Aggregation** = Multiple workers counting and summarizing

### Example:
```sql
-- Enable parallel query processing
ALTER SYSTEM SET max_parallel_workers_per_gather = 4;
ALTER SYSTEM SET max_parallel_workers = 8;
ALTER SYSTEM SET parallel_tuple_cost = 0.1;
ALTER SYSTEM SET parallel_setup_cost = 1000.0;
SELECT pg_reload_conf();

-- Create a large table for testing
CREATE TABLE large_table (
    id SERIAL PRIMARY KEY,
    data TEXT,
    value INTEGER,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Insert test data
INSERT INTO large_table (data, value)
SELECT 
    'Data ' || generate_series(1, 1000000),
    (random() * 1000)::INTEGER
FROM generate_series(1, 1000000);

-- Analyze the table
ANALYZE large_table;

-- Test parallel sequential scan
EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON)
SELECT 
    value,
    COUNT(*) as count,
    AVG(value) as avg_value
FROM large_table
WHERE value > 500
GROUP BY value
ORDER BY count DESC;

-- Test parallel hash join
EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON)
SELECT 
    t1.value,
    COUNT(*) as count
FROM large_table t1
JOIN large_table t2 ON t1.value = t2.value
WHERE t1.value > 100
GROUP BY t1.value
ORDER BY count DESC;

-- Monitor parallel query execution
SELECT 
    pid,
    usename,
    application_name,
    state,
    query,
    parallel_workers
FROM pg_stat_activity
WHERE parallel_workers > 0;
```

## 19.4 JIT Compilation

Just-In-Time (JIT) compilation compiles SQL queries to machine code at runtime, providing significant performance improvements for complex queries.

### JIT Components:
- **Expression JIT**: Compiling individual expressions
- **Tuple Deforming**: Optimizing tuple access
- **Inlining**: Inlining function calls
- **LLVM**: Low-level virtual machine for compilation

### Real-World Analogy:
JIT compilation is like having a translator who learns your language:
- **Expression JIT** = Translating individual phrases
- **Tuple Deforming** = Optimizing data access patterns
- **Inlining** = Combining related translations
- **LLVM** = The translation engine

### Example:
```sql
-- Enable JIT compilation
ALTER SYSTEM SET jit = on;
ALTER SYSTEM SET jit_above_cost = 100000;
ALTER SYSTEM SET jit_optimize_above_cost = 500000;
ALTER SYSTEM SET jit_inline_above_cost = 500000;
SELECT pg_reload_conf();

-- Check JIT settings
SELECT 
    name,
    setting,
    unit,
    short_desc
FROM pg_settings
WHERE name LIKE 'jit%';

-- Create a complex query for JIT testing
CREATE TABLE sales_data (
    id SERIAL PRIMARY KEY,
    product_id INTEGER,
    customer_id INTEGER,
    sale_date DATE,
    quantity INTEGER,
    unit_price DECIMAL(10,2),
    discount DECIMAL(5,2),
    region VARCHAR(50)
);

-- Insert test data
INSERT INTO sales_data (product_id, customer_id, sale_date, quantity, unit_price, discount, region)
SELECT 
    (random() * 1000)::INTEGER,
    (random() * 10000)::INTEGER,
    '2024-01-01'::DATE + (random() * 365)::INTEGER,
    (random() * 100)::INTEGER,
    (random() * 1000)::DECIMAL(10,2),
    (random() * 20)::DECIMAL(5,2),
    CASE (random() * 4)::INTEGER
        WHEN 0 THEN 'North'
        WHEN 1 THEN 'South'
        WHEN 2 THEN 'East'
        ELSE 'West'
    END
FROM generate_series(1, 1000000);

-- Analyze the table
ANALYZE sales_data;

-- Test JIT compilation with complex query
EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON)
SELECT 
    region,
    product_id,
    COUNT(*) as sales_count,
    SUM(quantity * unit_price * (1 - discount/100)) as total_revenue,
    AVG(quantity * unit_price * (1 - discount/100)) as avg_revenue,
    STDDEV(quantity * unit_price * (1 - discount/100)) as revenue_stddev
FROM sales_data
WHERE sale_date >= '2024-01-01'
    AND sale_date < '2024-07-01'
    AND quantity > 10
    AND unit_price > 50
GROUP BY region, product_id
HAVING COUNT(*) > 5
ORDER BY total_revenue DESC
LIMIT 100;

-- Check JIT compilation statistics
SELECT 
    jit_generation_time,
    jit_inlining_time,
    jit_optimization_time,
    jit_emission_time
FROM pg_stat_statements
WHERE query LIKE '%sales_data%'
ORDER BY total_time DESC
LIMIT 1;
```

## 19.5 Advanced Indexing Techniques

Advanced indexing techniques provide specialized indexing solutions for complex data types and query patterns.

### Advanced Index Types:
- **Partial Indexes**: Indexes on subset of data
- **Expression Indexes**: Indexes on computed expressions
- **Covering Indexes**: Indexes that include additional columns
- **Multi-column Indexes**: Indexes on multiple columns

### Real-World Analogy:
Advanced indexing techniques are like specialized filing systems:
- **Partial Indexes** = Filing only specific categories
- **Expression Indexes** = Filing by computed values
- **Covering Indexes** = Filing with additional information
- **Multi-column Indexes** = Filing by multiple criteria

### Example:
```sql
-- Create partial indexes
CREATE INDEX idx_active_orders ON orders (order_date) 
WHERE status = 'active';

CREATE INDEX idx_high_value_orders ON orders (customer_id, order_date) 
WHERE total_amount > 1000;

-- Create expression indexes
CREATE INDEX idx_orders_upper_customer ON orders (UPPER(customer_name));
CREATE INDEX idx_orders_year_month ON orders (EXTRACT(YEAR FROM order_date), EXTRACT(MONTH FROM order_date));

-- Create covering indexes
CREATE INDEX idx_orders_covering ON orders (customer_id) 
INCLUDE (order_date, total_amount, status);

-- Create multi-column indexes
CREATE INDEX idx_orders_customer_date_status ON orders (customer_id, order_date, status);

-- Test index usage
EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON)
SELECT 
    customer_id,
    order_date,
    total_amount
FROM orders
WHERE customer_id = 123
    AND order_date >= '2024-01-01'
    AND status = 'active'
ORDER BY order_date DESC;

-- Monitor index usage
SELECT 
    schemaname,
    tablename,
    indexname,
    idx_scan,
    idx_tup_read,
    idx_tup_fetch
FROM pg_stat_user_indexes
WHERE schemaname = 'public'
ORDER BY idx_scan DESC;
```

## 19.6 Advanced Partitioning

Advanced partitioning techniques provide sophisticated data organization strategies for large tables.

### Partitioning Strategies:
- **Range Partitioning**: Partitioning by value ranges
- **List Partitioning**: Partitioning by specific values
- **Hash Partitioning**: Partitioning by hash values
- **Composite Partitioning**: Combining multiple partitioning strategies

### Real-World Analogy:
Advanced partitioning is like organizing a large library:
- **Range Partitioning** = Organizing by date ranges
- **List Partitioning** = Organizing by specific categories
- **Hash Partitioning** = Organizing by hash values
- **Composite Partitioning** = Organizing by multiple criteria

### Example:
```sql
-- Create range-partitioned table
CREATE TABLE sales (
    id SERIAL,
    sale_date DATE,
    product_id INTEGER,
    customer_id INTEGER,
    amount DECIMAL(10,2)
) PARTITION BY RANGE (sale_date);

-- Create monthly partitions
CREATE TABLE sales_2024_01 PARTITION OF sales
    FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');

CREATE TABLE sales_2024_02 PARTITION OF sales
    FOR VALUES FROM ('2024-02-01') TO ('2024-03-01');

CREATE TABLE sales_2024_03 PARTITION OF sales
    FOR VALUES FROM ('2024-03-01') TO ('2024-04-01');

-- Create list-partitioned table
CREATE TABLE products (
    id SERIAL,
    name VARCHAR(100),
    category VARCHAR(50),
    price DECIMAL(10,2)
) PARTITION BY LIST (category);

-- Create category partitions
CREATE TABLE products_electronics PARTITION OF products
    FOR VALUES IN ('Electronics', 'Computers', 'Mobile');

CREATE TABLE products_clothing PARTITION OF products
    FOR VALUES IN ('Clothing', 'Shoes', 'Accessories');

CREATE TABLE products_books PARTITION OF products
    FOR VALUES IN ('Books', 'Magazines', 'E-books');

-- Create hash-partitioned table
CREATE TABLE user_sessions (
    id SERIAL,
    user_id INTEGER,
    session_data JSONB,
    created_at TIMESTAMP
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

-- Test partition pruning
EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON)
SELECT 
    product_id,
    SUM(amount) as total_sales
FROM sales
WHERE sale_date >= '2024-01-01'
    AND sale_date < '2024-02-01'
GROUP BY product_id
ORDER BY total_sales DESC;
```

## 19.7 Advanced Security Features

Advanced security features provide comprehensive protection for PostgreSQL databases.

### Security Features:
- **Row Level Security**: Fine-grained access control
- **Column Level Security**: Column-specific access control
- **Encryption**: Data encryption at rest and in transit
- **Audit Logging**: Comprehensive audit trails

### Real-World Analogy:
Advanced security features are like a multi-layered security system:
- **Row Level Security** = Access control to specific rooms
- **Column Level Security** = Access control to specific information
- **Encryption** = Secure communication channels
- **Audit Logging** = Security camera system

### Example:
```sql
-- Enable row level security
CREATE TABLE sensitive_data (
    id SERIAL PRIMARY KEY,
    user_id INTEGER,
    data TEXT,
    classification VARCHAR(20),
    created_at TIMESTAMP DEFAULT NOW()
);

ALTER TABLE sensitive_data ENABLE ROW LEVEL SECURITY;

-- Create RLS policies
CREATE POLICY user_data_policy ON sensitive_data
    FOR ALL TO app_user
    USING (user_id = current_setting('app.current_user_id')::INTEGER);

CREATE POLICY admin_data_policy ON sensitive_data
    FOR ALL TO admin_user
    USING (classification IN ('public', 'internal', 'confidential'));

-- Create column-level security
CREATE TABLE user_profiles (
    id SERIAL PRIMARY KEY,
    user_id INTEGER,
    public_name VARCHAR(100),
    private_email VARCHAR(100),
    internal_notes TEXT
);

-- Grant column-specific access
GRANT SELECT (id, user_id, public_name) ON user_profiles TO public_user;
GRANT SELECT (id, user_id, public_name, private_email) ON user_profiles TO registered_user;
GRANT ALL ON user_profiles TO admin_user;

-- Enable audit logging
CREATE EXTENSION IF NOT EXISTS pgaudit;

-- Configure audit logging
ALTER SYSTEM SET pgaudit.log = 'write, ddl';
ALTER SYSTEM SET pgaudit.log_catalog = off;
ALTER SYSTEM SET pgaudit.log_parameter = on;
SELECT pg_reload_conf();

-- Test security features
-- Set user context
SET app.current_user_id = '123';

-- Test RLS
SELECT * FROM sensitive_data WHERE user_id = 123;
SELECT * FROM sensitive_data WHERE user_id = 456; -- Should return no rows

-- Test column-level security
SELECT id, user_id, public_name FROM user_profiles; -- Should work for public_user
SELECT id, user_id, public_name, private_email FROM user_profiles; -- Should work for registered_user
```

## 19.8 Advanced Monitoring

Advanced monitoring provides comprehensive insights into database performance and health.

### Monitoring Components:
- **Performance Metrics**: Query performance and resource utilization
- **Health Checks**: Database health and availability
- **Alerting**: Automated notifications for issues
- **Dashboards**: Visual representation of metrics

### Real-World Analogy:
Advanced monitoring is like a comprehensive health monitoring system:
- **Performance Metrics** = Vital signs monitoring
- **Health Checks** = Regular health assessments
- **Alerting** = Emergency notification system
- **Dashboards** = Health status display

### Example:
```sql
-- Create comprehensive monitoring function
CREATE OR REPLACE FUNCTION get_database_health()
RETURNS TABLE(
    metric_name TEXT,
    metric_value TEXT,
    status TEXT,
    recommendation TEXT
) AS $$
BEGIN
    -- Check database size
    RETURN QUERY
    SELECT 
        'Database Size'::TEXT,
        pg_size_pretty(pg_database_size(current_database()))::TEXT,
        CASE 
            WHEN pg_database_size(current_database()) > 1000000000000 THEN 'WARNING'
            ELSE 'OK'
        END,
        CASE 
            WHEN pg_database_size(current_database()) > 1000000000000 THEN 'Consider archiving old data'
            ELSE 'Size is acceptable'
        END;
    
    -- Check connection usage
    RETURN QUERY
    SELECT 
        'Connection Usage'::TEXT,
        (SELECT count(*) FROM pg_stat_activity)::TEXT || '/' || 
        (SELECT setting FROM pg_settings WHERE name = 'max_connections')::TEXT,
        CASE 
            WHEN (SELECT count(*) FROM pg_stat_activity)::float / 
                 (SELECT setting::float FROM pg_settings WHERE name = 'max_connections') > 0.8 
            THEN 'WARNING'
            ELSE 'OK'
        END,
        CASE 
            WHEN (SELECT count(*) FROM pg_stat_activity)::float / 
                 (SELECT setting::float FROM pg_settings WHERE name = 'max_connections') > 0.8 
            THEN 'Consider connection pooling'
            ELSE 'Connection usage is acceptable'
        END;
    
    -- Check cache hit ratio
    RETURN QUERY
    SELECT 
        'Cache Hit Ratio'::TEXT,
        round(blks_hit::float / (blks_hit + blks_read) * 100, 2)::TEXT || '%',
        CASE 
            WHEN blks_hit::float / (blks_hit + blks_read) < 0.9 THEN 'WARNING'
            ELSE 'OK'
        END,
        CASE 
            WHEN blks_hit::float / (blks_hit + blks_read) < 0.9 THEN 'Consider increasing shared_buffers'
            ELSE 'Cache hit ratio is good'
        END
    FROM pg_stat_database
    WHERE datname = current_database();
    
    -- Check for long-running queries
    RETURN QUERY
    SELECT 
        'Long Running Queries'::TEXT,
        count(*)::TEXT,
        CASE 
            WHEN count(*) > 0 THEN 'WARNING'
            ELSE 'OK'
        END,
        CASE 
            WHEN count(*) > 0 THEN 'Review and optimize long-running queries'
            ELSE 'No long-running queries'
        END
    FROM pg_stat_activity
    WHERE state = 'active' 
        AND now() - query_start > interval '5 minutes';
END;
$$ LANGUAGE plpgsql;

-- Use the monitoring function
SELECT * FROM get_database_health();
```

## 19.9 Advanced Backup and Recovery

Advanced backup and recovery techniques provide comprehensive data protection and recovery capabilities.

### Backup Strategies:
- **Continuous Archiving**: Continuous WAL archiving
- **Point-in-Time Recovery**: Recovery to specific points in time
- **Incremental Backups**: Backing up only changed data
- **Cross-Platform Recovery**: Recovery across different platforms

### Real-World Analogy:
Advanced backup and recovery is like a comprehensive insurance system:
- **Continuous Archiving** = Continuous documentation
- **Point-in-Time Recovery** = Restoring to specific moments
- **Incremental Backups** = Updating only changed documents
- **Cross-Platform Recovery** = Universal document format

### Example:
```sql
-- Configure continuous archiving
ALTER SYSTEM SET wal_level = replica;
ALTER SYSTEM SET archive_mode = on;
ALTER SYSTEM SET archive_command = 'cp %p /backup/wal_archive/%f';
ALTER SYSTEM SET max_wal_senders = 3;
ALTER SYSTEM SET wal_keep_segments = 64;
SELECT pg_reload_conf();

-- Create base backup
-- pg_basebackup -D /backup/base_backup -Ft -z -P

-- Test point-in-time recovery
-- Create recovery.conf
-- restore_command = 'cp /backup/wal_archive/%f %p'
-- recovery_target_time = '2024-01-01 12:00:00'

-- Monitor backup status
SELECT 
    archived_count,
    last_archived_wal,
    last_archived_time,
    failed_count,
    last_failed_wal,
    last_failed_time
FROM pg_stat_archiver;

-- Check WAL generation
SELECT 
    pg_current_wal_lsn() as current_lsn,
    pg_walfile_name(pg_current_wal_lsn()) as current_wal_file;
```

## 19.10 Best Practices

Best practices for advanced features ensure optimal performance, security, and maintainability.

### Key Practices:
- **Feature Selection**: Choose appropriate features for your use case
- **Performance Testing**: Test advanced features thoroughly
- **Security Review**: Regular security assessments
- **Documentation**: Document advanced feature usage
- **Monitoring**: Continuous monitoring of advanced features

### Real-World Analogy:
Best practices are like maintaining a high-performance vehicle:
- **Feature Selection** = Choosing appropriate upgrades
- **Performance Testing** = Regular performance testing
- **Security Review** = Regular security inspections
- **Documentation** = Keeping maintenance records
- **Monitoring** = Regular performance monitoring

### Example:
```sql
-- Create a comprehensive feature monitoring function
CREATE OR REPLACE FUNCTION monitor_advanced_features()
RETURNS TABLE(
    feature_name TEXT,
    status TEXT,
    configuration TEXT,
    recommendation TEXT
) AS $$
BEGIN
    -- Check logical replication
    RETURN QUERY
    SELECT 
        'Logical Replication'::TEXT,
        CASE 
            WHEN EXISTS (SELECT 1 FROM pg_subscription) THEN 'ACTIVE'
            ELSE 'INACTIVE'
        END,
        (SELECT count(*) FROM pg_subscription)::TEXT || ' subscriptions',
        CASE 
            WHEN NOT EXISTS (SELECT 1 FROM pg_subscription) THEN 'Consider logical replication for data distribution'
            ELSE 'Logical replication is configured'
        END;
    
    -- Check foreign data wrappers
    RETURN QUERY
    SELECT 
        'Foreign Data Wrappers'::TEXT,
        CASE 
            WHEN EXISTS (SELECT 1 FROM pg_foreign_server) THEN 'ACTIVE'
            ELSE 'INACTIVE'
        END,
        (SELECT count(*) FROM pg_foreign_server)::TEXT || ' foreign servers',
        CASE 
            WHEN NOT EXISTS (SELECT 1 FROM pg_foreign_server) THEN 'Consider FDW for data federation'
            ELSE 'Foreign data wrappers are configured'
        END;
    
    -- Check parallel query processing
    RETURN QUERY
    SELECT 
        'Parallel Query Processing'::TEXT,
        CASE 
            WHEN (SELECT setting::int FROM pg_settings WHERE name = 'max_parallel_workers_per_gather') > 0 THEN 'ENABLED'
            ELSE 'DISABLED'
        END,
        'Max parallel workers: ' || (SELECT setting FROM pg_settings WHERE name = 'max_parallel_workers_per_gather'),
        CASE 
            WHEN (SELECT setting::int FROM pg_settings WHERE name = 'max_parallel_workers_per_gather') = 0 THEN 'Consider enabling parallel query processing'
            ELSE 'Parallel query processing is enabled'
        END;
    
    -- Check JIT compilation
    RETURN QUERY
    SELECT 
        'JIT Compilation'::TEXT,
        CASE 
            WHEN (SELECT setting FROM pg_settings WHERE name = 'jit') = 'on' THEN 'ENABLED'
            ELSE 'DISABLED'
        END,
        'JIT cost threshold: ' || (SELECT setting FROM pg_settings WHERE name = 'jit_above_cost'),
        CASE 
            WHEN (SELECT setting FROM pg_settings WHERE name = 'jit') = 'off' THEN 'Consider enabling JIT compilation for complex queries'
            ELSE 'JIT compilation is enabled'
        END;
END;
$$ LANGUAGE plpgsql;

-- Use the monitoring function
SELECT * FROM monitor_advanced_features();
```