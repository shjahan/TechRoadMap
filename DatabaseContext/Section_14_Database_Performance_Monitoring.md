# Section 14 – Database Performance Monitoring

## 14.1 Performance Metrics

Database performance metrics provide insights into system health, efficiency, and bottlenecks, enabling proactive optimization and troubleshooting.

### Key Performance Metrics:
- **Throughput**: Transactions per second (TPS)
- **Latency**: Response time for operations
- **CPU Usage**: Processor utilization percentage
- **Memory Usage**: RAM consumption and buffer pool efficiency
- **I/O Operations**: Disk read/write performance
- **Connection Count**: Active database connections
- **Lock Waits**: Time spent waiting for locks
- **Cache Hit Ratio**: Buffer pool hit percentage

### Real-World Analogy:
Performance metrics are like a car's dashboard:
- **Throughput** = Speedometer (transactions per second)
- **Latency** = Response time (how quickly you get there)
- **CPU Usage** = Engine RPM (how hard the engine is working)
- **Memory Usage** = Fuel gauge (how much memory is used)
- **I/O Operations** = Tire pressure (disk performance)
- **Connection Count** = Number of passengers
- **Lock Waits** = Traffic jams
- **Cache Hit Ratio** = How often you find what you need

### Java Example - Performance Metrics Collection:
```java
import java.sql.*;
import java.util.concurrent.Executors;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.TimeUnit;

public class PerformanceMetricsCollector {
    private Connection connection;
    private ScheduledExecutorService scheduler;
    private MetricsData metricsData;
    
    public PerformanceMetricsCollector(Connection connection) {
        this.connection = connection;
        this.scheduler = Executors.newScheduledThreadPool(1);
        this.metricsData = new MetricsData();
    }
    
    // Start metrics collection
    public void startCollection() {
        scheduler.scheduleAtFixedRate(this::collectMetrics, 0, 30, TimeUnit.SECONDS);
        System.out.println("Performance metrics collection started");
    }
    
    // Stop metrics collection
    public void stopCollection() {
        scheduler.shutdown();
        System.out.println("Performance metrics collection stopped");
    }
    
    // Collect performance metrics
    private void collectMetrics() {
        try {
            // Collect basic metrics
            collectBasicMetrics();
            
            // Collect query performance
            collectQueryMetrics();
            
            // Collect system metrics
            collectSystemMetrics();
            
            // Print metrics
            printMetrics();
            
        } catch (SQLException e) {
            System.err.println("Error collecting metrics: " + e.getMessage());
        }
    }
    
    private void collectBasicMetrics() throws SQLException {
        // Connection count
        String sql = "SHOW STATUS LIKE 'Threads_connected'";
        try (Statement stmt = connection.createStatement();
             ResultSet rs = stmt.executeQuery(sql)) {
            if (rs.next()) {
                metricsData.connectionCount = rs.getInt("Value");
            }
        }
        
        // Uptime
        sql = "SHOW STATUS LIKE 'Uptime'";
        try (Statement stmt = connection.createStatement();
             ResultSet rs = stmt.executeQuery(sql)) {
            if (rs.next()) {
                metricsData.uptime = rs.getLong("Value");
            }
        }
    }
    
    private void collectQueryMetrics() throws SQLException {
        // Slow queries
        String sql = "SHOW STATUS LIKE 'Slow_queries'";
        try (Statement stmt = connection.createStatement();
             ResultSet rs = stmt.executeQuery(sql)) {
            if (rs.next()) {
                metricsData.slowQueries = rs.getLong("Value");
            }
        }
        
        // Questions (queries)
        sql = "SHOW STATUS LIKE 'Questions'";
        try (Statement stmt = connection.createStatement();
             ResultSet rs = stmt.executeQuery(sql)) {
            if (rs.next()) {
                metricsData.totalQueries = rs.getLong("Value");
            }
        }
    }
    
    private void collectSystemMetrics() throws SQLException {
        // Buffer pool hit ratio
        String sql = """
            SELECT 
                (1 - (Innodb_buffer_pool_reads / Innodb_buffer_pool_read_requests)) * 100 as hit_ratio
            FROM (
                SELECT 
                    VARIABLE_VALUE as Innodb_buffer_pool_reads
                FROM information_schema.GLOBAL_STATUS 
                WHERE VARIABLE_NAME = 'Innodb_buffer_pool_reads'
            ) a
            CROSS JOIN (
                SELECT 
                    VARIABLE_VALUE as Innodb_buffer_pool_read_requests
                FROM information_schema.GLOBAL_STATUS 
                WHERE VARIABLE_NAME = 'Innodb_buffer_pool_read_requests'
            ) b
            """;
        
        try (Statement stmt = connection.createStatement();
             ResultSet rs = stmt.executeQuery(sql)) {
            if (rs.next()) {
                metricsData.cacheHitRatio = rs.getDouble("hit_ratio");
            }
        }
    }
    
    private void printMetrics() {
        System.out.println("=== Database Performance Metrics ===");
        System.out.println("Connection Count: " + metricsData.connectionCount);
        System.out.println("Uptime: " + metricsData.uptime + " seconds");
        System.out.println("Total Queries: " + metricsData.totalQueries);
        System.out.println("Slow Queries: " + metricsData.slowQueries);
        System.out.println("Cache Hit Ratio: " + String.format("%.2f", metricsData.cacheHitRatio) + "%");
        System.out.println("=====================================");
    }
    
    // Metrics data class
    private static class MetricsData {
        int connectionCount = 0;
        long uptime = 0;
        long totalQueries = 0;
        long slowQueries = 0;
        double cacheHitRatio = 0.0;
    }
}
```

## 14.2 Database Monitoring Tools

Database monitoring tools provide comprehensive visibility into database performance, health, and usage patterns.

### Monitoring Tool Categories:
- **Built-in Tools**: Database-specific monitoring
- **Third-party Tools**: Commercial monitoring solutions
- **Open-source Tools**: Free monitoring alternatives
- **Cloud Tools**: Managed monitoring services
- **Custom Tools**: Application-specific monitoring

### Real-World Analogy:
Database monitoring tools are like security cameras:
- **Built-in Tools** = Basic security system
- **Third-party Tools** = Professional security company
- **Open-source Tools** = DIY security system
- **Cloud Tools** = Remote monitoring service
- **Custom Tools** = Specialized surveillance

### Java Example - Custom Monitoring Tool:
```java
public class DatabaseMonitoringTool {
    private Connection connection;
    private Map<String, Long> queryTimes = new HashMap<>();
    private Map<String, Integer> queryCounts = new HashMap<>();
    
    public DatabaseMonitoringTool(Connection connection) {
        this.connection = connection;
    }
    
    // Monitor query execution
    public void monitorQuery(String queryName, String sql) throws SQLException {
        long startTime = System.currentTimeMillis();
        
        try (Statement stmt = connection.createStatement();
             ResultSet rs = stmt.executeQuery(sql)) {
            
            long endTime = System.currentTimeMillis();
            long executionTime = endTime - startTime;
            
            // Record metrics
            queryTimes.merge(queryName, executionTime, Long::max);
            queryCounts.merge(queryName, 1, Integer::sum);
            
            System.out.println("Query '" + queryName + "' executed in " + executionTime + "ms");
            
        } catch (SQLException e) {
            System.err.println("Query '" + queryName + "' failed: " + e.getMessage());
            throw e;
        }
    }
    
    // Get query statistics
    public void printQueryStatistics() {
        System.out.println("=== Query Statistics ===");
        for (String queryName : queryTimes.keySet()) {
            long maxTime = queryTimes.get(queryName);
            int count = queryCounts.get(queryName);
            double avgTime = (double) maxTime / count;
            
            System.out.println(queryName + ":");
            System.out.println("  Count: " + count);
            System.out.println("  Max Time: " + maxTime + "ms");
            System.out.println("  Avg Time: " + String.format("%.2f", avgTime) + "ms");
        }
        System.out.println("========================");
    }
    
    // Monitor connection pool
    public void monitorConnectionPool() throws SQLException {
        String sql = "SHOW STATUS LIKE 'Threads_connected'";
        try (Statement stmt = connection.createStatement();
             ResultSet rs = stmt.executeQuery(sql)) {
            if (rs.next()) {
                int connections = rs.getInt("Value");
                System.out.println("Active Connections: " + connections);
                
                if (connections > 100) {
                    System.out.println("WARNING: High connection count detected");
                }
            }
        }
    }
    
    // Monitor slow queries
    public void monitorSlowQueries() throws SQLException {
        String sql = "SHOW STATUS LIKE 'Slow_queries'";
        try (Statement stmt = connection.createStatement();
             ResultSet rs = stmt.executeQuery(sql)) {
            if (rs.next()) {
                long slowQueries = rs.getLong("Value");
                System.out.println("Slow Queries: " + slowQueries);
                
                if (slowQueries > 10) {
                    System.out.println("WARNING: High number of slow queries detected");
                }
            }
        }
    }
}
```

## 14.3 Query Performance Analysis

Query performance analysis identifies slow queries, bottlenecks, and optimization opportunities to improve database performance.

### Analysis Techniques:
- **Query Profiling**: Detailed execution analysis
- **Execution Plans**: Step-by-step query execution
- **Index Usage**: Index utilization analysis
- **Resource Consumption**: CPU, memory, I/O usage
- **Wait Events**: Time spent waiting for resources

### Real-World Analogy:
Query performance analysis is like diagnosing a car's performance:
- **Query Profiling** = Engine diagnostics
- **Execution Plans** = Step-by-step engine analysis
- **Index Usage** = Fuel efficiency analysis
- **Resource Consumption** = Engine load analysis
- **Wait Events** = Traffic jam analysis

### Java Example - Query Performance Analysis:
```java
public class QueryPerformanceAnalyzer {
    private Connection connection;
    
    public QueryPerformanceAnalyzer(Connection connection) {
        this.connection = connection;
    }
    
    // Analyze query performance
    public void analyzeQuery(String sql) throws SQLException {
        System.out.println("Analyzing query: " + sql);
        
        // Enable profiling
        try (Statement stmt = connection.createStatement()) {
            stmt.execute("SET profiling = 1");
        }
        
        // Execute query
        long startTime = System.currentTimeMillis();
        try (Statement stmt = connection.createStatement();
             ResultSet rs = stmt.executeQuery(sql)) {
            
            long endTime = System.currentTimeMillis();
            long executionTime = endTime - startTime;
            
            System.out.println("Query executed in " + executionTime + "ms");
            
            // Get detailed profile
            getQueryProfile();
            
        } finally {
            // Disable profiling
            try (Statement stmt = connection.createStatement()) {
                stmt.execute("SET profiling = 0");
            }
        }
    }
    
    // Get query profile
    private void getQueryProfile() throws SQLException {
        String sql = "SHOW PROFILES";
        try (Statement stmt = connection.createStatement();
             ResultSet rs = stmt.executeQuery(sql)) {
            
            System.out.println("Query Profile:");
            while (rs.next()) {
                System.out.println("Query ID: " + rs.getInt("Query_ID"));
                System.out.println("Duration: " + rs.getString("Duration"));
                System.out.println("Query: " + rs.getString("Query"));
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
                System.out.println("Query Time: " + rs.getString("query_time"));
                System.out.println("Lock Time: " + rs.getString("lock_time"));
                System.out.println("Rows Sent: " + rs.getInt("rows_sent"));
                System.out.println("Rows Examined: " + rs.getInt("rows_examined"));
                System.out.println("SQL: " + rs.getString("sql_text"));
                System.out.println("---");
            }
        }
    }
    
    // Check index usage
    public void checkIndexUsage(String tableName) throws SQLException {
        String sql = """
            SELECT 
                index_name,
                column_name,
                seq_in_index,
                cardinality
            FROM information_schema.statistics
            WHERE table_name = ? AND table_schema = DATABASE()
            ORDER BY index_name, seq_in_index
            """;
        
        try (PreparedStatement stmt = connection.prepareStatement(sql)) {
            stmt.setString(1, tableName);
            
            try (ResultSet rs = stmt.executeQuery()) {
                System.out.println("Index Usage for table " + tableName + ":");
                while (rs.next()) {
                    System.out.println("Index: " + rs.getString("index_name"));
                    System.out.println("Column: " + rs.getString("column_name"));
                    System.out.println("Sequence: " + rs.getInt("seq_in_index"));
                    System.out.println("Cardinality: " + rs.getLong("cardinality"));
                    System.out.println("---");
                }
            }
        }
    }
}
```

## 14.4 Resource Utilization Monitoring

Resource utilization monitoring tracks CPU, memory, disk, and network usage to identify bottlenecks and optimize performance.

### Resource Types:
- **CPU Utilization**: Processor usage percentage
- **Memory Usage**: RAM consumption and buffer pools
- **Disk I/O**: Read/write operations and latency
- **Network I/O**: Bandwidth usage and latency
- **Connection Usage**: Database connection utilization

### Real-World Analogy:
Resource utilization monitoring is like monitoring a factory:
- **CPU Utilization** = Machine usage
- **Memory Usage** = Raw material storage
- **Disk I/O** = Conveyor belt speed
- **Network I/O** = Transportation between departments
- **Connection Usage** = Worker availability

### Java Example - Resource Utilization Monitoring:
```java
public class ResourceUtilizationMonitor {
    private Connection connection;
    
    public ResourceUtilizationMonitor(Connection connection) {
        this.connection = connection;
    }
    
    // Monitor CPU usage
    public void monitorCPUUsage() throws SQLException {
        String sql = "SHOW STATUS LIKE 'Cpu_usage'";
        try (Statement stmt = connection.createStatement();
             ResultSet rs = stmt.executeQuery(sql)) {
            if (rs.next()) {
                String cpuUsage = rs.getString("Value");
                System.out.println("CPU Usage: " + cpuUsage);
            }
        }
    }
    
    // Monitor memory usage
    public void monitorMemoryUsage() throws SQLException {
        String sql = """
            SELECT 
                VARIABLE_NAME,
                VARIABLE_VALUE
            FROM information_schema.GLOBAL_STATUS
            WHERE VARIABLE_NAME IN (
                'Innodb_buffer_pool_pages_data',
                'Innodb_buffer_pool_pages_free',
                'Innodb_buffer_pool_pages_total'
            )
            """;
        
        try (Statement stmt = connection.createStatement();
             ResultSet rs = stmt.executeQuery(sql)) {
            
            System.out.println("Memory Usage:");
            while (rs.next()) {
                System.out.println(rs.getString("VARIABLE_NAME") + ": " + 
                                 rs.getString("VARIABLE_VALUE"));
            }
        }
    }
    
    // Monitor disk I/O
    public void monitorDiskIO() throws SQLException {
        String sql = """
            SELECT 
                VARIABLE_NAME,
                VARIABLE_VALUE
            FROM information_schema.GLOBAL_STATUS
            WHERE VARIABLE_NAME IN (
                'Innodb_data_reads',
                'Innodb_data_writes',
                'Innodb_data_read',
                'Innodb_data_written'
            )
            """;
        
        try (Statement stmt = connection.createStatement();
             ResultSet rs = stmt.executeQuery(sql)) {
            
            System.out.println("Disk I/O:");
            while (rs.next()) {
                System.out.println(rs.getString("VARIABLE_NAME") + ": " + 
                                 rs.getString("VARIABLE_VALUE"));
            }
        }
    }
    
    // Monitor connection usage
    public void monitorConnectionUsage() throws SQLException {
        String sql = "SHOW STATUS LIKE 'Threads_connected'";
        try (Statement stmt = connection.createStatement();
             ResultSet rs = stmt.executeQuery(sql)) {
            if (rs.next()) {
                int connections = rs.getInt("Value");
                System.out.println("Active Connections: " + connections);
                
                // Check if approaching limit
                String maxConnSql = "SHOW VARIABLES LIKE 'max_connections'";
                try (Statement maxStmt = connection.createStatement();
                     ResultSet maxRs = maxStmt.executeQuery(maxConnSql)) {
                    if (maxRs.next()) {
                        int maxConnections = maxRs.getInt("Value");
                        double usagePercent = (double) connections / maxConnections * 100;
                        System.out.println("Connection Usage: " + String.format("%.2f", usagePercent) + "%");
                        
                        if (usagePercent > 80) {
                            System.out.println("WARNING: High connection usage detected");
                        }
                    }
                }
            }
        }
    }
}
```

## 14.5 Alerting and Notification

Alerting and notification systems provide real-time alerts when database performance issues or anomalies are detected.

### Alert Types:
- **Performance Alerts**: Slow queries, high CPU usage
- **Resource Alerts**: Memory usage, disk space
- **Error Alerts**: Connection failures, query errors
- **Threshold Alerts**: Exceeding predefined limits
- **Anomaly Alerts**: Unusual patterns or behaviors

### Real-World Analogy:
Alerting and notification are like smoke detectors:
- **Performance Alerts** = Smoke detector for slow performance
- **Resource Alerts** = Low battery warning
- **Error Alerts** = Fire alarm
- **Threshold Alerts** = Temperature warning
- **Anomaly Alerts** = Unusual smoke pattern detection

### Java Example - Alerting System:
```java
import java.util.concurrent.Executors;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.TimeUnit;

public class DatabaseAlertingSystem {
    private Connection connection;
    private ScheduledExecutorService scheduler;
    private AlertThresholds thresholds;
    
    public DatabaseAlertingSystem(Connection connection) {
        this.connection = connection;
        this.scheduler = Executors.newScheduledThreadPool(1);
        this.thresholds = new AlertThresholds();
    }
    
    // Start alerting system
    public void startAlerting() {
        scheduler.scheduleAtFixedRate(this::checkAlerts, 0, 60, TimeUnit.SECONDS);
        System.out.println("Database alerting system started");
    }
    
    // Stop alerting system
    public void stopAlerting() {
        scheduler.shutdown();
        System.out.println("Database alerting system stopped");
    }
    
    // Check for alerts
    private void checkAlerts() {
        try {
            checkPerformanceAlerts();
            checkResourceAlerts();
            checkErrorAlerts();
        } catch (SQLException e) {
            System.err.println("Error checking alerts: " + e.getMessage());
        }
    }
    
    // Check performance alerts
    private void checkPerformanceAlerts() throws SQLException {
        // Check slow queries
        String sql = "SHOW STATUS LIKE 'Slow_queries'";
        try (Statement stmt = connection.createStatement();
             ResultSet rs = stmt.executeQuery(sql)) {
            if (rs.next()) {
                long slowQueries = rs.getLong("Value");
                if (slowQueries > thresholds.maxSlowQueries) {
                    sendAlert("PERFORMANCE", "High number of slow queries: " + slowQueries);
                }
            }
        }
    }
    
    // Check resource alerts
    private void checkResourceAlerts() throws SQLException {
        // Check connection count
        String sql = "SHOW STATUS LIKE 'Threads_connected'";
        try (Statement stmt = connection.createStatement();
             ResultSet rs = stmt.executeQuery(sql)) {
            if (rs.next()) {
                int connections = rs.getInt("Value");
                if (connections > thresholds.maxConnections) {
                    sendAlert("RESOURCE", "High connection count: " + connections);
                }
            }
        }
    }
    
    // Check error alerts
    private void checkErrorAlerts() throws SQLException {
        // Check for connection errors
        String sql = "SHOW STATUS LIKE 'Connection_errors_internal'";
        try (Statement stmt = connection.createStatement();
             ResultSet rs = stmt.executeQuery(sql)) {
            if (rs.next()) {
                long errors = rs.getLong("Value");
                if (errors > thresholds.maxErrors) {
                    sendAlert("ERROR", "High number of connection errors: " + errors);
                }
            }
        }
    }
    
    // Send alert
    private void sendAlert(String type, String message) {
        System.out.println("ALERT [" + type + "]: " + message);
        
        // In real implementation, this would send email, SMS, or other notifications
        // For example:
        // emailService.sendAlert(type, message);
        // smsService.sendAlert(type, message);
        // slackService.sendAlert(type, message);
    }
    
    // Alert thresholds
    private static class AlertThresholds {
        long maxSlowQueries = 10;
        int maxConnections = 100;
        long maxErrors = 5;
    }
}
```

## 14.6 Capacity Planning

Capacity planning involves predicting future resource needs and ensuring the database can handle expected growth and load.

### Planning Factors:
- **Historical Data**: Past performance trends
- **Growth Projections**: Expected data and user growth
- **Performance Requirements**: Response time and throughput needs
- **Resource Constraints**: Hardware and budget limitations
- **Scaling Strategies**: Vertical vs horizontal scaling

### Real-World Analogy:
Capacity planning is like city planning:
- **Historical Data** = Past population growth
- **Growth Projections** = Expected population increase
- **Performance Requirements** = Traffic flow needs
- **Resource Constraints** = Budget and land availability
- **Scaling Strategies** = Building up vs building out

### Java Example - Capacity Planning:
```java
public class CapacityPlanner {
    private Connection connection;
    private List<PerformanceData> historicalData = new ArrayList<>();
    
    public CapacityPlanner(Connection connection) {
        this.connection = connection;
    }
    
    // Collect historical data
    public void collectHistoricalData() throws SQLException {
        String sql = """
            SELECT 
                DATE(created_at) as date,
                COUNT(*) as daily_queries,
                AVG(execution_time) as avg_execution_time
            FROM query_log
            WHERE created_at >= DATE_SUB(NOW(), INTERVAL 30 DAY)
            GROUP BY DATE(created_at)
            ORDER BY date
            """;
        
        try (Statement stmt = connection.createStatement();
             ResultSet rs = stmt.executeQuery(sql)) {
            
            while (rs.next()) {
                PerformanceData data = new PerformanceData();
                data.date = rs.getDate("date");
                data.dailyQueries = rs.getLong("daily_queries");
                data.avgExecutionTime = rs.getDouble("avg_execution_time");
                historicalData.add(data);
            }
        }
    }
    
    // Predict future capacity needs
    public void predictCapacityNeeds(int daysAhead) {
        if (historicalData.size() < 7) {
            System.out.println("Insufficient historical data for prediction");
            return;
        }
        
        // Simple linear regression for prediction
        double[] x = new double[historicalData.size()];
        double[] y = new double[historicalData.size()];
        
        for (int i = 0; i < historicalData.size(); i++) {
            x[i] = i;
            y[i] = historicalData.get(i).dailyQueries;
        }
        
        // Calculate slope and intercept
        double slope = calculateSlope(x, y);
        double intercept = calculateIntercept(x, y, slope);
        
        // Predict future values
        int futureIndex = historicalData.size() + daysAhead;
        double predictedQueries = slope * futureIndex + intercept;
        
        System.out.println("Capacity Prediction for " + daysAhead + " days ahead:");
        System.out.println("Predicted daily queries: " + String.format("%.0f", predictedQueries));
        
        // Calculate resource requirements
        calculateResourceRequirements(predictedQueries);
    }
    
    // Calculate slope for linear regression
    private double calculateSlope(double[] x, double[] y) {
        int n = x.length;
        double sumX = 0, sumY = 0, sumXY = 0, sumXX = 0;
        
        for (int i = 0; i < n; i++) {
            sumX += x[i];
            sumY += y[i];
            sumXY += x[i] * y[i];
            sumXX += x[i] * x[i];
        }
        
        return (n * sumXY - sumX * sumY) / (n * sumXX - sumX * sumX);
    }
    
    // Calculate intercept for linear regression
    private double calculateIntercept(double[] x, double[] y, double slope) {
        double sumX = 0, sumY = 0;
        for (int i = 0; i < x.length; i++) {
            sumX += x[i];
            sumY += y[i];
        }
        return (sumY - slope * sumX) / x.length;
    }
    
    // Calculate resource requirements
    private void calculateResourceRequirements(double predictedQueries) {
        // Estimate CPU requirements (queries per second)
        double queriesPerSecond = predictedQueries / 86400; // 24 hours
        double cpuCores = queriesPerSecond / 1000; // Assume 1000 queries per core
        
        // Estimate memory requirements
        double memoryGB = queriesPerSecond * 0.1; // Assume 0.1GB per query per second
        
        // Estimate storage requirements
        double storageGB = predictedQueries * 0.001; // Assume 0.001GB per query
        
        System.out.println("Estimated Resource Requirements:");
        System.out.println("CPU Cores: " + String.format("%.2f", cpuCores));
        System.out.println("Memory (GB): " + String.format("%.2f", memoryGB));
        System.out.println("Storage (GB): " + String.format("%.2f", storageGB));
    }
    
    // Performance data class
    private static class PerformanceData {
        java.sql.Date date;
        long dailyQueries;
        double avgExecutionTime;
    }
}
```

## 14.7 Performance Benchmarking

Performance benchmarking compares database performance against established standards and identifies optimization opportunities.

### Benchmarking Types:
- **Synthetic Benchmarks**: Artificial workload testing
- **Real-world Benchmarks**: Production-like workload testing
- **Comparative Benchmarks**: Comparing different configurations
- **Regression Benchmarks**: Detecting performance regressions
- **Load Testing**: Testing under various load conditions

### Real-World Analogy:
Performance benchmarking is like car testing:
- **Synthetic Benchmarks** = Test track performance
- **Real-world Benchmarks** = City driving conditions
- **Comparative Benchmarks** = Comparing different car models
- **Regression Benchmarks** = Before/after maintenance testing
- **Load Testing** = Testing with different passenger loads

### Java Example - Performance Benchmarking:
```java
public class PerformanceBenchmark {
    private Connection connection;
    private BenchmarkResults results;
    
    public PerformanceBenchmark(Connection connection) {
        this.connection = connection;
        this.results = new BenchmarkResults();
    }
    
    // Run benchmark tests
    public void runBenchmark() throws SQLException {
        System.out.println("Starting performance benchmark...");
        
        // Test 1: Simple SELECT queries
        benchmarkSelectQueries();
        
        // Test 2: Complex JOIN queries
        benchmarkJoinQueries();
        
        // Test 3: INSERT operations
        benchmarkInsertOperations();
        
        // Test 4: UPDATE operations
        benchmarkUpdateOperations();
        
        // Test 5: DELETE operations
        benchmarkDeleteOperations();
        
        // Print results
        printBenchmarkResults();
    }
    
    // Benchmark SELECT queries
    private void benchmarkSelectQueries() throws SQLException {
        String sql = "SELECT * FROM students WHERE gpa > 3.0";
        long totalTime = 0;
        int iterations = 100;
        
        for (int i = 0; i < iterations; i++) {
            long startTime = System.currentTimeMillis();
            
            try (Statement stmt = connection.createStatement();
                 ResultSet rs = stmt.executeQuery(sql)) {
                while (rs.next()) {
                    // Process result
                }
            }
            
            long endTime = System.currentTimeMillis();
            totalTime += (endTime - startTime);
        }
        
        results.selectAvgTime = (double) totalTime / iterations;
        System.out.println("SELECT queries benchmark completed");
    }
    
    // Benchmark JOIN queries
    private void benchmarkJoinQueries() throws SQLException {
        String sql = """
            SELECT s.name, c.course_name, e.grade
            FROM students s
            JOIN enrollments e ON s.id = e.student_id
            JOIN courses c ON e.course_id = c.id
            WHERE s.gpa > 3.0
            """;
        
        long totalTime = 0;
        int iterations = 50;
        
        for (int i = 0; i < iterations; i++) {
            long startTime = System.currentTimeMillis();
            
            try (Statement stmt = connection.createStatement();
                 ResultSet rs = stmt.executeQuery(sql)) {
                while (rs.next()) {
                    // Process result
                }
            }
            
            long endTime = System.currentTimeMillis();
            totalTime += (endTime - startTime);
        }
        
        results.joinAvgTime = (double) totalTime / iterations;
        System.out.println("JOIN queries benchmark completed");
    }
    
    // Benchmark INSERT operations
    private void benchmarkInsertOperations() throws SQLException {
        String sql = "INSERT INTO test_table (name, value) VALUES (?, ?)";
        long totalTime = 0;
        int iterations = 1000;
        
        try (PreparedStatement stmt = connection.prepareStatement(sql)) {
            for (int i = 0; i < iterations; i++) {
                long startTime = System.currentTimeMillis();
                
                stmt.setString(1, "test" + i);
                stmt.setString(2, "value" + i);
                stmt.executeUpdate();
                
                long endTime = System.currentTimeMillis();
                totalTime += (endTime - startTime);
            }
        }
        
        results.insertAvgTime = (double) totalTime / iterations;
        System.out.println("INSERT operations benchmark completed");
    }
    
    // Benchmark UPDATE operations
    private void benchmarkUpdateOperations() throws SQLException {
        String sql = "UPDATE test_table SET value = ? WHERE name = ?";
        long totalTime = 0;
        int iterations = 500;
        
        try (PreparedStatement stmt = connection.prepareStatement(sql)) {
            for (int i = 0; i < iterations; i++) {
                long startTime = System.currentTimeMillis();
                
                stmt.setString(1, "updated" + i);
                stmt.setString(2, "test" + i);
                stmt.executeUpdate();
                
                long endTime = System.currentTimeMillis();
                totalTime += (endTime - startTime);
            }
        }
        
        results.updateAvgTime = (double) totalTime / iterations;
        System.out.println("UPDATE operations benchmark completed");
    }
    
    // Benchmark DELETE operations
    private void benchmarkDeleteOperations() throws SQLException {
        String sql = "DELETE FROM test_table WHERE name = ?";
        long totalTime = 0;
        int iterations = 500;
        
        try (PreparedStatement stmt = connection.prepareStatement(sql)) {
            for (int i = 0; i < iterations; i++) {
                long startTime = System.currentTimeMillis();
                
                stmt.setString(1, "test" + i);
                stmt.executeUpdate();
                
                long endTime = System.currentTimeMillis();
                totalTime += (endTime - startTime);
            }
        }
        
        results.deleteAvgTime = (double) totalTime / iterations;
        System.out.println("DELETE operations benchmark completed");
    }
    
    // Print benchmark results
    private void printBenchmarkResults() {
        System.out.println("=== Benchmark Results ===");
        System.out.println("SELECT queries: " + String.format("%.2f", results.selectAvgTime) + "ms");
        System.out.println("JOIN queries: " + String.format("%.2f", results.joinAvgTime) + "ms");
        System.out.println("INSERT operations: " + String.format("%.2f", results.insertAvgTime) + "ms");
        System.out.println("UPDATE operations: " + String.format("%.2f", results.updateAvgTime) + "ms");
        System.out.println("DELETE operations: " + String.format("%.2f", results.deleteAvgTime) + "ms");
        System.out.println("========================");
    }
    
    // Benchmark results class
    private static class BenchmarkResults {
        double selectAvgTime = 0.0;
        double joinAvgTime = 0.0;
        double insertAvgTime = 0.0;
        double updateAvgTime = 0.0;
        double deleteAvgTime = 0.0;
    }
}
```

## 14.8 Troubleshooting Performance Issues

Troubleshooting performance issues involves identifying root causes and implementing solutions to resolve database performance problems.

### Troubleshooting Steps:
- **Identify Symptoms**: Slow queries, high CPU, memory issues
- **Gather Data**: Performance metrics, logs, execution plans
- **Analyze Root Causes**: Bottlenecks, resource constraints
- **Implement Solutions**: Optimize queries, add indexes, scale resources
- **Monitor Results**: Verify improvements and prevent regressions

### Real-World Analogy:
Troubleshooting performance issues is like diagnosing a sick patient:
- **Identify Symptoms** = Fever, pain, fatigue
- **Gather Data** = Medical tests, X-rays, blood work
- **Analyze Root Causes** = Infection, injury, disease
- **Implement Solutions** = Medication, surgery, therapy
- **Monitor Results** = Follow-up appointments, tests

### Java Example - Performance Troubleshooting:
```java
public class PerformanceTroubleshooter {
    private Connection connection;
    
    public PerformanceTroubleshooter(Connection connection) {
        this.connection = connection;
    }
    
    // Diagnose performance issues
    public void diagnosePerformanceIssues() throws SQLException {
        System.out.println("Diagnosing performance issues...");
        
        // Check for slow queries
        checkSlowQueries();
        
        // Check for missing indexes
        checkMissingIndexes();
        
        // Check for resource constraints
        checkResourceConstraints();
        
        // Check for lock contention
        checkLockContention();
        
        // Check for connection issues
        checkConnectionIssues();
    }
    
    // Check for slow queries
    private void checkSlowQueries() throws SQLException {
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
            LIMIT 5
            """;
        
        try (Statement stmt = connection.createStatement();
             ResultSet rs = stmt.executeQuery(sql)) {
            
            System.out.println("Slow Queries Analysis:");
            while (rs.next()) {
                System.out.println("Query Time: " + rs.getString("query_time"));
                System.out.println("Rows Examined: " + rs.getInt("rows_examined"));
                System.out.println("SQL: " + rs.getString("sql_text"));
                System.out.println("---");
            }
        }
    }
    
    // Check for missing indexes
    private void checkMissingIndexes() throws SQLException {
        String sql = """
            SELECT 
                table_name,
                column_name,
                cardinality
            FROM information_schema.statistics
            WHERE table_schema = DATABASE()
            AND cardinality = 0
            """;
        
        try (Statement stmt = connection.createStatement();
             ResultSet rs = stmt.executeQuery(sql)) {
            
            System.out.println("Missing Indexes Analysis:");
            while (rs.next()) {
                System.out.println("Table: " + rs.getString("table_name"));
                System.out.println("Column: " + rs.getString("column_name"));
                System.out.println("Cardinality: " + rs.getLong("cardinality"));
                System.out.println("---");
            }
        }
    }
    
    // Check for resource constraints
    private void checkResourceConstraints() throws SQLException {
        // Check CPU usage
        String sql = "SHOW STATUS LIKE 'Cpu_usage'";
        try (Statement stmt = connection.createStatement();
             ResultSet rs = stmt.executeQuery(sql)) {
            if (rs.next()) {
                String cpuUsage = rs.getString("Value");
                System.out.println("CPU Usage: " + cpuUsage);
            }
        }
        
        // Check memory usage
        sql = "SHOW STATUS LIKE 'Innodb_buffer_pool_pages_data'";
        try (Statement stmt = connection.createStatement();
             ResultSet rs = stmt.executeQuery(sql)) {
            if (rs.next()) {
                long dataPages = rs.getLong("Value");
                System.out.println("Buffer Pool Data Pages: " + dataPages);
            }
        }
    }
    
    // Check for lock contention
    private void checkLockContention() throws SQLException {
        String sql = """
            SELECT 
                COUNT(*) as lock_waits
            FROM information_schema.INNODB_LOCKS
            """;
        
        try (Statement stmt = connection.createStatement();
             ResultSet rs = stmt.executeQuery(sql)) {
            if (rs.next()) {
                long lockWaits = rs.getLong("lock_waits");
                if (lockWaits > 0) {
                    System.out.println("WARNING: Lock contention detected: " + lockWaits + " locks");
                } else {
                    System.out.println("No lock contention detected");
                }
            }
        }
    }
    
    // Check for connection issues
    private void checkConnectionIssues() throws SQLException {
        String sql = "SHOW STATUS LIKE 'Threads_connected'";
        try (Statement stmt = connection.createStatement();
             ResultSet rs = stmt.executeQuery(sql)) {
            if (rs.next()) {
                int connections = rs.getInt("Value");
                System.out.println("Active Connections: " + connections);
                
                if (connections > 80) {
                    System.out.println("WARNING: High connection count detected");
                }
            }
        }
    }
    
    // Provide optimization recommendations
    public void provideOptimizationRecommendations() {
        System.out.println("=== Optimization Recommendations ===");
        System.out.println("1. Add indexes on frequently queried columns");
        System.out.println("2. Optimize slow queries using EXPLAIN");
        System.out.println("3. Consider partitioning large tables");
        System.out.println("4. Increase buffer pool size if memory allows");
        System.out.println("5. Use connection pooling to manage connections");
        System.out.println("6. Consider read replicas for read-heavy workloads");
        System.out.println("7. Monitor and tune query cache settings");
        System.out.println("8. Regular maintenance and statistics updates");
        System.out.println("=====================================");
    }
}
```