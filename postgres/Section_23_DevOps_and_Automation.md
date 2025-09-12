# Section 23 – DevOps and Automation

## 23.1 DevOps Fundamentals

DevOps for PostgreSQL involves integrating development and operations practices to improve database deployment, monitoring, and maintenance.

### Key DevOps Principles:
- **Infrastructure as Code**: Managing infrastructure through code
- **Continuous Integration**: Automated testing and integration
- **Continuous Deployment**: Automated deployment processes
- **Monitoring and Logging**: Comprehensive system observability

### Real-World Analogy:
DevOps is like having a well-orchestrated restaurant kitchen:
- **Infrastructure as Code** = Standardized recipes and procedures
- **Continuous Integration** = Quality control checks
- **Continuous Deployment** = Efficient service delivery
- **Monitoring and Logging** = Kitchen management systems

### Example:
```sql
-- Create DevOps configuration table
CREATE TABLE devops_config (
    id SERIAL PRIMARY KEY,
    environment VARCHAR(50) NOT NULL,
    config_key VARCHAR(100) NOT NULL,
    config_value TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Insert environment configurations
INSERT INTO devops_config (environment, config_key, config_value) VALUES
('development', 'max_connections', '100'),
('development', 'shared_buffers', '256MB'),
('staging', 'max_connections', '200'),
('staging', 'shared_buffers', '512MB'),
('production', 'max_connections', '500'),
('production', 'shared_buffers', '2GB');

-- Create configuration management function
CREATE OR REPLACE FUNCTION get_config_value(env VARCHAR(50), key VARCHAR(100))
RETURNS TEXT AS $$
DECLARE
    value TEXT;
BEGIN
    SELECT config_value INTO value
    FROM devops_config
    WHERE environment = env AND config_key = key;
    
    RETURN value;
END;
$$ LANGUAGE plpgsql;
```

## 23.2 Infrastructure as Code

Infrastructure as Code (IaC) manages PostgreSQL infrastructure through version-controlled configuration files.

### IaC Components:
- **Configuration Files**: YAML, JSON, or HCL files
- **Templates**: Reusable infrastructure templates
- **State Management**: Tracking infrastructure state
- **Provisioning**: Automated resource creation

### Real-World Analogy:
Infrastructure as Code is like having architectural blueprints:
- **Configuration Files** = Detailed blueprints
- **Templates** = Standard building designs
- **State Management** = Construction progress tracking
- **Provisioning** = Automated construction

### Example:
```yaml
# PostgreSQL Infrastructure Configuration
# postgres-infrastructure.yml
apiVersion: v1
kind: ConfigMap
metadata:
  name: postgres-config
data:
  POSTGRES_DB: "myapp"
  POSTGRES_USER: "app_user"
  POSTGRES_PASSWORD: "secure_password"
  MAX_CONNECTIONS: "200"
  SHARED_BUFFERS: "256MB"
  EFFECTIVE_CACHE_SIZE: "1GB"

---
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: postgres
spec:
  serviceName: postgres
  replicas: 1
  selector:
    matchLabels:
      app: postgres
  template:
    metadata:
      labels:
        app: postgres
    spec:
      containers:
      - name: postgres
        image: postgres:15
        ports:
        - containerPort: 5432
        envFrom:
        - configMapRef:
            name: postgres-config
        volumeMounts:
        - name: postgres-storage
          mountPath: /var/lib/postgresql/data
  volumeClaimTemplates:
  - metadata:
      name: postgres-storage
    spec:
      accessModes: ["ReadWriteOnce"]
      resources:
        requests:
          storage: 20Gi
```

## 23.3 Continuous Integration

Continuous Integration (CI) automates testing and integration of database changes.

### CI Components:
- **Version Control**: Git-based change management
- **Automated Testing**: Automated test execution
- **Code Quality**: Static analysis and linting
- **Build Automation**: Automated build processes

### Real-World Analogy:
Continuous Integration is like having an automated quality control system:
- **Version Control** = Change tracking system
- **Automated Testing** = Quality control checks
- **Code Quality** = Standards compliance
- **Build Automation** = Production line automation

### Example:
```yaml
# CI/CD Pipeline Configuration
# .github/workflows/postgres-ci.yml
name: PostgreSQL CI/CD

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: test_db
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432

    steps:
    - uses: actions/checkout@v3
    
    - name: Setup PostgreSQL
      run: |
        psql -h localhost -U postgres -d test_db -c "CREATE EXTENSION IF NOT EXISTS pg_stat_statements;"
    
    - name: Run Database Tests
      run: |
        psql -h localhost -U postgres -d test_db -f tests/schema.sql
        psql -h localhost -U postgres -d test_db -f tests/data.sql
        psql -h localhost -U postgres -d test_db -f tests/test_runner.sql
    
    - name: Run Performance Tests
      run: |
        psql -h localhost -U postgres -d test_db -f tests/performance_tests.sql
    
    - name: Generate Test Report
      run: |
        psql -h localhost -U postgres -d test_db -c "SELECT * FROM generate_test_report();" > test_report.json
```

## 23.4 Continuous Deployment

Continuous Deployment (CD) automates the deployment of database changes to different environments.

### CD Components:
- **Deployment Pipelines**: Automated deployment workflows
- **Environment Management**: Managing multiple environments
- **Rollback Capabilities**: Ability to revert changes
- **Blue-Green Deployment**: Zero-downtime deployments

### Real-World Analogy:
Continuous Deployment is like having an automated delivery system:
- **Deployment Pipelines** = Delivery routes
- **Environment Management** = Different delivery locations
- **Rollback Capabilities** = Return to sender
- **Blue-Green Deployment** = Parallel delivery systems

### Example:
```sql
-- Create deployment tracking table
CREATE TABLE deployments (
    id SERIAL PRIMARY KEY,
    version VARCHAR(50) NOT NULL,
    environment VARCHAR(50) NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',
    deployed_by VARCHAR(100),
    deployed_at TIMESTAMP,
    rollback_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Create deployment function
CREATE OR REPLACE FUNCTION deploy_version(
    version VARCHAR(50),
    environment VARCHAR(50),
    deployed_by VARCHAR(100)
)
RETURNS INTEGER AS $$
DECLARE
    deployment_id INTEGER;
BEGIN
    -- Create deployment record
    INSERT INTO deployments (version, environment, deployed_by, status)
    VALUES (version, environment, deployed_by, 'deploying')
    RETURNING id INTO deployment_id;
    
    -- Execute deployment steps
    PERFORM execute_deployment_steps(version, environment);
    
    -- Update deployment status
    UPDATE deployments
    SET status = 'deployed', deployed_at = NOW()
    WHERE id = deployment_id;
    
    RETURN deployment_id;
END;
$$ LANGUAGE plpgsql;

-- Create rollback function
CREATE OR REPLACE FUNCTION rollback_deployment(deployment_id INTEGER)
RETURNS BOOLEAN AS $$
DECLARE
    deployment_record RECORD;
BEGIN
    -- Get deployment details
    SELECT * INTO deployment_record
    FROM deployments
    WHERE id = deployment_id;
    
    -- Execute rollback steps
    PERFORM execute_rollback_steps(deployment_record.version, deployment_record.environment);
    
    -- Update deployment status
    UPDATE deployments
    SET status = 'rolled_back', rollback_at = NOW()
    WHERE id = deployment_id;
    
    RETURN TRUE;
END;
$$ LANGUAGE plpgsql;
```

## 23.5 Monitoring and Alerting

Monitoring and alerting provide real-time visibility into PostgreSQL performance and health.

### Monitoring Components:
- **Metrics Collection**: Gathering performance metrics
- **Dashboards**: Visual representation of metrics
- **Alerting**: Automated notifications for issues
- **Logging**: Comprehensive log management

### Real-World Analogy:
Monitoring and alerting are like having a comprehensive control room:
- **Metrics Collection** = Data sensors
- **Dashboards** = Control panels
- **Alerting** = Alarm systems
- **Logging** = Activity records

### Example:
```sql
-- Create monitoring tables
CREATE TABLE system_metrics (
    id SERIAL PRIMARY KEY,
    metric_name VARCHAR(100) NOT NULL,
    metric_value DECIMAL(15,4) NOT NULL,
    timestamp TIMESTAMP DEFAULT NOW()
);

CREATE TABLE alerts (
    id SERIAL PRIMARY KEY,
    alert_name VARCHAR(100) NOT NULL,
    severity VARCHAR(20) NOT NULL,
    message TEXT NOT NULL,
    status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT NOW(),
    resolved_at TIMESTAMP
);

-- Create monitoring function
CREATE OR REPLACE FUNCTION collect_system_metrics()
RETURNS VOID AS $$
BEGIN
    -- Collect connection metrics
    INSERT INTO system_metrics (metric_name, metric_value)
    SELECT 'active_connections', COUNT(*)
    FROM pg_stat_activity
    WHERE state = 'active';
    
    -- Collect database size
    INSERT INTO system_metrics (metric_name, metric_value)
    SELECT 'database_size', pg_database_size(current_database());
    
    -- Collect cache hit ratio
    INSERT INTO system_metrics (metric_name, metric_value)
    SELECT 'cache_hit_ratio', 
           round(blks_hit::float / (blks_hit + blks_read) * 100, 2)
    FROM pg_stat_database
    WHERE datname = current_database();
    
    -- Collect query performance
    INSERT INTO system_metrics (metric_name, metric_value)
    SELECT 'avg_query_time', 
           round(avg(total_time), 2)
    FROM pg_stat_statements
    WHERE calls > 0;
END;
$$ LANGUAGE plpgsql;

-- Create alerting function
CREATE OR REPLACE FUNCTION check_alerts()
RETURNS VOID AS $$
DECLARE
    alert_record RECORD;
BEGIN
    -- Check for high connection usage
    IF (SELECT metric_value FROM system_metrics 
        WHERE metric_name = 'active_connections' 
        ORDER BY timestamp DESC LIMIT 1) > 80 THEN
        
        INSERT INTO alerts (alert_name, severity, message)
        VALUES ('High Connection Usage', 'WARNING', 
                'Active connections exceed 80% of maximum');
    END IF;
    
    -- Check for low cache hit ratio
    IF (SELECT metric_value FROM system_metrics 
        WHERE metric_name = 'cache_hit_ratio' 
        ORDER BY timestamp DESC LIMIT 1) < 90 THEN
        
        INSERT INTO alerts (alert_name, severity, message)
        VALUES ('Low Cache Hit Ratio', 'WARNING', 
                'Cache hit ratio below 90%');
    END IF;
    
    -- Check for slow queries
    IF (SELECT metric_value FROM system_metrics 
        WHERE metric_name = 'avg_query_time' 
        ORDER BY timestamp DESC LIMIT 1) > 1000 THEN
        
        INSERT INTO alerts (alert_name, severity, message)
        VALUES ('Slow Queries', 'CRITICAL', 
                'Average query time exceeds 1 second');
    END IF;
END;
$$ LANGUAGE plpgsql;
```

## 23.6 Log Management

Log management involves collecting, storing, and analyzing PostgreSQL logs for troubleshooting and auditing.

### Log Management Components:
- **Log Collection**: Gathering logs from multiple sources
- **Log Storage**: Centralized log storage
- **Log Analysis**: Parsing and analyzing logs
- **Log Retention**: Managing log lifecycle

### Real-World Analogy:
Log management is like maintaining a comprehensive library:
- **Log Collection** = Gathering books from different sources
- **Log Storage** = Organizing books in the library
- **Log Analysis** = Cataloging and indexing books
- **Log Retention** = Managing book lifecycle

### Example:
```sql
-- Create log management tables
CREATE TABLE log_entries (
    id SERIAL PRIMARY KEY,
    log_level VARCHAR(20) NOT NULL,
    log_message TEXT NOT NULL,
    source VARCHAR(100),
    timestamp TIMESTAMP DEFAULT NOW(),
    metadata JSONB
);

CREATE TABLE log_patterns (
    id SERIAL PRIMARY KEY,
    pattern_name VARCHAR(100) NOT NULL,
    regex_pattern TEXT NOT NULL,
    severity VARCHAR(20) NOT NULL,
    description TEXT
);

-- Create log analysis function
CREATE OR REPLACE FUNCTION analyze_logs()
RETURNS TABLE(
    pattern_name VARCHAR(100),
    occurrence_count BIGINT,
    severity VARCHAR(20),
    sample_message TEXT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        lp.pattern_name,
        COUNT(*) as occurrence_count,
        lp.severity,
        le.log_message as sample_message
    FROM log_entries le
    JOIN log_patterns lp ON le.log_message ~ lp.regex_pattern
    WHERE le.timestamp >= NOW() - INTERVAL '1 hour'
    GROUP BY lp.pattern_name, lp.severity, le.log_message
    ORDER BY occurrence_count DESC;
END;
$$ LANGUAGE plpgsql;

-- Create log retention function
CREATE OR REPLACE FUNCTION cleanup_old_logs(retention_days INTEGER)
RETURNS INTEGER AS $$
DECLARE
    deleted_count INTEGER;
BEGIN
    DELETE FROM log_entries
    WHERE timestamp < NOW() - (retention_days || ' days')::INTERVAL;
    
    GET DIAGNOSTICS deleted_count = ROW_COUNT;
    
    RETURN deleted_count;
END;
$$ LANGUAGE plpgsql;
```

## 23.7 Backup Automation

Backup automation ensures consistent and reliable database backups without manual intervention.

### Backup Components:
- **Scheduled Backups**: Automated backup scheduling
- **Backup Verification**: Validating backup integrity
- **Backup Retention**: Managing backup lifecycle
- **Recovery Testing**: Testing backup restoration

### Real-World Analogy:
Backup automation is like having an automated security system:
- **Scheduled Backups** = Regular security patrols
- **Backup Verification** = Security system testing
- **Backup Retention** = Security footage management
- **Recovery Testing** = Emergency response drills

### Example:
```sql
-- Create backup tracking table
CREATE TABLE backup_history (
    id SERIAL PRIMARY KEY,
    backup_type VARCHAR(50) NOT NULL,
    backup_size BIGINT,
    backup_location VARCHAR(500),
    status VARCHAR(20) DEFAULT 'pending',
    started_at TIMESTAMP DEFAULT NOW(),
    completed_at TIMESTAMP,
    verified_at TIMESTAMP
);

-- Create backup function
CREATE OR REPLACE FUNCTION create_backup(
    backup_type VARCHAR(50),
    backup_location VARCHAR(500)
)
RETURNS INTEGER AS $$
DECLARE
    backup_id INTEGER;
    backup_size BIGINT;
BEGIN
    -- Create backup record
    INSERT INTO backup_history (backup_type, backup_location, status)
    VALUES (backup_type, backup_location, 'in_progress')
    RETURNING id INTO backup_id;
    
    -- Execute backup (this would typically call external tools)
    -- For demonstration, we'll simulate the backup process
    PERFORM pg_sleep(1); -- Simulate backup time
    
    -- Calculate backup size (simulated)
    backup_size := pg_database_size(current_database());
    
    -- Update backup record
    UPDATE backup_history
    SET 
        backup_size = backup_size,
        status = 'completed',
        completed_at = NOW()
    WHERE id = backup_id;
    
    RETURN backup_id;
END;
$$ LANGUAGE plpgsql;

-- Create backup verification function
CREATE OR REPLACE FUNCTION verify_backup(backup_id INTEGER)
RETURNS BOOLEAN AS $$
DECLARE
    backup_record RECORD;
    verification_result BOOLEAN := TRUE;
BEGIN
    -- Get backup details
    SELECT * INTO backup_record
    FROM backup_history
    WHERE id = backup_id;
    
    -- Perform verification checks
    -- Check if backup file exists and is readable
    -- Check backup size matches expected size
    -- Check backup integrity
    
    -- Update verification status
    UPDATE backup_history
    SET 
        verified_at = NOW(),
        status = CASE WHEN verification_result THEN 'verified' ELSE 'failed' END
    WHERE id = backup_id;
    
    RETURN verification_result;
END;
$$ LANGUAGE plpgsql;
```

## 23.8 Security Automation

Security automation implements automated security measures and compliance checks.

### Security Components:
- **Access Control**: Automated user management
- **Audit Logging**: Automated security event logging
- **Compliance Checks**: Automated compliance validation
- **Threat Detection**: Automated threat monitoring

### Real-World Analogy:
Security automation is like having an automated security system:
- **Access Control** = Automated door locks
- **Audit Logging** = Security camera recordings
- **Compliance Checks** = Security protocol validation
- **Threat Detection** = Intrusion detection systems

### Example:
```sql
-- Create security audit table
CREATE TABLE security_audit (
    id SERIAL PRIMARY KEY,
    event_type VARCHAR(50) NOT NULL,
    user_name VARCHAR(100),
    ip_address INET,
    event_details JSONB,
    severity VARCHAR(20) DEFAULT 'INFO',
    timestamp TIMESTAMP DEFAULT NOW()
);

-- Create security monitoring function
CREATE OR REPLACE FUNCTION monitor_security_events()
RETURNS VOID AS $$
BEGIN
    -- Log failed login attempts
    INSERT INTO security_audit (event_type, user_name, ip_address, severity, event_details)
    SELECT 
        'failed_login',
        usename,
        client_addr,
        'WARNING',
        json_build_object(
            'database', datname,
            'application', application_name,
            'state', state
        )
    FROM pg_stat_activity
    WHERE state = 'idle in transaction (aborted)'
        AND usename IS NOT NULL;
    
    -- Log privilege escalations
    INSERT INTO security_audit (event_type, user_name, severity, event_details)
    SELECT 
        'privilege_escalation',
        usename,
        'CRITICAL',
        json_build_object(
            'database', datname,
            'superuser', usesuper,
            'createdb', usecreatedb
        )
    FROM pg_user
    WHERE usesuper = true
        AND usename NOT IN ('postgres', 'rdsadmin');
    
    -- Log data access patterns
    INSERT INTO security_audit (event_type, user_name, severity, event_details)
    SELECT 
        'data_access',
        usename,
        'INFO',
        json_build_object(
            'database', datname,
            'query_count', query_count,
            'avg_query_time', avg_query_time
        )
    FROM (
        SELECT 
            usename,
            datname,
            COUNT(*) as query_count,
            AVG(total_time) as avg_query_time
        FROM pg_stat_statements
        JOIN pg_user ON pg_stat_statements.userid = pg_user.usesysid
        WHERE calls > 0
        GROUP BY usename, datname
    ) access_stats;
END;
$$ LANGUAGE plpgsql;
```

## 23.9 Performance Automation

Performance automation implements automated performance monitoring and optimization.

### Performance Components:
- **Performance Monitoring**: Automated performance tracking
- **Query Optimization**: Automated query tuning
- **Resource Management**: Automated resource allocation
- **Capacity Planning**: Automated capacity management

### Real-World Analogy:
Performance automation is like having an automated performance tuning system:
- **Performance Monitoring** = Performance sensors
- **Query Optimization** = Automatic tuning
- **Resource Management** = Dynamic resource allocation
- **Capacity Planning** = Predictive scaling

### Example:
```sql
-- Create performance automation table
CREATE TABLE performance_automation (
    id SERIAL PRIMARY KEY,
    automation_type VARCHAR(50) NOT NULL,
    target_object VARCHAR(100),
    action_taken TEXT,
    performance_impact DECIMAL(10,2),
    timestamp TIMESTAMP DEFAULT NOW()
);

-- Create performance optimization function
CREATE OR REPLACE FUNCTION optimize_performance()
RETURNS VOID AS $$
DECLARE
    slow_query RECORD;
    optimization_action TEXT;
BEGIN
    -- Find slow queries
    FOR slow_query IN
        SELECT 
            query,
            calls,
            total_time,
            mean_time
        FROM pg_stat_statements
        WHERE mean_time > 1000 -- Queries taking more than 1 second
        ORDER BY mean_time DESC
        LIMIT 10
    LOOP
        -- Analyze query and suggest optimization
        IF slow_query.query LIKE '%SELECT%' AND slow_query.query LIKE '%WHERE%' THEN
            optimization_action := 'Consider adding indexes for WHERE clause columns';
        ELSIF slow_query.query LIKE '%JOIN%' THEN
            optimization_action := 'Consider optimizing JOIN conditions';
        ELSIF slow_query.query LIKE '%ORDER BY%' THEN
            optimization_action := 'Consider adding indexes for ORDER BY columns';
        ELSE
            optimization_action := 'Review query structure and execution plan';
        END IF;
        
        -- Log optimization suggestion
        INSERT INTO performance_automation (
            automation_type, 
            target_object, 
            action_taken, 
            performance_impact
        ) VALUES (
            'query_optimization',
            'slow_query',
            optimization_action,
            slow_query.mean_time
        );
    END LOOP;
    
    -- Check for missing indexes
    PERFORM check_missing_indexes();
    
    -- Check for table bloat
    PERFORM check_table_bloat();
END;
$$ LANGUAGE plpgsql;

-- Create missing index check function
CREATE OR REPLACE FUNCTION check_missing_indexes()
RETURNS VOID AS $$
DECLARE
    table_record RECORD;
BEGIN
    FOR table_record IN
        SELECT 
            schemaname,
            tablename,
            seq_scan,
            seq_tup_read,
            idx_scan,
            idx_tup_fetch
        FROM pg_stat_user_tables
        WHERE seq_scan > idx_scan * 2 -- More sequential scans than index scans
    LOOP
        INSERT INTO performance_automation (
            automation_type,
            target_object,
            action_taken,
            performance_impact
        ) VALUES (
            'index_optimization',
            table_record.schemaname || '.' || table_record.tablename,
            'Consider adding indexes to reduce sequential scans',
            table_record.seq_tup_read::DECIMAL
        );
    END LOOP;
END;
$$ LANGUAGE plpgsql;
```

## 23.10 Best Practices

Best practices for DevOps and automation ensure effective and reliable database operations.

### Key Practices:
- **Infrastructure as Code**: Version control all infrastructure
- **Automated Testing**: Comprehensive test automation
- **Monitoring**: Continuous monitoring and alerting
- **Documentation**: Maintain up-to-date documentation

### Real-World Analogy:
Best practices are like following professional standards:
- **Infrastructure as Code** = Standardized procedures
- **Automated Testing** = Quality control systems
- **Monitoring** = Performance tracking
- **Documentation** = Professional records

### Example:
```sql
-- Create DevOps best practices monitoring function
CREATE OR REPLACE FUNCTION check_devops_best_practices()
RETURNS TABLE(
    practice_name TEXT,
    status TEXT,
    recommendation TEXT
) AS $$
BEGIN
    -- Check infrastructure as code
    RETURN QUERY
    SELECT 
        'Infrastructure as Code'::TEXT,
        CASE 
            WHEN EXISTS (SELECT 1 FROM devops_config) THEN 'GOOD'
            ELSE 'NEEDS_ATTENTION'
        END,
        CASE 
            WHEN EXISTS (SELECT 1 FROM devops_config) THEN 'Infrastructure is managed as code'
            ELSE 'Implement infrastructure as code practices'
        END;
    
    -- Check monitoring
    RETURN QUERY
    SELECT 
        'Monitoring'::TEXT,
        CASE 
            WHEN COUNT(*) > 0 THEN 'GOOD'
            ELSE 'NEEDS_ATTENTION'
        END,
        CASE 
            WHEN COUNT(*) > 0 THEN 'Monitoring is implemented'
            ELSE 'Implement comprehensive monitoring'
        END
    FROM system_metrics
    WHERE timestamp >= NOW() - INTERVAL '1 hour';
    
    -- Check backup automation
    RETURN QUERY
    SELECT 
        'Backup Automation'::TEXT,
        CASE 
            WHEN COUNT(*) > 0 THEN 'GOOD'
            ELSE 'NEEDS_ATTENTION'
        END,
        CASE 
            WHEN COUNT(*) > 0 THEN 'Backup automation is working'
            ELSE 'Implement automated backup processes'
        END
    FROM backup_history
    WHERE started_at >= NOW() - INTERVAL '24 hours';
    
    -- Check security automation
    RETURN QUERY
    SELECT 
        'Security Automation'::TEXT,
        CASE 
            WHEN COUNT(*) > 0 THEN 'GOOD'
            ELSE 'NEEDS_ATTENTION'
        END,
        CASE 
            WHEN COUNT(*) > 0 THEN 'Security automation is active'
            ELSE 'Implement security automation'
        END
    FROM security_audit
    WHERE timestamp >= NOW() - INTERVAL '1 hour';
END;
$$ LANGUAGE plpgsql;
```