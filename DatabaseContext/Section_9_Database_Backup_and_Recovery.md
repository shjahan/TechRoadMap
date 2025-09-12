# Section 9 – Database Backup and Recovery

## 9.1 Backup Strategies

Database backup strategies ensure data protection and business continuity by creating copies of data that can be restored when needed.

### Backup Types:
- **Full Backup**: Complete copy of all data
- **Incremental Backup**: Only changed data since last backup
- **Differential Backup**: All changes since last full backup
- **Continuous Backup**: Real-time data replication
- **Snapshot Backup**: Point-in-time data capture

### Real-World Analogy:
Backup strategies are like document management:
- **Full Backup** = Complete photocopy of all documents
- **Incremental Backup** = Only copy new/changed documents
- **Differential Backup** = Copy all changes since last full copy
- **Continuous Backup** = Live document synchronization
- **Snapshot Backup** = Photograph of documents at specific time

### Java Example - Backup Implementation:
```java
import java.io.*;
import java.sql.*;
import java.time.LocalDateTime;

public class DatabaseBackup {
    private Connection connection;
    
    public DatabaseBackup(Connection connection) {
        this.connection = connection;
    }
    
    // Full database backup
    public void fullBackup(String backupPath) throws SQLException, IOException {
        String timestamp = LocalDateTime.now().toString().replace(":", "-");
        String backupFile = backupPath + "/full_backup_" + timestamp + ".sql";
        
        // Create backup using mysqldump
        ProcessBuilder pb = new ProcessBuilder(
            "mysqldump", 
            "--user=root", 
            "--password=password", 
            "--all-databases", 
            "--routines", 
            "--triggers",
            "--single-transaction",
            "--result-file=" + backupFile
        );
        
        Process process = pb.start();
        int exitCode = process.waitFor();
        
        if (exitCode == 0) {
            System.out.println("Full backup completed: " + backupFile);
        } else {
            System.err.println("Full backup failed with exit code: " + exitCode);
        }
    }
    
    // Incremental backup using binary logs
    public void incrementalBackup(String backupPath) throws SQLException, IOException {
        String timestamp = LocalDateTime.now().toString().replace(":", "-");
        String backupFile = backupPath + "/incremental_backup_" + timestamp + ".sql";
        
        // Flush binary logs
        try (Statement stmt = connection.createStatement()) {
            stmt.execute("FLUSH BINARY LOGS");
        }
        
        // Get current binary log file
        String currentLogFile = getCurrentBinaryLogFile();
        
        // Create incremental backup
        ProcessBuilder pb = new ProcessBuilder(
            "mysqlbinlog",
            "--start-datetime=" + getLastBackupTime(),
            currentLogFile,
            "--result-file=" + backupFile
        );
        
        Process process = pb.start();
        int exitCode = process.waitFor();
        
        if (exitCode == 0) {
            System.out.println("Incremental backup completed: " + backupFile);
        } else {
            System.err.println("Incremental backup failed with exit code: " + exitCode);
        }
    }
    
    private String getCurrentBinaryLogFile() throws SQLException {
        String sql = "SHOW MASTER STATUS";
        try (Statement stmt = connection.createStatement();
             ResultSet rs = stmt.executeQuery(sql)) {
            if (rs.next()) {
                return rs.getString("File");
            }
        }
        return null;
    }
    
    private String getLastBackupTime() {
        // Return timestamp of last backup
        return "2024-01-01 00:00:00";
    }
}
```

## 9.2 Full, Incremental, and Differential Backups

Understanding different backup types helps choose the right strategy for data protection and recovery time objectives.

### Full Backup:
- **Complete Data**: All data and database objects
- **Recovery Time**: Fastest restore time
- **Storage Space**: Highest storage requirements
- **Frequency**: Typically daily or weekly

### Incremental Backup:
- **Changed Data Only**: Only data changed since last backup
- **Recovery Time**: Slower (requires all incremental backups)
- **Storage Space**: Lowest storage requirements
- **Frequency**: Typically hourly or daily

### Differential Backup:
- **Cumulative Changes**: All changes since last full backup
- **Recovery Time**: Moderate (requires full + last differential)
- **Storage Space**: Moderate storage requirements
- **Frequency**: Typically daily

### Real-World Analogy:
Backup types are like different photo storage strategies:
- **Full Backup** = Complete photo album copy
- **Incremental Backup** = Only new photos since last backup
- **Differential Backup** = All photos since last complete album

### SQL Example - Backup Types:
```sql
-- Full backup using mysqldump
mysqldump --user=root --password=password --all-databases --single-transaction > full_backup.sql

-- Incremental backup using binary logs
mysqlbinlog --start-datetime="2024-01-01 00:00:00" mysql-bin.000001 > incremental_backup.sql

-- Differential backup (custom approach)
mysqldump --user=root --password=password --where="updated_at > '2024-01-01'" database_name > differential_backup.sql
```

## 9.3 Point-in-Time Recovery

Point-in-time recovery allows restoring a database to a specific moment in time, providing granular recovery options.

### Recovery Components:
- **Full Backup**: Base restore point
- **Binary Logs**: Transaction log for incremental recovery
- **Recovery Time**: Target point in time
- **Data Consistency**: Ensures data integrity

### Real-World Analogy:
Point-in-time recovery is like rewinding a video:
- **Full Backup** = Starting point of the video
- **Binary Logs** = Frame-by-frame recording
- **Recovery Time** = Specific moment to rewind to
- **Data Consistency** = Smooth playback without glitches

### Java Example - Point-in-Time Recovery:
```java
public class PointInTimeRecovery {
    private Connection connection;
    
    public PointInTimeRecovery(Connection connection) {
        this.connection = connection;
    }
    
    // Restore to specific point in time
    public void restoreToPointInTime(String targetTime, String backupPath) throws SQLException, IOException {
        System.out.println("Starting point-in-time recovery to: " + targetTime);
        
        // Step 1: Restore full backup
        restoreFullBackup(backupPath + "/full_backup.sql");
        
        // Step 2: Apply binary logs up to target time
        applyBinaryLogs(targetTime, backupPath);
        
        System.out.println("Point-in-time recovery completed");
    }
    
    private void restoreFullBackup(String backupFile) throws SQLException, IOException {
        ProcessBuilder pb = new ProcessBuilder(
            "mysql",
            "--user=root",
            "--password=password",
            "database_name",
            "<",
            backupFile
        );
        
        Process process = pb.start();
        int exitCode = process.waitFor();
        
        if (exitCode == 0) {
            System.out.println("Full backup restored successfully");
        } else {
            System.err.println("Full backup restore failed");
        }
    }
    
    private void applyBinaryLogs(String targetTime, String backupPath) throws SQLException, IOException {
        // Get binary log files
        List<String> logFiles = getBinaryLogFiles();
        
        for (String logFile : logFiles) {
            ProcessBuilder pb = new ProcessBuilder(
                "mysqlbinlog",
                "--start-datetime=" + getLastBackupTime(),
                "--stop-datetime=" + targetTime,
                logFile,
                "|",
                "mysql",
                "--user=root",
                "--password=password",
                "database_name"
            );
            
            Process process = pb.start();
            int exitCode = process.waitFor();
            
            if (exitCode == 0) {
                System.out.println("Applied binary log: " + logFile);
            } else {
                System.err.println("Failed to apply binary log: " + logFile);
                break;
            }
        }
    }
    
    private List<String> getBinaryLogFiles() throws SQLException {
        List<String> logFiles = new ArrayList<>();
        String sql = "SHOW BINARY LOGS";
        
        try (Statement stmt = connection.createStatement();
             ResultSet rs = stmt.executeQuery(sql)) {
            while (rs.next()) {
                logFiles.add(rs.getString("Log_name"));
            }
        }
        return logFiles;
    }
}
```

## 9.4 Disaster Recovery Planning

Disaster recovery planning ensures business continuity by preparing for various failure scenarios and defining recovery procedures.

### Disaster Types:
- **Natural Disasters**: Earthquakes, floods, hurricanes
- **Human Errors**: Accidental data deletion, configuration mistakes
- **Hardware Failures**: Server crashes, disk failures
- **Cyber Attacks**: Ransomware, data breaches
- **Power Outages**: Electrical failures, grid issues

### Recovery Objectives:
- **RTO (Recovery Time Objective)**: Maximum acceptable downtime
- **RPO (Recovery Point Objective)**: Maximum acceptable data loss
- **MTBF (Mean Time Between Failures)**: Average time between failures
- **MTTR (Mean Time To Recovery)**: Average time to restore service

### Real-World Analogy:
Disaster recovery is like having a fire evacuation plan:
- **Disaster Types** = Different emergency scenarios
- **Recovery Objectives** = How quickly to evacuate and what to save
- **Backup Procedures** = Emergency supplies and escape routes
- **Testing** = Fire drills and practice runs

### Java Example - Disaster Recovery:
```java
public class DisasterRecovery {
    private Connection connection;
    
    public DisasterRecovery(Connection connection) {
        this.connection = connection;
    }
    
    // Test disaster recovery procedures
    public void testDisasterRecovery() throws SQLException {
        System.out.println("Testing Disaster Recovery Procedures:");
        
        // Test 1: Data corruption recovery
        testDataCorruptionRecovery();
        
        // Test 2: Hardware failure recovery
        testHardwareFailureRecovery();
        
        // Test 3: Network failure recovery
        testNetworkFailureRecovery();
        
        System.out.println("Disaster recovery tests completed");
    }
    
    private void testDataCorruptionRecovery() throws SQLException {
        System.out.println("Testing data corruption recovery...");
        
        // Simulate data corruption
        try (Statement stmt = connection.createStatement()) {
            stmt.execute("UPDATE students SET email = 'corrupted' WHERE student_id = 1");
        }
        
        // Restore from backup
        restoreFromBackup("students", "student_id = 1");
        
        System.out.println("Data corruption recovery test completed");
    }
    
    private void testHardwareFailureRecovery() throws SQLException {
        System.out.println("Testing hardware failure recovery...");
        
        // Check if failover is working
        boolean failoverActive = checkFailoverStatus();
        
        if (failoverActive) {
            System.out.println("Failover system is active");
        } else {
            System.out.println("Failover system is not active - CRITICAL");
        }
    }
    
    private void testNetworkFailureRecovery() throws SQLException {
        System.out.println("Testing network failure recovery...");
        
        // Check connection to backup systems
        boolean backupReachable = checkBackupSystemReachability();
        
        if (backupReachable) {
            System.out.println("Backup systems are reachable");
        } else {
            System.out.println("Backup systems are not reachable - CRITICAL");
        }
    }
    
    private void restoreFromBackup(String tableName, String condition) throws SQLException {
        // Implementation for restoring specific data
        System.out.println("Restoring " + tableName + " where " + condition);
    }
    
    private boolean checkFailoverStatus() throws SQLException {
        // Check if failover system is active
        String sql = "SELECT @@read_only";
        try (Statement stmt = connection.createStatement();
             ResultSet rs = stmt.executeQuery(sql)) {
            if (rs.next()) {
                return rs.getInt(1) == 0; // 0 means not read-only
            }
        }
        return false;
    }
    
    private boolean checkBackupSystemReachability() {
        // Check if backup systems are reachable
        // This would typically involve network connectivity tests
        return true; // Simplified for example
    }
}
```

## 9.5 High Availability (HA)

High availability ensures continuous database service with minimal downtime through redundancy and failover mechanisms.

### HA Components:
- **Primary Database**: Main database server
- **Secondary Database**: Backup database server
- **Load Balancer**: Distributes requests
- **Monitoring**: Health checks and alerts
- **Failover**: Automatic switching to backup

### Real-World Analogy:
High availability is like having a backup generator:
- **Primary Database** = Main power source
- **Secondary Database** = Backup generator
- **Load Balancer** = Power distribution system
- **Monitoring** = Power monitoring system
- **Failover** = Automatic generator activation

### Java Example - High Availability:
```java
public class HighAvailability {
    private List<Connection> connections;
    private int currentConnectionIndex = 0;
    
    public HighAvailability(List<Connection> connections) {
        this.connections = connections;
    }
    
    // Get connection with failover
    public Connection getConnection() throws SQLException {
        for (int i = 0; i < connections.size(); i++) {
            int index = (currentConnectionIndex + i) % connections.size();
            Connection conn = connections.get(index);
            
            if (isConnectionHealthy(conn)) {
                currentConnectionIndex = index;
                return conn;
            }
        }
        
        throw new SQLException("No healthy connections available");
    }
    
    // Check connection health
    private boolean isConnectionHealthy(Connection conn) {
        try {
            if (conn.isClosed()) {
                return false;
            }
            
            // Test connection with simple query
            try (Statement stmt = conn.createStatement();
                 ResultSet rs = stmt.executeQuery("SELECT 1")) {
                return rs.next();
            }
        } catch (SQLException e) {
            return false;
        }
    }
    
    // Monitor database health
    public void monitorDatabaseHealth() throws SQLException {
        for (int i = 0; i < connections.size(); i++) {
            Connection conn = connections.get(i);
            boolean healthy = isConnectionHealthy(conn);
            
            System.out.println("Database " + i + ": " + (healthy ? "HEALTHY" : "UNHEALTHY"));
            
            if (!healthy) {
                // Log alert or trigger failover
                System.err.println("Database " + i + " is unhealthy - triggering failover");
            }
        }
    }
    
    // Execute query with automatic failover
    public ResultSet executeQueryWithFailover(String sql) throws SQLException {
        SQLException lastException = null;
        
        for (int i = 0; i < connections.size(); i++) {
            try {
                Connection conn = getConnection();
                Statement stmt = conn.createStatement();
                return stmt.executeQuery(sql);
            } catch (SQLException e) {
                lastException = e;
                System.err.println("Query failed on connection " + i + ": " + e.getMessage());
            }
        }
        
        throw new SQLException("Query failed on all connections", lastException);
    }
}
```

## 9.6 Database Replication

Database replication creates copies of data across multiple servers to improve availability, performance, and disaster recovery.

### Replication Types:
- **Master-Slave**: One master, multiple slaves
- **Master-Master**: Multiple masters
- **Circular**: Chain of replication
- **Multi-Master**: Multiple masters with conflict resolution

### Real-World Analogy:
Database replication is like having multiple copies of important documents:
- **Master-Slave** = Original document with photocopies
- **Master-Master** = Multiple original documents
- **Circular** = Document passed around in a circle
- **Multi-Master** = Multiple people editing the same document

### Java Example - Database Replication:
```java
public class DatabaseReplication {
    private Connection masterConnection;
    private List<Connection> slaveConnections;
    
    public DatabaseReplication(Connection masterConnection, List<Connection> slaveConnections) {
        this.masterConnection = masterConnection;
        this.slaveConnections = slaveConnections;
    }
    
    // Write to master
    public void writeToMaster(String sql) throws SQLException {
        try (Statement stmt = masterConnection.createStatement()) {
            stmt.execute(sql);
            System.out.println("Write operation completed on master");
        }
    }
    
    // Read from slaves
    public ResultSet readFromSlaves(String sql) throws SQLException {
        for (Connection slave : slaveConnections) {
            try {
                if (isSlaveHealthy(slave)) {
                    Statement stmt = slave.createStatement();
                    return stmt.executeQuery(sql);
                }
            } catch (SQLException e) {
                System.err.println("Slave read failed: " + e.getMessage());
            }
        }
        
        throw new SQLException("All slaves are unavailable");
    }
    
    // Check slave health
    private boolean isSlaveHealthy(Connection slave) throws SQLException {
        try {
            if (slave.isClosed()) {
                return false;
            }
            
            // Check replication lag
            String sql = "SHOW SLAVE STATUS";
            try (Statement stmt = slave.createStatement();
                 ResultSet rs = stmt.executeQuery(sql)) {
                if (rs.next()) {
                    int lag = rs.getInt("Seconds_Behind_Master");
                    return lag < 60; // Acceptable lag is less than 60 seconds
                }
            }
        } catch (SQLException e) {
            return false;
        }
        return false;
    }
    
    // Monitor replication status
    public void monitorReplicationStatus() throws SQLException {
        for (int i = 0; i < slaveConnections.size(); i++) {
            Connection slave = slaveConnections.get(i);
            
            try {
                String sql = "SHOW SLAVE STATUS";
                try (Statement stmt = slave.createStatement();
                     ResultSet rs = stmt.executeQuery(sql)) {
                    if (rs.next()) {
                        String status = rs.getString("Slave_IO_Running");
                        String sqlStatus = rs.getString("Slave_SQL_Running");
                        int lag = rs.getInt("Seconds_Behind_Master");
                        
                        System.out.printf("Slave %d: IO=%s, SQL=%s, Lag=%ds%n",
                            i, status, sqlStatus, lag);
                    }
                }
            } catch (SQLException e) {
                System.err.println("Slave " + i + " monitoring failed: " + e.getMessage());
            }
        }
    }
}
```

## 9.7 Failover and Failback

Failover automatically switches to a backup system when the primary system fails, while failback returns to the primary system when it's restored.

### Failover Types:
- **Automatic Failover**: System automatically switches
- **Manual Failover**: Administrator manually switches
- **Planned Failover**: Scheduled maintenance switch
- **Unplanned Failover**: Emergency failure switch

### Real-World Analogy:
Failover and failback are like having a backup driver:
- **Failover** = Backup driver takes over when main driver is unavailable
- **Failback** = Main driver resumes when available again
- **Automatic** = Backup driver automatically takes over
- **Manual** = Someone decides when to switch drivers

### Java Example - Failover and Failback:
```java
public class FailoverManager {
    private Connection primaryConnection;
    private Connection secondaryConnection;
    private boolean isFailoverActive = false;
    
    public FailoverManager(Connection primaryConnection, Connection secondaryConnection) {
        this.primaryConnection = primaryConnection;
        this.secondaryConnection = secondaryConnection;
    }
    
    // Check if failover is needed
    public void checkFailoverNeeded() throws SQLException {
        if (!isConnectionHealthy(primaryConnection)) {
            System.out.println("Primary connection unhealthy - initiating failover");
            initiateFailover();
        } else if (isFailoverActive && isConnectionHealthy(primaryConnection)) {
            System.out.println("Primary connection restored - initiating failback");
            initiateFailback();
        }
    }
    
    // Initiate failover
    public void initiateFailover() throws SQLException {
        if (!isFailoverActive) {
            isFailoverActive = true;
            System.out.println("Failover initiated - switching to secondary connection");
            
            // Update application configuration
            updateApplicationConfiguration(secondaryConnection);
            
            // Notify administrators
            notifyAdministrators("Failover initiated");
        }
    }
    
    // Initiate failback
    public void initiateFailback() throws SQLException {
        if (isFailoverActive) {
            isFailoverActive = false;
            System.out.println("Failback initiated - switching to primary connection");
            
            // Update application configuration
            updateApplicationConfiguration(primaryConnection);
            
            // Notify administrators
            notifyAdministrators("Failback initiated");
        }
    }
    
    // Get current connection
    public Connection getCurrentConnection() {
        return isFailoverActive ? secondaryConnection : primaryConnection;
    }
    
    // Check connection health
    private boolean isConnectionHealthy(Connection conn) {
        try {
            if (conn.isClosed()) {
                return false;
            }
            
            try (Statement stmt = conn.createStatement();
                 ResultSet rs = stmt.executeQuery("SELECT 1")) {
                return rs.next();
            }
        } catch (SQLException e) {
            return false;
        }
    }
    
    // Update application configuration
    private void updateApplicationConfiguration(Connection newConnection) {
        // Update connection pool or configuration
        System.out.println("Application configuration updated to use new connection");
    }
    
    // Notify administrators
    private void notifyAdministrators(String message) {
        System.out.println("Administrator notification: " + message);
        // Send email, SMS, or other notifications
    }
}
```

## 9.8 Business Continuity

Business continuity ensures that critical business functions continue during and after a disaster or disruption.

### Continuity Components:
- **Business Impact Analysis**: Identify critical functions
- **Recovery Strategies**: Define recovery approaches
- **Communication Plans**: Coordinate response efforts
- **Testing and Training**: Regular practice and updates
- **Documentation**: Maintain current procedures

### Real-World Analogy:
Business continuity is like having a comprehensive emergency plan:
- **Business Impact Analysis** = Identify what's most important
- **Recovery Strategies** = Plan how to restore operations
- **Communication Plans** = Coordinate with team members
- **Testing and Training** = Practice emergency procedures
- **Documentation** = Keep plans up to date

### Java Example - Business Continuity:
```java
public class BusinessContinuity {
    private Connection connection;
    
    public BusinessContinuity(Connection connection) {
        this.connection = connection;
    }
    
    // Assess business impact
    public void assessBusinessImpact() throws SQLException {
        System.out.println("Business Impact Assessment:");
        
        // Check critical tables
        checkCriticalTables();
        
        // Check data integrity
        checkDataIntegrity();
        
        // Check performance metrics
        checkPerformanceMetrics();
        
        System.out.println("Business impact assessment completed");
    }
    
    private void checkCriticalTables() throws SQLException {
        String[] criticalTables = {"users", "orders", "payments", "inventory"};
        
        for (String table : criticalTables) {
            String sql = "SELECT COUNT(*) as count FROM " + table;
            try (Statement stmt = connection.createStatement();
                 ResultSet rs = stmt.executeQuery(sql)) {
                if (rs.next()) {
                    int count = rs.getInt("count");
                    System.out.println("Table " + table + ": " + count + " records");
                }
            }
        }
    }
    
    private void checkDataIntegrity() throws SQLException {
        // Check for orphaned records
        String sql = """
            SELECT COUNT(*) as orphaned_count
            FROM orders o
            LEFT JOIN users u ON o.user_id = u.id
            WHERE u.id IS NULL
            """;
        
        try (Statement stmt = connection.createStatement();
             ResultSet rs = stmt.executeQuery(sql)) {
            if (rs.next()) {
                int orphanedCount = rs.getInt("orphaned_count");
                if (orphanedCount > 0) {
                    System.out.println("WARNING: " + orphanedCount + " orphaned records found");
                } else {
                    System.out.println("Data integrity check passed");
                }
            }
        }
    }
    
    private void checkPerformanceMetrics() throws SQLException {
        // Check slow queries
        String sql = """
            SELECT COUNT(*) as slow_queries
            FROM mysql.slow_log
            WHERE start_time > DATE_SUB(NOW(), INTERVAL 1 HOUR)
            """;
        
        try (Statement stmt = connection.createStatement();
             ResultSet rs = stmt.executeQuery(sql)) {
            if (rs.next()) {
                int slowQueries = rs.getInt("slow_queries");
                System.out.println("Slow queries in last hour: " + slowQueries);
            }
        }
    }
}
```