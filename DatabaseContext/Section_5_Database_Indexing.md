# Section 5 – Database Indexing

## 5.1 Index Fundamentals

Database indexes are data structures that improve the speed of data retrieval operations on a database table. They work like an index in a book, allowing the database to quickly locate specific rows without scanning the entire table.

### Key Concepts:
- **Index**: A data structure that points to the physical location of data
- **Index Key**: The column(s) used to create the index
- **Index Entry**: A single record in the index containing the key value and pointer
- **Index Scan**: Using the index to find data
- **Table Scan**: Reading the entire table to find data

### Real-World Analogy:
Think of a database index like a phone book:
- **Index** = Alphabetical listing of names
- **Index Key** = Last name (what you look up by)
- **Index Entry** = Name + Phone number + Address
- **Index Scan** = Looking up "Smith" in the S section
- **Table Scan** = Reading every entry from A to Z

### Java Example - Index Usage:
```java
import java.sql.*;

public class IndexExample {
    private Connection connection;
    
    public IndexExample(Connection connection) {
        this.connection = connection;
    }
    
    // Create an index
    public void createIndex() throws SQLException {
        String sql = "CREATE INDEX idx_students_email ON students(email)";
        
        try (Statement stmt = connection.createStatement()) {
            stmt.execute(sql);
            System.out.println("Index created successfully");
        }
    }
    
    // Query that benefits from index
    public void findStudentByEmail(String email) throws SQLException {
        String sql = "SELECT * FROM students WHERE email = ?";
        
        try (PreparedStatement stmt = connection.prepareStatement(sql)) {
            stmt.setString(1, email);
            
            long startTime = System.currentTimeMillis();
            try (ResultSet rs = stmt.executeQuery()) {
                long endTime = System.currentTimeMillis();
                System.out.println("Query executed in " + (endTime - startTime) + "ms");
                
                while (rs.next()) {
                    System.out.println("Found: " + rs.getString("first_name") + " " + rs.getString("last_name"));
                }
            }
        }
    }
}
```

## 5.2 B-Tree Indexes

B-Tree (Balanced Tree) indexes are the most common type of database index. They maintain sorted data and allow efficient searches, insertions, and deletions.

### B-Tree Characteristics:
- **Balanced**: All leaf nodes are at the same level
- **Sorted**: Data is stored in sorted order
- **Multi-level**: Tree structure with root, internal, and leaf nodes
- **Efficient**: O(log n) search time complexity

### Real-World Analogy:
B-Tree is like a multi-level filing system:
- **Root** = Main filing cabinet drawer
- **Internal Nodes** = Sub-drawers within the main drawer
- **Leaf Nodes** = Individual file folders
- **Search Process** = Start at root, navigate through sub-drawers, find the folder

### SQL Example - B-Tree Index:
```sql
-- Create B-Tree index
CREATE INDEX idx_students_name ON students(last_name, first_name);

-- Query that uses B-Tree index efficiently
SELECT * FROM students 
WHERE last_name = 'Smith' 
AND first_name = 'John';

-- Range query that uses B-Tree index
SELECT * FROM students 
WHERE last_name BETWEEN 'A' AND 'M'
ORDER BY last_name, first_name;
```

## 5.3 Hash Indexes

Hash indexes use a hash function to map index keys to specific locations in the index. They provide very fast lookups but have limitations.

### Hash Index Characteristics:
- **Fast Lookups**: O(1) average time complexity
- **No Range Queries**: Cannot efficiently handle range operations
- **Memory Intensive**: Often stored in memory
- **Collision Handling**: Must handle hash collisions

### Real-World Analogy:
Hash index is like a parking garage with numbered spots:
- **Hash Function** = Parking spot assignment algorithm
- **Index Key** = License plate number
- **Hash Value** = Parking spot number
- **Collision** = Two cars assigned to same spot

### Java Example - Hash Index Simulation:
```java
import java.util.HashMap;
import java.util.Map;

public class HashIndexExample {
    private Map<String, Integer> hashIndex = new HashMap<>();
    
    // Simulate hash index creation
    public void createHashIndex() {
        // In real database, this would be done by the DBMS
        hashIndex.put("john@example.com", 1);
        hashIndex.put("jane@example.com", 2);
        hashIndex.put("bob@example.com", 3);
        System.out.println("Hash index created with " + hashIndex.size() + " entries");
    }
    
    // Fast lookup using hash index
    public Integer findStudentId(String email) {
        long startTime = System.nanoTime();
        Integer studentId = hashIndex.get(email);
        long endTime = System.nanoTime();
        
        System.out.println("Hash lookup took " + (endTime - startTime) + " nanoseconds");
        return studentId;
    }
}
```

## 5.4 Bitmap Indexes

Bitmap indexes use bit arrays to represent the presence or absence of values. They are particularly efficient for columns with low cardinality.

### Bitmap Index Characteristics:
- **Space Efficient**: One bit per row per distinct value
- **Fast Boolean Operations**: Efficient AND, OR, NOT operations
- **Low Cardinality**: Best for columns with few distinct values
- **Compression**: Can be highly compressed

### Real-World Analogy:
Bitmap index is like a seating chart:
- **Rows** = Seats in a theater
- **Columns** = Different attributes (VIP, Aisle, Window)
- **Bits** = 1 if seat has attribute, 0 if not
- **Query** = "Find all VIP aisle seats" = AND operation

### SQL Example - Bitmap Index:
```sql
-- Create bitmap index on low cardinality column
CREATE BITMAP INDEX idx_students_status ON students(status);

-- Query that benefits from bitmap index
SELECT * FROM students 
WHERE status = 'ACTIVE' 
AND department = 'COMPUTER_SCIENCE';

-- Multiple bitmap operations
SELECT * FROM students 
WHERE (status = 'ACTIVE' OR status = 'PENDING')
AND gpa > 3.0;
```

## 5.5 Composite Indexes

Composite indexes are created on multiple columns. The order of columns in the index is crucial for query performance.

### Composite Index Rules:
- **Leftmost Prefix**: Queries must use columns from left to right
- **Column Order**: Most selective columns should come first
- **Query Patterns**: Design based on actual query patterns
- **Size Consideration**: More columns = larger index

### Real-World Analogy:
Composite index is like a phone book sorted by last name, then first name:
- **Last Name** = Primary sort key
- **First Name** = Secondary sort key
- **Query "John Smith"** = Can use the index efficiently
- **Query "Smith"** = Can use the index efficiently
- **Query "John"** = Cannot use the index efficiently

### Java Example - Composite Index:
```java
public class CompositeIndexExample {
    private Connection connection;
    
    public CompositeIndexExample(Connection connection) {
        this.connection = connection;
    }
    
    // Create composite index
    public void createCompositeIndex() throws SQLException {
        String sql = "CREATE INDEX idx_students_dept_gpa ON students(department, gpa)";
        
        try (Statement stmt = connection.createStatement()) {
            stmt.execute(sql);
            System.out.println("Composite index created");
        }
    }
    
    // Query that uses composite index efficiently
    public void findStudentsByDeptAndGpa(String department, double minGpa) throws SQLException {
        String sql = "SELECT * FROM students WHERE department = ? AND gpa >= ?";
        
        try (PreparedStatement stmt = connection.prepareStatement(sql)) {
            stmt.setString(1, department);
            stmt.setDouble(2, minGpa);
            
            try (ResultSet rs = stmt.executeQuery()) {
                while (rs.next()) {
                    System.out.println("Student: " + rs.getString("first_name") + 
                                     " " + rs.getString("last_name"));
                }
            }
        }
    }
}
```

## 5.6 Partial Indexes

Partial indexes include only a subset of rows from a table, based on a WHERE condition. They are smaller and faster than full indexes.

### Partial Index Benefits:
- **Smaller Size**: Only index relevant rows
- **Faster Operations**: Less data to process
- **Storage Savings**: Reduced disk space usage
- **Maintenance Efficiency**: Faster index maintenance

### Real-World Analogy:
Partial index is like creating a VIP guest list:
- **Full Index** = List of all hotel guests
- **Partial Index** = List of only VIP guests
- **Query "Find VIP guests"** = Much faster with partial index
- **Query "Find all guests"** = Cannot use partial index

### SQL Example - Partial Index:
```sql
-- Create partial index for active students only
CREATE INDEX idx_active_students_gpa ON students(gpa) 
WHERE status = 'ACTIVE';

-- Query that uses partial index
SELECT * FROM students 
WHERE status = 'ACTIVE' 
AND gpa > 3.5;

-- This query cannot use the partial index
SELECT * FROM students 
WHERE gpa > 3.5;  -- status condition missing
```

## 5.7 Index Optimization

Index optimization involves analyzing query patterns and index usage to improve performance while minimizing overhead.

### Optimization Strategies:
- **Query Analysis**: Identify frequently used query patterns
- **Index Usage Monitoring**: Track which indexes are actually used
- **Duplicate Index Removal**: Remove redundant indexes
- **Index Consolidation**: Combine multiple indexes into one

### Real-World Analogy:
Index optimization is like organizing a library:
- **Analyze Usage** = See which books are checked out most
- **Remove Unused** = Remove books nobody reads
- **Consolidate** = Combine related book sections
- **Monitor Performance** = Track how quickly books are found

### Java Example - Index Optimization:
```java
public class IndexOptimization {
    private Connection connection;
    
    public IndexOptimization(Connection connection) {
        this.connection = connection;
    }
    
    // Analyze index usage
    public void analyzeIndexUsage() throws SQLException {
        String sql = """
            SELECT 
                index_name,
                table_name,
                cardinality,
                sub_part,
                packed,
                nullable,
                index_type
            FROM information_schema.statistics 
            WHERE table_schema = 'university_db'
            ORDER BY table_name, index_name
            """;
        
        try (Statement stmt = connection.createStatement();
             ResultSet rs = stmt.executeQuery(sql)) {
            
            System.out.println("Index Analysis:");
            while (rs.next()) {
                System.out.printf("Index: %s, Table: %s, Cardinality: %d%n",
                    rs.getString("index_name"),
                    rs.getString("table_name"),
                    rs.getLong("cardinality"));
            }
        }
    }
    
    // Find unused indexes
    public void findUnusedIndexes() throws SQLException {
        String sql = """
            SELECT 
                t.table_name,
                s.index_name,
                s.cardinality
            FROM information_schema.tables t
            LEFT JOIN information_schema.statistics s 
                ON t.table_name = s.table_name
            WHERE t.table_schema = 'university_db'
            AND s.index_name IS NOT NULL
            AND s.cardinality = 0
            """;
        
        try (Statement stmt = connection.createStatement();
             ResultSet rs = stmt.executeQuery(sql)) {
            
            System.out.println("Potentially Unused Indexes:");
            while (rs.next()) {
                System.out.println("Table: " + rs.getString("table_name") + 
                                 ", Index: " + rs.getString("index_name"));
            }
        }
    }
}
```

## 5.8 Index Maintenance

Index maintenance involves keeping indexes up-to-date and performing optimally as data changes.

### Maintenance Tasks:
- **Rebuilding**: Recreate indexes to eliminate fragmentation
- **Reorganizing**: Defragment indexes without rebuilding
- **Statistics Updates**: Keep index statistics current
- **Monitoring**: Track index health and performance

### Real-World Analogy:
Index maintenance is like maintaining a filing system:
- **Rebuilding** = Completely reorganize the filing system
- **Reorganizing** = Straighten up files without major changes
- **Statistics Updates** = Update the filing system index
- **Monitoring** = Check if files are easy to find

### Java Example - Index Maintenance:
```java
public class IndexMaintenance {
    private Connection connection;
    
    public IndexMaintenance(Connection connection) {
        this.connection = connection;
    }
    
    // Rebuild index
    public void rebuildIndex(String tableName, String indexName) throws SQLException {
        String sql = "ALTER INDEX " + indexName + " ON " + tableName + " REBUILD";
        
        try (Statement stmt = connection.createStatement()) {
            long startTime = System.currentTimeMillis();
            stmt.execute(sql);
            long endTime = System.currentTimeMillis();
            
            System.out.println("Index " + indexName + " rebuilt in " + 
                             (endTime - startTime) + "ms");
        }
    }
    
    // Update statistics
    public void updateStatistics(String tableName) throws SQLException {
        String sql = "UPDATE STATISTICS " + tableName;
        
        try (Statement stmt = connection.createStatement()) {
            stmt.execute(sql);
            System.out.println("Statistics updated for table " + tableName);
        }
    }
    
    // Check index fragmentation
    public void checkIndexFragmentation() throws SQLException {
        String sql = """
            SELECT 
                object_name(object_id) as table_name,
                index_id,
                avg_fragmentation_in_percent,
                page_count
            FROM sys.dm_db_index_physical_stats(DB_ID(), NULL, NULL, NULL, 'LIMITED')
            WHERE avg_fragmentation_in_percent > 10
            ORDER BY avg_fragmentation_in_percent DESC
            """;
        
        try (Statement stmt = connection.createStatement();
             ResultSet rs = stmt.executeQuery(sql)) {
            
            System.out.println("Fragmented Indexes:");
            while (rs.next()) {
                System.out.printf("Table: %s, Fragmentation: %.2f%%, Pages: %d%n",
                    rs.getString("table_name"),
                    rs.getDouble("avg_fragmentation_in_percent"),
                    rs.getLong("page_count"));
            }
        }
    }
}
```