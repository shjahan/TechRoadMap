# Section 22 – Testing and Quality Assurance

## 22.1 Database Testing Fundamentals

Database testing ensures data integrity, performance, and reliability through systematic validation of database functionality.

### Key Testing Types:
- **Unit Testing**: Testing individual database functions
- **Integration Testing**: Testing database interactions
- **Performance Testing**: Testing database performance
- **Security Testing**: Testing database security

### Real-World Analogy:
Database testing is like quality control in manufacturing:
- **Unit Testing** = Testing individual components
- **Integration Testing** = Testing component interactions
- **Performance Testing** = Stress testing the system
- **Security Testing** = Security vulnerability testing

### Example:
```sql
-- Create test database
CREATE DATABASE test_db;

-- Create test schema
CREATE SCHEMA test_schema;

-- Create test tables
CREATE TABLE test_users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Create test data
INSERT INTO test_users (username, email) VALUES
('testuser1', 'test1@example.com'),
('testuser2', 'test2@example.com'),
('testuser3', 'test3@example.com');

-- Create test function
CREATE OR REPLACE FUNCTION test_user_creation()
RETURNS BOOLEAN AS $$
DECLARE
    user_count INTEGER;
BEGIN
    -- Test user creation
    INSERT INTO test_users (username, email) 
    VALUES ('newuser', 'newuser@example.com');
    
    -- Verify user was created
    SELECT COUNT(*) INTO user_count
    FROM test_users
    WHERE username = 'newuser';
    
    RETURN user_count = 1;
END;
$$ LANGUAGE plpgsql;
```

## 22.2 Unit Testing

Unit testing validates individual database functions, procedures, and triggers in isolation.

### Unit Testing Components:
- **Test Functions**: Functions that test specific functionality
- **Test Data**: Controlled test data sets
- **Assertions**: Validation of expected results
- **Test Execution**: Automated test running

### Real-World Analogy:
Unit testing is like testing individual car parts:
- **Test Functions** = Testing procedures
- **Test Data** = Test scenarios
- **Assertions** = Pass/fail criteria
- **Test Execution** = Automated testing

### Example:
```sql
-- Create unit test framework
CREATE TABLE unit_tests (
    id SERIAL PRIMARY KEY,
    test_name VARCHAR(100) NOT NULL,
    test_function VARCHAR(100) NOT NULL,
    expected_result BOOLEAN,
    actual_result BOOLEAN,
    test_data JSONB,
    status VARCHAR(20) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT NOW(),
    executed_at TIMESTAMP
);

-- Create test execution function
CREATE OR REPLACE FUNCTION run_unit_test(test_id INTEGER)
RETURNS BOOLEAN AS $$
DECLARE
    test_record RECORD;
    result BOOLEAN;
BEGIN
    -- Get test details
    SELECT * INTO test_record
    FROM unit_tests
    WHERE id = test_id;
    
    -- Execute test function
    EXECUTE 'SELECT ' || test_record.test_function || '()' INTO result;
    
    -- Update test results
    UPDATE unit_tests
    SET 
        actual_result = result,
        status = CASE WHEN result = test_record.expected_result THEN 'passed' ELSE 'failed' END,
        executed_at = NOW()
    WHERE id = test_id;
    
    RETURN result = test_record.expected_result;
END;
$$ LANGUAGE plpgsql;

-- Add test cases
INSERT INTO unit_tests (test_name, test_function, expected_result, test_data)
VALUES 
('User Creation Test', 'test_user_creation', TRUE, '{}'),
('User Validation Test', 'test_user_validation', TRUE, '{}'),
('User Deletion Test', 'test_user_deletion', TRUE, '{}');
```

## 22.3 Integration Testing

Integration testing validates how different database components work together.

### Integration Testing Areas:
- **Data Flow**: Testing data movement between components
- **Transaction Integrity**: Testing transaction boundaries
- **Concurrency**: Testing concurrent operations
- **Error Handling**: Testing error scenarios

### Real-World Analogy:
Integration testing is like testing how different car systems work together:
- **Data Flow** = Testing fuel flow through the engine
- **Transaction Integrity** = Testing gear shifting
- **Concurrency** = Testing multiple systems simultaneously
- **Error Handling** = Testing safety systems

### Example:
```sql
-- Create integration test tables
CREATE TABLE test_orders (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES test_users(id),
    total_amount DECIMAL(10,2),
    status VARCHAR(20) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE test_order_items (
    id SERIAL PRIMARY KEY,
    order_id INTEGER REFERENCES test_orders(id),
    product_name VARCHAR(100),
    quantity INTEGER,
    unit_price DECIMAL(10,2)
);

-- Create integration test function
CREATE OR REPLACE FUNCTION test_order_creation()
RETURNS BOOLEAN AS $$
DECLARE
    order_id INTEGER;
    item_count INTEGER;
    total_amount DECIMAL(10,2);
BEGIN
    -- Create order
    INSERT INTO test_orders (user_id, total_amount)
    VALUES (1, 100.00)
    RETURNING id INTO order_id;
    
    -- Add order items
    INSERT INTO test_order_items (order_id, product_name, quantity, unit_price)
    VALUES 
    (order_id, 'Product A', 2, 30.00),
    (order_id, 'Product B', 1, 40.00);
    
    -- Verify order creation
    SELECT COUNT(*) INTO item_count
    FROM test_order_items
    WHERE order_id = order_id;
    
    -- Verify total amount
    SELECT total_amount INTO total_amount
    FROM test_orders
    WHERE id = order_id;
    
    RETURN item_count = 2 AND total_amount = 100.00;
END;
$$ LANGUAGE plpgsql;
```

## 22.4 Performance Testing

Performance testing validates database performance under various load conditions.

### Performance Testing Types:
- **Load Testing**: Testing under normal expected load
- **Stress Testing**: Testing under extreme load
- **Volume Testing**: Testing with large data volumes
- **Concurrency Testing**: Testing with multiple users

### Real-World Analogy:
Performance testing is like testing a car's performance:
- **Load Testing** = Normal driving conditions
- **Stress Testing** = Extreme driving conditions
- **Volume Testing** = Testing with heavy cargo
- **Concurrency Testing** = Testing with multiple passengers

### Example:
```sql
-- Create performance test data
CREATE TABLE performance_test (
    id SERIAL PRIMARY KEY,
    data TEXT,
    value INTEGER,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Generate test data
INSERT INTO performance_test (data, value)
SELECT 
    'Test data ' || generate_series(1, 100000),
    (random() * 1000)::INTEGER
FROM generate_series(1, 100000);

-- Create performance test function
CREATE OR REPLACE FUNCTION test_query_performance()
RETURNS TABLE(
    test_name TEXT,
    execution_time INTEGER,
    result_count BIGINT,
    status TEXT
) AS $$
DECLARE
    start_time TIMESTAMP;
    end_time TIMESTAMP;
    execution_time INTEGER;
    result_count BIGINT;
BEGIN
    -- Test 1: Simple SELECT
    start_time := clock_timestamp();
    SELECT COUNT(*) INTO result_count FROM performance_test WHERE value > 500;
    end_time := clock_timestamp();
    execution_time := EXTRACT(EPOCH FROM (end_time - start_time))::INTEGER;
    
    RETURN QUERY
    SELECT 
        'Simple SELECT'::TEXT,
        execution_time,
        result_count,
        CASE WHEN execution_time < 1000 THEN 'PASS' ELSE 'FAIL' END;
    
    -- Test 2: Complex JOIN
    start_time := clock_timestamp();
    SELECT COUNT(*) INTO result_count
    FROM performance_test p1
    JOIN performance_test p2 ON p1.value = p2.value
    WHERE p1.id < p2.id;
    end_time := clock_timestamp();
    execution_time := EXTRACT(EPOCH FROM (end_time - start_time))::INTEGER;
    
    RETURN QUERY
    SELECT 
        'Complex JOIN'::TEXT,
        execution_time,
        result_count,
        CASE WHEN execution_time < 5000 THEN 'PASS' ELSE 'FAIL' END;
END;
$$ LANGUAGE plpgsql;
```

## 22.5 Security Testing

Security testing validates database security measures and identifies vulnerabilities.

### Security Testing Areas:
- **Authentication**: Testing user authentication
- **Authorization**: Testing access control
- **Data Encryption**: Testing data protection
- **SQL Injection**: Testing injection vulnerabilities

### Real-World Analogy:
Security testing is like testing a building's security system:
- **Authentication** = Testing access cards
- **Authorization** = Testing restricted areas
- **Data Encryption** = Testing secure storage
- **SQL Injection** = Testing for forced entry

### Example:
```sql
-- Create security test tables
CREATE TABLE security_test_users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) DEFAULT 'user',
    created_at TIMESTAMP DEFAULT NOW()
);

-- Create security test function
CREATE OR REPLACE FUNCTION test_sql_injection()
RETURNS TABLE(
    test_case TEXT,
    input_value TEXT,
    is_vulnerable BOOLEAN,
    status TEXT
) AS $$
DECLARE
    test_inputs TEXT[] := ARRAY[
        '1 OR 1=1',
        '1; DROP TABLE security_test_users;',
        '1 UNION SELECT * FROM security_test_users',
        '1 AND (SELECT COUNT(*) FROM security_test_users) > 0'
    ];
    input_value TEXT;
    is_vulnerable BOOLEAN;
BEGIN
    FOREACH input_value IN ARRAY test_inputs
    LOOP
        -- Test for SQL injection vulnerability
        BEGIN
            EXECUTE 'SELECT COUNT(*) FROM security_test_users WHERE id = ' || input_value;
            is_vulnerable := TRUE;
        EXCEPTION
            WHEN OTHERS THEN
                is_vulnerable := FALSE;
        END;
        
        RETURN QUERY
        SELECT 
            'SQL Injection Test'::TEXT,
            input_value,
            is_vulnerable,
            CASE WHEN is_vulnerable THEN 'VULNERABLE' ELSE 'SAFE' END;
    END LOOP;
END;
$$ LANGUAGE plpgsql;

-- Create authentication test
CREATE OR REPLACE FUNCTION test_authentication()
RETURNS TABLE(
    test_case TEXT,
    username TEXT,
    password TEXT,
    is_authenticated BOOLEAN,
    status TEXT
) AS $$
DECLARE
    test_credentials RECORD;
BEGIN
    FOR test_credentials IN
        SELECT 
            'valid_user' as username,
            'valid_password' as password,
            TRUE as expected
        UNION ALL
        SELECT 
            'invalid_user' as username,
            'invalid_password' as password,
            FALSE as expected
    LOOP
        -- Test authentication
        DECLARE
            user_exists BOOLEAN;
        BEGIN
            SELECT EXISTS(
                SELECT 1 FROM security_test_users
                WHERE username = test_credentials.username
                AND password_hash = crypt(test_credentials.password, password_hash)
            ) INTO user_exists;
            
            RETURN QUERY
            SELECT 
                'Authentication Test'::TEXT,
                test_credentials.username,
                test_credentials.password,
                user_exists,
                CASE 
                    WHEN user_exists = test_credentials.expected THEN 'PASS'
                    ELSE 'FAIL'
                END;
        END;
    END LOOP;
END;
$$ LANGUAGE plpgsql;
```

## 22.6 Data Quality Testing

Data quality testing ensures data accuracy, completeness, and consistency.

### Data Quality Dimensions:
- **Accuracy**: Data correctness
- **Completeness**: Data availability
- **Consistency**: Data uniformity
- **Validity**: Data format compliance

### Real-World Analogy:
Data quality testing is like quality control in food production:
- **Accuracy** = Correct ingredients
- **Completeness** = All required ingredients
- **Consistency** = Uniform quality
- **Validity** = Proper packaging

### Example:
```sql
-- Create data quality test function
CREATE OR REPLACE FUNCTION test_data_quality()
RETURNS TABLE(
    quality_dimension TEXT,
    test_result TEXT,
    status TEXT,
    recommendation TEXT
) AS $$
BEGIN
    -- Test data accuracy
    RETURN QUERY
    SELECT 
        'Accuracy'::TEXT,
        'Checking for invalid email formats'::TEXT,
        CASE 
            WHEN COUNT(*) = 0 THEN 'PASS'
            ELSE 'FAIL'
        END,
        CASE 
            WHEN COUNT(*) = 0 THEN 'All emails are valid'
            ELSE 'Fix invalid email formats'
        END
    FROM test_users
    WHERE email !~ '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$';
    
    -- Test data completeness
    RETURN QUERY
    SELECT 
        'Completeness'::TEXT,
        'Checking for missing usernames'::TEXT,
        CASE 
            WHEN COUNT(*) = 0 THEN 'PASS'
            ELSE 'FAIL'
        END,
        CASE 
            WHEN COUNT(*) = 0 THEN 'All users have usernames'
            ELSE 'Fill in missing usernames'
        END
    FROM test_users
    WHERE username IS NULL OR username = '';
    
    -- Test data consistency
    RETURN QUERY
    SELECT 
        'Consistency'::TEXT,
        'Checking for duplicate usernames'::TEXT,
        CASE 
            WHEN COUNT(*) = 0 THEN 'PASS'
            ELSE 'FAIL'
        END,
        CASE 
            WHEN COUNT(*) = 0 THEN 'No duplicate usernames'
            ELSE 'Remove duplicate usernames'
        END
    FROM (
        SELECT username, COUNT(*)
        FROM test_users
        GROUP BY username
        HAVING COUNT(*) > 1
    ) duplicates;
    
    -- Test data validity
    RETURN QUERY
    SELECT 
        'Validity'::TEXT,
        'Checking for future creation dates'::TEXT,
        CASE 
            WHEN COUNT(*) = 0 THEN 'PASS'
            ELSE 'FAIL'
        END,
        CASE 
            WHEN COUNT(*) = 0 THEN 'All dates are valid'
            ELSE 'Fix future creation dates'
        END
    FROM test_users
    WHERE created_at > NOW();
END;
$$ LANGUAGE plpgsql;
```

## 22.7 Test Automation

Test automation involves creating automated test suites that can run without manual intervention.

### Automation Components:
- **Test Scripts**: Automated test execution scripts
- **Test Data Management**: Automated test data setup
- **Test Reporting**: Automated test result reporting
- **Continuous Integration**: Automated test execution in CI/CD

### Real-World Analogy:
Test automation is like having a robot assembly line:
- **Test Scripts** = Automated assembly procedures
- **Test Data Management** = Automated material handling
- **Test Reporting** = Automated quality reports
- **Continuous Integration** = Automated production line

### Example:
```sql
-- Create test automation framework
CREATE TABLE test_suites (
    id SERIAL PRIMARY KEY,
    suite_name VARCHAR(100) NOT NULL,
    description TEXT,
    status VARCHAR(20) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT NOW(),
    executed_at TIMESTAMP
);

CREATE TABLE test_results (
    id SERIAL PRIMARY KEY,
    suite_id INTEGER REFERENCES test_suites(id),
    test_name VARCHAR(100) NOT NULL,
    status VARCHAR(20) NOT NULL,
    execution_time INTEGER,
    error_message TEXT,
    executed_at TIMESTAMP DEFAULT NOW()
);

-- Create test suite execution function
CREATE OR REPLACE FUNCTION execute_test_suite(suite_id INTEGER)
RETURNS BOOLEAN AS $$
DECLARE
    suite_record RECORD;
    test_record RECORD;
    all_passed BOOLEAN := TRUE;
    start_time TIMESTAMP;
    end_time TIMESTAMP;
BEGIN
    -- Get suite details
    SELECT * INTO suite_record
    FROM test_suites
    WHERE id = suite_id;
    
    -- Mark suite as running
    UPDATE test_suites
    SET status = 'running', executed_at = NOW()
    WHERE id = suite_id;
    
    -- Execute all tests in the suite
    FOR test_record IN
        SELECT * FROM unit_tests
        WHERE test_name LIKE '%' || suite_record.suite_name || '%'
    LOOP
        start_time := clock_timestamp();
        
        -- Execute individual test
        DECLARE
            test_result BOOLEAN;
        BEGIN
            EXECUTE 'SELECT ' || test_record.test_function || '()' INTO test_result;
            
            end_time := clock_timestamp();
            
            -- Record test result
            INSERT INTO test_results (suite_id, test_name, status, execution_time, executed_at)
            VALUES (
                suite_id,
                test_record.test_name,
                CASE WHEN test_result THEN 'passed' ELSE 'failed' END,
                EXTRACT(EPOCH FROM (end_time - start_time))::INTEGER,
                NOW()
            );
            
            IF NOT test_result THEN
                all_passed := FALSE;
            END IF;
        EXCEPTION
            WHEN OTHERS THEN
                end_time := clock_timestamp();
                
                INSERT INTO test_results (suite_id, test_name, status, execution_time, error_message, executed_at)
                VALUES (
                    suite_id,
                    test_record.test_name,
                    'error',
                    EXTRACT(EPOCH FROM (end_time - start_time))::INTEGER,
                    SQLERRM,
                    NOW()
                );
                
                all_passed := FALSE;
        END;
    END LOOP;
    
    -- Update suite status
    UPDATE test_suites
    SET status = CASE WHEN all_passed THEN 'passed' ELSE 'failed' END
    WHERE id = suite_id;
    
    RETURN all_passed;
END;
$$ LANGUAGE plpgsql;
```

## 22.8 Test Data Management

Test data management involves creating, maintaining, and cleaning test data for consistent testing.

### Data Management Tasks:
- **Data Generation**: Creating test data
- **Data Seeding**: Populating test databases
- **Data Cleanup**: Cleaning up after tests
- **Data Masking**: Protecting sensitive data

### Real-World Analogy:
Test data management is like managing a test kitchen:
- **Data Generation** = Preparing test ingredients
- **Data Seeding** = Setting up test recipes
- **Data Cleanup** = Cleaning up after testing
- **Data Masking** = Protecting secret recipes

### Example:
```sql
-- Create test data generation function
CREATE OR REPLACE FUNCTION generate_test_data(table_name VARCHAR(100), record_count INTEGER)
RETURNS VOID AS $$
DECLARE
    i INTEGER;
BEGIN
    CASE table_name
        WHEN 'test_users' THEN
            FOR i IN 1..record_count LOOP
                INSERT INTO test_users (username, email)
                VALUES (
                    'testuser' || i,
                    'testuser' || i || '@example.com'
                );
            END LOOP;
        
        WHEN 'test_orders' THEN
            FOR i IN 1..record_count LOOP
                INSERT INTO test_orders (user_id, total_amount, status)
                VALUES (
                    (random() * 100)::INTEGER + 1,
                    (random() * 1000)::DECIMAL(10,2),
                    CASE (random() * 3)::INTEGER
                        WHEN 0 THEN 'pending'
                        WHEN 1 THEN 'completed'
                        ELSE 'cancelled'
                    END
                );
            END LOOP;
        
        ELSE
            RAISE EXCEPTION 'Unknown table: %', table_name;
    END CASE;
END;
$$ LANGUAGE plpgsql;

-- Create test data cleanup function
CREATE OR REPLACE FUNCTION cleanup_test_data()
RETURNS VOID AS $$
BEGIN
    -- Clean up test tables
    TRUNCATE TABLE test_order_items CASCADE;
    TRUNCATE TABLE test_orders CASCADE;
    TRUNCATE TABLE test_users CASCADE;
    TRUNCATE TABLE performance_test CASCADE;
    TRUNCATE TABLE security_test_users CASCADE;
    
    -- Reset sequences
    ALTER SEQUENCE test_users_id_seq RESTART WITH 1;
    ALTER SEQUENCE test_orders_id_seq RESTART WITH 1;
    ALTER SEQUENCE test_order_items_id_seq RESTART WITH 1;
    ALTER SEQUENCE performance_test_id_seq RESTART WITH 1;
    ALTER SEQUENCE security_test_users_id_seq RESTART WITH 1;
END;
$$ LANGUAGE plpgsql;
```

## 22.9 Test Reporting

Test reporting provides comprehensive information about test execution and results.

### Report Types:
- **Test Summary**: Overall test results
- **Detailed Reports**: Individual test results
- **Trend Reports**: Test results over time
- **Coverage Reports**: Test coverage analysis

### Real-World Analogy:
Test reporting is like quality control reports:
- **Test Summary** = Overall quality summary
- **Detailed Reports** = Individual component reports
- **Trend Reports** = Quality trends over time
- **Coverage Reports** = Coverage analysis

### Example:
```sql
-- Create test reporting function
CREATE OR REPLACE FUNCTION generate_test_report(suite_id INTEGER)
RETURNS TABLE(
    report_section TEXT,
    report_data JSONB
) AS $$
BEGIN
    -- Test summary
    RETURN QUERY
    SELECT 
        'Test Summary'::TEXT,
        json_build_object(
            'total_tests', COUNT(*),
            'passed_tests', COUNT(*) FILTER (WHERE status = 'passed'),
            'failed_tests', COUNT(*) FILTER (WHERE status = 'failed'),
            'error_tests', COUNT(*) FILTER (WHERE status = 'error'),
            'pass_rate', ROUND(COUNT(*) FILTER (WHERE status = 'passed')::DECIMAL / COUNT(*) * 100, 2)
        )
    FROM test_results
    WHERE suite_id = $1;
    
    -- Test details
    RETURN QUERY
    SELECT 
        'Test Details'::TEXT,
        json_agg(
            json_build_object(
                'test_name', test_name,
                'status', status,
                'execution_time', execution_time,
                'error_message', error_message,
                'executed_at', executed_at
            )
        )
    FROM test_results
    WHERE suite_id = $1
    ORDER BY executed_at DESC;
    
    -- Performance metrics
    RETURN QUERY
    SELECT 
        'Performance Metrics'::TEXT,
        json_build_object(
            'total_execution_time', SUM(execution_time),
            'average_execution_time', ROUND(AVG(execution_time), 2),
            'max_execution_time', MAX(execution_time),
            'min_execution_time', MIN(execution_time)
        )
    FROM test_results
    WHERE suite_id = $1;
END;
$$ LANGUAGE plpgsql;
```

## 22.10 Best Practices

Best practices for database testing ensure effective and reliable testing processes.

### Key Practices:
- **Test Isolation**: Ensuring tests don't interfere with each other
- **Test Data Management**: Proper test data handling
- **Test Automation**: Automating repetitive testing tasks
- **Continuous Testing**: Integrating testing into development workflow

### Real-World Analogy:
Best practices are like following professional standards:
- **Test Isolation** = Separate testing areas
- **Test Data Management** = Proper material handling
- **Test Automation** = Automated quality control
- **Continuous Testing** = Continuous quality monitoring

### Example:
```sql
-- Create best practices monitoring function
CREATE OR REPLACE FUNCTION check_testing_best_practices()
RETURNS TABLE(
    practice_name TEXT,
    status TEXT,
    recommendation TEXT
) AS $$
BEGIN
    -- Check test isolation
    RETURN QUERY
    SELECT 
        'Test Isolation'::TEXT,
        CASE 
            WHEN EXISTS (SELECT 1 FROM test_suites WHERE status = 'running') THEN 'NEEDS_ATTENTION'
            ELSE 'GOOD'
        END,
        CASE 
            WHEN EXISTS (SELECT 1 FROM test_suites WHERE status = 'running') THEN 'Complete running tests before starting new ones'
            ELSE 'Test isolation is maintained'
        END;
    
    -- Check test data management
    RETURN QUERY
    SELECT 
        'Test Data Management'::TEXT,
        CASE 
            WHEN COUNT(*) > 1000 THEN 'NEEDS_ATTENTION'
            ELSE 'GOOD'
        END,
        CASE 
            WHEN COUNT(*) > 1000 THEN 'Consider cleaning up old test data'
            ELSE 'Test data management is good'
        END
    FROM test_results
    WHERE executed_at < NOW() - INTERVAL '30 days';
    
    -- Check test automation
    RETURN QUERY
    SELECT 
        'Test Automation'::TEXT,
        CASE 
            WHEN COUNT(*) > 0 THEN 'GOOD'
            ELSE 'NEEDS_ATTENTION'
        END,
        CASE 
            WHEN COUNT(*) > 0 THEN 'Test automation is implemented'
            ELSE 'Implement test automation'
        END
    FROM test_suites
    WHERE status IN ('passed', 'failed');
END;
$$ LANGUAGE plpgsql;
```