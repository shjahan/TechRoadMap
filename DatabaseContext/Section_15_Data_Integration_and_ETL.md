# Section 15 – Data Integration and ETL

## 15.1 Extract, Transform, Load (ETL)

ETL is a data integration process that extracts data from source systems, transforms it into a usable format, and loads it into a target database.

### ETL Components:
- **Extract**: Pull data from source systems
- **Transform**: Clean, validate, and format data
- **Load**: Insert data into target database
- **Scheduling**: Automate ETL processes
- **Monitoring**: Track ETL job status and performance

### Real-World Analogy:
ETL is like moving and organizing a library:
- **Extract** = Packing books from old library
- **Transform** = Sorting and cataloging books
- **Load** = Placing books in new library
- **Scheduling** = Moving schedule
- **Monitoring** = Tracking progress

### Java Example - ETL Process:
```java
import java.sql.*;
import java.util.List;
import java.util.ArrayList;

public class ETLProcess {
    private Connection sourceConnection;
    private Connection targetConnection;
    
    public ETLProcess(Connection sourceConnection, Connection targetConnection) {
        this.sourceConnection = sourceConnection;
        this.targetConnection = targetConnection;
    }
    
    // Extract data from source
    public List<StudentData> extractData() throws SQLException {
        List<StudentData> students = new ArrayList<>();
        String sql = "SELECT * FROM students WHERE updated_at > ?";
        
        try (PreparedStatement stmt = sourceConnection.prepareStatement(sql)) {
            stmt.setTimestamp(1, getLastExtractTime());
            
            try (ResultSet rs = stmt.executeQuery()) {
                while (rs.next()) {
                    StudentData student = new StudentData();
                    student.id = rs.getInt("id");
                    student.name = rs.getString("name");
                    student.email = rs.getString("email");
                    student.gpa = rs.getDouble("gpa");
                    student.updatedAt = rs.getTimestamp("updated_at");
                    students.add(student);
                }
            }
        }
        
        System.out.println("Extracted " + students.size() + " records");
        return students;
    }
    
    // Transform data
    public List<StudentData> transformData(List<StudentData> students) {
        List<StudentData> transformedStudents = new ArrayList<>();
        
        for (StudentData student : students) {
            // Clean and validate data
            if (isValidStudent(student)) {
                // Transform data
                student.name = student.name.trim().toUpperCase();
                student.email = student.email.toLowerCase();
                student.gpa = Math.round(student.gpa * 100.0) / 100.0; // Round to 2 decimal places
                
                transformedStudents.add(student);
            }
        }
        
        System.out.println("Transformed " + transformedStudents.size() + " records");
        return transformedStudents;
    }
    
    // Load data into target
    public void loadData(List<StudentData> students) throws SQLException {
        String sql = """
            INSERT INTO students (id, name, email, gpa, updated_at)
            VALUES (?, ?, ?, ?, ?)
            ON DUPLICATE KEY UPDATE
                name = VALUES(name),
                email = VALUES(email),
                gpa = VALUES(gpa),
                updated_at = VALUES(updated_at)
            """;
        
        try (PreparedStatement stmt = targetConnection.prepareStatement(sql)) {
            for (StudentData student : students) {
                stmt.setInt(1, student.id);
                stmt.setString(2, student.name);
                stmt.setString(3, student.email);
                stmt.setDouble(4, student.gpa);
                stmt.setTimestamp(5, student.updatedAt);
                stmt.addBatch();
            }
            
            int[] results = stmt.executeBatch();
            System.out.println("Loaded " + results.length + " records");
        }
    }
    
    // Complete ETL process
    public void runETL() throws SQLException {
        System.out.println("Starting ETL process...");
        
        // Extract
        List<StudentData> students = extractData();
        
        // Transform
        List<StudentData> transformedStudents = transformData(students);
        
        // Load
        loadData(transformedStudents);
        
        System.out.println("ETL process completed");
    }
    
    private boolean isValidStudent(StudentData student) {
        return student.name != null && !student.name.trim().isEmpty() &&
               student.email != null && student.email.contains("@") &&
               student.gpa >= 0.0 && student.gpa <= 4.0;
    }
    
    private Timestamp getLastExtractTime() {
        // Return timestamp of last successful extract
        return Timestamp.valueOf("2024-01-01 00:00:00");
    }
    
    // Student data class
    private static class StudentData {
        int id;
        String name;
        String email;
        double gpa;
        Timestamp updatedAt;
    }
}
```

## 15.2 Extract, Load, Transform (ELT)

ELT is a data integration approach that loads raw data into the target system first, then transforms it using the target system's processing power.

### ELT Benefits:
- **Faster Loading**: No transformation during extraction
- **Scalability**: Leverage target system's processing power
- **Flexibility**: Transform data as needed
- **Cost Efficiency**: Reduce processing on source systems
- **Real-time Processing**: Process data as it arrives

### Real-World Analogy:
ELT is like moving everything to a new house first, then organizing:
- **Extract** = Pack everything quickly
- **Load** = Move everything to new house
- **Transform** = Organize and arrange in new house
- **Benefits** = Faster moving, more space to organize

### Java Example - ELT Process:
```java
public class ELTProcess {
    private Connection sourceConnection;
    private Connection targetConnection;
    
    public ELTProcess(Connection sourceConnection, Connection targetConnection) {
        this.sourceConnection = sourceConnection;
        this.targetConnection = targetConnection;
    }
    
    // Extract and load raw data
    public void extractAndLoad() throws SQLException {
        String sql = "SELECT * FROM students";
        
        try (Statement stmt = sourceConnection.createStatement();
             ResultSet rs = stmt.executeQuery(sql)) {
            
            String insertSql = "INSERT INTO raw_students (id, name, email, gpa, updated_at) VALUES (?, ?, ?, ?, ?)";
            try (PreparedStatement insertStmt = targetConnection.prepareStatement(insertSql)) {
                while (rs.next()) {
                    insertStmt.setInt(1, rs.getInt("id"));
                    insertStmt.setString(2, rs.getString("name"));
                    insertStmt.setString(3, rs.getString("email"));
                    insertStmt.setDouble(4, rs.getDouble("gpa"));
                    insertStmt.setTimestamp(5, rs.getTimestamp("updated_at"));
                    insertStmt.addBatch();
                }
                insertStmt.executeBatch();
            }
        }
        
        System.out.println("Raw data extracted and loaded");
    }
    
    // Transform data in target system
    public void transformInTarget() throws SQLException {
        String sql = """
            INSERT INTO students (id, name, email, gpa, updated_at)
            SELECT 
                id,
                UPPER(TRIM(name)) as name,
                LOWER(email) as email,
                ROUND(gpa, 2) as gpa,
                updated_at
            FROM raw_students
            WHERE name IS NOT NULL 
            AND email LIKE '%@%'
            AND gpa >= 0.0 AND gpa <= 4.0
            """;
        
        try (Statement stmt = targetConnection.createStatement()) {
            int rowsAffected = stmt.executeUpdate(sql);
            System.out.println("Transformed " + rowsAffected + " records");
        }
    }
    
    // Complete ELT process
    public void runELT() throws SQLException {
        System.out.println("Starting ELT process...");
        
        // Extract and load
        extractAndLoad();
        
        // Transform
        transformInTarget();
        
        System.out.println("ELT process completed");
    }
}
```

## 15.3 Data Integration Patterns

Data integration patterns provide standardized approaches for connecting and synchronizing data between different systems.

### Common Patterns:
- **Batch Integration**: Process data in batches
- **Real-time Integration**: Process data as it arrives
- **Event-driven Integration**: Respond to data events
- **API Integration**: Use APIs for data exchange
- **Message Queue Integration**: Use message queues for data flow

### Real-World Analogy:
Data integration patterns are like different communication methods:
- **Batch Integration** = Daily mail delivery
- **Real-time Integration** = Instant messaging
- **Event-driven Integration** = Push notifications
- **API Integration** = Phone calls
- **Message Queue Integration** = Voicemail system

### Java Example - Data Integration Patterns:
```java
import java.util.concurrent.BlockingQueue;
import java.util.concurrent.LinkedBlockingQueue;

public class DataIntegrationPatterns {
    private BlockingQueue<DataEvent> messageQueue = new LinkedBlockingQueue<>();
    
    // Batch integration pattern
    public void batchIntegration() throws SQLException {
        System.out.println("Running batch integration...");
        
        // Process data in batches
        int batchSize = 1000;
        int offset = 0;
        
        while (true) {
            List<DataRecord> batch = getBatchData(offset, batchSize);
            if (batch.isEmpty()) {
                break;
            }
            
            processBatch(batch);
            offset += batchSize;
        }
        
        System.out.println("Batch integration completed");
    }
    
    // Real-time integration pattern
    public void realTimeIntegration() throws SQLException {
        System.out.println("Starting real-time integration...");
        
        // Process data as it arrives
        while (true) {
            DataRecord record = getNextRecord();
            if (record != null) {
                processRecord(record);
            } else {
                break;
            }
        }
        
        System.out.println("Real-time integration completed");
    }
    
    // Event-driven integration pattern
    public void eventDrivenIntegration() {
        System.out.println("Starting event-driven integration...");
        
        // Listen for events
        while (true) {
            try {
                DataEvent event = messageQueue.take();
                processEvent(event);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                break;
            }
        }
        
        System.out.println("Event-driven integration completed");
    }
    
    // API integration pattern
    public void apiIntegration() {
        System.out.println("Starting API integration...");
        
        // Call external API
        String apiUrl = "https://api.example.com/data";
        String response = callExternalAPI(apiUrl);
        
        if (response != null) {
            processAPIResponse(response);
        }
        
        System.out.println("API integration completed");
    }
    
    // Message queue integration pattern
    public void messageQueueIntegration() {
        System.out.println("Starting message queue integration...");
        
        // Send message to queue
        DataEvent event = new DataEvent("data_updated", "student_123");
        messageQueue.offer(event);
        
        // Process messages from queue
        while (!messageQueue.isEmpty()) {
            DataEvent queuedEvent = messageQueue.poll();
            if (queuedEvent != null) {
                processEvent(queuedEvent);
            }
        }
        
        System.out.println("Message queue integration completed");
    }
    
    private List<DataRecord> getBatchData(int offset, int batchSize) {
        // Implementation for getting batch data
        return new ArrayList<>();
    }
    
    private void processBatch(List<DataRecord> batch) {
        // Implementation for processing batch
        System.out.println("Processing batch of " + batch.size() + " records");
    }
    
    private DataRecord getNextRecord() {
        // Implementation for getting next record
        return null;
    }
    
    private void processRecord(DataRecord record) {
        // Implementation for processing record
        System.out.println("Processing record: " + record.getId());
    }
    
    private void processEvent(DataEvent event) {
        // Implementation for processing event
        System.out.println("Processing event: " + event.getType() + " - " + event.getData());
    }
    
    private String callExternalAPI(String apiUrl) {
        // Implementation for calling external API
        return "API response";
    }
    
    private void processAPIResponse(String response) {
        // Implementation for processing API response
        System.out.println("Processing API response: " + response);
    }
    
    // Data classes
    private static class DataRecord {
        private String id;
        private String data;
        
        public String getId() { return id; }
        public String getData() { return data; }
    }
    
    private static class DataEvent {
        private String type;
        private String data;
        
        public DataEvent(String type, String data) {
            this.type = type;
            this.data = data;
        }
        
        public String getType() { return type; }
        public String getData() { return data; }
    }
}
```

## 15.4 Real-time Data Processing

Real-time data processing handles data as it arrives, providing immediate insights and responses to data changes.

### Real-time Processing Components:
- **Stream Processing**: Process continuous data streams
- **Event Processing**: Handle real-time events
- **Complex Event Processing**: Analyze event patterns
- **Real-time Analytics**: Generate immediate insights
- **Alert Processing**: Trigger immediate responses

### Real-World Analogy:
Real-time data processing is like a live news broadcast:
- **Stream Processing** = Live video feed
- **Event Processing** = Breaking news alerts
- **Complex Event Processing** = Pattern analysis
- **Real-time Analytics** = Live statistics
- **Alert Processing** = Emergency notifications

### Java Example - Real-time Data Processing:
```java
import java.util.concurrent.BlockingQueue;
import java.util.concurrent.LinkedBlockingQueue;
import java.util.concurrent.Executors;
import java.util.concurrent.ExecutorService;

public class RealTimeDataProcessor {
    private BlockingQueue<DataEvent> eventQueue = new LinkedBlockingQueue<>();
    private ExecutorService executor = Executors.newFixedThreadPool(4);
    private boolean running = false;
    
    // Start real-time processing
    public void startProcessing() {
        running = true;
        executor.submit(this::processEvents);
        System.out.println("Real-time data processing started");
    }
    
    // Stop real-time processing
    public void stopProcessing() {
        running = false;
        executor.shutdown();
        System.out.println("Real-time data processing stopped");
    }
    
    // Process events in real-time
    private void processEvents() {
        while (running) {
            try {
                DataEvent event = eventQueue.take();
                processEvent(event);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                break;
            }
        }
    }
    
    // Add event to queue
    public void addEvent(DataEvent event) {
        eventQueue.offer(event);
    }
    
    // Process individual event
    private void processEvent(DataEvent event) {
        System.out.println("Processing event: " + event.getType() + " - " + event.getData());
        
        switch (event.getType()) {
            case "student_enrolled":
                handleStudentEnrolled(event);
                break;
            case "grade_updated":
                handleGradeUpdated(event);
                break;
            case "payment_received":
                handlePaymentReceived(event);
                break;
            default:
                System.out.println("Unknown event type: " + event.getType());
        }
    }
    
    // Handle student enrollment event
    private void handleStudentEnrolled(DataEvent event) {
        System.out.println("Student enrolled: " + event.getData());
        // Send welcome email, update statistics, etc.
    }
    
    // Handle grade update event
    private void handleGradeUpdated(DataEvent event) {
        System.out.println("Grade updated: " + event.getData());
        // Update GPA, check for honors, etc.
    }
    
    // Handle payment received event
    private void handlePaymentReceived(DataEvent event) {
        System.out.println("Payment received: " + event.getData());
        // Update account balance, send receipt, etc.
    }
    
    // Data event class
    private static class DataEvent {
        private String type;
        private String data;
        private long timestamp;
        
        public DataEvent(String type, String data) {
            this.type = type;
            this.data = data;
            this.timestamp = System.currentTimeMillis();
        }
        
        public String getType() { return type; }
        public String getData() { return data; }
        public long getTimestamp() { return timestamp; }
    }
}
```

## 15.5 Batch Processing

Batch processing handles large volumes of data in scheduled batches, typically during off-peak hours.

### Batch Processing Characteristics:
- **Scheduled Execution**: Run at specific times
- **Large Volumes**: Process many records at once
- **Off-peak Hours**: Minimize impact on system performance
- **Error Handling**: Robust error recovery
- **Monitoring**: Track batch job status

### Real-World Analogy:
Batch processing is like overnight package sorting:
- **Scheduled Execution** = Night shift work
- **Large Volumes** = Thousands of packages
- **Off-peak Hours** = When system is less busy
- **Error Handling** = Handling damaged packages
- **Monitoring** = Tracking sorting progress

### Java Example - Batch Processing:
```java
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;

public class BatchProcessor {
    private Connection connection;
    private ScheduledExecutorService scheduler;
    
    public BatchProcessor(Connection connection) {
        this.connection = connection;
        this.scheduler = Executors.newScheduledThreadPool(2);
    }
    
    // Schedule batch jobs
    public void scheduleBatchJobs() {
        // Daily student data sync at 2 AM
        scheduler.scheduleAtFixedRate(this::syncStudentData, 0, 24, TimeUnit.HOURS);
        
        // Weekly report generation on Sundays at 3 AM
        scheduler.scheduleAtFixedRate(this::generateWeeklyReport, 0, 7, TimeUnit.DAYS);
        
        // Monthly data cleanup on 1st at 4 AM
        scheduler.scheduleAtFixedRate(this::cleanupOldData, 0, 30, TimeUnit.DAYS);
        
        System.out.println("Batch jobs scheduled");
    }
    
    // Sync student data
    private void syncStudentData() {
        try {
            System.out.println("Starting student data sync...");
            
            // Extract data from source
            List<StudentData> students = extractStudentData();
            
            // Transform data
            List<StudentData> transformedStudents = transformStudentData(students);
            
            // Load data
            loadStudentData(transformedStudents);
            
            System.out.println("Student data sync completed");
            
        } catch (Exception e) {
            System.err.println("Error in student data sync: " + e.getMessage());
        }
    }
    
    // Generate weekly report
    private void generateWeeklyReport() {
        try {
            System.out.println("Generating weekly report...");
            
            // Generate report data
            String reportData = generateReportData();
            
            // Save report
            saveReport("weekly_report_" + System.currentTimeMillis() + ".csv", reportData);
            
            System.out.println("Weekly report generated");
            
        } catch (Exception e) {
            System.err.println("Error generating weekly report: " + e.getMessage());
        }
    }
    
    // Cleanup old data
    private void cleanupOldData() {
        try {
            System.out.println("Starting data cleanup...");
            
            // Delete old log entries
            String sql = "DELETE FROM log_entries WHERE created_at < DATE_SUB(NOW(), INTERVAL 90 DAY)";
            try (Statement stmt = connection.createStatement()) {
                int deletedRows = stmt.executeUpdate(sql);
                System.out.println("Deleted " + deletedRows + " old log entries");
            }
            
            // Archive old student records
            archiveOldStudentRecords();
            
            System.out.println("Data cleanup completed");
            
        } catch (Exception e) {
            System.err.println("Error in data cleanup: " + e.getMessage());
        }
    }
    
    private List<StudentData> extractStudentData() {
        // Implementation for extracting student data
        return new ArrayList<>();
    }
    
    private List<StudentData> transformStudentData(List<StudentData> students) {
        // Implementation for transforming student data
        return students;
    }
    
    private void loadStudentData(List<StudentData> students) {
        // Implementation for loading student data
        System.out.println("Loaded " + students.size() + " student records");
    }
    
    private String generateReportData() {
        // Implementation for generating report data
        return "Report data";
    }
    
    private void saveReport(String filename, String data) {
        // Implementation for saving report
        System.out.println("Report saved: " + filename);
    }
    
    private void archiveOldStudentRecords() {
        // Implementation for archiving old records
        System.out.println("Old student records archived");
    }
    
    // Student data class
    private static class StudentData {
        int id;
        String name;
        String email;
        double gpa;
    }
}
```

## 15.6 Data Pipeline Design

Data pipeline design involves creating efficient, scalable, and maintainable data processing workflows.

### Pipeline Design Principles:
- **Modularity**: Break pipeline into reusable components
- **Scalability**: Handle increasing data volumes
- **Reliability**: Ensure data integrity and error handling
- **Monitoring**: Track pipeline performance and health
- **Maintainability**: Easy to update and modify

### Real-World Analogy:
Data pipeline design is like designing a factory assembly line:
- **Modularity** = Separate work stations
- **Scalability** = Add more stations as needed
- **Reliability** = Quality control at each station
- **Monitoring** = Production tracking
- **Maintainability** = Easy to modify stations

### Java Example - Data Pipeline Design:
```java
import java.util.concurrent.BlockingQueue;
import java.util.concurrent.LinkedBlockingQueue;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class DataPipeline {
    private BlockingQueue<DataRecord> inputQueue = new LinkedBlockingQueue<>();
    private BlockingQueue<DataRecord> outputQueue = new LinkedBlockingQueue<>();
    private ExecutorService executor = Executors.newFixedThreadPool(4);
    private boolean running = false;
    
    // Start pipeline
    public void startPipeline() {
        running = true;
        
        // Start processing stages
        executor.submit(this::extractStage);
        executor.submit(this::transformStage);
        executor.submit(this::loadStage);
        executor.submit(this::monitorStage);
        
        System.out.println("Data pipeline started");
    }
    
    // Stop pipeline
    public void stopPipeline() {
        running = false;
        executor.shutdown();
        System.out.println("Data pipeline stopped");
    }
    
    // Extract stage
    private void extractStage() {
        while (running) {
            try {
                DataRecord record = getNextRecord();
                if (record != null) {
                    inputQueue.offer(record);
                } else {
                    Thread.sleep(1000); // Wait for more data
                }
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                break;
            }
        }
    }
    
    // Transform stage
    private void transformStage() {
        while (running) {
            try {
                DataRecord record = inputQueue.take();
                DataRecord transformedRecord = transformRecord(record);
                outputQueue.offer(transformedRecord);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                break;
            }
        }
    }
    
    // Load stage
    private void loadStage() {
        while (running) {
            try {
                DataRecord record = outputQueue.take();
                loadRecord(record);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                break;
            }
        }
    }
    
    // Monitor stage
    private void monitorStage() {
        while (running) {
            try {
                Thread.sleep(5000); // Check every 5 seconds
                printPipelineStatus();
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                break;
            }
        }
    }
    
    private DataRecord getNextRecord() {
        // Implementation for getting next record
        return null;
    }
    
    private DataRecord transformRecord(DataRecord record) {
        // Implementation for transforming record
        return record;
    }
    
    private void loadRecord(DataRecord record) {
        // Implementation for loading record
        System.out.println("Loaded record: " + record.getId());
    }
    
    private void printPipelineStatus() {
        System.out.println("Pipeline Status:");
        System.out.println("Input Queue Size: " + inputQueue.size());
        System.out.println("Output Queue Size: " + outputQueue.size());
    }
    
    // Data record class
    private static class DataRecord {
        private String id;
        private String data;
        
        public String getId() { return id; }
        public String getData() { return data; }
    }
}
```

## 15.7 Data Quality Management

Data quality management ensures data accuracy, completeness, consistency, and reliability throughout the data lifecycle.

### Data Quality Dimensions:
- **Accuracy**: Data is correct and free from errors
- **Completeness**: All required data is present
- **Consistency**: Data is consistent across systems
- **Timeliness**: Data is current and up-to-date
- **Validity**: Data conforms to defined rules

### Real-World Analogy:
Data quality management is like quality control in manufacturing:
- **Accuracy** = Products meet specifications
- **Completeness** = All parts are included
- **Consistency** = Same quality across all products
- **Timeliness** = Products delivered on time
- **Validity** = Products meet standards

### Java Example - Data Quality Management:
```java
public class DataQualityManager {
    private Connection connection;
    
    public DataQualityManager(Connection connection) {
        this.connection = connection;
    }
    
    // Validate data quality
    public DataQualityReport validateDataQuality() {
        DataQualityReport report = new DataQualityReport();
        
        // Check accuracy
        report.accuracyScore = checkAccuracy();
        
        // Check completeness
        report.completenessScore = checkCompleteness();
        
        // Check consistency
        report.consistencyScore = checkConsistency();
        
        // Check timeliness
        report.timelinessScore = checkTimeliness();
        
        // Check validity
        report.validityScore = checkValidity();
        
        // Calculate overall score
        report.overallScore = calculateOverallScore(report);
        
        return report;
    }
    
    // Check data accuracy
    private double checkAccuracy() {
        try {
            String sql = """
                SELECT 
                    COUNT(*) as total_records,
                    SUM(CASE WHEN email LIKE '%@%' THEN 1 ELSE 0 END) as valid_emails,
                    SUM(CASE WHEN gpa >= 0.0 AND gpa <= 4.0 THEN 1 ELSE 0 END) as valid_gpas
                FROM students
                """;
            
            try (Statement stmt = connection.createStatement();
                 ResultSet rs = stmt.executeQuery(sql)) {
                if (rs.next()) {
                    int totalRecords = rs.getInt("total_records");
                    int validEmails = rs.getInt("valid_emails");
                    int validGpas = rs.getInt("valid_gpas");
                    
                    double emailAccuracy = (double) validEmails / totalRecords;
                    double gpaAccuracy = (double) validGpas / totalRecords;
                    
                    return (emailAccuracy + gpaAccuracy) / 2;
                }
            }
        } catch (SQLException e) {
            System.err.println("Error checking accuracy: " + e.getMessage());
        }
        
        return 0.0;
    }
    
    // Check data completeness
    private double checkCompleteness() {
        try {
            String sql = """
                SELECT 
                    COUNT(*) as total_records,
                    SUM(CASE WHEN name IS NOT NULL AND name != '' THEN 1 ELSE 0 END) as complete_names,
                    SUM(CASE WHEN email IS NOT NULL AND email != '' THEN 1 ELSE 0 END) as complete_emails,
                    SUM(CASE WHEN gpa IS NOT NULL THEN 1 ELSE 0 END) as complete_gpas
                FROM students
                """;
            
            try (Statement stmt = connection.createStatement();
                 ResultSet rs = stmt.executeQuery(sql)) {
                if (rs.next()) {
                    int totalRecords = rs.getInt("total_records");
                    int completeNames = rs.getInt("complete_names");
                    int completeEmails = rs.getInt("complete_emails");
                    int completeGpas = rs.getInt("complete_gpas");
                    
                    double nameCompleteness = (double) completeNames / totalRecords;
                    double emailCompleteness = (double) completeEmails / totalRecords;
                    double gpaCompleteness = (double) completeGpas / totalRecords;
                    
                    return (nameCompleteness + emailCompleteness + gpaCompleteness) / 3;
                }
            }
        } catch (SQLException e) {
            System.err.println("Error checking completeness: " + e.getMessage());
        }
        
        return 0.0;
    }
    
    // Check data consistency
    private double checkConsistency() {
        try {
            String sql = """
                SELECT 
                    COUNT(DISTINCT LENGTH(name)) as name_length_variations,
                    COUNT(DISTINCT SUBSTRING(email, LOCATE('@', email) + 1)) as email_domains
                FROM students
                WHERE name IS NOT NULL AND email IS NOT NULL
                """;
            
            try (Statement stmt = connection.createStatement();
                 ResultSet rs = stmt.executeQuery(sql)) {
                if (rs.next()) {
                    int nameLengthVariations = rs.getInt("name_length_variations");
                    int emailDomains = rs.getInt("email_domains");
                    
                    // Lower variation indicates higher consistency
                    double nameConsistency = Math.max(0, 1.0 - (nameLengthVariations / 10.0));
                    double emailConsistency = Math.max(0, 1.0 - (emailDomains / 5.0));
                    
                    return (nameConsistency + emailConsistency) / 2;
                }
            }
        } catch (SQLException e) {
            System.err.println("Error checking consistency: " + e.getMessage());
        }
        
        return 0.0;
    }
    
    // Check data timeliness
    private double checkTimeliness() {
        try {
            String sql = """
                SELECT 
                    COUNT(*) as total_records,
                    SUM(CASE WHEN updated_at > DATE_SUB(NOW(), INTERVAL 7 DAY) THEN 1 ELSE 0 END) as recent_updates
                FROM students
                """;
            
            try (Statement stmt = connection.createStatement();
                 ResultSet rs = stmt.executeQuery(sql)) {
                if (rs.next()) {
                    int totalRecords = rs.getInt("total_records");
                    int recentUpdates = rs.getInt("recent_updates");
                    
                    return (double) recentUpdates / totalRecords;
                }
            }
        } catch (SQLException e) {
            System.err.println("Error checking timeliness: " + e.getMessage());
        }
        
        return 0.0;
    }
    
    // Check data validity
    private double checkValidity() {
        try {
            String sql = """
                SELECT 
                    COUNT(*) as total_records,
                    SUM(CASE WHEN name REGEXP '^[A-Za-z ]+$' THEN 1 ELSE 0 END) as valid_names,
                    SUM(CASE WHEN email REGEXP '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$' THEN 1 ELSE 0 END) as valid_emails
                FROM students
                """;
            
            try (Statement stmt = connection.createStatement();
                 ResultSet rs = stmt.executeQuery(sql)) {
                if (rs.next()) {
                    int totalRecords = rs.getInt("total_records");
                    int validNames = rs.getInt("valid_names");
                    int validEmails = rs.getInt("valid_emails");
                    
                    double nameValidity = (double) validNames / totalRecords;
                    double emailValidity = (double) validEmails / totalRecords;
                    
                    return (nameValidity + emailValidity) / 2;
                }
            }
        } catch (SQLException e) {
            System.err.println("Error checking validity: " + e.getMessage());
        }
        
        return 0.0;
    }
    
    private double calculateOverallScore(DataQualityReport report) {
        return (report.accuracyScore + report.completenessScore + 
                report.consistencyScore + report.timelinessScore + 
                report.validityScore) / 5;
    }
    
    // Data quality report class
    private static class DataQualityReport {
        double accuracyScore = 0.0;
        double completenessScore = 0.0;
        double consistencyScore = 0.0;
        double timelinessScore = 0.0;
        double validityScore = 0.0;
        double overallScore = 0.0;
        
        public void printReport() {
            System.out.println("=== Data Quality Report ===");
            System.out.println("Accuracy Score: " + String.format("%.2f", accuracyScore));
            System.out.println("Completeness Score: " + String.format("%.2f", completenessScore));
            System.out.println("Consistency Score: " + String.format("%.2f", consistencyScore));
            System.out.println("Timeliness Score: " + String.format("%.2f", timelinessScore));
            System.out.println("Validity Score: " + String.format("%.2f", validityScore));
            System.out.println("Overall Score: " + String.format("%.2f", overallScore));
            System.out.println("==========================");
        }
    }
}
```

## 15.8 Data Lineage and Governance

Data lineage tracks the flow of data from source to destination, while data governance ensures proper data management and compliance.

### Data Lineage Components:
- **Source Systems**: Where data originates
- **Transformations**: How data is modified
- **Dependencies**: Data relationships and dependencies
- **Impact Analysis**: Effect of changes on downstream systems
- **Audit Trail**: Complete history of data changes

### Data Governance Components:
- **Data Policies**: Rules and guidelines for data usage
- **Data Ownership**: Who is responsible for data
- **Data Classification**: Categorizing data by sensitivity
- **Access Control**: Who can access what data
- **Compliance**: Meeting regulatory requirements

### Real-World Analogy:
Data lineage and governance are like tracking a package:
- **Source Systems** = Where package is sent from
- **Transformations** = How package is handled
- **Dependencies** = What the package depends on
- **Impact Analysis** = What happens if package is delayed
- **Audit Trail** = Complete tracking history

### Java Example - Data Lineage and Governance:
```java
import java.util.Map;
import java.util.HashMap;
import java.util.List;
import java.util.ArrayList;

public class DataLineageAndGovernance {
    private Map<String, DataLineage> lineageMap = new HashMap<>();
    private Map<String, DataGovernance> governanceMap = new HashMap<>();
    
    // Track data lineage
    public void trackDataLineage(String dataId, String source, String transformation, String destination) {
        DataLineage lineage = new DataLineage();
        lineage.dataId = dataId;
        lineage.source = source;
        lineage.transformation = transformation;
        lineage.destination = destination;
        lineage.timestamp = System.currentTimeMillis();
        
        lineageMap.put(dataId, lineage);
        System.out.println("Data lineage tracked for: " + dataId);
    }
    
    // Get data lineage
    public DataLineage getDataLineage(String dataId) {
        return lineageMap.get(dataId);
    }
    
    // Analyze impact of changes
    public void analyzeImpact(String dataId) {
        DataLineage lineage = lineageMap.get(dataId);
        if (lineage != null) {
            System.out.println("Impact Analysis for: " + dataId);
            System.out.println("Source: " + lineage.source);
            System.out.println("Transformation: " + lineage.transformation);
            System.out.println("Destination: " + lineage.destination);
            System.out.println("Timestamp: " + new java.util.Date(lineage.timestamp));
        }
    }
    
    // Set data governance policies
    public void setDataGovernance(String dataId, String owner, String classification, String accessLevel) {
        DataGovernance governance = new DataGovernance();
        governance.dataId = dataId;
        governance.owner = owner;
        governance.classification = classification;
        governance.accessLevel = accessLevel;
        governance.timestamp = System.currentTimeMillis();
        
        governanceMap.put(dataId, governance);
        System.out.println("Data governance set for: " + dataId);
    }
    
    // Check data access permissions
    public boolean checkDataAccess(String dataId, String userId) {
        DataGovernance governance = governanceMap.get(dataId);
        if (governance != null) {
            // Check if user has access based on classification and access level
            return hasAccess(userId, governance.classification, governance.accessLevel);
        }
        return false;
    }
    
    // Audit data access
    public void auditDataAccess(String dataId, String userId, String action) {
        System.out.println("Data Access Audit:");
        System.out.println("Data ID: " + dataId);
        System.out.println("User: " + userId);
        System.out.println("Action: " + action);
        System.out.println("Timestamp: " + new java.util.Date());
    }
    
    private boolean hasAccess(String userId, String classification, String accessLevel) {
        // Implementation for checking access permissions
        return true; // Simplified for example
    }
    
    // Data lineage class
    private static class DataLineage {
        String dataId;
        String source;
        String transformation;
        String destination;
        long timestamp;
    }
    
    // Data governance class
    private static class DataGovernance {
        String dataId;
        String owner;
        String classification;
        String accessLevel;
        long timestamp;
    }
}
```