# Section 16 – Data Warehousing

## 16.1 Data Warehouse Architecture

A data warehouse is a centralized repository that stores integrated data from multiple sources, designed for analytical processing and business intelligence.

### Key Components:
- **Data Sources**: Operational systems, external data, files
- **ETL Process**: Extract, Transform, Load operations
- **Data Warehouse**: Central storage for integrated data
- **Data Marts**: Subset of data warehouse for specific departments
- **OLAP Tools**: Online Analytical Processing tools
- **Metadata**: Data about data

### Real-World Analogy:
A data warehouse is like a central library system:
- **Data Sources** = Different book publishers and authors
- **ETL Process** = Librarians organizing and cataloging books
- **Data Warehouse** = Main library with all books
- **Data Marts** = Specialized sections (fiction, non-fiction, reference)
- **OLAP Tools** = Search systems and catalogs
- **Metadata** = Card catalog system

### Java Example - Data Warehouse Architecture:
```java
public class DataWarehouseArchitecture {
    private List<DataSource> dataSources;
    private ETLProcessor etlProcessor;
    private DataWarehouse dataWarehouse;
    private List<DataMart> dataMarts;
    
    public DataWarehouseArchitecture() {
        this.dataSources = new ArrayList<>();
        this.etlProcessor = new ETLProcessor();
        this.dataWarehouse = new DataWarehouse();
        this.dataMarts = new ArrayList<>();
    }
    
    // Add data source
    public void addDataSource(DataSource source) {
        dataSources.add(source);
        System.out.println("Data source added: " + source.getName());
    }
    
    // Process data from all sources
    public void processData() {
        for (DataSource source : dataSources) {
            RawData rawData = source.extract();
            ProcessedData processedData = etlProcessor.transform(rawData);
            dataWarehouse.load(processedData);
        }
        System.out.println("Data processing completed");
    }
    
    // Create data mart
    public void createDataMart(String name, String[] tables) {
        DataMart mart = new DataMart(name, tables);
        dataMarts.add(mart);
        System.out.println("Data mart created: " + name);
    }
}

// Data source interface
interface DataSource {
    String getName();
    RawData extract();
}

// ETL processor
class ETLProcessor {
    public ProcessedData transform(RawData rawData) {
        // Data transformation logic
        return new ProcessedData(rawData.getData());
    }
}

// Data warehouse
class DataWarehouse {
    private Map<String, Table> tables = new HashMap<>();
    
    public void load(ProcessedData data) {
        // Load data into warehouse
        System.out.println("Data loaded into warehouse");
    }
}

// Data mart
class DataMart {
    private String name;
    private String[] tables;
    
    public DataMart(String name, String[] tables) {
        this.name = name;
        this.tables = tables;
    }
}
```

## 16.2 Star Schema and Snowflake Schema

Star and snowflake schemas are dimensional modeling approaches used in data warehouses to organize data for efficient querying.

### Star Schema:
- **Fact Table**: Central table with measures and foreign keys
- **Dimension Tables**: Surrounding tables with descriptive attributes
- **Simple Structure**: One level of dimension tables
- **Fast Queries**: Optimized for analytical queries

### Snowflake Schema:
- **Normalized Dimensions**: Dimension tables can have sub-dimensions
- **Hierarchical Structure**: Multiple levels of dimension relationships
- **Space Efficient**: Reduces data redundancy
- **Complex Queries**: May require more joins

### Real-World Analogy:
- **Star Schema** = Simple family tree (parents and children)
- **Snowflake Schema** = Extended family tree (grandparents, parents, children, cousins)

### SQL Example - Star Schema:
```sql
-- Fact table (sales)
CREATE TABLE fact_sales (
    sale_id INT PRIMARY KEY,
    product_id INT,
    customer_id INT,
    date_id INT,
    store_id INT,
    quantity INT,
    unit_price DECIMAL(10,2),
    total_amount DECIMAL(10,2),
    FOREIGN KEY (product_id) REFERENCES dim_product(product_id),
    FOREIGN KEY (customer_id) REFERENCES dim_customer(customer_id),
    FOREIGN KEY (date_id) REFERENCES dim_date(date_id),
    FOREIGN KEY (store_id) REFERENCES dim_store(store_id)
);

-- Dimension tables
CREATE TABLE dim_product (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(100),
    category VARCHAR(50),
    brand VARCHAR(50),
    price DECIMAL(10,2)
);

CREATE TABLE dim_customer (
    customer_id INT PRIMARY KEY,
    customer_name VARCHAR(100),
    city VARCHAR(50),
    state VARCHAR(50),
    country VARCHAR(50)
);

CREATE TABLE dim_date (
    date_id INT PRIMARY KEY,
    full_date DATE,
    year INT,
    quarter INT,
    month INT,
    day INT,
    day_of_week VARCHAR(10)
);

CREATE TABLE dim_store (
    store_id INT PRIMARY KEY,
    store_name VARCHAR(100),
    city VARCHAR(50),
    state VARCHAR(50),
    manager VARCHAR(100)
);
```

### SQL Example - Snowflake Schema:
```sql
-- Normalized dimension tables
CREATE TABLE dim_product (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(100),
    category_id INT,
    brand_id INT,
    price DECIMAL(10,2),
    FOREIGN KEY (category_id) REFERENCES dim_category(category_id),
    FOREIGN KEY (brand_id) REFERENCES dim_brand(brand_id)
);

CREATE TABLE dim_category (
    category_id INT PRIMARY KEY,
    category_name VARCHAR(50),
    department_id INT,
    FOREIGN KEY (department_id) REFERENCES dim_department(department_id)
);

CREATE TABLE dim_department (
    department_id INT PRIMARY KEY,
    department_name VARCHAR(50)
);

CREATE TABLE dim_brand (
    brand_id INT PRIMARY KEY,
    brand_name VARCHAR(50),
    manufacturer_id INT,
    FOREIGN KEY (manufacturer_id) REFERENCES dim_manufacturer(manufacturer_id)
);

CREATE TABLE dim_manufacturer (
    manufacturer_id INT PRIMARY KEY,
    manufacturer_name VARCHAR(100),
    country VARCHAR(50)
);
```

## 16.3 Fact Tables and Dimension Tables

Fact and dimension tables are the core components of dimensional modeling in data warehouses.

### Fact Tables:
- **Measures**: Numerical values that can be aggregated
- **Foreign Keys**: Links to dimension tables
- **Grain**: Level of detail in the fact table
- **Additive Measures**: Can be summed across dimensions
- **Semi-Additive Measures**: Can be summed across some dimensions
- **Non-Additive Measures**: Cannot be summed (ratios, percentages)

### Dimension Tables:
- **Descriptive Attributes**: Textual descriptions
- **Hierarchies**: Natural groupings of attributes
- **Slowly Changing Dimensions**: Handle changes over time
- **Surrogate Keys**: Artificial keys for dimension tables
- **Natural Keys**: Business keys from source systems

### Real-World Analogy:
- **Fact Table** = Sales receipt with quantities and amounts
- **Dimension Tables** = Product catalog, customer directory, store locations

### Java Example - Fact and Dimension Tables:
```java
// Fact table representation
public class FactSales {
    private int saleId;
    private int productId;
    private int customerId;
    private int dateId;
    private int storeId;
    private int quantity;
    private BigDecimal unitPrice;
    private BigDecimal totalAmount;
    
    // Constructors, getters, setters
    public FactSales(int saleId, int productId, int customerId, int dateId, 
                    int storeId, int quantity, BigDecimal unitPrice) {
        this.saleId = saleId;
        this.productId = productId;
        this.customerId = customerId;
        this.dateId = dateId;
        this.storeId = storeId;
        this.quantity = quantity;
        this.unitPrice = unitPrice;
        this.totalAmount = unitPrice.multiply(BigDecimal.valueOf(quantity));
    }
    
    // Additive measure
    public BigDecimal getTotalAmount() {
        return totalAmount;
    }
    
    // Semi-additive measure
    public int getQuantity() {
        return quantity;
    }
    
    // Non-additive measure
    public BigDecimal getAveragePrice() {
        return totalAmount.divide(BigDecimal.valueOf(quantity), 2, RoundingMode.HALF_UP);
    }
}

// Dimension table representation
public class DimProduct {
    private int productId;
    private String productName;
    private String category;
    private String brand;
    private BigDecimal price;
    
    public DimProduct(int productId, String productName, String category, 
                     String brand, BigDecimal price) {
        this.productId = productId;
        this.productName = productName;
        this.category = category;
        this.brand = brand;
        this.price = price;
    }
    
    // Getters and setters
    public int getProductId() { return productId; }
    public String getProductName() { return productName; }
    public String getCategory() { return category; }
    public String getBrand() { return brand; }
    public BigDecimal getPrice() { return price; }
}

// Slowly changing dimension
public class DimCustomer {
    private int customerId;
    private String customerName;
    private String city;
    private String state;
    private String country;
    private Date effectiveDate;
    private Date endDate;
    private boolean isCurrent;
    
    public DimCustomer(int customerId, String customerName, String city, 
                      String state, String country, Date effectiveDate) {
        this.customerId = customerId;
        this.customerName = customerName;
        this.city = city;
        this.state = state;
        this.country = country;
        this.effectiveDate = effectiveDate;
        this.endDate = null;
        this.isCurrent = true;
    }
    
    // Handle customer address change
    public DimCustomer createNewVersion(String newCity, String newState, String newCountry) {
        DimCustomer newVersion = new DimCustomer(customerId, customerName, newCity, newState, newCountry, new Date());
        this.endDate = new Date();
        this.isCurrent = false;
        return newVersion;
    }
}
```

## 16.4 ETL for Data Warehousing

ETL (Extract, Transform, Load) processes are essential for populating data warehouses with clean, integrated data.

### ETL Process Steps:
- **Extract**: Pull data from source systems
- **Transform**: Clean, validate, and format data
- **Load**: Insert data into target warehouse
- **Validation**: Ensure data quality and integrity
- **Monitoring**: Track ETL process performance

### ETL Challenges:
- **Data Quality**: Inconsistent, incomplete, or invalid data
- **Data Volume**: Large amounts of data to process
- **Performance**: ETL processes can be time-consuming
- **Error Handling**: Managing failed records and retries
- **Scheduling**: Coordinating ETL jobs with source systems

### Real-World Analogy:
ETL is like a food processing plant:
- **Extract** = Harvesting raw ingredients
- **Transform** = Cleaning, cutting, and preparing ingredients
- **Load** = Packaging finished products
- **Validation** = Quality control checks
- **Monitoring** = Production line oversight

### Java Example - ETL Process:
```java
public class ETLProcessor {
    private DataExtractor extractor;
    private DataTransformer transformer;
    private DataLoader loader;
    private DataValidator validator;
    
    public ETLProcessor() {
        this.extractor = new DataExtractor();
        this.transformer = new DataTransformer();
        this.loader = new DataLoader();
        this.validator = new DataValidator();
    }
    
    // Main ETL process
    public void processETL(String sourceSystem, String targetTable) {
        try {
            // Extract data
            List<RawRecord> rawData = extractor.extract(sourceSystem);
            System.out.println("Extracted " + rawData.size() + " records from " + sourceSystem);
            
            // Transform data
            List<ProcessedRecord> processedData = transformer.transform(rawData);
            System.out.println("Transformed " + processedData.size() + " records");
            
            // Validate data
            List<ProcessedRecord> validData = validator.validate(processedData);
            System.out.println("Validated " + validData.size() + " records");
            
            // Load data
            loader.load(validData, targetTable);
            System.out.println("Loaded " + validData.size() + " records into " + targetTable);
            
        } catch (Exception e) {
            System.err.println("ETL process failed: " + e.getMessage());
            throw new RuntimeException("ETL process failed", e);
        }
    }
}

// Data extractor
class DataExtractor {
    public List<RawRecord> extract(String sourceSystem) {
        List<RawRecord> records = new ArrayList<>();
        
        // Simulate data extraction
        for (int i = 1; i <= 1000; i++) {
            records.add(new RawRecord(i, "Product" + i, "Category" + (i % 10), 
                                    new BigDecimal(10 + (i % 100))));
        }
        
        return records;
    }
}

// Data transformer
class DataTransformer {
    public List<ProcessedRecord> transform(List<RawRecord> rawData) {
        List<ProcessedRecord> processedData = new ArrayList<>();
        
        for (RawRecord raw : rawData) {
            // Clean and transform data
            String cleanName = raw.getName().trim().toUpperCase();
            String cleanCategory = raw.getCategory().trim().toUpperCase();
            BigDecimal cleanPrice = raw.getPrice().setScale(2, RoundingMode.HALF_UP);
            
            processedData.add(new ProcessedRecord(raw.getId(), cleanName, 
                                                cleanCategory, cleanPrice));
        }
        
        return processedData;
    }
}

// Data loader
class DataLoader {
    public void load(List<ProcessedRecord> data, String targetTable) {
        // Simulate data loading
        System.out.println("Loading data into " + targetTable);
        for (ProcessedRecord record : data) {
            // Insert record into target table
            System.out.println("Inserted: " + record);
        }
    }
}

// Data validator
class DataValidator {
    public List<ProcessedRecord> validate(List<ProcessedRecord> data) {
        List<ProcessedRecord> validData = new ArrayList<>();
        
        for (ProcessedRecord record : data) {
            if (isValid(record)) {
                validData.add(record);
            } else {
                System.out.println("Invalid record rejected: " + record);
            }
        }
        
        return validData;
    }
    
    private boolean isValid(ProcessedRecord record) {
        return record.getName() != null && !record.getName().isEmpty() &&
               record.getCategory() != null && !record.getCategory().isEmpty() &&
               record.getPrice().compareTo(BigDecimal.ZERO) > 0;
    }
}
```

## 16.5 Data Marts

Data marts are specialized subsets of a data warehouse designed for specific business functions or departments.

### Data Mart Types:
- **Dependent Data Marts**: Built from existing data warehouse
- **Independent Data Marts**: Built directly from source systems
- **Hybrid Data Marts**: Combination of both approaches

### Data Mart Benefits:
- **Focused Data**: Only relevant data for specific users
- **Faster Queries**: Smaller datasets for better performance
- **Easier Management**: Simpler to understand and maintain
- **Departmental Ownership**: Business units can own their data marts

### Real-World Analogy:
Data marts are like specialized sections in a library:
- **Dependent Data Marts** = Copies of books from main library
- **Independent Data Marts** = Separate collections for specific topics
- **Hybrid Data Marts** = Combination of both approaches

### Java Example - Data Mart Management:
```java
public class DataMartManager {
    private Map<String, DataMart> dataMarts = new HashMap<>();
    private DataWarehouse warehouse;
    
    public DataMartManager(DataWarehouse warehouse) {
        this.warehouse = warehouse;
    }
    
    // Create dependent data mart
    public void createDependentDataMart(String name, String[] tables, String[] filters) {
        DataMart mart = new DataMart(name, "dependent");
        
        for (String table : tables) {
            TableData data = warehouse.getTableData(table, filters);
            mart.addTable(table, data);
        }
        
        dataMarts.put(name, mart);
        System.out.println("Dependent data mart created: " + name);
    }
    
    // Create independent data mart
    public void createIndependentDataMart(String name, String[] sourceSystems) {
        DataMart mart = new DataMart(name, "independent");
        
        for (String source : sourceSystems) {
            TableData data = extractFromSource(source);
            mart.addTable(source, data);
        }
        
        dataMarts.put(name, mart);
        System.out.println("Independent data mart created: " + name);
    }
    
    // Query data mart
    public List<Record> queryDataMart(String martName, String query) {
        DataMart mart = dataMarts.get(martName);
        if (mart != null) {
            return mart.executeQuery(query);
        }
        return new ArrayList<>();
    }
    
    // Refresh dependent data mart
    public void refreshDataMart(String martName) {
        DataMart mart = dataMarts.get(martName);
        if (mart != null && "dependent".equals(mart.getType())) {
            // Refresh data from warehouse
            mart.refreshFromWarehouse(warehouse);
            System.out.println("Data mart refreshed: " + martName);
        }
    }
    
    private TableData extractFromSource(String source) {
        // Simulate data extraction from source system
        return new TableData();
    }
}

// Data mart class
class DataMart {
    private String name;
    private String type;
    private Map<String, TableData> tables = new HashMap<>();
    
    public DataMart(String name, String type) {
        this.name = name;
        this.type = type;
    }
    
    public void addTable(String tableName, TableData data) {
        tables.put(tableName, data);
    }
    
    public List<Record> executeQuery(String query) {
        // Simulate query execution
        return new ArrayList<>();
    }
    
    public void refreshFromWarehouse(DataWarehouse warehouse) {
        // Refresh data from warehouse
        System.out.println("Refreshing data from warehouse");
    }
    
    // Getters
    public String getName() { return name; }
    public String getType() { return type; }
}
```

## 16.6 OLAP vs OLTP

OLAP (Online Analytical Processing) and OLTP (Online Transaction Processing) serve different purposes in data management.

### OLTP Characteristics:
- **Transaction-Oriented**: Handles day-to-day business operations
- **Real-Time**: Immediate response to user requests
- **Normalized Data**: Optimized for data integrity
- **Small Transactions**: Quick, simple operations
- **High Concurrency**: Many users performing transactions

### OLAP Characteristics:
- **Analysis-Oriented**: Supports business intelligence and reporting
- **Batch Processing**: Processes large amounts of data
- **Denormalized Data**: Optimized for query performance
- **Complex Queries**: Aggregations and multi-dimensional analysis
- **Read-Heavy**: Primarily read operations

### Real-World Analogy:
- **OLTP** = Cash register at a store (quick transactions)
- **OLAP** = Financial analysis department (complex reports and analysis)

### Java Example - OLTP vs OLAP:
```java
// OLTP System - Transaction Processing
public class OLTPSystem {
    private Connection connection;
    
    public OLTPSystem(Connection connection) {
        this.connection = connection;
    }
    
    // Process a sale transaction
    public void processSale(int customerId, int productId, int quantity) {
        try {
            connection.setAutoCommit(false);
            
            // Check inventory
            if (checkInventory(productId, quantity)) {
                // Update inventory
                updateInventory(productId, quantity);
                
                // Create sale record
                createSaleRecord(customerId, productId, quantity);
                
                // Update customer account
                updateCustomerAccount(customerId, productId, quantity);
                
                connection.commit();
                System.out.println("Sale processed successfully");
            } else {
                connection.rollback();
                System.out.println("Insufficient inventory");
            }
        } catch (SQLException e) {
            try {
                connection.rollback();
            } catch (SQLException ex) {
                ex.printStackTrace();
            }
            throw new RuntimeException("Transaction failed", e);
        }
    }
    
    private boolean checkInventory(int productId, int quantity) throws SQLException {
        String sql = "SELECT stock_quantity FROM inventory WHERE product_id = ?";
        try (PreparedStatement stmt = connection.prepareStatement(sql)) {
            stmt.setInt(1, productId);
            try (ResultSet rs = stmt.executeQuery()) {
                if (rs.next()) {
                    return rs.getInt("stock_quantity") >= quantity;
                }
            }
        }
        return false;
    }
    
    private void updateInventory(int productId, int quantity) throws SQLException {
        String sql = "UPDATE inventory SET stock_quantity = stock_quantity - ? WHERE product_id = ?";
        try (PreparedStatement stmt = connection.prepareStatement(sql)) {
            stmt.setInt(1, quantity);
            stmt.setInt(2, productId);
            stmt.executeUpdate();
        }
    }
    
    private void createSaleRecord(int customerId, int productId, int quantity) throws SQLException {
        String sql = "INSERT INTO sales (customer_id, product_id, quantity, sale_date) VALUES (?, ?, ?, NOW())";
        try (PreparedStatement stmt = connection.prepareStatement(sql)) {
            stmt.setInt(1, customerId);
            stmt.setInt(2, productId);
            stmt.setInt(3, quantity);
            stmt.executeUpdate();
        }
    }
    
    private void updateCustomerAccount(int customerId, int productId, int quantity) throws SQLException {
        String sql = "UPDATE customer_accounts SET total_purchases = total_purchases + ? WHERE customer_id = ?";
        try (PreparedStatement stmt = connection.prepareStatement(sql)) {
            stmt.setInt(1, quantity);
            stmt.setInt(2, customerId);
            stmt.executeUpdate();
        }
    }
}

// OLAP System - Analytical Processing
public class OLAPSystem {
    private Connection connection;
    
    public OLAPSystem(Connection connection) {
        this.connection = connection;
    }
    
    // Generate sales report by product category
    public SalesReport generateSalesReportByCategory(String startDate, String endDate) {
        String sql = """
            SELECT 
                p.category,
                COUNT(s.sale_id) as total_sales,
                SUM(s.quantity) as total_quantity,
                SUM(s.quantity * p.price) as total_revenue,
                AVG(s.quantity * p.price) as average_sale_value
            FROM sales s
            JOIN products p ON s.product_id = p.product_id
            WHERE s.sale_date BETWEEN ? AND ?
            GROUP BY p.category
            ORDER BY total_revenue DESC
            """;
        
        try (PreparedStatement stmt = connection.prepareStatement(sql)) {
            stmt.setString(1, startDate);
            stmt.setString(2, endDate);
            
            try (ResultSet rs = stmt.executeQuery()) {
                SalesReport report = new SalesReport();
                while (rs.next()) {
                    CategorySales categorySales = new CategorySales(
                        rs.getString("category"),
                        rs.getInt("total_sales"),
                        rs.getInt("total_quantity"),
                        rs.getBigDecimal("total_revenue"),
                        rs.getBigDecimal("average_sale_value")
                    );
                    report.addCategorySales(categorySales);
                }
                return report;
            }
        } catch (SQLException e) {
            throw new RuntimeException("Failed to generate sales report", e);
        }
    }
    
    // Generate customer analysis
    public CustomerAnalysis generateCustomerAnalysis() {
        String sql = """
            SELECT 
                c.customer_id,
                c.customer_name,
                COUNT(s.sale_id) as total_purchases,
                SUM(s.quantity * p.price) as total_spent,
                AVG(s.quantity * p.price) as average_purchase,
                MAX(s.sale_date) as last_purchase_date
            FROM customers c
            LEFT JOIN sales s ON c.customer_id = s.customer_id
            LEFT JOIN products p ON s.product_id = p.product_id
            GROUP BY c.customer_id, c.customer_name
            ORDER BY total_spent DESC
            """;
        
        try (Statement stmt = connection.createStatement();
             ResultSet rs = stmt.executeQuery(sql)) {
            
            CustomerAnalysis analysis = new CustomerAnalysis();
            while (rs.next()) {
                CustomerMetrics metrics = new CustomerMetrics(
                    rs.getInt("customer_id"),
                    rs.getString("customer_name"),
                    rs.getInt("total_purchases"),
                    rs.getBigDecimal("total_spent"),
                    rs.getBigDecimal("average_purchase"),
                    rs.getDate("last_purchase_date")
                );
                analysis.addCustomerMetrics(metrics);
            }
            return analysis;
        } catch (SQLException e) {
            throw new RuntimeException("Failed to generate customer analysis", e);
        }
    }
}

// Report classes
class SalesReport {
    private List<CategorySales> categorySales = new ArrayList<>();
    
    public void addCategorySales(CategorySales categorySales) {
        this.categorySales.add(categorySales);
    }
    
    public List<CategorySales> getCategorySales() {
        return categorySales;
    }
}

class CategorySales {
    private String category;
    private int totalSales;
    private int totalQuantity;
    private BigDecimal totalRevenue;
    private BigDecimal averageSaleValue;
    
    public CategorySales(String category, int totalSales, int totalQuantity, 
                        BigDecimal totalRevenue, BigDecimal averageSaleValue) {
        this.category = category;
        this.totalSales = totalSales;
        this.totalQuantity = totalQuantity;
        this.totalRevenue = totalRevenue;
        this.averageSaleValue = averageSaleValue;
    }
    
    // Getters
    public String getCategory() { return category; }
    public int getTotalSales() { return totalSales; }
    public int getTotalQuantity() { return totalQuantity; }
    public BigDecimal getTotalRevenue() { return totalRevenue; }
    public BigDecimal getAverageSaleValue() { return averageSaleValue; }
}
```

## 16.7 Data Warehouse Design Patterns

Data warehouse design patterns provide proven approaches for organizing data in analytical systems.

### Common Design Patterns:
- **Kimball Methodology**: Bottom-up approach with dimensional modeling
- **Inmon Methodology**: Top-down approach with normalized data warehouse
- **Data Vault**: Hybrid approach with hubs, links, and satellites
- **Anchor Modeling**: Sixth normal form approach
- **Data Mesh**: Decentralized data architecture

### Pattern Selection Criteria:
- **Data Volume**: Amount of data to be stored
- **Query Patterns**: Types of analytical queries
- **Data Quality**: Source data quality and consistency
- **Performance Requirements**: Query response time needs
- **Maintenance Complexity**: Ongoing maintenance effort

### Real-World Analogy:
Data warehouse design patterns are like architectural blueprints:
- **Kimball** = Modular building approach
- **Inmon** = Centralized building approach
- **Data Vault** = Flexible building approach
- **Anchor Modeling** = Highly normalized approach
- **Data Mesh** = Distributed building approach

### Java Example - Data Warehouse Design Patterns:
```java
// Kimball Methodology - Dimensional Modeling
public class KimballDataWarehouse {
    private Map<String, FactTable> factTables = new HashMap<>();
    private Map<String, DimensionTable> dimensionTables = new HashMap<>();
    
    public void createDimensionalModel() {
        // Create dimension tables
        createDimensionTable("dim_product", new String[]{"product_id", "product_name", "category", "brand"});
        createDimensionTable("dim_customer", new String[]{"customer_id", "customer_name", "city", "state"});
        createDimensionTable("dim_date", new String[]{"date_id", "full_date", "year", "quarter", "month"});
        
        // Create fact table
        createFactTable("fact_sales", new String[]{"sale_id", "product_id", "customer_id", "date_id", "quantity", "amount"});
        
        System.out.println("Kimball dimensional model created");
    }
    
    private void createDimensionTable(String name, String[] columns) {
        DimensionTable table = new DimensionTable(name, columns);
        dimensionTables.put(name, table);
    }
    
    private void createFactTable(String name, String[] columns) {
        FactTable table = new FactTable(name, columns);
        factTables.put(name, table);
    }
}

// Inmon Methodology - Normalized Data Warehouse
public class InmonDataWarehouse {
    private Map<String, NormalizedTable> tables = new HashMap<>();
    
    public void createNormalizedModel() {
        // Create normalized tables
        createTable("products", new String[]{"product_id", "product_name", "category_id", "brand_id"});
        createTable("categories", new String[]{"category_id", "category_name", "department_id"});
        createTable("departments", new String[]{"department_id", "department_name"});
        createTable("brands", new String[]{"brand_id", "brand_name", "manufacturer_id"});
        createTable("manufacturers", new String[]{"manufacturer_id", "manufacturer_name"});
        
        System.out.println("Inmon normalized model created");
    }
    
    private void createTable(String name, String[] columns) {
        NormalizedTable table = new NormalizedTable(name, columns);
        tables.put(name, table);
    }
}

// Data Vault Methodology
public class DataVaultWarehouse {
    private Map<String, Hub> hubs = new HashMap<>();
    private Map<String, Link> links = new HashMap<>();
    private Map<String, Satellite> satellites = new HashMap<>();
    
    public void createDataVaultModel() {
        // Create hubs (business keys)
        createHub("hub_product", "product_id");
        createHub("hub_customer", "customer_id");
        createHub("hub_sale", "sale_id");
        
        // Create links (relationships)
        createLink("link_product_sale", new String[]{"product_id", "sale_id"});
        createLink("link_customer_sale", new String[]{"customer_id", "sale_id"});
        
        // Create satellites (descriptive data)
        createSatellite("sat_product", "product_id", new String[]{"product_name", "category", "brand"});
        createSatellite("sat_customer", "customer_id", new String[]{"customer_name", "city", "state"});
        createSatellite("sat_sale", "sale_id", new String[]{"quantity", "amount", "sale_date"});
        
        System.out.println("Data Vault model created");
    }
    
    private void createHub(String name, String businessKey) {
        Hub hub = new Hub(name, businessKey);
        hubs.put(name, hub);
    }
    
    private void createLink(String name, String[] businessKeys) {
        Link link = new Link(name, businessKeys);
        links.put(name, link);
    }
    
    private void createSatellite(String name, String parentKey, String[] attributes) {
        Satellite satellite = new Satellite(name, parentKey, attributes);
        satellites.put(name, satellite);
    }
}

// Table classes
class DimensionTable {
    private String name;
    private String[] columns;
    
    public DimensionTable(String name, String[] columns) {
        this.name = name;
        this.columns = columns;
    }
}

class FactTable {
    private String name;
    private String[] columns;
    
    public FactTable(String name, String[] columns) {
        this.name = name;
        this.columns = columns;
    }
}

class NormalizedTable {
    private String name;
    private String[] columns;
    
    public NormalizedTable(String name, String[] columns) {
        this.name = name;
        this.columns = columns;
    }
}

class Hub {
    private String name;
    private String businessKey;
    
    public Hub(String name, String businessKey) {
        this.name = name;
        this.businessKey = businessKey;
    }
}

class Link {
    private String name;
    private String[] businessKeys;
    
    public Link(String name, String[] businessKeys) {
        this.name = name;
        this.businessKeys = businessKeys;
    }
}

class Satellite {
    private String name;
    private String parentKey;
    private String[] attributes;
    
    public Satellite(String name, String parentKey, String[] attributes) {
        this.name = name;
        this.parentKey = parentKey;
        this.attributes = attributes;
    }
}
```

## 16.8 Modern Data Warehousing

Modern data warehousing incorporates cloud technologies, real-time processing, and advanced analytics capabilities.

### Modern Data Warehouse Features:
- **Cloud-Native**: Built for cloud environments
- **Real-Time Processing**: Stream processing capabilities
- **Machine Learning Integration**: Built-in ML capabilities
- **Serverless Architecture**: Automatic scaling and management
- **Multi-Cloud Support**: Works across different cloud providers
- **Data Lake Integration**: Combines structured and unstructured data

### Modern Technologies:
- **Snowflake**: Cloud data warehouse platform
- **BigQuery**: Google's serverless data warehouse
- **Redshift**: Amazon's cloud data warehouse
- **Synapse**: Microsoft's analytics platform
- **Databricks**: Unified analytics platform

### Real-World Analogy:
Modern data warehousing is like a smart city:
- **Cloud-Native** = Connected infrastructure
- **Real-Time Processing** = Live traffic monitoring
- **Machine Learning** = Smart city AI
- **Serverless** = Automatic resource management
- **Multi-Cloud** = Multiple service providers
- **Data Lake Integration** = Unified data management

### Java Example - Modern Data Warehouse:
```java
public class ModernDataWarehouse {
    private CloudDataWarehouse cloudWarehouse;
    private StreamProcessor streamProcessor;
    private MLProcessor mlProcessor;
    private DataLakeConnector dataLakeConnector;
    
    public ModernDataWarehouse() {
        this.cloudWarehouse = new CloudDataWarehouse();
        this.streamProcessor = new StreamProcessor();
        this.mlProcessor = new MLProcessor();
        this.dataLakeConnector = new DataLakeConnector();
    }
    
    // Real-time data ingestion
    public void ingestRealTimeData(StreamData data) {
        // Process streaming data
        ProcessedData processed = streamProcessor.process(data);
        
        // Store in cloud warehouse
        cloudWarehouse.store(processed);
        
        // Trigger ML analysis
        mlProcessor.analyze(processed);
        
        System.out.println("Real-time data ingested and processed");
    }
    
    // Batch data processing
    public void processBatchData(String sourcePath) {
        // Extract data from source
        List<RawData> rawData = extractFromSource(sourcePath);
        
        // Transform data
        List<ProcessedData> processedData = transformData(rawData);
        
        // Load into warehouse
        cloudWarehouse.batchLoad(processedData);
        
        System.out.println("Batch data processed: " + processedData.size() + " records");
    }
    
    // ML-powered analytics
    public MLInsights generateMLInsights(String query) {
        // Query data from warehouse
        List<DataRecord> data = cloudWarehouse.query(query);
        
        // Apply ML models
        MLInsights insights = mlProcessor.generateInsights(data);
        
        return insights;
    }
    
    // Data lake integration
    public void integrateDataLake(String lakePath) {
        // Connect to data lake
        List<UnstructuredData> lakeData = dataLakeConnector.extract(lakePath);
        
        // Process unstructured data
        List<StructuredData> structuredData = processUnstructuredData(lakeData);
        
        // Store in warehouse
        cloudWarehouse.store(structuredData);
        
        System.out.println("Data lake integrated: " + structuredData.size() + " records");
    }
    
    // Auto-scaling
    public void autoScale() {
        // Monitor performance
        PerformanceMetrics metrics = cloudWarehouse.getPerformanceMetrics();
        
        if (metrics.getCpuUsage() > 80) {
            cloudWarehouse.scaleUp();
            System.out.println("Scaling up due to high CPU usage");
        } else if (metrics.getCpuUsage() < 20) {
            cloudWarehouse.scaleDown();
            System.out.println("Scaling down due to low CPU usage");
        }
    }
    
    private List<RawData> extractFromSource(String sourcePath) {
        // Simulate data extraction
        return new ArrayList<>();
    }
    
    private List<ProcessedData> transformData(List<RawData> rawData) {
        // Simulate data transformation
        return new ArrayList<>();
    }
    
    private List<StructuredData> processUnstructuredData(List<UnstructuredData> lakeData) {
        // Simulate unstructured data processing
        return new ArrayList<>();
    }
}

// Cloud data warehouse
class CloudDataWarehouse {
    public void store(ProcessedData data) {
        // Store data in cloud warehouse
        System.out.println("Data stored in cloud warehouse");
    }
    
    public void batchLoad(List<ProcessedData> data) {
        // Batch load data
        System.out.println("Batch loaded " + data.size() + " records");
    }
    
    public List<DataRecord> query(String query) {
        // Execute query
        return new ArrayList<>();
    }
    
    public PerformanceMetrics getPerformanceMetrics() {
        // Get performance metrics
        return new PerformanceMetrics();
    }
    
    public void scaleUp() {
        System.out.println("Scaling up warehouse");
    }
    
    public void scaleDown() {
        System.out.println("Scaling down warehouse");
    }
}

// Stream processor
class StreamProcessor {
    public ProcessedData process(StreamData data) {
        // Process streaming data
        return new ProcessedData();
    }
}

// ML processor
class MLProcessor {
    public void analyze(ProcessedData data) {
        // Perform ML analysis
        System.out.println("ML analysis completed");
    }
    
    public MLInsights generateInsights(List<DataRecord> data) {
        // Generate ML insights
        return new MLInsights();
    }
}

// Data lake connector
class DataLakeConnector {
    public List<UnstructuredData> extract(String lakePath) {
        // Extract data from data lake
        return new ArrayList<>();
    }
}

// Data classes
class StreamData {}
class ProcessedData {}
class RawData {}
class UnstructuredData {}
class StructuredData {}
class DataRecord {}
class MLInsights {}
class PerformanceMetrics {
    public double getCpuUsage() {
        return Math.random() * 100;
    }
}
```