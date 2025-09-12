# Section 8 – Stored Procedures and Functions

## 8.1 PL/pgSQL Fundamentals

PL/pgSQL is PostgreSQL's procedural language for creating stored procedures and functions.

### PL/pgSQL Features:
- **Block Structure**: BEGIN...END blocks for code organization
- **Variables**: DECLARE section for variable declarations
- **Control Structures**: IF, LOOP, WHILE, FOR statements
- **Exception Handling**: TRY...CATCH equivalent with EXCEPTION
- **SQL Integration**: Seamless integration with SQL

### Real-World Analogy:
PL/pgSQL is like a programming language for databases:
- **Block Structure** = Code organization like functions
- **Variables** = Memory storage for values
- **Control Structures** = Decision making and repetition
- **Exception Handling** = Error management
- **SQL Integration** = Direct database access

### SQL Example - PL/pgSQL Basics:
```sql
-- Simple function
CREATE OR REPLACE FUNCTION get_customer_count()
RETURNS INTEGER AS $$
BEGIN
    RETURN (SELECT COUNT(*) FROM customers);
END;
$$ LANGUAGE plpgsql;

-- Function with parameters
CREATE OR REPLACE FUNCTION get_customer_by_id(customer_id INTEGER)
RETURNS TABLE(name VARCHAR, email VARCHAR) AS $$
BEGIN
    RETURN QUERY
    SELECT c.name, c.email
    FROM customers c
    WHERE c.customer_id = $1;
END;
$$ LANGUAGE plpgsql;

-- Function with variables
CREATE OR REPLACE FUNCTION calculate_order_total(order_id INTEGER)
RETURNS NUMERIC AS $$
DECLARE
    total_amount NUMERIC := 0;
    item_count INTEGER;
BEGIN
    SELECT COUNT(*), COALESCE(SUM(quantity * unit_price), 0)
    INTO item_count, total_amount
    FROM order_items
    WHERE order_id = $1;
    
    RETURN total_amount;
END;
$$ LANGUAGE plpgsql;
```

## 8.2 Function Creation and Management

PostgreSQL provides comprehensive tools for creating and managing functions.

### Function Types:
- **Scalar Functions**: Return single values
- **Table Functions**: Return table-like results
- **Aggregate Functions**: Custom aggregation logic
- **Window Functions**: Custom window function logic
- **Trigger Functions**: Functions called by triggers

### Function Management:
- **CREATE FUNCTION**: Create new functions
- **ALTER FUNCTION**: Modify function properties
- **DROP FUNCTION**: Remove functions
- **GRANT/REVOKE**: Manage function permissions
- **Function Overloading**: Multiple functions with same name

### Real-World Analogy:
Function management is like managing a library of tools:
- **Scalar Functions** = Simple tools that return one result
- **Table Functions** = Tools that return multiple results
- **Aggregate Functions** = Tools that summarize data
- **Window Functions** = Tools that work with data windows
- **Trigger Functions** = Tools that respond to events

### SQL Example - Function Management:
```sql
-- Create scalar function
CREATE OR REPLACE FUNCTION format_currency(amount NUMERIC)
RETURNS TEXT AS $$
BEGIN
    RETURN '$' || TO_CHAR(amount, 'FM999,999.00');
END;
$$ LANGUAGE plpgsql;

-- Create table function
CREATE OR REPLACE FUNCTION get_top_customers(limit_count INTEGER)
RETURNS TABLE(
    customer_id INTEGER,
    customer_name VARCHAR,
    total_orders INTEGER,
    total_spent NUMERIC
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        c.customer_id,
        c.name,
        COUNT(o.order_id)::INTEGER,
        COALESCE(SUM(o.total_amount), 0)
    FROM customers c
    LEFT JOIN orders o ON c.customer_id = o.customer_id
    GROUP BY c.customer_id, c.name
    ORDER BY total_spent DESC
    LIMIT limit_count;
END;
$$ LANGUAGE plpgsql;

-- Create aggregate function
CREATE OR REPLACE FUNCTION median(NUMERIC)
RETURNS NUMERIC AS $$
BEGIN
    RETURN (
        SELECT PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY $1)
        FROM unnest($1) AS value
    );
END;
$$ LANGUAGE plpgsql;

-- Function overloading
CREATE OR REPLACE FUNCTION calculate_discount(amount NUMERIC)
RETURNS NUMERIC AS $$
BEGIN
    IF amount >= 1000 THEN
        RETURN amount * 0.1;
    ELSE
        RETURN amount * 0.05;
    END IF;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION calculate_discount(amount NUMERIC, rate NUMERIC)
RETURNS NUMERIC AS $$
BEGIN
    RETURN amount * rate;
END;
$$ LANGUAGE plpgsql;

-- Alter function
ALTER FUNCTION calculate_discount(NUMERIC) OWNER TO postgres;

-- Grant permissions
GRANT EXECUTE ON FUNCTION calculate_discount(NUMERIC) TO public;

-- Drop function
DROP FUNCTION IF EXISTS calculate_discount(NUMERIC, NUMERIC);
```

## 8.3 Stored Procedures

PostgreSQL 11+ supports stored procedures with transaction control.

### Stored Procedure Features:
- **Transaction Control**: COMMIT/ROLLBACK within procedures
- **Output Parameters**: INOUT parameters for returning values
- **Exception Handling**: Comprehensive error handling
- **Nested Transactions**: Savepoints for partial rollbacks
- **Security**: Definer/Invoker rights

### Real-World Analogy:
Stored procedures are like automated workflows:
- **Transaction Control** = Ability to commit or rollback work
- **Output Parameters** = Returning results from the workflow
- **Exception Handling** = Error recovery procedures
- **Nested Transactions** = Checkpoints in the workflow
- **Security** = Access control for the workflow

### SQL Example - Stored Procedures:
```sql
-- Create stored procedure
CREATE OR REPLACE PROCEDURE process_order(
    p_customer_id INTEGER,
    p_order_date DATE,
    p_total_amount NUMERIC,
    OUT p_order_id INTEGER
) AS $$
DECLARE
    v_order_id INTEGER;
BEGIN
    -- Start transaction
    BEGIN
        -- Insert order
        INSERT INTO orders (customer_id, order_date, total_amount, status)
        VALUES (p_customer_id, p_order_date, p_total_amount, 'pending')
        RETURNING order_id INTO v_order_id;
        
        -- Update customer statistics
        UPDATE customers 
        SET last_order_date = p_order_date
        WHERE customer_id = p_customer_id;
        
        -- Set output parameter
        p_order_id := v_order_id;
        
        -- Commit transaction
        COMMIT;
        
    EXCEPTION
        WHEN OTHERS THEN
            ROLLBACK;
            RAISE;
    END;
END;
$$ LANGUAGE plpgsql;

-- Call stored procedure
CALL process_order(1, '2024-01-15', 150.00, NULL);

-- Procedure with savepoints
CREATE OR REPLACE PROCEDURE complex_order_processing(
    p_customer_id INTEGER,
    p_items JSONB
) AS $$
DECLARE
    v_order_id INTEGER;
    v_item RECORD;
BEGIN
    -- Start transaction
    BEGIN
        -- Create order
        INSERT INTO orders (customer_id, order_date, total_amount, status)
        VALUES (p_customer_id, CURRENT_DATE, 0, 'processing')
        RETURNING order_id INTO v_order_id;
        
        -- Process items
        FOR v_item IN SELECT * FROM jsonb_to_recordset(p_items) AS x(
            product_name TEXT,
            quantity INTEGER,
            unit_price NUMERIC
        )
        LOOP
            -- Savepoint for each item
            SAVEPOINT item_processing;
            
            BEGIN
                -- Insert order item
                INSERT INTO order_items (order_id, product_name, quantity, unit_price)
                VALUES (v_order_id, v_item.product_name, v_item.quantity, v_item.unit_price);
                
            EXCEPTION
                WHEN OTHERS THEN
                    ROLLBACK TO SAVEPOINT item_processing;
                    RAISE NOTICE 'Failed to process item: %', v_item.product_name;
            END;
        END LOOP;
        
        -- Update order total
        UPDATE orders 
        SET total_amount = (
            SELECT COALESCE(SUM(quantity * unit_price), 0)
            FROM order_items
            WHERE order_id = v_order_id
        )
        WHERE order_id = v_order_id;
        
        -- Commit transaction
        COMMIT;
        
    EXCEPTION
        WHEN OTHERS THEN
            ROLLBACK;
            RAISE;
    END;
END;
$$ LANGUAGE plpgsql;
```

## 8.4 Triggers and Trigger Functions

Triggers automatically execute functions when specific database events occur.

### Trigger Types:
- **BEFORE Triggers**: Execute before the event
- **AFTER Triggers**: Execute after the event
- **INSTEAD OF Triggers**: Replace the event (views only)
- **Row-Level Triggers**: Execute for each row
- **Statement-Level Triggers**: Execute once per statement

### Trigger Events:
- **INSERT**: When new rows are inserted
- **UPDATE**: When rows are updated
- **DELETE**: When rows are deleted
- **TRUNCATE**: When tables are truncated

### Real-World Analogy:
Triggers are like automatic responses:
- **BEFORE Triggers** = Pre-flight checks
- **AFTER Triggers** = Post-action notifications
- **INSTEAD OF Triggers** = Custom replacements
- **Row-Level Triggers** = Per-item processing
- **Statement-Level Triggers** = Batch processing

### SQL Example - Triggers and Trigger Functions:
```sql
-- Create trigger function for audit logging
CREATE OR REPLACE FUNCTION audit_trigger_function()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        INSERT INTO audit_log (table_name, operation, old_values, new_values, changed_by, changed_at)
        VALUES (TG_TABLE_NAME, TG_OP, NULL, row_to_json(NEW), current_user, CURRENT_TIMESTAMP);
        RETURN NEW;
    ELSIF TG_OP = 'UPDATE' THEN
        INSERT INTO audit_log (table_name, operation, old_values, new_values, changed_by, changed_at)
        VALUES (TG_TABLE_NAME, TG_OP, row_to_json(OLD), row_to_json(NEW), current_user, CURRENT_TIMESTAMP);
        RETURN NEW;
    ELSIF TG_OP = 'DELETE' THEN
        INSERT INTO audit_log (table_name, operation, old_values, new_values, changed_by, changed_at)
        VALUES (TG_TABLE_NAME, TG_OP, row_to_json(OLD), NULL, current_user, CURRENT_TIMESTAMP);
        RETURN OLD;
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

-- Create audit log table
CREATE TABLE audit_log (
    log_id SERIAL PRIMARY KEY,
    table_name VARCHAR(100),
    operation VARCHAR(10),
    old_values JSONB,
    new_values JSONB,
    changed_by VARCHAR(100),
    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create trigger
CREATE TRIGGER customers_audit_trigger
    AFTER INSERT OR UPDATE OR DELETE ON customers
    FOR EACH ROW EXECUTE FUNCTION audit_trigger_function();

-- Test trigger
INSERT INTO customers (name, email, city) VALUES ('Test User', 'test@example.com', 'Test City');
UPDATE customers SET city = 'Updated City' WHERE name = 'Test User';
DELETE FROM customers WHERE name = 'Test User';

-- Check audit log
SELECT * FROM audit_log ORDER BY changed_at DESC;

-- Trigger for updating timestamps
CREATE OR REPLACE FUNCTION update_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Add updated_at column
ALTER TABLE customers ADD COLUMN updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;

-- Create trigger for timestamp updates
CREATE TRIGGER customers_update_timestamp
    BEFORE UPDATE ON customers
    FOR EACH ROW EXECUTE FUNCTION update_timestamp();

-- Test timestamp trigger
UPDATE customers SET city = 'New City' WHERE customer_id = 1;
SELECT name, city, updated_at FROM customers WHERE customer_id = 1;
```

## 8.5 Event Triggers

Event triggers respond to database-level events rather than table-level events.

### Event Trigger Types:
- **DDL Events**: Data Definition Language events
- **Database Events**: Database-level events
- **Command Events**: SQL command events
- **System Events**: System-level events

### Event Trigger Events:
- **CREATE**: When objects are created
- **DROP**: When objects are dropped
- **ALTER**: When objects are modified
- **GRANT/REVOKE**: When permissions change

### Real-World Analogy:
Event triggers are like security cameras:
- **DDL Events** = Monitoring structural changes
- **Database Events** = Monitoring database operations
- **Command Events** = Monitoring specific commands
- **System Events** = Monitoring system changes

### SQL Example - Event Triggers:
```sql
-- Create event trigger function
CREATE OR REPLACE FUNCTION ddl_audit_function()
RETURNS event_trigger AS $$
DECLARE
    r RECORD;
BEGIN
    FOR r IN SELECT * FROM pg_event_trigger_ddl_commands()
    LOOP
        INSERT INTO ddl_audit_log (
            event_type,
            command_tag,
            object_type,
            object_name,
            schema_name,
            executed_by,
            executed_at
        ) VALUES (
            tg_event,
            r.command_tag,
            r.object_type,
            r.object_identity,
            r.schema_name,
            current_user,
            CURRENT_TIMESTAMP
        );
    END LOOP;
END;
$$ LANGUAGE plpgsql;

-- Create DDL audit log table
CREATE TABLE ddl_audit_log (
    log_id SERIAL PRIMARY KEY,
    event_type TEXT,
    command_tag TEXT,
    object_type TEXT,
    object_name TEXT,
    schema_name TEXT,
    executed_by VARCHAR(100),
    executed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create event trigger
CREATE EVENT TRIGGER ddl_audit_trigger
    ON ddl_command_end
    EXECUTE FUNCTION ddl_audit_function();

-- Test event trigger
CREATE TABLE test_table (id SERIAL PRIMARY KEY, name VARCHAR(100));
ALTER TABLE test_table ADD COLUMN description TEXT;
DROP TABLE test_table;

-- Check DDL audit log
SELECT * FROM ddl_audit_log ORDER BY executed_at DESC;
```

## 8.6 Custom Functions

Custom functions extend PostgreSQL's functionality with user-defined logic.

### Custom Function Types:
- **Scalar Functions**: Return single values
- **Aggregate Functions**: Custom aggregation logic
- **Window Functions**: Custom window function logic
- **Table Functions**: Return table-like results
- **C Functions**: Functions written in C

### Real-World Analogy:
Custom functions are like specialized tools:
- **Scalar Functions** = Single-purpose tools
- **Aggregate Functions** = Summary tools
- **Window Functions** = Analysis tools
- **Table Functions** = Multi-result tools
- **C Functions** = High-performance tools

### SQL Example - Custom Functions:
```sql
-- Custom aggregate function
CREATE OR REPLACE FUNCTION custom_median(NUMERIC[])
RETURNS NUMERIC AS $$
DECLARE
    sorted_array NUMERIC[];
    array_length INTEGER;
    median_value NUMERIC;
BEGIN
    -- Sort the array
    SELECT ARRAY(SELECT unnest($1) ORDER BY 1) INTO sorted_array;
    
    -- Get array length
    array_length := array_length(sorted_array, 1);
    
    -- Calculate median
    IF array_length % 2 = 0 THEN
        median_value := (sorted_array[array_length/2] + sorted_array[array_length/2 + 1]) / 2;
    ELSE
        median_value := sorted_array[(array_length + 1)/2];
    END IF;
    
    RETURN median_value;
END;
$$ LANGUAGE plpgsql;

-- Custom window function
CREATE OR REPLACE FUNCTION running_total(NUMERIC)
RETURNS NUMERIC AS $$
DECLARE
    total NUMERIC := 0;
BEGIN
    total := total + $1;
    RETURN total;
END;
$$ LANGUAGE plpgsql;

-- Custom table function
CREATE OR REPLACE FUNCTION get_customer_orders(customer_id INTEGER)
RETURNS TABLE(
    order_id INTEGER,
    order_date DATE,
    total_amount NUMERIC,
    item_count INTEGER
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        o.order_id,
        o.order_date,
        o.total_amount,
        COUNT(oi.item_id)::INTEGER as item_count
    FROM orders o
    LEFT JOIN order_items oi ON o.order_id = oi.order_id
    WHERE o.customer_id = $1
    GROUP BY o.order_id, o.order_date, o.total_amount
    ORDER BY o.order_date DESC;
END;
$$ LANGUAGE plpgsql;

-- Test custom functions
SELECT custom_median(ARRAY[1, 2, 3, 4, 5]);
SELECT custom_median(ARRAY[1, 2, 3, 4, 5, 6]);

SELECT * FROM get_customer_orders(1);
```

## 8.7 Function Overloading

Function overloading allows multiple functions with the same name but different parameters.

### Overloading Rules:
- **Parameter Types**: Different parameter types
- **Parameter Count**: Different number of parameters
- **Parameter Names**: Parameter names don't matter
- **Return Types**: Return types can be different
- **Resolution**: PostgreSQL chooses best match

### Real-World Analogy:
Function overloading is like having multiple tools with the same name:
- **Parameter Types** = Different tool sizes
- **Parameter Count** = Different tool configurations
- **Parameter Names** = Tool labels don't matter
- **Return Types** = Different tool outputs
- **Resolution** = Choosing the right tool

### SQL Example - Function Overloading:
```sql
-- Overloaded functions with different parameter types
CREATE OR REPLACE FUNCTION calculate_discount(amount NUMERIC)
RETURNS NUMERIC AS $$
BEGIN
    IF amount >= 1000 THEN
        RETURN amount * 0.1;
    ELSE
        RETURN amount * 0.05;
    END IF;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION calculate_discount(amount INTEGER)
RETURNS NUMERIC AS $$
BEGIN
    RETURN calculate_discount(amount::NUMERIC);
END;
$$ LANGUAGE plpgsql;

-- Overloaded functions with different parameter counts
CREATE OR REPLACE FUNCTION format_name(first_name VARCHAR, last_name VARCHAR)
RETURNS TEXT AS $$
BEGIN
    RETURN first_name || ' ' || last_name;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION format_name(first_name VARCHAR, middle_name VARCHAR, last_name VARCHAR)
RETURNS TEXT AS $$
BEGIN
    RETURN first_name || ' ' || middle_name || ' ' || last_name;
END;
$$ LANGUAGE plpgsql;

-- Overloaded functions with different return types
CREATE OR REPLACE FUNCTION get_customer_info(customer_id INTEGER)
RETURNS TEXT AS $$
BEGIN
    RETURN (SELECT name FROM customers WHERE customer_id = $1);
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_customer_info(customer_id INTEGER)
RETURNS TABLE(name VARCHAR, email VARCHAR) AS $$
BEGIN
    RETURN QUERY
    SELECT c.name, c.email
    FROM customers c
    WHERE c.customer_id = $1;
END;
$$ LANGUAGE plpgsql;

-- Test overloaded functions
SELECT calculate_discount(1500.00);
SELECT calculate_discount(1500);
SELECT format_name('John', 'Doe');
SELECT format_name('John', 'Michael', 'Doe');
SELECT get_customer_info(1);
```

## 8.8 Security and Permissions

PostgreSQL provides comprehensive security features for functions and procedures.

### Security Features:
- **Definer Rights**: Functions run with definer's privileges
- **Invoker Rights**: Functions run with invoker's privileges
- **SECURITY DEFINER**: Run with definer's privileges
- **SECURITY INVOKER**: Run with invoker's privileges
- **GRANT/REVOKE**: Manage function permissions

### Real-World Analogy:
Function security is like access control:
- **Definer Rights** = Using the creator's access
- **Invoker Rights** = Using the caller's access
- **SECURITY DEFINER** = Elevated privileges
- **SECURITY INVOKER** = Standard privileges
- **GRANT/REVOKE** = Permission management

### SQL Example - Security and Permissions:
```sql
-- Create function with definer rights
CREATE OR REPLACE FUNCTION get_sensitive_data()
RETURNS TABLE(customer_id INTEGER, name VARCHAR) AS $$
BEGIN
    RETURN QUERY
    SELECT c.customer_id, c.name
    FROM customers c
    WHERE c.customer_id > 0;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Create function with invoker rights
CREATE OR REPLACE FUNCTION get_public_data()
RETURNS TABLE(customer_id INTEGER, name VARCHAR) AS $$
BEGIN
    RETURN QUERY
    SELECT c.customer_id, c.name
    FROM customers c
    WHERE c.customer_id > 0;
END;
$$ LANGUAGE plpgsql SECURITY INVOKER;

-- Grant permissions
GRANT EXECUTE ON FUNCTION get_sensitive_data() TO public;
GRANT EXECUTE ON FUNCTION get_public_data() TO public;

-- Revoke permissions
REVOKE EXECUTE ON FUNCTION get_sensitive_data() FROM public;

-- Check function permissions
SELECT 
    n.nspname as schema_name,
    p.proname as function_name,
    pg_get_function_identity_arguments(p.oid) as arguments,
    p.prosecdef as security_definer,
    p.proacl as permissions
FROM pg_proc p
JOIN pg_namespace n ON p.pronamespace = n.oid
WHERE p.proname LIKE 'get_%_data'
ORDER BY n.nspname, p.proname;
```

## 8.9 Performance Considerations

Function performance can significantly impact database performance.

### Performance Factors:
- **Function Complexity**: Complex functions are slower
- **SQL Integration**: Embedded SQL affects performance
- **Parameter Passing**: Parameter types affect performance
- **Caching**: Function result caching
- **Index Usage**: Functions can prevent index usage

### Real-World Analogy:
Function performance is like tool efficiency:
- **Function Complexity** = Complex tools are slower
- **SQL Integration** = Tool integration affects speed
- **Parameter Passing** = Tool setup affects performance
- **Caching** = Tool result storage
- **Index Usage** = Tool optimization

### SQL Example - Performance Considerations:
```sql
-- Simple function (fast)
CREATE OR REPLACE FUNCTION simple_calculation(a NUMERIC, b NUMERIC)
RETURNS NUMERIC AS $$
BEGIN
    RETURN a + b;
END;
$$ LANGUAGE plpgsql;

-- Complex function (slower)
CREATE OR REPLACE FUNCTION complex_calculation(a NUMERIC, b NUMERIC)
RETURNS NUMERIC AS $$
DECLARE
    result NUMERIC := 0;
    i INTEGER;
BEGIN
    FOR i IN 1..1000 LOOP
        result := result + (a * b) / i;
    END LOOP;
    RETURN result;
END;
$$ LANGUAGE plpgsql;

-- Function with SQL (can be slow)
CREATE OR REPLACE FUNCTION get_customer_count()
RETURNS INTEGER AS $$
DECLARE
    count INTEGER;
BEGIN
    SELECT COUNT(*) INTO count FROM customers;
    RETURN count;
END;
$$ LANGUAGE plpgsql;

-- Function that prevents index usage
CREATE OR REPLACE FUNCTION get_customers_by_name_pattern(pattern TEXT)
RETURNS TABLE(customer_id INTEGER, name VARCHAR) AS $$
BEGIN
    RETURN QUERY
    SELECT c.customer_id, c.name
    FROM customers c
    WHERE c.name LIKE pattern;
END;
$$ LANGUAGE plpgsql;

-- Test performance
EXPLAIN ANALYZE SELECT simple_calculation(10, 20);
EXPLAIN ANALYZE SELECT complex_calculation(10, 20);
EXPLAIN ANALYZE SELECT get_customer_count();
EXPLAIN ANALYZE SELECT * FROM get_customers_by_name_pattern('J%');
```

## 8.10 Debugging and Testing

PostgreSQL provides tools for debugging and testing functions.

### Debugging Tools:
- **RAISE Statements**: Output debugging information
- **Exception Handling**: Catch and handle errors
- **Logging**: Function execution logging
- **Profiling**: Performance profiling
- **Testing**: Unit testing functions

### Real-World Analogy:
Function debugging is like troubleshooting:
- **RAISE Statements** = Diagnostic messages
- **Exception Handling** = Error recovery
- **Logging** = Activity records
- **Profiling** = Performance analysis
- **Testing** = Quality assurance

### SQL Example - Debugging and Testing:
```sql
-- Function with debugging
CREATE OR REPLACE FUNCTION debug_function(input_value INTEGER)
RETURNS INTEGER AS $$
DECLARE
    result INTEGER;
BEGIN
    RAISE NOTICE 'Input value: %', input_value;
    
    BEGIN
        result := input_value * 2;
        RAISE NOTICE 'Calculation result: %', result;
        
        IF result > 100 THEN
            RAISE WARNING 'Result is greater than 100: %', result;
        END IF;
        
        RETURN result;
        
    EXCEPTION
        WHEN OTHERS THEN
            RAISE EXCEPTION 'Error in debug_function: %', SQLERRM;
    END;
END;
$$ LANGUAGE plpgsql;

-- Test function
SELECT debug_function(50);

-- Function with comprehensive error handling
CREATE OR REPLACE FUNCTION safe_division(a NUMERIC, b NUMERIC)
RETURNS NUMERIC AS $$
DECLARE
    result NUMERIC;
BEGIN
    -- Input validation
    IF a IS NULL OR b IS NULL THEN
        RAISE EXCEPTION 'Input values cannot be NULL';
    END IF;
    
    IF b = 0 THEN
        RAISE EXCEPTION 'Division by zero is not allowed';
    END IF;
    
    -- Perform calculation
    result := a / b;
    
    -- Result validation
    IF result < 0 THEN
        RAISE WARNING 'Result is negative: %', result;
    END IF;
    
    RETURN result;
    
EXCEPTION
    WHEN division_by_zero THEN
        RAISE EXCEPTION 'Division by zero error';
    WHEN numeric_value_out_of_range THEN
        RAISE EXCEPTION 'Numeric value out of range';
    WHEN OTHERS THEN
        RAISE EXCEPTION 'Unexpected error: %', SQLERRM;
END;
$$ LANGUAGE plpgsql;

-- Test error handling
SELECT safe_division(10, 2);
SELECT safe_division(10, 0);
SELECT safe_division(NULL, 5);

-- Function testing
CREATE OR REPLACE FUNCTION test_functions()
RETURNS TABLE(test_name TEXT, result TEXT) AS $$
BEGIN
    -- Test 1: Normal case
    BEGIN
        PERFORM safe_division(10, 2);
        RETURN QUERY SELECT 'Normal division'::TEXT, 'PASS'::TEXT;
    EXCEPTION
        WHEN OTHERS THEN
            RETURN QUERY SELECT 'Normal division'::TEXT, 'FAIL'::TEXT;
    END;
    
    -- Test 2: Division by zero
    BEGIN
        PERFORM safe_division(10, 0);
        RETURN QUERY SELECT 'Division by zero'::TEXT, 'FAIL'::TEXT;
    EXCEPTION
        WHEN OTHERS THEN
            RETURN QUERY SELECT 'Division by zero'::TEXT, 'PASS'::TEXT;
    END;
    
    -- Test 3: NULL input
    BEGIN
        PERFORM safe_division(NULL, 5);
        RETURN QUERY SELECT 'NULL input'::TEXT, 'FAIL'::TEXT;
    EXCEPTION
        WHEN OTHERS THEN
            RETURN QUERY SELECT 'NULL input'::TEXT, 'PASS'::TEXT;
    END;
END;
$$ LANGUAGE plpgsql;

-- Run tests
SELECT * FROM test_functions();
```