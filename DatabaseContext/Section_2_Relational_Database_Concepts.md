# Section 2 – Relational Database Concepts

## 2.1 Relational Model Fundamentals

The relational model is a mathematical approach to organizing data using tables (relations) where data is stored in rows (tuples) and columns (attributes). It was first proposed by Edgar F. Codd in 1970 and forms the foundation of modern database systems.

### Key Concepts:
- **Relation**: A table with rows and columns representing an entity
- **Tuple**: A single row in a table representing one instance of an entity
- **Attribute**: A column in a table representing a property of an entity
- **Domain**: The set of valid values for an attribute
- **Schema**: The structure of the database including tables and relationships

### Mathematical Foundation:
The relational model is based on set theory and predicate logic:
- **Set Theory**: Tables are sets of tuples
- **Predicate Logic**: Queries are logical expressions
- **Relational Algebra**: Operations on relations (select, project, join)

### Real-World Analogy:
Think of the relational model like a well-organized filing system:
- **File Cabinet** (Database): Contains multiple drawers
- **Drawer** (Table): Contains related documents
- **File Folder** (Row/Tuple): Contains information about one specific item
- **Label on Folder** (Attribute/Column): Describes what information is in the folder
- **Filing System Rules** (Schema): Defines how folders are organized and labeled

### Java Example - Relational Model Implementation:
```java
// Representing a relation (table) in Java
public class Student {
    // Attributes (columns)
    private int studentId;        // Primary key
    private String firstName;     // Attribute
    private String lastName;      // Attribute
    private String email;         // Attribute
    private String major;         // Attribute
    private double gpa;           // Attribute
    
    // Constructor
    public Student(int studentId, String firstName, String lastName, 
                   String email, String major, double gpa) {
        this.studentId = studentId;
        this.firstName = firstName;
        this.lastName = lastName;
        this.email = email;
        this.major = major;
        this.gpa = gpa;
    }
    
    // Getters and setters
    public int getStudentId() { return studentId; }
    public void setStudentId(int studentId) { this.studentId = studentId; }
    
    public String getFirstName() { return firstName; }
    public void setFirstName(String firstName) { this.firstName = firstName; }
    
    // Domain validation
    public void setGpa(double gpa) {
        if (gpa < 0.0 || gpa > 4.0) {
            throw new IllegalArgumentException("GPA must be between 0.0 and 4.0");
        }
        this.gpa = gpa;
    }
}

// Representing multiple relations
public class Course {
    private int courseId;
    private String courseName;
    private String department;
    private int credits;
    
    // Constructor and methods...
}

public class Enrollment {
    private int studentId;    // Foreign key to Student
    private int courseId;     // Foreign key to Course
    private String semester;
    private String grade;
    
    // Constructor and methods...
}
```

## 2.2 Tables, Rows, and Columns

Understanding the basic structure of relational databases is fundamental to working with data effectively.

### Table (Relation):
- **Definition**: A two-dimensional structure that stores data about a specific entity
- **Characteristics**: Has a fixed structure with defined columns
- **Purpose**: Organizes related data in a structured format
- **Example**: A "Students" table contains information about all students

### Rows (Tuples/Records):
- **Definition**: Individual entries in a table representing one instance of an entity
- **Characteristics**: Each row contains values for all columns
- **Uniqueness**: Each row should be unique (usually enforced by primary key)
- **Example**: One row represents one specific student

### Columns (Attributes/Fields):
- **Definition**: Vertical structures that represent specific properties of an entity
- **Characteristics**: Each column has a data type and constraints
- **Purpose**: Define what information is stored about each entity
- **Example**: "firstName", "lastName", "email" are columns in a Students table

### Real-World Analogy:
Think of a table like a spreadsheet or a form:

**Table** = A Blank Form Template:
- Has predefined fields (columns) for specific information
- Can be filled out multiple times (rows)
- Each form follows the same structure

**Row** = A Completed Form:
- Contains actual data filled in all the fields
- Represents one specific instance (one student, one product, etc.)
- All forms have the same fields but different values

**Column** = A Field on the Form:
- "Name" field, "Address" field, "Phone" field
- Each field has specific rules (text, numbers, etc.)
- Same field appears on every form

### Java Example - Table Structure:
```java
// Creating a table structure using annotations
@Entity
@Table(name = "students")
public class Student {
    
    // Column definitions
    @Id
    @Column(name = "student_id")
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer studentId;  // Primary key column
    
    @Column(name = "first_name", nullable = false, length = 50)
    private String firstName;   // Required column with max length
    
    @Column(name = "last_name", nullable = false, length = 50)
    private String lastName;    // Required column with max length
    
    @Column(name = "email", unique = true, length = 100)
    private String email;       // Unique column
    
    @Column(name = "date_of_birth")
    private LocalDate dateOfBirth;  // Date column
    
    @Column(name = "gpa", precision = 3, scale = 2)
    private BigDecimal gpa;     // Decimal column with precision
    
    @Column(name = "is_active")
    private Boolean isActive;   // Boolean column
    
    // Default constructor
    public Student() {}
    
    // Constructor with parameters
    public Student(String firstName, String lastName, String email) {
        this.firstName = firstName;
        this.lastName = lastName;
        this.email = email;
        this.isActive = true;
    }
    
    // Getters and setters
    public Integer getStudentId() { return studentId; }
    public void setStudentId(Integer studentId) { this.studentId = studentId; }
    
    public String getFirstName() { return firstName; }
    public void setFirstName(String firstName) { this.firstName = firstName; }
    
    // Business logic methods
    public String getFullName() {
        return firstName + " " + lastName;
    }
    
    public boolean isEligibleForHonors() {
        return gpa != null && gpa.compareTo(new BigDecimal("3.5")) >= 0;
    }
}

// Working with table data
public class StudentService {
    
    // Insert a new row
    public Student createStudent(String firstName, String lastName, String email) {
        Student student = new Student(firstName, lastName, email);
        return studentRepository.save(student);
    }
    
    // Retrieve a specific row
    public Student getStudentById(Integer studentId) {
        return studentRepository.findById(studentId)
            .orElseThrow(() -> new StudentNotFoundException("Student not found"));
    }
    
    // Retrieve multiple rows
    public List<Student> getAllStudents() {
        return studentRepository.findAll();
    }
    
    // Update a row
    public Student updateStudent(Integer studentId, String newEmail) {
        Student student = getStudentById(studentId);
        student.setEmail(newEmail);
        return studentRepository.save(student);
    }
    
    // Delete a row
    public void deleteStudent(Integer studentId) {
        studentRepository.deleteById(studentId);
    }
}
```

## 2.3 Primary Keys and Foreign Keys

Keys are fundamental to relational database design, enabling unique identification of records and establishing relationships between tables.

### Primary Key:
- **Definition**: A column or combination of columns that uniquely identifies each row in a table
- **Characteristics**: Must be unique, non-null, and immutable
- **Purpose**: Ensures each record can be uniquely identified
- **Types**: Natural keys (meaningful data) or surrogate keys (auto-generated)

### Foreign Key:
- **Definition**: A column or combination of columns that references the primary key of another table
- **Characteristics**: Must match the data type and values of the referenced primary key
- **Purpose**: Establishes relationships between tables and maintains referential integrity
- **Behavior**: Can be null (optional relationship) or not null (required relationship)

### Real-World Analogy:
Think of keys like identification systems:

**Primary Key** = Social Security Number:
- Each person has a unique SSN
- No two people can have the same SSN
- SSN never changes and is always present
- Used to uniquely identify a person

**Foreign Key** = Employee ID in a Department:
- References the employee's SSN (primary key)
- Links the employee to their department
- Can be null if employee is not assigned to a department
- Must be a valid SSN that exists in the employee table

### Java Example - Primary and Foreign Keys:
```java
// Parent table with Primary Key
@Entity
@Table(name = "departments")
public class Department {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "department_id")
    private Integer departmentId;  // Primary Key
    
    @Column(name = "department_name", nullable = false, unique = true)
    private String departmentName;
    
    @Column(name = "budget")
    private BigDecimal budget;
    
    // One-to-many relationship
    @OneToMany(mappedBy = "department", cascade = CascadeType.ALL)
    private List<Employee> employees;
    
    // Constructors, getters, setters...
}

// Child table with Foreign Key
@Entity
@Table(name = "employees")
public class Employee {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "employee_id")
    private Integer employeeId;  // Primary Key
    
    @Column(name = "first_name", nullable = false)
    private String firstName;
    
    @Column(name = "last_name", nullable = false)
    private String lastName;
    
    @Column(name = "email", unique = true)
    private String email;
    
    // Foreign Key
    @ManyToOne
    @JoinColumn(name = "department_id")
    private Department department;  // References Department.departmentId
    
    @Column(name = "salary")
    private BigDecimal salary;
    
    // Constructors, getters, setters...
}

// Composite Primary Key example
@Embeddable
public class OrderItemId implements Serializable {
    @Column(name = "order_id")
    private Integer orderId;
    
    @Column(name = "product_id")
    private Integer productId;
    
    // Constructors, equals, hashCode...
}

@Entity
@Table(name = "order_items")
@IdClass(OrderItemId.class)
public class OrderItem {
    @Id
    @Column(name = "order_id")
    private Integer orderId;  // Part of composite primary key
    
    @Id
    @Column(name = "product_id")
    private Integer productId;  // Part of composite primary key
    
    @Column(name = "quantity")
    private Integer quantity;
    
    @Column(name = "unit_price")
    private BigDecimal unitPrice;
    
    // Foreign keys
    @ManyToOne
    @JoinColumn(name = "order_id", insertable = false, updatable = false)
    private Order order;
    
    @ManyToOne
    @JoinColumn(name = "product_id", insertable = false, updatable = false)
    private Product product;
    
    // Constructors, getters, setters...
}
```

## 2.4 Relationships (One-to-One, One-to-Many, Many-to-Many)

Relationships define how entities are connected to each other in a relational database. Understanding relationship types is crucial for proper database design.

### One-to-One (1:1) Relationship:
- **Definition**: Each record in Table A relates to exactly one record in Table B, and vice versa
- **Characteristics**: Both tables have unique constraints on the foreign key
- **Examples**: Person ↔ Passport, User ↔ UserProfile
- **Implementation**: Foreign key in either table with unique constraint

### One-to-Many (1:M) Relationship:
- **Definition**: One record in Table A can relate to many records in Table B, but each record in Table B relates to only one record in Table A
- **Characteristics**: Most common relationship type
- **Examples**: Department → Employees, Customer → Orders, Author → Books
- **Implementation**: Foreign key in the "many" side table

### Many-to-Many (M:N) Relationship:
- **Definition**: Records in Table A can relate to many records in Table B, and records in Table B can relate to many records in Table A
- **Characteristics**: Requires a junction/bridge table
- **Examples**: Students ↔ Courses, Products ↔ Orders, Authors ↔ Books
- **Implementation**: Junction table with foreign keys to both tables

### Real-World Analogy:
Think of relationships like connections between people and organizations:

**One-to-One** = Person ↔ Social Security Number:
- Each person has exactly one SSN
- Each SSN belongs to exactly one person
- Like a unique ID card for each person

**One-to-Many** = Company → Employees:
- One company can have many employees
- Each employee works for only one company
- Like a company directory with many employees

**Many-to-Many** = Students ↔ Courses:
- One student can take many courses
- One course can have many students
- Like a class enrollment system

### Java Example - Relationship Implementation:
```java
// One-to-One Relationship
@Entity
@Table(name = "users")
public class User {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    private String username;
    private String email;
    
    // One-to-One relationship
    @OneToOne(mappedBy = "user", cascade = CascadeType.ALL)
    private UserProfile profile;
    
    // Getters and setters...
}

@Entity
@Table(name = "user_profiles")
public class UserProfile {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    private String firstName;
    private String lastName;
    private String bio;
    
    // One-to-One relationship
    @OneToOne
    @JoinColumn(name = "user_id")
    private User user;
    
    // Getters and setters...
}

// One-to-Many Relationship
@Entity
@Table(name = "categories")
public class Category {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    private String name;
    private String description;
    
    // One-to-Many relationship
    @OneToMany(mappedBy = "category", cascade = CascadeType.ALL, fetch = FetchType.LAZY)
    private List<Product> products = new ArrayList<>();
    
    // Getters and setters...
}

@Entity
@Table(name = "products")
public class Product {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    private String name;
    private BigDecimal price;
    
    // Many-to-One relationship
    @ManyToOne
    @JoinColumn(name = "category_id")
    private Category category;
    
    // Getters and setters...
}

// Many-to-Many Relationship
@Entity
@Table(name = "students")
public class Student {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    private String name;
    private String email;
    
    // Many-to-Many relationship
    @ManyToMany(cascade = {CascadeType.PERSIST, CascadeType.MERGE})
    @JoinTable(
        name = "student_courses",
        joinColumns = @JoinColumn(name = "student_id"),
        inverseJoinColumns = @JoinColumn(name = "course_id")
    )
    private Set<Course> courses = new HashSet<>();
    
    // Getters and setters...
}

@Entity
@Table(name = "courses")
public class Course {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    private String title;
    private String code;
    private Integer credits;
    
    // Many-to-Many relationship
    @ManyToMany(mappedBy = "courses")
    private Set<Student> students = new HashSet<>();
    
    // Getters and setters...
}

// Junction table for additional attributes
@Entity
@Table(name = "enrollments")
public class Enrollment {
    @EmbeddedId
    private EnrollmentId id;
    
    @ManyToOne
    @MapsId("studentId")
    @JoinColumn(name = "student_id")
    private Student student;
    
    @ManyToOne
    @MapsId("courseId")
    @JoinColumn(name = "course_id")
    private Course course;
    
    private LocalDate enrollmentDate;
    private String grade;
    private Integer semester;
    
    // Getters and setters...
}
```

## 2.5 Normalization (1NF, 2NF, 3NF, BCNF)

Normalization is the process of organizing data in a database to eliminate redundancy and improve data integrity. It involves applying a series of rules to ensure data is stored efficiently and consistently.

### First Normal Form (1NF):
- **Rule**: Each column must contain atomic (indivisible) values
- **Requirements**: No repeating groups, no multi-valued attributes
- **Example**: Instead of storing "John, Jane, Bob" in one cell, create separate rows

### Second Normal Form (2NF):
- **Rule**: Must be in 1NF and all non-key attributes must be fully functionally dependent on the primary key
- **Requirements**: No partial dependencies
- **Example**: If primary key is composite, all attributes must depend on the entire key

### Third Normal Form (3NF):
- **Rule**: Must be in 2NF and no transitive dependencies
- **Requirements**: Non-key attributes cannot depend on other non-key attributes
- **Example**: If A→B and B→C, then A→C is a transitive dependency

### Boyce-Codd Normal Form (BCNF):
- **Rule**: Must be in 3NF and every determinant must be a candidate key
- **Requirements**: No overlapping candidate keys
- **Example**: Every attribute that determines another attribute must be a key

### Real-World Analogy:
Think of normalization like organizing a filing system:

**1NF** = Separate File Folders:
- Each piece of information gets its own folder
- No folder contains multiple unrelated documents
- Like separating "John's phone, Jane's phone, Bob's phone" into individual folders

**2NF** = Logical Grouping:
- All documents in a folder must relate to the same person
- No mixing of different people's information in one folder
- Like ensuring all documents in "John's folder" are actually John's

**3NF** = Eliminating Redundancy:
- Don't store the same information in multiple places
- If you know John's address, don't repeat it in every document
- Like having a master address book instead of repeating addresses

**BCNF** = Perfect Organization:
- Every piece of information has exactly one place to be stored
- No ambiguity about where to find information
- Like having a perfectly organized library where every book has exactly one location

### Java Example - Normalization Process:
```java
// UNNORMALIZED - All data in one table (violates 1NF)
@Entity
@Table(name = "student_courses_unnormalized")
public class StudentCourseUnnormalized {
    @Id
    private Long id;
    
    // Violates 1NF - storing multiple values in one field
    private String studentNames;  // "John, Jane, Bob"
    private String courseNames;   // "Math, Science, English"
    private String grades;        // "A, B, C"
}

// 1NF - Atomic values, separate rows
@Entity
@Table(name = "student_courses_1nf")
public class StudentCourse1NF {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    private String studentName;   // Atomic value
    private String courseName;    // Atomic value
    private String grade;         // Atomic value
}

// 2NF - Separate entities, eliminate partial dependencies
@Entity
@Table(name = "students_2nf")
public class Student2NF {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    private String name;
    private String email;
    private String address;
    
    // All attributes depend on the entire primary key
}

@Entity
@Table(name = "courses_2nf")
public class Course2NF {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    private String name;
    private String department;
    private Integer credits;
    
    // All attributes depend on the entire primary key
}

@Entity
@Table(name = "enrollments_2nf")
public class Enrollment2NF {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    private Long studentId;
    private Long courseId;
    private String grade;
    private LocalDate enrollmentDate;
    
    // All attributes depend on the entire primary key
}

// 3NF - Eliminate transitive dependencies
@Entity
@Table(name = "students_3nf")
public class Student3NF {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    private String name;
    private String email;
    private Long addressId;  // Reference to address table
    
    @ManyToOne
    @JoinColumn(name = "address_id")
    private Address address;
}

@Entity
@Table(name = "addresses_3nf")
public class Address {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    private String street;
    private String city;
    private String state;
    private String zipCode;
    
    // No transitive dependencies
}

// BCNF - Every determinant is a candidate key
@Entity
@Table(name = "course_instructors_bcnf")
public class CourseInstructor {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    private Long courseId;
    private Long instructorId;
    private String semester;
    
    // Every determinant (courseId, instructorId, semester) is a candidate key
    @UniqueConstraint(columnNames = {"courseId", "instructorId", "semester"})
    public class CourseInstructorConstraint {}
}
```

## 2.6 Denormalization Strategies

Denormalization is the intentional process of adding redundant data to improve query performance, often at the cost of increased storage and potential data inconsistency.

### When to Denormalize:
- **Performance Critical**: Queries are too slow with normalized structure
- **Read-Heavy Workloads**: More reads than writes
- **Reporting Requirements**: Complex analytical queries
- **Real-time Systems**: Need for immediate data access

### Common Denormalization Techniques:

#### 1. Redundant Columns
- **Purpose**: Store frequently accessed data in multiple tables
- **Example**: Store customer name in orders table to avoid joins
- **Trade-off**: Faster queries vs. data redundancy

#### 2. Derived Columns
- **Purpose**: Store calculated values instead of computing them
- **Example**: Store order total instead of calculating sum of line items
- **Trade-off**: Faster reads vs. slower writes

#### 3. Duplicate Tables
- **Purpose**: Create specialized tables for specific use cases
- **Example**: Separate reporting table with denormalized data
- **Trade-off**: Better performance vs. data synchronization

#### 4. Summary Tables
- **Purpose**: Pre-calculate aggregations for reporting
- **Example**: Daily sales summary table
- **Trade-off**: Fast reporting vs. complex maintenance

### Real-World Analogy:
Think of denormalization like creating shortcuts in a library:

**Normalized** = Centralized Catalog:
- All information in one place
- Must look up references to find related information
- Like checking the catalog, then going to different sections

**Denormalized** = Multiple Reference Copies:
- Keep copies of frequently used information in multiple places
- Faster access to common information
- Like having a copy of the phone book in every department

### Java Example - Denormalization Strategies:
```java
// Normalized structure
@Entity
@Table(name = "orders")
public class Order {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    private Long customerId;
    private LocalDateTime orderDate;
    private String status;
    
    @ManyToOne
    @JoinColumn(name = "customer_id")
    private Customer customer;
    
    @OneToMany(mappedBy = "order")
    private List<OrderItem> items;
}

@Entity
@Table(name = "customers")
public class Customer {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    private String firstName;
    private String lastName;
    private String email;
    private String phone;
}

// Denormalized structure for performance
@Entity
@Table(name = "orders_denormalized")
public class OrderDenormalized {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    // Redundant columns for faster queries
    private String customerName;      // Denormalized from Customer
    private String customerEmail;     // Denormalized from Customer
    private BigDecimal orderTotal;    // Derived column
    private Integer itemCount;        // Derived column
    
    private LocalDateTime orderDate;
    private String status;
    
    // Original foreign key for data integrity
    private Long customerId;
}

// Summary table for reporting
@Entity
@Table(name = "daily_sales_summary")
public class DailySalesSummary {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    private LocalDate date;
    private BigDecimal totalSales;
    private Integer totalOrders;
    private Integer totalCustomers;
    private BigDecimal averageOrderValue;
    
    // Pre-calculated aggregations
    @PrePersist
    @PreUpdate
    public void calculateDerivedFields() {
        if (totalOrders > 0) {
            averageOrderValue = totalSales.divide(
                BigDecimal.valueOf(totalOrders), 2, RoundingMode.HALF_UP);
        }
    }
}

// Service for maintaining denormalized data
@Service
public class DenormalizationService {
    
    @Autowired
    private OrderRepository orderRepository;
    
    @Autowired
    private OrderDenormalizedRepository orderDenormalizedRepository;
    
    // Update denormalized data when source changes
    @Transactional
    public void updateOrderDenormalized(Order order) {
        OrderDenormalized denormalized = orderDenormalizedRepository
            .findById(order.getId())
            .orElse(new OrderDenormalized());
        
        // Update denormalized fields
        denormalized.setId(order.getId());
        denormalized.setCustomerName(order.getCustomer().getFirstName() + " " + 
                                   order.getCustomer().getLastName());
        denormalized.setCustomerEmail(order.getCustomer().getEmail());
        denormalized.setOrderTotal(calculateOrderTotal(order));
        denormalized.setItemCount(order.getItems().size());
        denormalized.setOrderDate(order.getOrderDate());
        denormalized.setStatus(order.getStatus());
        denormalized.setCustomerId(order.getCustomerId());
        
        orderDenormalizedRepository.save(denormalized);
    }
    
    // Update summary table
    @Scheduled(cron = "0 0 1 * * ?") // Daily at 1 AM
    public void updateDailySalesSummary() {
        LocalDate yesterday = LocalDate.now().minusDays(1);
        
        // Calculate summary data
        BigDecimal totalSales = orderRepository.getTotalSalesByDate(yesterday);
        Integer totalOrders = orderRepository.getOrderCountByDate(yesterday);
        Integer totalCustomers = orderRepository.getUniqueCustomerCountByDate(yesterday);
        
        // Save or update summary
        DailySalesSummary summary = dailySalesSummaryRepository
            .findByDate(yesterday)
            .orElse(new DailySalesSummary());
        
        summary.setDate(yesterday);
        summary.setTotalSales(totalSales);
        summary.setTotalOrders(totalOrders);
        summary.setTotalCustomers(totalCustomers);
        
        dailySalesSummaryRepository.save(summary);
    }
}
```

## 2.7 Referential Integrity

Referential integrity ensures that relationships between tables remain consistent and valid. It prevents orphaned records and maintains data consistency across related tables.

### Key Concepts:
- **Foreign Key Constraint**: Ensures foreign key values exist in the referenced table
- **Cascade Operations**: Automatically propagate changes to related records
- **Restrict Operations**: Prevent changes that would violate referential integrity
- **Set Null Operations**: Set foreign key to null when referenced record is deleted

### Referential Integrity Rules:
1. **Insert Rule**: Cannot insert a record with a foreign key that doesn't exist
2. **Update Rule**: Cannot update a foreign key to a non-existent value
3. **Delete Rule**: Cannot delete a record that is referenced by other records
4. **Cascade Rule**: Changes to parent records automatically affect child records

### Real-World Analogy:
Think of referential integrity like a library's book tracking system:

**Foreign Key Constraint** = Book Checkout System:
- You can't check out a book that doesn't exist in the catalog
- You can't return a book to a shelf that doesn't exist
- Every checkout must reference a valid book and valid borrower

**Cascade Operations** = Book Series Management:
- If a book series is discontinued, all individual books in the series are also removed
- If a borrower's account is closed, all their current checkouts are automatically returned

**Restrict Operations** = Book Reservation System:
- You can't delete a book that has active reservations
- You can't remove a borrower who has books checked out

### Java Example - Referential Integrity Implementation:
```java
// Parent table with referential integrity constraints
@Entity
@Table(name = "departments")
public class Department {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @Column(unique = true, nullable = false)
    private String name;
    
    private String description;
    
    // One-to-many relationship with cascade options
    @OneToMany(mappedBy = "department", cascade = CascadeType.ALL, orphanRemoval = true)
    private List<Employee> employees = new ArrayList<>();
    
    // Getters and setters...
}

// Child table with foreign key constraints
@Entity
@Table(name = "employees")
public class Employee {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @Column(nullable = false)
    private String firstName;
    
    @Column(nullable = false)
    private String lastName;
    
    @Column(unique = true)
    private String email;
    
    // Foreign key with referential integrity
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "department_id", nullable = false)
    private Department department;
    
    // Getters and setters...
}

// Service demonstrating referential integrity
@Service
public class ReferentialIntegrityService {
    
    @Autowired
    private DepartmentRepository departmentRepository;
    
    @Autowired
    private EmployeeRepository employeeRepository;
    
    // Valid operation - creating employee with existing department
    @Transactional
    public Employee createEmployee(String firstName, String lastName, String email, Long departmentId) {
        Department department = departmentRepository.findById(departmentId)
            .orElseThrow(() -> new DepartmentNotFoundException("Department not found"));
        
        Employee employee = new Employee();
        employee.setFirstName(firstName);
        employee.setLastName(lastName);
        employee.setEmail(email);
        employee.setDepartment(department);
        
        return employeeRepository.save(employee);
    }
    
    // Invalid operation - would violate referential integrity
    @Transactional
    public void createEmployeeWithInvalidDepartment(String firstName, String lastName, String email, Long departmentId) {
        // This will fail if departmentId doesn't exist
        Department department = new Department();
        department.setId(departmentId); // This department doesn't exist in database
        
        Employee employee = new Employee();
        employee.setFirstName(firstName);
        employee.setLastName(lastName);
        employee.setEmail(email);
        employee.setDepartment(department);
        
        // This will throw a constraint violation exception
        employeeRepository.save(employee);
    }
    
    // Cascade delete - deleting department will delete all employees
    @Transactional
    public void deleteDepartment(Long departmentId) {
        Department department = departmentRepository.findById(departmentId)
            .orElseThrow(() -> new DepartmentNotFoundException("Department not found"));
        
        // This will cascade delete all employees in the department
        departmentRepository.delete(department);
    }
    
    // Restrict delete - cannot delete department with employees
    @Transactional
    public void deleteDepartmentWithRestriction(Long departmentId) {
        Department department = departmentRepository.findById(departmentId)
            .orElseThrow(() -> new DepartmentNotFoundException("Department not found"));
        
        // Check if department has employees
        if (!department.getEmployees().isEmpty()) {
            throw new ReferentialIntegrityException("Cannot delete department with employees");
        }
        
        departmentRepository.delete(department);
    }
}

// Custom exception for referential integrity violations
public class ReferentialIntegrityException extends RuntimeException {
    public ReferentialIntegrityException(String message) {
        super(message);
    }
}

// Database-level referential integrity constraints
@SQLRestriction("department_id IN (SELECT id FROM departments)")
@Entity
@Table(name = "employees")
public class Employee {
    // Entity definition...
}

// Application-level referential integrity validation
@Component
public class ReferentialIntegrityValidator {
    
    public void validateEmployee(Employee employee) {
        if (employee.getDepartment() == null) {
            throw new ValidationException("Employee must have a department");
        }
        
        if (employee.getDepartment().getId() == null) {
            throw new ValidationException("Department must have a valid ID");
        }
        
        // Additional validation logic...
    }
}
```

## 2.8 Entity-Relationship (ER) Modeling

Entity-Relationship modeling is a graphical technique for designing databases that visually represents entities, attributes, and relationships in a database schema.

### ER Model Components:

#### 1. Entities
- **Definition**: Objects or concepts that have independent existence
- **Representation**: Rectangles in ER diagrams
- **Examples**: Student, Course, Department, Employee
- **Characteristics**: Have attributes and can participate in relationships

#### 2. Attributes
- **Definition**: Properties or characteristics of entities
- **Representation**: Ovals connected to entities
- **Types**: Simple, Composite, Single-valued, Multi-valued, Derived
- **Examples**: Student ID, Name, Email, Date of Birth

#### 3. Relationships
- **Definition**: Associations between entities
- **Representation**: Diamonds connected to entities
- **Types**: One-to-One, One-to-Many, Many-to-Many
- **Examples**: Enrolls, Works-for, Manages

#### 4. Cardinality
- **Definition**: Number of instances of one entity that can be associated with another
- **Types**: One-to-One (1:1), One-to-Many (1:M), Many-to-Many (M:N)
- **Representation**: Numbers or symbols on relationship lines

### ER Diagram Notation:
- **Entity**: Rectangle
- **Attribute**: Oval
- **Relationship**: Diamond
- **Primary Key**: Underlined attribute
- **Foreign Key**: Dashed line
- **Cardinality**: Numbers (1, M, N) on relationship lines

### Real-World Analogy:
Think of ER modeling like creating a map of a city:

**Entities** = Buildings:
- Each building represents a distinct concept (School, Hospital, Library)
- Buildings have specific purposes and characteristics
- Like entities in a database

**Attributes** = Building Details:
- Address, number of floors, capacity, year built
- Each building has specific properties
- Like attributes of entities

**Relationships** = Roads and Connections:
- Roads connect buildings to each other
- Some buildings are connected by multiple roads
- Like relationships between entities

**Cardinality** = Traffic Rules:
- One-way street (1:1 relationship)
- Main road with many side streets (1:M relationship)
- Intersection with multiple roads (M:N relationship)

### Java Example - ER Model Implementation:
```java
// Entity: Student
@Entity
@Table(name = "students")
public class Student {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;  // Primary Key attribute
    
    @Column(nullable = false)
    private String firstName;  // Simple attribute
    
    @Column(nullable = false)
    private String lastName;   // Simple attribute
    
    @Column(unique = true)
    private String email;      // Simple attribute
    
    @Embedded
    private Address address;   // Composite attribute
    
    @ElementCollection
    @CollectionTable(name = "student_phone_numbers")
    private List<String> phoneNumbers;  // Multi-valued attribute
    
    @Transient
    private String fullName;   // Derived attribute
    
    // Relationships
    @ManyToMany(mappedBy = "students")
    private Set<Course> courses = new HashSet<>();
    
    @OneToMany(mappedBy = "student")
    private List<Enrollment> enrollments = new ArrayList<>();
    
    // Getters and setters...
    
    // Derived attribute getter
    public String getFullName() {
        return firstName + " " + lastName;
    }
}

// Composite Attribute: Address
@Embeddable
public class Address {
    private String street;
    private String city;
    private String state;
    private String zipCode;
    private String country;
    
    // Getters and setters...
}

// Entity: Course
@Entity
@Table(name = "courses")
public class Course {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;  // Primary Key attribute
    
    @Column(nullable = false, unique = true)
    private String courseCode;  // Simple attribute
    
    @Column(nullable = false)
    private String title;       // Simple attribute
    
    private String description; // Simple attribute
    
    @Column(nullable = false)
    private Integer credits;    // Simple attribute
    
    // Relationships
    @ManyToMany
    @JoinTable(
        name = "course_students",
        joinColumns = @JoinColumn(name = "course_id"),
        inverseJoinColumns = @JoinColumn(name = "student_id")
    )
    private Set<Student> students = new HashSet<>();
    
    @ManyToOne
    @JoinColumn(name = "department_id")
    private Department department;
    
    @OneToMany(mappedBy = "course")
    private List<Enrollment> enrollments = new ArrayList<>();
    
    // Getters and setters...
}

// Entity: Department
@Entity
@Table(name = "departments")
public class Department {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;  // Primary Key attribute
    
    @Column(nullable = false, unique = true)
    private String name;  // Simple attribute
    
    private String description;  // Simple attribute
    
    // Relationships
    @OneToMany(mappedBy = "department")
    private List<Course> courses = new ArrayList<>();
    
    @OneToMany(mappedBy = "department")
    private List<Instructor> instructors = new ArrayList<>();
    
    // Getters and setters...
}

// Relationship Entity: Enrollment
@Entity
@Table(name = "enrollments")
public class Enrollment {
    @EmbeddedId
    private EnrollmentId id;  // Composite Primary Key
    
    @ManyToOne
    @MapsId("studentId")
    @JoinColumn(name = "student_id")
    private Student student;  // Foreign Key to Student
    
    @ManyToOne
    @MapsId("courseId")
    @JoinColumn(name = "course_id")
    private Course course;    // Foreign Key to Course
    
    private LocalDate enrollmentDate;  // Relationship attribute
    private String grade;              // Relationship attribute
    private String semester;           // Relationship attribute
    
    // Getters and setters...
}

// Composite Primary Key for Enrollment
@Embeddable
public class EnrollmentId implements Serializable {
    private Long studentId;  // Part of composite key
    private Long courseId;   // Part of composite key
    
    // Constructors, equals, hashCode...
}

// Service for ER model operations
@Service
public class ERModelService {
    
    @Autowired
    private StudentRepository studentRepository;
    
    @Autowired
    private CourseRepository courseRepository;
    
    @Autowired
    private DepartmentRepository departmentRepository;
    
    // Create entity with relationships
    @Transactional
    public Student createStudentWithEnrollment(String firstName, String lastName, 
                                             String email, Long courseId) {
        // Create student entity
        Student student = new Student();
        student.setFirstName(firstName);
        student.setLastName(lastName);
        student.setEmail(email);
        
        // Establish relationship with course
        Course course = courseRepository.findById(courseId)
            .orElseThrow(() -> new CourseNotFoundException("Course not found"));
        
        student.getCourses().add(course);
        course.getStudents().add(student);
        
        return studentRepository.save(student);
    }
    
    // Query entities with relationships
    public List<Student> getStudentsByDepartment(String departmentName) {
        return studentRepository.findByCoursesDepartmentName(departmentName);
    }
    
    // Update relationship
    @Transactional
    public void enrollStudentInCourse(Long studentId, Long courseId) {
        Student student = studentRepository.findById(studentId)
            .orElseThrow(() -> new StudentNotFoundException("Student not found"));
        
        Course course = courseRepository.findById(courseId)
            .orElseThrow(() -> new CourseNotFoundException("Course not found"));
        
        // Add relationship
        student.getCourses().add(course);
        course.getStudents().add(student);
        
        studentRepository.save(student);
        courseRepository.save(course);
    }
}
```