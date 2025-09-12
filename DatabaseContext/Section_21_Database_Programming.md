# Section 21 – Database Programming

## 21.1 Stored Procedures and Functions

Stored procedures and functions are precompiled database objects that contain SQL statements and can be called from applications.

### Key Features:
- **Precompiled**: Compiled once and stored in database
- **Reusable**: Can be called multiple times
- **Performance**: Faster execution than dynamic SQL
- **Security**: Controlled access to database operations
- **Modularity**: Encapsulate business logic
- **Parameters**: Accept input and output parameters

### Real-World Analogy:
Stored procedures are like pre-written recipes:
- **Precompiled** = Recipe already written
- **Reusable** = Use recipe multiple times
- **Performance** = Faster than writing from scratch
- **Security** = Controlled access to kitchen
- **Modularity** = Complete dish in one recipe
- **Parameters** = Adjust ingredients as needed

### Java Example - Stored Procedures:
```java
import java.sql.*;
import java.util.*;

public class StoredProcedureExample {
    private Connection connection;
    
    public StoredProcedureExample(Connection connection) {
        this.connection = connection;
    }
    
    // Create stored procedure
    public void createStoredProcedure() throws SQLException {
        String sql = """
            CREATE PROCEDURE GetUserById(IN user_id INT)
            BEGIN
                SELECT id, username, email, created_at
                FROM users
                WHERE id = user_id;
            END
            """;
        
        try (Statement stmt = connection.createStatement()) {
            stmt.execute(sql);
        }
        
        System.out.println("Stored procedure created successfully");
    }
    
    // Call stored procedure
    public void callStoredProcedure(int userId) throws SQLException {
        String sql = "CALL GetUserById(?)";
        
        try (CallableStatement stmt = connection.prepareCall(sql)) {
            stmt.setInt(1, userId);
            
            try (ResultSet rs = stmt.executeQuery()) {
                while (rs.next()) {
                    System.out.println("User: " + rs.getString("username") + 
                                     ", Email: " + rs.getString("email"));
                }
            }
        }
    }
    
    // Create function
    public void createFunction() throws SQLException {
        String sql = """
            CREATE FUNCTION GetUserCount() RETURNS INT
            READS SQL DATA
            DETERMINISTIC
            BEGIN
                DECLARE user_count INT;
                SELECT COUNT(*) INTO user_count FROM users;
                RETURN user_count;
            END
            """;
        
        try (Statement stmt = connection.createStatement()) {
            stmt.execute(sql);
        }
        
        System.out.println("Function created successfully");
    }
    
    // Call function
    public int callFunction() throws SQLException {
        String sql = "SELECT GetUserCount()";
        
        try (Statement stmt = connection.createStatement();
             ResultSet rs = stmt.executeQuery(sql)) {
            
            if (rs.next()) {
                return rs.getInt(1);
            }
        }
        
        return 0;
    }
}
```

## 21.2 Triggers

Triggers are database objects that automatically execute in response to specific database events.

### Trigger Types:
- **BEFORE INSERT**: Execute before insert operation
- **AFTER INSERT**: Execute after insert operation
- **BEFORE UPDATE**: Execute before update operation
- **AFTER UPDATE**: Execute after update operation
- **BEFORE DELETE**: Execute before delete operation
- **AFTER DELETE**: Execute after delete operation

### Real-World Analogy:
Triggers are like automatic security systems:
- **BEFORE INSERT** = Check before allowing entry
- **AFTER INSERT** = Log entry after it happens
- **BEFORE UPDATE** = Validate before allowing changes
- **AFTER UPDATE** = Log changes after they happen
- **BEFORE DELETE** = Check before allowing removal
- **AFTER DELETE** = Log removal after it happens

### Java Example - Triggers:
```java
import java.sql.*;
import java.util.*;

public class TriggerExample {
    private Connection connection;
    
    public TriggerExample(Connection connection) {
        this.connection = connection;
    }
    
    // Create trigger
    public void createTrigger() throws SQLException {
        String sql = """
            CREATE TRIGGER user_audit_trigger
            AFTER INSERT ON users
            FOR EACH ROW
            BEGIN
                INSERT INTO user_audit (user_id, action, timestamp)
                VALUES (NEW.id, 'INSERT', NOW());
            END
            """;
        
        try (Statement stmt = connection.createStatement()) {
            stmt.execute(sql);
        }
        
        System.out.println("Trigger created successfully");
    }
    
    // Test trigger
    public void testTrigger() throws SQLException {
        String sql = "INSERT INTO users (username, email) VALUES (?, ?)";
        
        try (PreparedStatement stmt = connection.prepareStatement(sql)) {
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
                System.out.println("Trigger fired " + count + " times");
            }
        }
    }
}
```

## 21.3 Views and Materialized Views

Views are virtual tables based on the result of a SQL query, while materialized views store the result physically.

### View Types:
- **Simple Views**: Based on single table
- **Complex Views**: Based on multiple tables
- **Materialized Views**: Physically stored results
- **Indexed Views**: Views with indexes
- **Partitioned Views**: Views across partitions
- **System Views**: Built-in database views

### Real-World Analogy:
Views are like different perspectives of the same data:
- **Simple Views** = Single camera angle
- **Complex Views** = Multiple camera angles combined
- **Materialized Views** = Pre-recorded video
- **Indexed Views** = Optimized video
- **Partitioned Views** = Video split into segments
- **System Views** = Built-in camera views

### Java Example - Views:
```java
import java.sql.*;
import java.util.*;

public class ViewExample {
    private Connection connection;
    
    public ViewExample(Connection connection) {
        this.connection = connection;
    }
    
    // Create view
    public void createView() throws SQLException {
        String sql = """
            CREATE VIEW user_posts_view AS
            SELECT u.username, p.title, p.created_at
            FROM users u
            JOIN posts p ON u.id = p.user_id
            WHERE p.created_at > DATE_SUB(NOW(), INTERVAL 30 DAY)
            """;
        
        try (Statement stmt = connection.createStatement()) {
            stmt.execute(sql);
        }
        
        System.out.println("View created successfully");
    }
    
    // Query view
    public void queryView() throws SQLException {
        String sql = "SELECT * FROM user_posts_view ORDER BY created_at DESC";
        
        try (Statement stmt = connection.createStatement();
             ResultSet rs = stmt.executeQuery(sql)) {
            
            System.out.println("Recent user posts:");
            while (rs.next()) {
                System.out.println("User: " + rs.getString("username") + 
                                 ", Post: " + rs.getString("title") + 
                                 ", Date: " + rs.getTimestamp("created_at"));
            }
        }
    }
    
    // Create materialized view
    public void createMaterializedView() throws SQLException {
        String sql = """
            CREATE TABLE user_stats_mv AS
            SELECT 
                u.id,
                u.username,
                COUNT(p.id) as post_count,
                MAX(p.created_at) as last_post_date
            FROM users u
            LEFT JOIN posts p ON u.id = p.user_id
            GROUP BY u.id, u.username
            """;
        
        try (Statement stmt = connection.createStatement()) {
            stmt.execute(sql);
        }
        
        System.out.println("Materialized view created successfully");
    }
    
    // Refresh materialized view
    public void refreshMaterializedView() throws SQLException {
        String sql = """
            INSERT INTO user_stats_mv
            SELECT 
                u.id,
                u.username,
                COUNT(p.id) as post_count,
                MAX(p.created_at) as last_post_date
            FROM users u
            LEFT JOIN posts p ON u.id = p.user_id
            GROUP BY u.id, u.username
            ON DUPLICATE KEY UPDATE
                post_count = VALUES(post_count),
                last_post_date = VALUES(last_post_date)
            """;
        
        try (Statement stmt = connection.createStatement()) {
            stmt.execute(sql);
        }
        
        System.out.println("Materialized view refreshed");
    }
}
```

## 21.4 Cursors

Cursors are database objects that allow row-by-row processing of result sets.

### Cursor Types:
- **Static Cursors**: Fixed result set
- **Dynamic Cursors**: Dynamic result set
- **Forward-Only Cursors**: Move forward only
- **Scrollable Cursors**: Move in any direction
- **Keyset Cursors**: Based on key values
- **Read-Only Cursors**: Cannot modify data

### Real-World Analogy:
Cursors are like reading a book:
- **Static Cursors** = Fixed book content
- **Dynamic Cursors** = Book content changes
- **Forward-Only Cursors** = Read page by page
- **Scrollable Cursors** = Jump to any page
- **Keyset Cursors** = Bookmark-based reading
- **Read-Only Cursors** = Cannot write in book

### Java Example - Cursors:
```java
import java.sql.*;
import java.util.*;

public class CursorExample {
    private Connection connection;
    
    public CursorExample(Connection connection) {
        this.connection = connection;
    }
    
    // Process result set with cursor-like behavior
    public void processResultSetWithCursor() throws SQLException {
        String sql = "SELECT id, username, email FROM users ORDER BY id";
        
        try (Statement stmt = connection.createStatement();
             ResultSet rs = stmt.executeQuery(sql)) {
            
            System.out.println("Processing users with cursor-like behavior:");
            
            while (rs.next()) {
                int id = rs.getInt("id");
                String username = rs.getString("username");
                String email = rs.getString("email");
                
                System.out.println("ID: " + id + ", Username: " + username + ", Email: " + email);
                
                // Process each row
                processUser(id, username, email);
            }
        }
    }
    
    // Process individual user
    private void processUser(int id, String username, String email) {
        System.out.println("Processing user: " + username);
        
        // Simulate processing
        try {
            Thread.sleep(100); // Simulate processing time
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }
    
    // Scrollable result set
    public void scrollableResultSet() throws SQLException {
        String sql = "SELECT id, username, email FROM users ORDER BY id";
        
        try (Statement stmt = connection.createStatement(
                ResultSet.TYPE_SCROLL_INSENSITIVE, 
                ResultSet.CONCUR_READ_ONLY);
             ResultSet rs = stmt.executeQuery(sql)) {
            
            // Move to last row
            rs.last();
            int totalRows = rs.getRow();
            System.out.println("Total rows: " + totalRows);
            
            // Move to first row
            rs.first();
            System.out.println("First user: " + rs.getString("username"));
            
            // Move to middle
            rs.absolute(totalRows / 2);
            System.out.println("Middle user: " + rs.getString("username"));
            
            // Move to last row
            rs.last();
            System.out.println("Last user: " + rs.getString("username"));
        }
    }
}
```

## 21.5 Database Programming Languages

Database programming languages are specialized languages for database operations and stored procedures.

### Common Languages:
- **SQL**: Standard query language
- **PL/SQL**: Oracle's procedural language
- **T-SQL**: Microsoft's SQL Server language
- **PL/pgSQL**: PostgreSQL's procedural language
- **MySQL**: MySQL's stored procedure language
- **JavaScript**: Some databases support JavaScript

### Real-World Analogy:
Database programming languages are like different tools:
- **SQL** = Basic tool
- **PL/SQL** = Professional tool
- **T-SQL** = Microsoft tool
- **PL/pgSQL** = Open source tool
- **MySQL** = MySQL-specific tool
- **JavaScript** = Modern tool

### Java Example - Database Programming Languages:
```java
import java.sql.*;
import java.util.*;

public class DatabaseProgrammingLanguages {
    private Connection connection;
    
    public DatabaseProgrammingLanguages(Connection connection) {
        this.connection = connection;
    }
    
    // Execute SQL stored procedure
    public void executeSQLStoredProcedure() throws SQLException {
        String sql = "CALL GetUserCount()";
        
        try (CallableStatement stmt = connection.prepareCall(sql)) {
            try (ResultSet rs = stmt.executeQuery()) {
                if (rs.next()) {
                    int count = rs.getInt(1);
                    System.out.println("User count: " + count);
                }
            }
        }
    }
    
    // Execute PL/SQL-like procedure
    public void executePLSQLProcedure() throws SQLException {
        String sql = """
            BEGIN
                DECLARE user_count INT;
                SELECT COUNT(*) INTO user_count FROM users;
                SELECT user_count;
            END
            """;
        
        try (Statement stmt = connection.createStatement()) {
            stmt.execute(sql);
        }
    }
    
    // Execute T-SQL-like procedure
    public void executeTSQLProcedure() throws SQLException {
        String sql = """
            DECLARE @user_count INT;
            SELECT @user_count = COUNT(*) FROM users;
            SELECT @user_count;
            """;
        
        try (Statement stmt = connection.createStatement()) {
            stmt.execute(sql);
        }
    }
    
    // Execute JavaScript-like procedure
    public void executeJavaScriptProcedure() throws SQLException {
        String sql = """
            CREATE FUNCTION js_function() RETURNS INT
            LANGUAGE JAVASCRIPT
            AS $$
                var result = db.users.count();
                return result;
            $$
            """;
        
        try (Statement stmt = connection.createStatement()) {
            stmt.execute(sql);
        }
    }
}
```

## 21.6 ORM (Object-Relational Mapping)

ORM is a programming technique that converts data between incompatible type systems in object-oriented programming languages.

### ORM Benefits:
- **Abstraction**: Hide database complexity
- **Productivity**: Faster development
- **Maintainability**: Easier to maintain
- **Portability**: Database independence
- **Type Safety**: Compile-time type checking
- **Caching**: Built-in caching mechanisms

### Real-World Analogy:
ORM is like a translator:
- **Abstraction** = Hide language complexity
- **Productivity** = Faster communication
- **Maintainability** = Easier to update
- **Portability** = Works with different languages
- **Type Safety** = Correct translation
- **Caching** = Remember common translations

### Java Example - ORM:
```java
import java.sql.*;
import java.util.*;

// Entity class
public class User {
    private int id;
    private String username;
    private String email;
    private Date createdAt;
    
    // Constructors
    public User() {}
    
    public User(int id, String username, String email, Date createdAt) {
        this.id = id;
        this.username = username;
        this.email = email;
        this.createdAt = createdAt;
    }
    
    // Getters and setters
    public int getId() { return id; }
    public void setId(int id) { this.id = id; }
    
    public String getUsername() { return username; }
    public void setUsername(String username) { this.username = username; }
    
    public String getEmail() { return email; }
    public void setEmail(String email) { this.email = email; }
    
    public Date getCreatedAt() { return createdAt; }
    public void setCreatedAt(Date createdAt) { this.createdAt = createdAt; }
}

// ORM implementation
public class UserORM {
    private Connection connection;
    
    public UserORM(Connection connection) {
        this.connection = connection;
    }
    
    // Save user
    public void save(User user) throws SQLException {
        String sql = "INSERT INTO users (username, email) VALUES (?, ?)";
        
        try (PreparedStatement stmt = connection.prepareStatement(sql, Statement.RETURN_GENERATED_KEYS)) {
            stmt.setString(1, user.getUsername());
            stmt.setString(2, user.getEmail());
            stmt.executeUpdate();
            
            try (ResultSet rs = stmt.getGeneratedKeys()) {
                if (rs.next()) {
                    user.setId(rs.getInt(1));
                }
            }
        }
    }
    
    // Find user by ID
    public User findById(int id) throws SQLException {
        String sql = "SELECT * FROM users WHERE id = ?";
        
        try (PreparedStatement stmt = connection.prepareStatement(sql)) {
            stmt.setInt(1, id);
            
            try (ResultSet rs = stmt.executeQuery()) {
                if (rs.next()) {
                    return mapResultSetToUser(rs);
                }
            }
        }
        
        return null;
    }
    
    // Find all users
    public List<User> findAll() throws SQLException {
        List<User> users = new ArrayList<>();
        String sql = "SELECT * FROM users ORDER BY id";
        
        try (Statement stmt = connection.createStatement();
             ResultSet rs = stmt.executeQuery(sql)) {
            
            while (rs.next()) {
                users.add(mapResultSetToUser(rs));
            }
        }
        
        return users;
    }
    
    // Update user
    public void update(User user) throws SQLException {
        String sql = "UPDATE users SET username = ?, email = ? WHERE id = ?";
        
        try (PreparedStatement stmt = connection.prepareStatement(sql)) {
            stmt.setString(1, user.getUsername());
            stmt.setString(2, user.getEmail());
            stmt.setInt(3, user.getId());
            stmt.executeUpdate();
        }
    }
    
    // Delete user
    public void delete(int id) throws SQLException {
        String sql = "DELETE FROM users WHERE id = ?";
        
        try (PreparedStatement stmt = connection.prepareStatement(sql)) {
            stmt.setInt(1, id);
            stmt.executeUpdate();
        }
    }
    
    // Map result set to user object
    private User mapResultSetToUser(ResultSet rs) throws SQLException {
        User user = new User();
        user.setId(rs.getInt("id"));
        user.setUsername(rs.getString("username"));
        user.setEmail(rs.getString("email"));
        user.setCreatedAt(rs.getDate("created_at"));
        return user;
    }
}
```

## 21.7 Database APIs and Drivers

Database APIs and drivers provide interfaces for applications to interact with databases.

### API Types:
- **JDBC**: Java Database Connectivity
- **ODBC**: Open Database Connectivity
- **ADO.NET**: Microsoft's data access technology
- **PDO**: PHP Data Objects
- **SQLAlchemy**: Python SQL toolkit
- **REST APIs**: HTTP-based database APIs

### Real-World Analogy:
Database APIs are like different ways to communicate:
- **JDBC** = Java language
- **ODBC** = Universal language
- **ADO.NET** = Microsoft language
- **PDO** = PHP language
- **SQLAlchemy** = Python language
- **REST APIs** = Web language

### Java Example - Database APIs:
```java
import java.sql.*;
import java.util.*;

public class DatabaseAPIs {
    private Connection connection;
    
    public DatabaseAPIs(Connection connection) {
        this.connection = connection;
    }
    
    // JDBC example
    public void jdbcExample() throws SQLException {
        String sql = "SELECT * FROM users WHERE id = ?";
        
        try (PreparedStatement stmt = connection.prepareStatement(sql)) {
            stmt.setInt(1, 1);
            
            try (ResultSet rs = stmt.executeQuery()) {
                while (rs.next()) {
                    System.out.println("User: " + rs.getString("username"));
                }
            }
        }
    }
    
    // Connection pooling example
    public void connectionPoolingExample() {
        // In real implementation, use connection pool
        System.out.println("Using connection pool for better performance");
    }
    
    // Batch processing example
    public void batchProcessingExample() throws SQLException {
        String sql = "INSERT INTO users (username, email) VALUES (?, ?)";
        
        try (PreparedStatement stmt = connection.prepareStatement(sql)) {
            // Add multiple statements to batch
            stmt.setString(1, "user1");
            stmt.setString(2, "user1@example.com");
            stmt.addBatch();
            
            stmt.setString(1, "user2");
            stmt.setString(2, "user2@example.com");
            stmt.addBatch();
            
            // Execute batch
            int[] results = stmt.executeBatch();
            System.out.println("Batch executed: " + results.length + " statements");
        }
    }
    
    // Transaction example
    public void transactionExample() throws SQLException {
        connection.setAutoCommit(false);
        
        try {
            // First operation
            String sql1 = "INSERT INTO users (username, email) VALUES (?, ?)";
            try (PreparedStatement stmt = connection.prepareStatement(sql1)) {
                stmt.setString(1, "user3");
                stmt.setString(2, "user3@example.com");
                stmt.executeUpdate();
            }
            
            // Second operation
            String sql2 = "INSERT INTO posts (user_id, title) VALUES (?, ?)";
            try (PreparedStatement stmt = connection.prepareStatement(sql2)) {
                stmt.setInt(1, 1);
                stmt.setString(2, "First Post");
                stmt.executeUpdate();
            }
            
            // Commit transaction
            connection.commit();
            System.out.println("Transaction committed successfully");
            
        } catch (SQLException e) {
            // Rollback transaction
            connection.rollback();
            System.err.println("Transaction rolled back: " + e.getMessage());
            throw e;
        } finally {
            connection.setAutoCommit(true);
        }
    }
}
```

## 21.8 Database Application Development

Database application development involves creating applications that interact with databases.

### Development Areas:
- **Data Access Layer**: Interface between application and database
- **Business Logic**: Application-specific logic
- **User Interface**: User interaction layer
- **Error Handling**: Proper error management
- **Logging**: Application logging
- **Testing**: Application testing

### Real-World Analogy:
Database application development is like building a house:
- **Data Access Layer** = Foundation
- **Business Logic** = Structure
- **User Interface** = Exterior
- **Error Handling** = Safety systems
- **Logging** = Security system
- **Testing** = Quality inspection

### Java Example - Database Application:
```java
import java.sql.*;
import java.util.*;

public class DatabaseApplication {
    private Connection connection;
    private UserORM userORM;
    
    public DatabaseApplication(Connection connection) {
        this.connection = connection;
        this.userORM = new UserORM(connection);
    }
    
    // Create user
    public void createUser(String username, String email) {
        try {
            User user = new User(0, username, email, new Date());
            userORM.save(user);
            System.out.println("User created successfully: " + username);
        } catch (SQLException e) {
            System.err.println("Error creating user: " + e.getMessage());
        }
    }
    
    // Get user
    public User getUser(int id) {
        try {
            return userORM.findById(id);
        } catch (SQLException e) {
            System.err.println("Error getting user: " + e.getMessage());
            return null;
        }
    }
    
    // Update user
    public void updateUser(int id, String username, String email) {
        try {
            User user = userORM.findById(id);
            if (user != null) {
                user.setUsername(username);
                user.setEmail(email);
                userORM.update(user);
                System.out.println("User updated successfully: " + username);
            } else {
                System.out.println("User not found with ID: " + id);
            }
        } catch (SQLException e) {
            System.err.println("Error updating user: " + e.getMessage());
        }
    }
    
    // Delete user
    public void deleteUser(int id) {
        try {
            userORM.delete(id);
            System.out.println("User deleted successfully with ID: " + id);
        } catch (SQLException e) {
            System.err.println("Error deleting user: " + e.getMessage());
        }
    }
    
    // List all users
    public void listUsers() {
        try {
            List<User> users = userORM.findAll();
            System.out.println("All users:");
            for (User user : users) {
                System.out.println("ID: " + user.getId() + 
                                 ", Username: " + user.getUsername() + 
                                 ", Email: " + user.getEmail());
            }
        } catch (SQLException e) {
            System.err.println("Error listing users: " + e.getMessage());
        }
    }
    
    // Main application method
    public static void main(String[] args) {
        try (Connection conn = DriverManager.getConnection(
                "jdbc:mysql://localhost:3306/database", "username", "password")) {
            
            DatabaseApplication app = new DatabaseApplication(conn);
            
            // Create users
            app.createUser("john_doe", "john@example.com");
            app.createUser("jane_smith", "jane@example.com");
            
            // List users
            app.listUsers();
            
            // Update user
            app.updateUser(1, "john_updated", "john_updated@example.com");
            
            // Get user
            User user = app.getUser(1);
            if (user != null) {
                System.out.println("Retrieved user: " + user.getUsername());
            }
            
            // Delete user
            app.deleteUser(2);
            
            // List users again
            app.listUsers();
            
        } catch (SQLException e) {
            System.err.println("Database error: " + e.getMessage());
        }
    }
}
```