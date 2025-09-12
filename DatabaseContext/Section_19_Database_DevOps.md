# Section 19 – Database DevOps

## 19.1 Database Version Control

Database version control involves tracking and managing changes to database schemas, data, and configurations over time.

### Key Features:
- **Schema Versioning**: Track schema changes
- **Data Versioning**: Track data changes
- **Configuration Versioning**: Track configuration changes
- **Change Tracking**: Monitor all database changes
- **Rollback Capability**: Revert to previous versions
- **Collaboration**: Multiple developers working together

### Real-World Analogy:
Database version control is like a library system:
- **Schema Versioning** = Book catalog updates
- **Data Versioning** = Book content updates
- **Configuration Versioning** = Library rules updates
- **Change Tracking** = Check-in/check-out system
- **Rollback Capability** = Restore previous versions
- **Collaboration** = Multiple librarians

### Java Example - Database Version Control:
```java
import java.sql.*;
import java.util.*;

public class DatabaseVersionControl {
    private Connection connection;
    private Map<String, String> schemaVersions = new HashMap<>();
    
    public DatabaseVersionControl(Connection connection) {
        this.connection = connection;
    }
    
    // Create version table
    public void createVersionTable() throws SQLException {
        String sql = """
            CREATE TABLE IF NOT EXISTS schema_versions (
                id INT AUTO_INCREMENT PRIMARY KEY,
                version VARCHAR(50) NOT NULL,
                description TEXT,
                applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                applied_by VARCHAR(100)
            )
            """;
        
        try (Statement stmt = connection.createStatement()) {
            stmt.execute(sql);
        }
    }
    
    // Apply schema change
    public void applySchemaChange(String version, String description, String sql) throws SQLException {
        connection.setAutoCommit(false);
        
        try {
            // Execute schema change
            try (Statement stmt = connection.createStatement()) {
                stmt.execute(sql);
            }
            
            // Record version
            String insertSQL = "INSERT INTO schema_versions (version, description, applied_by) VALUES (?, ?, ?)";
            try (PreparedStatement stmt = connection.prepareStatement(insertSQL)) {
                stmt.setString(1, version);
                stmt.setString(2, description);
                stmt.setString(3, System.getProperty("user.name"));
                stmt.executeUpdate();
            }
            
            connection.commit();
            System.out.println("Schema change applied: " + version);
            
        } catch (SQLException e) {
            connection.rollback();
            throw e;
        } finally {
            connection.setAutoCommit(true);
        }
    }
    
    // Get current version
    public String getCurrentVersion() throws SQLException {
        String sql = "SELECT version FROM schema_versions ORDER BY applied_at DESC LIMIT 1";
        
        try (Statement stmt = connection.createStatement();
             ResultSet rs = stmt.executeQuery(sql)) {
            
            if (rs.next()) {
                return rs.getString("version");
            }
        }
        
        return "0.0.0";
    }
    
    // List all versions
    public void listVersions() throws SQLException {
        String sql = "SELECT version, description, applied_at, applied_by FROM schema_versions ORDER BY applied_at";
        
        try (Statement stmt = connection.createStatement();
             ResultSet rs = stmt.executeQuery(sql)) {
            
            System.out.println("Database Versions:");
            while (rs.next()) {
                System.out.println("Version: " + rs.getString("version") + 
                                 " - " + rs.getString("description") + 
                                 " (Applied: " + rs.getTimestamp("applied_at") + 
                                 " by " + rs.getString("applied_by") + ")");
            }
        }
    }
}
```

## 19.2 Database Schema Migration

Database schema migration involves applying incremental changes to database schemas in a controlled and reversible manner.

### Migration Types:
- **Forward Migrations**: Apply schema changes
- **Rollback Migrations**: Revert schema changes
- **Data Migrations**: Transform data during schema changes
- **Seed Migrations**: Insert initial data
- **Reference Data**: Insert reference data

### Real-World Analogy:
Database schema migration is like renovating a building:
- **Forward Migrations** = Adding new rooms
- **Rollback Migrations** = Removing additions
- **Data Migrations** = Moving furniture
- **Seed Migrations** = Adding initial furniture
- **Reference Data** = Adding standard fixtures

### Java Example - Schema Migration:
```java
import java.sql.*;
import java.util.*;

public class DatabaseSchemaMigration {
    private Connection connection;
    private List<Migration> migrations = new ArrayList<>();
    
    public DatabaseSchemaMigration(Connection connection) {
        this.connection = connection;
        loadMigrations();
    }
    
    // Migration class
    public static class Migration {
        private String version;
        private String description;
        private String forwardSQL;
        private String rollbackSQL;
        
        public Migration(String version, String description, String forwardSQL, String rollbackSQL) {
            this.version = version;
            this.description = description;
            this.forwardSQL = forwardSQL;
            this.rollbackSQL = rollbackSQL;
        }
        
        // Getters
        public String getVersion() { return version; }
        public String getDescription() { return description; }
        public String getForwardSQL() { return forwardSQL; }
        public String getRollbackSQL() { return rollbackSQL; }
    }
    
    private void loadMigrations() {
        // Add sample migrations
        migrations.add(new Migration("1.0.0", "Create users table", 
            "CREATE TABLE users (id INT PRIMARY KEY, name VARCHAR(100))", 
            "DROP TABLE users"));
        
        migrations.add(new Migration("1.0.1", "Add email column to users", 
            "ALTER TABLE users ADD COLUMN email VARCHAR(255)", 
            "ALTER TABLE users DROP COLUMN email"));
        
        migrations.add(new Migration("1.0.2", "Create posts table", 
            "CREATE TABLE posts (id INT PRIMARY KEY, user_id INT, title VARCHAR(255))", 
            "DROP TABLE posts"));
    }
    
    // Run migrations
    public void runMigrations() throws SQLException {
        String currentVersion = getCurrentVersion();
        System.out.println("Current version: " + currentVersion);
        
        for (Migration migration : migrations) {
            if (isVersionNewer(migration.getVersion(), currentVersion)) {
                runMigration(migration);
            }
        }
    }
    
    // Run single migration
    private void runMigration(Migration migration) throws SQLException {
        System.out.println("Running migration: " + migration.getVersion() + " - " + migration.getDescription());
        
        connection.setAutoCommit(false);
        
        try {
            // Execute forward migration
            try (Statement stmt = connection.createStatement()) {
                stmt.execute(migration.getForwardSQL());
            }
            
            // Record migration
            recordMigration(migration);
            
            connection.commit();
            System.out.println("Migration completed: " + migration.getVersion());
            
        } catch (SQLException e) {
            connection.rollback();
            System.err.println("Migration failed: " + migration.getVersion() + " - " + e.getMessage());
            throw e;
        } finally {
            connection.setAutoCommit(true);
        }
    }
    
    // Rollback migration
    public void rollbackMigration(String version) throws SQLException {
        Migration migration = findMigration(version);
        if (migration == null) {
            throw new SQLException("Migration not found: " + version);
        }
        
        System.out.println("Rolling back migration: " + version);
        
        connection.setAutoCommit(false);
        
        try {
            // Execute rollback migration
            try (Statement stmt = connection.createStatement()) {
                stmt.execute(migration.getRollbackSQL());
            }
            
            // Remove migration record
            removeMigrationRecord(version);
            
            connection.commit();
            System.out.println("Rollback completed: " + version);
            
        } catch (SQLException e) {
            connection.rollback();
            System.err.println("Rollback failed: " + version + " - " + e.getMessage());
            throw e;
        } finally {
            connection.setAutoCommit(true);
        }
    }
    
    private String getCurrentVersion() throws SQLException {
        String sql = "SELECT version FROM schema_versions ORDER BY applied_at DESC LIMIT 1";
        
        try (Statement stmt = connection.createStatement();
             ResultSet rs = stmt.executeQuery(sql)) {
            
            if (rs.next()) {
                return rs.getString("version");
            }
        }
        
        return "0.0.0";
    }
    
    private boolean isVersionNewer(String version1, String version2) {
        // Simple version comparison (in practice, use proper version comparison)
        return version1.compareTo(version2) > 0;
    }
    
    private void recordMigration(Migration migration) throws SQLException {
        String sql = "INSERT INTO schema_versions (version, description, applied_by) VALUES (?, ?, ?)";
        try (PreparedStatement stmt = connection.prepareStatement(sql)) {
            stmt.setString(1, migration.getVersion());
            stmt.setString(2, migration.getDescription());
            stmt.setString(3, System.getProperty("user.name"));
            stmt.executeUpdate();
        }
    }
    
    private Migration findMigration(String version) {
        return migrations.stream()
            .filter(m -> m.getVersion().equals(version))
            .findFirst()
            .orElse(null);
    }
    
    private void removeMigrationRecord(String version) throws SQLException {
        String sql = "DELETE FROM schema_versions WHERE version = ?";
        try (PreparedStatement stmt = connection.prepareStatement(sql)) {
            stmt.setString(1, version);
            stmt.executeUpdate();
        }
    }
}
```

## 19.3 Infrastructure as Code (IaC)

Infrastructure as Code involves managing and provisioning database infrastructure through code rather than manual processes.

### Key Benefits:
- **Version Control**: Track infrastructure changes
- **Reproducibility**: Consistent environments
- **Automation**: Automated provisioning
- **Scalability**: Easy scaling
- **Documentation**: Self-documenting infrastructure
- **Testing**: Test infrastructure changes

### Real-World Analogy:
Infrastructure as Code is like having blueprints for buildings:
- **Version Control** = Blueprint revisions
- **Reproducibility** = Same building every time
- **Automation** = Automated construction
- **Scalability** = Easy to build multiple buildings
- **Documentation** = Blueprints document everything
- **Testing** = Test building plans

### Java Example - Infrastructure as Code:
```java
import java.util.*;
import java.io.*;

public class DatabaseInfrastructureAsCode {
    private Map<String, DatabaseConfig> environments = new HashMap<>();
    
    // Database configuration
    public static class DatabaseConfig {
        private String name;
        private String host;
        private int port;
        private String database;
        private String username;
        private String password;
        private Map<String, String> parameters;
        
        public DatabaseConfig(String name, String host, int port, String database, 
                            String username, String password, Map<String, String> parameters) {
            this.name = name;
            this.host = host;
            this.port = port;
            this.database = database;
            this.username = username;
            this.password = password;
            this.parameters = parameters;
        }
        
        // Getters
        public String getName() { return name; }
        public String getHost() { return host; }
        public int getPort() { return port; }
        public String getDatabase() { return database; }
        public String getUsername() { return username; }
        public String getPassword() { return password; }
        public Map<String, String> getParameters() { return parameters; }
    }
    
    public DatabaseInfrastructureAsCode() {
        loadEnvironments();
    }
    
    private void loadEnvironments() {
        // Development environment
        Map<String, String> devParams = new HashMap<>();
        devParams.put("max_connections", "100");
        devParams.put("memory", "2GB");
        
        environments.put("dev", new DatabaseConfig(
            "dev-db", "localhost", 3306, "dev_database", 
            "dev_user", "dev_password", devParams));
        
        // Staging environment
        Map<String, String> stagingParams = new HashMap<>();
        stagingParams.put("max_connections", "500");
        stagingParams.put("memory", "8GB");
        
        environments.put("staging", new DatabaseConfig(
            "staging-db", "staging.example.com", 3306, "staging_database", 
            "staging_user", "staging_password", stagingParams));
        
        // Production environment
        Map<String, String> prodParams = new HashMap<>();
        prodParams.put("max_connections", "1000");
        prodParams.put("memory", "32GB");
        
        environments.put("prod", new DatabaseConfig(
            "prod-db", "prod.example.com", 3306, "prod_database", 
            "prod_user", "prod_password", prodParams));
    }
    
    // Provision database infrastructure
    public void provisionDatabase(String environment) {
        DatabaseConfig config = environments.get(environment);
        if (config == null) {
            throw new IllegalArgumentException("Environment not found: " + environment);
        }
        
        System.out.println("Provisioning database for environment: " + environment);
        System.out.println("Host: " + config.getHost());
        System.out.println("Port: " + config.getPort());
        System.out.println("Database: " + config.getDatabase());
        System.out.println("Parameters: " + config.getParameters());
        
        // In real implementation, this would call cloud provider APIs
        createDatabaseInstance(config);
        configureDatabase(config);
        setupMonitoring(config);
    }
    
    // Create database instance
    private void createDatabaseInstance(DatabaseConfig config) {
        System.out.println("Creating database instance: " + config.getName());
        // In real implementation, call cloud provider API
    }
    
    // Configure database
    private void configureDatabase(DatabaseConfig config) {
        System.out.println("Configuring database: " + config.getName());
        // In real implementation, apply configuration
    }
    
    // Setup monitoring
    private void setupMonitoring(DatabaseConfig config) {
        System.out.println("Setting up monitoring for: " + config.getName());
        // In real implementation, configure monitoring
    }
    
    // Generate infrastructure configuration
    public void generateInfrastructureConfig(String environment) {
        DatabaseConfig config = environments.get(environment);
        if (config == null) {
            throw new IllegalArgumentException("Environment not found: " + environment);
        }
        
        System.out.println("Generating infrastructure configuration for: " + environment);
        
        // Generate Terraform-like configuration
        String terraformConfig = generateTerraformConfig(config);
        System.out.println(terraformConfig);
    }
    
    private String generateTerraformConfig(DatabaseConfig config) {
        return String.format("""
            resource "aws_db_instance" "%s" {
              identifier = "%s"
              engine = "mysql"
              engine_version = "8.0"
              instance_class = "db.t3.micro"
              allocated_storage = 20
              storage_type = "gp2"
              db_name = "%s"
              username = "%s"
              password = "%s"
              vpc_security_group_ids = ["sg-12345678"]
              db_subnet_group_name = "default"
              
              tags = {
                Name = "%s"
                Environment = "%s"
              }
            }
            """, config.getName(), config.getName(), config.getDatabase(), 
                 config.getUsername(), config.getPassword(), config.getName(), environment);
    }
}
```

## 19.4 Database CI/CD Pipelines

Database CI/CD pipelines automate the process of building, testing, and deploying database changes.

### Pipeline Stages:
- **Build**: Compile and package database changes
- **Test**: Run automated tests
- **Deploy**: Deploy to target environments
- **Verify**: Verify deployment success
- **Rollback**: Rollback if deployment fails

### Real-World Analogy:
Database CI/CD pipelines are like assembly lines:
- **Build** = Assembling products
- **Test** = Quality control
- **Deploy** = Shipping products
- **Verify** = Final inspection
- **Rollback** = Return defective products

### Java Example - Database CI/CD Pipeline:
```java
import java.sql.*;
import java.util.*;

public class DatabaseCICDPipeline {
    private Connection connection;
    private List<PipelineStage> stages = new ArrayList<>();
    
    public DatabaseCICDPipeline(Connection connection) {
        this.connection = connection;
        initializeStages();
    }
    
    // Pipeline stage
    public static class PipelineStage {
        private String name;
        private Runnable action;
        private boolean required;
        
        public PipelineStage(String name, Runnable action, boolean required) {
            this.name = name;
            this.action = action;
            this.required = required;
        }
        
        // Getters
        public String getName() { return name; }
        public Runnable getAction() { return action; }
        public boolean isRequired() { return required; }
    }
    
    private void initializeStages() {
        stages.add(new PipelineStage("Build", this::buildDatabase, true));
        stages.add(new PipelineStage("Test", this::testDatabase, true));
        stages.add(new PipelineStage("Deploy", this::deployDatabase, true));
        stages.add(new PipelineStage("Verify", this::verifyDeployment, true));
        stages.add(new PipelineStage("Rollback", this::rollbackDeployment, false));
    }
    
    // Run pipeline
    public void runPipeline() {
        System.out.println("Starting Database CI/CD Pipeline");
        
        for (PipelineStage stage : stages) {
            try {
                System.out.println("Running stage: " + stage.getName());
                stage.getAction().run();
                System.out.println("Stage completed: " + stage.getName());
                
            } catch (Exception e) {
                System.err.println("Stage failed: " + stage.getName() + " - " + e.getMessage());
                
                if (stage.isRequired()) {
                    System.err.println("Pipeline failed at required stage: " + stage.getName());
                    break;
                } else {
                    System.out.println("Continuing pipeline despite optional stage failure");
                }
            }
        }
        
        System.out.println("Pipeline completed");
    }
    
    // Build database
    private void buildDatabase() {
        System.out.println("Building database schema...");
        // In real implementation, compile schema files
    }
    
    // Test database
    private void testDatabase() throws SQLException {
        System.out.println("Running database tests...");
        
        // Test connection
        if (connection.isClosed()) {
            throw new SQLException("Database connection is closed");
        }
        
        // Test basic functionality
        try (Statement stmt = connection.createStatement();
             ResultSet rs = stmt.executeQuery("SELECT 1")) {
            
            if (!rs.next()) {
                throw new SQLException("Database test query failed");
            }
        }
        
        System.out.println("Database tests passed");
    }
    
    // Deploy database
    private void deployDatabase() throws SQLException {
        System.out.println("Deploying database changes...");
        
        // Apply schema changes
        String sql = "CREATE TABLE IF NOT EXISTS test_table (id INT PRIMARY KEY)";
        try (Statement stmt = connection.createStatement()) {
            stmt.execute(sql);
        }
        
        System.out.println("Database deployment completed");
    }
    
    // Verify deployment
    private void verifyDeployment() throws SQLException {
        System.out.println("Verifying deployment...");
        
        // Check if changes were applied
        String sql = "SELECT COUNT(*) FROM test_table";
        try (Statement stmt = connection.createStatement();
             ResultSet rs = stmt.executeQuery(sql)) {
            
            if (rs.next()) {
                int count = rs.getInt(1);
                System.out.println("Verification successful: " + count + " records found");
            }
        }
    }
    
    // Rollback deployment
    private void rollbackDeployment() throws SQLException {
        System.out.println("Rolling back deployment...");
        
        // Rollback changes
        String sql = "DROP TABLE IF EXISTS test_table";
        try (Statement stmt = connection.createStatement()) {
            stmt.execute(sql);
        }
        
        System.out.println("Rollback completed");
    }
}
```

## 19.5 Database Testing Strategies

Database testing strategies involve testing database functionality, performance, and data integrity.

### Testing Types:
- **Unit Testing**: Test individual database components
- **Integration Testing**: Test database interactions
- **Performance Testing**: Test database performance
- **Data Testing**: Test data integrity
- **Security Testing**: Test database security
- **Load Testing**: Test under load

### Real-World Analogy:
Database testing is like quality control in manufacturing:
- **Unit Testing** = Testing individual parts
- **Integration Testing** = Testing assembled products
- **Performance Testing** = Testing product performance
- **Data Testing** = Testing product specifications
- **Security Testing** = Testing product security
- **Load Testing** = Testing under stress

### Java Example - Database Testing:
```java
import java.sql.*;
import java.util.*;

public class DatabaseTesting {
    private Connection connection;
    
    public DatabaseTesting(Connection connection) {
        this.connection = connection;
    }
    
    // Unit test for database function
    public void testDatabaseFunction() throws SQLException {
        System.out.println("Testing database function...");
        
        // Test function exists
        String sql = "SELECT COUNT(*) FROM information_schema.routines WHERE routine_name = 'test_function'";
        try (Statement stmt = connection.createStatement();
             ResultSet rs = stmt.executeQuery(sql)) {
            
            if (rs.next() && rs.getInt(1) > 0) {
                System.out.println("Function exists: test_function");
            } else {
                System.out.println("Function not found: test_function");
            }
        }
    }
    
    // Integration test
    public void testDatabaseIntegration() throws SQLException {
        System.out.println("Testing database integration...");
        
        // Test table relationships
        String sql = """
            SELECT COUNT(*) 
            FROM users u 
            JOIN posts p ON u.id = p.user_id
            """;
        
        try (Statement stmt = connection.createStatement();
             ResultSet rs = stmt.executeQuery(sql)) {
            
            if (rs.next()) {
                int count = rs.getInt(1);
                System.out.println("Integration test passed: " + count + " related records found");
            }
        }
    }
    
    // Performance test
    public void testDatabasePerformance() throws SQLException {
        System.out.println("Testing database performance...");
        
        long startTime = System.currentTimeMillis();
        
        // Execute test query
        String sql = "SELECT * FROM users WHERE created_at > DATE_SUB(NOW(), INTERVAL 1 DAY)";
        try (Statement stmt = connection.createStatement();
             ResultSet rs = stmt.executeQuery(sql)) {
            
            int count = 0;
            while (rs.next()) {
                count++;
            }
            
            long endTime = System.currentTimeMillis();
            long executionTime = endTime - startTime;
            
            System.out.println("Performance test completed:");
            System.out.println("Records processed: " + count);
            System.out.println("Execution time: " + executionTime + "ms");
            
            if (executionTime > 1000) {
                System.out.println("WARNING: Query execution time exceeds 1 second");
            }
        }
    }
    
    // Data integrity test
    public void testDataIntegrity() throws SQLException {
        System.out.println("Testing data integrity...");
        
        // Test foreign key constraints
        String sql = "SELECT COUNT(*) FROM posts p LEFT JOIN users u ON p.user_id = u.id WHERE u.id IS NULL";
        try (Statement stmt = connection.createStatement();
             ResultSet rs = stmt.executeQuery(sql)) {
            
            if (rs.next()) {
                int orphanedRecords = rs.getInt(1);
                if (orphanedRecords > 0) {
                    System.out.println("Data integrity violation: " + orphanedRecords + " orphaned records found");
                } else {
                    System.out.println("Data integrity test passed: No orphaned records found");
                }
            }
        }
    }
    
    // Security test
    public void testDatabaseSecurity() throws SQLException {
        System.out.println("Testing database security...");
        
        // Test user permissions
        String sql = "SELECT USER(), CURRENT_USER()";
        try (Statement stmt = connection.createStatement();
             ResultSet rs = stmt.executeQuery(sql)) {
            
            if (rs.next()) {
                String currentUser = rs.getString(1);
                System.out.println("Current user: " + currentUser);
                
                // Check if user has appropriate permissions
                if (currentUser.contains("root") || currentUser.contains("admin")) {
                    System.out.println("WARNING: Using privileged user account");
                } else {
                    System.out.println("Security test passed: Using non-privileged user");
                }
            }
        }
    }
    
    // Load test
    public void testDatabaseLoad() throws SQLException {
        System.out.println("Testing database under load...");
        
        int numberOfThreads = 10;
        int queriesPerThread = 100;
        
        List<Thread> threads = new ArrayList<>();
        
        for (int i = 0; i < numberOfThreads; i++) {
            Thread thread = new Thread(() -> {
                try {
                    for (int j = 0; j < queriesPerThread; j++) {
                        String sql = "SELECT COUNT(*) FROM users";
                        try (Statement stmt = connection.createStatement();
                             ResultSet rs = stmt.executeQuery(sql)) {
                            // Process result
                        }
                    }
                } catch (SQLException e) {
                    System.err.println("Load test error: " + e.getMessage());
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
        
        System.out.println("Load test completed: " + numberOfThreads + " threads, " + 
                         (numberOfThreads * queriesPerThread) + " queries");
    }
}
```

## 19.6 Database Deployment Automation

Database deployment automation involves automating the process of deploying database changes to different environments.

### Automation Benefits:
- **Consistency**: Consistent deployments across environments
- **Speed**: Faster deployment process
- **Reliability**: Reduced human errors
- **Traceability**: Track deployment history
- **Rollback**: Easy rollback capability
- **Scheduling**: Scheduled deployments

### Real-World Analogy:
Database deployment automation is like automated manufacturing:
- **Consistency** = Same product every time
- **Speed** = Faster production
- **Reliability** = Fewer defects
- **Traceability** = Track production history
- **Rollback** = Recall defective products
- **Scheduling** = Scheduled production runs

### Java Example - Database Deployment Automation:
```java
import java.sql.*;
import java.util.*;
import java.util.concurrent.*;

public class DatabaseDeploymentAutomation {
    private Connection connection;
    private ScheduledExecutorService scheduler;
    
    public DatabaseDeploymentAutomation(Connection connection) {
        this.connection = connection;
        this.scheduler = Executors.newScheduledThreadPool(4);
    }
    
    // Deploy database changes
    public void deployDatabaseChanges(String environment, List<String> changes) throws SQLException {
        System.out.println("Deploying database changes to: " + environment);
        
        connection.setAutoCommit(false);
        
        try {
            for (String change : changes) {
                System.out.println("Applying change: " + change);
                applyChange(change);
            }
            
            connection.commit();
            System.out.println("Database deployment completed successfully");
            
        } catch (SQLException e) {
            connection.rollback();
            System.err.println("Database deployment failed: " + e.getMessage());
            throw e;
        } finally {
            connection.setAutoCommit(true);
        }
    }
    
    // Apply individual change
    private void applyChange(String change) throws SQLException {
        try (Statement stmt = connection.createStatement()) {
            stmt.execute(change);
        }
    }
    
    // Schedule deployment
    public void scheduleDeployment(String environment, List<String> changes, long delayMinutes) {
        System.out.println("Scheduling deployment to " + environment + " in " + delayMinutes + " minutes");
        
        scheduler.schedule(() -> {
            try {
                deployDatabaseChanges(environment, changes);
            } catch (SQLException e) {
                System.err.println("Scheduled deployment failed: " + e.getMessage());
            }
        }, delayMinutes, TimeUnit.MINUTES);
    }
    
    // Deploy with rollback capability
    public void deployWithRollback(String environment, List<String> changes) throws SQLException {
        System.out.println("Deploying with rollback capability to: " + environment);
        
        // Create backup
        String backupName = "backup_" + System.currentTimeMillis();
        createBackup(backupName);
        
        try {
            deployDatabaseChanges(environment, changes);
            System.out.println("Deployment successful, backup: " + backupName);
            
        } catch (SQLException e) {
            System.err.println("Deployment failed, rolling back...");
            rollbackFromBackup(backupName);
            throw e;
        }
    }
    
    // Create backup
    private void createBackup(String backupName) throws SQLException {
        System.out.println("Creating backup: " + backupName);
        // In real implementation, create actual backup
    }
    
    // Rollback from backup
    private void rollbackFromBackup(String backupName) throws SQLException {
        System.out.println("Rolling back from backup: " + backupName);
        // In real implementation, restore from backup
    }
    
    // Deploy to multiple environments
    public void deployToMultipleEnvironments(Map<String, List<String>> environmentChanges) {
        System.out.println("Deploying to multiple environments...");
        
        for (Map.Entry<String, List<String>> entry : environmentChanges.entrySet()) {
            String environment = entry.getKey();
            List<String> changes = entry.getValue();
            
            try {
                deployDatabaseChanges(environment, changes);
                System.out.println("Deployment to " + environment + " completed");
                
            } catch (SQLException e) {
                System.err.println("Deployment to " + environment + " failed: " + e.getMessage());
            }
        }
    }
    
    // Shutdown scheduler
    public void shutdown() {
        scheduler.shutdown();
        try {
            if (!scheduler.awaitTermination(60, TimeUnit.SECONDS)) {
                scheduler.shutdownNow();
            }
        } catch (InterruptedException e) {
            scheduler.shutdownNow();
            Thread.currentThread().interrupt();
        }
    }
}
```

## 19.7 Database Monitoring and Alerting

Database monitoring and alerting involves continuously monitoring database performance and health, and alerting when issues occur.

### Monitoring Areas:
- **Performance**: Query performance, response times
- **Resources**: CPU, memory, disk usage
- **Connections**: Active connections, connection pool
- **Errors**: Error rates, failed queries
- **Availability**: Uptime, downtime
- **Security**: Failed login attempts, suspicious activity

### Real-World Analogy:
Database monitoring is like a security system:
- **Performance** = System efficiency
- **Resources** = Power and water usage
- **Connections** = People entering/leaving
- **Errors** = System malfunctions
- **Availability** = System uptime
- **Security** = Intrusion detection

### Java Example - Database Monitoring:
```java
import java.sql.*;
import java.util.*;
import java.util.concurrent.*;

public class DatabaseMonitoring {
    private Connection connection;
    private ScheduledExecutorService scheduler;
    private List<Alert> alerts = new ArrayList<>();
    
    public DatabaseMonitoring(Connection connection) {
        this.connection = connection;
        this.scheduler = Executors.newScheduledThreadPool(2);
    }
    
    // Alert class
    public static class Alert {
        private String id;
        private String type;
        private String message;
        private String severity;
        private long timestamp;
        
        public Alert(String id, String type, String message, String severity) {
            this.id = id;
            this.message = message;
            this.severity = severity;
            this.timestamp = System.currentTimeMillis();
        }
        
        // Getters
        public String getId() { return id; }
        public String getType() { return type; }
        public String getMessage() { return message; }
        public String getSeverity() { return severity; }
        public long getTimestamp() { return timestamp; }
    }
    
    // Start monitoring
    public void startMonitoring() {
        System.out.println("Starting database monitoring...");
        
        // Monitor performance every 30 seconds
        scheduler.scheduleAtFixedRate(this::monitorPerformance, 0, 30, TimeUnit.SECONDS);
        
        // Monitor resources every 60 seconds
        scheduler.scheduleAtFixedRate(this::monitorResources, 0, 60, TimeUnit.SECONDS);
        
        // Monitor connections every 10 seconds
        scheduler.scheduleAtFixedRate(this::monitorConnections, 0, 10, TimeUnit.SECONDS);
    }
    
    // Monitor performance
    private void monitorPerformance() {
        try {
            // Check slow queries
            String sql = "SELECT COUNT(*) FROM information_schema.processlist WHERE time > 5";
            try (Statement stmt = connection.createStatement();
                 ResultSet rs = stmt.executeQuery(sql)) {
                
                if (rs.next()) {
                    int slowQueries = rs.getInt(1);
                    if (slowQueries > 0) {
                        createAlert("PERFORMANCE", "Slow queries detected: " + slowQueries, "WARNING");
                    }
                }
            }
            
        } catch (SQLException e) {
            System.err.println("Performance monitoring error: " + e.getMessage());
        }
    }
    
    // Monitor resources
    private void monitorResources() {
        try {
            // Check disk usage
            String sql = "SELECT ROUND(SUM(data_length + index_length) / 1024 / 1024, 1) AS 'DB Size in MB' FROM information_schema.tables";
            try (Statement stmt = connection.createStatement();
                 ResultSet rs = stmt.executeQuery(sql)) {
                
                if (rs.next()) {
                    double dbSize = rs.getDouble(1);
                    if (dbSize > 1000) { // 1GB threshold
                        createAlert("RESOURCE", "Database size exceeds 1GB: " + dbSize + "MB", "WARNING");
                    }
                }
            }
            
        } catch (SQLException e) {
            System.err.println("Resource monitoring error: " + e.getMessage());
        }
    }
    
    // Monitor connections
    private void monitorConnections() {
        try {
            // Check active connections
            String sql = "SELECT COUNT(*) FROM information_schema.processlist";
            try (Statement stmt = connection.createStatement();
                 ResultSet rs = stmt.executeQuery(sql)) {
                
                if (rs.next()) {
                    int activeConnections = rs.getInt(1);
                    if (activeConnections > 100) { // 100 connection threshold
                        createAlert("CONNECTION", "High connection count: " + activeConnections, "WARNING");
                    }
                }
            }
            
        } catch (SQLException e) {
            System.err.println("Connection monitoring error: " + e.getMessage());
        }
    }
    
    // Create alert
    private void createAlert(String type, String message, String severity) {
        String alertId = UUID.randomUUID().toString();
        Alert alert = new Alert(alertId, type, message, severity);
        alerts.add(alert);
        
        System.out.println("ALERT [" + severity + "]: " + message);
        
        // In real implementation, send alert to monitoring system
        sendAlert(alert);
    }
    
    // Send alert
    private void sendAlert(Alert alert) {
        // In real implementation, send to monitoring system (e.g., email, Slack, PagerDuty)
        System.out.println("Sending alert: " + alert.getMessage());
    }
    
    // Get recent alerts
    public List<Alert> getRecentAlerts(long timeWindowMs) {
        long currentTime = System.currentTimeMillis();
        return alerts.stream()
            .filter(alert -> currentTime - alert.getTimestamp() < timeWindowMs)
            .collect(Collectors.toList());
    }
    
    // Stop monitoring
    public void stopMonitoring() {
        scheduler.shutdown();
        System.out.println("Database monitoring stopped");
    }
}
```

## 19.8 Database Operations (DBOps)

Database Operations (DBOps) involves the day-to-day operations and maintenance of database systems.

### DBOps Activities:
- **Monitoring**: Continuous monitoring of database health
- **Maintenance**: Regular maintenance tasks
- **Backup**: Backup and recovery operations
- **Performance Tuning**: Optimizing database performance
- **Security**: Security monitoring and updates
- **Incident Response**: Handling database incidents

### Real-World Analogy:
DBOps is like maintaining a building:
- **Monitoring** = Building surveillance
- **Maintenance** = Regular upkeep
- **Backup** = Emergency systems
- **Performance Tuning** = Optimizing systems
- **Security** = Security measures
- **Incident Response** = Emergency response

### Java Example - Database Operations:
```java
import java.sql.*;
import java.util.*;

public class DatabaseOperations {
    private Connection connection;
    
    public DatabaseOperations(Connection connection) {
        this.connection = connection;
    }
    
    // Daily maintenance tasks
    public void performDailyMaintenance() throws SQLException {
        System.out.println("Performing daily maintenance...");
        
        // Update statistics
        updateStatistics();
        
        // Check for errors
        checkForErrors();
        
        // Clean up old data
        cleanupOldData();
        
        System.out.println("Daily maintenance completed");
    }
    
    // Update statistics
    private void updateStatistics() throws SQLException {
        System.out.println("Updating database statistics...");
        
        String sql = "ANALYZE TABLE users, posts, comments";
        try (Statement stmt = connection.createStatement()) {
            stmt.execute(sql);
        }
    }
    
    // Check for errors
    private void checkForErrors() throws SQLException {
        System.out.println("Checking for database errors...");
        
        String sql = "SHOW ENGINE INNODB STATUS";
        try (Statement stmt = connection.createStatement();
             ResultSet rs = stmt.executeQuery(sql)) {
            
            if (rs.next()) {
                String status = rs.getString(1);
                if (status.contains("ERROR")) {
                    System.out.println("Database errors detected");
                } else {
                    System.out.println("No database errors found");
                }
            }
        }
    }
    
    // Clean up old data
    private void cleanupOldData() throws SQLException {
        System.out.println("Cleaning up old data...");
        
        // Delete old log entries
        String sql = "DELETE FROM logs WHERE created_at < DATE_SUB(NOW(), INTERVAL 30 DAY)";
        try (Statement stmt = connection.createStatement()) {
            int deletedRows = stmt.executeUpdate(sql);
            System.out.println("Deleted " + deletedRows + " old log entries");
        }
    }
    
    // Performance tuning
    public void performPerformanceTuning() throws SQLException {
        System.out.println("Performing performance tuning...");
        
        // Check slow query log
        checkSlowQueries();
        
        // Optimize tables
        optimizeTables();
        
        // Check indexes
        checkIndexes();
        
        System.out.println("Performance tuning completed");
    }
    
    // Check slow queries
    private void checkSlowQueries() throws SQLException {
        System.out.println("Checking slow queries...");
        
        String sql = "SELECT COUNT(*) FROM information_schema.processlist WHERE time > 10";
        try (Statement stmt = connection.createStatement();
             ResultSet rs = stmt.executeQuery(sql)) {
            
            if (rs.next()) {
                int slowQueries = rs.getInt(1);
                if (slowQueries > 0) {
                    System.out.println("Found " + slowQueries + " slow queries");
                } else {
                    System.out.println("No slow queries found");
                }
            }
        }
    }
    
    // Optimize tables
    private void optimizeTables() throws SQLException {
        System.out.println("Optimizing tables...");
        
        String[] tables = {"users", "posts", "comments"};
        for (String table : tables) {
            String sql = "OPTIMIZE TABLE " + table;
            try (Statement stmt = connection.createStatement()) {
                stmt.execute(sql);
                System.out.println("Optimized table: " + table);
            }
        }
    }
    
    // Check indexes
    private void checkIndexes() throws SQLException {
        System.out.println("Checking indexes...");
        
        String sql = "SHOW INDEX FROM users";
        try (Statement stmt = connection.createStatement();
             ResultSet rs = stmt.executeQuery(sql)) {
            
            System.out.println("Indexes on users table:");
            while (rs.next()) {
                System.out.println("  " + rs.getString("Key_name") + 
                                 " (" + rs.getString("Column_name") + ")");
            }
        }
    }
    
    // Incident response
    public void handleIncident(String incidentType) throws SQLException {
        System.out.println("Handling incident: " + incidentType);
        
        switch (incidentType) {
            case "CONNECTION_ISSUE":
                handleConnectionIssue();
                break;
            case "PERFORMANCE_ISSUE":
                handlePerformanceIssue();
                break;
            case "DATA_CORRUPTION":
                handleDataCorruption();
                break;
            default:
                System.out.println("Unknown incident type: " + incidentType);
        }
    }
    
    // Handle connection issue
    private void handleConnectionIssue() throws SQLException {
        System.out.println("Handling connection issue...");
        
        // Check connection status
        if (connection.isClosed()) {
            System.out.println("Connection is closed, attempting to reconnect...");
            // In real implementation, reconnect
        } else {
            System.out.println("Connection is active");
        }
    }
    
    // Handle performance issue
    private void handlePerformanceIssue() throws SQLException {
        System.out.println("Handling performance issue...");
        
        // Kill long-running queries
        String sql = "SELECT ID FROM information_schema.processlist WHERE time > 300";
        try (Statement stmt = connection.createStatement();
             ResultSet rs = stmt.executeQuery(sql)) {
            
            while (rs.next()) {
                int processId = rs.getInt("ID");
                System.out.println("Killing long-running query: " + processId);
                // In real implementation, kill the query
            }
        }
    }
    
    // Handle data corruption
    private void handleDataCorruption() throws SQLException {
        System.out.println("Handling data corruption...");
        
        // Check table integrity
        String sql = "CHECK TABLE users, posts, comments";
        try (Statement stmt = connection.createStatement();
             ResultSet rs = stmt.executeQuery(sql)) {
            
            while (rs.next()) {
                String table = rs.getString("Table");
                String status = rs.getString("Msg_text");
                System.out.println("Table " + table + ": " + status);
            }
        }
    }
}
```