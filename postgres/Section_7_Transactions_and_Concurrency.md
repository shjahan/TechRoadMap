# Section 7 – Transactions and Concurrency

## 7.1 ACID Properties in PostgreSQL

ACID properties ensure reliable database transactions: Atomicity, Consistency, Isolation, and Durability.

### ACID Properties:
- **Atomicity**: All operations in a transaction succeed or all fail
- **Consistency**: Database remains in a valid state after transaction
- **Isolation**: Concurrent transactions don't interfere with each other
- **Durability**: Committed changes persist even after system failure

### PostgreSQL ACID Implementation:
- **Atomicity**: Transaction rollback on errors
- **Consistency**: Constraint enforcement and validation
- **Isolation**: MVCC (Multi-Version Concurrency Control)
- **Durability**: WAL (Write-Ahead Logging)

### Real-World Analogy:
ACID properties are like a bank transaction:
- **Atomicity** = Either the entire transfer succeeds or nothing happens
- **Consistency** = Account balances remain valid after transfer
- **Isolation** = Multiple transfers don't interfere with each other
- **Durability** = Transfer records are permanently saved

### SQL Example - ACID Properties:
```sql
-- Create sample tables
CREATE TABLE accounts (
    account_id SERIAL PRIMARY KEY,
    account_name VARCHAR(100),
    balance NUMERIC(10,2) CHECK (balance >= 0)
);

CREATE TABLE transactions (
    transaction_id SERIAL PRIMARY KEY,
    from_account INTEGER REFERENCES accounts(account_id),
    to_account INTEGER REFERENCES accounts(account_id),
    amount NUMERIC(10,2) CHECK (amount > 0),
    transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert sample data
INSERT INTO accounts (account_name, balance) VALUES
    ('Alice Account', 1000.00),
    ('Bob Account', 500.00);

-- Atomicity example
BEGIN;
UPDATE accounts SET balance = balance - 100 WHERE account_id = 1;
UPDATE accounts SET balance = balance + 100 WHERE account_id = 2;
INSERT INTO transactions (from_account, to_account, amount) VALUES (1, 2, 100);
COMMIT;

-- Atomicity with rollback
BEGIN;
UPDATE accounts SET balance = balance - 200 WHERE account_id = 1;
UPDATE accounts SET balance = balance + 200 WHERE account_id = 2;
-- Simulate error
ROLLBACK;

-- Consistency example
BEGIN;
-- This will fail due to check constraint
UPDATE accounts SET balance = -50 WHERE account_id = 1;
ROLLBACK;

-- Isolation example (run in separate sessions)
-- Session 1
BEGIN;
UPDATE accounts SET balance = balance - 50 WHERE account_id = 1;
-- Don't commit yet

-- Session 2 (in another connection)
BEGIN;
SELECT balance FROM accounts WHERE account_id = 1;
-- Will see original value due to isolation
COMMIT;

-- Session 1
COMMIT;

-- Durability example
BEGIN;
UPDATE accounts SET balance = balance + 100 WHERE account_id = 1;
COMMIT;
-- Changes are now durable and will survive system restart
```

## 7.2 Transaction Isolation Levels

PostgreSQL supports different isolation levels that control how transactions interact with each other.

### Isolation Levels:
- **READ UNCOMMITTED**: Can read uncommitted changes (not supported in PostgreSQL)
- **READ COMMITTED**: Default level, can read committed changes
- **REPEATABLE READ**: Consistent reads within transaction
- **SERIALIZABLE**: Highest isolation, prevents all anomalies

### Isolation Level Characteristics:
- **Dirty Reads**: Reading uncommitted data
- **Non-Repeatable Reads**: Same query returns different results
- **Phantom Reads**: New rows appear in result set
- **Serialization Anomalies**: Inconsistent results from concurrent transactions

### Real-World Analogy:
Isolation levels are like different privacy settings:
- **READ UNCOMMITTED** = No privacy (not available)
- **READ COMMITTED** = Basic privacy (default)
- **REPEATABLE READ** = Enhanced privacy
- **SERIALIZABLE** = Maximum privacy

### SQL Example - Isolation Levels:
```sql
-- Create sample table
CREATE TABLE inventory (
    product_id SERIAL PRIMARY KEY,
    product_name VARCHAR(100),
    stock_quantity INTEGER,
    price NUMERIC(10,2)
);

INSERT INTO inventory (product_name, stock_quantity, price) VALUES
    ('Laptop', 10, 999.99),
    ('Mouse', 50, 25.99),
    ('Keyboard', 30, 75.99);

-- READ COMMITTED (default)
BEGIN;
SET TRANSACTION ISOLATION LEVEL READ COMMITTED;
SELECT stock_quantity FROM inventory WHERE product_id = 1;
-- Other session can modify data here
SELECT stock_quantity FROM inventory WHERE product_id = 1;
COMMIT;

-- REPEATABLE READ
BEGIN;
SET TRANSACTION ISOLATION LEVEL REPEATABLE READ;
SELECT stock_quantity FROM inventory WHERE product_id = 1;
-- Other session cannot modify data here
SELECT stock_quantity FROM inventory WHERE product_id = 1;
COMMIT;

-- SERIALIZABLE
BEGIN;
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;
SELECT SUM(stock_quantity) FROM inventory;
-- Other session cannot modify data here
SELECT SUM(stock_quantity) FROM inventory;
COMMIT;

-- Demonstrate non-repeatable read
-- Session 1
BEGIN;
SELECT stock_quantity FROM inventory WHERE product_id = 1;
-- Wait for other session to update
SELECT stock_quantity FROM inventory WHERE product_id = 1;
COMMIT;

-- Session 2 (in another connection)
BEGIN;
UPDATE inventory SET stock_quantity = stock_quantity - 1 WHERE product_id = 1;
COMMIT;

-- Demonstrate phantom read
-- Session 1
BEGIN;
SELECT COUNT(*) FROM inventory;
-- Wait for other session to insert
SELECT COUNT(*) FROM inventory;
COMMIT;

-- Session 2 (in another connection)
BEGIN;
INSERT INTO inventory (product_name, stock_quantity, price) VALUES ('Monitor', 20, 299.99);
COMMIT;
```

## 7.3 MVCC (Multi-Version Concurrency Control)

MVCC allows multiple transactions to access the same data simultaneously without blocking each other.

### MVCC Concepts:
- **Versioning**: Multiple versions of each row
- **Visibility**: Each transaction sees consistent snapshot
- **No Locking**: Readers don't block writers
- **Write Conflicts**: Writers can conflict with each other
- **Vacuum**: Cleanup of old versions

### MVCC Benefits:
- **Concurrency**: High concurrent read performance
- **Consistency**: Consistent snapshots for each transaction
- **No Deadlocks**: Readers don't cause deadlocks
- **Scalability**: Better performance under load

### Real-World Analogy:
MVCC is like a version control system:
- **Versioning** = Multiple versions of files
- **Visibility** = Each user sees their own version
- **No Locking** = Users can read without waiting
- **Write Conflicts** = Users can't edit same file simultaneously
- **Vacuum** = Cleaning up old versions

### SQL Example - MVCC:
```sql
-- Create table for MVCC demonstration
CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    product_name VARCHAR(100),
    price NUMERIC(10,2),
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO products (product_name, price) VALUES
    ('Laptop', 999.99),
    ('Mouse', 25.99),
    ('Keyboard', 75.99);

-- MVCC demonstration
-- Session 1: Start transaction
BEGIN;
SELECT product_name, price FROM products WHERE product_id = 1;

-- Session 2: Update in another transaction
BEGIN;
UPDATE products SET price = 1099.99 WHERE product_id = 1;
COMMIT;

-- Session 1: Still sees original price
SELECT product_name, price FROM products WHERE product_id = 1;
COMMIT;

-- MVCC with row versioning
-- Session 1: Long-running transaction
BEGIN;
SELECT product_name, price FROM products WHERE product_id = 1;
-- Wait for other session to update
SELECT product_name, price FROM products WHERE product_id = 1;
COMMIT;

-- Session 2: Update and commit
BEGIN;
UPDATE products SET price = 1199.99 WHERE product_id = 1;
COMMIT;

-- Check row versions
SELECT 
    xmin,
    xmax,
    cmin,
    cmax,
    product_name,
    price
FROM products 
WHERE product_id = 1;

-- MVCC with concurrent updates
-- Session 1
BEGIN;
UPDATE products SET price = price + 100 WHERE product_id = 1;
-- Don't commit yet

-- Session 2
BEGIN;
UPDATE products SET price = price * 1.1 WHERE product_id = 1;
-- This will wait for session 1 to commit or rollback
COMMIT;

-- Session 1
COMMIT;
```

## 7.4 Locking Mechanisms

PostgreSQL uses various locking mechanisms to control access to database objects.

### Lock Types:
- **Table Locks**: Lock entire tables
- **Row Locks**: Lock individual rows
- **Page Locks**: Lock data pages
- **Advisory Locks**: Application-level locks
- **Deadlock Detection**: Automatic deadlock resolution

### Lock Modes:
- **ACCESS SHARE**: Lightest lock, allows concurrent reads
- **ROW SHARE**: Allows concurrent reads, blocks exclusive locks
- **ROW EXCLUSIVE**: Allows concurrent reads, blocks other exclusive locks
- **SHARE UPDATE EXCLUSIVE**: Allows concurrent reads, blocks other share locks
- **SHARE**: Allows concurrent reads, blocks all writes
- **SHARE ROW EXCLUSIVE**: Allows concurrent reads, blocks other share locks
- **EXCLUSIVE**: Blocks all other locks except ACCESS SHARE
- **ACCESS EXCLUSIVE**: Blocks all other locks

### Real-World Analogy:
Locking mechanisms are like different types of access control:
- **Table Locks** = Locking entire building
- **Row Locks** = Locking individual rooms
- **Page Locks** = Locking floors
- **Advisory Locks** = Custom access rules
- **Deadlock Detection** = Automatic conflict resolution

### SQL Example - Locking Mechanisms:
```sql
-- Create table for locking demonstration
CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    customer_id INTEGER,
    order_date DATE,
    total_amount NUMERIC(10,2),
    status VARCHAR(20)
);

INSERT INTO orders (customer_id, order_date, total_amount, status) VALUES
    (1, '2024-01-15', 150.00, 'pending'),
    (2, '2024-01-16', 299.99, 'pending'),
    (3, '2024-01-17', 75.50, 'pending');

-- Table locks
BEGIN;
LOCK TABLE orders IN SHARE MODE;
SELECT COUNT(*) FROM orders;
-- Other sessions can read but not write
COMMIT;

-- Row locks
BEGIN;
SELECT * FROM orders WHERE order_id = 1 FOR UPDATE;
-- Other sessions cannot update this row
COMMIT;

-- Advisory locks
SELECT pg_advisory_lock(12345);
-- Other sessions cannot acquire same advisory lock
SELECT pg_advisory_unlock(12345);

-- Deadlock demonstration
-- Session 1
BEGIN;
UPDATE orders SET status = 'processing' WHERE order_id = 1;
-- Wait for session 2
UPDATE orders SET status = 'shipped' WHERE order_id = 2;
COMMIT;

-- Session 2
BEGIN;
UPDATE orders SET status = 'processing' WHERE order_id = 2;
-- Wait for session 1
UPDATE orders SET status = 'shipped' WHERE order_id = 1;
COMMIT;

-- Check current locks
SELECT 
    locktype,
    database,
    relation,
    page,
    tuple,
    virtualxid,
    transactionid,
    classid,
    objid,
    objsubid,
    virtualtransaction,
    pid,
    mode,
    granted
FROM pg_locks 
WHERE relation IS NOT NULL
ORDER BY relation, mode;

-- Check lock waits
SELECT 
    blocked_locks.pid AS blocked_pid,
    blocked_activity.usename AS blocked_user,
    blocking_locks.pid AS blocking_pid,
    blocking_activity.usename AS blocking_user,
    blocked_activity.query AS blocked_statement,
    blocking_activity.query AS current_statement_in_blocking_process
FROM pg_catalog.pg_locks blocked_locks
JOIN pg_catalog.pg_stat_activity blocked_activity ON blocked_activity.pid = blocked_locks.pid
JOIN pg_catalog.pg_locks blocking_locks ON blocking_locks.locktype = blocked_locks.locktype
    AND blocking_locks.database IS NOT DISTINCT FROM blocked_locks.database
    AND blocking_locks.relation IS NOT DISTINCT FROM blocked_locks.relation
    AND blocking_locks.page IS NOT DISTINCT FROM blocked_locks.page
    AND blocking_locks.tuple IS NOT DISTINCT FROM blocked_locks.tuple
    AND blocking_locks.virtualxid IS NOT DISTINCT FROM blocked_locks.virtualxid
    AND blocking_locks.transactionid IS NOT DISTINCT FROM blocked_locks.transactionid
    AND blocking_locks.classid IS NOT DISTINCT FROM blocked_locks.classid
    AND blocking_locks.objid IS NOT DISTINCT FROM blocked_locks.objid
    AND blocking_locks.objsubid IS NOT DISTINCT FROM blocked_locks.objsubid
    AND blocking_locks.pid != blocked_locks.pid
JOIN pg_catalog.pg_stat_activity blocking_activity ON blocking_activity.pid = blocking_locks.pid
WHERE NOT blocked_locks.granted;
```

## 7.5 Deadlock Detection and Prevention

PostgreSQL automatically detects and resolves deadlocks by aborting one of the conflicting transactions.

### Deadlock Detection:
- **Automatic**: PostgreSQL detects deadlocks automatically
- **Timeout**: Configurable deadlock detection timeout
- **Victim Selection**: Chooses transaction to abort
- **Rollback**: Aborted transaction is rolled back
- **Retry**: Application can retry the transaction

### Deadlock Prevention:
- **Lock Ordering**: Acquire locks in consistent order
- **Short Transactions**: Minimize lock duration
- **Index Usage**: Use indexes to reduce lock scope
- **Advisory Locks**: Use application-level locking
- **Timeout Settings**: Configure appropriate timeouts

### Real-World Analogy:
Deadlock detection is like traffic management:
- **Automatic** = Traffic lights automatically resolve conflicts
- **Timeout** = Maximum wait time before intervention
- **Victim Selection** = Choosing which car to move
- **Rollback** = Moving car back to previous position
- **Retry** = Trying the route again

### SQL Example - Deadlock Detection:
```sql
-- Create tables for deadlock demonstration
CREATE TABLE accounts (
    account_id SERIAL PRIMARY KEY,
    account_name VARCHAR(100),
    balance NUMERIC(10,2)
);

CREATE TABLE transactions (
    transaction_id SERIAL PRIMARY KEY,
    from_account INTEGER REFERENCES accounts(account_id),
    to_account INTEGER REFERENCES accounts(account_id),
    amount NUMERIC(10,2)
);

INSERT INTO accounts (account_name, balance) VALUES
    ('Alice Account', 1000.00),
    ('Bob Account', 500.00);

-- Deadlock scenario
-- Session 1
BEGIN;
UPDATE accounts SET balance = balance - 100 WHERE account_id = 1;
-- Wait for session 2
UPDATE accounts SET balance = balance + 100 WHERE account_id = 2;
COMMIT;

-- Session 2
BEGIN;
UPDATE accounts SET balance = balance - 50 WHERE account_id = 2;
-- Wait for session 1
UPDATE accounts SET balance = balance + 50 WHERE account_id = 1;
COMMIT;

-- Deadlock prevention with lock ordering
-- Session 1
BEGIN;
UPDATE accounts SET balance = balance - 100 WHERE account_id = 1;
UPDATE accounts SET balance = balance + 100 WHERE account_id = 2;
COMMIT;

-- Session 2
BEGIN;
UPDATE accounts SET balance = balance - 50 WHERE account_id = 1;
UPDATE accounts SET balance = balance + 50 WHERE account_id = 2;
COMMIT;

-- Deadlock prevention with advisory locks
-- Session 1
BEGIN;
SELECT pg_advisory_lock(1);
SELECT pg_advisory_lock(2);
UPDATE accounts SET balance = balance - 100 WHERE account_id = 1;
UPDATE accounts SET balance = balance + 100 WHERE account_id = 2;
SELECT pg_advisory_unlock(1);
SELECT pg_advisory_unlock(2);
COMMIT;

-- Session 2
BEGIN;
SELECT pg_advisory_lock(1);
SELECT pg_advisory_lock(2);
UPDATE accounts SET balance = balance - 50 WHERE account_id = 2;
UPDATE accounts SET balance = balance + 50 WHERE account_id = 1;
SELECT pg_advisory_unlock(1);
SELECT pg_advisory_unlock(2);
COMMIT;

-- Check deadlock statistics
SELECT 
    datname,
    deadlocks
FROM pg_stat_database 
WHERE datname = current_database();

-- Configure deadlock detection timeout
SHOW deadlock_timeout;
SET deadlock_timeout = '1s';
SHOW deadlock_timeout;
```

## 7.6 Serializable Snapshot Isolation (SSI)

SSI provides the highest isolation level by preventing all serialization anomalies.

### SSI Features:
- **Serialization Anomalies**: Prevents all types of anomalies
- **Conflict Detection**: Detects read-write conflicts
- **Abort and Retry**: Aborts conflicting transactions
- **Performance**: Higher overhead than other isolation levels
- **Consistency**: Ensures serializable execution

### SSI Use Cases:
- **Financial Systems**: Critical for financial transactions
- **Audit Systems**: Ensures data consistency
- **Complex Queries**: Multi-table operations
- **Data Integrity**: When consistency is paramount

### Real-World Analogy:
SSI is like having a strict traffic controller:
- **Serialization Anomalies** = Preventing all traffic conflicts
- **Conflict Detection** = Detecting potential collisions
- **Abort and Retry** = Stopping and restarting traffic
- **Performance** = Slower but safer traffic flow
- **Consistency** = Ensuring smooth traffic flow

### SQL Example - Serializable Snapshot Isolation:
```sql
-- Create table for SSI demonstration
CREATE TABLE inventory (
    product_id SERIAL PRIMARY KEY,
    product_name VARCHAR(100),
    stock_quantity INTEGER,
    reserved_quantity INTEGER DEFAULT 0
);

INSERT INTO inventory (product_name, stock_quantity) VALUES
    ('Laptop', 10),
    ('Mouse', 50),
    ('Keyboard', 30);

-- SSI demonstration
-- Session 1
BEGIN;
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;
SELECT stock_quantity FROM inventory WHERE product_id = 1;
-- Wait for session 2
UPDATE inventory SET stock_quantity = stock_quantity - 1 WHERE product_id = 1;
COMMIT;

-- Session 2
BEGIN;
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;
SELECT stock_quantity FROM inventory WHERE product_id = 1;
-- Wait for session 1
UPDATE inventory SET stock_quantity = stock_quantity - 1 WHERE product_id = 1;
COMMIT;

-- SSI with conflict detection
-- Session 1
BEGIN;
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;
SELECT SUM(stock_quantity) FROM inventory;
-- Wait for session 2
UPDATE inventory SET stock_quantity = stock_quantity - 1 WHERE product_id = 1;
COMMIT;

-- Session 2
BEGIN;
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;
SELECT SUM(stock_quantity) FROM inventory;
-- Wait for session 1
UPDATE inventory SET stock_quantity = stock_quantity - 1 WHERE product_id = 2;
COMMIT;

-- SSI with retry logic
DO $$
DECLARE
    retry_count INTEGER := 0;
    max_retries INTEGER := 3;
BEGIN
    LOOP
        BEGIN
            -- Start serializable transaction
            BEGIN;
            SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;
            
            -- Perform operations
            UPDATE inventory SET stock_quantity = stock_quantity - 1 WHERE product_id = 1;
            UPDATE inventory SET reserved_quantity = reserved_quantity + 1 WHERE product_id = 1;
            
            COMMIT;
            EXIT; -- Success, exit loop
            
        EXCEPTION
            WHEN serialization_failure THEN
                ROLLBACK;
                retry_count := retry_count + 1;
                IF retry_count >= max_retries THEN
                    RAISE EXCEPTION 'Max retries exceeded';
                END IF;
                -- Wait before retry
                PERFORM pg_sleep(0.1);
        END;
    END LOOP;
END $$;
```

## 7.7 Advisory Locks

Advisory locks provide application-level locking mechanisms for coordinating access to resources.

### Advisory Lock Types:
- **Session-Level**: Locks that persist for the session
- **Transaction-Level**: Locks that are released at transaction end
- **Numeric**: Integer-based lock identifiers
- **String**: Text-based lock identifiers
- **Exclusive**: Only one session can hold the lock
- **Shared**: Multiple sessions can hold the lock

### Advisory Lock Use Cases:
- **Resource Coordination**: Coordinating access to external resources
- **Batch Processing**: Preventing duplicate batch processing
- **Maintenance Tasks**: Coordinating maintenance operations
- **Data Migration**: Coordinating data movement
- **Scheduled Jobs**: Preventing overlapping job execution

### Real-World Analogy:
Advisory locks are like reservation systems:
- **Session-Level** = Long-term reservations
- **Transaction-Level** = Short-term reservations
- **Numeric** = Reservation numbers
- **String** = Reservation names
- **Exclusive** = Private reservations
- **Shared** = Group reservations

### SQL Example - Advisory Locks:
```sql
-- Session-level advisory locks
SELECT pg_advisory_lock(12345);
-- Other sessions cannot acquire this lock
SELECT pg_advisory_unlock(12345);

-- Transaction-level advisory locks
BEGIN;
SELECT pg_advisory_xact_lock(12345);
-- Lock is automatically released at transaction end
COMMIT;

-- String-based advisory locks
SELECT pg_advisory_lock('maintenance_task');
SELECT pg_advisory_unlock('maintenance_task');

-- Shared advisory locks
SELECT pg_advisory_lock_shared(12345);
-- Multiple sessions can acquire shared lock
SELECT pg_advisory_unlock_shared(12345);

-- Advisory lock with timeout
SELECT pg_advisory_lock(12345);
-- Try to acquire lock with timeout
SELECT pg_try_advisory_lock(12345, 5000); -- 5 second timeout

-- Check advisory locks
SELECT 
    locktype,
    database,
    classid,
    objid,
    objsubid,
    virtualtransaction,
    pid,
    mode,
    granted
FROM pg_locks 
WHERE locktype = 'advisory'
ORDER BY classid, objid;

-- Advisory lock for batch processing
DO $$
DECLARE
    lock_acquired BOOLEAN;
BEGIN
    -- Try to acquire lock for batch processing
    SELECT pg_try_advisory_lock('batch_processing') INTO lock_acquired;
    
    IF lock_acquired THEN
        RAISE NOTICE 'Batch processing started';
        -- Perform batch processing
        PERFORM pg_sleep(5); -- Simulate work
        RAISE NOTICE 'Batch processing completed';
        -- Release lock
        PERFORM pg_advisory_unlock('batch_processing');
    ELSE
        RAISE NOTICE 'Batch processing already running, skipping';
    END IF;
END $$;

-- Advisory lock for maintenance tasks
DO $$
DECLARE
    lock_acquired BOOLEAN;
BEGIN
    -- Try to acquire lock for maintenance
    SELECT pg_try_advisory_xact_lock('maintenance') INTO lock_acquired;
    
    IF lock_acquired THEN
        RAISE NOTICE 'Maintenance started';
        -- Perform maintenance
        PERFORM pg_sleep(3); -- Simulate work
        RAISE NOTICE 'Maintenance completed';
        -- Lock is automatically released at transaction end
    ELSE
        RAISE NOTICE 'Maintenance already running, skipping';
    END IF;
END $$;
```

## 7.8 Transaction Logging (WAL)

WAL (Write-Ahead Logging) ensures data durability by logging changes before they are written to disk.

### WAL Concepts:
- **Write-Ahead**: Changes are logged before being written to data files
- **Crash Recovery**: WAL is used to recover from crashes
- **Point-in-Time Recovery**: WAL enables recovery to specific points
- **Replication**: WAL is used for streaming replication
- **Archiving**: WAL files can be archived for long-term storage

### WAL Configuration:
- **wal_level**: Level of WAL logging
- **max_wal_size**: Maximum size of WAL files
- **min_wal_size**: Minimum size of WAL files
- **checkpoint_segments**: Number of WAL segments between checkpoints
- **archive_mode**: Enable WAL archiving

### Real-World Analogy:
WAL is like a flight data recorder:
- **Write-Ahead** = Recording before taking action
- **Crash Recovery** = Using recordings to reconstruct events
- **Point-in-Time Recovery** = Replaying to specific moments
- **Replication** = Sharing recordings with other systems
- **Archiving** = Storing recordings for future reference

### SQL Example - WAL Configuration:
```sql
-- Check WAL configuration
SELECT 
    name,
    setting,
    unit,
    context,
    short_desc
FROM pg_settings 
WHERE name LIKE 'wal_%' OR name LIKE '%wal%'
ORDER BY name;

-- Check WAL level
SHOW wal_level;

-- Check WAL size settings
SHOW max_wal_size;
SHOW min_wal_size;

-- Check checkpoint settings
SHOW checkpoint_segments;
SHOW checkpoint_timeout;

-- Check archive settings
SHOW archive_mode;
SHOW archive_command;

-- Monitor WAL activity
SELECT 
    pg_current_wal_lsn() as current_wal_lsn,
    pg_walfile_name(pg_current_wal_lsn()) as current_wal_file;

-- Check WAL statistics
SELECT 
    wal_records,
    wal_fpi,
    wal_bytes,
    wal_buffers_full,
    wal_write,
    wal_sync,
    wal_write_time,
    wal_sync_time
FROM pg_stat_wal;

-- Check WAL file information
SELECT 
    name,
    size,
    modification
FROM pg_ls_waldir()
ORDER BY modification DESC
LIMIT 10;

-- Force WAL switch
SELECT pg_switch_wal();

-- Check WAL replication lag
SELECT 
    client_addr,
    state,
    sent_lsn,
    write_lsn,
    flush_lsn,
    replay_lsn,
    write_lag,
    flush_lag,
    replay_lag
FROM pg_stat_replication;
```

## 7.9 Vacuum and Autovacuum

Vacuum and autovacuum clean up dead tuples and maintain database performance.

### Vacuum Functions:
- **Dead Tuple Cleanup**: Remove old row versions
- **Space Reclamation**: Free up space for reuse
- **Statistics Update**: Update table statistics
- **Index Cleanup**: Clean up index entries
- **Free Space Map**: Update free space information

### Autovacuum Features:
- **Automatic**: Runs automatically in background
- **Configurable**: Many configuration parameters
- **Monitoring**: Built-in monitoring and logging
- **Tuning**: Can be tuned for specific workloads
- **Maintenance**: Keeps database healthy

### Real-World Analogy:
Vacuum is like housekeeping:
- **Dead Tuple Cleanup** = Removing old, unused items
- **Space Reclamation** = Organizing storage space
- **Statistics Update** = Updating inventory records
- **Index Cleanup** = Organizing reference materials
- **Free Space Map** = Tracking available space

### SQL Example - Vacuum and Autovacuum:
```sql
-- Check autovacuum settings
SELECT 
    name,
    setting,
    unit,
    context,
    short_desc
FROM pg_settings 
WHERE name LIKE 'autovacuum%'
ORDER BY name;

-- Check autovacuum status
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
ORDER BY n_dead_tup DESC;

-- Manual vacuum
VACUUM orders;

-- Full vacuum (locks table)
VACUUM FULL orders;

-- Analyze table
ANALYZE orders;

-- Vacuum with options
VACUUM (VERBOSE, ANALYZE) orders;

-- Vacuum specific columns
VACUUM (ANALYZE) orders (customer_id, order_date);

-- Check vacuum progress
SELECT 
    pid,
    datname,
    phase,
    heap_blks_total,
    heap_blks_scanned,
    heap_blks_vacuumed,
    index_rebuild_count,
    max_dead_tuples,
    num_dead_tuples
FROM pg_stat_progress_vacuum;

-- Configure autovacuum for specific table
ALTER TABLE orders SET (autovacuum_vacuum_threshold = 1000);
ALTER TABLE orders SET (autovacuum_vacuum_scale_factor = 0.1);
ALTER TABLE orders SET (autovacuum_analyze_threshold = 500);
ALTER TABLE orders SET (autovacuum_analyze_scale_factor = 0.05);

-- Check table-specific autovacuum settings
SELECT 
    schemaname,
    tablename,
    attname,
    n_distinct,
    correlation
FROM pg_stats 
WHERE tablename = 'orders'
ORDER BY attname;

-- Monitor autovacuum activity
SELECT 
    schemaname,
    tablename,
    last_autovacuum,
    last_autoanalyze,
    autovacuum_count,
    autoanalyze_count
FROM pg_stat_user_tables 
WHERE autovacuum_count > 0 OR autoanalyze_count > 0
ORDER BY last_autovacuum DESC;
```

## 7.10 Hot Updates and HOT Pruning

HOT (Heap-Only Tuples) updates and pruning optimize UPDATE operations by avoiding index updates.

### HOT Concepts:
- **Heap-Only Tuples**: Updated tuples that don't require index updates
- **HOT Updates**: Updates that can be done without index changes
- **HOT Pruning**: Removal of old tuple versions
- **Index Maintenance**: Reduced index maintenance overhead
- **Performance**: Better UPDATE performance

### HOT Requirements:
- **Same Page**: New tuple must fit on same page as old tuple
- **No Index Changes**: No indexed columns can be modified
- **Free Space**: Sufficient free space on page
- **Compatible**: Only certain operations are HOT-compatible

### Real-World Analogy:
HOT updates are like updating a document in place:
- **Heap-Only Tuples** = Updated versions in same location
- **HOT Updates** = Changes that don't require reindexing
- **HOT Pruning** = Removing old versions
- **Index Maintenance** = Keeping references up to date
- **Performance** = Faster updates

### SQL Example - HOT Updates:
```sql
-- Create table for HOT demonstration
CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    product_name VARCHAR(100),
    price NUMERIC(10,2),
    description TEXT,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create index on non-updated column
CREATE INDEX idx_products_name ON products(product_name);

-- Insert sample data
INSERT INTO products (product_name, price, description) VALUES
    ('Laptop', 999.99, 'High-performance laptop'),
    ('Mouse', 25.99, 'Wireless mouse'),
    ('Keyboard', 75.99, 'Mechanical keyboard');

-- HOT update (only non-indexed columns)
UPDATE products 
SET description = 'Updated description', last_updated = CURRENT_TIMESTAMP 
WHERE product_id = 1;

-- Check if update was HOT
SELECT 
    schemaname,
    tablename,
    n_tup_hot_upd,
    n_tup_upd
FROM pg_stat_user_tables 
WHERE tablename = 'products';

-- Non-HOT update (indexed column changed)
UPDATE products 
SET product_name = 'Updated Laptop' 
WHERE product_id = 1;

-- Check HOT vs non-HOT updates
SELECT 
    schemaname,
    tablename,
    n_tup_hot_upd,
    n_tup_upd,
    n_tup_hot_upd::float / n_tup_upd::float * 100 as hot_percentage
FROM pg_stat_user_tables 
WHERE tablename = 'products';

-- Monitor HOT pruning
SELECT 
    schemaname,
    tablename,
    n_tup_hot_upd,
    n_tup_upd,
    n_dead_tup,
    last_vacuum,
    last_autovacuum
FROM pg_stat_user_tables 
WHERE tablename = 'products';

-- Force HOT pruning
VACUUM products;

-- Check after pruning
SELECT 
    schemaname,
    tablename,
    n_dead_tup,
    n_live_tup
FROM pg_stat_user_tables 
WHERE tablename = 'products';

-- Configure for better HOT updates
ALTER TABLE products SET (fillfactor = 90);

-- Check fillfactor
SELECT 
    schemaname,
    tablename,
    fillfactor
FROM pg_class c
JOIN pg_namespace n ON c.relnamespace = n.oid
WHERE c.relname = 'products';
```