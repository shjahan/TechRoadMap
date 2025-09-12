# Section 16 – Extensions and Customization

## 16.1 PostgreSQL Extensions

PostgreSQL extensions are add-on modules that provide additional functionality beyond the core database features. They allow you to extend PostgreSQL's capabilities with specialized data types, functions, operators, and more.

### Key Concepts:
- **Extension System**: Built-in mechanism for managing add-on modules
- **Extension Catalog**: Central registry of available extensions
- **Dependencies**: Extensions can depend on other extensions
- **Versioning**: Extensions have version numbers for compatibility

### Real-World Analogy:
PostgreSQL extensions are like apps on your smartphone:
- **Core OS** = PostgreSQL core functionality
- **App Store** = Extension catalog (pg_available_extensions)
- **Installed Apps** = Active extensions (pg_extension)
- **App Updates** = Extension version upgrades

### Example:
```sql
-- List available extensions
SELECT * FROM pg_available_extensions 
WHERE name LIKE '%postgis%';

-- Install an extension
CREATE EXTENSION IF NOT EXISTS postgis;

-- List installed extensions
SELECT * FROM pg_extension;

-- Check extension details
\dx postgis
```

## 16.2 Popular Extensions

Popular PostgreSQL extensions provide specialized functionality for various use cases, from geographic data processing to advanced analytics.

### Geographic Extensions:
- **PostGIS**: Geographic objects and spatial operations
- **PostGIS Topology**: Topological data structures
- **PostGIS Raster**: Raster data support

### Analytics Extensions:
- **pg_stat_statements**: Query performance statistics
- **pg_stat_kcache**: Kernel-level statistics
- **pg_stat_bgwriter**: Background writer statistics

### Data Type Extensions:
- **hstore**: Key-value storage
- **jsonb**: Binary JSON storage
- **uuid-ossp**: UUID generation functions

### Example:
```sql
-- Install PostGIS for geographic data
CREATE EXTENSION postgis;

-- Create a table with geographic data
CREATE TABLE locations (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    geom GEOMETRY(POINT, 4326)
);

-- Insert geographic data
INSERT INTO locations (name, geom) VALUES 
('New York', ST_GeomFromText('POINT(-74.0060 40.7128)', 4326)),
('London', ST_GeomFromText('POINT(-0.1276 51.5074)', 4326));

-- Calculate distance between points
SELECT 
    a.name as city1,
    b.name as city2,
    ST_Distance(a.geom, b.geom) as distance_km
FROM locations a, locations b 
WHERE a.id < b.id;
```

## 16.3 Custom Functions and Procedures

Custom functions and procedures allow you to extend PostgreSQL with application-specific logic, improving code reusability and performance.

### Function Types:
- **SQL Functions**: Written in SQL language
- **PL/pgSQL Functions**: Written in PL/pgSQL procedural language
- **C Functions**: Written in C language for maximum performance
- **Other Languages**: Python, Perl, Tcl, etc.

### Real-World Analogy:
Custom functions are like specialized tools in a workshop:
- **Basic Tools** = Built-in functions
- **Custom Tools** = Your own functions
- **Tool Manual** = Function documentation
- **Tool Storage** = Function catalog

### Example:
```sql
-- Create a simple SQL function
CREATE OR REPLACE FUNCTION calculate_age(birth_date DATE)
RETURNS INTEGER AS $$
    SELECT EXTRACT(YEAR FROM AGE(birth_date))::INTEGER;
$$ LANGUAGE SQL;

-- Create a PL/pgSQL function with complex logic
CREATE OR REPLACE FUNCTION get_employee_info(emp_id INTEGER)
RETURNS TABLE(
    employee_name VARCHAR,
    department_name VARCHAR,
    salary_level VARCHAR
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        e.first_name || ' ' || e.last_name,
        d.department_name,
        CASE 
            WHEN e.salary > 100000 THEN 'High'
            WHEN e.salary > 50000 THEN 'Medium'
            ELSE 'Low'
        END
    FROM employees e
    JOIN departments d ON e.department_id = d.id
    WHERE e.id = emp_id;
END;
$$ LANGUAGE plpgsql;

-- Use the functions
SELECT calculate_age('1990-01-01'::DATE);
SELECT * FROM get_employee_info(1);
```

## 16.4 Custom Data Types

Custom data types allow you to define domain-specific data structures that can be used throughout your database schema.

### Type Categories:
- **Base Types**: Fundamental data types (like C structures)
- **Composite Types**: User-defined record types
- **Domain Types**: Constrained versions of existing types
- **Enum Types**: User-defined enumeration types

### Real-World Analogy:
Custom data types are like creating specialized containers:
- **Standard Boxes** = Built-in data types
- **Custom Boxes** = Your own data types
- **Box Labels** = Type names
- **Box Contents** = Type values

### Example:
```sql
-- Create an enum type
CREATE TYPE order_status AS ENUM (
    'pending', 'processing', 'shipped', 'delivered', 'cancelled'
);

-- Create a composite type
CREATE TYPE address AS (
    street VARCHAR(100),
    city VARCHAR(50),
    state VARCHAR(20),
    zip_code VARCHAR(10)
);

-- Create a domain type
CREATE DOMAIN email_address AS VARCHAR(255)
CHECK (VALUE ~ '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$');

-- Use custom types in tables
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    customer_email email_address,
    shipping_address address,
    status order_status DEFAULT 'pending'
);

-- Insert data using custom types
INSERT INTO orders (customer_email, shipping_address, status) VALUES 
(
    'john@example.com',
    ('123 Main St', 'New York', 'NY', '10001')::address,
    'pending'
);
```

## 16.5 Custom Operators

Custom operators allow you to define new operations for your data types, making queries more readable and expressive.

### Operator Categories:
- **Unary Operators**: Operate on single operand (e.g., !, ~)
- **Binary Operators**: Operate on two operands (e.g., +, -, *)
- **Comparison Operators**: Return boolean results (e.g., =, <, >)
- **Logical Operators**: Boolean operations (e.g., AND, OR)

### Real-World Analogy:
Custom operators are like creating new gestures for communication:
- **Standard Gestures** = Built-in operators
- **Custom Gestures** = Your own operators
- **Gesture Meaning** = Operator functionality
- **Gesture Rules** = Operator precedence

### Example:
```sql
-- Create a custom data type for complex numbers
CREATE TYPE complex AS (
    real_part DOUBLE PRECISION,
    imag_part DOUBLE PRECISION
);

-- Create custom operators for complex numbers
CREATE OR REPLACE FUNCTION complex_add(a complex, b complex)
RETURNS complex AS $$
BEGIN
    RETURN (a.real_part + b.real_part, a.imag_part + b.imag_part);
END;
$$ LANGUAGE plpgsql;

-- Define the + operator for complex numbers
CREATE OPERATOR + (
    LEFTARG = complex,
    RIGHTARG = complex,
    PROCEDURE = complex_add
);

-- Create comparison operator
CREATE OR REPLACE FUNCTION complex_magnitude(a complex)
RETURNS DOUBLE PRECISION AS $$
BEGIN
    RETURN SQRT(a.real_part^2 + a.imag_part^2);
END;
$$ LANGUAGE plpgsql;

CREATE OPERATOR > (
    LEFTARG = complex,
    RIGHTARG = complex,
    PROCEDURE = complex_magnitude
);

-- Use custom operators
SELECT (3, 4)::complex + (1, 2)::complex;
SELECT (3, 4)::complex > (1, 2)::complex;
```

## 16.6 Custom Aggregates

Custom aggregates allow you to define new aggregation functions that can be used with GROUP BY clauses and window functions.

### Aggregate Components:
- **State Type**: Data type for intermediate results
- **State Function**: Function to update state with new values
- **Final Function**: Function to compute final result from state
- **Initial Condition**: Initial value for the state

### Real-World Analogy:
Custom aggregates are like creating new ways to summarize data:
- **Standard Summaries** = Built-in aggregates (SUM, AVG, COUNT)
- **Custom Summaries** = Your own aggregates
- **Summary Process** = State and final functions
- **Summary Result** = Final aggregate value

### Example:
```sql
-- Create a custom aggregate for geometric mean
CREATE OR REPLACE FUNCTION geometric_mean_accum(state DOUBLE PRECISION[], value DOUBLE PRECISION)
RETURNS DOUBLE PRECISION[] AS $$
BEGIN
    state[1] := state[1] + LN(value);  -- Sum of logarithms
    state[2] := state[2] + 1;          -- Count
    RETURN state;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION geometric_mean_final(state DOUBLE PRECISION[])
RETURNS DOUBLE PRECISION AS $$
BEGIN
    IF state[2] = 0 THEN
        RETURN NULL;
    END IF;
    RETURN EXP(state[1] / state[2]);  -- Geometric mean
END;
$$ LANGUAGE plpgsql;

-- Create the aggregate
CREATE AGGREGATE geometric_mean(DOUBLE PRECISION) (
    SFUNC = geometric_mean_accum,
    STYPE = DOUBLE PRECISION[],
    FINALFUNC = geometric_mean_final,
    INITCOND = '{0,0}'
);

-- Use the custom aggregate
CREATE TABLE test_values (value DOUBLE PRECISION);
INSERT INTO test_values VALUES (2), (8), (32), (128);

SELECT 
    AVG(value) as arithmetic_mean,
    geometric_mean(value) as geometric_mean
FROM test_values;
```

## 16.7 Extension Management

Extension management involves installing, updating, and removing extensions while maintaining database integrity and managing dependencies.

### Management Operations:
- **Installation**: Adding new extensions to the database
- **Updates**: Upgrading extensions to newer versions
- **Removal**: Uninstalling extensions (if no dependencies)
- **Dependency Resolution**: Managing extension dependencies

### Real-World Analogy:
Extension management is like managing software on your computer:
- **Installation** = Installing new software
- **Updates** = Updating existing software
- **Removal** = Uninstalling software
- **Dependencies** = Required libraries and components

### Example:
```sql
-- Check extension status
SELECT 
    extname as extension_name,
    extversion as version,
    extrelocatable as relocatable
FROM pg_extension;

-- Update an extension
ALTER EXTENSION postgis UPDATE TO '3.1.0';

-- Check for available updates
SELECT 
    name,
    default_version,
    installed_version,
    comment
FROM pg_available_extensions 
WHERE installed_version IS NOT NULL
AND default_version != installed_version;

-- Remove an extension (if no dependencies)
DROP EXTENSION IF EXISTS hstore;

-- Check extension dependencies
SELECT 
    e.extname as extension,
    d.extname as depends_on
FROM pg_extension e
JOIN pg_depend dep ON e.oid = dep.objid
JOIN pg_extension d ON dep.refobjid = d.oid
WHERE dep.deptype = 'e';
```

## 16.8 Performance Considerations

When using extensions and custom code, performance considerations are crucial for maintaining optimal database performance.

### Performance Factors:
- **Function Overhead**: Cost of function calls
- **Type Conversion**: Automatic type conversions
- **Index Usage**: Custom operators and index compatibility
- **Memory Usage**: Extension memory requirements

### Real-World Analogy:
Performance considerations are like optimizing a production line:
- **Function Overhead** = Setup time for each operation
- **Type Conversion** = Converting materials between stations
- **Index Usage** = Using efficient lookup systems
- **Memory Usage** = Storage space for tools and materials

### Example:
```sql
-- Create an optimized function with proper cost estimates
CREATE OR REPLACE FUNCTION fast_calculation(input_value INTEGER)
RETURNS INTEGER AS $$
BEGIN
    RETURN input_value * 2 + 1;
END;
$$ LANGUAGE plpgsql
COST 1  -- Low cost for simple calculations
IMMUTABLE  -- Function always returns same result for same input
PARALLEL SAFE;  -- Safe for parallel execution

-- Create a function with higher cost for complex operations
CREATE OR REPLACE FUNCTION complex_calculation(input_value INTEGER)
RETURNS INTEGER AS $$
DECLARE
    result INTEGER := 0;
    i INTEGER;
BEGIN
    FOR i IN 1..input_value LOOP
        result := result + i * i;
    END LOOP;
    RETURN result;
END;
$$ LANGUAGE plpgsql
COST 100  -- Higher cost for complex operations
STABLE;  -- Function returns same result within a transaction

-- Use functions in queries
EXPLAIN (ANALYZE, BUFFERS) 
SELECT fast_calculation(id) 
FROM generate_series(1, 1000) as id;
```

## 16.9 Security Considerations

Security considerations for extensions and custom code involve ensuring that custom functionality doesn't introduce vulnerabilities.

### Security Aspects:
- **Privilege Escalation**: Preventing unauthorized access
- **SQL Injection**: Protecting against malicious input
- **Code Execution**: Controlling execution context
- **Data Access**: Limiting data exposure

### Real-World Analogy:
Security considerations are like securing a building:
- **Privilege Escalation** = Unauthorized access to restricted areas
- **SQL Injection** = Forced entry through weak points
- **Code Execution** = Controlling who can operate equipment
- **Data Access** = Limiting access to sensitive information

### Example:
```sql
-- Create a secure function with proper permissions
CREATE OR REPLACE FUNCTION get_user_data(user_id INTEGER)
RETURNS TABLE(
    username VARCHAR,
    email VARCHAR,
    created_at TIMESTAMP
) AS $$
BEGIN
    -- Check if current user can access this data
    IF NOT (current_user = 'admin' OR current_user = 'data_reader') THEN
        RAISE EXCEPTION 'Insufficient privileges';
    END IF;
    
    -- Return only safe data
    RETURN QUERY
    SELECT 
        u.username,
        CASE 
            WHEN current_user = 'admin' THEN u.email
            ELSE '***@***.***'
        END,
        u.created_at
    FROM users u
    WHERE u.id = user_id;
END;
$$ LANGUAGE plpgsql
SECURITY DEFINER  -- Run with definer's privileges
SET search_path = public;  -- Limit search path

-- Grant appropriate permissions
GRANT EXECUTE ON FUNCTION get_user_data(INTEGER) TO data_reader;
GRANT EXECUTE ON FUNCTION get_user_data(INTEGER) TO admin;
```

## 16.10 Best Practices

Best practices for extensions and customization ensure maintainable, secure, and performant custom functionality.

### Key Practices:
- **Documentation**: Document all custom functions and types
- **Testing**: Test custom code thoroughly
- **Version Control**: Track changes to custom code
- **Performance Monitoring**: Monitor custom code performance
- **Security Review**: Regular security audits

### Real-World Analogy:
Best practices are like maintaining a professional workshop:
- **Documentation** = Keeping manuals and instructions
- **Testing** = Quality control and testing procedures
- **Version Control** = Tracking tool and equipment changes
- **Performance Monitoring** = Regular efficiency checks
- **Security Review** = Regular safety inspections

### Example:
```sql
-- Create a well-documented function
/**
 * Calculate the distance between two geographic points
 * @param lat1 Latitude of first point
 * @param lon1 Longitude of first point  
 * @param lat2 Latitude of second point
 * @param lon2 Longitude of second point
 * @return Distance in kilometers
 */
CREATE OR REPLACE FUNCTION calculate_distance(
    lat1 DOUBLE PRECISION,
    lon1 DOUBLE PRECISION,
    lat2 DOUBLE PRECISION,
    lon2 DOUBLE PRECISION
)
RETURNS DOUBLE PRECISION AS $$
DECLARE
    earth_radius DOUBLE PRECISION := 6371.0;  -- Earth radius in km
    dlat DOUBLE PRECISION;
    dlon DOUBLE PRECISION;
    a DOUBLE PRECISION;
    c DOUBLE PRECISION;
BEGIN
    -- Input validation
    IF lat1 < -90 OR lat1 > 90 OR lat2 < -90 OR lat2 > 90 THEN
        RAISE EXCEPTION 'Invalid latitude: must be between -90 and 90';
    END IF;
    
    IF lon1 < -180 OR lon1 > 180 OR lon2 < -180 OR lon2 > 180 THEN
        RAISE EXCEPTION 'Invalid longitude: must be between -180 and 180';
    END IF;
    
    -- Convert to radians
    dlat := radians(lat2 - lat1);
    dlon := radians(lon2 - lon1);
    
    -- Haversine formula
    a := sin(dlat/2)^2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)^2;
    c := 2 * asin(sqrt(a));
    
    RETURN earth_radius * c;
END;
$$ LANGUAGE plpgsql
IMMUTABLE
PARALLEL SAFE
COST 100;

-- Create a test for the function
CREATE OR REPLACE FUNCTION test_calculate_distance()
RETURNS BOOLEAN AS $$
DECLARE
    result DOUBLE PRECISION;
    expected DOUBLE PRECISION := 5570.0;  -- Approximate distance NY to London
    tolerance DOUBLE PRECISION := 100.0;  -- 100km tolerance
BEGIN
    -- Test with known coordinates (NY to London)
    result := calculate_distance(40.7128, -74.0060, 51.5074, -0.1276);
    
    -- Check if result is within tolerance
    IF ABS(result - expected) <= tolerance THEN
        RETURN TRUE;
    ELSE
        RAISE NOTICE 'Test failed: expected ~%, got %', expected, result;
        RETURN FALSE;
    END IF;
END;
$$ LANGUAGE plpgsql;

-- Run the test
SELECT test_calculate_distance();
```