# Section 4 – Advanced SQL Features

## 4.1 Window Functions

Window functions perform calculations across a set of rows related to the current row, without collapsing the result set like GROUP BY does.

### Window Function Concepts:
- **Partition**: Groups rows for calculation (PARTITION BY)
- **Ordering**: Defines order within partitions (ORDER BY)
- **Frame**: Defines which rows to include in calculation (ROWS/RANGE)
- **Aggregate Functions**: SUM, AVG, COUNT, MIN, MAX
- **Ranking Functions**: ROW_NUMBER, RANK, DENSE_RANK, NTILE
- **Value Functions**: LAG, LEAD, FIRST_VALUE, LAST_VALUE

### Real-World Analogy:
Window functions are like looking through a window at data:
- **Partition** = Different rooms (groups) to look through
- **Ordering** = Arranging items in each room
- **Frame** = How much of the room you can see
- **Aggregate Functions** = Counting or summing items in view
- **Ranking Functions** = Numbering items by position
- **Value Functions** = Looking at previous or next items

### SQL Example - Window Functions:
```sql
-- Create sample data
CREATE TABLE sales (
    id SERIAL PRIMARY KEY,
    product_name VARCHAR(100),
    category VARCHAR(50),
    sales_date DATE,
    amount NUMERIC(10,2),
    region VARCHAR(50)
);

INSERT INTO sales (product_name, category, sales_date, amount, region) VALUES
    ('Laptop', 'Electronics', '2024-01-15', 1200.00, 'North'),
    ('Mouse', 'Electronics', '2024-01-15', 25.00, 'North'),
    ('Laptop', 'Electronics', '2024-01-16', 1200.00, 'South'),
    ('Keyboard', 'Electronics', '2024-01-16', 75.00, 'South'),
    ('Laptop', 'Electronics', '2024-01-17', 1200.00, 'East'),
    ('Mouse', 'Electronics', '2024-01-17', 25.00, 'East'),
    ('Book', 'Education', '2024-01-15', 30.00, 'North'),
    ('Book', 'Education', '2024-01-16', 30.00, 'South'),
    ('Book', 'Education', '2024-01-17', 30.00, 'East');

-- Basic window functions
SELECT 
    product_name,
    category,
    sales_date,
    amount,
    ROW_NUMBER() OVER (PARTITION BY category ORDER BY amount DESC) as row_num,
    RANK() OVER (PARTITION BY category ORDER BY amount DESC) as rank,
    DENSE_RANK() OVER (PARTITION BY category ORDER BY amount DESC) as dense_rank,
    NTILE(3) OVER (PARTITION BY category ORDER BY amount DESC) as ntile
FROM sales
ORDER BY category, amount DESC;

-- Aggregate window functions
SELECT 
    product_name,
    category,
    amount,
    SUM(amount) OVER (PARTITION BY category) as category_total,
    AVG(amount) OVER (PARTITION BY category) as category_avg,
    COUNT(*) OVER (PARTITION BY category) as category_count,
    amount / SUM(amount) OVER (PARTITION BY category) * 100 as pct_of_category
FROM sales
ORDER BY category, amount DESC;

-- Value functions
SELECT 
    product_name,
    sales_date,
    amount,
    LAG(amount, 1) OVER (PARTITION BY product_name ORDER BY sales_date) as prev_amount,
    LEAD(amount, 1) OVER (PARTITION BY product_name ORDER BY sales_date) as next_amount,
    FIRST_VALUE(amount) OVER (PARTITION BY product_name ORDER BY sales_date) as first_amount,
    LAST_VALUE(amount) OVER (PARTITION BY product_name ORDER BY sales_date 
        ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) as last_amount
FROM sales
ORDER BY product_name, sales_date;
```

## 4.2 Common Table Expressions (CTEs)

CTEs provide a way to define temporary result sets that exist only for the duration of a single query, improving readability and enabling recursive queries.

### CTE Types:
- **Non-Recursive CTEs**: Simple temporary result sets
- **Recursive CTEs**: Self-referencing CTEs for hierarchical data
- **Multiple CTEs**: Multiple CTEs in a single query
- **CTE with Modifying Statements**: CTEs with INSERT, UPDATE, DELETE

### Real-World Analogy:
CTEs are like temporary notes while working:
- **Non-Recursive CTEs** = Simple notes for reference
- **Recursive CTEs** = Notes that reference themselves (like family trees)
- **Multiple CTEs** = Multiple note pages
- **CTE with Modifying** = Notes that change the original data

### SQL Example - Common Table Expressions:
```sql
-- Non-recursive CTE
WITH high_value_sales AS (
    SELECT product_name, amount, sales_date
    FROM sales
    WHERE amount > 1000
),
category_totals AS (
    SELECT category, SUM(amount) as total_amount
    FROM sales
    GROUP BY category
)
SELECT 
    hvs.product_name,
    hvs.amount,
    hvs.sales_date,
    ct.total_amount as category_total
FROM high_value_sales hvs
JOIN sales s ON hvs.product_name = s.product_name
JOIN category_totals ct ON s.category = ct.category
ORDER BY hvs.amount DESC;

-- Recursive CTE for hierarchical data
CREATE TABLE employees (
    emp_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    manager_id INTEGER REFERENCES employees(emp_id),
    position VARCHAR(100)
);

INSERT INTO employees (name, manager_id, position) VALUES
    ('John CEO', NULL, 'CEO'),
    ('Alice VP', 1, 'VP Sales'),
    ('Bob Manager', 2, 'Sales Manager'),
    ('Carol Manager', 2, 'Sales Manager'),
    ('David Rep', 3, 'Sales Rep'),
    ('Eve Rep', 3, 'Sales Rep'),
    ('Frank Rep', 4, 'Sales Rep');

-- Recursive CTE to show hierarchy
WITH RECURSIVE employee_hierarchy AS (
    -- Base case: top-level employees
    SELECT emp_id, name, manager_id, position, 0 as level, 
           name as hierarchy_path
    FROM employees 
    WHERE manager_id IS NULL
    
    UNION ALL
    
    -- Recursive case: employees with managers
    SELECT e.emp_id, e.name, e.manager_id, e.position, 
           eh.level + 1,
           eh.hierarchy_path || ' -> ' || e.name
    FROM employees e
    JOIN employee_hierarchy eh ON e.manager_id = eh.emp_id
)
SELECT 
    level,
    hierarchy_path,
    position
FROM employee_hierarchy
ORDER BY level, name;
```

## 4.3 Recursive Queries

Recursive queries use CTEs to process hierarchical or graph data by repeatedly applying a query to its own results.

### Recursive Query Structure:
- **Base Case**: Initial condition that stops recursion
- **Recursive Case**: Condition that continues recursion
- **Termination**: Automatic when no more rows are returned
- **Depth Control**: Optional limits on recursion depth

### Common Use Cases:
- **Hierarchical Data**: Organizational charts, file systems
- **Graph Traversal**: Social networks, dependencies
- **Data Generation**: Creating test data, sequences
- **Path Finding**: Shortest paths, all paths

### Real-World Analogy:
Recursive queries are like following a chain of references:
- **Base Case** = Starting point (no more references)
- **Recursive Case** = Following the next reference
- **Termination** = When you reach the end of the chain
- **Depth Control** = Limiting how far you follow

### SQL Example - Recursive Queries:
```sql
-- Create hierarchical data
CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    parent_id INTEGER REFERENCES categories(id)
);

INSERT INTO categories (name, parent_id) VALUES
    ('Electronics', NULL),
    ('Computers', 1),
    ('Laptops', 2),
    ('Desktops', 2),
    ('Accessories', 1),
    ('Mice', 5),
    ('Keyboards', 5),
    ('Gaming Laptops', 3),
    ('Business Laptops', 3);

-- Recursive query to show full hierarchy
WITH RECURSIVE category_tree AS (
    -- Base case: root categories
    SELECT id, name, parent_id, 0 as level, 
           name as full_path
    FROM categories 
    WHERE parent_id IS NULL
    
    UNION ALL
    
    -- Recursive case: child categories
    SELECT c.id, c.name, c.parent_id, ct.level + 1,
           ct.full_path || ' > ' || c.name
    FROM categories c
    JOIN category_tree ct ON c.parent_id = ct.id
)
SELECT 
    level,
    full_path,
    name
FROM category_tree
ORDER BY level, full_path;

-- Recursive query with depth limit
WITH RECURSIVE category_tree AS (
    SELECT id, name, parent_id, 0 as level, 
           name as full_path
    FROM categories 
    WHERE parent_id IS NULL
    
    UNION ALL
    
    SELECT c.id, c.name, c.parent_id, ct.level + 1,
           ct.full_path || ' > ' || c.name
    FROM categories c
    JOIN category_tree ct ON c.parent_id = ct.id
    WHERE ct.level < 2  -- Limit depth to 2 levels
)
SELECT 
    level,
    full_path,
    name
FROM category_tree
ORDER BY level, full_path;
```

## 4.4 Lateral Joins

Lateral joins allow subqueries in the FROM clause to reference columns from preceding tables in the same FROM clause.

### Lateral Join Features:
- **Correlation**: Subquery can reference outer query columns
- **Performance**: Can be more efficient than correlated subqueries
- **Flexibility**: Enables complex join patterns
- **PostgreSQL Specific**: Not part of SQL standard

### Real-World Analogy:
Lateral joins are like having a helper who can see what you're working on:
- **Correlation** = Helper can see your current work
- **Performance** = More efficient than asking for help separately
- **Flexibility** = Helper can adapt based on what they see
- **PostgreSQL Specific** = Special feature of this system

### SQL Example - Lateral Joins:
```sql
-- Create sample data
CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    customer_id INTEGER,
    order_date DATE,
    total_amount NUMERIC(10,2)
);

CREATE TABLE order_items (
    item_id SERIAL PRIMARY KEY,
    order_id INTEGER REFERENCES orders(order_id),
    product_name VARCHAR(100),
    quantity INTEGER,
    unit_price NUMERIC(10,2)
);

INSERT INTO orders (customer_id, order_date, total_amount) VALUES
    (1, '2024-01-15', 150.00),
    (2, '2024-01-16', 299.99),
    (3, '2024-01-17', 75.50);

INSERT INTO order_items (order_id, product_name, quantity, unit_price) VALUES
    (1, 'Laptop', 1, 1200.00),
    (1, 'Mouse', 2, 25.00),
    (2, 'Gaming Laptop', 1, 1299.99),
    (2, 'Gaming Mouse', 1, 79.99),
    (3, 'Book', 1, 30.00),
    (3, 'Pen', 5, 2.50);

-- Lateral join example
SELECT 
    o.order_id,
    o.customer_id,
    o.order_date,
    o.total_amount,
    top_items.product_name,
    top_items.quantity,
    top_items.unit_price
FROM orders o
CROSS JOIN LATERAL (
    SELECT product_name, quantity, unit_price
    FROM order_items oi
    WHERE oi.order_id = o.order_id
    ORDER BY oi.unit_price DESC
    LIMIT 2
) AS top_items
ORDER BY o.order_id, top_items.unit_price DESC;

-- Lateral join with aggregation
SELECT 
    o.order_id,
    o.customer_id,
    o.order_date,
    o.total_amount,
    item_stats.item_count,
    item_stats.avg_price,
    item_stats.max_price
FROM orders o
CROSS JOIN LATERAL (
    SELECT 
        COUNT(*) as item_count,
        AVG(unit_price) as avg_price,
        MAX(unit_price) as max_price
    FROM order_items oi
    WHERE oi.order_id = o.order_id
) AS item_stats
ORDER BY o.order_id;
```

## 4.5 Advanced Joins

PostgreSQL supports various join types and advanced join techniques for complex data relationships.

### Join Types:
- **INNER JOIN**: Returns matching rows from both tables
- **LEFT JOIN**: Returns all rows from left table, matching from right
- **RIGHT JOIN**: Returns all rows from right table, matching from left
- **FULL OUTER JOIN**: Returns all rows from both tables
- **CROSS JOIN**: Cartesian product of both tables
- **SELF JOIN**: Table joined with itself

### Advanced Join Techniques:
- **Multiple Joins**: Joining more than two tables
- **Conditional Joins**: Joins with complex conditions
- **Join Optimization**: Using indexes and hints
- **Anti-Joins**: Finding non-matching rows

### Real-World Analogy:
Advanced joins are like matching different types of information:
- **INNER JOIN** = Finding exact matches
- **LEFT JOIN** = Keeping all from one list, adding matches from another
- **RIGHT JOIN** = Keeping all from second list, adding matches from first
- **FULL OUTER JOIN** = Keeping everything from both lists
- **CROSS JOIN** = Combining every item from one list with every item from another

### SQL Example - Advanced Joins:
```sql
-- Create sample data
CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    city VARCHAR(50)
);

CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    customer_id INTEGER REFERENCES customers(customer_id),
    order_date DATE,
    total_amount NUMERIC(10,2)
);

CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    category VARCHAR(50),
    price NUMERIC(10,2)
);

CREATE TABLE order_items (
    order_id INTEGER REFERENCES orders(order_id),
    product_id INTEGER REFERENCES products(product_id),
    quantity INTEGER,
    unit_price NUMERIC(10,2),
    PRIMARY KEY (order_id, product_id)
);

INSERT INTO customers (name, email, city) VALUES
    ('John Doe', 'john@example.com', 'New York'),
    ('Alice Smith', 'alice@example.com', 'San Francisco'),
    ('Bob Wilson', 'bob@example.com', 'Chicago'),
    ('Carol Brown', 'carol@example.com', 'New York');

INSERT INTO orders (customer_id, order_date, total_amount) VALUES
    (1, '2024-01-15', 150.00),
    (2, '2024-01-16', 299.99),
    (3, '2024-01-17', 75.50),
    (1, '2024-01-18', 200.00);

INSERT INTO products (name, category, price) VALUES
    ('Laptop', 'Electronics', 1200.00),
    ('Mouse', 'Electronics', 25.00),
    ('Book', 'Education', 30.00);

INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES
    (1, 1, 1, 1200.00),
    (1, 2, 2, 25.00),
    (2, 1, 1, 1299.99),
    (3, 3, 1, 30.00),
    (4, 2, 4, 25.00);

-- Multiple joins
SELECT 
    c.name as customer_name,
    c.city,
    o.order_date,
    o.total_amount,
    p.name as product_name,
    oi.quantity,
    oi.unit_price
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id
INNER JOIN order_items oi ON o.order_id = oi.order_id
INNER JOIN products p ON oi.product_id = p.product_id
ORDER BY c.name, o.order_date;

-- Left join to show all customers
SELECT 
    c.name as customer_name,
    c.city,
    o.order_id,
    o.order_date,
    o.total_amount
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
ORDER BY c.name, o.order_date;

-- Full outer join
SELECT 
    c.name as customer_name,
    o.order_id,
    o.order_date,
    o.total_amount
FROM customers c
FULL OUTER JOIN orders o ON c.customer_id = o.customer_id
ORDER BY c.name, o.order_date;

-- Anti-join (customers without orders)
SELECT 
    c.name as customer_name,
    c.email,
    c.city
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
WHERE o.customer_id IS NULL;
```

## 4.6 Subqueries and Correlated Subqueries

Subqueries are queries nested within other queries, while correlated subqueries reference columns from the outer query.

### Subquery Types:
- **Scalar Subqueries**: Return single value
- **Row Subqueries**: Return single row
- **Table Subqueries**: Return multiple rows
- **Correlated Subqueries**: Reference outer query columns
- **EXISTS Subqueries**: Check for existence

### Real-World Analogy:
Subqueries are like asking questions within questions:
- **Scalar Subqueries** = Asking for a single answer
- **Row Subqueries** = Asking for one complete record
- **Table Subqueries** = Asking for multiple records
- **Correlated Subqueries** = Questions that depend on the current context
- **EXISTS Subqueries** = Questions about whether something exists

### SQL Example - Subqueries:
```sql
-- Scalar subquery
SELECT 
    name,
    total_amount,
    (SELECT AVG(total_amount) FROM orders) as avg_order_amount,
    total_amount - (SELECT AVG(total_amount) FROM orders) as difference_from_avg
FROM orders
WHERE total_amount > (SELECT AVG(total_amount) FROM orders);

-- Row subquery
SELECT 
    c.name,
    c.city,
    o.order_date,
    o.total_amount
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
WHERE (o.order_date, o.total_amount) IN (
    SELECT order_date, total_amount
    FROM orders
    WHERE total_amount > 200
);

-- Table subquery
SELECT 
    c.name,
    c.city,
    order_count,
    total_spent
FROM customers c
JOIN (
    SELECT 
        customer_id,
        COUNT(*) as order_count,
        SUM(total_amount) as total_spent
    FROM orders
    GROUP BY customer_id
) o_stats ON c.customer_id = o_stats.customer_id
ORDER BY total_spent DESC;

-- Correlated subquery
SELECT 
    c.name,
    c.city,
    o.order_date,
    o.total_amount,
    (SELECT COUNT(*) 
     FROM orders o2 
     WHERE o2.customer_id = o.customer_id 
     AND o2.order_date < o.order_date) as previous_orders
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
ORDER BY c.name, o.order_date;

-- EXISTS subquery
SELECT 
    c.name,
    c.email,
    c.city
FROM customers c
WHERE EXISTS (
    SELECT 1 
    FROM orders o 
    WHERE o.customer_id = c.customer_id 
    AND o.total_amount > 100
);

-- NOT EXISTS subquery
SELECT 
    c.name,
    c.email,
    c.city
FROM customers c
WHERE NOT EXISTS (
    SELECT 1 
    FROM orders o 
    WHERE o.customer_id = c.customer_id
);
```

## 4.7 Set Operations (UNION, INTERSECT, EXCEPT)

Set operations combine results from multiple queries using mathematical set theory.

### Set Operation Types:
- **UNION**: Combines results, removes duplicates
- **UNION ALL**: Combines results, keeps duplicates
- **INTERSECT**: Returns common rows
- **EXCEPT**: Returns rows from first query not in second
- **INTERSECT ALL**: Returns common rows, keeps duplicates
- **EXCEPT ALL**: Returns rows from first query not in second, keeps duplicates

### Real-World Analogy:
Set operations are like combining different lists:
- **UNION** = Merging two lists, removing duplicates
- **UNION ALL** = Merging two lists, keeping duplicates
- **INTERSECT** = Finding items that appear in both lists
- **EXCEPT** = Finding items in first list but not in second
- **INTERSECT ALL** = Finding common items, keeping duplicates
- **EXCEPT ALL** = Finding unique items, keeping duplicates

### SQL Example - Set Operations:
```sql
-- Create sample data
CREATE TABLE employees_2023 (
    emp_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    department VARCHAR(50),
    salary NUMERIC(10,2)
);

CREATE TABLE employees_2024 (
    emp_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    department VARCHAR(50),
    salary NUMERIC(10,2)
);

INSERT INTO employees_2023 (name, department, salary) VALUES
    ('John Doe', 'Sales', 50000),
    ('Alice Smith', 'Marketing', 55000),
    ('Bob Wilson', 'IT', 60000),
    ('Carol Brown', 'Sales', 52000);

INSERT INTO employees_2024 (name, department, salary) VALUES
    ('John Doe', 'Sales', 52000),
    ('Alice Smith', 'Marketing', 57000),
    ('Bob Wilson', 'IT', 62000),
    ('David Lee', 'IT', 58000),
    ('Eve Johnson', 'HR', 48000);

-- UNION (all employees from both years)
SELECT name, department, salary, '2023' as year
FROM employees_2023
UNION
SELECT name, department, salary, '2024' as year
FROM employees_2024
ORDER BY name, year;

-- UNION ALL (all employees, keeping duplicates)
SELECT name, department, salary, '2023' as year
FROM employees_2023
UNION ALL
SELECT name, department, salary, '2024' as year
FROM employees_2024
ORDER BY name, year;

-- INTERSECT (employees in both years)
SELECT name, department
FROM employees_2023
INTERSECT
SELECT name, department
FROM employees_2024
ORDER BY name;

-- EXCEPT (employees only in 2023)
SELECT name, department
FROM employees_2023
EXCEPT
SELECT name, department
FROM employees_2024
ORDER BY name;

-- EXCEPT (employees only in 2024)
SELECT name, department
FROM employees_2024
EXCEPT
SELECT name, department
FROM employees_2023
ORDER BY name;

-- Complex set operations
SELECT 
    name,
    department,
    salary,
    '2023' as year
FROM employees_2023
WHERE department = 'Sales'
UNION
SELECT 
    name,
    department,
    salary,
    '2024' as year
FROM employees_2024
WHERE department = 'Sales'
ORDER BY name, year;
```

## 4.8 Full-Text Search

PostgreSQL provides powerful full-text search capabilities using specialized data types and functions.

### Full-Text Search Components:
- **tsvector**: Text search vector (normalized text)
- **tsquery**: Text search query (search terms)
- **Search Functions**: to_tsvector, to_tsquery, plainto_tsquery
- **Operators**: @@ (matches), && (overlaps), @> (contains)
- **Ranking**: ts_rank, ts_rank_cd

### Real-World Analogy:
Full-text search is like having a smart librarian:
- **tsvector** = Index of all words in books
- **tsquery** = Your search request
- **Search Functions** = Librarian's search tools
- **Operators** = Different ways to search
- **Ranking** = Librarian's recommendations

### SQL Example - Full-Text Search:
```sql
-- Create table with text content
CREATE TABLE articles (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200),
    content TEXT,
    author VARCHAR(100),
    published_date DATE
);

INSERT INTO articles (title, content, author, published_date) VALUES
    ('PostgreSQL Basics', 'PostgreSQL is a powerful open-source database system with advanced features.', 'John Doe', '2024-01-15'),
    ('Advanced SQL Queries', 'Learn about window functions, CTEs, and recursive queries in PostgreSQL.', 'Alice Smith', '2024-01-16'),
    ('Database Performance', 'Optimizing database performance requires understanding indexes and query plans.', 'Bob Wilson', '2024-01-17'),
    ('PostgreSQL Extensions', 'PostgreSQL supports many extensions like PostGIS for geospatial data.', 'Carol Brown', '2024-01-18');

-- Create full-text search index
CREATE INDEX idx_articles_search ON articles USING GIN (to_tsvector('english', title || ' ' || content));

-- Basic full-text search
SELECT 
    title,
    author,
    published_date,
    ts_rank(to_tsvector('english', title || ' ' || content), to_tsquery('english', 'PostgreSQL')) as rank
FROM articles
WHERE to_tsvector('english', title || ' ' || content) @@ to_tsquery('english', 'PostgreSQL')
ORDER BY rank DESC;

-- Search with multiple terms
SELECT 
    title,
    author,
    published_date
FROM articles
WHERE to_tsvector('english', title || ' ' || content) @@ to_tsquery('english', 'PostgreSQL & performance')
ORDER BY published_date DESC;

-- Search with phrase
SELECT 
    title,
    author,
    published_date
FROM articles
WHERE to_tsvector('english', title || ' ' || content) @@ phraseto_tsquery('english', 'database performance')
ORDER BY published_date DESC;

-- Search with wildcards
SELECT 
    title,
    author,
    published_date
FROM articles
WHERE to_tsvector('english', title || ' ' || content) @@ to_tsquery('english', 'Postgre:*')
ORDER BY published_date DESC;

-- Highlight search results
SELECT 
    title,
    author,
    ts_headline('english', content, to_tsquery('english', 'PostgreSQL'), 'MaxWords=10, MinWords=5') as headline
FROM articles
WHERE to_tsvector('english', title || ' ' || content) @@ to_tsquery('english', 'PostgreSQL')
ORDER BY published_date DESC;
```

## 4.9 Regular Expressions

PostgreSQL supports regular expressions for pattern matching and text manipulation.

### Regular Expression Features:
- **Pattern Matching**: ~, ~*, !~, !~*
- **Case Sensitivity**: ~ (case-sensitive), ~* (case-insensitive)
- **Negation**: !~ (does not match), !~* (does not match case-insensitive)
- **Functions**: regexp_replace, regexp_split_to_array, regexp_split_to_table
- **Operators**: SIMILAR TO, POSIX regular expressions

### Real-World Analogy:
Regular expressions are like advanced search patterns:
- **Pattern Matching** = Finding text that follows specific rules
- **Case Sensitivity** = Whether to care about uppercase/lowercase
- **Negation** = Finding text that doesn't follow patterns
- **Functions** = Tools for manipulating text based on patterns
- **Operators** = Different ways to apply patterns

### SQL Example - Regular Expressions:
```sql
-- Create table with text data
CREATE TABLE user_data (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50),
    email VARCHAR(100),
    phone VARCHAR(20),
    full_name VARCHAR(100)
);

INSERT INTO user_data (username, email, phone, full_name) VALUES
    ('jdoe', 'john.doe@example.com', '+1-555-123-4567', 'John Doe'),
    ('asmith', 'alice.smith@company.org', '(555) 987-6543', 'Alice Smith'),
    ('bwilson', 'bob.wilson@test.net', '555.456.7890', 'Bob Wilson'),
    ('cbrown', 'carol.brown@example.com', '+1 555 321 9876', 'Carol Brown');

-- Basic pattern matching
SELECT 
    username,
    email,
    full_name
FROM user_data
WHERE email ~ '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$';

-- Case-insensitive matching
SELECT 
    username,
    email,
    full_name
FROM user_data
WHERE full_name ~* '^[a-z]+ [a-z]+$';

-- Negation (does not match)
SELECT 
    username,
    email,
    full_name
FROM user_data
WHERE email !~ '\.com$';

-- Extract parts using regular expressions
SELECT 
    username,
    email,
    regexp_replace(email, '@.*', '') as local_part,
    regexp_replace(email, '.*@', '') as domain
FROM user_data;

-- Split text using regular expressions
SELECT 
    username,
    full_name,
    regexp_split_to_array(full_name, ' ') as name_parts
FROM user_data;

-- Complex pattern matching
SELECT 
    username,
    phone,
    CASE 
        WHEN phone ~ '^\+1' THEN 'US Format'
        WHEN phone ~ '^\(555\)' THEN 'Parentheses Format'
        WHEN phone ~ '^555\.' THEN 'Dot Format'
        ELSE 'Other Format'
    END as phone_format
FROM user_data;

-- Replace using regular expressions
SELECT 
    username,
    phone,
    regexp_replace(phone, '[^0-9]', '', 'g') as digits_only
FROM user_data;

-- Extract specific patterns
SELECT 
    username,
    email,
    regexp_replace(email, '^([^@]+)@.*', '\1') as extracted_username
FROM user_data;
```

## 4.10 Advanced Aggregation

PostgreSQL provides advanced aggregation functions and techniques for complex data analysis.

### Advanced Aggregation Features:
- **Grouping Sets**: Multiple grouping levels in one query
- **Rollup**: Hierarchical grouping
- **Cube**: All possible grouping combinations
- **Filtering**: FILTER clause for conditional aggregation
- **Ordering**: ORDER BY in aggregate functions
- **Custom Aggregates**: User-defined aggregate functions

### Real-World Analogy:
Advanced aggregation is like creating different types of summaries:
- **Grouping Sets** = Multiple summary reports at once
- **Rollup** = Hierarchical summaries (by year, then by month)
- **Cube** = All possible combinations of summaries
- **Filtering** = Conditional summaries (only certain conditions)
- **Ordering** = Sorted summaries
- **Custom Aggregates** = Specialized summary methods

### SQL Example - Advanced Aggregation:
```sql
-- Create sample data
CREATE TABLE sales_data (
    id SERIAL PRIMARY KEY,
    product_category VARCHAR(50),
    product_name VARCHAR(100),
    region VARCHAR(50),
    quarter VARCHAR(10),
    year INTEGER,
    sales_amount NUMERIC(10,2)
);

INSERT INTO sales_data (product_category, product_name, region, quarter, year, sales_amount) VALUES
    ('Electronics', 'Laptop', 'North', 'Q1', 2024, 50000),
    ('Electronics', 'Laptop', 'South', 'Q1', 2024, 45000),
    ('Electronics', 'Mouse', 'North', 'Q1', 2024, 5000),
    ('Electronics', 'Mouse', 'South', 'Q1', 2024, 4000),
    ('Electronics', 'Laptop', 'North', 'Q2', 2024, 55000),
    ('Electronics', 'Laptop', 'South', 'Q2', 2024, 48000),
    ('Electronics', 'Mouse', 'North', 'Q2', 2024, 6000),
    ('Electronics', 'Mouse', 'South', 'Q2', 2024, 4500),
    ('Books', 'Programming', 'North', 'Q1', 2024, 10000),
    ('Books', 'Programming', 'South', 'Q1', 2024, 8000),
    ('Books', 'Programming', 'North', 'Q2', 2024, 12000),
    ('Books', 'Programming', 'South', 'Q2', 2024, 9000);

-- Basic aggregation
SELECT 
    product_category,
    SUM(sales_amount) as total_sales,
    AVG(sales_amount) as avg_sales,
    COUNT(*) as record_count
FROM sales_data
GROUP BY product_category
ORDER BY total_sales DESC;

-- Grouping sets
SELECT 
    product_category,
    region,
    quarter,
    SUM(sales_amount) as total_sales
FROM sales_data
GROUP BY GROUPING SETS (
    (product_category),
    (region),
    (quarter),
    (product_category, region),
    (product_category, quarter),
    (region, quarter),
    (product_category, region, quarter)
)
ORDER BY product_category, region, quarter;

-- Rollup (hierarchical grouping)
SELECT 
    year,
    quarter,
    product_category,
    SUM(sales_amount) as total_sales
FROM sales_data
GROUP BY ROLLUP (year, quarter, product_category)
ORDER BY year, quarter, product_category;

-- Cube (all combinations)
SELECT 
    product_category,
    region,
    quarter,
    SUM(sales_amount) as total_sales
FROM sales_data
GROUP BY CUBE (product_category, region, quarter)
ORDER BY product_category, region, quarter;

-- Filtering in aggregation
SELECT 
    product_category,
    SUM(sales_amount) as total_sales,
    SUM(sales_amount) FILTER (WHERE quarter = 'Q1') as q1_sales,
    SUM(sales_amount) FILTER (WHERE quarter = 'Q2') as q2_sales,
    SUM(sales_amount) FILTER (WHERE region = 'North') as north_sales,
    SUM(sales_amount) FILTER (WHERE region = 'South') as south_sales
FROM sales_data
GROUP BY product_category
ORDER BY total_sales DESC;

-- Ordering in aggregate functions
SELECT 
    product_category,
    array_agg(product_name ORDER BY sales_amount DESC) as products_by_sales,
    string_agg(product_name, ', ' ORDER BY sales_amount DESC) as products_list
FROM sales_data
GROUP BY product_category
ORDER BY product_category;

-- Advanced aggregation with window functions
SELECT 
    product_category,
    region,
    quarter,
    sales_amount,
    SUM(sales_amount) OVER (PARTITION BY product_category) as category_total,
    SUM(sales_amount) OVER (PARTITION BY product_category, region) as region_total,
    ROW_NUMBER() OVER (PARTITION BY product_category ORDER BY sales_amount DESC) as rank_in_category
FROM sales_data
ORDER BY product_category, region, quarter;
```