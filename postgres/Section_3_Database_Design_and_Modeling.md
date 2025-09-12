# Section 3 – Database Design and Modeling

## 3.1 Database Schema Design

Database schema design is the process of creating a logical structure for organizing data in a database, defining tables, relationships, and constraints.

### Schema Design Principles:
- **Normalization**: Eliminate data redundancy and dependency
- **Denormalization**: Strategic redundancy for performance
- **Consistency**: Uniform naming conventions and data types
- **Scalability**: Design for future growth and changes
- **Performance**: Optimize for common query patterns

### Design Process:
1. **Requirements Analysis**: Understand business needs
2. **Conceptual Design**: Create entity-relationship diagrams
3. **Logical Design**: Define tables, columns, and relationships
4. **Physical Design**: Optimize for specific database system
5. **Implementation**: Create actual database objects

### Real-World Analogy:
Database schema design is like designing a building's floor plan:
- **Normalization** = Efficient use of space without duplication
- **Denormalization** = Strategic duplication for convenience
- **Consistency** = Uniform architectural style
- **Scalability** = Ability to add floors or wings
- **Performance** = Easy navigation and access

### SQL Example - Schema Design:
```sql
-- Create database schema
CREATE SCHEMA university;

-- Set search path
SET search_path TO university, public;

-- Create tables with proper relationships
CREATE TABLE departments (
    dept_id SERIAL PRIMARY KEY,
    dept_name VARCHAR(100) NOT NULL UNIQUE,
    budget NUMERIC(12,2),
    established_date DATE DEFAULT CURRENT_DATE
);

CREATE TABLE professors (
    prof_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE,
    dept_id INTEGER REFERENCES departments(dept_id),
    hire_date DATE DEFAULT CURRENT_DATE,
    salary NUMERIC(10,2)
);

CREATE TABLE students (
    student_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE,
    enrollment_date DATE DEFAULT CURRENT_DATE,
    gpa NUMERIC(3,2) CHECK (gpa >= 0.0 AND gpa <= 4.0)
);

-- Create junction table for many-to-many relationship
CREATE TABLE enrollments (
    enrollment_id SERIAL PRIMARY KEY,
    student_id INTEGER REFERENCES students(student_id),
    course_id INTEGER REFERENCES courses(course_id),
    semester VARCHAR(20),
    grade CHAR(1) CHECK (grade IN ('A', 'B', 'C', 'D', 'F')),
    enrollment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(student_id, course_id, semester)
);
```

## 3.2 Table Design and Relationships

Table design involves creating tables that represent entities and their attributes, with proper relationships between them.

### Table Design Elements:
- **Primary Keys**: Unique identifiers for each row
- **Foreign Keys**: References to other tables
- **Columns**: Attributes of the entity
- **Data Types**: Appropriate types for each column
- **Constraints**: Rules that data must follow

### Relationship Types:
- **One-to-One**: Each record in one table relates to one record in another
- **One-to-Many**: One record relates to many records in another table
- **Many-to-Many**: Many records relate to many records in another table

### Real-World Analogy:
Table design is like organizing a filing system:
- **Primary Keys** = Unique file numbers
- **Foreign Keys** = Cross-references to other files
- **Columns** = Information fields on each file
- **Data Types** = Different types of information (text, numbers, dates)
- **Constraints** = Filing rules and requirements

### SQL Example - Table Relationships:
```sql
-- Create courses table
CREATE TABLE courses (
    course_id SERIAL PRIMARY KEY,
    course_code VARCHAR(10) NOT NULL UNIQUE,
    course_name VARCHAR(100) NOT NULL,
    credits INTEGER CHECK (credits > 0 AND credits <= 6),
    dept_id INTEGER REFERENCES departments(dept_id),
    prof_id INTEGER REFERENCES professors(prof_id)
);

-- Create one-to-many relationship (Department -> Professors)
-- Each department can have many professors
-- Each professor belongs to one department

-- Create many-to-many relationship (Students <-> Courses)
-- Each student can enroll in many courses
-- Each course can have many students
-- Junction table: enrollments

-- Add constraints and indexes
ALTER TABLE professors 
ADD CONSTRAINT fk_prof_dept 
FOREIGN KEY (dept_id) REFERENCES departments(dept_id);

ALTER TABLE courses 
ADD CONSTRAINT fk_course_dept 
FOREIGN KEY (dept_id) REFERENCES departments(dept_id);

ALTER TABLE courses 
ADD CONSTRAINT fk_course_prof 
FOREIGN KEY (prof_id) REFERENCES professors(prof_id);

-- Create indexes for performance
CREATE INDEX idx_professors_dept ON professors(dept_id);
CREATE INDEX idx_courses_dept ON courses(dept_id);
CREATE INDEX idx_enrollments_student ON enrollments(student_id);
CREATE INDEX idx_enrollments_course ON enrollments(course_id);
```

## 3.3 Primary Keys and Constraints

Primary keys uniquely identify each row in a table, while constraints ensure data integrity and enforce business rules.

### Primary Key Types:
- **Natural Keys**: Business-meaningful identifiers
- **Surrogate Keys**: System-generated identifiers (SERIAL, UUID)
- **Composite Keys**: Multiple columns forming the key

### Constraint Types:
- **NOT NULL**: Column cannot be empty
- **UNIQUE**: Column values must be unique
- **CHECK**: Column values must meet conditions
- **DEFAULT**: Default value when not specified
- **FOREIGN KEY**: References to other tables

### Real-World Analogy:
Primary keys and constraints are like identification systems:
- **Primary Keys** = Social Security Numbers (unique identifiers)
- **NOT NULL** = Required fields on forms
- **UNIQUE** = One-of-a-kind items
- **CHECK** = Validation rules
- **DEFAULT** = Pre-filled form fields
- **FOREIGN KEY** = References to other documents

### SQL Example - Primary Keys and Constraints:
```sql
-- Create table with various constraints
CREATE TABLE employees (
    emp_id SERIAL PRIMARY KEY,  -- Surrogate key
    employee_number VARCHAR(10) UNIQUE NOT NULL,  -- Natural key
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE,
    phone VARCHAR(15),
    hire_date DATE NOT NULL DEFAULT CURRENT_DATE,
    salary NUMERIC(10,2) CHECK (salary > 0),
    department_id INTEGER,
    manager_id INTEGER,
    status VARCHAR(20) DEFAULT 'active' CHECK (status IN ('active', 'inactive', 'terminated')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Add foreign key constraints
ALTER TABLE employees 
ADD CONSTRAINT fk_emp_dept 
FOREIGN KEY (department_id) REFERENCES departments(dept_id);

ALTER TABLE employees 
ADD CONSTRAINT fk_emp_manager 
FOREIGN KEY (manager_id) REFERENCES employees(emp_id);

-- Create composite unique constraint
CREATE UNIQUE INDEX idx_emp_name_email 
ON employees(first_name, last_name, email);

-- Add check constraint for email format
ALTER TABLE employees 
ADD CONSTRAINT chk_email_format 
CHECK (email ~ '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$');

-- Insert sample data
INSERT INTO employees (employee_number, first_name, last_name, email, salary, department_id)
VALUES 
    ('EMP001', 'John', 'Doe', 'john.doe@company.com', 75000.00, 1),
    ('EMP002', 'Jane', 'Smith', 'jane.smith@company.com', 80000.00, 1),
    ('EMP003', 'Bob', 'Johnson', 'bob.johnson@company.com', 70000.00, 2);
```

## 3.4 Foreign Keys and Referential Integrity

Foreign keys establish relationships between tables and ensure referential integrity by maintaining consistency across related tables.

### Foreign Key Concepts:
- **Referential Integrity**: Ensures foreign key values exist in referenced table
- **Cascade Operations**: Automatic updates/deletes when referenced data changes
- **Deferrable Constraints**: Constraints that can be deferred until transaction end
- **Self-Referencing**: Foreign key pointing to same table

### Cascade Options:
- **CASCADE**: Propagate changes to dependent rows
- **SET NULL**: Set foreign key to NULL when referenced row is deleted
- **SET DEFAULT**: Set foreign key to default value
- **RESTRICT**: Prevent deletion if dependent rows exist
- **NO ACTION**: Similar to RESTRICT but checked at end of statement

### Real-World Analogy:
Foreign keys are like cross-references in a library system:
- **Referential Integrity** = Ensuring all book references point to existing books
- **Cascade Operations** = When a book is removed, update all references
- **Deferrable Constraints** = Allow temporary inconsistencies during updates
- **Self-Referencing** = Books referencing other books in the same catalog

### SQL Example - Foreign Key Management:
```sql
-- Create tables with foreign key relationships
CREATE TABLE categories (
    category_id SERIAL PRIMARY KEY,
    category_name VARCHAR(100) NOT NULL UNIQUE,
    parent_category_id INTEGER REFERENCES categories(category_id)
);

CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    category_id INTEGER NOT NULL,
    supplier_id INTEGER,
    price NUMERIC(10,2) CHECK (price > 0),
    stock_quantity INTEGER DEFAULT 0 CHECK (stock_quantity >= 0)
);

CREATE TABLE suppliers (
    supplier_id SERIAL PRIMARY KEY,
    supplier_name VARCHAR(100) NOT NULL,
    contact_email VARCHAR(100),
    status VARCHAR(20) DEFAULT 'active'
);

-- Add foreign key constraints with different cascade options
ALTER TABLE products 
ADD CONSTRAINT fk_product_category 
FOREIGN KEY (category_id) REFERENCES categories(category_id)
ON DELETE RESTRICT ON UPDATE CASCADE;

ALTER TABLE products 
ADD CONSTRAINT fk_product_supplier 
FOREIGN KEY (supplier_id) REFERENCES suppliers(supplier_id)
ON DELETE SET NULL ON UPDATE CASCADE;

-- Create self-referencing foreign key for categories
ALTER TABLE categories 
ADD CONSTRAINT fk_category_parent 
FOREIGN KEY (parent_category_id) REFERENCES categories(category_id)
ON DELETE SET NULL ON UPDATE CASCADE;

-- Insert sample data
INSERT INTO categories (category_name, parent_category_id) VALUES 
    ('Electronics', NULL),
    ('Computers', 1),
    ('Laptops', 2),
    ('Desktops', 2),
    ('Accessories', 1);

INSERT INTO suppliers (supplier_name, contact_email) VALUES 
    ('TechCorp', 'contact@techcorp.com'),
    ('GadgetWorld', 'info@gadgetworld.com');

INSERT INTO products (product_name, category_id, supplier_id, price, stock_quantity) VALUES 
    ('MacBook Pro', 3, 1, 1999.99, 10),
    ('Dell XPS', 3, 1, 1299.99, 15),
    ('Gaming Desktop', 4, 2, 1499.99, 5);
```

## 3.5 Check Constraints

Check constraints enforce business rules by validating data against specified conditions using boolean expressions.

### Check Constraint Features:
- **Boolean Expressions**: Use any valid SQL boolean expression
- **Column-Level**: Applied to individual columns
- **Table-Level**: Applied to multiple columns
- **Named Constraints**: Constraints with explicit names
- **Deferrable**: Can be deferred until transaction end

### Common Check Patterns:
- **Range Validation**: Numeric values within specific ranges
- **Format Validation**: String patterns using regular expressions
- **Enumeration**: Values from a specific set
- **Cross-Column**: Relationships between multiple columns

### Real-World Analogy:
Check constraints are like validation rules on forms:
- **Range Validation** = Age must be between 18 and 65
- **Format Validation** = Phone number must follow specific pattern
- **Enumeration** = Status must be one of predefined values
- **Cross-Column** = End date must be after start date

### SQL Example - Check Constraints:
```sql
-- Create table with various check constraints
CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    order_date DATE NOT NULL DEFAULT CURRENT_DATE,
    ship_date DATE,
    total_amount NUMERIC(10,2) NOT NULL CHECK (total_amount > 0),
    tax_rate NUMERIC(5,4) CHECK (tax_rate >= 0 AND tax_rate <= 1),
    status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'processing', 'shipped', 'delivered', 'cancelled')),
    priority VARCHAR(10) DEFAULT 'normal' CHECK (priority IN ('low', 'normal', 'high', 'urgent')),
    discount_percent NUMERIC(5,2) CHECK (discount_percent >= 0 AND discount_percent <= 100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Add table-level check constraint
ALTER TABLE orders 
ADD CONSTRAINT chk_ship_date_after_order 
CHECK (ship_date IS NULL OR ship_date >= order_date);

-- Add check constraint for business logic
ALTER TABLE orders 
ADD CONSTRAINT chk_discount_high_priority 
CHECK (NOT (priority = 'high' AND discount_percent > 50));

-- Create table with complex check constraints
CREATE TABLE employees (
    emp_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE CHECK (email ~ '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'),
    phone VARCHAR(15) CHECK (phone ~ '^\+?[1-9]\d{1,14}$'),
    hire_date DATE NOT NULL DEFAULT CURRENT_DATE,
    birth_date DATE CHECK (birth_date < CURRENT_DATE - INTERVAL '16 years'),
    salary NUMERIC(10,2) CHECK (salary > 0),
    commission_pct NUMERIC(5,2) CHECK (commission_pct >= 0 AND commission_pct <= 100),
    manager_id INTEGER,
    department_id INTEGER
);

-- Add cross-column check constraint
ALTER TABLE employees 
ADD CONSTRAINT chk_commission_salary 
CHECK (commission_pct = 0 OR salary >= 30000);

-- Insert sample data
INSERT INTO orders (customer_id, total_amount, tax_rate, status, priority, discount_percent) VALUES 
    (1, 150.00, 0.08, 'pending', 'normal', 10.00),
    (2, 299.99, 0.10, 'processing', 'high', 5.00),
    (3, 75.50, 0.06, 'shipped', 'low', 0.00);
```

## 3.6 Unique Constraints

Unique constraints ensure that values in specified columns are unique across all rows in a table.

### Unique Constraint Types:
- **Column-Level**: Single column uniqueness
- **Table-Level**: Multiple column uniqueness
- **Partial**: Uniqueness with WHERE condition
- **Deferrable**: Can be deferred until transaction end

### Unique vs Primary Key:
- **Primary Key**: Cannot be NULL, only one per table
- **Unique**: Can be NULL, multiple per table
- **Both**: Create indexes for performance

### Real-World Analogy:
Unique constraints are like unique identifiers in real life:
- **Column-Level** = Unique email addresses
- **Table-Level** = Unique combination of first name and last name
- **Partial** = Unique active email addresses
- **Deferrable** = Allow temporary duplicates during updates

### SQL Example - Unique Constraints:
```sql
-- Create table with unique constraints
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    phone VARCHAR(15) UNIQUE,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    status VARCHAR(20) DEFAULT 'active' CHECK (status IN ('active', 'inactive', 'suspended')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create composite unique constraint
CREATE UNIQUE INDEX idx_user_name_unique 
ON users(first_name, last_name) 
WHERE status = 'active';

-- Create table with deferrable unique constraint
CREATE TABLE reservations (
    reservation_id SERIAL PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    room_number VARCHAR(10) NOT NULL,
    check_in_date DATE NOT NULL,
    check_out_date DATE NOT NULL,
    status VARCHAR(20) DEFAULT 'confirmed' CHECK (status IN ('confirmed', 'cancelled', 'completed')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Add deferrable unique constraint
ALTER TABLE reservations 
ADD CONSTRAINT uk_reservation_room_date 
UNIQUE (room_number, check_in_date, check_out_date) 
DEFERRABLE INITIALLY DEFERRED;

-- Create partial unique index
CREATE UNIQUE INDEX idx_active_reservations 
ON reservations(room_number, check_in_date) 
WHERE status = 'confirmed';

-- Insert sample data
INSERT INTO users (username, email, phone, first_name, last_name) VALUES 
    ('jdoe', 'john.doe@example.com', '+1234567890', 'John', 'Doe'),
    ('asmith', 'alice.smith@example.com', '+1987654321', 'Alice', 'Smith'),
    ('bwilson', 'bob.wilson@example.com', NULL, 'Bob', 'Wilson');

-- Test unique constraints
INSERT INTO reservations (customer_id, room_number, check_in_date, check_out_date) VALUES 
    (1, '101', '2024-06-01', '2024-06-05'),
    (2, '102', '2024-06-01', '2024-06-03'),
    (3, '101', '2024-06-06', '2024-06-10');
```

## 3.7 Not Null Constraints

NOT NULL constraints ensure that columns cannot contain NULL values, making them mandatory for data entry.

### NOT NULL Features:
- **Column-Level**: Applied to individual columns
- **Default Values**: Can be combined with DEFAULT constraints
- **Performance**: Slightly better performance than nullable columns
- **Indexing**: NOT NULL columns can be indexed more efficiently

### When to Use NOT NULL:
- **Required Fields**: Essential business data
- **Primary Keys**: Always required
- **Foreign Keys**: Usually required
- **Business Logic**: Fields that must have values

### Real-World Analogy:
NOT NULL constraints are like required fields on forms:
- **Required Fields** = Must be filled out
- **Default Values** = Pre-filled fields
- **Performance** = Faster processing of complete forms
- **Indexing** = Easier to find complete records

### SQL Example - NOT NULL Constraints:
```sql
-- Create table with NOT NULL constraints
CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    phone VARCHAR(15) NOT NULL,
    date_of_birth DATE NOT NULL,
    registration_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP,
    status VARCHAR(20) NOT NULL DEFAULT 'active' CHECK (status IN ('active', 'inactive', 'suspended'))
);

-- Create table with conditional NOT NULL
CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    order_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ship_date TIMESTAMP,
    delivery_date TIMESTAMP,
    status VARCHAR(20) NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'processing', 'shipped', 'delivered', 'cancelled')),
    total_amount NUMERIC(10,2) NOT NULL CHECK (total_amount > 0),
    notes TEXT
);

-- Add NOT NULL constraint to existing column
ALTER TABLE orders 
ALTER COLUMN ship_date SET NOT NULL;

-- Add NOT NULL constraint with default value
ALTER TABLE orders 
ALTER COLUMN notes SET DEFAULT 'No notes',
ALTER COLUMN notes SET NOT NULL;

-- Insert sample data
INSERT INTO customers (first_name, last_name, email, phone, date_of_birth) VALUES 
    ('John', 'Doe', 'john.doe@example.com', '+1234567890', '1990-05-15'),
    ('Alice', 'Smith', 'alice.smith@example.com', '+1987654321', '1985-12-03'),
    ('Bob', 'Wilson', 'bob.wilson@example.com', '+1555123456', '1992-08-22');

-- Insert orders with required fields
INSERT INTO orders (customer_id, total_amount, status) VALUES 
    (1, 150.00, 'pending'),
    (2, 299.99, 'processing'),
    (3, 75.50, 'shipped');
```

## 3.8 Default Values and Sequences

Default values provide fallback values when data is not specified, while sequences generate unique sequential numbers.

### Default Value Types:
- **Constants**: Fixed values like strings, numbers
- **Functions**: CURRENT_TIMESTAMP, CURRENT_DATE, CURRENT_USER
- **Sequences**: Auto-incrementing numbers
- **Expressions**: Computed values

### Sequence Features:
- **SERIAL**: Auto-incrementing integer column
- **BIGSERIAL**: Auto-incrementing bigint column
- **Custom Sequences**: Full control over sequence properties
- **Identity Columns**: SQL standard auto-increment

### Real-World Analogy:
Default values and sequences are like automatic form filling:
- **Constants** = Pre-filled form fields
- **Functions** = Auto-generated timestamps
- **Sequences** = Auto-generated ID numbers
- **Expressions** = Calculated fields

### SQL Example - Default Values and Sequences:
```sql
-- Create table with various default values
CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,  -- Auto-incrementing sequence
    product_code VARCHAR(20) NOT NULL,
    product_name VARCHAR(100) NOT NULL,
    description TEXT,
    price NUMERIC(10,2) NOT NULL DEFAULT 0.00,
    stock_quantity INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by VARCHAR(50) DEFAULT CURRENT_USER,
    status VARCHAR(20) DEFAULT 'active' CHECK (status IN ('active', 'inactive', 'discontinued')),
    version INTEGER DEFAULT 1
);

-- Create custom sequence
CREATE SEQUENCE order_number_seq
    START WITH 1000
    INCREMENT BY 1
    MINVALUE 1000
    MAXVALUE 999999
    CACHE 10;

-- Create table using custom sequence
CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    order_number INTEGER DEFAULT nextval('order_number_seq'),
    customer_id INTEGER NOT NULL,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total_amount NUMERIC(10,2) NOT NULL DEFAULT 0.00,
    status VARCHAR(20) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create table with identity column (SQL standard)
CREATE TABLE invoices (
    invoice_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    invoice_number VARCHAR(20) NOT NULL,
    customer_id INTEGER NOT NULL,
    invoice_date DATE DEFAULT CURRENT_DATE,
    due_date DATE DEFAULT (CURRENT_DATE + INTERVAL '30 days'),
    total_amount NUMERIC(10,2) NOT NULL DEFAULT 0.00,
    status VARCHAR(20) DEFAULT 'draft' CHECK (status IN ('draft', 'sent', 'paid', 'overdue')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert sample data
INSERT INTO products (product_code, product_name, description, price, stock_quantity) VALUES 
    ('LAPTOP001', 'Gaming Laptop', 'High-performance gaming laptop', 1299.99, 10),
    ('MOUSE001', 'Wireless Mouse', 'Ergonomic wireless mouse', 29.99, 50),
    ('KEYBOARD001', 'Mechanical Keyboard', 'RGB mechanical keyboard', 149.99, 25);

-- Insert orders (order_number will be auto-generated)
INSERT INTO orders (customer_id, total_amount) VALUES 
    (1, 150.00),
    (2, 299.99),
    (3, 75.50);

-- Insert invoices (invoice_id will be auto-generated)
INSERT INTO invoices (invoice_number, customer_id, total_amount) VALUES 
    ('INV-2024-001', 1, 150.00),
    ('INV-2024-002', 2, 299.99),
    ('INV-2024-003', 3, 75.50);

-- Query with default values
SELECT 
    product_id,
    product_name,
    price,
    stock_quantity,
    created_at,
    created_by,
    status
FROM products
WHERE status = 'active'
ORDER BY created_at DESC;
```