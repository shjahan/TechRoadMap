# Section 3 – SQL Fundamentals

## 3.1 SQL Language Overview

SQL (Structured Query Language) is a standardized programming language designed for managing and manipulating relational databases. It provides a comprehensive set of commands for data definition, manipulation, control, and querying.

### Key Characteristics:
- **Declarative Language**: Specify what you want, not how to get it
- **Standardized**: ANSI/ISO standards ensure portability
- **Non-procedural**: Focus on data rather than algorithms
- **English-like Syntax**: Readable and intuitive commands

### SQL Categories:
- **DDL (Data Definition Language)**: CREATE, ALTER, DROP
- **DML (Data Manipulation Language)**: INSERT, UPDATE, DELETE
- **DCL (Data Control Language)**: GRANT, REVOKE
- **DQL (Data Query Language)**: SELECT

### Real-World Analogy:
SQL is like a universal language for talking to databases:
- **Like English**: Everyone understands the same commands
- **Like a Recipe**: You describe what you want to cook, not how to use the stove
- **Like a Library**: You ask for books by title, not by shelf position

### Java Example - SQL Integration:
```java
import java.sql.*;

public class SQLBasics {
    private Connection connection;
    
    public SQLBasics(Connection connection) {
        this.connection = connection;
    }
    
    // DDL - Create table
    public void createTable() throws SQLException {
        String sql = """
            CREATE TABLE students (
                id INT PRIMARY KEY AUTO_INCREMENT,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(100) UNIQUE,
                age INT CHECK (age >= 0),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """;
        
        try (Statement stmt = connection.createStatement()) {
            stmt.execute(sql);
            System.out.println("Table created successfully");
        }
    }
    
    // DML - Insert data
    public void insertStudent(String name, String email, int age) throws SQLException {
        String sql = "INSERT INTO students (name, email, age) VALUES (?, ?, ?)";
        
        try (PreparedStatement stmt = connection.prepareStatement(sql)) {
            stmt.setString(1, name);
            stmt.setString(2, email);
            stmt.setInt(3, age);
            stmt.executeUpdate();
            System.out.println("Student inserted successfully");
        }
    }
    
    // DQL - Query data
    public void getAllStudents() throws SQLException {
        String sql = "SELECT id, name, email, age FROM students";
        
        try (Statement stmt = connection.createStatement();
             ResultSet rs = stmt.executeQuery(sql)) {
            
            while (rs.next()) {
                System.out.printf("ID: %d, Name: %s, Email: %s, Age: %d%n",
                    rs.getInt("id"),
                    rs.getString("name"),
                    rs.getString("email"),
                    rs.getInt("age"));
            }
        }
    }
}
```

## 3.2 Data Definition Language (DDL)

DDL commands are used to define and modify the structure of database objects like tables, indexes, views, and schemas.

### Key DDL Commands:
- **CREATE**: Create new database objects
- **ALTER**: Modify existing database objects
- **DROP**: Remove database objects
- **TRUNCATE**: Remove all data from a table
- **RENAME**: Rename database objects

### Real-World Analogy:
DDL is like construction and renovation:
- **CREATE** = Building a new house
- **ALTER** = Renovating an existing house
- **DROP** = Demolishing a house
- **TRUNCATE** = Emptying a house of all furniture
- **RENAME** = Changing the house address

### Java Example - DDL Operations:
```java
public class DDLOperations {
    private Connection connection;
    
    public DDLOperations(Connection connection) {
        this.connection = connection;
    }
    
    // CREATE TABLE
    public void createStudentsTable() throws SQLException {
        String sql = """
            CREATE TABLE students (
                student_id INT PRIMARY KEY AUTO_INCREMENT,
                first_name VARCHAR(50) NOT NULL,
                last_name VARCHAR(50) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                date_of_birth DATE,
                gpa DECIMAL(3,2) CHECK (gpa >= 0.0 AND gpa <= 4.0),
                enrollment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """;
        
        executeDDL(sql, "Students table created");
    }
    
    // CREATE INDEX
    public void createIndexes() throws SQLException {
        String[] indexes = {
            "CREATE INDEX idx_students_email ON students(email)",
            "CREATE INDEX idx_students_name ON students(last_name, first_name)",
            "CREATE INDEX idx_students_gpa ON students(gpa)"
        };
        
        for (String sql : indexes) {
            executeDDL(sql, "Index created");
        }
    }
    
    // ALTER TABLE
    public void alterStudentsTable() throws SQLException {
        String[] alterations = {
            "ALTER TABLE students ADD COLUMN phone VARCHAR(20)",
            "ALTER TABLE students MODIFY COLUMN gpa DECIMAL(4,2)",
            "ALTER TABLE students ADD CONSTRAINT chk_phone CHECK (phone REGEXP '^[0-9-+() ]+$')"
        };
        
        for (String sql : alterations) {
            executeDDL(sql, "Table altered");
        }
    }
    
    // DROP TABLE
    public void dropTable(String tableName) throws SQLException {
        String sql = "DROP TABLE IF EXISTS " + tableName;
        executeDDL(sql, "Table dropped");
    }
    
    private void executeDDL(String sql, String message) throws SQLException {
        try (Statement stmt = connection.createStatement()) {
            stmt.execute(sql);
            System.out.println(message);
        }
    }
}
```

## 3.3 Data Manipulation Language (DML)

DML commands are used to manipulate data within database tables, including inserting, updating, and deleting records.

### Key DML Commands:
- **INSERT**: Add new records to tables
- **UPDATE**: Modify existing records
- **DELETE**: Remove records from tables
- **MERGE**: Insert or update records based on conditions

### Real-World Analogy:
DML is like managing a filing cabinet:
- **INSERT** = Adding new files to the cabinet
- **UPDATE** = Modifying existing files
- **DELETE** = Removing files from the cabinet
- **MERGE** = Updating files if they exist, adding them if they don't

### Java Example - DML Operations:
```java
public class DMLOperations {
    private Connection connection;
    
    public DMLOperations(Connection connection) {
        this.connection = connection;
    }
    
    // INSERT - Single record
    public void insertStudent(String firstName, String lastName, String email, 
                            LocalDate dateOfBirth, BigDecimal gpa) throws SQLException {
        String sql = """
            INSERT INTO students (first_name, last_name, email, date_of_birth, gpa)
            VALUES (?, ?, ?, ?, ?)
            """;
        
        try (PreparedStatement stmt = connection.prepareStatement(sql)) {
            stmt.setString(1, firstName);
            stmt.setString(2, lastName);
            stmt.setString(3, email);
            stmt.setDate(4, Date.valueOf(dateOfBirth));
            stmt.setBigDecimal(5, gpa);
            
            int rowsAffected = stmt.executeUpdate();
            System.out.println("Inserted " + rowsAffected + " student(s)");
        }
    }
    
    // INSERT - Multiple records
    public void insertMultipleStudents(List<Student> students) throws SQLException {
        String sql = """
            INSERT INTO students (first_name, last_name, email, date_of_birth, gpa)
            VALUES (?, ?, ?, ?, ?)
            """;
        
        try (PreparedStatement stmt = connection.prepareStatement(sql)) {
            for (Student student : students) {
                stmt.setString(1, student.getFirstName());
                stmt.setString(2, student.getLastName());
                stmt.setString(3, student.getEmail());
                stmt.setDate(4, Date.valueOf(student.getDateOfBirth()));
                stmt.setBigDecimal(5, student.getGpa());
                stmt.addBatch();
            }
            
            int[] results = stmt.executeBatch();
            System.out.println("Batch insert completed. Rows affected: " + results.length);
        }
    }
    
    // UPDATE
    public void updateStudentGpa(String email, BigDecimal newGpa) throws SQLException {
        String sql = "UPDATE students SET gpa = ? WHERE email = ?";
        
        try (PreparedStatement stmt = connection.prepareStatement(sql)) {
            stmt.setBigDecimal(1, newGpa);
            stmt.setString(2, email);
            
            int rowsAffected = stmt.executeUpdate();
            if (rowsAffected > 0) {
                System.out.println("Updated " + rowsAffected + " student(s)");
            } else {
                System.out.println("No student found with email: " + email);
            }
        }
    }
    
    // DELETE
    public void deleteStudent(String email) throws SQLException {
        String sql = "DELETE FROM students WHERE email = ?";
        
        try (PreparedStatement stmt = connection.prepareStatement(sql)) {
            stmt.setString(1, email);
            
            int rowsAffected = stmt.executeUpdate();
            if (rowsAffected > 0) {
                System.out.println("Deleted " + rowsAffected + " student(s)");
            } else {
                System.out.println("No student found with email: " + email);
            }
        }
    }
    
    // MERGE (MySQL syntax)
    public void mergeStudent(String firstName, String lastName, String email, 
                           LocalDate dateOfBirth, BigDecimal gpa) throws SQLException {
        String sql = """
            INSERT INTO students (first_name, last_name, email, date_of_birth, gpa)
            VALUES (?, ?, ?, ?, ?)
            ON DUPLICATE KEY UPDATE
                first_name = VALUES(first_name),
                last_name = VALUES(last_name),
                date_of_birth = VALUES(date_of_birth),
                gpa = VALUES(gpa)
            """;
        
        try (PreparedStatement stmt = connection.prepareStatement(sql)) {
            stmt.setString(1, firstName);
            stmt.setString(2, lastName);
            stmt.setString(3, email);
            stmt.setDate(4, Date.valueOf(dateOfBirth));
            stmt.setBigDecimal(5, gpa);
            
            int rowsAffected = stmt.executeUpdate();
            System.out.println("Merge operation completed. Rows affected: " + rowsAffected);
        }
    }
}
```

## 3.4 Data Control Language (DCL)

DCL commands are used to control access to database objects and manage user permissions and security.

### Key DCL Commands:
- **GRANT**: Give privileges to users or roles
- **REVOKE**: Remove privileges from users or roles
- **DENY**: Explicitly deny access (SQL Server specific)

### Privilege Types:
- **Object Privileges**: SELECT, INSERT, UPDATE, DELETE on specific tables
- **System Privileges**: CREATE, ALTER, DROP on database objects
- **Role Privileges**: Grant privileges through roles

### Real-World Analogy:
DCL is like managing building access:
- **GRANT** = Giving someone a key to a room
- **REVOKE** = Taking back the key
- **DENY** = Explicitly saying "no access allowed"
- **Roles** = Different types of keys (master key, office key, storage key)

### Java Example - DCL Operations:
```java
public class DCLOperations {
    private Connection connection;
    
    public DCLOperations(Connection connection) {
        this.connection = connection;
    }
    
    // GRANT privileges
    public void grantPrivileges() throws SQLException {
        String[] grants = {
            "GRANT SELECT, INSERT, UPDATE ON students TO 'student_user'@'localhost'",
            "GRANT ALL PRIVILEGES ON university_db.* TO 'admin_user'@'localhost'",
            "GRANT CREATE, DROP ON university_db.* TO 'dba_user'@'localhost'"
        };
        
        for (String sql : grants) {
            executeDCL(sql, "Privileges granted");
        }
    }
    
    // REVOKE privileges
    public void revokePrivileges() throws SQLException {
        String[] revokes = {
            "REVOKE INSERT, UPDATE ON students FROM 'student_user'@'localhost'",
            "REVOKE DROP ON university_db.* FROM 'dba_user'@'localhost'"
        };
        
        for (String sql : revokes) {
            executeDCL(sql, "Privileges revoked");
        }
    }
    
    // Create and manage roles
    public void manageRoles() throws SQLException {
        String[] roleCommands = {
            "CREATE ROLE 'student_role'",
            "CREATE ROLE 'instructor_role'",
            "CREATE ROLE 'admin_role'",
            "GRANT SELECT ON students TO 'student_role'",
            "GRANT SELECT, INSERT, UPDATE ON students TO 'instructor_role'",
            "GRANT ALL PRIVILEGES ON university_db.* TO 'admin_role'",
            "GRANT 'student_role' TO 'student_user'@'localhost'",
            "GRANT 'instructor_role' TO 'instructor_user'@'localhost'"
        };
        
        for (String sql : roleCommands) {
            executeDCL(sql, "Role operation completed");
        }
    }
    
    private void executeDCL(String sql, String message) throws SQLException {
        try (Statement stmt = connection.createStatement()) {
            stmt.execute(sql);
            System.out.println(message);
        }
    }
}
```

## 3.5 Data Query Language (DQL)

DQL consists primarily of the SELECT statement, which is used to retrieve data from database tables with various filtering, sorting, and grouping options.

### SELECT Statement Components:
- **SELECT clause**: Specify columns to retrieve
- **FROM clause**: Specify tables to query
- **WHERE clause**: Filter rows based on conditions
- **GROUP BY clause**: Group rows for aggregate functions
- **HAVING clause**: Filter groups based on aggregate conditions
- **ORDER BY clause**: Sort result set
- **LIMIT clause**: Limit number of rows returned

### Real-World Analogy:
SELECT is like asking questions in a library:
- **SELECT** = "I want to see these specific books"
- **FROM** = "From this section of the library"
- **WHERE** = "That meet these criteria"
- **GROUP BY** = "Organized by category"
- **ORDER BY** = "Sorted alphabetically"
- **LIMIT** = "Show me only the first 10"

### Java Example - DQL Operations:
```java
public class DQLOperations {
    private Connection connection;
    
    public DQLOperations(Connection connection) {
        this.connection = connection;
    }
    
    // Basic SELECT
    public void selectAllStudents() throws SQLException {
        String sql = "SELECT * FROM students";
        
        try (Statement stmt = connection.createStatement();
             ResultSet rs = stmt.executeQuery(sql)) {
            
            System.out.println("All Students:");
            while (rs.next()) {
                System.out.printf("ID: %d, Name: %s %s, Email: %s, GPA: %.2f%n",
                    rs.getInt("student_id"),
                    rs.getString("first_name"),
                    rs.getString("last_name"),
                    rs.getString("email"),
                    rs.getBigDecimal("gpa"));
            }
        }
    }
    
    // SELECT with WHERE clause
    public void selectStudentsByGpa(double minGpa) throws SQLException {
        String sql = "SELECT * FROM students WHERE gpa >= ? ORDER BY gpa DESC";
        
        try (PreparedStatement stmt = connection.prepareStatement(sql)) {
            stmt.setDouble(1, minGpa);
            
            try (ResultSet rs = stmt.executeQuery()) {
                System.out.println("Students with GPA >= " + minGpa + ":");
                while (rs.next()) {
                    System.out.printf("Name: %s %s, GPA: %.2f%n",
                        rs.getString("first_name"),
                        rs.getString("last_name"),
                        rs.getBigDecimal("gpa"));
                }
            }
        }
    }
    
    // SELECT with JOIN
    public void selectStudentsWithCourses() throws SQLException {
        String sql = """
            SELECT s.first_name, s.last_name, c.course_name, e.grade
            FROM students s
            JOIN enrollments e ON s.student_id = e.student_id
            JOIN courses c ON e.course_id = c.course_id
            ORDER BY s.last_name, c.course_name
            """;
        
        try (Statement stmt = connection.createStatement();
             ResultSet rs = stmt.executeQuery(sql)) {
            
            System.out.println("Students and their courses:");
            while (rs.next()) {
                System.out.printf("%s %s - %s (Grade: %s)%n",
                    rs.getString("first_name"),
                    rs.getString("last_name"),
                    rs.getString("course_name"),
                    rs.getString("grade"));
            }
        }
    }
    
    // SELECT with GROUP BY and aggregate functions
    public void selectGpaStatistics() throws SQLException {
        String sql = """
            SELECT 
                COUNT(*) as total_students,
                AVG(gpa) as average_gpa,
                MIN(gpa) as min_gpa,
                MAX(gpa) as max_gpa,
                STDDEV(gpa) as gpa_stddev
            FROM students
            WHERE gpa IS NOT NULL
            """;
        
        try (Statement stmt = connection.createStatement();
             ResultSet rs = stmt.executeQuery(sql)) {
            
            if (rs.next()) {
                System.out.println("GPA Statistics:");
                System.out.printf("Total Students: %d%n", rs.getInt("total_students"));
                System.out.printf("Average GPA: %.2f%n", rs.getDouble("average_gpa"));
                System.out.printf("Min GPA: %.2f%n", rs.getDouble("min_gpa"));
                System.out.printf("Max GPA: %.2f%n", rs.getDouble("max_gpa"));
                System.out.printf("Standard Deviation: %.2f%n", rs.getDouble("gpa_stddev"));
            }
        }
    }
    
    // SELECT with subquery
    public void selectTopStudents() throws SQLException {
        String sql = """
            SELECT first_name, last_name, gpa
            FROM students
            WHERE gpa >= (
                SELECT AVG(gpa) + 0.5
                FROM students
                WHERE gpa IS NOT NULL
            )
            ORDER BY gpa DESC
            """;
        
        try (Statement stmt = connection.createStatement();
             ResultSet rs = stmt.executeQuery(sql)) {
            
            System.out.println("Top performing students:");
            while (rs.next()) {
                System.out.printf("%s %s - GPA: %.2f%n",
                    rs.getString("first_name"),
                    rs.getString("last_name"),
                    rs.getBigDecimal("gpa"));
            }
        }
    }
}
```

## 3.6 SQL Data Types

SQL provides various data types to store different kinds of data efficiently and accurately.

### Numeric Types:
- **INTEGER**: Whole numbers (-2,147,483,648 to 2,147,483,647)
- **BIGINT**: Large whole numbers
- **DECIMAL/NUMERIC**: Exact decimal numbers
- **FLOAT/REAL**: Approximate floating-point numbers
- **DOUBLE**: Double-precision floating-point numbers

### String Types:
- **CHAR(n)**: Fixed-length character strings
- **VARCHAR(n)**: Variable-length character strings
- **TEXT**: Large text data
- **NCHAR/NVARCHAR**: Unicode character strings

### Date/Time Types:
- **DATE**: Date values (YYYY-MM-DD)
- **TIME**: Time values (HH:MM:SS)
- **DATETIME/TIMESTAMP**: Date and time values
- **YEAR**: Year values

### Binary Types:
- **BLOB**: Binary large objects
- **BINARY**: Fixed-length binary data
- **VARBINARY**: Variable-length binary data

### Real-World Analogy:
Data types are like different containers for different items:
- **INTEGER** = Small box for whole numbers
- **VARCHAR** = Flexible bag for text
- **DATE** = Calendar for dates
- **BLOB** = Large storage box for files

### Java Example - Data Type Handling:
```java
public class SQLDataTypes {
    private Connection connection;
    
    public SQLDataTypes(Connection connection) {
        this.connection = connection;
    }
    
    // Create table with various data types
    public void createDataTypesTable() throws SQLException {
        String sql = """
            CREATE TABLE data_types_example (
                id INT PRIMARY KEY AUTO_INCREMENT,
                name VARCHAR(100) NOT NULL,
                age TINYINT UNSIGNED,
                salary DECIMAL(10,2),
                is_active BOOLEAN DEFAULT TRUE,
                birth_date DATE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                profile_image BLOB,
                description TEXT,
                metadata JSON
            )
            """;
        
        try (Statement stmt = connection.createStatement()) {
            stmt.execute(sql);
            System.out.println("Data types table created");
        }
    }
    
    // Insert data with different types
    public void insertDataWithTypes() throws SQLException {
        String sql = """
            INSERT INTO data_types_example 
            (name, age, salary, is_active, birth_date, description, metadata)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """;
        
        try (PreparedStatement stmt = connection.prepareStatement(sql)) {
            stmt.setString(1, "John Doe");
            stmt.setInt(2, 30);
            stmt.setBigDecimal(3, new BigDecimal("75000.50"));
            stmt.setBoolean(4, true);
            stmt.setDate(5, Date.valueOf(LocalDate.of(1990, 5, 15)));
            stmt.setString(6, "This is a long description that can contain multiple lines of text.");
            stmt.setString(7, "{\"department\": \"IT\", \"level\": \"Senior\"}");
            
            stmt.executeUpdate();
            System.out.println("Data inserted with various types");
        }
    }
    
    // Query data with type-specific operations
    public void queryDataWithTypes() throws SQLException {
        String sql = """
            SELECT 
                name,
                age,
                salary,
                is_active,
                birth_date,
                YEAR(birth_date) as birth_year,
                DATEDIFF(CURRENT_DATE, birth_date) / 365 as age_in_years,
                CASE 
                    WHEN salary > 100000 THEN 'High'
                    WHEN salary > 50000 THEN 'Medium'
                    ELSE 'Low'
                END as salary_category
            FROM data_types_example
            """;
        
        try (Statement stmt = connection.createStatement();
             ResultSet rs = stmt.executeQuery(sql)) {
            
            while (rs.next()) {
                System.out.printf("Name: %s, Age: %d, Salary: $%.2f, Active: %s%n",
                    rs.getString("name"),
                    rs.getInt("age"),
                    rs.getBigDecimal("salary"),
                    rs.getBoolean("is_active"));
                
                System.out.printf("Birth Year: %d, Age in Years: %.1f, Salary Category: %s%n",
                    rs.getInt("birth_year"),
                    rs.getDouble("age_in_years"),
                    rs.getString("salary_category"));
            }
        }
    }
}
```

## 3.7 SQL Functions and Operators

SQL provides a rich set of built-in functions and operators for data manipulation, calculation, and transformation.

### String Functions:
- **CONCAT**: Concatenate strings
- **SUBSTRING**: Extract part of a string
- **UPPER/LOWER**: Convert case
- **LENGTH**: Get string length
- **TRIM**: Remove leading/trailing spaces

### Numeric Functions:
- **ABS**: Absolute value
- **ROUND**: Round to specified decimal places
- **CEIL/FLOOR**: Round up/down
- **MOD**: Modulo operation
- **POWER**: Exponentiation

### Date Functions:
- **NOW/CURRENT_TIMESTAMP**: Current date and time
- **DATE_ADD/DATE_SUB**: Add/subtract time intervals
- **DATEDIFF**: Difference between dates
- **YEAR/MONTH/DAY**: Extract date parts

### Aggregate Functions:
- **COUNT**: Count rows
- **SUM**: Sum values
- **AVG**: Average values
- **MIN/MAX**: Minimum/maximum values
- **GROUP_CONCAT**: Concatenate group values

### Real-World Analogy:
SQL functions are like tools in a workshop:
- **String Functions** = Text processing tools (scissors, glue)
- **Numeric Functions** = Calculator functions
- **Date Functions** = Calendar and clock tools
- **Aggregate Functions** = Summary and counting tools

### Java Example - SQL Functions:
```java
public class SQLFunctions {
    private Connection connection;
    
    public SQLFunctions(Connection connection) {
        this.connection = connection;
    }
    
    // String functions
    public void demonstrateStringFunctions() throws SQLException {
        String sql = """
            SELECT 
                CONCAT(first_name, ' ', last_name) as full_name,
                UPPER(email) as email_upper,
                LENGTH(first_name) as name_length,
                SUBSTRING(email, 1, LOCATE('@', email) - 1) as username
            FROM students
            LIMIT 5
            """;
        
        try (Statement stmt = connection.createStatement();
             ResultSet rs = stmt.executeQuery(sql)) {
            
            System.out.println("String Functions Demo:");
            while (rs.next()) {
                System.out.printf("Full Name: %s, Email: %s, Name Length: %d, Username: %s%n",
                    rs.getString("full_name"),
                    rs.getString("email_upper"),
                    rs.getInt("name_length"),
                    rs.getString("username"));
            }
        }
    }
    
    // Numeric functions
    public void demonstrateNumericFunctions() throws SQLException {
        String sql = """
            SELECT 
                gpa,
                ROUND(gpa, 1) as gpa_rounded,
                CEIL(gpa) as gpa_ceiling,
                FLOOR(gpa) as gpa_floor,
                ABS(gpa - 3.0) as distance_from_3_0
            FROM students
            WHERE gpa IS NOT NULL
            LIMIT 5
            """;
        
        try (Statement stmt = connection.createStatement();
             ResultSet rs = stmt.executeQuery(sql)) {
            
            System.out.println("Numeric Functions Demo:");
            while (rs.next()) {
                System.out.printf("GPA: %.2f, Rounded: %.1f, Ceiling: %.0f, Floor: %.0f, Distance: %.2f%n",
                    rs.getDouble("gpa"),
                    rs.getDouble("gpa_rounded"),
                    rs.getDouble("gpa_ceiling"),
                    rs.getDouble("gpa_floor"),
                    rs.getDouble("distance_from_3_0"));
            }
        }
    }
    
    // Date functions
    public void demonstrateDateFunctions() throws SQLException {
        String sql = """
            SELECT 
                first_name,
                last_name,
                date_of_birth,
                YEAR(date_of_birth) as birth_year,
                DATEDIFF(CURRENT_DATE, date_of_birth) / 365 as age_years,
                DATE_ADD(date_of_birth, INTERVAL 18 YEAR) as age_18_date
            FROM students
            WHERE date_of_birth IS NOT NULL
            LIMIT 5
            """;
        
        try (Statement stmt = connection.createStatement();
             ResultSet rs = stmt.executeQuery(sql)) {
            
            System.out.println("Date Functions Demo:");
            while (rs.next()) {
                System.out.printf("Name: %s %s, Birth Year: %d, Age: %.1f years%n",
                    rs.getString("first_name"),
                    rs.getString("last_name"),
                    rs.getInt("birth_year"),
                    rs.getDouble("age_years"));
            }
        }
    }
    
    // Aggregate functions
    public void demonstrateAggregateFunctions() throws SQLException {
        String sql = """
            SELECT 
                COUNT(*) as total_students,
                COUNT(gpa) as students_with_gpa,
                AVG(gpa) as average_gpa,
                MIN(gpa) as min_gpa,
                MAX(gpa) as max_gpa,
                STDDEV(gpa) as gpa_stddev,
                GROUP_CONCAT(DISTINCT SUBSTRING(first_name, 1, 1) ORDER BY first_name) as first_letters
            FROM students
            """;
        
        try (Statement stmt = connection.createStatement();
             ResultSet rs = stmt.executeQuery(sql)) {
            
            if (rs.next()) {
                System.out.println("Aggregate Functions Demo:");
                System.out.printf("Total Students: %d%n", rs.getInt("total_students"));
                System.out.printf("Students with GPA: %d%n", rs.getInt("students_with_gpa"));
                System.out.printf("Average GPA: %.2f%n", rs.getDouble("average_gpa"));
                System.out.printf("Min GPA: %.2f%n", rs.getDouble("min_gpa"));
                System.out.printf("Max GPA: %.2f%n", rs.getDouble("max_gpa"));
                System.out.printf("GPA Std Dev: %.2f%n", rs.getDouble("gpa_stddev"));
                System.out.printf("First Letters: %s%n", rs.getString("first_letters"));
            }
        }
    }
}
```

## 3.8 SQL Standards and Variations

SQL has evolved through various standards and implementations, each with specific features and syntax variations.

### SQL Standards:
- **SQL-86**: First ANSI standard
- **SQL-89**: Added integrity constraints
- **SQL-92**: Major revision with many new features
- **SQL:1999**: Added object-oriented features
- **SQL:2003**: Added XML support
- **SQL:2008**: Added MERGE statement
- **SQL:2011**: Added temporal features
- **SQL:2016**: Added JSON support

### Database Variations:
- **MySQL**: Open-source, popular for web applications
- **PostgreSQL**: Advanced open-source with many features
- **Oracle**: Enterprise-grade with advanced features
- **SQL Server**: Microsoft's enterprise database
- **SQLite**: Lightweight, embedded database

### Real-World Analogy:
SQL standards are like language dialects:
- **Standard SQL** = Proper English grammar
- **MySQL** = American English dialect
- **PostgreSQL** = British English dialect
- **Oracle** = Academic English dialect
- **SQL Server** = Microsoft English dialect

### Java Example - Database Variations:
```java
public class SQLVariations {
    private Connection connection;
    private String databaseType;
    
    public SQLVariations(Connection connection, String databaseType) {
        this.connection = connection;
        this.databaseType = databaseType;
    }
    
    // MySQL specific syntax
    public void mysqlSpecificOperations() throws SQLException {
        if (!"mysql".equalsIgnoreCase(databaseType)) {
            System.out.println("MySQL specific operations skipped");
            return;
        }
        
        String[] mysqlQueries = {
            "SELECT @@version as mysql_version",
            "SHOW TABLES",
            "DESCRIBE students",
            "SELECT * FROM students LIMIT 10"
        };
        
        for (String sql : mysqlQueries) {
            executeQuery(sql, "MySQL Query");
        }
    }
    
    // PostgreSQL specific syntax
    public void postgresqlSpecificOperations() throws SQLException {
        if (!"postgresql".equalsIgnoreCase(databaseType)) {
            System.out.println("PostgreSQL specific operations skipped");
            return;
        }
        
        String[] postgresQueries = {
            "SELECT version() as postgres_version",
            "SELECT tablename FROM pg_tables WHERE schemaname = 'public'",
            "SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'students'",
            "SELECT * FROM students LIMIT 10"
        };
        
        for (String sql : postgresQueries) {
            executeQuery(sql, "PostgreSQL Query");
        }
    }
    
    // Oracle specific syntax
    public void oracleSpecificOperations() throws SQLException {
        if (!"oracle".equalsIgnoreCase(databaseType)) {
            System.out.println("Oracle specific operations skipped");
            return;
        }
        
        String[] oracleQueries = {
            "SELECT * FROM v$version WHERE rownum = 1",
            "SELECT table_name FROM user_tables",
            "SELECT column_name, data_type FROM user_tab_columns WHERE table_name = 'STUDENTS'",
            "SELECT * FROM students WHERE rownum <= 10"
        };
        
        for (String sql : oracleQueries) {
            executeQuery(sql, "Oracle Query");
        }
    }
    
    // Cross-database compatible queries
    public void crossDatabaseQueries() throws SQLException {
        String sql = "SELECT COUNT(*) as student_count FROM students";
        
        try (Statement stmt = connection.createStatement();
             ResultSet rs = stmt.executeQuery(sql)) {
            
            if (rs.next()) {
                System.out.println("Cross-database compatible query result:");
                System.out.println("Student count: " + rs.getInt("student_count"));
            }
        }
    }
    
    private void executeQuery(String sql, String description) throws SQLException {
        try (Statement stmt = connection.createStatement();
             ResultSet rs = stmt.executeQuery(sql)) {
            
            System.out.println(description + ":");
            ResultSetMetaData metaData = rs.getMetaData();
            int columnCount = metaData.getColumnCount();
            
            while (rs.next()) {
                for (int i = 1; i <= columnCount; i++) {
                    System.out.print(metaData.getColumnName(i) + ": " + rs.getString(i) + " ");
                }
                System.out.println();
            }
        }
    }
}
```