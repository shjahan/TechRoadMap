# Section 22 – Database Testing

## 22.1 Unit Testing for Databases

Unit testing for databases involves testing individual database components in isolation to ensure they work correctly.

### Testing Areas:
- **Stored Procedures**: Test individual procedures
- **Functions**: Test database functions
- **Triggers**: Test trigger behavior
- **Views**: Test view functionality
- **Constraints**: Test data constraints
- **Indexes**: Test index performance

### Real-World Analogy:
Unit testing is like testing individual car parts:
- **Stored Procedures** = Test engine
- **Functions** = Test transmission
- **Triggers** = Test safety systems
- **Views** = Test dashboard
- **Constraints** = Test safety features
- **Indexes** = Test performance

### Java Example - Database Unit Testing:
```java
import java.sql.*;
import java.util.*;

public class DatabaseUnitTesting {
    private Connection connection;
    
    public DatabaseUnitTesting(Connection connection) {
        this.connection = connection;
    }
    
    // Test stored procedure
    public void testStoredProcedure() throws SQLException {
        System.out.println("Testing stored procedure...");
        
        // Test with valid input
        String sql = "CALL GetUserById(?)";
        try (CallableStatement stmt = connection.prepareCall(sql)) {
            stmt.setInt(1, 1);
            
            try (ResultSet rs = stmt.executeQuery()) {
                assert rs.next() : "Expected at least one result";
                assert rs.getString("username") != null : "Username should not be null";
                System.out.println("Stored procedure test passed");
            }
        }
    }
    
    // Test database function
    public void testDatabaseFunction() throws SQLException {
        System.out.println("Testing database function...");
        
        String sql = "SELECT GetUserCount()";
        try (Statement stmt = connection.createStatement();
             ResultSet rs = stmt.executeQuery(sql)) {
            
            if (rs.next()) {
                int count = rs.getInt(1);
                assert count >= 0 : "User count should be non-negative";
                System.out.println("Database function test passed: " + count + " users");
            }
        }
    }
    
    // Test trigger
    public void testTrigger() throws SQLException {
        System.out.println("Testing trigger...");
        
        // Insert test data
        String insertSQL = "INSERT INTO users (username, email) VALUES (?, ?)";
        try (PreparedStatement stmt = connection.prepareStatement(insertSQL)) {
            stmt.setString(1, "testuser");
            stmt.setString(2, "test@example.com");
            stmt.executeUpdate();
        }
        
        // Check if trigger fired
        String checkSQL = "SELECT COUNT(*) FROM user_audit WHERE action = 'INSERT'";
        try (Statement stmt = connection.createStatement();
             ResultSet rs = stmt.executeQuery(checkSQL)) {
            
            if (rs.next()) {
                int count = rs.getInt(1);
                assert count > 0 : "Trigger should have fired";
                System.out.println("Trigger test passed: " + count + " audit records");
            }
        }
    }
    
    // Test view
    public void testView() throws SQLException {
        System.out.println("Testing view...");
        
        String sql = "SELECT * FROM user_posts_view LIMIT 1";
        try (Statement stmt = connection.createStatement();
             ResultSet rs = stmt.executeQuery(sql)) {
            
            if (rs.next()) {
                assert rs.getString("username") != null : "Username should not be null";
                assert rs.getString("title") != null : "Title should not be null";
                System.out.println("View test passed");
            }
        }
    }
    
    // Test constraints
    public void testConstraints() throws SQLException {
        System.out.println("Testing constraints...");
        
        // Test unique constraint
        String sql = "INSERT INTO users (username, email) VALUES (?, ?)";
        try (PreparedStatement stmt = connection.prepareStatement(sql)) {
            stmt.setString(1, "duplicate_user");
            stmt.setString(2, "duplicate@example.com");
            stmt.executeUpdate();
            
            // Try to insert duplicate
            stmt.setString(1, "duplicate_user");
            stmt.setString(2, "duplicate2@example.com");
            
            try {
                stmt.executeUpdate();
                assert false : "Should have thrown exception for duplicate username";
            } catch (SQLException e) {
                System.out.println("Unique constraint test passed");
            }
        }
    }
}
```

## 22.2 Integration Testing

Integration testing involves testing how different database components work together.

### Testing Areas:
- **Data Flow**: Test data flow between components
- **Transaction Management**: Test transaction handling
- **Concurrency**: Test concurrent operations
- **Data Consistency**: Test data consistency
- **Performance**: Test integrated performance
- **Error Handling**: Test error propagation

### Real-World Analogy:
Integration testing is like testing how car systems work together:
- **Data Flow** = Test fuel flow
- **Transaction Management** = Test gear shifting
- **Concurrency** = Test multiple systems
- **Data Consistency** = Test synchronization
- **Performance** = Test overall performance
- **Error Handling** = Test error recovery

### Java Example - Integration Testing:
```java
import java.sql.*;
import java.util.*;

public class DatabaseIntegrationTesting {
    private Connection connection;
    
    public DatabaseIntegrationTesting(Connection connection) {
        this.connection = connection;
    }
    
    // Test data flow
    public void testDataFlow() throws SQLException {
        System.out.println("Testing data flow...");
        
        // Insert user
        String insertUserSQL = "INSERT INTO users (username, email) VALUES (?, ?)";
        int userId = 0;
        
        try (PreparedStatement stmt = connection.prepareStatement(insertUserSQL, Statement.RETURN_GENERATED_KEYS)) {
            stmt.setString(1, "testuser");
            stmt.setString(2, "test@example.com");
            stmt.executeUpdate();
            
            try (ResultSet rs = stmt.getGeneratedKeys()) {
                if (rs.next()) {
                    userId = rs.getInt(1);
                }
            }
        }
        
        // Insert post for user
        String insertPostSQL = "INSERT INTO posts (user_id, title, content) VALUES (?, ?, ?)";
        try (PreparedStatement stmt = connection.prepareStatement(insertPostSQL)) {
            stmt.setInt(1, userId);
            stmt.setString(2, "Test Post");
            stmt.setString(3, "This is a test post");
            stmt.executeUpdate();
        }
        
        // Verify data flow
        String verifySQL = "SELECT u.username, p.title FROM users u JOIN posts p ON u.id = p.user_id WHERE u.id = ?";
        try (PreparedStatement stmt = connection.prepareStatement(verifySQL)) {
            stmt.setInt(1, userId);
            
            try (ResultSet rs = stmt.executeQuery()) {
                assert rs.next() : "Expected data flow result";
                assert "testuser".equals(rs.getString("username")) : "Username mismatch";
                assert "Test Post".equals(rs.getString("title")) : "Title mismatch";
                System.out.println("Data flow test passed");
            }
        }
    }
    
    // Test transaction management
    public void testTransactionManagement() throws SQLException {
        System.out.println("Testing transaction management...");
        
        connection.setAutoCommit(false);
        
        try {
            // First operation
            String sql1 = "INSERT INTO users (username, email) VALUES (?, ?)";
            try (PreparedStatement stmt = connection.prepareStatement(sql1)) {
                stmt.setString(1, "txuser1");
                stmt.setString(2, "txuser1@example.com");
                stmt.executeUpdate();
            }
            
            // Second operation
            String sql2 = "INSERT INTO posts (user_id, title) VALUES (?, ?)";
            try (PreparedStatement stmt = connection.prepareStatement(sql2)) {
                stmt.setInt(1, 1);
                stmt.setString(2, "Transaction Post");
                stmt.executeUpdate();
            }
            
            // Commit transaction
            connection.commit();
            System.out.println("Transaction management test passed");
            
        } catch (SQLException e) {
            connection.rollback();
            System.err.println("Transaction rolled back: " + e.getMessage());
            throw e;
        } finally {
            connection.setAutoCommit(true);
        }
    }
    
    // Test concurrency
    public void testConcurrency() throws SQLException {
        System.out.println("Testing concurrency...");
        
        // Simulate concurrent access
        List<Thread> threads = new ArrayList<>();
        int numberOfThreads = 5;
        
        for (int i = 0; i < numberOfThreads; i++) {
            final int threadId = i;
            Thread thread = new Thread(() -> {
                try {
                    String sql = "INSERT INTO users (username, email) VALUES (?, ?)";
                    try (PreparedStatement stmt = connection.prepareStatement(sql)) {
                        stmt.setString(1, "concurrent_user_" + threadId);
                        stmt.setString(2, "concurrent" + threadId + "@example.com");
                        stmt.executeUpdate();
                    }
                } catch (SQLException e) {
                    System.err.println("Concurrency test error: " + e.getMessage());
                }
            });
            
            threads.add(thread);
            thread.start();
        }
        
        // Wait for all threads to complete
        for (Thread thread : threads) {
            try {
                thread.join();
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        }
        
        System.out.println("Concurrency test completed");
    }
}
```

## 22.3 Performance Testing

Performance testing involves testing database performance under various conditions.

### Testing Areas:
- **Load Testing**: Test under normal load
- **Stress Testing**: Test under high load
- **Volume Testing**: Test with large data volumes
- **Response Time**: Test query response times
- **Throughput**: Test transaction throughput
- **Resource Usage**: Test resource consumption

### Real-World Analogy:
Performance testing is like testing car performance:
- **Load Testing** = Test normal driving
- **Stress Testing** = Test high-speed driving
- **Volume Testing** = Test with heavy load
- **Response Time** = Test acceleration
- **Throughput** = Test fuel efficiency
- **Resource Usage** = Test fuel consumption

### Java Example - Performance Testing:
```java
import java.sql.*;
import java.util.*;

public class DatabasePerformanceTesting {
    private Connection connection;
    
    public DatabasePerformanceTesting(Connection connection) {
        this.connection = connection;
    }
    
    // Test query performance
    public void testQueryPerformance() throws SQLException {
        System.out.println("Testing query performance...");
        
        String sql = "SELECT * FROM users WHERE created_at > DATE_SUB(NOW(), INTERVAL 1 DAY)";
        
        long startTime = System.currentTimeMillis();
        
        try (Statement stmt = connection.createStatement();
             ResultSet rs = stmt.executeQuery(sql)) {
            
            int count = 0;
            while (rs.next()) {
                count++;
            }
            
            long endTime = System.currentTimeMillis();
            long executionTime = endTime - startTime;
            
            System.out.println("Query executed in " + executionTime + "ms");
            System.out.println("Records returned: " + count);
            
            if (executionTime > 1000) {
                System.out.println("WARNING: Query execution time exceeds 1 second");
            }
        }
    }
    
    // Test load performance
    public void testLoadPerformance() throws SQLException {
        System.out.println("Testing load performance...");
        
        int numberOfQueries = 100;
        long totalTime = 0;
        
        for (int i = 0; i < numberOfQueries; i++) {
            String sql = "SELECT COUNT(*) FROM users";
            
            long startTime = System.currentTimeMillis();
            
            try (Statement stmt = connection.createStatement();
                 ResultSet rs = stmt.executeQuery(sql)) {
                
                if (rs.next()) {
                    rs.getInt(1);
                }
            }
            
            long endTime = System.currentTimeMillis();
            totalTime += (endTime - startTime);
        }
        
        double averageTime = (double) totalTime / numberOfQueries;
        System.out.println("Average query time: " + averageTime + "ms");
        System.out.println("Total time: " + totalTime + "ms");
    }
    
    // Test stress performance
    public void testStressPerformance() throws SQLException {
        System.out.println("Testing stress performance...");
        
        int numberOfThreads = 10;
        int queriesPerThread = 50;
        List<Thread> threads = new ArrayList<>();
        
        for (int i = 0; i < numberOfThreads; i++) {
            Thread thread = new Thread(() -> {
                try {
                    for (int j = 0; j < queriesPerThread; j++) {
                        String sql = "SELECT * FROM users WHERE id = ?";
                        try (PreparedStatement stmt = connection.prepareStatement(sql)) {
                            stmt.setInt(1, j % 100 + 1);
                            try (ResultSet rs = stmt.executeQuery()) {
                                // Process result
                            }
                        }
                    }
                } catch (SQLException e) {
                    System.err.println("Stress test error: " + e.getMessage());
                }
            });
            
            threads.add(thread);
            thread.start();
        }
        
        // Wait for all threads to complete
        for (Thread thread : threads) {
            try {
                thread.join();
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        }
        
        System.out.println("Stress test completed");
    }
}
```

## 22.4 Load Testing

Load testing involves testing database performance under expected load conditions.

### Testing Areas:
- **Concurrent Users**: Test with multiple users
- **Query Load**: Test with multiple queries
- **Data Volume**: Test with large datasets
- **Connection Pool**: Test connection pooling
- **Memory Usage**: Test memory consumption
- **CPU Usage**: Test CPU utilization

### Real-World Analogy:
Load testing is like testing a bridge:
- **Concurrent Users** = Multiple vehicles
- **Query Load** = Traffic volume
- **Data Volume** = Bridge weight capacity
- **Connection Pool** = Traffic lanes
- **Memory Usage** = Bridge stress
- **CPU Usage** = Bridge load

### Java Example - Load Testing:
```java
import java.sql.*;
import java.util.*;
import java.util.concurrent.*;

public class DatabaseLoadTesting {
    private Connection connection;
    private ExecutorService executor;
    
    public DatabaseLoadTesting(Connection connection) {
        this.connection = connection;
        this.executor = Executors.newFixedThreadPool(10);
    }
    
    // Test concurrent users
    public void testConcurrentUsers() throws SQLException {
        System.out.println("Testing concurrent users...");
        
        int numberOfUsers = 20;
        List<Future<Long>> futures = new ArrayList<>();
        
        for (int i = 0; i < numberOfUsers; i++) {
            final int userId = i;
            Future<Long> future = executor.submit(() -> {
                long startTime = System.currentTimeMillis();
                
                try {
                    String sql = "SELECT * FROM users WHERE id = ?";
                    try (PreparedStatement stmt = connection.prepareStatement(sql)) {
                        stmt.setInt(1, userId % 100 + 1);
                        try (ResultSet rs = stmt.executeQuery()) {
                            while (rs.next()) {
                                // Process result
                            }
                        }
                    }
                } catch (SQLException e) {
                    System.err.println("Concurrent user error: " + e.getMessage());
                }
                
                return System.currentTimeMillis() - startTime;
            });
            
            futures.add(future);
        }
        
        // Collect results
        long totalTime = 0;
        for (Future<Long> future : futures) {
            try {
                totalTime += future.get();
            } catch (InterruptedException | ExecutionException e) {
                System.err.println("Error getting future result: " + e.getMessage());
            }
        }
        
        double averageTime = (double) totalTime / numberOfUsers;
        System.out.println("Average response time: " + averageTime + "ms");
    }
    
    // Test query load
    public void testQueryLoad() throws SQLException {
        System.out.println("Testing query load...");
        
        int numberOfQueries = 1000;
        long startTime = System.currentTimeMillis();
        
        for (int i = 0; i < numberOfQueries; i++) {
            String sql = "SELECT COUNT(*) FROM users";
            try (Statement stmt = connection.createStatement();
                 ResultSet rs = stmt.executeQuery(sql)) {
                // Process result
            }
        }
        
        long endTime = System.currentTimeMillis();
        long totalTime = endTime - startTime;
        double queriesPerSecond = (double) numberOfQueries / (totalTime / 1000.0);
        
        System.out.println("Queries per second: " + queriesPerSecond);
        System.out.println("Total time: " + totalTime + "ms");
    }
    
    // Test data volume
    public void testDataVolume() throws SQLException {
        System.out.println("Testing data volume...");
        
        // Insert large amount of data
        String sql = "INSERT INTO users (username, email) VALUES (?, ?)";
        int numberOfRecords = 10000;
        
        long startTime = System.currentTimeMillis();
        
        try (PreparedStatement stmt = connection.prepareStatement(sql)) {
            for (int i = 0; i < numberOfRecords; i++) {
                stmt.setString(1, "user_" + i);
                stmt.setString(2, "user" + i + "@example.com");
                stmt.addBatch();
                
                if (i % 1000 == 0) {
                    stmt.executeBatch();
                }
            }
            stmt.executeBatch();
        }
        
        long endTime = System.currentTimeMillis();
        long totalTime = endTime - startTime;
        double recordsPerSecond = (double) numberOfRecords / (totalTime / 1000.0);
        
        System.out.println("Records inserted: " + numberOfRecords);
        System.out.println("Records per second: " + recordsPerSecond);
        System.out.println("Total time: " + totalTime + "ms");
    }
    
    // Shutdown executor
    public void shutdown() {
        executor.shutdown();
        try {
            if (!executor.awaitTermination(60, TimeUnit.SECONDS)) {
                executor.shutdownNow();
            }
        } catch (InterruptedException e) {
            executor.shutdownNow();
            Thread.currentThread().interrupt();
        }
    }
}
```

## 22.5 Stress Testing

Stress testing involves testing database performance under extreme conditions.

### Testing Areas:
- **High Load**: Test under very high load
- **Resource Limits**: Test resource exhaustion
- **Error Conditions**: Test error handling
- **Recovery**: Test recovery from stress
- **Stability**: Test system stability
- **Degradation**: Test performance degradation

### Real-World Analogy:
Stress testing is like testing a car at its limits:
- **High Load** = Maximum speed
- **Resource Limits** = Fuel exhaustion
- **Error Conditions** = Engine failure
- **Recovery** = Recovery from failure
- **Stability** = System stability
- **Degradation** = Performance degradation

### Java Example - Stress Testing:
```java
import java.sql.*;
import java.util.*;
import java.util.concurrent.*;

public class DatabaseStressTesting {
    private Connection connection;
    private ExecutorService executor;
    
    public DatabaseStressTesting(Connection connection) {
        this.connection = connection;
        this.executor = Executors.newFixedThreadPool(50);
    }
    
    // Test high load
    public void testHighLoad() throws SQLException {
        System.out.println("Testing high load...");
        
        int numberOfThreads = 100;
        int queriesPerThread = 100;
        List<Future<Long>> futures = new ArrayList<>();
        
        for (int i = 0; i < numberOfThreads; i++) {
            final int threadId = i;
            Future<Long> future = executor.submit(() -> {
                long startTime = System.currentTimeMillis();
                
                try {
                    for (int j = 0; j < queriesPerThread; j++) {
                        String sql = "SELECT * FROM users WHERE id = ?";
                        try (PreparedStatement stmt = connection.prepareStatement(sql)) {
                            stmt.setInt(1, (threadId * queriesPerThread + j) % 1000 + 1);
                            try (ResultSet rs = stmt.executeQuery()) {
                                while (rs.next()) {
                                    // Process result
                                }
                            }
                        }
                    }
                } catch (SQLException e) {
                    System.err.println("High load test error: " + e.getMessage());
                }
                
                return System.currentTimeMillis() - startTime;
            });
            
            futures.add(future);
        }
        
        // Collect results
        long totalTime = 0;
        int successfulThreads = 0;
        
        for (Future<Long> future : futures) {
            try {
                totalTime += future.get();
                successfulThreads++;
            } catch (InterruptedException | ExecutionException e) {
                System.err.println("Error getting future result: " + e.getMessage());
            }
        }
        
        double averageTime = (double) totalTime / successfulThreads;
        System.out.println("Successful threads: " + successfulThreads);
        System.out.println("Average response time: " + averageTime + "ms");
    }
    
    // Test resource limits
    public void testResourceLimits() throws SQLException {
        System.out.println("Testing resource limits...");
        
        // Test connection limit
        List<Connection> connections = new ArrayList<>();
        int maxConnections = 100;
        
        try {
            for (int i = 0; i < maxConnections; i++) {
                Connection conn = DriverManager.getConnection(
                    "jdbc:mysql://localhost:3306/database", "username", "password");
                connections.add(conn);
            }
            
            System.out.println("Created " + connections.size() + " connections");
            
        } catch (SQLException e) {
            System.out.println("Connection limit reached: " + e.getMessage());
        } finally {
            // Close all connections
            for (Connection conn : connections) {
                try {
                    conn.close();
                } catch (SQLException e) {
                    System.err.println("Error closing connection: " + e.getMessage());
                }
            }
        }
    }
    
    // Test error conditions
    public void testErrorConditions() throws SQLException {
        System.out.println("Testing error conditions...");
        
        // Test invalid query
        try {
            String sql = "SELECT * FROM non_existent_table";
            try (Statement stmt = connection.createStatement();
                 ResultSet rs = stmt.executeQuery(sql)) {
                // This should throw an exception
            }
        } catch (SQLException e) {
            System.out.println("Error condition test passed: " + e.getMessage());
        }
        
        // Test invalid data
        try {
            String sql = "INSERT INTO users (username, email) VALUES (?, ?)";
            try (PreparedStatement stmt = connection.prepareStatement(sql)) {
                stmt.setString(1, null); // Invalid data
                stmt.setString(2, "test@example.com");
                stmt.executeUpdate();
            }
        } catch (SQLException e) {
            System.out.println("Invalid data test passed: " + e.getMessage());
        }
    }
    
    // Shutdown executor
    public void shutdown() {
        executor.shutdown();
        try {
            if (!executor.awaitTermination(60, TimeUnit.SECONDS)) {
                executor.shutdownNow();
            }
        } catch (InterruptedException e) {
            executor.shutdownNow();
            Thread.currentThread().interrupt();
        }
    }
}
```

## 22.6 Security Testing

Security testing involves testing database security measures and vulnerabilities.

### Testing Areas:
- **Authentication**: Test user authentication
- **Authorization**: Test access control
- **SQL Injection**: Test SQL injection vulnerabilities
- **Data Encryption**: Test data encryption
- **Audit Logging**: Test audit logging
- **Access Control**: Test access restrictions

### Real-World Analogy:
Security testing is like testing building security:
- **Authentication** = Test access cards
- **Authorization** = Test permission levels
- **SQL Injection** = Test for forced entry
- **Data Encryption** = Test safe locks
- **Audit Logging** = Test security cameras
- **Access Control** = Test door locks

### Java Example - Security Testing:
```java
import java.sql.*;
import java.util.*;

public class DatabaseSecurityTesting {
    private Connection connection;
    
    public DatabaseSecurityTesting(Connection connection) {
        this.connection = connection;
    }
    
    // Test authentication
    public void testAuthentication() throws SQLException {
        System.out.println("Testing authentication...");
        
        // Test valid credentials
        try (Connection conn = DriverManager.getConnection(
                "jdbc:mysql://localhost:3306/database", "valid_user", "valid_password")) {
            System.out.println("Valid authentication test passed");
        } catch (SQLException e) {
            System.out.println("Valid authentication test failed: " + e.getMessage());
        }
        
        // Test invalid credentials
        try (Connection conn = DriverManager.getConnection(
                "jdbc:mysql://localhost:3306/database", "invalid_user", "invalid_password")) {
            System.out.println("Invalid authentication test failed");
        } catch (SQLException e) {
            System.out.println("Invalid authentication test passed: " + e.getMessage());
        }
    }
    
    // Test SQL injection
    public void testSQLInjection() throws SQLException {
        System.out.println("Testing SQL injection...");
        
        // Test SQL injection attempt
        String maliciousInput = "'; DROP TABLE users; --";
        String sql = "SELECT * FROM users WHERE username = ?";
        
        try (PreparedStatement stmt = connection.prepareStatement(sql)) {
            stmt.setString(1, maliciousInput);
            try (ResultSet rs = stmt.executeQuery()) {
                // This should not execute the DROP TABLE command
                System.out.println("SQL injection test passed - no data dropped");
            }
        }
    }
    
    // Test authorization
    public void testAuthorization() throws SQLException {
        System.out.println("Testing authorization...");
        
        // Test user permissions
        String sql = "SELECT * FROM information_schema.user_privileges WHERE grantee = ?";
        try (PreparedStatement stmt = connection.prepareStatement(sql)) {
            stmt.setString(1, "current_user");
            
            try (ResultSet rs = stmt.executeQuery()) {
                System.out.println("User privileges:");
                while (rs.next()) {
                    System.out.println("  " + rs.getString("privilege_type"));
                }
            }
        }
    }
    
    // Test data encryption
    public void testDataEncryption() throws SQLException {
        System.out.println("Testing data encryption...");
        
        // Check if data is encrypted
        String sql = "SHOW VARIABLES LIKE 'innodb_encryption%'";
        try (Statement stmt = connection.createStatement();
             ResultSet rs = stmt.executeQuery(sql)) {
            
            System.out.println("Encryption settings:");
            while (rs.next()) {
                System.out.println("  " + rs.getString("Variable_name") + " = " + rs.getString("Value"));
            }
        }
    }
    
    // Test audit logging
    public void testAuditLogging() throws SQLException {
        System.out.println("Testing audit logging...");
        
        // Check if audit logging is enabled
        String sql = "SHOW VARIABLES LIKE 'audit%'";
        try (Statement stmt = connection.createStatement();
             ResultSet rs = stmt.executeQuery(sql)) {
            
            System.out.println("Audit settings:");
            while (rs.next()) {
                System.out.println("  " + rs.getString("Variable_name") + " = " + rs.getString("Value"));
            }
        }
    }
}
```

## 22.7 Data Quality Testing

Data quality testing involves testing data integrity, accuracy, and consistency.

### Testing Areas:
- **Data Integrity**: Test data consistency
- **Data Accuracy**: Test data correctness
- **Data Completeness**: Test data completeness
- **Data Validity**: Test data validity
- **Data Consistency**: Test data consistency
- **Data Timeliness**: Test data freshness

### Real-World Analogy:
Data quality testing is like quality control in manufacturing:
- **Data Integrity** = Check product integrity
- **Data Accuracy** = Check product accuracy
- **Data Completeness** = Check product completeness
- **Data Validity** = Check product validity
- **Data Consistency** = Check product consistency
- **Data Timeliness** = Check product freshness

### Java Example - Data Quality Testing:
```java
import java.sql.*;
import java.util.*;

public class DatabaseDataQualityTesting {
    private Connection connection;
    
    public DatabaseDataQualityTesting(Connection connection) {
        this.connection = connection;
    }
    
    // Test data integrity
    public void testDataIntegrity() throws SQLException {
        System.out.println("Testing data integrity...");
        
        // Test foreign key constraints
        String sql = "SELECT COUNT(*) FROM posts p LEFT JOIN users u ON p.user_id = u.id WHERE u.id IS NULL";
        try (Statement stmt = connection.createStatement();
             ResultSet rs = stmt.executeQuery(sql)) {
            
            if (rs.next()) {
                int orphanedRecords = rs.getInt(1);
                if (orphanedRecords > 0) {
                    System.out.println("Data integrity violation: " + orphanedRecords + " orphaned records");
                } else {
                    System.out.println("Data integrity test passed: No orphaned records");
                }
            }
        }
    }
    
    // Test data accuracy
    public void testDataAccuracy() throws SQLException {
        System.out.println("Testing data accuracy...");
        
        // Test email format
        String sql = "SELECT COUNT(*) FROM users WHERE email NOT LIKE '%@%.%'";
        try (Statement stmt = connection.createStatement();
             ResultSet rs = stmt.executeQuery(sql)) {
            
            if (rs.next()) {
                int invalidEmails = rs.getInt(1);
                if (invalidEmails > 0) {
                    System.out.println("Data accuracy violation: " + invalidEmails + " invalid emails");
                } else {
                    System.out.println("Data accuracy test passed: All emails valid");
                }
            }
        }
    }
    
    // Test data completeness
    public void testDataCompleteness() throws SQLException {
        System.out.println("Testing data completeness...");
        
        // Test for null values
        String sql = "SELECT COUNT(*) FROM users WHERE username IS NULL OR email IS NULL";
        try (Statement stmt = connection.createStatement();
             ResultSet rs = stmt.executeQuery(sql)) {
            
            if (rs.next()) {
                int nullRecords = rs.getInt(1);
                if (nullRecords > 0) {
                    System.out.println("Data completeness violation: " + nullRecords + " records with null values");
                } else {
                    System.out.println("Data completeness test passed: No null values");
                }
            }
        }
    }
    
    // Test data validity
    public void testDataValidity() throws SQLException {
        System.out.println("Testing data validity...");
        
        // Test username length
        String sql = "SELECT COUNT(*) FROM users WHERE LENGTH(username) < 3 OR LENGTH(username) > 50";
        try (Statement stmt = connection.createStatement();
             ResultSet rs = stmt.executeQuery(sql)) {
            
            if (rs.next()) {
                int invalidUsernames = rs.getInt(1);
                if (invalidUsernames > 0) {
                    System.out.println("Data validity violation: " + invalidUsernames + " invalid usernames");
                } else {
                    System.out.println("Data validity test passed: All usernames valid");
                }
            }
        }
    }
    
    // Test data consistency
    public void testDataConsistency() throws SQLException {
        System.out.println("Testing data consistency...");
        
        // Test duplicate usernames
        String sql = "SELECT username, COUNT(*) as count FROM users GROUP BY username HAVING COUNT(*) > 1";
        try (Statement stmt = connection.createStatement();
             ResultSet rs = stmt.executeQuery(sql)) {
            
            if (rs.next()) {
                System.out.println("Data consistency violation: Duplicate usernames found");
            } else {
                System.out.println("Data consistency test passed: No duplicate usernames");
            }
        }
    }
}
```

## 22.8 Test Data Management

Test data management involves creating, maintaining, and managing test data for database testing.

### Management Areas:
- **Data Creation**: Create test data
- **Data Maintenance**: Maintain test data
- **Data Cleanup**: Clean up test data
- **Data Versioning**: Version test data
- **Data Privacy**: Protect sensitive data
- **Data Refresh**: Refresh test data

### Real-World Analogy:
Test data management is like managing a test kitchen:
- **Data Creation** = Prepare test ingredients
- **Data Maintenance** = Keep ingredients fresh
- **Data Cleanup** = Clean up after testing
- **Data Versioning** = Track ingredient versions
- **Data Privacy** = Protect secret recipes
- **Data Refresh** = Get fresh ingredients

### Java Example - Test Data Management:
```java
import java.sql.*;
import java.util.*;

public class DatabaseTestDataManagement {
    private Connection connection;
    
    public DatabaseTestDataManagement(Connection connection) {
        this.connection = connection;
    }
    
    // Create test data
    public void createTestData() throws SQLException {
        System.out.println("Creating test data...");
        
        // Create test users
        String sql = "INSERT INTO users (username, email) VALUES (?, ?)";
        try (PreparedStatement stmt = connection.prepareStatement(sql)) {
            for (int i = 1; i <= 100; i++) {
                stmt.setString(1, "testuser" + i);
                stmt.setString(2, "testuser" + i + "@example.com");
                stmt.addBatch();
            }
            stmt.executeBatch();
        }
        
        // Create test posts
        sql = "INSERT INTO posts (user_id, title, content) VALUES (?, ?, ?)";
        try (PreparedStatement stmt = connection.prepareStatement(sql)) {
            for (int i = 1; i <= 100; i++) {
                stmt.setInt(1, i);
                stmt.setString(2, "Test Post " + i);
                stmt.setString(3, "This is test post " + i);
                stmt.addBatch();
            }
            stmt.executeBatch();
        }
        
        System.out.println("Test data created successfully");
    }
    
    // Clean up test data
    public void cleanupTestData() throws SQLException {
        System.out.println("Cleaning up test data...");
        
        // Delete test posts
        String sql = "DELETE FROM posts WHERE title LIKE 'Test Post%'";
        try (Statement stmt = connection.createStatement()) {
            int deletedPosts = stmt.executeUpdate(sql);
            System.out.println("Deleted " + deletedPosts + " test posts");
        }
        
        // Delete test users
        sql = "DELETE FROM users WHERE username LIKE 'testuser%'";
        try (Statement stmt = connection.createStatement()) {
            int deletedUsers = stmt.executeUpdate(sql);
            System.out.println("Deleted " + deletedUsers + " test users");
        }
        
        System.out.println("Test data cleanup completed");
    }
    
    // Refresh test data
    public void refreshTestData() throws SQLException {
        System.out.println("Refreshing test data...");
        
        // Clean up existing test data
        cleanupTestData();
        
        // Create new test data
        createTestData();
        
        System.out.println("Test data refreshed successfully");
    }
    
    // Anonymize sensitive data
    public void anonymizeSensitiveData() throws SQLException {
        System.out.println("Anonymizing sensitive data...");
        
        // Anonymize email addresses
        String sql = "UPDATE users SET email = CONCAT('user', id, '@example.com') WHERE email LIKE '%@%'";
        try (Statement stmt = connection.createStatement()) {
            int updatedRecords = stmt.executeUpdate(sql);
            System.out.println("Anonymized " + updatedRecords + " email addresses");
        }
        
        // Anonymize usernames
        sql = "UPDATE users SET username = CONCAT('user', id) WHERE username IS NOT NULL";
        try (Statement stmt = connection.createStatement()) {
            int updatedRecords = stmt.executeUpdate(sql);
            System.out.println("Anonymized " + updatedRecords + " usernames");
        }
        
        System.out.println("Data anonymization completed");
    }
}
```