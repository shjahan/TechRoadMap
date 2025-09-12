# Section 15 – Monitoring and Maintenance

## 15.1 PostgreSQL Monitoring Tools

PostgreSQL provides comprehensive monitoring tools for database administration.

### Monitoring Tools:
- **System Catalogs**: Built-in monitoring views
- **Statistics Views**: Performance statistics
- **Logging**: Comprehensive logging system
- **External Tools**: Third-party monitoring tools
- **Custom Monitoring**: Custom monitoring solutions

### Real-World Analogy:
Monitoring tools are like having a dashboard in a car:
- **System Catalogs** = Built-in gauges
- **Statistics Views** = Performance meters
- **Logging** = Trip recorder
- **External Tools** = GPS and navigation
- **Custom Monitoring** = Custom dashboard

### SQL Example - Monitoring Tools:
```sql
-- Check database statistics
SELECT 
    datname,
    numbackends,
    xact_commit,
    xact_rollback,
    blks_read,
    blks_hit,
    100.0 * blks_hit / (blks_hit + blks_read) AS hit_percent,
    tup_returned,
    tup_fetched,
    tup_inserted,
    tup_updated,
    tup_deleted
FROM pg_stat_database
WHERE datname = current_database();

-- Check table statistics
SELECT 
    schemaname,
    tablename,
    n_tup_ins,
    n_tup_upd,
    n_tup_del,
    n_live_tup,
    n_dead_tup,
    n_mod_since_analyze,
    last_vacuum,
    last_autovacuum,
    last_analyze,
    last_autoanalyze
FROM pg_stat_user_tables
ORDER BY n_live_tup DESC;

-- Check index statistics
SELECT 
    schemaname,
    tablename,
    indexname,
    idx_scan,
    idx_tup_read,
    idx_tup_fetch
FROM pg_stat_user_indexes
ORDER BY idx_scan DESC;

-- Check function statistics
SELECT 
    schemaname,
    funcname,
    calls,
    total_time,
    mean_time,
    stddev_time
FROM pg_stat_user_functions
ORDER BY total_time DESC;

-- Check connection statistics
SELECT 
    state,
    COUNT(*) as connection_count
FROM pg_stat_activity
GROUP BY state
ORDER BY connection_count DESC;
```

## 15.2 System Catalogs and Views

PostgreSQL system catalogs provide detailed information about database objects.

### System Catalogs:
- **pg_class**: Tables, indexes, sequences
- **pg_namespace**: Schemas
- **pg_attribute**: Table columns
- **pg_index**: Index information
- **pg_constraint**: Constraints

### Real-World Analogy:
System catalogs are like a detailed building directory:
- **pg_class** = Room listings
- **pg_namespace** = Floor plans
- **pg_attribute** = Room details
- **pg_index** = Room indexes
- **pg_constraint** = Building rules

### SQL Example - System Catalogs:
```sql
-- Check table information
SELECT 
    c.relname as table_name,
    n.nspname as schema_name,
    c.relkind,
    c.reltuples,
    c.relpages,
    pg_size_pretty(pg_total_relation_size(c.oid)) as size
FROM pg_class c
JOIN pg_namespace n ON c.relnamespace = n.oid
WHERE c.relkind = 'r'
AND n.nspname = 'public'
ORDER BY pg_total_relation_size(c.oid) DESC;

-- Check index information
SELECT 
    c.relname as index_name,
    n.nspname as schema_name,
    t.relname as table_name,
    c.relkind,
    c.reltuples,
    c.relpages,
    pg_size_pretty(pg_relation_size(c.oid)) as size
FROM pg_class c
JOIN pg_namespace n ON c.relnamespace = n.oid
JOIN pg_index i ON c.oid = i.indexrelid
JOIN pg_class t ON i.indrelid = t.oid
WHERE c.relkind = 'i'
AND n.nspname = 'public'
ORDER BY pg_relation_size(c.oid) DESC;

-- Check column information
SELECT 
    c.relname as table_name,
    n.nspname as schema_name,
    a.attname as column_name,
    a.attnum as column_number,
    t.typname as data_type,
    a.attnotnull as not_null,
    a.atthasdef as has_default
FROM pg_class c
JOIN pg_namespace n ON c.relnamespace = n.oid
JOIN pg_attribute a ON c.oid = a.attrelid
JOIN pg_type t ON a.atttypid = t.oid
WHERE c.relkind = 'r'
AND n.nspname = 'public'
AND a.attnum > 0
ORDER BY c.relname, a.attnum;

-- Check constraint information
SELECT 
    c.conname as constraint_name,
    c.contype as constraint_type,
    t.relname as table_name,
    n.nspname as schema_name
FROM pg_constraint c
JOIN pg_class t ON c.conrelid = t.oid
JOIN pg_namespace n ON t.relnamespace = n.oid
WHERE n.nspname = 'public'
ORDER BY t.relname, c.conname;
```

## 15.3 Performance Monitoring

Performance monitoring tracks database performance metrics.

### Performance Metrics:
- **Query Performance**: Query execution times
- **Resource Usage**: CPU, memory, I/O usage
- **Connection Metrics**: Connection counts and states
- **Lock Metrics**: Lock contention and waits
- **Cache Metrics**: Buffer cache hit ratios

### Real-World Analogy:
Performance monitoring is like monitoring a factory:
- **Query Performance** = Production line speed
- **Resource Usage** = Machine utilization
- **Connection Metrics** = Worker count
- **Lock Metrics** = Production bottlenecks
- **Cache Metrics** = Inventory efficiency

### SQL Example - Performance Monitoring:
```sql
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

-- Check resource usage
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

-- Check connection metrics
SELECT 
    state,
    COUNT(*) as connection_count,
    AVG(EXTRACT(EPOCH FROM (now() - backend_start))) as avg_connection_time
FROM pg_stat_activity
GROUP BY state
ORDER BY connection_count DESC;

-- Check lock metrics
SELECT 
    mode,
    COUNT(*) as lock_count
FROM pg_locks
GROUP BY mode
ORDER BY lock_count DESC;

-- Check cache metrics
SELECT 
    schemaname,
    tablename,
    heap_blks_read,
    heap_blks_hit,
    100.0 * heap_blks_hit / (heap_blks_hit + heap_blks_read) AS hit_percent
FROM pg_statio_user_tables
WHERE heap_blks_hit + heap_blks_read > 0
ORDER BY hit_percent ASC;
```

## 15.4 Log Analysis

Log analysis helps identify issues and optimize performance.

### Log Types:
- **Error Logs**: Error and warning messages
- **Query Logs**: SQL query logging
- **Connection Logs**: Connection and disconnection events
- **Checkpoint Logs**: Checkpoint events
- **WAL Logs**: Write-ahead log events

### Real-World Analogy:
Log analysis is like reviewing security camera footage:
- **Error Logs** = Security incidents
- **Query Logs** = Activity logs
- **Connection Logs** = Entry/exit logs
- **Checkpoint Logs** = System checkpoints
- **WAL Logs** = Change logs

### SQL Example - Log Analysis:
```sql
-- Check logging configuration
SELECT 
    name,
    setting,
    unit,
    context,
    short_desc
FROM pg_settings 
WHERE name IN (
    'log_destination',
    'logging_collector',
    'log_directory',
    'log_filename',
    'log_statement',
    'log_connections',
    'log_disconnections',
    'log_hostname',
    'log_line_prefix'
);

-- Check log destination
SHOW log_destination;

-- Check logging collector
SHOW logging_collector;

-- Check log directory
SHOW log_directory;

-- Check log filename
SHOW log_filename;

-- Check log statement
SHOW log_statement;

-- Check log connections
SHOW log_connections;

-- Check log disconnections
SHOW log_disconnections;

-- Check log hostname
SHOW log_hostname;

-- Check log line prefix
SHOW log_line_prefix;

-- Check current connections
SELECT 
    pid,
    usename,
    application_name,
    client_addr,
    client_port,
    backend_start,
    state,
    query
FROM pg_stat_activity
WHERE state = 'active'
ORDER BY backend_start DESC;
```

## 15.5 Database Statistics

Database statistics provide insights into database usage and performance.

### Statistics Types:
- **Table Statistics**: Table usage statistics
- **Index Statistics**: Index usage statistics
- **Function Statistics**: Function call statistics
- **Database Statistics**: Database-level statistics
- **System Statistics**: System-level statistics

### Real-World Analogy:
Database statistics are like business analytics:
- **Table Statistics** = Product sales data
- **Index Statistics** = Customer search patterns
- **Function Statistics** = Service usage data
- **Database Statistics** = Overall business metrics
- **System Statistics** = Infrastructure metrics

### SQL Example - Database Statistics:
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
    n_mod_since_analyze,
    last_vacuum,
    last_autovacuum,
    last_analyze,
    last_autoanalyze
FROM pg_stat_user_tables
ORDER BY n_live_tup DESC;

-- Check index statistics
SELECT 
    schemaname,
    tablename,
    indexname,
    idx_scan,
    idx_tup_read,
    idx_tup_fetch
FROM pg_stat_user_indexes
ORDER BY idx_scan DESC;

-- Check function statistics
SELECT 
    schemaname,
    funcname,
    calls,
    total_time,
    mean_time,
    stddev_time
FROM pg_stat_user_functions
ORDER BY total_time DESC;

-- Check database statistics
SELECT 
    datname,
    numbackends,
    xact_commit,
    xact_rollback,
    blks_read,
    blks_hit,
    100.0 * blks_hit / (blks_hit + blks_read) AS hit_percent,
    tup_returned,
    tup_fetched,
    tup_inserted,
    tup_updated,
    tup_deleted
FROM pg_stat_database
WHERE datname = current_database();

-- Check system statistics
SELECT 
    checkpoints_timed,
    checkpoints_req,
    checkpoint_write_time,
    checkpoint_sync_time,
    buffers_checkpoint,
    buffers_clean,
    maxwritten_clean,
    buffers_backend,
    buffers_backend_fsync,
    buffers_alloc
FROM pg_stat_bgwriter;
```

## 15.6 Maintenance Tasks

Regular maintenance tasks keep the database running optimally.

### Maintenance Tasks:
- **Vacuum**: Remove dead tuples
- **Analyze**: Update statistics
- **Reindex**: Rebuild indexes
- **Cluster**: Reorganize tables
- **Checkpoint**: Force WAL checkpoint

### Real-World Analogy:
Maintenance tasks are like regular building maintenance:
- **Vacuum** = Cleaning and organizing
- **Analyze** = Updating building records
- **Reindex** = Reorganizing filing systems
- **Cluster** = Rearranging furniture
- **Checkpoint** = System checkpoints

### SQL Example - Maintenance Tasks:
```sql
-- Check vacuum status
SELECT 
    schemaname,
    tablename,
    n_dead_tup,
    n_live_tup,
    n_dead_tup::float / n_live_tup::float * 100 as bloat_percent
FROM pg_stat_user_tables
WHERE n_live_tup > 0
ORDER BY bloat_percent DESC;

-- Check analyze status
SELECT 
    schemaname,
    tablename,
    last_analyze,
    last_autoanalyze,
    n_mod_since_analyze
FROM pg_stat_user_tables
ORDER BY n_mod_since_analyze DESC;

-- Check index bloat
SELECT 
    schemaname,
    tablename,
    indexname,
    pg_size_pretty(pg_relation_size(indexname::regclass)) as index_size
FROM pg_indexes
WHERE schemaname = 'public'
ORDER BY pg_relation_size(indexname::regclass) DESC;

-- Check table bloat
SELECT 
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as table_size
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;

-- Check sequence status
SELECT 
    schemaname,
    sequencename,
    last_value,
    start_value,
    increment_by,
    max_value,
    min_value,
    cache_value,
    is_cycled
FROM pg_sequences
WHERE schemaname = 'public'
ORDER BY sequencename;
```

## 15.7 Vacuum and Analyze

Vacuum and analyze are essential maintenance operations.

### Vacuum Operations:
- **VACUUM**: Remove dead tuples
- **VACUUM FULL**: Reclaim space and reorder
- **VACUUM ANALYZE**: Vacuum and update statistics
- **AUTOVACUUM**: Automatic vacuum operations
- **VACUUM VERBOSE**: Detailed vacuum information

### Real-World Analogy:
Vacuum and analyze are like housekeeping:
- **VACUUM** = Regular cleaning
- **VACUUM FULL** = Deep cleaning and reorganization
- **VACUUM ANALYZE** = Cleaning and updating records
- **AUTOVACUUM** = Automatic cleaning service
- **VACUUM VERBOSE** = Detailed cleaning report

### SQL Example - Vacuum and Analyze:
```sql
-- Check vacuum configuration
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
    n_dead_tup,
    n_live_tup,
    n_dead_tup::float / n_live_tup::float * 100 as bloat_percent,
    last_vacuum,
    last_autovacuum,
    last_analyze,
    last_autoanalyze
FROM pg_stat_user_tables
WHERE n_live_tup > 0
ORDER BY bloat_percent DESC;

-- Manual vacuum
VACUUM;

-- Full vacuum
VACUUM FULL;

-- Vacuum with analyze
VACUUM ANALYZE;

-- Vacuum specific table
VACUUM users;

-- Vacuum with options
VACUUM (VERBOSE, ANALYZE) users;

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

-- Check analyze progress
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
FROM pg_stat_progress_analyze;
```

## 15.8 Index Maintenance

Index maintenance ensures optimal query performance.

### Index Maintenance Tasks:
- **Index Rebuilding**: Rebuild fragmented indexes
- **Index Statistics**: Update index statistics
- **Index Monitoring**: Monitor index usage
- **Index Cleanup**: Remove unused indexes
- **Index Optimization**: Optimize index configuration

### Real-World Analogy:
Index maintenance is like maintaining a library catalog:
- **Index Rebuilding** = Reorganizing catalog
- **Index Statistics** = Updating usage data
- **Index Monitoring** = Tracking catalog usage
- **Index Cleanup** = Removing outdated entries
- **Index Optimization** = Improving catalog efficiency

### SQL Example - Index Maintenance:
```sql
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

-- Check unused indexes
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
    pg_stat_get_tuples_fetched(indexname::regclass) as tuples_fetched
FROM pg_indexes
WHERE schemaname = 'public'
ORDER BY pg_relation_size(indexname::regclass) DESC;

-- Rebuild specific index
REINDEX INDEX idx_users_email;

-- Rebuild all indexes on table
REINDEX TABLE users;

-- Rebuild all indexes in database
REINDEX DATABASE mydb;

-- Check index statistics
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

-- Check index size
SELECT 
    schemaname,
    tablename,
    indexname,
    pg_size_pretty(pg_relation_size(indexname::regclass)) as index_size
FROM pg_indexes
WHERE schemaname = 'public'
ORDER BY pg_relation_size(indexname::regclass) DESC;
```

## 15.9 Database Health Checks

Database health checks identify potential issues and performance problems.

### Health Check Areas:
- **Connection Health**: Connection counts and states
- **Query Health**: Query performance and patterns
- **Resource Health**: CPU, memory, and I/O usage
- **Storage Health**: Disk space and file system health
- **Replication Health**: Replication status and lag

### Real-World Analogy:
Database health checks are like medical checkups:
- **Connection Health** = Vital signs
- **Query Health** = Activity levels
- **Resource Health** = Organ function
- **Storage Health** = Physical condition
- **Replication Health** = Backup systems

### SQL Example - Database Health Checks:
```sql
-- Check connection health
SELECT 
    state,
    COUNT(*) as connection_count,
    AVG(EXTRACT(EPOCH FROM (now() - backend_start))) as avg_connection_time
FROM pg_stat_activity
GROUP BY state
ORDER BY connection_count DESC;

-- Check query health
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

-- Check resource health
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

-- Check storage health
SELECT 
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as table_size
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;

-- Check replication health
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
FROM pg_stat_replication
ORDER BY client_addr;
```

## 15.10 Alerting and Notifications

Alerting and notifications help administrators respond to issues quickly.

### Alerting Areas:
- **Performance Alerts**: Query performance issues
- **Resource Alerts**: CPU, memory, disk usage
- **Connection Alerts**: Connection count and state
- **Error Alerts**: Error and warning messages
- **Replication Alerts**: Replication lag and failures

### Real-World Analogy:
Alerting and notifications are like having a security system:
- **Performance Alerts** = Performance warnings
- **Resource Alerts** = Resource usage warnings
- **Connection Alerts** = Connection warnings
- **Error Alerts** = Error notifications
- **Replication Alerts** = Backup warnings

### SQL Example - Alerting and Notifications:
```sql
-- Check performance alerts
SELECT 
    query,
    calls,
    total_time,
    mean_time,
    stddev_time,
    rows
FROM pg_stat_statements
WHERE total_time > 1000 -- Alert if total time > 1000ms
ORDER BY total_time DESC;

-- Check resource alerts
SELECT 
    datname,
    numbackends,
    xact_commit,
    xact_rollback,
    blks_read,
    blks_hit,
    100.0 * blks_hit / (blks_hit + blks_read) AS hit_percent
FROM pg_stat_database
WHERE datname = current_database()
AND 100.0 * blks_hit / (blks_hit + blks_read) < 90; -- Alert if hit ratio < 90%

-- Check connection alerts
SELECT 
    state,
    COUNT(*) as connection_count
FROM pg_stat_activity
GROUP BY state
HAVING COUNT(*) > 100; -- Alert if connection count > 100

-- Check error alerts
SELECT 
    client_addr,
    usename,
    application_name,
    backend_start,
    state
FROM pg_stat_activity
WHERE state = 'idle'
ORDER BY backend_start DESC;

-- Check replication alerts
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
FROM pg_stat_replication
WHERE state != 'streaming' -- Alert if replication not streaming
ORDER BY client_addr;
```