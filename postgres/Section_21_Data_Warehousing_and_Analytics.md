# Section 21 – Data Warehousing and Analytics

## 21.1 Data Warehouse Design

Data warehouse design involves creating a centralized repository for analytical data that supports business intelligence and reporting.

### Key Concepts:
- **Star Schema**: Central fact table with dimension tables
- **Snowflake Schema**: Normalized dimension tables
- **Fact Tables**: Contain measurable business events
- **Dimension Tables**: Contain descriptive attributes

### Real-World Analogy:
Data warehouse design is like organizing a library:
- **Star Schema** = Central catalog with subject sections
- **Snowflake Schema** = Detailed subject classifications
- **Fact Tables** = Transaction records
- **Dimension Tables** = Reference information

### Example:
```sql
-- Create fact table
CREATE TABLE sales_fact (
    sale_id SERIAL PRIMARY KEY,
    product_id INTEGER,
    customer_id INTEGER,
    date_id INTEGER,
    quantity INTEGER,
    unit_price DECIMAL(10,2),
    total_amount DECIMAL(10,2)
);

-- Create dimension tables
CREATE TABLE dim_product (
    product_id SERIAL PRIMARY KEY,
    product_name VARCHAR(100),
    category VARCHAR(50),
    brand VARCHAR(50)
);

CREATE TABLE dim_customer (
    customer_id SERIAL PRIMARY KEY,
    customer_name VARCHAR(100),
    city VARCHAR(50),
    state VARCHAR(50)
);

CREATE TABLE dim_date (
    date_id INTEGER PRIMARY KEY,
    full_date DATE,
    year INTEGER,
    quarter INTEGER,
    month INTEGER,
    day_of_week INTEGER
);
```

## 21.2 ETL Processes

ETL (Extract, Transform, Load) processes move data from source systems to the data warehouse.

### ETL Components:
- **Extract**: Pull data from source systems
- **Transform**: Clean and format data
- **Load**: Insert data into warehouse
- **Scheduling**: Automated ETL execution

### Real-World Analogy:
ETL processes are like a manufacturing assembly line:
- **Extract** = Raw material collection
- **Transform** = Processing and refinement
- **Load** = Final product assembly
- **Scheduling** = Production line timing

### Example:
```sql
-- Create ETL staging table
CREATE TABLE etl_staging (
    id SERIAL PRIMARY KEY,
    source_system VARCHAR(50),
    raw_data JSONB,
    processed_data JSONB,
    status VARCHAR(20) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT NOW()
);

-- Create ETL function
CREATE OR REPLACE FUNCTION etl_process_data()
RETURNS VOID AS $$
DECLARE
    record RECORD;
BEGIN
    FOR record IN
        SELECT * FROM etl_staging WHERE status = 'pending'
    LOOP
        -- Transform data
        UPDATE etl_staging
        SET 
            processed_data = jsonb_build_object(
                'product_id', (raw_data->>'product_id')::INTEGER,
                'customer_id', (raw_data->>'customer_id')::INTEGER,
                'sale_date', (raw_data->>'sale_date')::DATE,
                'amount', (raw_data->>'amount')::DECIMAL(10,2)
            ),
            status = 'processed'
        WHERE id = record.id;
    END LOOP;
END;
$$ LANGUAGE plpgsql;
```

## 21.3 OLAP Operations

OLAP (Online Analytical Processing) operations enable complex analytical queries on multidimensional data.

### OLAP Operations:
- **Roll-up**: Aggregating data to higher levels
- **Drill-down**: Breaking data into lower levels
- **Slice**: Filtering data by dimension
- **Dice**: Filtering data by multiple dimensions

### Real-World Analogy:
OLAP operations are like analyzing sales data:
- **Roll-up** = Monthly to yearly sales
- **Drill-down** = Product to category sales
- **Slice** = Sales by region
- **Dice** = Sales by region and time

### Example:
```sql
-- Roll-up: Monthly to yearly sales
SELECT 
    d.year,
    SUM(sf.total_amount) as yearly_sales
FROM sales_fact sf
JOIN dim_date d ON sf.date_id = d.date_id
GROUP BY d.year
ORDER BY d.year;

-- Drill-down: Product to category sales
SELECT 
    p.category,
    p.product_name,
    SUM(sf.total_amount) as sales_amount
FROM sales_fact sf
JOIN dim_product p ON sf.product_id = p.product_id
GROUP BY p.category, p.product_name
ORDER BY p.category, sales_amount DESC;

-- Slice: Sales by region
SELECT 
    c.state,
    SUM(sf.total_amount) as state_sales
FROM sales_fact sf
JOIN dim_customer c ON sf.customer_id = c.customer_id
GROUP BY c.state
ORDER BY state_sales DESC;
```

## 21.4 Data Cubes

Data cubes provide multidimensional views of data for analytical purposes.

### Cube Operations:
- **Aggregation**: Summing measures across dimensions
- **Grouping**: Grouping data by dimensions
- **Filtering**: Applying filters to dimensions
- **Sorting**: Ordering results

### Real-World Analogy:
Data cubes are like Rubik's cubes:
- **Aggregation** = Combining colors
- **Grouping** = Organizing by color
- **Filtering** = Focusing on specific colors
- **Sorting** = Arranging in order

### Example:
```sql
-- Create data cube view
CREATE VIEW sales_cube AS
SELECT 
    d.year,
    d.quarter,
    d.month,
    p.category,
    p.brand,
    c.state,
    SUM(sf.total_amount) as total_sales,
    COUNT(*) as transaction_count,
    AVG(sf.unit_price) as avg_price
FROM sales_fact sf
JOIN dim_date d ON sf.date_id = d.date_id
JOIN dim_product p ON sf.product_id = p.product_id
JOIN dim_customer c ON sf.customer_id = c.customer_id
GROUP BY 
    d.year, d.quarter, d.month,
    p.category, p.brand,
    c.state;

-- Query the cube
SELECT 
    year,
    quarter,
    category,
    SUM(total_sales) as quarterly_sales
FROM sales_cube
WHERE year = 2024
GROUP BY year, quarter, category
ORDER BY quarterly_sales DESC;
```

## 21.5 Reporting and Dashboards

Reporting and dashboards provide visual representations of analytical data.

### Report Types:
- **Summary Reports**: High-level overviews
- **Detail Reports**: Detailed data views
- **Trend Reports**: Time-based analysis
- **Comparative Reports**: Side-by-side comparisons

### Real-World Analogy:
Reporting and dashboards are like business presentations:
- **Summary Reports** = Executive summaries
- **Detail Reports** = Detailed analysis
- **Trend Reports** = Historical trends
- **Comparative Reports** = Performance comparisons

### Example:
```sql
-- Create summary report
CREATE OR REPLACE FUNCTION generate_summary_report()
RETURNS TABLE(
    metric_name TEXT,
    metric_value TEXT,
    period TEXT
) AS $$
BEGIN
    -- Monthly sales summary
    RETURN QUERY
    SELECT 
        'Monthly Sales'::TEXT,
        TO_CHAR(SUM(sf.total_amount), 'FM$999,999,999.00')::TEXT,
        'Current Month'::TEXT
    FROM sales_fact sf
    JOIN dim_date d ON sf.date_id = d.date_id
    WHERE d.year = EXTRACT(YEAR FROM CURRENT_DATE)
        AND d.month = EXTRACT(MONTH FROM CURRENT_DATE);
    
    -- Top products
    RETURN QUERY
    SELECT 
        'Top Product'::TEXT,
        p.product_name,
        'Current Month'::TEXT
    FROM sales_fact sf
    JOIN dim_product p ON sf.product_id = p.product_id
    JOIN dim_date d ON sf.date_id = d.date_id
    WHERE d.year = EXTRACT(YEAR FROM CURRENT_DATE)
        AND d.month = EXTRACT(MONTH FROM CURRENT_DATE)
    GROUP BY p.product_name
    ORDER BY SUM(sf.total_amount) DESC
    LIMIT 1;
END;
$$ LANGUAGE plpgsql;
```

## 21.6 Data Mining

Data mining involves discovering patterns and relationships in large datasets.

### Mining Techniques:
- **Classification**: Categorizing data
- **Clustering**: Grouping similar data
- **Association**: Finding relationships
- **Prediction**: Forecasting future values

### Real-World Analogy:
Data mining is like archaeological excavation:
- **Classification** = Categorizing artifacts
- **Clustering** = Grouping similar finds
- **Association** = Finding artifact relationships
- **Prediction** = Predicting excavation sites

### Example:
```sql
-- Customer segmentation
CREATE OR REPLACE FUNCTION segment_customers()
RETURNS TABLE(
    customer_id INTEGER,
    customer_name VARCHAR(100),
    total_spent DECIMAL(10,2),
    segment VARCHAR(20)
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        c.customer_id,
        c.customer_name,
        SUM(sf.total_amount) as total_spent,
        CASE 
            WHEN SUM(sf.total_amount) > 10000 THEN 'High Value'
            WHEN SUM(sf.total_amount) > 5000 THEN 'Medium Value'
            ELSE 'Low Value'
        END as segment
    FROM dim_customer c
    JOIN sales_fact sf ON c.customer_id = sf.customer_id
    GROUP BY c.customer_id, c.customer_name
    ORDER BY total_spent DESC;
END;
$$ LANGUAGE plpgsql;

-- Product association analysis
CREATE OR REPLACE FUNCTION analyze_product_associations()
RETURNS TABLE(
    product1 VARCHAR(100),
    product2 VARCHAR(100),
    support DECIMAL(5,4),
    confidence DECIMAL(5,4)
) AS $$
BEGIN
    RETURN QUERY
    WITH product_pairs AS (
        SELECT DISTINCT
            p1.product_name as product1,
            p2.product_name as product2
        FROM sales_fact sf1
        JOIN sales_fact sf2 ON sf1.sale_id = sf2.sale_id
        JOIN dim_product p1 ON sf1.product_id = p1.product_id
        JOIN dim_product p2 ON sf2.product_id = p2.product_id
        WHERE p1.product_id < p2.product_id
    )
    SELECT 
        pp.product1,
        pp.product2,
        ROUND(
            COUNT(*)::DECIMAL / (SELECT COUNT(*) FROM sales_fact), 4
        ) as support,
        ROUND(
            COUNT(*)::DECIMAL / (
                SELECT COUNT(*) FROM sales_fact sf
                JOIN dim_product p ON sf.product_id = p.product_id
                WHERE p.product_name = pp.product1
            ), 4
        ) as confidence
    FROM product_pairs pp
    GROUP BY pp.product1, pp.product2
    HAVING COUNT(*) > 10
    ORDER BY support DESC;
END;
$$ LANGUAGE plpgsql;
```

## 21.7 Performance Optimization

Performance optimization for data warehousing involves tuning queries and database configuration for analytical workloads.

### Optimization Techniques:
- **Materialized Views**: Pre-computed query results
- **Partitioning**: Dividing large tables
- **Indexing**: Optimizing query performance
- **Compression**: Reducing storage requirements

### Real-World Analogy:
Performance optimization is like tuning a race car:
- **Materialized Views** = Pre-tuned engine settings
- **Partitioning** = Optimized fuel distribution
- **Indexing** = Efficient gear ratios
- **Compression** = Lightweight materials

### Example:
```sql
-- Create materialized view
CREATE MATERIALIZED VIEW mv_monthly_sales AS
SELECT 
    d.year,
    d.month,
    p.category,
    SUM(sf.total_amount) as total_sales,
    COUNT(*) as transaction_count
FROM sales_fact sf
JOIN dim_date d ON sf.date_id = d.date_id
JOIN dim_product p ON sf.product_id = p.product_id
GROUP BY d.year, d.month, p.category;

-- Create index on materialized view
CREATE INDEX idx_mv_monthly_sales_year_month ON mv_monthly_sales (year, month);

-- Refresh materialized view
REFRESH MATERIALIZED VIEW mv_monthly_sales;

-- Create partitioned fact table
CREATE TABLE sales_fact_partitioned (
    LIKE sales_fact INCLUDING ALL
) PARTITION BY RANGE (date_id);

-- Create monthly partitions
CREATE TABLE sales_fact_2024_01 PARTITION OF sales_fact_partitioned
    FOR VALUES FROM (20240101) TO (20240201);

CREATE TABLE sales_fact_2024_02 PARTITION OF sales_fact_partitioned
    FOR VALUES FROM (20240201) TO (20240301);
```

## 21.8 Data Quality

Data quality ensures that analytical data is accurate, complete, and consistent.

### Quality Dimensions:
- **Accuracy**: Data correctness
- **Completeness**: Data availability
- **Consistency**: Data uniformity
- **Timeliness**: Data freshness

### Real-World Analogy:
Data quality is like maintaining a clean laboratory:
- **Accuracy** = Precise measurements
- **Completeness** = All required samples
- **Consistency** = Standardized procedures
- **Timeliness** = Fresh samples

### Example:
```sql
-- Create data quality checks
CREATE OR REPLACE FUNCTION check_data_quality()
RETURNS TABLE(
    check_name TEXT,
    status TEXT,
    details TEXT
) AS $$
BEGIN
    -- Check for missing values
    RETURN QUERY
    SELECT 
        'Missing Values'::TEXT,
        CASE 
            WHEN COUNT(*) = 0 THEN 'PASS'
            ELSE 'FAIL'
        END,
        'Found ' || COUNT(*) || ' records with missing values'::TEXT
    FROM sales_fact
    WHERE product_id IS NULL OR customer_id IS NULL OR total_amount IS NULL;
    
    -- Check for negative amounts
    RETURN QUERY
    SELECT 
        'Negative Amounts'::TEXT,
        CASE 
            WHEN COUNT(*) = 0 THEN 'PASS'
            ELSE 'FAIL'
        END,
        'Found ' || COUNT(*) || ' records with negative amounts'::TEXT
    FROM sales_fact
    WHERE total_amount < 0;
    
    -- Check for duplicate records
    RETURN QUERY
    SELECT 
        'Duplicate Records'::TEXT,
        CASE 
            WHEN COUNT(*) = 0 THEN 'PASS'
            ELSE 'FAIL'
        END,
        'Found ' || COUNT(*) || ' duplicate records'::TEXT
    FROM (
        SELECT product_id, customer_id, date_id, COUNT(*)
        FROM sales_fact
        GROUP BY product_id, customer_id, date_id
        HAVING COUNT(*) > 1
    ) duplicates;
END;
$$ LANGUAGE plpgsql;
```

## 21.9 Real-time Analytics

Real-time analytics provides immediate insights from streaming data.

### Real-time Components:
- **Stream Processing**: Processing data as it arrives
- **Real-time Dashboards**: Live data visualization
- **Event-driven Architecture**: Responding to data events
- **In-memory Processing**: Fast data processing

### Real-World Analogy:
Real-time analytics is like a live sports broadcast:
- **Stream Processing** = Live commentary
- **Real-time Dashboards** = Live scoreboards
- **Event-driven Architecture** = Instant reactions
- **In-memory Processing** = Fast response times

### Example:
```sql
-- Create real-time analytics table
CREATE TABLE real_time_metrics (
    id SERIAL PRIMARY KEY,
    metric_name VARCHAR(100) NOT NULL,
    metric_value DECIMAL(15,2) NOT NULL,
    timestamp TIMESTAMP DEFAULT NOW()
);

-- Create real-time aggregation function
CREATE OR REPLACE FUNCTION update_real_time_metrics()
RETURNS TRIGGER AS $$
BEGIN
    -- Update daily sales metric
    INSERT INTO real_time_metrics (metric_name, metric_value)
    VALUES (
        'daily_sales',
        (SELECT COALESCE(SUM(total_amount), 0) 
         FROM sales_fact sf
         JOIN dim_date d ON sf.date_id = d.date_id
         WHERE d.full_date = CURRENT_DATE)
    );
    
    -- Update hourly sales metric
    INSERT INTO real_time_metrics (metric_name, metric_value)
    VALUES (
        'hourly_sales',
        (SELECT COALESCE(SUM(total_amount), 0) 
         FROM sales_fact sf
         JOIN dim_date d ON sf.date_id = d.date_id
         WHERE d.full_date = CURRENT_DATE
         AND EXTRACT(HOUR FROM NOW()) = EXTRACT(HOUR FROM sf.timestamp))
    );
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create trigger for real-time updates
CREATE TRIGGER real_time_metrics_trigger
    AFTER INSERT ON sales_fact
    FOR EACH ROW EXECUTE FUNCTION update_real_time_metrics();
```

## 21.10 Best Practices

Best practices for data warehousing ensure effective analytical data management.

### Key Practices:
- **Data Modeling**: Proper dimensional modeling
- **ETL Design**: Efficient data processing
- **Performance Tuning**: Optimizing analytical queries
- **Data Governance**: Managing data quality and security

### Real-World Analogy:
Best practices are like following professional standards:
- **Data Modeling** = Architectural blueprints
- **ETL Design** = Efficient manufacturing processes
- **Performance Tuning** = Optimizing production lines
- **Data Governance** = Quality control standards

### Example:
```sql
-- Create data warehouse health check
CREATE OR REPLACE FUNCTION check_warehouse_health()
RETURNS TABLE(
    check_name TEXT,
    status TEXT,
    recommendation TEXT
) AS $$
BEGIN
    -- Check data freshness
    RETURN QUERY
    SELECT 
        'Data Freshness'::TEXT,
        CASE 
            WHEN MAX(d.full_date) >= CURRENT_DATE - INTERVAL '1 day' THEN 'GOOD'
            ELSE 'NEEDS_ATTENTION'
        END,
        CASE 
            WHEN MAX(d.full_date) >= CURRENT_DATE - INTERVAL '1 day' THEN 'Data is current'
            ELSE 'Update ETL processes to ensure daily data refresh'
        END
    FROM sales_fact sf
    JOIN dim_date d ON sf.date_id = d.date_id;
    
    -- Check data volume
    RETURN QUERY
    SELECT 
        'Data Volume'::TEXT,
        CASE 
            WHEN COUNT(*) > 1000000 THEN 'GOOD'
            ELSE 'NEEDS_ATTENTION'
        END,
        CASE 
            WHEN COUNT(*) > 1000000 THEN 'Sufficient data for analysis'
            ELSE 'Consider data retention policies or additional data sources'
        END
    FROM sales_fact;
    
    -- Check query performance
    RETURN QUERY
    SELECT 
        'Query Performance'::TEXT,
        CASE 
            WHEN AVG(response_time) < 5000 THEN 'GOOD'
            ELSE 'NEEDS_ATTENTION'
        END,
        CASE 
            WHEN AVG(response_time) < 5000 THEN 'Query performance is acceptable'
            ELSE 'Consider adding indexes or materialized views'
        END
    FROM (
        SELECT EXTRACT(EPOCH FROM (clock_timestamp() - query_start)) * 1000 as response_time
        FROM pg_stat_activity
        WHERE state = 'active'
    ) query_times;
END;
$$ LANGUAGE plpgsql;
```