# Section 13 – Security and Authentication

## 13.1 PostgreSQL Security Model

PostgreSQL implements a comprehensive security model with multiple layers of protection.

### Security Layers:
- **Network Security**: Connection encryption and access control
- **Authentication**: User identity verification
- **Authorization**: Permission and access control
- **Data Encryption**: Data protection at rest and in transit
- **Audit Logging**: Security event monitoring

### Real-World Analogy:
PostgreSQL security is like a secure building:
- **Network Security** = Building perimeter security
- **Authentication** = ID verification at entrance
- **Authorization** = Access control to different floors
- **Data Encryption** = Secure storage rooms
- **Audit Logging** = Security camera system

### SQL Example - Security Model:
```sql
-- Check current user and database
SELECT current_user, current_database();

-- Check user roles and permissions
SELECT 
    rolname,
    rolsuper,
    rolinherit,
    rolcreaterole,
    rolcreatedb,
    rolcanlogin,
    rolreplication,
    rolconnlimit,
    rolvaliduntil
FROM pg_roles
WHERE rolname = current_user;

-- Check database permissions
SELECT 
    datname,
    datacl,
    datowner
FROM pg_database
WHERE datname = current_database();

-- Check table permissions
SELECT 
    schemaname,
    tablename,
    tableowner,
    has_table_privilege(current_user, schemaname||'.'||tablename, 'SELECT') as can_select,
    has_table_privilege(current_user, schemaname||'.'||tablename, 'INSERT') as can_insert,
    has_table_privilege(current_user, schemaname||'.'||tablename, 'UPDATE') as can_update,
    has_table_privilege(current_user, schemaname||'.'||tablename, 'DELETE') as can_delete
FROM pg_tables
WHERE schemaname = 'public'
LIMIT 5;

-- Check column permissions
SELECT 
    schemaname,
    tablename,
    columnname,
    has_column_privilege(current_user, schemaname||'.'||tablename||'.'||columnname, 'SELECT') as can_select,
    has_column_privilege(current_user, schemaname||'.'||tablename||'.'||columnname, 'INSERT') as can_insert,
    has_column_privilege(current_user, schemaname||'.'||tablename||'.'||columnname, 'UPDATE') as can_update
FROM pg_columns
WHERE schemaname = 'public'
LIMIT 5;
```

## 13.2 User and Role Management

PostgreSQL uses roles for user and permission management.

### Role Types:
- **Login Roles**: Can connect to database
- **Group Roles**: Cannot connect, used for grouping
- **Superuser Roles**: Full system access
- **Database Roles**: Database-specific access
- **Schema Roles**: Schema-specific access

### Real-World Analogy:
Roles are like different types of building access:
- **Login Roles** = Building residents
- **Group Roles** = Department groups
- **Superuser Roles** = Building managers
- **Database Roles** = Floor access
- **Schema Roles** = Room access

### SQL Example - User and Role Management:
```sql
-- Create login role
CREATE ROLE app_user WITH LOGIN PASSWORD 'secure_password';

-- Create group role
CREATE ROLE developers;

-- Create superuser role
CREATE ROLE admin_user WITH LOGIN PASSWORD 'admin_password' SUPERUSER;

-- Grant role to user
GRANT developers TO app_user;

-- Create database role
CREATE ROLE db_reader WITH LOGIN PASSWORD 'reader_password';

-- Grant database permissions
GRANT CONNECT ON DATABASE mydb TO db_reader;
GRANT USAGE ON SCHEMA public TO db_reader;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO db_reader;

-- Create schema role
CREATE ROLE schema_owner;

-- Grant schema permissions
GRANT USAGE ON SCHEMA public TO schema_owner;
GRANT CREATE ON SCHEMA public TO schema_owner;

-- Check role information
SELECT 
    rolname,
    rolsuper,
    rolinherit,
    rolcreaterole,
    rolcreatedb,
    rolcanlogin,
    rolreplication,
    rolconnlimit,
    rolvaliduntil
FROM pg_roles
ORDER BY rolname;

-- Check role memberships
SELECT 
    r.rolname as role_name,
    m.rolname as member_name
FROM pg_auth_members am
JOIN pg_roles r ON am.roleid = r.oid
JOIN pg_roles m ON am.member = m.oid
ORDER BY r.rolname, m.rolname;

-- Check role permissions
SELECT 
    grantor,
    grantee,
    table_schema,
    table_name,
    privilege_type,
    is_grantable
FROM information_schema.table_privileges
WHERE grantee = 'app_user'
ORDER BY table_schema, table_name, privilege_type;
```

## 13.3 Authentication Methods

PostgreSQL supports multiple authentication methods for different security requirements.

### Authentication Methods:
- **Trust**: No password required
- **MD5**: MD5 password hashing
- **SCRAM-SHA-256**: Modern password hashing
- **GSSAPI**: Kerberos authentication
- **SSPI**: Windows authentication
- **LDAP**: LDAP directory authentication
- **PAM**: Pluggable Authentication Modules

### Real-World Analogy:
Authentication methods are like different types of door locks:
- **Trust** = No lock (open door)
- **MD5** = Basic lock
- **SCRAM-SHA-256** = High-security lock
- **GSSAPI** = Key card system
- **SSPI** = Windows domain authentication
- **LDAP** = Central directory system
- **PAM** = Custom authentication system

### SQL Example - Authentication Methods:
```sql
-- Check authentication configuration
SELECT 
    name,
    setting,
    unit,
    context,
    short_desc
FROM pg_settings 
WHERE name IN ('password_encryption', 'ssl', 'ssl_cert_file', 'ssl_key_file');

-- Check password encryption
SHOW password_encryption;

-- Check SSL configuration
SHOW ssl;

-- Check SSL certificate file
SHOW ssl_cert_file;

-- Check SSL key file
SHOW ssl_key_file;

-- Create user with different authentication methods
-- MD5 authentication
CREATE ROLE md5_user WITH LOGIN PASSWORD 'md5_password';

-- SCRAM-SHA-256 authentication
CREATE ROLE scram_user WITH LOGIN PASSWORD 'scram_password';

-- Check user authentication methods
SELECT 
    rolname,
    rolpassword
FROM pg_authid
WHERE rolname IN ('md5_user', 'scram_user');

-- Check SSL connections
SELECT 
    client_addr,
    usename,
    application_name,
    client_port,
    backend_start,
    state
FROM pg_stat_activity
WHERE ssl = true;

-- Check authentication failures
SELECT 
    client_addr,
    usename,
    application_name,
    backend_start,
    state
FROM pg_stat_activity
WHERE state = 'idle'
ORDER BY backend_start DESC;
```

## 13.4 SSL/TLS Configuration

SSL/TLS provides encrypted connections between clients and PostgreSQL servers.

### SSL/TLS Features:
- **Encryption**: Data encryption in transit
- **Authentication**: Server and client authentication
- **Certificate Management**: SSL certificate handling
- **Cipher Suites**: Encryption algorithm selection
- **Protocol Versions**: SSL/TLS protocol versions

### Real-World Analogy:
SSL/TLS is like having a secure communication channel:
- **Encryption** = Encrypted phone line
- **Authentication** = Verified caller ID
- **Certificate Management** = Digital certificates
- **Cipher Suites** = Encryption algorithms
- **Protocol Versions** = Communication protocols

### SQL Example - SSL/TLS Configuration:
```sql
-- Check SSL configuration
SELECT 
    name,
    setting,
    unit,
    context,
    short_desc
FROM pg_settings 
WHERE name LIKE 'ssl%'
ORDER BY name;

-- Check SSL status
SHOW ssl;

-- Check SSL certificate file
SHOW ssl_cert_file;

-- Check SSL key file
SHOW ssl_key_file;

-- Check SSL CA file
SHOW ssl_ca_file;

-- Check SSL cipher suites
SHOW ssl_ciphers;

-- Check SSL protocol versions
SHOW ssl_min_protocol_version;

-- Check SSL connections
SELECT 
    client_addr,
    usename,
    application_name,
    client_port,
    backend_start,
    state,
    ssl,
    ssl_version,
    ssl_cipher,
    ssl_bits,
    ssl_compression
FROM pg_stat_activity
WHERE ssl = true
ORDER BY backend_start DESC;

-- Check SSL statistics
SELECT 
    ssl_is_used,
    COUNT(*) as connection_count
FROM pg_stat_activity
GROUP BY ssl_is_used;

-- Check SSL configuration in pg_hba.conf
-- hostssl all all 0.0.0.0/0 md5
-- host all all 0.0.0.0/0 md5
```

## 13.5 Row Level Security (RLS)

Row Level Security provides fine-grained access control at the row level.

### RLS Features:
- **Row-Level Policies**: Define access policies per row
- **Policy Types**: SELECT, INSERT, UPDATE, DELETE policies
- **Policy Functions**: Custom policy functions
- **Policy Inheritance**: Inherit policies from parent tables
- **Policy Bypass**: Superuser and table owner bypass

### Real-World Analogy:
RLS is like having different access levels for different rooms:
- **Row-Level Policies** = Room access rules
- **Policy Types** = Different types of access
- **Policy Functions** = Custom access logic
- **Policy Inheritance** = Inheriting access rules
- **Policy Bypass** = Master key access

### SQL Example - Row Level Security:
```sql
-- Create table with RLS
CREATE TABLE employees (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    department VARCHAR(50),
    salary NUMERIC(10,2),
    manager_id INTEGER
);

-- Enable RLS
ALTER TABLE employees ENABLE ROW LEVEL SECURITY;

-- Create policy for SELECT
CREATE POLICY emp_select_policy ON employees
    FOR SELECT
    USING (department = current_user);

-- Create policy for INSERT
CREATE POLICY emp_insert_policy ON employees
    FOR INSERT
    WITH CHECK (department = current_user);

-- Create policy for UPDATE
CREATE POLICY emp_update_policy ON employees
    FOR UPDATE
    USING (department = current_user)
    WITH CHECK (department = current_user);

-- Create policy for DELETE
CREATE POLICY emp_delete_policy ON employees
    FOR DELETE
    USING (department = current_user);

-- Insert sample data
INSERT INTO employees (name, department, salary, manager_id) VALUES
    ('John Doe', 'engineering', 75000, 1),
    ('Alice Smith', 'marketing', 65000, 2),
    ('Bob Wilson', 'engineering', 80000, 1),
    ('Carol Brown', 'marketing', 70000, 2);

-- Create users for different departments
CREATE ROLE engineering_user WITH LOGIN PASSWORD 'eng_password';
CREATE ROLE marketing_user WITH LOGIN PASSWORD 'mkt_password';

-- Grant table permissions
GRANT SELECT, INSERT, UPDATE, DELETE ON employees TO engineering_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON employees TO marketing_user;

-- Check RLS policies
SELECT 
    schemaname,
    tablename,
    policyname,
    permissive,
    roles,
    cmd,
    qual,
    with_check
FROM pg_policies
WHERE tablename = 'employees'
ORDER BY policyname;

-- Test RLS (simulate different users)
-- Set role to engineering user
SET ROLE engineering_user;
SELECT * FROM employees;

-- Set role to marketing user
SET ROLE marketing_user;
SELECT * FROM employees;

-- Reset role
RESET ROLE;

-- Check RLS status
SELECT 
    schemaname,
    tablename,
    rowsecurity
FROM pg_tables
WHERE tablename = 'employees';
```

## 13.6 Column Level Security

Column Level Security provides fine-grained access control at the column level.

### Column Security Features:
- **Column Permissions**: Grant/revoke column permissions
- **View-Based Security**: Use views for column security
- **Function-Based Security**: Use functions for column access
- **Dynamic Security**: Runtime column access control
- **Audit Trail**: Track column access

### Real-World Analogy:
Column security is like having different access levels for different parts of a document:
- **Column Permissions** = Section access control
- **View-Based Security** = Filtered document views
- **Function-Based Security** = Custom access logic
- **Dynamic Security** = Runtime access control
- **Audit Trail** = Access logging

### SQL Example - Column Level Security:
```sql
-- Create table with sensitive data
CREATE TABLE customer_data (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    phone VARCHAR(20),
    ssn VARCHAR(11),
    credit_score INTEGER,
    salary NUMERIC(10,2)
);

-- Create users with different access levels
CREATE ROLE basic_user WITH LOGIN PASSWORD 'basic_password';
CREATE ROLE manager_user WITH LOGIN PASSWORD 'manager_password';
CREATE ROLE admin_user WITH LOGIN PASSWORD 'admin_password';

-- Grant basic permissions (name and email only)
GRANT SELECT (id, name, email) ON customer_data TO basic_user;

-- Grant manager permissions (all except SSN)
GRANT SELECT (id, name, email, phone, credit_score, salary) ON customer_data TO manager_user;

-- Grant admin permissions (all columns)
GRANT SELECT ON customer_data TO admin_user;

-- Insert sample data
INSERT INTO customer_data (name, email, phone, ssn, credit_score, salary) VALUES
    ('John Doe', 'john@example.com', '555-1234', '123-45-6789', 750, 75000),
    ('Alice Smith', 'alice@example.com', '555-5678', '987-65-4321', 800, 85000);

-- Test column-level access
-- Set role to basic user
SET ROLE basic_user;
SELECT * FROM customer_data; -- This will fail
SELECT id, name, email FROM customer_data; -- This will work

-- Set role to manager user
SET ROLE manager_user;
SELECT id, name, email, phone, credit_score, salary FROM customer_data; -- This will work
SELECT ssn FROM customer_data; -- This will fail

-- Set role to admin user
SET ROLE admin_user;
SELECT * FROM customer_data; -- This will work

-- Reset role
RESET ROLE;

-- Check column permissions
SELECT 
    grantor,
    grantee,
    table_schema,
    table_name,
    column_name,
    privilege_type,
    is_grantable
FROM information_schema.column_privileges
WHERE table_name = 'customer_data'
ORDER BY grantee, column_name, privilege_type;

-- Create view for column security
CREATE VIEW customer_public AS
SELECT id, name, email
FROM customer_data;

-- Grant view permissions
GRANT SELECT ON customer_public TO basic_user;

-- Test view access
SET ROLE basic_user;
SELECT * FROM customer_public;
RESET ROLE;
```

## 13.7 Database Encryption

PostgreSQL provides multiple encryption options for data protection.

### Encryption Types:
- **Transit Encryption**: SSL/TLS for data in transit
- **At-Rest Encryption**: Data encryption on disk
- **Application-Level Encryption**: Application-managed encryption
- **Column-Level Encryption**: Encrypt specific columns
- **Key Management**: Encryption key management

### Real-World Analogy:
Database encryption is like having multiple layers of security:
- **Transit Encryption** = Secure delivery service
- **At-Rest Encryption** = Safe storage
- **Application-Level Encryption** = Custom security
- **Column-Level Encryption** = Individual item security
- **Key Management** = Key storage system

### SQL Example - Database Encryption:
```sql
-- Check encryption configuration
SELECT 
    name,
    setting,
    unit,
    context,
    short_desc
FROM pg_settings 
WHERE name IN ('ssl', 'ssl_cert_file', 'ssl_key_file', 'ssl_ca_file');

-- Check SSL encryption
SHOW ssl;

-- Check SSL certificate
SHOW ssl_cert_file;

-- Check SSL key
SHOW ssl_key_file;

-- Check SSL CA
SHOW ssl_ca_file;

-- Create table with encrypted columns
CREATE TABLE encrypted_data (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    encrypted_ssn BYTEA,
    encrypted_credit_score BYTEA
);

-- Insert encrypted data
INSERT INTO encrypted_data (name, encrypted_ssn, encrypted_credit_score) VALUES
    ('John Doe', 
     pgp_sym_encrypt('123-45-6789', 'encryption_key'),
     pgp_sym_encrypt('750', 'encryption_key')),
    ('Alice Smith',
     pgp_sym_encrypt('987-65-4321', 'encryption_key'),
     pgp_sym_encrypt('800', 'encryption_key'));

-- Query encrypted data
SELECT 
    name,
    pgp_sym_decrypt(encrypted_ssn, 'encryption_key') as ssn,
    pgp_sym_decrypt(encrypted_credit_score, 'encryption_key') as credit_score
FROM encrypted_data;

-- Check encryption functions
SELECT 
    proname,
    prosrc
FROM pg_proc
WHERE proname LIKE 'pgp_%'
ORDER BY proname;

-- Check SSL connections
SELECT 
    client_addr,
    usename,
    application_name,
    ssl,
    ssl_version,
    ssl_cipher,
    ssl_bits
FROM pg_stat_activity
WHERE ssl = true
ORDER BY backend_start DESC;

-- Check encryption statistics
SELECT 
    ssl_is_used,
    COUNT(*) as connection_count
FROM pg_stat_activity
GROUP BY ssl_is_used;
```

## 13.8 Audit Logging

Audit logging tracks database access and changes for security monitoring.

### Audit Features:
- **Connection Logging**: Track database connections
- **Query Logging**: Log SQL queries
- **Data Change Logging**: Track data modifications
- **Permission Logging**: Track permission changes
- **Security Event Logging**: Track security events

### Real-World Analogy:
Audit logging is like having a security camera system:
- **Connection Logging** = Tracking who enters
- **Query Logging** = Recording what they do
- **Data Change Logging** = Tracking what they change
- **Permission Logging** = Recording access changes
- **Security Event Logging** = Recording security incidents

### SQL Example - Audit Logging:
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

-- Check connection statistics
SELECT 
    datname,
    numbackends,
    xact_commit,
    xact_rollback,
    blks_read,
    blks_hit,
    tup_returned,
    tup_fetched,
    tup_inserted,
    tup_updated,
    tup_deleted
FROM pg_stat_database
WHERE datname = current_database();

-- Check table access statistics
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
ORDER BY n_tup_ins + n_tup_upd + n_tup_del DESC;
```

## 13.9 Security Best Practices

Following security best practices ensures robust database security.

### Best Practices:
- **Principle of Least Privilege**: Grant minimum required permissions
- **Regular Updates**: Keep PostgreSQL updated
- **Strong Passwords**: Use complex passwords
- **Network Security**: Secure network connections
- **Audit Monitoring**: Regular security monitoring

### Real-World Analogy:
Security best practices are like following safety protocols:
- **Principle of Least Privilege** = Only give necessary access
- **Regular Updates** = Keep security systems current
- **Strong Passwords** = Use complex locks
- **Network Security** = Secure communication channels
- **Audit Monitoring** = Regular security checks

### SQL Example - Security Best Practices:
```sql
-- Check user permissions
SELECT 
    grantor,
    grantee,
    table_schema,
    table_name,
    privilege_type,
    is_grantable
FROM information_schema.table_privileges
WHERE grantee = current_user
ORDER BY table_schema, table_name, privilege_type;

-- Check role memberships
SELECT 
    r.rolname as role_name,
    m.rolname as member_name
FROM pg_auth_members am
JOIN pg_roles r ON am.roleid = r.oid
JOIN pg_roles m ON am.member = m.oid
WHERE m.rolname = current_user
ORDER BY r.rolname;

-- Check superuser status
SELECT 
    rolname,
    rolsuper,
    rolcreaterole,
    rolcreatedb
FROM pg_roles
WHERE rolname = current_user;

-- Check password expiration
SELECT 
    rolname,
    rolvaliduntil
FROM pg_roles
WHERE rolname = current_user;

-- Check SSL connections
SELECT 
    client_addr,
    usename,
    application_name,
    ssl,
    ssl_version,
    ssl_cipher
FROM pg_stat_activity
WHERE ssl = true
ORDER BY backend_start DESC;

-- Check failed connections
SELECT 
    client_addr,
    usename,
    application_name,
    backend_start,
    state
FROM pg_stat_activity
WHERE state = 'idle'
ORDER BY backend_start DESC;

-- Check RLS policies
SELECT 
    schemaname,
    tablename,
    policyname,
    permissive,
    roles,
    cmd,
    qual,
    with_check
FROM pg_policies
ORDER BY schemaname, tablename, policyname;

-- Check column permissions
SELECT 
    grantor,
    grantee,
    table_schema,
    table_name,
    column_name,
    privilege_type,
    is_grantable
FROM information_schema.column_privileges
WHERE grantee = current_user
ORDER BY table_schema, table_name, column_name, privilege_type;
```

## 13.10 Compliance and Regulations

PostgreSQL security features help meet various compliance requirements.

### Compliance Standards:
- **GDPR**: General Data Protection Regulation
- **HIPAA**: Health Insurance Portability and Accountability Act
- **SOX**: Sarbanes-Oxley Act
- **PCI DSS**: Payment Card Industry Data Security Standard
- **ISO 27001**: Information Security Management

### Real-World Analogy:
Compliance is like meeting building safety codes:
- **GDPR** = Privacy protection standards
- **HIPAA** = Healthcare data protection
- **SOX** = Financial reporting standards
- **PCI DSS** = Payment data security
- **ISO 27001** = Information security management

### SQL Example - Compliance and Regulations:
```sql
-- Check data protection features
SELECT 
    name,
    setting,
    unit,
    context,
    short_desc
FROM pg_settings 
WHERE name IN (
    'log_statement',
    'log_connections',
    'log_disconnections',
    'log_hostname',
    'log_line_prefix',
    'ssl',
    'ssl_cert_file',
    'ssl_key_file',
    'ssl_ca_file'
);

-- Check audit logging configuration
SHOW log_statement;
SHOW log_connections;
SHOW log_disconnections;
SHOW log_hostname;
SHOW log_line_prefix;

-- Check SSL configuration
SHOW ssl;
SHOW ssl_cert_file;
SHOW ssl_key_file;
SHOW ssl_ca_file;

-- Check RLS policies for data protection
SELECT 
    schemaname,
    tablename,
    policyname,
    permissive,
    roles,
    cmd,
    qual,
    with_check
FROM pg_policies
ORDER BY schemaname, tablename, policyname;

-- Check column permissions for data access control
SELECT 
    grantor,
    grantee,
    table_schema,
    table_name,
    column_name,
    privilege_type,
    is_grantable
FROM information_schema.column_privileges
ORDER BY table_schema, table_name, grantee, column_name;

-- Check user access patterns
SELECT 
    usename,
    application_name,
    client_addr,
    backend_start,
    state,
    ssl
FROM pg_stat_activity
ORDER BY backend_start DESC;

-- Check data modification tracking
SELECT 
    schemaname,
    tablename,
    n_tup_ins,
    n_tup_upd,
    n_tup_del,
    n_live_tup,
    n_dead_tup
FROM pg_stat_user_tables
ORDER BY n_tup_ins + n_tup_upd + n_tup_del DESC;
```