# Section 11 – NewSQL and Modern Databases

## 11.1 NewSQL Characteristics

NewSQL databases combine the benefits of traditional SQL databases with the scalability of NoSQL systems, providing ACID compliance with horizontal scaling.

### Key Characteristics:
- **ACID Compliance**: Full ACID transaction support
- **SQL Interface**: Standard SQL query language
- **Horizontal Scaling**: Distributed architecture
- **High Performance**: Optimized for modern workloads
- **Cloud-Native**: Designed for cloud environments

### Real-World Analogy:
NewSQL is like a modern hybrid vehicle:
- **ACID Compliance** = Reliable engine (traditional car reliability)
- **SQL Interface** = Familiar controls (standard driving experience)
- **Horizontal Scaling** = Electric motor (modern efficiency)
- **High Performance** = Hybrid power (best of both worlds)

### Java Example - NewSQL Database:
```java
import java.sql.*;
import java.util.Properties;

public class NewSQLExample {
    private Connection connection;
    
    public NewSQLExample() throws SQLException {
        // Connect to NewSQL database (e.g., CockroachDB)
        String url = "jdbc:postgresql://localhost:26257/university?sslmode=disable";
        Properties props = new Properties();
        props.setProperty("user", "root");
        props.setProperty("password", "");
        
        connection = DriverManager.getConnection(url, props);
    }
    
    // Create distributed table
    public void createDistributedTable() throws SQLException {
        String sql = """
            CREATE TABLE students (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                name STRING NOT NULL,
                email STRING UNIQUE NOT NULL,
                major STRING,
                gpa DECIMAL(3,2),
                created_at TIMESTAMP DEFAULT now()
            )
            """;
        
        try (Statement stmt = connection.createStatement()) {
            stmt.execute(sql);
            System.out.println("Distributed table created");
        }
    }
    
    // Insert data with ACID compliance
    public void insertStudentWithTransaction(String name, String email, String major, double gpa) throws SQLException {
        connection.setAutoCommit(false);
        
        try {
            String sql = "INSERT INTO students (name, email, major, gpa) VALUES (?, ?, ?, ?)";
            try (PreparedStatement stmt = connection.prepareStatement(sql)) {
                stmt.setString(1, name);
                stmt.setString(2, email);
                stmt.setString(3, major);
                stmt.setDouble(4, gpa);
                stmt.executeUpdate();
            }
            
            connection.commit();
            System.out.println("Student inserted with ACID compliance");
            
        } catch (SQLException e) {
            connection.rollback();
            System.err.println("Transaction failed: " + e.getMessage());
            throw e;
        } finally {
            connection.setAutoCommit(true);
        }
    }
    
    // Query with distributed execution
    public void queryDistributedData() throws SQLException {
        String sql = "SELECT name, email, major, gpa FROM students WHERE gpa > 3.5 ORDER BY gpa DESC";
        
        try (Statement stmt = connection.createStatement();
             ResultSet rs = stmt.executeQuery(sql)) {
            
            System.out.println("High-performing students:");
            while (rs.next()) {
                System.out.printf("Name: %s, Email: %s, Major: %s, GPA: %.2f%n",
                    rs.getString("name"),
                    rs.getString("email"),
                    rs.getString("major"),
                    rs.getDouble("gpa"));
            }
        }
    }
}
```

## 11.2 Distributed SQL Databases

Distributed SQL databases provide ACID compliance across multiple nodes while maintaining horizontal scalability and fault tolerance.

### Key Features:
- **Distributed Architecture**: Data spread across multiple nodes
- **Consensus Protocols**: Raft or Paxos for consistency
- **Automatic Sharding**: Transparent data distribution
- **Fault Tolerance**: Continues operating with node failures
- **Global Transactions**: Cross-node transaction support

### Real-World Analogy:
Distributed SQL is like a distributed library system:
- **Multiple Locations** = Different library branches
- **Consensus Protocols** = Coordinated catalog system
- **Automatic Sharding** = Books distributed by topic
- **Fault Tolerance** = System works even if some branches close
- **Global Transactions** = Check out books from any branch

### Java Example - Distributed SQL:
```java
public class DistributedSQLExample {
    private List<Connection> connections;
    
    public DistributedSQLExample(List<Connection> connections) {
        this.connections = connections;
    }
    
    // Execute distributed transaction
    public void executeDistributedTransaction() throws SQLException {
        // Start transaction on all nodes
        for (Connection conn : connections) {
            conn.setAutoCommit(false);
        }
        
        try {
            // Insert data on different nodes
            insertOnNode(connections.get(0), "Node 1 data");
            insertOnNode(connections.get(1), "Node 2 data");
            insertOnNode(connections.get(2), "Node 3 data");
            
            // Commit on all nodes
            for (Connection conn : connections) {
                conn.commit();
            }
            
            System.out.println("Distributed transaction completed");
            
        } catch (SQLException e) {
            // Rollback on all nodes
            for (Connection conn : connections) {
                conn.rollback();
            }
            throw e;
        } finally {
            // Restore auto-commit
            for (Connection conn : connections) {
                conn.setAutoCommit(true);
            }
        }
    }
    
    private void insertOnNode(Connection conn, String data) throws SQLException {
        String sql = "INSERT INTO distributed_table (data, node_id) VALUES (?, ?)";
        try (PreparedStatement stmt = conn.prepareStatement(sql)) {
            stmt.setString(1, data);
            stmt.setString(2, conn.getMetaData().getURL());
            stmt.executeUpdate();
        }
    }
    
    // Query across distributed nodes
    public void queryDistributedData() throws SQLException {
        for (int i = 0; i < connections.size(); i++) {
            Connection conn = connections.get(i);
            String sql = "SELECT * FROM distributed_table WHERE node_id = ?";
            
            try (PreparedStatement stmt = conn.prepareStatement(sql)) {
                stmt.setString(1, conn.getMetaData().getURL());
                
                try (ResultSet rs = stmt.executeQuery()) {
                    System.out.println("Data from node " + (i + 1) + ":");
                    while (rs.next()) {
                        System.out.println("- " + rs.getString("data"));
                    }
                }
            }
        }
    }
}
```

## 11.3 Cloud-Native Databases

Cloud-native databases are designed specifically for cloud environments, providing elasticity, managed services, and cloud integration.

### Key Features:
- **Elastic Scaling**: Automatic scaling based on demand
- **Managed Services**: Fully managed by cloud providers
- **Multi-Region**: Global distribution and replication
- **Pay-per-Use**: Cost based on actual usage
- **Cloud Integration**: Native integration with cloud services

### Real-World Analogy:
Cloud-native databases are like utility services:
- **Elastic Scaling** = Water pressure adjusts to demand
- **Managed Services** = Utility company maintains everything
- **Multi-Region** = Service available everywhere
- **Pay-per-Use** = Bill based on actual consumption
- **Cloud Integration** = Works with other utilities

### Java Example - Cloud-Native Database:
```java
import com.amazonaws.services.rds.AmazonRDS;
import com.amazonaws.services.rds.AmazonRDSClientBuilder;
import com.amazonaws.services.rds.model.*;

public class CloudNativeDatabase {
    private AmazonRDS rdsClient;
    
    public CloudNativeDatabase() {
        rdsClient = AmazonRDSClientBuilder.defaultClient();
    }
    
    // Create cloud database instance
    public void createCloudDatabaseInstance() {
        CreateDBInstanceRequest request = new CreateDBInstanceRequest()
            .withDBInstanceIdentifier("university-db")
            .withDBInstanceClass("db.t3.micro")
            .withEngine("mysql")
            .withMasterUsername("admin")
            .withMasterUserPassword("password123")
            .withAllocatedStorage(20)
            .withMultiAZ(false)
            .withPubliclyAccessible(true);
        
        try {
            DBInstance result = rdsClient.createDBInstance(request);
            System.out.println("Cloud database instance created: " + result.getDBInstanceIdentifier());
        } catch (AmazonRDSException e) {
            System.err.println("Error creating database instance: " + e.getMessage());
        }
    }
    
    // Scale database instance
    public void scaleDatabaseInstance(String instanceId, String newInstanceClass) {
        ModifyDBInstanceRequest request = new ModifyDBInstanceRequest()
            .withDBInstanceIdentifier(instanceId)
            .withDBInstanceClass(newInstanceClass)
            .withApplyImmediately(true);
        
        try {
            DBInstance result = rdsClient.modifyDBInstance(request);
            System.out.println("Database instance scaled to: " + result.getDBInstanceClass());
        } catch (AmazonRDSException e) {
            System.err.println("Error scaling database instance: " + e.getMessage());
        }
    }
    
    // Create read replica
    public void createReadReplica(String sourceInstanceId, String replicaId) {
        CreateDBInstanceReadReplicaRequest request = new CreateDBInstanceReadReplicaRequest()
            .withDBInstanceIdentifier(replicaId)
            .withSourceDBInstanceIdentifier(sourceInstanceId)
            .withDBInstanceClass("db.t3.micro");
        
        try {
            DBInstance result = rdsClient.createDBInstanceReadReplica(request);
            System.out.println("Read replica created: " + result.getDBInstanceIdentifier());
        } catch (AmazonRDSException e) {
            System.err.println("Error creating read replica: " + e.getMessage());
        }
    }
    
    // Monitor database performance
    public void monitorDatabasePerformance(String instanceId) {
        DescribeDBInstancesRequest request = new DescribeDBInstancesRequest()
            .withDBInstanceIdentifiers(instanceId);
        
        try {
            DescribeDBInstancesResult result = rdsClient.describeDBInstances(request);
            DBInstance instance = result.getDBInstances().get(0);
            
            System.out.println("Database Performance Metrics:");
            System.out.println("Instance Class: " + instance.getDBInstanceClass());
            System.out.println("Status: " + instance.getDBInstanceStatus());
            System.out.println("Multi-AZ: " + instance.getMultiAZ());
            System.out.println("Storage Type: " + instance.getStorageType());
            
        } catch (AmazonRDSException e) {
            System.err.println("Error monitoring database: " + e.getMessage());
        }
    }
}
```

## 11.4 Serverless Databases

Serverless databases automatically manage infrastructure, scaling, and maintenance, allowing developers to focus on application logic.

### Key Features:
- **Automatic Scaling**: Scales to zero when not in use
- **No Infrastructure Management**: Fully managed by provider
- **Pay-per-Request**: Cost based on actual usage
- **Instant Provisioning**: Immediate availability
- **Global Distribution**: Multi-region deployment

### Real-World Analogy:
Serverless databases are like on-demand services:
- **Automatic Scaling** = Service adjusts to demand automatically
- **No Infrastructure Management** = Provider handles everything
- **Pay-per-Request** = Pay only for what you use
- **Instant Provisioning** = Available immediately when needed
- **Global Distribution** = Service available worldwide

### Java Example - Serverless Database:
```java
import com.amazonaws.services.dynamodbv2.AmazonDynamoDB;
import com.amazonaws.services.dynamodbv2.AmazonDynamoDBClientBuilder;
import com.amazonaws.services.dynamodbv2.model.*;

public class ServerlessDatabaseExample {
    private AmazonDynamoDB dynamoDB;
    
    public ServerlessDatabaseExample() {
        dynamoDB = AmazonDynamoDBClientBuilder.defaultClient();
    }
    
    // Create serverless table
    public void createServerlessTable() {
        CreateTableRequest request = new CreateTableRequest()
            .withTableName("students")
            .withKeySchema(new KeySchemaElement("id", KeyType.HASH))
            .withAttributeDefinitions(new AttributeDefinition("id", ScalarAttributeType.S))
            .withBillingMode(BillingMode.PAY_PER_REQUEST);
        
        try {
            CreateTableResult result = dynamoDB.createTable(request);
            System.out.println("Serverless table created: " + result.getTableDescription().getTableName());
        } catch (ResourceInUseException e) {
            System.out.println("Table already exists");
        } catch (AmazonDynamoDBException e) {
            System.err.println("Error creating table: " + e.getMessage());
        }
    }
    
    // Insert item (automatically scales)
    public void insertItem(String id, String name, String email) {
        PutItemRequest request = new PutItemRequest()
            .withTableName("students")
            .withItem(Map.of(
                "id", new AttributeValue(id),
                "name", new AttributeValue(name),
                "email", new AttributeValue(email),
                "timestamp", new AttributeValue(String.valueOf(System.currentTimeMillis()))
            ));
        
        try {
            dynamoDB.putItem(request);
            System.out.println("Item inserted: " + name);
        } catch (AmazonDynamoDBException e) {
            System.err.println("Error inserting item: " + e.getMessage());
        }
    }
    
    // Query item (automatically scales)
    public void queryItem(String id) {
        GetItemRequest request = new GetItemRequest()
            .withTableName("students")
            .withKey(Map.of("id", new AttributeValue(id)));
        
        try {
            GetItemResult result = dynamoDB.getItem(request);
            if (result.getItem() != null) {
                System.out.println("Item found: " + result.getItem());
            } else {
                System.out.println("Item not found");
            }
        } catch (AmazonDynamoDBException e) {
            System.err.println("Error querying item: " + e.getMessage());
        }
    }
    
    // Scan table (automatically scales)
    public void scanTable() {
        ScanRequest request = new ScanRequest()
            .withTableName("students");
        
        try {
            ScanResult result = dynamoDB.scan(request);
            System.out.println("Table scan results:");
            for (Map<String, AttributeValue> item : result.getItems()) {
                System.out.println("- " + item);
            }
        } catch (AmazonDynamoDBException e) {
            System.err.println("Error scanning table: " + e.getMessage());
        }
    }
}
```

## 11.5 Multi-Model Databases

Multi-model databases support multiple data models within a single database system, providing flexibility for different use cases.

### Supported Models:
- **Document Model**: JSON/BSON documents
- **Key-Value Model**: Simple key-value pairs
- **Graph Model**: Nodes and edges
- **Column-Family Model**: Column-oriented storage
- **Relational Model**: Tables and relationships

### Real-World Analogy:
Multi-model databases are like Swiss Army knives:
- **Multiple Tools** = Different data models
- **Single Device** = One database system
- **Flexibility** = Choose the right tool for the job
- **Convenience** = Everything in one place

### Java Example - Multi-Model Database:
```java
public class MultiModelDatabase {
    private Connection connection;
    
    public MultiModelDatabase(Connection connection) {
        this.connection = connection;
    }
    
    // Document model operations
    public void documentOperations() throws SQLException {
        // Store JSON document
        String jsonDocument = """
            {
                "name": "John Doe",
                "email": "john@example.com",
                "address": {
                    "street": "123 Main St",
                    "city": "New York"
                }
            }
            """;
        
        String sql = "INSERT INTO documents (id, content) VALUES (?, ?)";
        try (PreparedStatement stmt = connection.prepareStatement(sql)) {
            stmt.setString(1, "doc1");
            stmt.setString(2, jsonDocument);
            stmt.executeUpdate();
        }
        
        // Query JSON document
        sql = "SELECT content FROM documents WHERE id = ?";
        try (PreparedStatement stmt = connection.prepareStatement(sql)) {
            stmt.setString(1, "doc1");
            try (ResultSet rs = stmt.executeQuery()) {
                if (rs.next()) {
                    System.out.println("Document: " + rs.getString("content"));
                }
            }
        }
    }
    
    // Key-value model operations
    public void keyValueOperations() throws SQLException {
        // Store key-value pair
        String sql = "INSERT INTO key_value (key, value) VALUES (?, ?)";
        try (PreparedStatement stmt = connection.prepareStatement(sql)) {
            stmt.setString(1, "user:123:name");
            stmt.setString(2, "John Doe");
            stmt.executeUpdate();
        }
        
        // Retrieve value
        sql = "SELECT value FROM key_value WHERE key = ?";
        try (PreparedStatement stmt = connection.prepareStatement(sql)) {
            stmt.setString(1, "user:123:name");
            try (ResultSet rs = stmt.executeQuery()) {
                if (rs.next()) {
                    System.out.println("Value: " + rs.getString("value"));
                }
            }
        }
    }
    
    // Graph model operations
    public void graphOperations() throws SQLException {
        // Create node
        String sql = "INSERT INTO nodes (id, label, properties) VALUES (?, ?, ?)";
        try (PreparedStatement stmt = connection.prepareStatement(sql)) {
            stmt.setString(1, "node1");
            stmt.setString(2, "Person");
            stmt.setString(3, "{\"name\": \"John\", \"age\": 30}");
            stmt.executeUpdate();
        }
        
        // Create relationship
        sql = "INSERT INTO edges (from_node, to_node, relationship, properties) VALUES (?, ?, ?, ?)";
        try (PreparedStatement stmt = connection.prepareStatement(sql)) {
            stmt.setString(1, "node1");
            stmt.setString(2, "node2");
            stmt.setString(3, "FRIENDS_WITH");
            stmt.setString(4, "{\"since\": \"2020\"}");
            stmt.executeUpdate();
        }
        
        // Query graph
        sql = "SELECT * FROM edges WHERE from_node = ?";
        try (PreparedStatement stmt = connection.prepareStatement(sql)) {
            stmt.setString(1, "node1");
            try (ResultSet rs = stmt.executeQuery()) {
                while (rs.next()) {
                    System.out.println("Relationship: " + rs.getString("relationship") + 
                                     " to " + rs.getString("to_node"));
                }
            }
        }
    }
}
```

## 11.6 In-Memory Databases

In-memory databases store data primarily in RAM, providing extremely fast access times for applications requiring high performance.

### Key Features:
- **RAM Storage**: Data stored in memory
- **High Performance**: Sub-millisecond response times
- **Volatile Storage**: Data lost on power failure
- **Persistence Options**: Optional disk persistence
- **Scalability**: Can be distributed across multiple nodes

### Real-World Analogy:
In-memory databases are like having everything in your immediate memory:
- **RAM Storage** = Everything in your head
- **High Performance** = Instant recall
- **Volatile Storage** = Forgot when you sleep
- **Persistence Options** = Writing things down
- **Scalability** = Multiple people remembering

### Java Example - In-Memory Database:
```java
import java.util.concurrent.ConcurrentHashMap;
import java.util.Map;
import java.util.List;
import java.util.ArrayList;

public class InMemoryDatabase {
    private Map<String, Object> dataStore = new ConcurrentHashMap<>();
    private Map<String, List<String>> indexes = new ConcurrentHashMap<>();
    
    // Store data in memory
    public void store(String key, Object value) {
        dataStore.put(key, value);
        System.out.println("Data stored in memory: " + key);
    }
    
    // Retrieve data from memory
    public Object retrieve(String key) {
        Object value = dataStore.get(key);
        if (value != null) {
            System.out.println("Data retrieved from memory: " + key);
        }
        return value;
    }
    
    // Create index for fast searching
    public void createIndex(String field, String key, Object value) {
        indexes.computeIfAbsent(field, k -> new ArrayList<>()).add(key);
        System.out.println("Index created for field: " + field);
    }
    
    // Search using index
    public List<String> searchByIndex(String field) {
        List<String> keys = indexes.get(field);
        if (keys != null) {
            System.out.println("Found " + keys.size() + " items in index: " + field);
        }
        return keys != null ? keys : new ArrayList<>();
    }
    
    // Batch operations for performance
    public void batchStore(Map<String, Object> batchData) {
        dataStore.putAll(batchData);
        System.out.println("Batch stored: " + batchData.size() + " items");
    }
    
    // Memory usage statistics
    public void printMemoryStats() {
        Runtime runtime = Runtime.getRuntime();
        long totalMemory = runtime.totalMemory();
        long freeMemory = runtime.freeMemory();
        long usedMemory = totalMemory - freeMemory;
        
        System.out.println("Memory Statistics:");
        System.out.println("Total Memory: " + totalMemory / 1024 / 1024 + " MB");
        System.out.println("Used Memory: " + usedMemory / 1024 / 1024 + " MB");
        System.out.println("Free Memory: " + freeMemory / 1024 / 1024 + " MB");
        System.out.println("Data Store Size: " + dataStore.size() + " items");
    }
    
    // Persist to disk (optional)
    public void persistToDisk(String filename) {
        try (ObjectOutputStream oos = new ObjectOutputStream(new FileOutputStream(filename))) {
            oos.writeObject(dataStore);
            System.out.println("Data persisted to disk: " + filename);
        } catch (IOException e) {
            System.err.println("Error persisting data: " + e.getMessage());
        }
    }
    
    // Load from disk
    public void loadFromDisk(String filename) {
        try (ObjectInputStream ois = new ObjectInputStream(new FileInputStream(filename))) {
            dataStore = (Map<String, Object>) ois.readObject();
            System.out.println("Data loaded from disk: " + filename);
        } catch (IOException | ClassNotFoundException e) {
            System.err.println("Error loading data: " + e.getMessage());
        }
    }
}
```

## 11.7 Edge Databases

Edge databases bring data processing closer to the source, reducing latency and improving performance for distributed applications.

### Key Features:
- **Geographic Distribution**: Deployed at edge locations
- **Low Latency**: Reduced network latency
- **Local Processing**: Data processed near the source
- **Offline Capability**: Works without internet connection
- **Data Synchronization**: Sync with central databases

### Real-World Analogy:
Edge databases are like local branch offices:
- **Geographic Distribution** = Offices in different cities
- **Low Latency** = Quick local service
- **Local Processing** = Handle local requests
- **Offline Capability** = Work even when headquarters is down
- **Data Synchronization** = Regular updates with headquarters

### Java Example - Edge Database:
```java
public class EdgeDatabase {
    private Connection localConnection;
    private Connection centralConnection;
    private String edgeLocation;
    
    public EdgeDatabase(Connection localConnection, Connection centralConnection, String edgeLocation) {
        this.localConnection = localConnection;
        this.centralConnection = centralConnection;
        this.edgeLocation = edgeLocation;
    }
    
    // Process data locally
    public void processLocally(String data) throws SQLException {
        String sql = "INSERT INTO local_data (data, location, timestamp) VALUES (?, ?, NOW())";
        
        try (PreparedStatement stmt = localConnection.prepareStatement(sql)) {
            stmt.setString(1, data);
            stmt.setString(2, edgeLocation);
            stmt.executeUpdate();
        }
        
        System.out.println("Data processed locally at: " + edgeLocation);
    }
    
    // Sync with central database
    public void syncWithCentral() throws SQLException {
        // Get local changes
        String sql = "SELECT * FROM local_data WHERE synced = false";
        
        try (Statement stmt = localConnection.createStatement();
             ResultSet rs = stmt.executeQuery(sql)) {
            
            while (rs.next()) {
                // Send to central database
                sendToCentral(rs.getString("data"), rs.getString("location"), rs.getTimestamp("timestamp"));
                
                // Mark as synced
                markAsSynced(rs.getInt("id"));
            }
        }
        
        System.out.println("Data synced with central database");
    }
    
    private void sendToCentral(String data, String location, Timestamp timestamp) throws SQLException {
        String sql = "INSERT INTO central_data (data, location, timestamp) VALUES (?, ?, ?)";
        
        try (PreparedStatement stmt = centralConnection.prepareStatement(sql)) {
            stmt.setString(1, data);
            stmt.setString(2, location);
            stmt.setTimestamp(3, timestamp);
            stmt.executeUpdate();
        }
    }
    
    private void markAsSynced(int id) throws SQLException {
        String sql = "UPDATE local_data SET synced = true WHERE id = ?";
        
        try (PreparedStatement stmt = localConnection.prepareStatement(sql)) {
            stmt.setInt(1, id);
            stmt.executeUpdate();
        }
    }
    
    // Handle offline mode
    public void handleOfflineMode() {
        System.out.println("Operating in offline mode at: " + edgeLocation);
        // Continue processing locally
        // Queue changes for later sync
    }
}
```

## 11.8 Database as a Service (DBaaS)

DBaaS provides fully managed database services in the cloud, eliminating the need for database administration and infrastructure management.

### Key Features:
- **Fully Managed**: Provider handles all administration
- **Automatic Scaling**: Scales based on demand
- **High Availability**: Built-in redundancy and failover
- **Security**: Managed security and compliance
- **Monitoring**: Built-in monitoring and alerting

### Real-World Analogy:
DBaaS is like having a personal assistant for your database:
- **Fully Managed** = Assistant handles everything
- **Automatic Scaling** = Assistant adjusts to your needs
- **High Availability** = Assistant is always available
- **Security** = Assistant protects your data
- **Monitoring** = Assistant keeps you informed

### Java Example - DBaaS Integration:
```java
public class DBaaSIntegration {
    private String dbEndpoint;
    private String apiKey;
    
    public DBaaSIntegration(String dbEndpoint, String apiKey) {
        this.dbEndpoint = dbEndpoint;
        this.apiKey = apiKey;
    }
    
    // Create database instance
    public void createDatabaseInstance(String instanceName, String instanceType) {
        // API call to create database instance
        System.out.println("Creating database instance: " + instanceName + " of type: " + instanceType);
        
        // Simulate API call
        try {
            Thread.sleep(1000); // Simulate API call delay
            System.out.println("Database instance created successfully");
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }
    
    // Scale database instance
    public void scaleDatabaseInstance(String instanceName, String newInstanceType) {
        System.out.println("Scaling database instance: " + instanceName + " to: " + newInstanceType);
        
        // Simulate scaling operation
        try {
            Thread.sleep(2000); // Simulate scaling delay
            System.out.println("Database instance scaled successfully");
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }
    
    // Get database metrics
    public void getDatabaseMetrics(String instanceName) {
        System.out.println("Database metrics for: " + instanceName);
        System.out.println("CPU Usage: 45%");
        System.out.println("Memory Usage: 67%");
        System.out.println("Storage Usage: 23%");
        System.out.println("Connections: 150/1000");
        System.out.println("Query Performance: Good");
    }
    
    // Create backup
    public void createBackup(String instanceName, String backupName) {
        System.out.println("Creating backup: " + backupName + " for instance: " + instanceName);
        
        // Simulate backup creation
        try {
            Thread.sleep(3000); // Simulate backup delay
            System.out.println("Backup created successfully");
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }
    
    // Restore from backup
    public void restoreFromBackup(String instanceName, String backupName) {
        System.out.println("Restoring from backup: " + backupName + " to instance: " + instanceName);
        
        // Simulate restore operation
        try {
            Thread.sleep(5000); // Simulate restore delay
            System.out.println("Restore completed successfully");
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }
}
```