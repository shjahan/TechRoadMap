# Section 14 – Backup and Recovery

## 14.1 Backup Strategies

PostgreSQL provides multiple backup strategies for different recovery requirements.

### Backup Types:
- **Logical Backups**: pg_dump and pg_dumpall
- **Physical Backups**: File system level backups
- **Continuous Archiving**: WAL-based backups
- **Point-in-Time Recovery**: Recovery to specific points
- **Incremental Backups**: Only changed data

### Real-World Analogy:
Backup strategies are like different ways to preserve important documents:
- **Logical Backups** = Making photocopies of documents
- **Physical Backups** = Copying entire filing cabinets
- **Continuous Archiving** = Keeping change logs
- **Point-in-Time Recovery** = Restoring to specific dates
- **Incremental Backups** = Only copying new documents

### SQL Example - Backup Strategies:
```sql
-- Check backup configuration
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
    'max_wal_size',
    'min_wal_size'
);

-- Check WAL level
SHOW wal_level;

-- Check archive mode
SHOW archive_mode;

-- Check archive command
SHOW archive_command;

-- Check restore command
SHOW restore_command;

-- Check WAL size settings
SHOW max_wal_size;
SHOW min_wal_size;

-- Check current WAL position
SELECT pg_current_wal_lsn();

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
```

## 14.2 pg_dump and pg_restore

pg_dump and pg_restore provide logical backup and restore capabilities.

### pg_dump Features:
- **Database Dumps**: Complete database backups
- **Schema Dumps**: Schema-only backups
- **Data Dumps**: Data-only backups
- **Custom Format**: Compressed and efficient format
- **Parallel Dumps**: Parallel backup processing

### Real-World Analogy:
pg_dump is like creating a detailed inventory of a library:
- **Database Dumps** = Complete library catalog
- **Schema Dumps** = Library structure only
- **Data Dumps** = Book contents only
- **Custom Format** = Compressed catalog
- **Parallel Dumps** = Multiple librarians working

### SQL Example - pg_dump and pg_restore:
```sql
-- Check database size
SELECT 
    datname,
    pg_size_pretty(pg_database_size(datname)) as size
FROM pg_database
WHERE datname = current_database();

-- Check table sizes
SELECT 
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as size
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;

-- Check index sizes
SELECT 
    schemaname,
    tablename,
    indexname,
    pg_size_pretty(pg_relation_size(indexname::regclass)) as size
FROM pg_indexes
WHERE schemaname = 'public'
ORDER BY pg_relation_size(indexname::regclass) DESC;

-- Check sequence sizes
SELECT 
    schemaname,
    sequencename,
    pg_size_pretty(pg_relation_size(schemaname||'.'||sequencename)) as size
FROM pg_sequences
WHERE schemaname = 'public'
ORDER BY pg_relation_size(schemaname||'.'||sequencename) DESC;

-- Check function sizes
SELECT 
    n.nspname as schema_name,
    p.proname as function_name,
    pg_size_pretty(pg_relation_size(p.oid)) as size
FROM pg_proc p
JOIN pg_namespace n ON p.pronamespace = n.oid
WHERE n.nspname = 'public'
ORDER BY pg_relation_size(p.oid) DESC;

-- Check view sizes
SELECT 
    schemaname,
    viewname,
    pg_size_pretty(pg_relation_size(schemaname||'.'||viewname)) as size
FROM pg_views
WHERE schemaname = 'public'
ORDER BY pg_relation_size(schemaname||'.'||viewname) DESC;
```

## 14.3 Physical Backups

Physical backups copy database files at the file system level.

### Physical Backup Features:
- **File System Copy**: Copy database directory
- **Hot Backups**: Online backup capability
- **Cold Backups**: Offline backup capability
- **Base Backups**: WAL-based physical backups
- **Recovery**: Point-in-time recovery

### Real-World Analogy:
Physical backups are like copying entire filing cabinets:
- **File System Copy** = Copying entire cabinets
- **Hot Backups** = Copying while in use
- **Cold Backups** = Copying when closed
- **Base Backups** = Copying with change logs
- **Recovery** = Restoring from copies

### SQL Example - Physical Backups:
```sql
-- Check database directory
SHOW data_directory;

-- Check WAL directory
SHOW data_directory;

-- Check WAL files
SELECT 
    name,
    size,
    modification
FROM pg_ls_waldir()
ORDER BY modification DESC
LIMIT 10;

-- Check WAL configuration
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
    'max_wal_size',
    'min_wal_size'
);

-- Check WAL level
SHOW wal_level;

-- Check archive mode
SHOW archive_mode;

-- Check archive command
SHOW archive_command;

-- Check restore command
SHOW restore_command;

-- Check WAL size settings
SHOW max_wal_size;
SHOW min_wal_size;

-- Check current WAL position
SELECT pg_current_wal_lsn();

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
```

## 14.4 Continuous Archiving

Continuous archiving provides point-in-time recovery capabilities.

### Continuous Archiving Features:
- **WAL Archiving**: Archive WAL files
- **Archive Command**: Custom archive commands
- **Restore Command**: Custom restore commands
- **Recovery Target**: Specify recovery points
- **Recovery Testing**: Test recovery procedures

### Real-World Analogy:
Continuous archiving is like keeping detailed change logs:
- **WAL Archiving** = Saving change logs
- **Archive Command** = How to save logs
- **Restore Command** = How to restore logs
- **Recovery Target** = Which point to restore to
- **Recovery Testing** = Testing restoration

### SQL Example - Continuous Archiving:
```sql
-- Check archive configuration
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
    'archive_timeout',
    'archive_lag_timeout'
);

-- Check WAL level
SHOW wal_level;

-- Check archive mode
SHOW archive_mode;

-- Check archive command
SHOW archive_command;

-- Check restore command
SHOW restore_command;

-- Check archive timeout
SHOW archive_timeout;

-- Check archive lag timeout
SHOW archive_lag_timeout;

-- Check current WAL position
SELECT pg_current_wal_lsn();

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

-- Check archive status
SELECT 
    archived_count,
    last_archived_wal,
    last_archived_time,
    failed_count,
    last_failed_wal,
    last_failed_time,
    stats_reset
FROM pg_stat_archiver;
```

## 14.5 Point-in-Time Recovery (PITR)

Point-in-Time Recovery allows recovery to specific points in time.

### PITR Features:
- **Recovery Target**: Specify recovery points
- **Recovery Commands**: Recovery configuration
- **WAL Replay**: Replay WAL files
- **Recovery Testing**: Test recovery procedures
- **Recovery Monitoring**: Monitor recovery progress

### Real-World Analogy:
PITR is like rewinding time to a specific moment:
- **Recovery Target** = Choosing the time to go back to
- **Recovery Commands** = How to rewind
- **WAL Replay** = Replaying events
- **Recovery Testing** = Testing the rewind
- **Recovery Monitoring** = Watching the process

### SQL Example - Point-in-Time Recovery:
```sql
-- Check recovery configuration
SELECT 
    name,
    setting,
    unit,
    context,
    short_desc
FROM pg_settings 
WHERE name IN (
    'recovery_target_time',
    'recovery_target_lsn',
    'recovery_target_name',
    'recovery_target_timeline',
    'recovery_target_action'
);

-- Check recovery target time
SHOW recovery_target_time;

-- Check recovery target LSN
SHOW recovery_target_lsn;

-- Check recovery target name
SHOW recovery_target_name;

-- Check recovery target timeline
SHOW recovery_target_timeline;

-- Check recovery target action
SHOW recovery_target_action;

-- Check current WAL position
SELECT pg_current_wal_lsn();

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

-- Check recovery status
SELECT 
    pg_is_in_recovery(),
    pg_last_wal_receive_lsn(),
    pg_last_wal_replay_lsn();
```

## 14.6 Base Backup and WAL Files

Base backups and WAL files provide the foundation for point-in-time recovery.

### Base Backup Features:
- **pg_basebackup**: Create base backups
- **WAL Files**: Transaction log files
- **Recovery**: Point-in-time recovery
- **Replication**: Streaming replication
- **Monitoring**: Backup monitoring

### Real-World Analogy:
Base backups and WAL files are like having a starting point and change log:
- **Base Backup** = Starting point snapshot
- **WAL Files** = Change log
- **Recovery** = Reconstructing from snapshot and changes
- **Replication** = Live change streaming
- **Monitoring** = Watching the process

### SQL Example - Base Backup and WAL Files:
```sql
-- Check WAL configuration
SELECT 
    name,
    setting,
    unit,
    context,
    short_desc
FROM pg_settings 
WHERE name IN (
    'wal_level',
    'max_wal_size',
    'min_wal_size',
    'checkpoint_segments',
    'checkpoint_timeout'
);

-- Check WAL level
SHOW wal_level;

-- Check WAL size settings
SHOW max_wal_size;
SHOW min_wal_size;

-- Check checkpoint segments
SHOW checkpoint_segments;

-- Check checkpoint timeout
SHOW checkpoint_timeout;

-- Check current WAL position
SELECT pg_current_wal_lsn();

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

-- Check checkpoint statistics
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

## 14.7 Backup Verification

Backup verification ensures backup integrity and recoverability.

### Verification Methods:
- **Integrity Checks**: Verify backup integrity
- **Recovery Testing**: Test recovery procedures
- **Data Validation**: Validate recovered data
- **Performance Testing**: Test recovery performance
- **Automated Testing**: Automated verification

### Real-World Analogy:
Backup verification is like testing emergency procedures:
- **Integrity Checks** = Checking if equipment works
- **Recovery Testing** = Practicing emergency procedures
- **Data Validation** = Verifying everything is correct
- **Performance Testing** = Testing response time
- **Automated Testing** = Regular drills

### SQL Example - Backup Verification:
```sql
-- Check database integrity
SELECT 
    datname,
    pg_database_size(datname) as size_bytes,
    pg_size_pretty(pg_database_size(datname)) as size_pretty
FROM pg_database
WHERE datname = current_database();

-- Check table integrity
SELECT 
    schemaname,
    tablename,
    pg_total_relation_size(schemaname||'.'||tablename) as size_bytes,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as size_pretty
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;

-- Check index integrity
SELECT 
    schemaname,
    tablename,
    indexname,
    pg_relation_size(indexname::regclass) as size_bytes,
    pg_size_pretty(pg_relation_size(indexname::regclass)) as size_pretty
FROM pg_indexes
WHERE schemaname = 'public'
ORDER BY pg_relation_size(indexname::regclass) DESC;

-- Check sequence integrity
SELECT 
    schemaname,
    sequencename,
    pg_relation_size(schemaname||'.'||sequencename) as size_bytes,
    pg_size_pretty(pg_relation_size(schemaname||'.'||sequencename)) as size_pretty
FROM pg_sequences
WHERE schemaname = 'public'
ORDER BY pg_relation_size(schemaname||'.'||sequencename) DESC;

-- Check function integrity
SELECT 
    n.nspname as schema_name,
    p.proname as function_name,
    pg_relation_size(p.oid) as size_bytes,
    pg_size_pretty(pg_relation_size(p.oid)) as size_pretty
FROM pg_proc p
JOIN pg_namespace n ON p.pronamespace = n.oid
WHERE n.nspname = 'public'
ORDER BY pg_relation_size(p.oid) DESC;

-- Check view integrity
SELECT 
    schemaname,
    viewname,
    pg_relation_size(schemaname||'.'||viewname) as size_bytes,
    pg_size_pretty(pg_relation_size(schemaname||'.'||viewname)) as size_pretty
FROM pg_views
WHERE schemaname = 'public'
ORDER BY pg_relation_size(schemaname||'.'||viewname) DESC;
```

## 14.8 Recovery Testing

Recovery testing validates backup and recovery procedures.

### Testing Methods:
- **Full Recovery**: Complete database recovery
- **Partial Recovery**: Partial database recovery
- **Point-in-Time Recovery**: Recovery to specific points
- **Performance Testing**: Recovery performance testing
- **Automated Testing**: Automated recovery testing

### Real-World Analogy:
Recovery testing is like practicing emergency procedures:
- **Full Recovery** = Complete system restoration
- **Partial Recovery** = Partial system restoration
- **Point-in-Time Recovery** = Restoring to specific time
- **Performance Testing** = Testing restoration speed
- **Automated Testing** = Regular practice drills

### SQL Example - Recovery Testing:
```sql
-- Check recovery configuration
SELECT 
    name,
    setting,
    unit,
    context,
    short_desc
FROM pg_settings 
WHERE name IN (
    'recovery_target_time',
    'recovery_target_lsn',
    'recovery_target_name',
    'recovery_target_timeline',
    'recovery_target_action'
);

-- Check recovery target time
SHOW recovery_target_time;

-- Check recovery target LSN
SHOW recovery_target_lsn;

-- Check recovery target name
SHOW recovery_target_name;

-- Check recovery target timeline
SHOW recovery_target_timeline;

-- Check recovery target action
SHOW recovery_target_action;

-- Check current WAL position
SELECT pg_current_wal_lsn();

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

-- Check recovery status
SELECT 
    pg_is_in_recovery(),
    pg_last_wal_receive_lsn(),
    pg_last_wal_replay_lsn();
```

## 14.9 Backup Automation

Backup automation ensures consistent and reliable backups.

### Automation Features:
- **Scheduled Backups**: Automated backup scheduling
- **Backup Scripts**: Custom backup scripts
- **Monitoring**: Backup monitoring and alerting
- **Retention**: Backup retention policies
- **Recovery**: Automated recovery procedures

### Real-World Analogy:
Backup automation is like having an automated security system:
- **Scheduled Backups** = Regular security checks
- **Backup Scripts** = Automated procedures
- **Monitoring** = Security monitoring
- **Retention** = Keeping records
- **Recovery** = Emergency procedures

### SQL Example - Backup Automation:
```sql
-- Check backup configuration
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
    'archive_timeout',
    'archive_lag_timeout'
);

-- Check WAL level
SHOW wal_level;

-- Check archive mode
SHOW archive_mode;

-- Check archive command
SHOW archive_command;

-- Check restore command
SHOW restore_command;

-- Check archive timeout
SHOW archive_timeout;

-- Check archive lag timeout
SHOW archive_lag_timeout;

-- Check current WAL position
SELECT pg_current_wal_lsn();

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

-- Check archive status
SELECT 
    archived_count,
    last_archived_wal,
    last_archived_time,
    failed_count,
    last_failed_wal,
    last_failed_time,
    stats_reset
FROM pg_stat_archiver;
```

## 14.10 Disaster Recovery Procedures

Disaster recovery procedures ensure business continuity during disasters.

### Recovery Procedures:
- **Recovery Planning**: Comprehensive recovery planning
- **Recovery Testing**: Regular recovery testing
- **Recovery Documentation**: Detailed recovery procedures
- **Recovery Training**: Staff training on recovery procedures
- **Recovery Monitoring**: Recovery process monitoring

### Real-World Analogy:
Disaster recovery procedures are like emergency response plans:
- **Recovery Planning** = Emergency response planning
- **Recovery Testing** = Emergency drills
- **Recovery Documentation** = Emergency procedures manual
- **Recovery Training** = Staff training
- **Recovery Monitoring** = Emergency monitoring

### SQL Example - Disaster Recovery Procedures:
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
    'recovery_target_name',
    'recovery_target_timeline',
    'recovery_target_action'
);

-- Check WAL level
SHOW wal_level;

-- Check archive mode
SHOW archive_mode;

-- Check archive command
SHOW archive_command;

-- Check restore command
SHOW restore_command;

-- Check recovery target time
SHOW recovery_target_time;

-- Check recovery target LSN
SHOW recovery_target_lsn;

-- Check recovery target name
SHOW recovery_target_name;

-- Check recovery target timeline
SHOW recovery_target_timeline;

-- Check recovery target action
SHOW recovery_target_action;

-- Check current WAL position
SELECT pg_current_wal_lsn();

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

-- Check recovery status
SELECT 
    pg_is_in_recovery(),
    pg_last_wal_receive_lsn(),
    pg_last_wal_replay_lsn();
```