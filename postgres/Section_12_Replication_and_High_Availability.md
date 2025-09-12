# Section 12 – Replication and High Availability

## 12.1 Replication Concepts

Replication creates copies of database data across multiple servers for redundancy and performance.

### Replication Types:
- **Physical Replication**: Copies physical data blocks
- **Logical Replication**: Copies logical changes
- **Synchronous Replication**: Waits for confirmation
- **Asynchronous Replication**: Doesn't wait for confirmation
- **Streaming Replication**: Continuous data streaming

### Real-World Analogy:
Replication is like having multiple copies of important documents:
- **Physical Replication** = Photocopying entire documents
- **Logical Replication** = Copying only changes
- **Synchronous Replication** = Waiting for confirmation
- **Asynchronous Replication** = Sending without waiting
- **Streaming Replication** = Continuous updates

### SQL Example - Replication Concepts:
```sql
-- Check replication status
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

-- Check WAL sender status
SELECT 
    pid,
    state,
    sent_lsn,
    write_lsn,
    flush_lsn,
    replay_lsn
FROM pg_stat_wal_sender;

-- Check replication slots
SELECT 
    slot_name,
    plugin,
    slot_type,
    database,
    active,
    xmin,
    catalog_xmin,
    restart_lsn,
    confirmed_flush_lsn
FROM pg_replication_slots;

-- Check WAL receiver status
SELECT 
    pid,
    status,
    receive_start_lsn,
    receive_start_tli,
    received_lsn,
    received_tli,
    last_msg_send_time,
    last_msg_receipt_time,
    latest_end_lsn,
    latest_end_time,
    slot_name,
    sender_host,
    sender_port,
    conninfo
FROM pg_stat_wal_receiver;
```

## 12.2 Streaming Replication

Streaming replication continuously streams WAL data from primary to standby servers.

### Streaming Replication Features:
- **Continuous Streaming**: Real-time data replication
- **WAL Shipping**: Ships WAL records as they're generated
- **Automatic Failover**: Automatic promotion of standby
- **Read Replicas**: Standby servers for read operations
- **Lag Monitoring**: Monitor replication lag

### Real-World Analogy:
Streaming replication is like live TV broadcasting:
- **Continuous Streaming** = Live transmission
- **WAL Shipping** = Sending video frames
- **Automatic Failover** = Switching to backup transmitter
- **Read Replicas** = Multiple TV sets
- **Lag Monitoring** = Checking signal delay

### SQL Example - Streaming Replication:
```sql
-- Primary server configuration
-- postgresql.conf
-- wal_level = replica
-- max_wal_senders = 3
-- max_replication_slots = 3
-- hot_standby = on

-- pg_hba.conf
-- host replication replicator 192.168.1.0/24 md5

-- Create replication user
CREATE USER replicator WITH REPLICATION LOGIN PASSWORD 'replication_password';

-- Create replication slot
SELECT pg_create_physical_replication_slot('standby_slot');

-- Check replication configuration
SHOW wal_level;
SHOW max_wal_senders;
SHOW max_replication_slots;
SHOW hot_standby;

-- Monitor replication
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

-- Check WAL generation
SELECT 
    pg_current_wal_lsn() as current_lsn,
    pg_walfile_name(pg_current_wal_lsn()) as current_wal_file;

-- Check replication lag
SELECT 
    client_addr,
    state,
    pg_wal_lsn_diff(pg_current_wal_lsn(), sent_lsn) as sent_lag,
    pg_wal_lsn_diff(pg_current_wal_lsn(), write_lsn) as write_lag,
    pg_wal_lsn_diff(pg_current_wal_lsn(), flush_lsn) as flush_lag,
    pg_wal_lsn_diff(pg_current_wal_lsn(), replay_lsn) as replay_lag
FROM pg_stat_replication;
```

## 12.3 Logical Replication

Logical replication replicates data changes at the logical level rather than physical level.

### Logical Replication Features:
- **Table-Level**: Replicate specific tables
- **Column-Level**: Replicate specific columns
- **Filtering**: Filter data during replication
- **Transformations**: Transform data during replication
- **Cross-Version**: Replicate between different PostgreSQL versions

### Real-World Analogy:
Logical replication is like selective document copying:
- **Table-Level** = Copying specific document types
- **Column-Level** = Copying specific sections
- **Filtering** = Only copying relevant information
- **Transformations** = Modifying data during copying
- **Cross-Version** = Copying between different systems

### SQL Example - Logical Replication:
```sql
-- Enable logical replication
-- postgresql.conf
-- wal_level = logical
-- max_replication_slots = 10
-- max_wal_senders = 10

-- Create publication
CREATE PUBLICATION my_publication FOR TABLE users, orders;

-- Add table to publication
ALTER PUBLICATION my_publication ADD TABLE products;

-- Remove table from publication
ALTER PUBLICATION my_publication DROP TABLE products;

-- Create subscription
CREATE SUBSCRIPTION my_subscription
CONNECTION 'host=192.168.1.100 port=5432 user=replicator password=replication_password dbname=mydb'
PUBLICATION my_publication;

-- Check publication status
SELECT 
    pubname,
    pubowner,
    puballtables,
    pubinsert,
    pubupdate,
    pubdelete,
    pubtruncate
FROM pg_publication;

-- Check subscription status
SELECT 
    subname,
    subowner,
    subenabled,
    subconninfo,
    subslotname,
    subsynccommit,
    subpublications
FROM pg_subscription;

-- Check replication status
SELECT 
    subname,
    subslotname,
    subenabled,
    subpublications
FROM pg_subscription;

-- Monitor logical replication
SELECT 
    pid,
    usename,
    application_name,
    client_addr,
    state,
    sent_lsn,
    write_lsn,
    flush_lsn,
    replay_lsn
FROM pg_stat_replication
WHERE application_name = 'my_subscription';
```

## 12.4 Synchronous vs Asynchronous Replication

PostgreSQL supports both synchronous and asynchronous replication modes.

### Synchronous Replication:
- **Data Safety**: Ensures data is written to standby
- **Performance Impact**: Slower write performance
- **Consistency**: Strong consistency guarantees
- **Failover**: Automatic failover capabilities
- **Use Cases**: Critical applications requiring data safety

### Asynchronous Replication:
- **Performance**: Better write performance
- **Data Risk**: Risk of data loss
- **Consistency**: Eventual consistency
- **Lag**: Replication lag possible
- **Use Cases**: High-performance applications

### Real-World Analogy:
Replication modes are like different communication methods:
- **Synchronous** = Registered mail (confirmation required)
- **Asynchronous** = Regular mail (no confirmation)
- **Data Safety** = Guaranteed delivery
- **Performance** = Speed of delivery
- **Consistency** = Delivery reliability

### SQL Example - Synchronous vs Asynchronous:
```sql
-- Check current replication mode
SELECT 
    name,
    setting,
    unit,
    context,
    short_desc
FROM pg_settings 
WHERE name IN ('synchronous_commit', 'synchronous_standby_names');

-- Configure synchronous replication
-- postgresql.conf
-- synchronous_commit = on
-- synchronous_standby_names = 'standby1,standby2'

-- Check synchronous standby names
SHOW synchronous_standby_names;

-- Check synchronous commit setting
SHOW synchronous_commit;

-- Monitor synchronous replication
SELECT 
    client_addr,
    state,
    sent_lsn,
    write_lsn,
    flush_lsn,
    replay_lsn,
    sync_state,
    sync_priority,
    sync_standby
FROM pg_stat_replication;

-- Check replication lag for synchronous replication
SELECT 
    client_addr,
    state,
    sync_state,
    pg_wal_lsn_diff(pg_current_wal_lsn(), sent_lsn) as sent_lag,
    pg_wal_lsn_diff(pg_current_wal_lsn(), write_lsn) as write_lag,
    pg_wal_lsn_diff(pg_current_wal_lsn(), flush_lsn) as flush_lag,
    pg_wal_lsn_diff(pg_current_wal_lsn(), replay_lsn) as replay_lag
FROM pg_stat_replication
WHERE sync_state = 'sync';

-- Configure asynchronous replication
-- postgresql.conf
-- synchronous_commit = off
-- synchronous_standby_names = ''

-- Check asynchronous replication performance
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
WHERE sync_state = 'async';
```

## 12.5 Failover and Switchover

Failover and switchover provide high availability by promoting standby servers.

### Failover:
- **Automatic**: Automatic promotion of standby
- **Manual**: Manual promotion of standby
- **Trigger**: Failure of primary server
- **Recovery**: Recovery of failed primary
- **Data Loss**: Potential data loss

### Switchover:
- **Planned**: Planned promotion of standby
- **Manual**: Manual promotion of standby
- **Trigger**: Maintenance or upgrade
- **Recovery**: Graceful transition
- **Data Loss**: No data loss

### Real-World Analogy:
Failover and switchover are like changing leadership:
- **Failover** = Emergency succession
- **Switchover** = Planned succession
- **Automatic** = Automatic succession
- **Manual** = Manual succession
- **Recovery** = Restoring original leader

### SQL Example - Failover and Switchover:
```sql
-- Check current server role
SELECT pg_is_in_recovery();

-- Check standby server status
SELECT 
    client_addr,
    state,
    sent_lsn,
    write_lsn,
    flush_lsn,
    replay_lsn
FROM pg_stat_replication;

-- Manual failover (on standby server)
-- pg_ctl promote -D /var/lib/postgresql/data

-- Check promotion status
SELECT pg_is_in_recovery();

-- Check WAL receiver status
SELECT 
    pid,
    status,
    receive_start_lsn,
    received_lsn,
    latest_end_lsn
FROM pg_stat_wal_receiver;

-- Check replication slots after failover
SELECT 
    slot_name,
    plugin,
    slot_type,
    database,
    active,
    xmin,
    catalog_xmin,
    restart_lsn,
    confirmed_flush_lsn
FROM pg_replication_slots;

-- Configure new primary for replication
-- postgresql.conf
-- wal_level = replica
-- max_wal_senders = 3
-- max_replication_slots = 3

-- Create replication slot
SELECT pg_create_physical_replication_slot('new_standby_slot');

-- Check replication configuration
SHOW wal_level;
SHOW max_wal_senders;
SHOW max_replication_slots;
```

## 12.6 Read Replicas

Read replicas provide read-only access to replicated data for load balancing.

### Read Replica Features:
- **Read-Only**: Cannot accept writes
- **Load Balancing**: Distribute read queries
- **Performance**: Improved read performance
- **Consistency**: Eventual consistency
- **Scaling**: Horizontal scaling for reads

### Real-World Analogy:
Read replicas are like having multiple reading rooms:
- **Read-Only** = Only for reading, not writing
- **Load Balancing** = Distributing readers
- **Performance** = Faster access to books
- **Consistency** = Eventually up-to-date
- **Scaling** = Adding more reading rooms

### SQL Example - Read Replicas:
```sql
-- Check if server is in recovery mode (read replica)
SELECT pg_is_in_recovery();

-- Check standby server status
SELECT 
    client_addr,
    state,
    sent_lsn,
    write_lsn,
    flush_lsn,
    replay_lsn
FROM pg_stat_replication;

-- Check WAL receiver status
SELECT 
    pid,
    status,
    receive_start_lsn,
    received_lsn,
    latest_end_lsn
FROM pg_stat_wal_receiver;

-- Check replication lag
SELECT 
    client_addr,
    state,
    pg_wal_lsn_diff(pg_current_wal_lsn(), sent_lsn) as sent_lag,
    pg_wal_lsn_diff(pg_current_wal_lsn(), write_lsn) as write_lag,
    pg_wal_lsn_diff(pg_current_wal_lsn(), flush_lsn) as flush_lag,
    pg_wal_lsn_diff(pg_current_wal_lsn(), replay_lsn) as replay_lag
FROM pg_stat_replication;

-- Check read replica performance
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

-- Check read replica queries
SELECT 
    query,
    calls,
    total_time,
    mean_time,
    rows
FROM pg_stat_statements
ORDER BY total_time DESC
LIMIT 10;
```

## 12.7 Cascading Replication

Cascading replication allows standby servers to act as replication sources.

### Cascading Replication Features:
- **Multi-Level**: Multiple levels of replication
- **Reduced Load**: Reduces load on primary
- **Network Efficiency**: Efficient network usage
- **Complexity**: More complex setup
- **Failure Points**: Additional failure points

### Real-World Analogy:
Cascading replication is like a chain of command:
- **Multi-Level** = Multiple levels of authority
- **Reduced Load** = Distributing responsibility
- **Network Efficiency** = Efficient communication
- **Complexity** = More complex organization
- **Failure Points** = More potential failure points

### SQL Example - Cascading Replication:
```sql
-- Check replication hierarchy
SELECT 
    client_addr,
    state,
    sent_lsn,
    write_lsn,
    flush_lsn,
    replay_lsn
FROM pg_stat_replication;

-- Check WAL sender status
SELECT 
    pid,
    state,
    sent_lsn,
    write_lsn,
    flush_lsn,
    replay_lsn
FROM pg_stat_wal_sender;

-- Check replication slots
SELECT 
    slot_name,
    plugin,
    slot_type,
    database,
    active,
    xmin,
    catalog_xmin,
    restart_lsn,
    confirmed_flush_lsn
FROM pg_replication_slots;

-- Monitor cascading replication
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

-- Check replication lag in cascading setup
SELECT 
    client_addr,
    state,
    pg_wal_lsn_diff(pg_current_wal_lsn(), sent_lsn) as sent_lag,
    pg_wal_lsn_diff(pg_current_wal_lsn(), write_lsn) as write_lag,
    pg_wal_lsn_diff(pg_current_wal_lsn(), flush_lsn) as flush_lag,
    pg_wal_lsn_diff(pg_current_wal_lsn(), replay_lsn) as replay_lag
FROM pg_stat_replication
ORDER BY client_addr;
```

## 12.8 Replication Monitoring

Monitoring replication is essential for maintaining high availability.

### Monitoring Metrics:
- **Replication Lag**: Time delay between primary and standby
- **Connection Status**: Status of replication connections
- **WAL Generation**: WAL generation rate
- **Slot Status**: Replication slot status
- **Performance**: Replication performance metrics

### Real-World Analogy:
Replication monitoring is like monitoring a communication system:
- **Replication Lag** = Communication delay
- **Connection Status** = Connection quality
- **WAL Generation** = Message generation rate
- **Slot Status** = Channel status
- **Performance** = System performance

### SQL Example - Replication Monitoring:
```sql
-- Check replication status
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

-- Check WAL generation
SELECT 
    pg_current_wal_lsn() as current_lsn,
    pg_walfile_name(pg_current_wal_lsn()) as current_wal_file,
    pg_wal_lsn_diff(pg_current_wal_lsn(), '0/0') as total_wal_bytes;

-- Check replication slots
SELECT 
    slot_name,
    plugin,
    slot_type,
    database,
    active,
    xmin,
    catalog_xmin,
    restart_lsn,
    confirmed_flush_lsn
FROM pg_replication_slots;

-- Check WAL sender statistics
SELECT 
    pid,
    state,
    sent_lsn,
    write_lsn,
    flush_lsn,
    replay_lsn
FROM pg_stat_wal_sender;

-- Check WAL receiver statistics
SELECT 
    pid,
    status,
    receive_start_lsn,
    received_lsn,
    latest_end_lsn
FROM pg_stat_wal_receiver;

-- Monitor replication lag
SELECT 
    client_addr,
    state,
    pg_wal_lsn_diff(pg_current_wal_lsn(), sent_lsn) as sent_lag_bytes,
    pg_wal_lsn_diff(pg_current_wal_lsn(), write_lsn) as write_lag_bytes,
    pg_wal_lsn_diff(pg_current_wal_lsn(), flush_lsn) as flush_lag_bytes,
    pg_wal_lsn_diff(pg_current_wal_lsn(), replay_lsn) as replay_lag_bytes
FROM pg_stat_replication;

-- Check replication performance
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
WHERE state = 'streaming';
```

## 12.9 Backup and Point-in-Time Recovery

Backup and point-in-time recovery provide data protection and recovery capabilities.

### Backup Types:
- **Full Backup**: Complete database backup
- **Incremental Backup**: Only changed data
- **WAL Backup**: WAL file backup
- **Base Backup**: Physical backup
- **Logical Backup**: Logical backup

### Point-in-Time Recovery:
- **WAL Files**: Use WAL files for recovery
- **Recovery Target**: Specify recovery point
- **Recovery Mode**: Recovery mode operation
- **Recovery Testing**: Test recovery procedures
- **Recovery Monitoring**: Monitor recovery progress

### Real-World Analogy:
Backup and recovery are like document archiving:
- **Full Backup** = Complete document archive
- **Incremental Backup** = Only new documents
- **WAL Backup** = Change log backup
- **Base Backup** = Physical document backup
- **Logical Backup** = Content backup

### SQL Example - Backup and Recovery:
```sql
-- Check WAL configuration
SELECT 
    name,
    setting,
    unit,
    context,
    short_desc
FROM pg_settings 
WHERE name IN ('wal_level', 'archive_mode', 'archive_command', 'restore_command');

-- Check archive mode
SHOW archive_mode;

-- Check archive command
SHOW archive_command;

-- Check restore command
SHOW restore_command;

-- Check WAL files
SELECT 
    name,
    size,
    modification
FROM pg_ls_waldir()
ORDER BY modification DESC
LIMIT 10;

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

-- Check backup status
SELECT 
    pg_is_in_backup(),
    pg_backup_start_time(),
    pg_backup_stop_time();

-- Check recovery status
SELECT 
    pg_is_in_recovery(),
    pg_last_wal_receive_lsn(),
    pg_last_wal_replay_lsn();

-- Check recovery target
SELECT 
    name,
    setting,
    unit,
    context,
    short_desc
FROM pg_settings 
WHERE name LIKE 'recovery%';
```

## 12.10 Disaster Recovery Planning

Disaster recovery planning ensures business continuity during disasters.

### Disaster Recovery Components:
- **Recovery Time Objective (RTO)**: Maximum acceptable downtime
- **Recovery Point Objective (RPO)**: Maximum acceptable data loss
- **Backup Strategy**: Comprehensive backup strategy
- **Recovery Procedures**: Step-by-step recovery procedures
- **Testing**: Regular disaster recovery testing

### Real-World Analogy:
Disaster recovery planning is like having a fire evacuation plan:
- **RTO** = Maximum time to evacuate
- **RPO** = Maximum acceptable loss
- **Backup Strategy** = Multiple exit routes
- **Recovery Procedures** = Step-by-step evacuation
- **Testing** = Regular fire drills

### SQL Example - Disaster Recovery Planning:
```sql
-- Check disaster recovery configuration
SELECT 
    name,
    setting,
    unit,
    context,
    short_desc
FROM pg_settings 
WHERE name IN (
    'wal_level',
    'archive_mode',
    'archive_command',
    'restore_command',
    'recovery_target_time',
    'recovery_target_lsn',
    'recovery_target_name'
);

-- Check replication status
SELECT 
    client_addr,
    state,
    sent_lsn,
    write_lsn,
    flush_lsn,
    replay_lsn
FROM pg_stat_replication;

-- Check replication slots
SELECT 
    slot_name,
    plugin,
    slot_type,
    database,
    active,
    xmin,
    catalog_xmin,
    restart_lsn,
    confirmed_flush_lsn
FROM pg_replication_slots;

-- Check backup status
SELECT 
    pg_is_in_backup(),
    pg_backup_start_time(),
    pg_backup_stop_time();

-- Check recovery status
SELECT 
    pg_is_in_recovery(),
    pg_last_wal_receive_lsn(),
    pg_last_wal_replay_lsn();

-- Check disaster recovery metrics
SELECT 
    client_addr,
    state,
    pg_wal_lsn_diff(pg_current_wal_lsn(), sent_lsn) as sent_lag_bytes,
    pg_wal_lsn_diff(pg_current_wal_lsn(), write_lsn) as write_lag_bytes,
    pg_wal_lsn_diff(pg_current_wal_lsn(), flush_lsn) as flush_lag_bytes,
    pg_wal_lsn_diff(pg_current_wal_lsn(), replay_lsn) as replay_lag_bytes
FROM pg_stat_replication
WHERE state = 'streaming';
```