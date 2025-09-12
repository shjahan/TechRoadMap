# Section 4 – Database Design and Modeling

## 4.1 Conceptual Data Modeling

Conceptual data modeling is the first phase of database design, focusing on identifying and defining the main entities, attributes, and relationships in a high-level, technology-independent manner.

### Key Concepts:
- **Entity**: A person, place, thing, or concept about which data is collected
- **Attribute**: A property or characteristic of an entity
- **Relationship**: An association between entities
- **Business Rules**: Constraints and requirements that govern data

### Modeling Process:
1. **Identify Entities**: Find the main objects in the business domain
2. **Define Attributes**: Determine properties for each entity
3. **Establish Relationships**: Connect entities based on business rules
4. **Apply Constraints**: Define rules and limitations
5. **Validate Model**: Ensure completeness and accuracy

### Real-World Analogy:
Conceptual modeling is like creating a blueprint for a building:
- **Entities** = Rooms (Kitchen, Bedroom, Living Room)
- **Attributes** = Room properties (Size, Color, Function)
- **Relationships** = How rooms connect (Kitchen connects to Dining Room)
- **Business Rules** = Building codes and regulations

### Java Example - Conceptual Model:
```java
// Conceptual model for a university system
public class ConceptualModel {
    
    // Entity: Student
    public static class Student {
        private String studentId;
        private String firstName;
        private String lastName;
        private String email;
        private LocalDate dateOfBirth;
        private String major;
        private BigDecimal gpa;
        
        // Relationships
        private Set<Course> enrolledCourses;
        private Department department;
        private List<Enrollment> enrollments;
    }
    
    // Entity: Course
    public static class Course {
        private String courseId;
        private String courseName;
        private String description;
        private Integer credits;
        private String department;
        
        // Relationships
        private Set<Student> enrolledStudents;
        private Instructor instructor;
        private List<Enrollment> enrollments;
    }
    
    // Entity: Instructor
    public static class Instructor {
        private String instructorId;
        private String firstName;
        private String lastName;
        private String email;
        private String department;
        private String title;
        
        // Relationships
        private Set<Course> taughtCourses;
        private Department department;
    }
    
    // Entity: Department
    public static class Department {
        private String departmentId;
        private String departmentName;
        private String description;
        private String location;
        
        // Relationships
        private Set<Student> students;
        private Set<Instructor> instructors;
        private Set<Course> courses;
    }
    
    // Relationship: Enrollment
    public static class Enrollment {
        private String studentId;
        private String courseId;
        private LocalDate enrollmentDate;
        private String grade;
        private String semester;
        
        // Navigation properties
        private Student student;
        private Course course;
    }
}
```

## 4.2 Logical Data Modeling

Logical data modeling translates the conceptual model into a detailed, technology-independent design that specifies tables, columns, data types, and relationships.

### Key Components:
- **Tables**: Represent entities with specific structure
- **Columns**: Represent attributes with data types
- **Primary Keys**: Unique identifiers for each table
- **Foreign Keys**: References between tables
- **Constraints**: Rules and limitations on data

### Design Principles:
- **Normalization**: Eliminate redundancy and ensure data integrity
- **Referential Integrity**: Maintain consistency across relationships
- **Data Types**: Choose appropriate types for each attribute
- **Indexing**: Plan for performance optimization

### Real-World Analogy:
Logical modeling is like creating detailed architectural plans:
- **Tables** = Detailed room layouts
- **Columns** = Specific measurements and specifications
- **Keys** = Room numbers and addresses
- **Constraints** = Building regulations and safety codes

### Java Example - Logical Model:
```java
// Logical data model implementation
@Entity
@Table(name = "students")
public class Student {
    @Id
    @Column(name = "student_id", length = 10)
    private String studentId;
    
    @Column(name = "first_name", nullable = false, length = 50)
    private String firstName;
    
    @Column(name = "last_name", nullable = false, length = 50)
    private String lastName;
    
    @Column(name = "email", unique = true, length = 100)
    private String email;
    
    @Column(name = "date_of_birth")
    private LocalDate dateOfBirth;
    
    @Column(name = "major", length = 50)
    private String major;
    
    @Column(name = "gpa", precision = 3, scale = 2)
    private BigDecimal gpa;
    
    @Column(name = "enrollment_date")
    private LocalDate enrollmentDate;
    
    // Foreign key relationship
    @ManyToOne
    @JoinColumn(name = "department_id")
    private Department department;
    
    // One-to-many relationships
    @OneToMany(mappedBy = "student", cascade = CascadeType.ALL)
    private List<Enrollment> enrollments = new ArrayList<>();
    
    // Getters and setters...
}

@Entity
@Table(name = "courses")
public class Course {
    @Id
    @Column(name = "course_id", length = 10)
    private String courseId;
    
    @Column(name = "course_name", nullable = false, length = 100)
    private String courseName;
    
    @Column(name = "description", length = 500)
    private String description;
    
    @Column(name = "credits", nullable = false)
    private Integer credits;
    
    @Column(name = "prerequisites", length = 200)
    private String prerequisites;
    
    // Foreign key relationships
    @ManyToOne
    @JoinColumn(name = "department_id")
    private Department department;
    
    @ManyToOne
    @JoinColumn(name = "instructor_id")
    private Instructor instructor;
    
    // One-to-many relationships
    @OneToMany(mappedBy = "course", cascade = CascadeType.ALL)
    private List<Enrollment> enrollments = new ArrayList<>();
    
    // Getters and setters...
}

@Entity
@Table(name = "departments")
public class Department {
    @Id
    @Column(name = "department_id", length = 10)
    private String departmentId;
    
    @Column(name = "department_name", nullable = false, unique = true, length = 100)
    private String departmentName;
    
    @Column(name = "description", length = 500)
    private String description;
    
    @Column(name = "location", length = 100)
    private String location;
    
    @Column(name = "budget", precision = 15, scale = 2)
    private BigDecimal budget;
    
    // One-to-many relationships
    @OneToMany(mappedBy = "department", cascade = CascadeType.ALL)
    private List<Student> students = new ArrayList<>();
    
    @OneToMany(mappedBy = "department", cascade = CascadeType.ALL)
    private List<Instructor> instructors = new ArrayList<>();
    
    @OneToMany(mappedBy = "department", cascade = CascadeType.ALL)
    private List<Course> courses = new ArrayList<>();
    
    // Getters and setters...
}

// Junction table for many-to-many relationship
@Entity
@Table(name = "enrollments")
@IdClass(EnrollmentId.class)
public class Enrollment {
    @Id
    @Column(name = "student_id", length = 10)
    private String studentId;
    
    @Id
    @Column(name = "course_id", length = 10)
    private String courseId;
    
    @Column(name = "enrollment_date", nullable = false)
    private LocalDate enrollmentDate;
    
    @Column(name = "grade", length = 2)
    private String grade;
    
    @Column(name = "semester", length = 20)
    private String semester;
    
    @Column(name = "credits_earned")
    private Integer creditsEarned;
    
    // Foreign key relationships
    @ManyToOne
    @JoinColumn(name = "student_id", insertable = false, updatable = false)
    private Student student;
    
    @ManyToOne
    @JoinColumn(name = "course_id", insertable = false, updatable = false)
    private Course course;
    
    // Getters and setters...
}

// Composite primary key for enrollment
@Embeddable
public class EnrollmentId implements Serializable {
    private String studentId;
    private String courseId;
    
    // Constructors, equals, hashCode...
}
```

## 4.3 Physical Data Modeling

Physical data modeling translates the logical model into a database-specific implementation, considering storage, performance, and platform-specific features.

### Key Considerations:
- **Storage Engine**: Choose appropriate storage mechanism
- **Indexing Strategy**: Plan indexes for performance
- **Partitioning**: Divide large tables for better performance
- **Data Types**: Select optimal database-specific types
- **Constraints**: Implement database-level constraints

### Performance Optimization:
- **Index Design**: Create indexes on frequently queried columns
- **Partitioning**: Split large tables by date, range, or hash
- **Clustering**: Organize data physically for better access
- **Compression**: Reduce storage space and improve I/O

### Real-World Analogy:
Physical modeling is like building the actual structure:
- **Storage Engine** = Foundation type (concrete, steel, wood)
- **Indexes** = Elevators and stairs for quick access
- **Partitioning** = Dividing large buildings into wings
- **Constraints** = Load-bearing walls and safety systems

### Java Example - Physical Model:
```java
// Physical data model with performance optimizations
@Entity
@Table(name = "students", 
       indexes = {
           @Index(name = "idx_students_email", columnList = "email"),
           @Index(name = "idx_students_department", columnList = "department_id"),
           @Index(name = "idx_students_gpa", columnList = "gpa"),
           @Index(name = "idx_students_name", columnList = "last_name, first_name")
       })
public class Student {
    @Id
    @Column(name = "student_id", length = 10)
    private String studentId;
    
    @Column(name = "first_name", nullable = false, length = 50)
    private String firstName;
    
    @Column(name = "last_name", nullable = false, length = 50)
    private String lastName;
    
    @Column(name = "email", unique = true, length = 100)
    private String email;
    
    @Column(name = "date_of_birth")
    private LocalDate dateOfBirth;
    
    @Column(name = "major", length = 50)
    private String major;
    
    @Column(name = "gpa", precision = 3, scale = 2)
    private BigDecimal gpa;
    
    @Column(name = "enrollment_date")
    private LocalDate enrollmentDate;
    
    @Column(name = "status", length = 20, nullable = false)
    private String status = "ACTIVE";
    
    @Column(name = "created_at", nullable = false)
    private LocalDateTime createdAt = LocalDateTime.now();
    
    @Column(name = "updated_at")
    private LocalDateTime updatedAt;
    
    // Foreign key relationship
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "department_id")
    private Department department;
    
    // One-to-many relationships with lazy loading
    @OneToMany(mappedBy = "student", cascade = CascadeType.ALL, fetch = FetchType.LAZY)
    private List<Enrollment> enrollments = new ArrayList<>();
    
    // Audit fields
    @PreUpdate
    public void preUpdate() {
        this.updatedAt = LocalDateTime.now();
    }
    
    // Getters and setters...
}

// Partitioned table for large datasets
@Entity
@Table(name = "student_activities")
public class StudentActivity {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @Column(name = "student_id", length = 10, nullable = false)
    private String studentId;
    
    @Column(name = "activity_type", length = 50, nullable = false)
    private String activityType;
    
    @Column(name = "activity_date", nullable = false)
    private LocalDate activityDate;
    
    @Column(name = "description", length = 500)
    private String description;
    
    @Column(name = "ip_address", length = 45)
    private String ipAddress;
    
    @Column(name = "user_agent", length = 500)
    private String userAgent;
    
    // Partitioning by date
    @Column(name = "partition_key")
    private String partitionKey;
    
    @PrePersist
    public void prePersist() {
        this.partitionKey = activityDate.format(DateTimeFormatter.ofPattern("yyyy-MM"));
    }
    
    // Getters and setters...
}

// Materialized view for reporting
@Entity
@Table(name = "student_summary_mv")
public class StudentSummary {
    @Id
    @Column(name = "student_id", length = 10)
    private String studentId;
    
    @Column(name = "full_name", length = 101)
    private String fullName;
    
    @Column(name = "department_name", length = 100)
    private String departmentName;
    
    @Column(name = "total_credits")
    private Integer totalCredits;
    
    @Column(name = "completed_credits")
    private Integer completedCredits;
    
    @Column(name = "current_gpa", precision = 3, scale = 2)
    private BigDecimal currentGpa;
    
    @Column(name = "enrollment_count")
    private Integer enrollmentCount;
    
    @Column(name = "last_activity_date")
    private LocalDate lastActivityDate;
    
    // Getters and setters...
}
```

## 4.4 Data Modeling Tools

Data modeling tools help designers create, visualize, and manage database schemas through graphical interfaces and automated code generation.

### Popular Tools:
- **ER/Studio**: Enterprise-grade data modeling
- **PowerDesigner**: Comprehensive modeling suite
- **MySQL Workbench**: Free tool for MySQL
- **pgAdmin**: PostgreSQL administration tool
- **Oracle SQL Developer**: Oracle's modeling tool

### Key Features:
- **Visual Design**: Drag-and-drop interface for creating models
- **Code Generation**: Automatic DDL script generation
- **Reverse Engineering**: Create models from existing databases
- **Version Control**: Track changes and collaborate
- **Documentation**: Generate comprehensive documentation

### Real-World Analogy:
Data modeling tools are like CAD software for architects:
- **Visual Design** = Drawing blueprints on computer
- **Code Generation** = Automatic construction instructions
- **Reverse Engineering** = Creating blueprints from existing building
- **Version Control** = Tracking design changes over time

### Java Example - Tool Integration:
```java
// Configuration for data modeling tools
@Configuration
public class DataModelingConfig {
    
    @Value("${database.url}")
    private String databaseUrl;
    
    @Value("${database.username}")
    private String username;
    
    @Value("${database.password}")
    private String password;
    
    @Bean
    public DataSource dataSource() {
        HikariConfig config = new HikariConfig();
        config.setJdbcUrl(databaseUrl);
        config.setUsername(username);
        config.setPassword(password);
        config.setMaximumPoolSize(10);
        return new HikariDataSource(config);
    }
    
    @Bean
    public JdbcTemplate jdbcTemplate(DataSource dataSource) {
        return new JdbcTemplate(dataSource);
    }
}

// Service for generating DDL from models
@Service
public class DDLGenerationService {
    
    @Autowired
    private JdbcTemplate jdbcTemplate;
    
    public String generateCreateTableDDL(String tableName) {
        String sql = """
            SELECT 
                COLUMN_NAME,
                DATA_TYPE,
                CHARACTER_MAXIMUM_LENGTH,
                IS_NULLABLE,
                COLUMN_DEFAULT,
                COLUMN_KEY,
                EXTRA
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_NAME = ? AND TABLE_SCHEMA = DATABASE()
            ORDER BY ORDINAL_POSITION
            """;
        
        List<Map<String, Object>> columns = jdbcTemplate.queryForList(sql, tableName);
        
        StringBuilder ddl = new StringBuilder();
        ddl.append("CREATE TABLE ").append(tableName).append(" (\n");
        
        for (int i = 0; i < columns.size(); i++) {
            Map<String, Object> column = columns.get(i);
            ddl.append("  ").append(column.get("COLUMN_NAME"));
            ddl.append(" ").append(column.get("DATA_TYPE"));
            
            if (column.get("CHARACTER_MAXIMUM_LENGTH") != null) {
                ddl.append("(").append(column.get("CHARACTER_MAXIMUM_LENGTH")).append(")");
            }
            
            if ("NO".equals(column.get("IS_NULLABLE"))) {
                ddl.append(" NOT NULL");
            }
            
            if (column.get("COLUMN_DEFAULT") != null) {
                ddl.append(" DEFAULT ").append(column.get("COLUMN_DEFAULT"));
            }
            
            if ("PRI".equals(column.get("COLUMN_KEY"))) {
                ddl.append(" PRIMARY KEY");
            }
            
            if ("auto_increment".equals(column.get("EXTRA"))) {
                ddl.append(" AUTO_INCREMENT");
            }
            
            if (i < columns.size() - 1) {
                ddl.append(",");
            }
            ddl.append("\n");
        }
        
        ddl.append(");");
        return ddl.toString();
    }
    
    public void generateIndexDDL(String tableName) {
        String sql = """
            SELECT 
                INDEX_NAME,
                COLUMN_NAME,
                NON_UNIQUE
            FROM INFORMATION_SCHEMA.STATISTICS
            WHERE TABLE_NAME = ? AND TABLE_SCHEMA = DATABASE()
            ORDER BY INDEX_NAME, SEQ_IN_INDEX
            """;
        
        List<Map<String, Object>> indexes = jdbcTemplate.queryForList(sql, tableName);
        
        String currentIndex = null;
        StringBuilder indexDDL = new StringBuilder();
        
        for (Map<String, Object> index : indexes) {
            String indexName = (String) index.get("INDEX_NAME");
            String columnName = (String) index.get("COLUMN_NAME");
            boolean isUnique = ((Number) index.get("NON_UNIQUE")).intValue() == 0;
            
            if (!indexName.equals(currentIndex)) {
                if (currentIndex != null) {
                    indexDDL.append(";\n");
                }
                
                if (isUnique) {
                    indexDDL.append("CREATE UNIQUE INDEX ").append(indexName);
                } else {
                    indexDDL.append("CREATE INDEX ").append(indexName);
                }
                indexDDL.append(" ON ").append(tableName).append(" (");
                currentIndex = indexName;
            } else {
                indexDDL.append(", ");
            }
            
            indexDDL.append(columnName);
        }
        
        if (currentIndex != null) {
            indexDDL.append(");");
        }
        
        System.out.println("Index DDL for " + tableName + ":");
        System.out.println(indexDDL.toString());
    }
}
```

## 4.5 Dimensional Modeling

Dimensional modeling is a data modeling technique used in data warehousing that organizes data into fact tables and dimension tables for optimal query performance.

### Key Components:
- **Fact Tables**: Contain measurable, quantitative data (facts)
- **Dimension Tables**: Contain descriptive attributes (dimensions)
- **Star Schema**: Central fact table surrounded by dimension tables
- **Snowflake Schema**: Dimension tables with sub-dimensions

### Design Principles:
- **Grain**: Level of detail in the fact table
- **Conformed Dimensions**: Shared dimensions across fact tables
- **Slowly Changing Dimensions**: Handle historical data changes
- **Aggregate Tables**: Pre-calculated summaries for performance

### Real-World Analogy:
Dimensional modeling is like organizing a retail store:
- **Fact Table** = Sales transactions (what was sold, when, how much)
- **Dimension Tables** = Product catalog, customer info, store locations
- **Star Schema** = Central cash register with product, customer, and store info nearby
- **Snowflake Schema** = Detailed product categories and subcategories

### Java Example - Dimensional Model:
```java
// Fact table for sales data
@Entity
@Table(name = "sales_fact")
public class SalesFact {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    // Foreign keys to dimension tables
    @Column(name = "product_id", nullable = false)
    private Long productId;
    
    @Column(name = "customer_id", nullable = false)
    private Long customerId;
    
    @Column(name = "store_id", nullable = false)
    private Long storeId;
    
    @Column(name = "date_id", nullable = false)
    private Long dateId;
    
    // Measures (facts)
    @Column(name = "quantity", nullable = false)
    private Integer quantity;
    
    @Column(name = "unit_price", precision = 10, scale = 2, nullable = false)
    private BigDecimal unitPrice;
    
    @Column(name = "total_amount", precision = 12, scale = 2, nullable = false)
    private BigDecimal totalAmount;
    
    @Column(name = "discount_amount", precision = 10, scale = 2)
    private BigDecimal discountAmount;
    
    @Column(name = "tax_amount", precision = 10, scale = 2)
    private BigDecimal taxAmount;
    
    // Relationships to dimension tables
    @ManyToOne
    @JoinColumn(name = "product_id", insertable = false, updatable = false)
    private ProductDimension product;
    
    @ManyToOne
    @JoinColumn(name = "customer_id", insertable = false, updatable = false)
    private CustomerDimension customer;
    
    @ManyToOne
    @JoinColumn(name = "store_id", insertable = false, updatable = false)
    private StoreDimension store;
    
    @ManyToOne
    @JoinColumn(name = "date_id", insertable = false, updatable = false)
    private DateDimension date;
    
    // Getters and setters...
}

// Dimension table for products
@Entity
@Table(name = "product_dimension")
public class ProductDimension {
    @Id
    @Column(name = "product_id")
    private Long productId;
    
    @Column(name = "product_name", nullable = false, length = 200)
    private String productName;
    
    @Column(name = "product_code", length = 50)
    private String productCode;
    
    @Column(name = "category_id")
    private Long categoryId;
    
    @Column(name = "category_name", length = 100)
    private String categoryName;
    
    @Column(name = "subcategory_id")
    private Long subcategoryId;
    
    @Column(name = "subcategory_name", length = 100)
    private String subcategoryName;
    
    @Column(name = "brand", length = 100)
    private String brand;
    
    @Column(name = "color", length = 50)
    private String color;
    
    @Column(name = "size", length = 20)
    private String size;
    
    @Column(name = "weight", precision = 8, scale = 2)
    private BigDecimal weight;
    
    @Column(name = "is_active")
    private Boolean isActive = true;
    
    @Column(name = "created_date")
    private LocalDate createdDate;
    
    @Column(name = "modified_date")
    private LocalDate modifiedDate;
    
    // Getters and setters...
}

// Dimension table for customers
@Entity
@Table(name = "customer_dimension")
public class CustomerDimension {
    @Id
    @Column(name = "customer_id")
    private Long customerId;
    
    @Column(name = "customer_name", nullable = false, length = 200)
    private String customerName;
    
    @Column(name = "email", length = 100)
    private String email;
    
    @Column(name = "phone", length = 20)
    private String phone;
    
    @Column(name = "address", length = 500)
    private String address;
    
    @Column(name = "city", length = 100)
    private String city;
    
    @Column(name = "state", length = 50)
    private String state;
    
    @Column(name = "zip_code", length = 20)
    private String zipCode;
    
    @Column(name = "country", length = 50)
    private String country;
    
    @Column(name = "customer_segment", length = 50)
    private String customerSegment;
    
    @Column(name = "registration_date")
    private LocalDate registrationDate;
    
    @Column(name = "is_active")
    private Boolean isActive = true;
    
    // Getters and setters...
}

// Dimension table for dates
@Entity
@Table(name = "date_dimension")
public class DateDimension {
    @Id
    @Column(name = "date_id")
    private Long dateId;
    
    @Column(name = "date", nullable = false)
    private LocalDate date;
    
    @Column(name = "day_of_week", length = 10)
    private String dayOfWeek;
    
    @Column(name = "day_of_month")
    private Integer dayOfMonth;
    
    @Column(name = "month", length = 10)
    private String month;
    
    @Column(name = "month_number")
    private Integer monthNumber;
    
    @Column(name = "quarter")
    private Integer quarter;
    
    @Column(name = "year")
    private Integer year;
    
    @Column(name = "is_weekend")
    private Boolean isWeekend;
    
    @Column(name = "is_holiday")
    private Boolean isHoliday;
    
    @Column(name = "holiday_name", length = 100)
    private String holidayName;
    
    @Column(name = "fiscal_year")
    private Integer fiscalYear;
    
    @Column(name = "fiscal_quarter")
    private Integer fiscalQuarter;
    
    // Getters and setters...
}

// Service for dimensional queries
@Service
public class DimensionalQueryService {
    
    @Autowired
    private JdbcTemplate jdbcTemplate;
    
    public List<Map<String, Object>> getSalesByProduct(String startDate, String endDate) {
        String sql = """
            SELECT 
                p.product_name,
                p.category_name,
                p.brand,
                SUM(sf.quantity) as total_quantity,
                SUM(sf.total_amount) as total_sales,
                AVG(sf.unit_price) as avg_unit_price
            FROM sales_fact sf
            JOIN product_dimension p ON sf.product_id = p.product_id
            JOIN date_dimension d ON sf.date_id = d.date_id
            WHERE d.date BETWEEN ? AND ?
            GROUP BY p.product_id, p.product_name, p.category_name, p.brand
            ORDER BY total_sales DESC
            """;
        
        return jdbcTemplate.queryForList(sql, startDate, endDate);
    }
    
    public List<Map<String, Object>> getSalesByTimePeriod(String period) {
        String sql = """
            SELECT 
                d.year,
                d.quarter,
                d.month,
                COUNT(*) as transaction_count,
                SUM(sf.total_amount) as total_sales,
                AVG(sf.total_amount) as avg_transaction_value
            FROM sales_fact sf
            JOIN date_dimension d ON sf.date_id = d.date_id
            GROUP BY d.year, d.quarter, d.month
            ORDER BY d.year, d.quarter, d.month
            """;
        
        return jdbcTemplate.queryForList(sql);
    }
}
```

## 4.6 Data Warehouse Design

Data warehouse design focuses on creating a centralized repository optimized for analytical queries and business intelligence reporting.

### Key Principles:
- **Subject-Oriented**: Organized around business subjects
- **Integrated**: Data from multiple sources combined consistently
- **Time-Variant**: Historical data maintained over time
- **Non-Volatile**: Data doesn't change once loaded

### Architecture Components:
- **Staging Area**: Temporary storage for data transformation
- **Data Warehouse**: Central repository for integrated data
- **Data Marts**: Subject-specific subsets of the warehouse
- **ETL Processes**: Extract, Transform, Load operations

### Real-World Analogy:
Data warehouse design is like creating a central library system:
- **Staging Area** = Sorting room where books are organized
- **Data Warehouse** = Main library with all books
- **Data Marts** = Specialized sections (Science, History, Fiction)
- **ETL Processes** = Librarians organizing and cataloging books

### Java Example - Data Warehouse Design:
```java
// Data warehouse configuration
@Configuration
public class DataWarehouseConfig {
    
    @Bean
    @Primary
    @ConfigurationProperties("warehouse.datasource")
    public DataSource warehouseDataSource() {
        return DataSourceBuilder.create().build();
    }
    
    @Bean
    @ConfigurationProperties("staging.datasource")
    public DataSource stagingDataSource() {
        return DataSourceBuilder.create().build();
    }
}

// ETL service for data warehouse
@Service
public class DataWarehouseETLService {
    
    @Autowired
    @Qualifier("warehouseDataSource")
    private DataSource warehouseDataSource;
    
    @Autowired
    @Qualifier("stagingDataSource")
    private DataSource stagingDataSource;
    
    @Scheduled(cron = "0 0 2 * * ?") // Daily at 2 AM
    public void performDailyETL() {
        try {
            // Extract data from source systems
            extractDataFromSources();
            
            // Transform data
            transformData();
            
            // Load data into warehouse
            loadDataIntoWarehouse();
            
            // Update data marts
            updateDataMarts();
            
            System.out.println("Daily ETL process completed successfully");
        } catch (Exception e) {
            System.err.println("ETL process failed: " + e.getMessage());
            // Log error and send notification
        }
    }
    
    private void extractDataFromSources() {
        // Extract from operational systems
        extractFromCRM();
        extractFromERP();
        extractFromWebAnalytics();
    }
    
    private void transformData() {
        // Clean and standardize data
        cleanCustomerData();
        standardizeProductData();
        calculateDerivedMetrics();
    }
    
    private void loadDataIntoWarehouse() {
        // Load into fact and dimension tables
        loadFactTables();
        loadDimensionTables();
        updateAggregates();
    }
    
    private void updateDataMarts() {
        // Update subject-specific data marts
        updateSalesDataMart();
        updateCustomerDataMart();
        updateProductDataMart();
    }
}

// Data warehouse query service
@Service
public class DataWarehouseQueryService {
    
    @Autowired
    @Qualifier("warehouseDataSource")
    private DataSource warehouseDataSource;
    
    public List<Map<String, Object>> getSalesTrends(int months) {
        String sql = """
            SELECT 
                d.year,
                d.month,
                SUM(sf.total_amount) as total_sales,
                COUNT(DISTINCT sf.customer_id) as unique_customers,
                COUNT(*) as transaction_count
            FROM sales_fact sf
            JOIN date_dimension d ON sf.date_id = d.date_id
            WHERE d.date >= DATE_SUB(CURRENT_DATE, INTERVAL ? MONTH)
            GROUP BY d.year, d.month
            ORDER BY d.year, d.month
            """;
        
        JdbcTemplate jdbcTemplate = new JdbcTemplate(warehouseDataSource);
        return jdbcTemplate.queryForList(sql, months);
    }
    
    public List<Map<String, Object>> getTopProducts(int limit) {
        String sql = """
            SELECT 
                p.product_name,
                p.category_name,
                SUM(sf.total_amount) as total_sales,
                SUM(sf.quantity) as total_quantity,
                COUNT(DISTINCT sf.customer_id) as unique_customers
            FROM sales_fact sf
            JOIN product_dimension p ON sf.product_id = p.product_id
            GROUP BY p.product_id, p.product_name, p.category_name
            ORDER BY total_sales DESC
            LIMIT ?
            """;
        
        JdbcTemplate jdbcTemplate = new JdbcTemplate(warehouseDataSource);
        return jdbcTemplate.queryForList(sql, limit);
    }
}
```

## 4.7 Data Lake Design

Data lake design focuses on storing raw data in its native format, enabling flexible analytics and machine learning applications.

### Key Characteristics:
- **Schema-on-Read**: Data structure defined when queried
- **Raw Data Storage**: Data stored in original format
- **Scalable Storage**: Handle massive volumes of data
- **Multiple Formats**: Support various data types and formats

### Architecture Components:
- **Ingestion Layer**: Data collection and ingestion
- **Storage Layer**: Raw data storage (HDFS, S3, etc.)
- **Processing Layer**: Data processing and transformation
- **Analytics Layer**: Query and analysis tools

### Real-World Analogy:
Data lake design is like creating a natural lake ecosystem:
- **Ingestion Layer** = Rivers and streams feeding the lake
- **Storage Layer** = The lake itself holding all the water
- **Processing Layer** = Water treatment and filtration systems
- **Analytics Layer** = Scientists studying the lake's contents

### Java Example - Data Lake Design:
```java
// Data lake configuration
@Configuration
public class DataLakeConfig {
    
    @Value("${datalake.s3.bucket}")
    private String s3Bucket;
    
    @Value("${datalake.s3.region}")
    private String s3Region;
    
    @Bean
    public AmazonS3 s3Client() {
        return AmazonS3ClientBuilder.standard()
            .withRegion(s3Region)
            .build();
    }
    
    @Bean
    public S3Template s3Template(AmazonS3 s3Client) {
        return new S3Template(s3Client);
    }
}

// Data lake ingestion service
@Service
public class DataLakeIngestionService {
    
    @Autowired
    private S3Template s3Template;
    
    @Value("${datalake.s3.bucket}")
    private String bucketName;
    
    public void ingestData(String dataType, String source, Object data) {
        try {
            String key = generateDataKey(dataType, source);
            String jsonData = objectMapper.writeValueAsString(data);
            
            s3Template.putObject(bucketName, key, jsonData);
            
            // Update metadata
            updateDataCatalog(dataType, source, key);
            
            System.out.println("Data ingested successfully: " + key);
        } catch (Exception e) {
            System.err.println("Data ingestion failed: " + e.getMessage());
        }
    }
    
    private String generateDataKey(String dataType, String source) {
        LocalDateTime now = LocalDateTime.now();
        String timestamp = now.format(DateTimeFormatter.ofPattern("yyyy/MM/dd/HH"));
        return String.format("%s/%s/%s/%s.json", dataType, source, timestamp, UUID.randomUUID());
    }
    
    private void updateDataCatalog(String dataType, String source, String key) {
        // Update data catalog with metadata
        DataCatalogEntry entry = new DataCatalogEntry();
        entry.setDataType(dataType);
        entry.setSource(source);
        entry.setS3Key(key);
        entry.setIngestionTime(LocalDateTime.now());
        entry.setSize(calculateSize(key));
        
        dataCatalogRepository.save(entry);
    }
}

// Data lake query service
@Service
public class DataLakeQueryService {
    
    @Autowired
    private S3Template s3Template;
    
    @Autowired
    private ObjectMapper objectMapper;
    
    public <T> List<T> queryData(String dataType, String source, 
                                LocalDate startDate, LocalDate endDate, 
                                Class<T> clazz) {
        List<T> results = new ArrayList<>();
        
        // Generate S3 keys for the date range
        List<String> keys = generateKeysForDateRange(dataType, source, startDate, endDate);
        
        for (String key : keys) {
            try {
                String jsonData = s3Template.getObjectAsString(bucketName, key);
                T data = objectMapper.readValue(jsonData, clazz);
                results.add(data);
            } catch (Exception e) {
                System.err.println("Error reading data from " + key + ": " + e.getMessage());
            }
        }
        
        return results;
    }
    
    private List<String> generateKeysForDateRange(String dataType, String source, 
                                                 LocalDate startDate, LocalDate endDate) {
        List<String> keys = new ArrayList<>();
        LocalDate currentDate = startDate;
        
        while (!currentDate.isAfter(endDate)) {
            String datePrefix = currentDate.format(DateTimeFormatter.ofPattern("yyyy/MM/dd"));
            String keyPattern = dataType + "/" + source + "/" + datePrefix + "/";
            
            // List objects with this prefix
            List<S3ObjectSummary> objects = s3Template.listObjects(bucketName, keyPattern);
            for (S3ObjectSummary object : objects) {
                keys.add(object.getKey());
            }
            
            currentDate = currentDate.plusDays(1);
        }
        
        return keys;
    }
}
```

## 4.8 Data Vault Modeling

Data Vault modeling is a hybrid approach combining 3NF and dimensional modeling, designed for data warehousing with emphasis on auditability and scalability.

### Key Components:
- **Hubs**: Business keys and metadata
- **Links**: Relationships between business keys
- **Satellites**: Descriptive attributes and context
- **Raw Vault**: Unprocessed data storage
- **Business Vault**: Processed and cleaned data

### Design Principles:
- **Auditability**: Complete history of all changes
- **Scalability**: Handle large volumes of data
- **Flexibility**: Adapt to changing requirements
- **Performance**: Optimized for loading and querying

### Real-World Analogy:
Data Vault modeling is like creating a comprehensive filing system:
- **Hubs** = Master index of all entities
- **Links** = Cross-reference system between entities
- **Satellites** = Detailed folders for each entity
- **Raw Vault** = Archive of original documents
- **Business Vault** = Processed and organized information

### Java Example - Data Vault Model:
```java
// Hub table for customers
@Entity
@Table(name = "hub_customer")
public class HubCustomer {
    @Id
    @Column(name = "customer_hkey", length = 32)
    private String customerHkey; // Hash of business key
    
    @Column(name = "customer_id", length = 50, nullable = false)
    private String customerId; // Business key
    
    @Column(name = "load_date", nullable = false)
    private LocalDateTime loadDate;
    
    @Column(name = "record_source", length = 100, nullable = false)
    private String recordSource;
    
    // Getters and setters...
}

// Link table for customer-product relationships
@Entity
@Table(name = "link_customer_product")
public class LinkCustomerProduct {
    @Id
    @Column(name = "link_hkey", length = 32)
    private String linkHkey; // Hash of combined business keys
    
    @Column(name = "customer_hkey", length = 32, nullable = false)
    private String customerHkey;
    
    @Column(name = "product_hkey", length = 32, nullable = false)
    private String productHkey;
    
    @Column(name = "load_date", nullable = false)
    private LocalDateTime loadDate;
    
    @Column(name = "record_source", length = 100, nullable = false)
    private String recordSource;
    
    // Getters and setters...
}

// Satellite table for customer details
@Entity
@Table(name = "sat_customer_details")
public class SatCustomerDetails {
    @Id
    @Column(name = "customer_hkey", length = 32)
    private String customerHkey;
    
    @Id
    @Column(name = "load_date")
    private LocalDateTime loadDate;
    
    @Column(name = "customer_name", length = 200)
    private String customerName;
    
    @Column(name = "email", length = 100)
    private String email;
    
    @Column(name = "phone", length = 20)
    private String phone;
    
    @Column(name = "address", length = 500)
    private String address;
    
    @Column(name = "city", length = 100)
    private String city;
    
    @Column(name = "state", length = 50)
    private String state;
    
    @Column(name = "zip_code", length = 20)
    private String zipCode;
    
    @Column(name = "country", length = 50)
    private String country;
    
    @Column(name = "record_source", length = 100, nullable = false)
    private String recordSource;
    
    @Column(name = "hash_diff", length = 32)
    private String hashDiff; // Hash of all attributes
    
    // Getters and setters...
}

// Data Vault ETL service
@Service
public class DataVaultETLService {
    
    @Autowired
    private HubCustomerRepository hubCustomerRepository;
    
    @Autowired
    private SatCustomerDetailsRepository satCustomerDetailsRepository;
    
    public void processCustomerData(CustomerData customerData) {
        // Generate hash keys
        String customerHkey = generateHashKey(customerData.getCustomerId());
        String hashDiff = generateHashDiff(customerData);
        
        // Process hub
        processHubCustomer(customerHkey, customerData);
        
        // Process satellite
        processSatelliteCustomerDetails(customerHkey, customerData, hashDiff);
    }
    
    private void processHubCustomer(String customerHkey, CustomerData customerData) {
        Optional<HubCustomer> existingHub = hubCustomerRepository.findById(customerHkey);
        
        if (existingHub.isEmpty()) {
            HubCustomer hub = new HubCustomer();
            hub.setCustomerHkey(customerHkey);
            hub.setCustomerId(customerData.getCustomerId());
            hub.setLoadDate(LocalDateTime.now());
            hub.setRecordSource(customerData.getSource());
            
            hubCustomerRepository.save(hub);
        }
    }
    
    private void processSatelliteCustomerDetails(String customerHkey, 
                                               CustomerData customerData, 
                                               String hashDiff) {
        // Check if data has changed
        Optional<SatCustomerDetails> latestSat = satCustomerDetailsRepository
            .findTopByCustomerHkeyOrderByLoadDateDesc(customerHkey);
        
        if (latestSat.isEmpty() || !hashDiff.equals(latestSat.get().getHashDiff())) {
            SatCustomerDetails sat = new SatCustomerDetails();
            sat.setCustomerHkey(customerHkey);
            sat.setLoadDate(LocalDateTime.now());
            sat.setCustomerName(customerData.getCustomerName());
            sat.setEmail(customerData.getEmail());
            sat.setPhone(customerData.getPhone());
            sat.setAddress(customerData.getAddress());
            sat.setCity(customerData.getCity());
            sat.setState(customerData.getState());
            sat.setZipCode(customerData.getZipCode());
            sat.setCountry(customerData.getCountry());
            sat.setRecordSource(customerData.getSource());
            sat.setHashDiff(hashDiff);
            
            satCustomerDetailsRepository.save(sat);
        }
    }
    
    private String generateHashKey(String businessKey) {
        return DigestUtils.md5Hex(businessKey).toUpperCase();
    }
    
    private String generateHashDiff(CustomerData customerData) {
        String data = customerData.getCustomerName() + 
                     customerData.getEmail() + 
                     customerData.getPhone() + 
                     customerData.getAddress();
        return DigestUtils.md5Hex(data).toUpperCase();
    }
}
```