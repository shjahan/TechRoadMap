# Section 24 – Troubleshooting and Problem Resolution

## 24.1 Troubleshooting Methodology

Troubleshooting methodology provides a systematic approach to identifying and resolving PostgreSQL issues.

### Troubleshooting Steps:
- **Problem Identification**: Recognizing and defining the issue
- **Information Gathering**: Collecting relevant data and logs
- **Root Cause Analysis**: Identifying the underlying cause
- **Solution Implementation**: Applying fixes and monitoring results

### Real-World Analogy:
Troubleshooting is like being a detective:
- **Problem Identification** = Recognizing a crime has occurred
- **Information Gathering** = Collecting evidence
- **Root Cause Analysis** = Determining who committed the crime
- **Solution Implementation** = Bringing the perpetrator to justice

### Example:
```sql
-- Create troubleshooting log table
CREATE TABLE troubleshooting_log (
    id SERIAL PRIMARY KEY,
    problem_description TEXT NOT NULL,
    symptoms TEXT,
    investigation_steps TEXT,
    root_cause TEXT,
    solution TEXT,
    status VARCHAR(20) DEFAULT 'open',
    created_at TIMESTAMP DEFAULT NOW(),
    resolved_at TIMESTAMP
);

-- Create problem identification function
CREATE OR REPLACE FUNCTION identify_database_problems()
RETURNS TABLE(
    problem_type TEXT,
    severity VARCHAR(20),
    description TEXT,
    affected_objects TEXT[]
) AS $$
BEGIN
    -- Check for connection issues
    RETURN QUERY
    SELECT 
        'Connection Issues'::TEXT,
        'HIGH'::VARCHAR(20),
        'High number of active connections'::TEXT,
        ARRAY['pg_stat_activity']::TEXT[]
    WHERE (SELECT COUNT(*) FROM pg_stat_activity) > 80;
    
    -- Check for performance issues
    RETURN QUERY
    SELECT 
        'Performance Issues'::TEXT,
        'MEDIUM'::VARCHAR(20),
        'Slow query execution detected'::TEXT,
        ARRAY['pg_stat_statements']::TEXT[]
    WHERE EXISTS (
        SELECT 1 FROM pg_stat_statements 
        WHERE mean_time > 1000
    );
    
    -- Check for storage issues
    RETURN QUERY
    SELECT 
        'Storage Issues'::TEXT,
        'HIGH'::VARCHAR(20),
        'Database size approaching limits'::TEXT,
        ARRAY['pg_database']::TEXT[]
    WHERE pg_database_size(current_database()) > 1000000000000; -- 1TB
END;
$$ LANGUAGE plpgsql;
```

## 24.2 Common Performance Issues

Common performance issues in PostgreSQL and their diagnostic approaches.

### Performance Issue Types:
- **Slow Queries**: Queries taking excessive time
- **High CPU Usage**: Excessive CPU consumption
- **Memory Issues**: Insufficient or excessive memory usage
- **I/O Bottlenecks**: Disk I/O performance problems

### Real-World Analogy:
Performance issues are like traffic problems:
- **Slow Queries** = Slow-moving traffic
- **High CPU Usage** = Overloaded engines
- **Memory Issues** = Insufficient fuel or storage
- **I/O Bottlenecks** = Narrow roads or traffic jams

### Example:
```sql
-- Create performance diagnostics function
CREATE OR REPLACE FUNCTION diagnose_performance_issues()
RETURNS TABLE(
    issue_type TEXT,
    severity VARCHAR(20),
    current_value TEXT,
    threshold_value TEXT,
    recommendation TEXT
) AS $$
BEGIN
    -- Check for slow queries
    RETURN QUERY
    SELECT 
        'Slow Queries'::TEXT,
        CASE 
            WHEN MAX(mean_time) > 5000 THEN 'CRITICAL'
            WHEN MAX(mean_time) > 1000 THEN 'HIGH'
            ELSE 'LOW'
        END,
        ROUND(MAX(mean_time), 2)::TEXT || ' ms',
        '1000 ms'::TEXT,
        CASE 
            WHEN MAX(mean_time) > 5000 THEN 'Immediate query optimization required'
            WHEN MAX(mean_time) > 1000 THEN 'Query optimization recommended'
            ELSE 'Query performance is acceptable'
        END
    FROM pg_stat_statements
    WHERE calls > 0;
    
    -- Check for high CPU usage
    RETURN QUERY
    SELECT 
        'High CPU Usage'::TEXT,
        CASE 
            WHEN COUNT(*) > 50 THEN 'HIGH'
            WHEN COUNT(*) > 20 THEN 'MEDIUM'
            ELSE 'LOW'
        END,
        COUNT(*)::TEXT || ' active queries',
        '20 active queries'::TEXT,
        CASE 
            WHEN COUNT(*) > 50 THEN 'Consider query optimization or connection pooling'
            WHEN COUNT(*) > 20 THEN 'Monitor query performance'
            ELSE 'CPU usage is normal'
        END
    FROM pg_stat_activity
    WHERE state = 'active';
    
    -- Check for memory issues
    RETURN QUERY
    SELECT 
        'Memory Usage'::TEXT,
        CASE 
            WHEN (blks_hit::float / (blks_hit + blks_read)) < 0.9 THEN 'HIGH'
            WHEN (blks_hit::float / (blks_hit + blks_read)) < 0.95 THEN 'MEDIUM'
            ELSE 'LOW'
        END,
        ROUND((blks_hit::float / (blks_hit + blks_read)) * 100, 2)::TEXT || '%',
        '95%'::TEXT,
        CASE 
            WHEN (blks_hit::float / (blks_hit + blks_read)) < 0.9 THEN 'Consider increasing shared_buffers'
            WHEN (blks_hit::float / (blks_hit + blks_read)) < 0.95 THEN 'Monitor cache hit ratio'
            ELSE 'Memory usage is optimal'
        END
    FROM pg_stat_database
    WHERE datname = current_database();
END;
$$ LANGUAGE plpgsql;
```

## 24.3 Connection Issues

Connection issues involve problems with database connectivity and session management.

### Connection Problem Types:
- **Connection Limits**: Too many concurrent connections
- **Connection Timeouts**: Connections timing out
- **Authentication Failures**: User authentication problems
- **Network Issues**: Network connectivity problems

### Real-World Analogy:
Connection issues are like phone system problems:
- **Connection Limits** = Busy signals
- **Connection Timeouts** = Dropped calls
- **Authentication Failures** = Wrong phone numbers
- **Network Issues** = Poor signal quality

### Example:
```sql
-- Create connection diagnostics function
CREATE OR REPLACE FUNCTION diagnose_connection_issues()
RETURNS TABLE(
    issue_type TEXT,
    current_value TEXT,
    max_value TEXT,
    recommendation TEXT
) AS $$
DECLARE
    max_conn INTEGER;
    current_conn INTEGER;
    active_conn INTEGER;
    idle_conn INTEGER;
BEGIN
    -- Get connection statistics
    SELECT setting::INTEGER INTO max_conn FROM pg_settings WHERE name = 'max_connections';
    SELECT COUNT(*) INTO current_conn FROM pg_stat_activity;
    SELECT COUNT(*) INTO active_conn FROM pg_stat_activity WHERE state = 'active';
    SELECT COUNT(*) INTO idle_conn FROM pg_stat_activity WHERE state = 'idle';
    
    -- Check connection limits
    RETURN QUERY
    SELECT 
        'Connection Usage'::TEXT,
        current_conn::TEXT || ' / ' || max_conn::TEXT,
        max_conn::TEXT,
        CASE 
            WHEN current_conn::float / max_conn > 0.8 THEN 'Consider connection pooling or increasing max_connections'
            ELSE 'Connection usage is normal'
        END;
    
    -- Check active connections
    RETURN QUERY
    SELECT 
        'Active Connections'::TEXT,
        active_conn::TEXT,
        '20'::TEXT,
        CASE 
            WHEN active_conn > 20 THEN 'High number of active connections - check for long-running queries'
            ELSE 'Active connection count is normal'
        END;
    
    -- Check idle connections
    RETURN QUERY
    SELECT 
        'Idle Connections'::TEXT,
        idle_conn::TEXT,
        '50'::TEXT,
        CASE 
            WHEN idle_conn > 50 THEN 'Many idle connections - consider connection pooling'
            ELSE 'Idle connection count is normal'
        END;
END;
$$ LANGUAGE plpgsql;

-- Create connection monitoring function
CREATE OR REPLACE FUNCTION monitor_connections()
RETURNS TABLE(
    username TEXT,
    application_name TEXT,
    client_addr INET,
    state TEXT,
    query_start TIMESTAMP,
    duration INTERVAL,
    query TEXT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        usename::TEXT,
        application_name::TEXT,
        client_addr,
        state::TEXT,
        query_start,
        NOW() - query_start as duration,
        LEFT(query, 100)::TEXT as query
    FROM pg_stat_activity
    WHERE usename IS NOT NULL
    ORDER BY query_start DESC;
END;
$$ LANGUAGE plpgsql;
```

## 24.4 Lock and Deadlock Issues

Lock and deadlock issues involve problems with concurrent access to database resources.

### Lock Problem Types:
- **Deadlocks**: Circular waiting for resources
- **Long-running Transactions**: Transactions holding locks too long
- **Lock Contention**: Multiple processes waiting for same resource
- **Lock Escalation**: Locks escalating to higher levels

### Real-World Analogy:
Lock issues are like traffic gridlocks:
- **Deadlocks** = Circular traffic jams
- **Long-running Transactions** = Slow-moving vehicles blocking traffic
- **Lock Contention** = Multiple vehicles waiting for same parking spot
- **Lock Escalation** = Traffic control measures

### Example:
```sql
-- Create lock monitoring function
CREATE OR REPLACE FUNCTION monitor_locks()
RETURNS TABLE(
    lock_type TEXT,
    database_name TEXT,
    table_name TEXT,
    mode TEXT,
    granted BOOLEAN,
    pid INTEGER,
    query TEXT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        l.locktype::TEXT,
        d.datname::TEXT,
        t.relname::TEXT,
        l.mode::TEXT,
        l.granted,
        l.pid,
        LEFT(a.query, 100)::TEXT as query
    FROM pg_locks l
    LEFT JOIN pg_database d ON l.database = d.oid
    LEFT JOIN pg_class t ON l.relation = t.oid
    LEFT JOIN pg_stat_activity a ON l.pid = a.pid
    WHERE l.database = (SELECT oid FROM pg_database WHERE datname = current_database())
    ORDER BY l.granted, l.pid;
END;
$$ LANGUAGE plpgsql;

-- Create deadlock detection function
CREATE OR REPLACE FUNCTION detect_deadlocks()
RETURNS TABLE(
    deadlock_info TEXT,
    recommendation TEXT
) AS $$
DECLARE
    lock_cycle RECORD;
BEGIN
    -- Check for potential deadlocks
    FOR lock_cycle IN
        SELECT 
            l1.pid as pid1,
            l2.pid as pid2,
            l1.mode as mode1,
            l2.mode as mode2,
            t1.relname as table1,
            t2.relname as table2
        FROM pg_locks l1
        JOIN pg_locks l2 ON l1.relation = l2.relation
        JOIN pg_class t1 ON l1.relation = t1.oid
        JOIN pg_class t2 ON l2.relation = t2.oid
        WHERE l1.pid != l2.pid
            AND l1.granted = true
            AND l2.granted = false
            AND l1.mode = 'ExclusiveLock'
            AND l2.mode = 'ExclusiveLock'
    LOOP
        RETURN QUERY
        SELECT 
            'Potential deadlock between PIDs ' || lock_cycle.pid1 || ' and ' || lock_cycle.pid2 || 
            ' on table ' || lock_cycle.table1::TEXT,
            'Consider transaction timeout or lock ordering'::TEXT;
    END LOOP;
    
    -- If no deadlocks found
    IF NOT FOUND THEN
        RETURN QUERY
        SELECT 
            'No deadlocks detected'::TEXT,
            'System is healthy'::TEXT;
    END IF;
END;
$$ LANGUAGE plpgsql;
```

## 24.5 Storage and Disk Issues

Storage and disk issues involve problems with database storage, disk space, and I/O performance.

### Storage Problem Types:
- **Disk Space**: Insufficient disk space
- **I/O Performance**: Slow disk I/O operations
- **Table Bloat**: Excessive table size due to dead tuples
- **Index Bloat**: Inefficient index storage

### Real-World Analogy:
Storage issues are like warehouse problems:
- **Disk Space** = Warehouse capacity
- **I/O Performance** = Loading and unloading efficiency
- **Table Bloat** = Cluttered storage areas
- **Index Bloat** = Inefficient organization

### Example:
```sql
-- Create storage diagnostics function
CREATE OR REPLACE FUNCTION diagnose_storage_issues()
RETURNS TABLE(
    issue_type TEXT,
    current_value TEXT,
    threshold_value TEXT,
    recommendation TEXT
) AS $$
BEGIN
    -- Check database size
    RETURN QUERY
    SELECT 
        'Database Size'::TEXT,
        pg_size_pretty(pg_database_size(current_database()))::TEXT,
        '1TB'::TEXT,
        CASE 
            WHEN pg_database_size(current_database()) > 1000000000000 THEN 'Consider archiving old data or partitioning'
            ELSE 'Database size is acceptable'
        END;
    
    -- Check for table bloat
    RETURN QUERY
    SELECT 
        'Table Bloat'::TEXT,
        ROUND(AVG(n_dead_tup::float / NULLIF(n_live_tup, 0)) * 100, 2)::TEXT || '%',
        '10%'::TEXT,
        CASE 
            WHEN AVG(n_dead_tup::float / NULLIF(n_live_tup, 0)) > 0.1 THEN 'Run VACUUM to clean up dead tuples'
            ELSE 'Table bloat is within acceptable limits'
        END
    FROM pg_stat_user_tables
    WHERE n_live_tup > 0;
    
    -- Check for index bloat
    RETURN QUERY
    SELECT 
        'Index Bloat'::TEXT,
        ROUND(AVG(pg_relation_size(indexrelid)::float / pg_relation_size(indrelid)) * 100, 2)::TEXT || '%',
        '20%'::TEXT,
        CASE 
            WHEN AVG(pg_relation_size(indexrelid)::float / pg_relation_size(indrelid)) > 0.2 THEN 'Consider rebuilding indexes'
            ELSE 'Index bloat is within acceptable limits'
        END
    FROM pg_stat_user_indexes
    WHERE pg_relation_size(indrelid) > 0;
END;
$$ LANGUAGE plpgsql;

-- Create table bloat analysis function
CREATE OR REPLACE FUNCTION analyze_table_bloat()
RETURNS TABLE(
    table_name TEXT,
    table_size TEXT,
    dead_tuple_percent DECIMAL(5,2),
    recommendation TEXT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        schemaname || '.' || tablename as table_name,
        pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as table_size,
        ROUND(n_dead_tup::float / NULLIF(n_live_tup, 0) * 100, 2) as dead_tuple_percent,
        CASE 
            WHEN n_dead_tup::float / NULLIF(n_live_tup, 0) > 0.1 THEN 'Run VACUUM FULL'
            WHEN n_dead_tup::float / NULLIF(n_live_tup, 0) > 0.05 THEN 'Run VACUUM'
            ELSE 'No action needed'
        END as recommendation
    FROM pg_stat_user_tables
    WHERE n_live_tup > 0
    ORDER BY n_dead_tup::float / NULLIF(n_live_tup, 0) DESC;
END;
$$ LANGUAGE plpgsql;
```

## 24.6 Memory Issues

Memory issues involve problems with PostgreSQL memory usage and configuration.

### Memory Problem Types:
- **Insufficient Memory**: Not enough memory allocated
- **Memory Leaks**: Memory not being released
- **Cache Issues**: Inefficient cache usage
- **Buffer Problems**: Buffer pool issues

### Real-World Analogy:
Memory issues are like fuel tank problems:
- **Insufficient Memory** = Not enough fuel
- **Memory Leaks** = Fuel leaks
- **Cache Issues** = Inefficient fuel usage
- **Buffer Problems** = Fuel distribution problems

### Example:
```sql
-- Create memory diagnostics function
CREATE OR REPLACE FUNCTION diagnose_memory_issues()
RETURNS TABLE(
    memory_component TEXT,
    current_value TEXT,
    recommended_value TEXT,
    status TEXT
) AS $$
DECLARE
    shared_buffers TEXT;
    work_mem TEXT;
    maintenance_work_mem TEXT;
    effective_cache_size TEXT;
    total_memory BIGINT;
BEGIN
    -- Get current memory settings
    SELECT setting INTO shared_buffers FROM pg_settings WHERE name = 'shared_buffers';
    SELECT setting INTO work_mem FROM pg_settings WHERE name = 'work_mem';
    SELECT setting INTO maintenance_work_mem FROM pg_settings WHERE name = 'maintenance_work_mem';
    SELECT setting INTO effective_cache_size FROM pg_settings WHERE name = 'effective_cache_size';
    
    -- Get total system memory (simplified)
    total_memory := 8589934592; -- 8GB example
    
    -- Check shared_buffers
    RETURN QUERY
    SELECT 
        'shared_buffers'::TEXT,
        shared_buffers,
        '25% of total memory'::TEXT,
        CASE 
            WHEN shared_buffers::BIGINT < total_memory * 0.2 THEN 'TOO_LOW'
            WHEN shared_buffers::BIGINT > total_memory * 0.4 THEN 'TOO_HIGH'
            ELSE 'OK'
        END;
    
    -- Check work_mem
    RETURN QUERY
    SELECT 
        'work_mem'::TEXT,
        work_mem,
        '4MB - 64MB'::TEXT,
        CASE 
            WHEN work_mem::BIGINT < 4194304 THEN 'TOO_LOW'
            WHEN work_mem::BIGINT > 67108864 THEN 'TOO_HIGH'
            ELSE 'OK'
        END;
    
    -- Check maintenance_work_mem
    RETURN QUERY
    SELECT 
        'maintenance_work_mem'::TEXT,
        maintenance_work_mem,
        '256MB - 1GB'::TEXT,
        CASE 
            WHEN maintenance_work_mem::BIGINT < 268435456 THEN 'TOO_LOW'
            WHEN maintenance_work_mem::BIGINT > 1073741824 THEN 'TOO_HIGH'
            ELSE 'OK'
        END;
    
    -- Check effective_cache_size
    RETURN QUERY
    SELECT 
        'effective_cache_size'::TEXT,
        effective_cache_size,
        '75% of total memory'::TEXT,
        CASE 
            WHEN effective_cache_size::BIGINT < total_memory * 0.5 THEN 'TOO_LOW'
            WHEN effective_cache_size::BIGINT > total_memory * 0.9 THEN 'TOO_HIGH'
            ELSE 'OK'
        END;
END;
$$ LANGUAGE plpgsql;
```

## 24.7 Query Performance Issues

Query performance issues involve problems with slow or inefficient queries.

### Query Problem Types:
- **Missing Indexes**: Queries not using indexes
- **Poor Query Plans**: Suboptimal execution plans
- **Resource Intensive Queries**: Queries consuming excessive resources
- **Blocking Queries**: Queries blocking other operations

### Real-World Analogy:
Query performance issues are like inefficient transportation:
- **Missing Indexes** = No direct routes
- **Poor Query Plans** = Inefficient routes
- **Resource Intensive Queries** = Heavy vehicles
- **Blocking Queries** = Traffic jams

### Example:
```sql
-- Create query performance analysis function
CREATE OR REPLACE FUNCTION analyze_query_performance()
RETURNS TABLE(
    query_id BIGINT,
    query_text TEXT,
    calls BIGINT,
    total_time DOUBLE PRECISION,
    mean_time DOUBLE PRECISION,
    rows BIGINT,
    performance_issue TEXT,
    recommendation TEXT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        qs.queryid,
        LEFT(qs.query, 100)::TEXT as query_text,
        qs.calls,
        qs.total_time,
        qs.mean_time,
        qs.rows,
        CASE 
            WHEN qs.mean_time > 5000 THEN 'Very Slow Query'
            WHEN qs.mean_time > 1000 THEN 'Slow Query'
            WHEN qs.calls > 10000 AND qs.mean_time > 100 THEN 'High Frequency Slow Query'
            WHEN qs.rows::float / qs.calls > 1000 THEN 'High Row Count Query'
            ELSE 'Normal Query'
        END as performance_issue,
        CASE 
            WHEN qs.mean_time > 5000 THEN 'Immediate optimization required'
            WHEN qs.mean_time > 1000 THEN 'Query optimization recommended'
            WHEN qs.calls > 10000 AND qs.mean_time > 100 THEN 'Consider caching or query optimization'
            WHEN qs.rows::float / qs.calls > 1000 THEN 'Consider adding LIMIT or filtering'
            ELSE 'Query performance is acceptable'
        END as recommendation
    FROM pg_stat_statements qs
    WHERE qs.calls > 0
    ORDER BY qs.mean_time DESC
    LIMIT 20;
END;
$$ LANGUAGE plpgsql;

-- Create missing index detection function
CREATE OR REPLACE FUNCTION detect_missing_indexes()
RETURNS TABLE(
    table_name TEXT,
    column_name TEXT,
    usage_count BIGINT,
    recommendation TEXT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        schemaname || '.' || tablename as table_name,
        'Multiple columns'::TEXT as column_name,
        seq_scan as usage_count,
        'Consider adding indexes for frequently queried columns'::TEXT as recommendation
    FROM pg_stat_user_tables
    WHERE seq_scan > idx_scan * 2
    ORDER BY seq_scan DESC;
END;
$$ LANGUAGE plpgsql;
```

## 24.8 Error Log Analysis

Error log analysis involves examining PostgreSQL logs to identify and resolve issues.

### Log Analysis Areas:
- **Error Messages**: Critical error identification
- **Warning Messages**: Potential issue warnings
- **Performance Logs**: Query performance information
- **Connection Logs**: Connection-related issues

### Real-World Analogy:
Error log analysis is like examining medical records:
- **Error Messages** = Critical symptoms
- **Warning Messages** = Early warning signs
- **Performance Logs** = Vital signs
- **Connection Logs** = Patient history

### Example:
```sql
-- Create log analysis function
CREATE OR REPLACE FUNCTION analyze_error_logs()
RETURNS TABLE(
    log_level TEXT,
    error_count BIGINT,
    common_errors TEXT[],
    recommendation TEXT
) AS $$
BEGIN
    -- Analyze error patterns (simplified example)
    RETURN QUERY
    SELECT 
        'ERROR'::TEXT,
        COUNT(*) as error_count,
        ARRAY['Connection timeout', 'Deadlock detected', 'Out of memory']::TEXT[],
        'Review error patterns and implement fixes'::TEXT
    FROM pg_stat_database
    WHERE datname = current_database();
    
    -- Analyze warning patterns
    RETURN QUERY
    SELECT 
        'WARNING'::TEXT,
        COUNT(*) as error_count,
        ARRAY['Long running query', 'High memory usage', 'Disk space low']::TEXT[],
        'Monitor warnings and take preventive action'::TEXT
    FROM pg_stat_activity
    WHERE state = 'active';
END;
$$ LANGUAGE plpgsql;
```

## 24.9 Recovery Procedures

Recovery procedures provide step-by-step processes for recovering from various database failures.

### Recovery Types:
- **Point-in-Time Recovery**: Recovery to specific time
- **Crash Recovery**: Recovery from system crashes
- **Data Corruption Recovery**: Recovery from data corruption
- **Replication Recovery**: Recovery from replication failures

### Real-World Analogy:
Recovery procedures are like emergency response protocols:
- **Point-in-Time Recovery** = Restoring to specific moment
- **Crash Recovery** = Emergency response
- **Data Corruption Recovery** = Damage repair
- **Replication Recovery** = Backup system activation

### Example:
```sql
-- Create recovery procedures table
CREATE TABLE recovery_procedures (
    id SERIAL PRIMARY KEY,
    procedure_name VARCHAR(100) NOT NULL,
    procedure_type VARCHAR(50) NOT NULL,
    steps TEXT[] NOT NULL,
    prerequisites TEXT[],
    estimated_time INTERVAL,
    risk_level VARCHAR(20) DEFAULT 'MEDIUM'
);

-- Insert recovery procedures
INSERT INTO recovery_procedures (procedure_name, procedure_type, steps, prerequisites, estimated_time, risk_level)
VALUES 
('Point-in-Time Recovery', 'Data Recovery', 
 ARRAY[
     'Stop PostgreSQL service',
     'Restore base backup',
     'Apply WAL files to target time',
     'Start PostgreSQL service',
     'Verify data integrity'
 ],
 ARRAY['Base backup available', 'WAL files available', 'Target time identified'],
 '2-4 hours', 'HIGH'),

('Crash Recovery', 'System Recovery',
 ARRAY[
     'Check system logs',
     'Verify disk space',
     'Start PostgreSQL service',
     'Check database consistency',
     'Run VACUUM if needed'
 ],
 ARRAY['System logs available', 'Disk space sufficient'],
 '30-60 minutes', 'MEDIUM'),

('Replication Recovery', 'High Availability',
 ARRAY[
     'Identify failed replica',
     'Stop replication',
     'Re-sync with primary',
     'Start replication',
     'Verify replication lag'
 ],
 ARRAY['Primary database healthy', 'Network connectivity'],
 '1-2 hours', 'LOW');

-- Create recovery execution function
CREATE OR REPLACE FUNCTION execute_recovery_procedure(procedure_id INTEGER)
RETURNS TABLE(
    step_number INTEGER,
    step_description TEXT,
    status TEXT,
    execution_time INTERVAL
) AS $$
DECLARE
    procedure_record RECORD;
    step TEXT;
    step_num INTEGER := 1;
    start_time TIMESTAMP;
    end_time TIMESTAMP;
BEGIN
    -- Get procedure details
    SELECT * INTO procedure_record
    FROM recovery_procedures
    WHERE id = procedure_id;
    
    -- Execute each step
    FOREACH step IN ARRAY procedure_record.steps
    LOOP
        start_time := clock_timestamp();
        
        -- Simulate step execution
        PERFORM pg_sleep(1);
        
        end_time := clock_timestamp();
        
        RETURN QUERY
        SELECT 
            step_num,
            step,
            'COMPLETED'::TEXT,
            end_time - start_time;
        
        step_num := step_num + 1;
    END LOOP;
END;
$$ LANGUAGE plpgsql;
```

## 24.10 Best Practices

Best practices for troubleshooting ensure effective problem resolution and prevention.

### Key Practices:
- **Documentation**: Document all troubleshooting steps
- **Prevention**: Implement preventive measures
- **Monitoring**: Continuous system monitoring
- **Training**: Regular team training

### Real-World Analogy:
Best practices are like following professional standards:
- **Documentation** = Keeping detailed records
- **Prevention** = Preventive maintenance
- **Monitoring** = Regular inspections
- **Training** = Professional development

### Example:
```sql
-- Create troubleshooting best practices monitoring function
CREATE OR REPLACE FUNCTION check_troubleshooting_best_practices()
RETURNS TABLE(
    practice_name TEXT,
    status TEXT,
    recommendation TEXT
) AS $$
BEGIN
    -- Check documentation
    RETURN QUERY
    SELECT 
        'Documentation'::TEXT,
        CASE 
            WHEN COUNT(*) > 0 THEN 'GOOD'
            ELSE 'NEEDS_ATTENTION'
        END,
        CASE 
            WHEN COUNT(*) > 0 THEN 'Troubleshooting procedures are documented'
            ELSE 'Document troubleshooting procedures'
        END
    FROM recovery_procedures;
    
    -- Check monitoring
    RETURN QUERY
    SELECT 
        'Monitoring'::TEXT,
        CASE 
            WHEN COUNT(*) > 0 THEN 'GOOD'
            ELSE 'NEEDS_ATTENTION'
        END,
        CASE 
            WHEN COUNT(*) > 0 THEN 'System monitoring is active'
            ELSE 'Implement comprehensive monitoring'
        END
    FROM pg_stat_activity
    WHERE state = 'active';
    
    -- Check preventive measures
    RETURN QUERY
    SELECT 
        'Prevention'::TEXT,
        CASE 
            WHEN COUNT(*) > 0 THEN 'GOOD'
            ELSE 'NEEDS_ATTENTION'
        END,
        CASE 
            WHEN COUNT(*) > 0 THEN 'Preventive measures are in place'
            ELSE 'Implement preventive measures'
        END
    FROM pg_stat_database
    WHERE datname = current_database();
END;
$$ LANGUAGE plpgsql;
```