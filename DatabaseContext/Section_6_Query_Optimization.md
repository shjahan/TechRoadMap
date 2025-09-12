# Section 6 – Query Optimization

## 6.1 Query Execution Plans

A query execution plan is a sequence of operations that the database engine uses to execute a SQL query. It shows how the database will access data, which indexes to use, and how to join tables.

### Key Components:
- **Operations**: Individual steps in query execution
- **Cost Estimates**: Predicted resource usage for each operation
- **Data Flow**: How data moves between operations
- **Index Usage**: Which indexes will be used
- **Join Methods**: How tables will be joined

### Real-World Analogy:
Query execution plan is like a recipe for cooking:
- **Ingredients** = Tables and data sources
- **Steps** = Individual cooking operations
- **Time Estimates** = Cost estimates for each step
- **Order** = Sequence of operations
- **Tools** = Indexes and optimization techniques

### Java Example - Execution Plan Analysis:
```java
import java.sql.*;

public class ExecutionPlanAnalyzer {
    private Connection connection;
    
    public ExecutionPlanAnalyzer(Connection connection) {
        this.connection = connection;
    }
    
    // Get execution plan for a query
    public void analyzeExecutionPlan(String query) throws SQLException {
        // Enable query plan collection
        try (Statement stmt = connection.createStatement()) {
            stmt.execute("SET profiling = 1");
        }
        
        // Execute the query
        try (PreparedStatement stmt = connection.prepareStatement(query);
             ResultSet rs = stmt.executeQuery()) {
            
            // Process results
            while (rs.next()) {
                // Process query results
            }
        }
        
        // Get execution plan
        String planQuery = "SHOW PROFILES";
        try (Statement stmt = connection.createStatement();
             ResultSet rs = stmt.executeQuery(planQuery)) {
            
            System.out.println("Query Execution Plan:");
            while (rs.next()) {
                System.out.printf("Query ID: %d, Duration: %s, Query: %s%n",
                    rs.getInt("Query_ID"),
                    rs.getString("Duration"),
                    rs.getString("Query"));
            }
        }
    }
    
    // Analyze slow queries
    public void analyzeSlowQueries() throws SQLException {
        String sql = """
            SELECT 
                query_time,
                lock_time,
                rows_sent,
                rows_examined,
                sql_text
            FROM mysql.slow_log
            WHERE start_time > DATE_SUB(NOW(), INTERVAL 1 HOUR)
            ORDER BY query_time DESC
            LIMIT 10
            """;
        
        try (Statement stmt = connection.createStatement();
             ResultSet rs = stmt.executeQuery(sql)) {
            
            System.out.println("Slow Queries Analysis:");
            while (rs.next()) {
                System.out.printf("Time: %s, Rows: %d, Query: %s%n",
                    rs.getString("query_time"),
                    rs.getInt("rows_examined"),
                    rs.getString("sql_text").substring(0, Math.min(100, rs.getString("sql_text").length())));
            }
        }
    }
}
```

## 6.2 Query Optimizer

The query optimizer is a component of the database engine that determines the most efficient way to execute a SQL query. It analyzes multiple execution strategies and selects the one with the lowest estimated cost.

### Optimizer Functions:
- **Parse Query**: Convert SQL to internal representation
- **Generate Plans**: Create multiple execution strategies
- **Cost Estimation**: Calculate resource usage for each plan
- **Plan Selection**: Choose the most efficient plan
- **Plan Execution**: Execute the selected plan

### Real-World Analogy:
Query optimizer is like a GPS navigation system:
- **Destination** = Query result
- **Multiple Routes** = Different execution plans
- **Traffic Analysis** = Cost estimation
- **Best Route** = Optimal execution plan
- **Real-time Updates** = Dynamic optimization

### SQL Example - Optimizer Hints:
```sql
-- Force index usage
SELECT * FROM students USE INDEX (idx_students_email) 
WHERE email = 'john@example.com';

-- Force table scan
SELECT * FROM students IGNORE INDEX (idx_students_email) 
WHERE email = 'john@example.com';

-- Optimize for specific join order
SELECT /*+ ORDERED */ s.*, c.*
FROM students s
JOIN enrollments e ON s.student_id = e.student_id
JOIN courses c ON e.course_id = c.course_id;

-- Use specific join algorithm
SELECT /*+ USE_HASH(s, e) */ s.*, e.*
FROM students s
JOIN enrollments e ON s.student_id = e.student_id;
```

## 6.3 Cost-Based Optimization

Cost-based optimization (CBO) uses statistical information about data distribution and system resources to estimate the cost of different execution plans.

### Cost Factors:
- **CPU Cost**: Processing time for operations
- **I/O Cost**: Disk read/write operations
- **Memory Cost**: RAM usage for operations
- **Network Cost**: Data transfer between nodes
- **Cardinality**: Number of rows in result sets

### Real-World Analogy:
Cost-based optimization is like choosing a transportation method:
- **Distance** = Data volume to process
- **Speed** = Processing power available
- **Cost** = Resource usage (fuel, time, money)
- **Traffic** = System load and contention
- **Best Choice** = Most cost-effective method

### Java Example - Cost Analysis:
```java
public class CostBasedOptimization {
    private Connection connection;
    
    public CostBasedOptimization(Connection connection) {
        this.connection = connection;
    }
    
    // Analyze table statistics
    public void analyzeTableStatistics(String tableName) throws SQLException {
        String sql = """
            SELECT 
                table_name,
                table_rows,
                avg_row_length,
                data_length,
                index_length,
                data_free
            FROM information_schema.tables
            WHERE table_schema = DATABASE()
            AND table_name = ?
            """;
        
        try (PreparedStatement stmt = connection.prepareStatement(sql)) {
            stmt.setString(1, tableName);
            
            try (ResultSet rs = stmt.executeQuery()) {
                if (rs.next()) {
                    System.out.println("Table Statistics for " + tableName + ":");
                    System.out.println("Rows: " + rs.getLong("table_rows"));
                    System.out.println("Avg Row Length: " + rs.getLong("avg_row_length"));
                    System.out.println("Data Length: " + rs.getLong("data_length"));
                    System.out.println("Index Length: " + rs.getLong("index_length"));
                }
            }
        }
    }
    
    // Update table statistics
    public void updateTableStatistics(String tableName) throws SQLException {
        String sql = "ANALYZE TABLE " + tableName;
        
        try (Statement stmt = connection.createStatement()) {
            stmt.execute(sql);
            System.out.println("Statistics updated for table " + tableName);
        }
    }
    
    // Compare query costs
    public void compareQueryCosts(String query1, String query2) throws SQLException {
        System.out.println("Comparing Query Costs:");
        
        // Execute first query and measure time
        long startTime = System.currentTimeMillis();
        executeQuery(query1);
        long endTime = System.currentTimeMillis();
        long query1Time = endTime - startTime;
        
        // Execute second query and measure time
        startTime = System.currentTimeMillis();
        executeQuery(query2);
        endTime = System.currentTimeMillis();
        long query2Time = endTime - startTime;
        
        System.out.println("Query 1 execution time: " + query1Time + "ms");
        System.out.println("Query 2 execution time: " + query2Time + "ms");
        System.out.println("Performance difference: " + Math.abs(query1Time - query2Time) + "ms");
    }
    
    private void executeQuery(String query) throws SQLException {
        try (Statement stmt = connection.createStatement();
             ResultSet rs = stmt.executeQuery(query)) {
            // Process results
            while (rs.next()) {
                // Minimal processing to measure execution time
            }
        }
    }
}
```

## 6.4 Rule-Based Optimization

Rule-based optimization (RBO) uses predefined rules and heuristics to determine query execution plans. It doesn't rely on statistical information about data distribution.

### RBO Rules:
- **Index Usage**: Use indexes when available
- **Join Order**: Join smaller tables first
- **Predicate Pushdown**: Apply filters as early as possible
- **Projection Pushdown**: Select only needed columns
- **Constant Folding**: Evaluate constant expressions

### Real-World Analogy:
Rule-based optimization is like following a recipe:
- **Recipe Steps** = Predefined optimization rules
- **Ingredient Order** = Join order rules
- **Cooking Time** = Execution time estimates
- **Standard Procedure** = Fixed optimization approach
- **No Adaptation** = Doesn't adjust to specific conditions

### SQL Example - Rule-Based Optimization:
```sql
-- Query that benefits from RBO rules
SELECT s.first_name, s.last_name, c.course_name
FROM students s
JOIN enrollments e ON s.student_id = e.student_id
JOIN courses c ON e.course_id = c.course_id
WHERE s.gpa > 3.5
AND c.department = 'COMPUTER_SCIENCE'
ORDER BY s.last_name;

-- RBO will typically:
-- 1. Apply WHERE clause filters first
-- 2. Use available indexes
-- 3. Join tables in order of size
-- 4. Apply ORDER BY last
```

## 6.5 Join Optimization

Join optimization focuses on efficiently combining data from multiple tables. The choice of join algorithm significantly impacts query performance.

### Join Algorithms:
- **Nested Loop Join**: For each row in outer table, scan inner table
- **Hash Join**: Build hash table from smaller table, probe with larger table
- **Sort-Merge Join**: Sort both tables, then merge sorted results
- **Index Nested Loop**: Use index to find matching rows

### Real-World Analogy:
Join optimization is like organizing a conference:
- **Nested Loop** = Check each attendee against each session
- **Hash Join** = Create a lookup table of sessions, then check attendees
- **Sort-Merge** = Sort attendees and sessions by time, then match
- **Index Nested Loop** = Use a schedule index to find matching sessions

### Java Example - Join Optimization:
```java
public class JoinOptimization {
    private Connection connection;
    
    public JoinOptimization(Connection connection) {
        this.connection = connection;
    }
    
    // Optimize join order
    public void optimizeJoinOrder() throws SQLException {
        // Query with suboptimal join order
        String suboptimalQuery = """
            SELECT s.first_name, s.last_name, c.course_name, e.grade
            FROM courses c
            JOIN enrollments e ON c.course_id = e.course_id
            JOIN students s ON e.student_id = s.student_id
            WHERE s.gpa > 3.0
            """;
        
        // Optimized query (smaller table first)
        String optimizedQuery = """
            SELECT s.first_name, s.last_name, c.course_name, e.grade
            FROM students s
            JOIN enrollments e ON s.student_id = e.student_id
            JOIN courses c ON e.course_id = c.course_id
            WHERE s.gpa > 3.0
            """;
        
        compareQueryPerformance(suboptimalQuery, optimizedQuery);
    }
    
    // Use appropriate join hints
    public void useJoinHints() throws SQLException {
        // Force hash join
        String hashJoinQuery = """
            SELECT /*+ USE_HASH(s, e) */ s.*, e.*
            FROM students s
            JOIN enrollments e ON s.student_id = e.student_id
            WHERE s.department = 'COMPUTER_SCIENCE'
            """;
        
        // Force nested loop join
        String nestedLoopQuery = """
            SELECT /*+ USE_NL(s, e) */ s.*, e.*
            FROM students s
            JOIN enrollments e ON s.student_id = e.student_id
            WHERE s.department = 'COMPUTER_SCIENCE'
            """;
        
        compareQueryPerformance(hashJoinQuery, nestedLoopQuery);
    }
    
    private void compareQueryPerformance(String query1, String query2) throws SQLException {
        System.out.println("Comparing join strategies:");
        
        long time1 = measureQueryTime(query1);
        long time2 = measureQueryTime(query2);
        
        System.out.println("Query 1 time: " + time1 + "ms");
        System.out.println("Query 2 time: " + time2 + "ms");
    }
    
    private long measureQueryTime(String query) throws SQLException {
        long startTime = System.currentTimeMillis();
        
        try (Statement stmt = connection.createStatement();
             ResultSet rs = stmt.executeQuery(query)) {
            while (rs.next()) {
                // Process results
            }
        }
        
        return System.currentTimeMillis() - startTime;
    }
}
```

## 6.6 Subquery Optimization

Subquery optimization involves transforming subqueries into more efficient forms, such as joins or derived tables, to improve performance.

### Subquery Types:
- **Correlated Subqueries**: Reference outer query columns
- **Uncorrelated Subqueries**: Independent of outer query
- **Scalar Subqueries**: Return single value
- **Table Subqueries**: Return multiple rows/columns

### Optimization Techniques:
- **Subquery to Join**: Convert subqueries to joins
- **EXISTS vs IN**: Choose appropriate subquery operator
- **Derived Tables**: Use temporary result sets
- **Window Functions**: Replace some subqueries with window functions

### Real-World Analogy:
Subquery optimization is like streamlining a multi-step process:
- **Original Process** = Nested subqueries
- **Streamlined Process** = Converted to joins
- **Efficiency Gain** = Reduced processing steps
- **Same Result** = Equivalent output

### SQL Example - Subquery Optimization:
```sql
-- Inefficient correlated subquery
SELECT s.first_name, s.last_name, s.gpa
FROM students s
WHERE s.gpa > (
    SELECT AVG(gpa) 
    FROM students s2 
    WHERE s2.department = s.department
);

-- Optimized using window function
SELECT first_name, last_name, gpa
FROM (
    SELECT first_name, last_name, gpa,
           AVG(gpa) OVER (PARTITION BY department) as dept_avg_gpa
    FROM students
) s
WHERE gpa > dept_avg_gpa;

-- Inefficient EXISTS subquery
SELECT s.first_name, s.last_name
FROM students s
WHERE EXISTS (
    SELECT 1 
    FROM enrollments e 
    WHERE e.student_id = s.student_id 
    AND e.grade = 'A'
);

-- Optimized using JOIN
SELECT DISTINCT s.first_name, s.last_name
FROM students s
JOIN enrollments e ON s.student_id = e.student_id
WHERE e.grade = 'A';
```

## 6.7 Query Hints and Directives

Query hints are instructions that guide the query optimizer to use specific execution strategies. They override the optimizer's automatic decisions.

### Common Hints:
- **Index Hints**: Force specific index usage
- **Join Hints**: Specify join algorithms
- **Query Hints**: Control overall execution strategy
- **Table Hints**: Influence table access methods

### Real-World Analogy:
Query hints are like giving specific instructions to a GPS:
- **"Avoid Highways"** = Index hint
- **"Use Fastest Route"** = Join hint
- **"Take Scenic Route"** = Query hint
- **"Avoid Tolls"** = Table hint

### Java Example - Query Hints:
```java
public class QueryHints {
    private Connection connection;
    
    public QueryHints(Connection connection) {
        this.connection = connection;
    }
    
    // Use index hints
    public void useIndexHints() throws SQLException {
        // Force index usage
        String sql = """
            SELECT /*+ USE_INDEX(students, idx_students_email) */ 
                   first_name, last_name, email
            FROM students 
            WHERE email LIKE '%@university.edu'
            """;
        
        executeQueryWithTiming(sql, "With index hint");
        
        // Ignore specific index
        String sqlIgnore = """
            SELECT /*+ IGNORE_INDEX(students, idx_students_email) */ 
                   first_name, last_name, email
            FROM students 
            WHERE email LIKE '%@university.edu'
            """;
        
        executeQueryWithTiming(sqlIgnore, "Ignoring index");
    }
    
    // Use join hints
    public void useJoinHints() throws SQLException {
        // Force hash join
        String hashJoin = """
            SELECT /*+ USE_HASH(s, e) */ s.first_name, e.grade
            FROM students s
            JOIN enrollments e ON s.student_id = e.student_id
            WHERE s.gpa > 3.5
            """;
        
        executeQueryWithTiming(hashJoin, "Hash join");
        
        // Force nested loop join
        String nestedLoop = """
            SELECT /*+ USE_NL(s, e) */ s.first_name, e.grade
            FROM students s
            JOIN enrollments e ON s.student_id = e.student_id
            WHERE s.gpa > 3.5
            """;
        
        executeQueryWithTiming(nestedLoop, "Nested loop join");
    }
    
    // Use query hints
    public void useQueryHints() throws SQLException {
        // Optimize for first rows
        String firstRows = """
            SELECT /*+ FIRST_ROWS(10) */ first_name, last_name, gpa
            FROM students
            ORDER BY gpa DESC
            """;
        
        executeQueryWithTiming(firstRows, "First rows optimization");
        
        // Optimize for all rows
        String allRows = """
            SELECT /*+ ALL_ROWS */ first_name, last_name, gpa
            FROM students
            ORDER BY gpa DESC
            """;
        
        executeQueryWithTiming(allRows, "All rows optimization");
    }
    
    private void executeQueryWithTiming(String sql, String description) throws SQLException {
        long startTime = System.currentTimeMillis();
        
        try (Statement stmt = connection.createStatement();
             ResultSet rs = stmt.executeQuery(sql)) {
            
            int rowCount = 0;
            while (rs.next()) {
                rowCount++;
            }
            
            long endTime = System.currentTimeMillis();
            System.out.println(description + ": " + (endTime - startTime) + "ms, " + rowCount + " rows");
        }
    }
}
```

## 6.8 Performance Tuning

Performance tuning involves systematically identifying and resolving performance bottlenecks in database queries and operations.

### Tuning Process:
- **Identify Bottlenecks**: Find slow queries and operations
- **Analyze Root Causes**: Understand why performance is poor
- **Apply Solutions**: Implement optimizations
- **Measure Impact**: Verify performance improvements
- **Monitor Continuously**: Track performance over time

### Real-World Analogy:
Performance tuning is like tuning a car engine:
- **Diagnose Problems** = Identify performance issues
- **Adjust Settings** = Apply optimizations
- **Test Performance** = Measure improvements
- **Fine-tune** = Make additional adjustments
- **Regular Maintenance** = Ongoing monitoring

### Java Example - Performance Tuning:
```java
public class PerformanceTuning {
    private Connection connection;
    
    public PerformanceTuning(Connection connection) {
        this.connection = connection;
    }
    
    // Identify slow queries
    public void identifySlowQueries() throws SQLException {
        String sql = """
            SELECT 
                query_time,
                lock_time,
                rows_sent,
                rows_examined,
                sql_text
            FROM mysql.slow_log
            WHERE start_time > DATE_SUB(NOW(), INTERVAL 1 DAY)
            ORDER BY query_time DESC
            LIMIT 20
            """;
        
        try (Statement stmt = connection.createStatement();
             ResultSet rs = stmt.executeQuery(sql)) {
            
            System.out.println("Slow Queries Report:");
            while (rs.next()) {
                System.out.printf("Time: %s, Rows Examined: %d, Query: %s%n",
                    rs.getString("query_time"),
                    rs.getInt("rows_examined"),
                    rs.getString("sql_text").substring(0, Math.min(80, rs.getString("sql_text").length())));
            }
        }
    }
    
    // Analyze query execution
    public void analyzeQueryExecution(String query) throws SQLException {
        // Enable query profiling
        try (Statement stmt = connection.createStatement()) {
            stmt.execute("SET profiling = 1");
        }
        
        // Execute query
        try (PreparedStatement stmt = connection.prepareStatement(query);
             ResultSet rs = stmt.executeQuery()) {
            
            // Process results
            while (rs.next()) {
                // Minimal processing
            }
        }
        
        // Get detailed execution information
        String profileQuery = "SHOW PROFILE FOR QUERY 1";
        try (Statement stmt = connection.createStatement();
             ResultSet rs = stmt.executeQuery(profileQuery)) {
            
            System.out.println("Query Execution Profile:");
            while (rs.next()) {
                System.out.printf("Step: %s, Duration: %s%n",
                    rs.getString("Status"),
                    rs.getString("Duration"));
            }
        }
    }
    
    // Optimize query performance
    public void optimizeQuery(String originalQuery, String optimizedQuery) throws SQLException {
        System.out.println("Query Optimization Analysis:");
        
        // Measure original query
        long originalTime = measureQueryTime(originalQuery);
        System.out.println("Original query time: " + originalTime + "ms");
        
        // Measure optimized query
        long optimizedTime = measureQueryTime(optimizedQuery);
        System.out.println("Optimized query time: " + optimizedTime + "ms");
        
        // Calculate improvement
        double improvement = ((double)(originalTime - optimizedTime) / originalTime) * 100;
        System.out.println("Performance improvement: " + String.format("%.2f", improvement) + "%");
    }
    
    private long measureQueryTime(String query) throws SQLException {
        long startTime = System.currentTimeMillis();
        
        try (Statement stmt = connection.createStatement();
             ResultSet rs = stmt.executeQuery(query)) {
            while (rs.next()) {
                // Process results
            }
        }
        
        return System.currentTimeMillis() - startTime;
    }
}
```