# Section 12 – Database Scaling Strategies

## 12.1 Vertical Scaling (Scale Up)

Vertical scaling involves increasing the capacity of a single server by adding more CPU, memory, storage, or other resources to handle increased load.

### Vertical Scaling Components:
- **CPU**: More processing cores and higher clock speeds
- **Memory**: Increased RAM for better caching
- **Storage**: Faster and larger storage devices
- **Network**: Higher bandwidth network interfaces
- **I/O**: Improved input/output performance

### Real-World Analogy:
Vertical scaling is like upgrading a single computer:
- **CPU** = Faster processor
- **Memory** = More RAM
- **Storage** = Larger, faster hard drive
- **Network** = Faster internet connection
- **I/O** = Better peripherals

### Java Example - Vertical Scaling:
```java
public class VerticalScalingExample {
    private Connection connection;
    
    public VerticalScalingExample(Connection connection) {
        this.connection = connection;
    }
    
    // Monitor system resources
    public void monitorSystemResources() {
        Runtime runtime = Runtime.getRuntime();
        
        System.out.println("System Resource Monitoring:");
        System.out.println("Available Processors: " + runtime.availableProcessors());
        System.out.println("Total Memory: " + runtime.totalMemory() / 1024 / 1024 + " MB");
        System.out.println("Free Memory: " + runtime.freeMemory() / 1024 / 1024 + " MB");
        System.out.println("Used Memory: " + (runtime.totalMemory() - runtime.freeMemory()) / 1024 / 1024 + " MB");
        System.out.println("Max Memory: " + runtime.maxMemory() / 1024 / 1024 + " MB");
    }
    
    // Optimize for vertical scaling
    public void optimizeForVerticalScaling() throws SQLException {
        // Increase connection pool size
        String sql = "SET GLOBAL max_connections = 1000";
        try (Statement stmt = connection.createStatement()) {
            stmt.execute(sql);
        }
        
        // Increase buffer pool size
        sql = "SET GLOBAL innodb_buffer_pool_size = 2G";
        try (Statement stmt = connection.createStatement()) {
            stmt.execute(sql);
        }
        
        // Increase query cache size
        sql = "SET GLOBAL query_cache_size = 256M";
        try (Statement stmt = connection.createStatement()) {
            stmt.execute(sql);
        }
        
        System.out.println("Database optimized for vertical scaling");
    }
    
    // Test performance with increased resources
    public void testPerformance() throws SQLException {
        long startTime = System.currentTimeMillis();
        
        // Execute complex query
        String sql = """
            SELECT s.name, s.email, c.course_name, e.grade
            FROM students s
            JOIN enrollments e ON s.id = e.student_id
            JOIN courses c ON e.course_id = c.id
            WHERE s.gpa > 3.5
            ORDER BY s.gpa DESC
            """;
        
        try (Statement stmt = connection.createStatement();
             ResultSet rs = stmt.executeQuery(sql)) {
            
            int rowCount = 0;
            while (rs.next()) {
                rowCount++;
            }
            
            long endTime = System.currentTimeMillis();
            System.out.println("Query executed in " + (endTime - startTime) + "ms");
            System.out.println("Rows returned: " + rowCount);
        }
    }
}
```

## 12.2 Horizontal Scaling (Scale Out)

Horizontal scaling involves adding more servers to distribute the load across multiple machines, providing better scalability and fault tolerance.

### Horizontal Scaling Components:
- **Load Balancer**: Distributes requests across servers
- **Multiple Servers**: Several database instances
- **Data Distribution**: Data spread across servers
- **Synchronization**: Keep data consistent across servers
- **Failover**: Automatic switching when servers fail

### Real-World Analogy:
Horizontal scaling is like adding more cashiers to a store:
- **Load Balancer** = Store manager directing customers
- **Multiple Servers** = Additional cashiers
- **Data Distribution** = Each cashier handles different products
- **Synchronization** = All cashiers have same pricing
- **Failover** = Backup cashiers when someone is sick

### Java Example - Horizontal Scaling:
```java
import java.util.List;
import java.util.ArrayList;
import java.util.Random;

public class HorizontalScalingExample {
    private List<Connection> connections;
    private LoadBalancer loadBalancer;
    
    public HorizontalScalingExample(List<Connection> connections) {
        this.connections = connections;
        this.loadBalancer = new LoadBalancer(connections);
    }
    
    // Distribute load across multiple servers
    public void distributeLoad() throws SQLException {
        System.out.println("Distributing load across " + connections.size() + " servers");
        
        // Simulate multiple concurrent requests
        for (int i = 0; i < 10; i++) {
            Connection conn = loadBalancer.getConnection();
            executeQuery(conn, "SELECT * FROM students WHERE id = " + i);
        }
    }
    
    // Execute query on specific connection
    private void executeQuery(Connection conn, String sql) throws SQLException {
        try (Statement stmt = conn.createStatement();
             ResultSet rs = stmt.executeQuery(sql)) {
            
            System.out.println("Query executed on server: " + conn.getMetaData().getURL());
        }
    }
    
    // Load balancer implementation
    private static class LoadBalancer {
        private List<Connection> connections;
        private Random random = new Random();
        
        public LoadBalancer(List<Connection> connections) {
            this.connections = connections;
        }
        
        public Connection getConnection() {
            // Simple round-robin load balancing
            int index = random.nextInt(connections.size());
            return connections.get(index);
        }
    }
}
```

## 12.3 Database Sharding

Database sharding involves partitioning data across multiple databases based on a shard key, allowing for horizontal scaling and improved performance.

### Sharding Strategies:
- **Range Sharding**: Partition by value ranges
- **Hash Sharding**: Partition using hash function
- **Directory Sharding**: Use lookup table for shard assignment
- **Consistent Hashing**: Distribute data evenly across shards
- **Geographic Sharding**: Partition by geographic location

### Real-World Analogy:
Database sharding is like organizing a library by sections:
- **Range Sharding** = Books A-M in section 1, N-Z in section 2
- **Hash Sharding** = Books distributed by author name hash
- **Directory Sharding** = Lookup table showing which section has which books
- **Consistent Hashing** = Even distribution across all sections
- **Geographic Sharding** = Different libraries in different cities

### Java Example - Database Sharding:
```java
public class DatabaseSharding {
    private List<Connection> shards;
    private ShardStrategy shardStrategy;
    
    public DatabaseSharding(List<Connection> shards, ShardStrategy shardStrategy) {
        this.shards = shards;
        this.shardStrategy = shardStrategy;
    }
    
    // Insert data with sharding
    public void insertData(String key, String data) throws SQLException {
        int shardIndex = shardStrategy.getShardIndex(key);
        Connection shard = shards.get(shardIndex);
        
        String sql = "INSERT INTO data_table (key, data) VALUES (?, ?)";
        try (PreparedStatement stmt = shard.prepareStatement(sql)) {
            stmt.setString(1, key);
            stmt.setString(2, data);
            stmt.executeUpdate();
        }
        
        System.out.println("Data inserted into shard " + shardIndex);
    }
    
    // Query data with sharding
    public String queryData(String key) throws SQLException {
        int shardIndex = shardStrategy.getShardIndex(key);
        Connection shard = shards.get(shardIndex);
        
        String sql = "SELECT data FROM data_table WHERE key = ?";
        try (PreparedStatement stmt = shard.prepareStatement(sql)) {
            stmt.setString(1, key);
            
            try (ResultSet rs = stmt.executeQuery()) {
                if (rs.next()) {
                    return rs.getString("data");
                }
            }
        }
        
        return null;
    }
    
    // Query across all shards
    public List<String> queryAllShards(String pattern) throws SQLException {
        List<String> results = new ArrayList<>();
        
        for (int i = 0; i < shards.size(); i++) {
            Connection shard = shards.get(i);
            String sql = "SELECT data FROM data_table WHERE data LIKE ?";
            
            try (PreparedStatement stmt = shard.prepareStatement(sql)) {
                stmt.setString(1, "%" + pattern + "%");
                
                try (ResultSet rs = stmt.executeQuery()) {
                    while (rs.next()) {
                        results.add("Shard " + i + ": " + rs.getString("data"));
                    }
                }
            }
        }
        
        return results;
    }
    
    // Shard strategy interface
    public interface ShardStrategy {
        int getShardIndex(String key);
    }
    
    // Hash-based sharding
    public static class HashShardStrategy implements ShardStrategy {
        private int shardCount;
        
        public HashShardStrategy(int shardCount) {
            this.shardCount = shardCount;
        }
        
        @Override
        public int getShardIndex(String key) {
            return Math.abs(key.hashCode()) % shardCount;
        }
    }
    
    // Range-based sharding
    public static class RangeShardStrategy implements ShardStrategy {
        private int shardCount;
        
        public RangeShardStrategy(int shardCount) {
            this.shardCount = shardCount;
        }
        
        @Override
        public int getShardIndex(String key) {
            // Simple range-based sharding
            char firstChar = key.charAt(0);
            return (firstChar - 'A') % shardCount;
        }
    }
}
```

## 12.4 Read Replicas

Read replicas are copies of the primary database that handle read operations, reducing load on the primary database and improving performance.

### Read Replica Benefits:
- **Load Distribution**: Spread read operations across replicas
- **Performance**: Faster read operations
- **Availability**: Continue serving reads during maintenance
- **Geographic Distribution**: Place replicas closer to users
- **Backup**: Additional copies for disaster recovery

### Real-World Analogy:
Read replicas are like having multiple copies of a book:
- **Primary Database** = Original book
- **Read Replicas** = Photocopies of the book
- **Load Distribution** = Different people read different copies
- **Performance** = No waiting for the original book
- **Availability** = Read copies even when original is being updated

### Java Example - Read Replicas:
```java
public class ReadReplicaExample {
    private Connection primaryConnection;
    private List<Connection> replicaConnections;
    private LoadBalancer readBalancer;
    
    public ReadReplicaExample(Connection primaryConnection, List<Connection> replicaConnections) {
        this.primaryConnection = primaryConnection;
        this.replicaConnections = replicaConnections;
        this.readBalancer = new LoadBalancer(replicaConnections);
    }
    
    // Write to primary database
    public void writeData(String data) throws SQLException {
        String sql = "INSERT INTO data_table (data) VALUES (?)";
        
        try (PreparedStatement stmt = primaryConnection.prepareStatement(sql)) {
            stmt.setString(1, data);
            stmt.executeUpdate();
        }
        
        System.out.println("Data written to primary database");
    }
    
    // Read from replica
    public String readData(int id) throws SQLException {
        Connection replica = readBalancer.getConnection();
        String sql = "SELECT data FROM data_table WHERE id = ?";
        
        try (PreparedStatement stmt = replica.prepareStatement(sql)) {
            stmt.setInt(1, id);
            
            try (ResultSet rs = stmt.executeQuery()) {
                if (rs.next()) {
                    return rs.getString("data");
                }
            }
        }
        
        return null;
    }
    
    // Read from all replicas for comparison
    public void compareReplicas(int id) throws SQLException {
        System.out.println("Comparing data across replicas:");
        
        for (int i = 0; i < replicaConnections.size(); i++) {
            Connection replica = replicaConnections.get(i);
            String sql = "SELECT data FROM data_table WHERE id = ?";
            
            try (PreparedStatement stmt = replica.prepareStatement(sql)) {
                stmt.setInt(1, id);
                
                try (ResultSet rs = stmt.executeQuery()) {
                    if (rs.next()) {
                        System.out.println("Replica " + i + ": " + rs.getString("data"));
                    }
                }
            }
        }
    }
    
    // Check replica lag
    public void checkReplicaLag() throws SQLException {
        for (int i = 0; i < replicaConnections.size(); i++) {
            Connection replica = replicaConnections.get(i);
            String sql = "SHOW SLAVE STATUS";
            
            try (Statement stmt = replica.createStatement();
                 ResultSet rs = stmt.executeQuery(sql)) {
                
                if (rs.next()) {
                    int lag = rs.getInt("Seconds_Behind_Master");
                    System.out.println("Replica " + i + " lag: " + lag + " seconds");
                }
            }
        }
    }
}
```

## 12.5 Master-Slave Replication

Master-slave replication involves one master database that handles writes and multiple slave databases that replicate data from the master for reads.

### Master-Slave Components:
- **Master Database**: Handles all write operations
- **Slave Databases**: Replicate data from master
- **Binary Logs**: Record all changes on master
- **Replication Process**: Transfer changes to slaves
- **Failover**: Promote slave to master if needed

### Real-World Analogy:
Master-slave replication is like a newspaper publishing system:
- **Master Database** = Main newspaper office
- **Slave Databases** = Local printing presses
- **Binary Logs** = Master copy of the newspaper
- **Replication Process** = Sending copies to local presses
- **Failover** = Local press becomes main office if needed

### Java Example - Master-Slave Replication:
```java
public class MasterSlaveReplication {
    private Connection masterConnection;
    private List<Connection> slaveConnections;
    
    public MasterSlaveReplication(Connection masterConnection, List<Connection> slaveConnections) {
        this.masterConnection = masterConnection;
        this.slaveConnections = slaveConnections;
    }
    
    // Write to master
    public void writeToMaster(String data) throws SQLException {
        String sql = "INSERT INTO data_table (data) VALUES (?)";
        
        try (PreparedStatement stmt = masterConnection.prepareStatement(sql)) {
            stmt.setString(1, data);
            stmt.executeUpdate();
        }
        
        System.out.println("Data written to master database");
    }
    
    // Read from slave
    public String readFromSlave(int id) throws SQLException {
        // Choose a random slave for load balancing
        Random random = new Random();
        Connection slave = slaveConnections.get(random.nextInt(slaveConnections.size()));
        
        String sql = "SELECT data FROM data_table WHERE id = ?";
        try (PreparedStatement stmt = slave.prepareStatement(sql)) {
            stmt.setInt(1, id);
            
            try (ResultSet rs = stmt.executeQuery()) {
                if (rs.next()) {
                    return rs.getString("data");
                }
            }
        }
        
        return null;
    }
    
    // Check replication status
    public void checkReplicationStatus() throws SQLException {
        System.out.println("Master-Slave Replication Status:");
        
        // Check master status
        String sql = "SHOW MASTER STATUS";
        try (Statement stmt = masterConnection.createStatement();
             ResultSet rs = stmt.executeQuery(sql)) {
            
            if (rs.next()) {
                System.out.println("Master Binary Log: " + rs.getString("File"));
                System.out.println("Master Position: " + rs.getLong("Position"));
            }
        }
        
        // Check slave status
        for (int i = 0; i < slaveConnections.size(); i++) {
            Connection slave = slaveConnections.get(i);
            sql = "SHOW SLAVE STATUS";
            
            try (Statement stmt = slave.createStatement();
                 ResultSet rs = stmt.executeQuery(sql)) {
                
                if (rs.next()) {
                    String ioRunning = rs.getString("Slave_IO_Running");
                    String sqlRunning = rs.getString("Slave_SQL_Running");
                    int lag = rs.getInt("Seconds_Behind_Master");
                    
                    System.out.println("Slave " + i + ": IO=" + ioRunning + 
                                     ", SQL=" + sqlRunning + ", Lag=" + lag + "s");
                }
            }
        }
    }
    
    // Promote slave to master
    public void promoteSlaveToMaster(int slaveIndex) throws SQLException {
        Connection slave = slaveConnections.get(slaveIndex);
        
        // Stop slave replication
        String sql = "STOP SLAVE";
        try (Statement stmt = slave.createStatement()) {
            stmt.execute(sql);
        }
        
        // Reset slave to become master
        sql = "RESET MASTER";
        try (Statement stmt = slave.createStatement()) {
            stmt.execute(sql);
        }
        
        System.out.println("Slave " + slaveIndex + " promoted to master");
    }
}
```

## 12.6 Master-Master Replication

Master-master replication allows multiple databases to act as both master and slave, enabling writes to any database in the cluster.

### Master-Master Components:
- **Multiple Masters**: Each database can handle writes
- **Bidirectional Replication**: Changes flow in both directions
- **Conflict Resolution**: Handle conflicting writes
- **Load Distribution**: Writes can go to any master
- **High Availability**: System continues if one master fails

### Real-World Analogy:
Master-master replication is like having multiple headquarters:
- **Multiple Masters** = Different headquarters offices
- **Bidirectional Replication** = Information flows between all offices
- **Conflict Resolution** = Resolve conflicting decisions
- **Load Distribution** = Work can be done at any office
- **High Availability** = System works even if one office closes

### Java Example - Master-Master Replication:
```java
public class MasterMasterReplication {
    private List<Connection> masterConnections;
    
    public MasterMasterReplication(List<Connection> masterConnections) {
        this.masterConnections = masterConnections;
    }
    
    // Write to any master
    public void writeToAnyMaster(String data) throws SQLException {
        // Choose a random master for load balancing
        Random random = new Random();
        Connection master = masterConnections.get(random.nextInt(masterConnections.size()));
        
        String sql = "INSERT INTO data_table (data) VALUES (?)";
        try (PreparedStatement stmt = master.prepareStatement(sql)) {
            stmt.setString(1, data);
            stmt.executeUpdate();
        }
        
        System.out.println("Data written to master: " + master.getMetaData().getURL());
    }
    
    // Read from any master
    public String readFromAnyMaster(int id) throws SQLException {
        // Choose a random master for load balancing
        Random random = new Random();
        Connection master = masterConnections.get(random.nextInt(masterConnections.size()));
        
        String sql = "SELECT data FROM data_table WHERE id = ?";
        try (PreparedStatement stmt = master.prepareStatement(sql)) {
            stmt.setInt(1, id);
            
            try (ResultSet rs = stmt.executeQuery()) {
                if (rs.next()) {
                    return rs.getString("data");
                }
            }
        }
        
        return null;
    }
    
    // Check replication status across all masters
    public void checkReplicationStatus() throws SQLException {
        System.out.println("Master-Master Replication Status:");
        
        for (int i = 0; i < masterConnections.size(); i++) {
            Connection master = masterConnections.get(i);
            String sql = "SHOW MASTER STATUS";
            
            try (Statement stmt = master.createStatement();
                 ResultSet rs = stmt.executeQuery(sql)) {
                
                if (rs.next()) {
                    System.out.println("Master " + i + ": Binary Log=" + rs.getString("File") + 
                                     ", Position=" + rs.getLong("Position"));
                }
            }
        }
    }
    
    // Handle write conflicts
    public void handleWriteConflicts() throws SQLException {
        System.out.println("Handling write conflicts:");
        
        // Simulate conflict resolution
        for (int i = 0; i < masterConnections.size(); i++) {
            Connection master = masterConnections.get(i);
            String sql = "SELECT COUNT(*) as conflict_count FROM data_table WHERE conflict_flag = 1";
            
            try (Statement stmt = master.createStatement();
                 ResultSet rs = stmt.executeQuery(sql)) {
                
                if (rs.next()) {
                    int conflictCount = rs.getInt("conflict_count");
                    if (conflictCount > 0) {
                        System.out.println("Master " + i + " has " + conflictCount + " conflicts");
                        resolveConflicts(master);
                    }
                }
            }
        }
    }
    
    private void resolveConflicts(Connection master) throws SQLException {
        // Simple conflict resolution: keep the latest timestamp
        String sql = """
            UPDATE data_table 
            SET conflict_flag = 0 
            WHERE id IN (
                SELECT id FROM (
                    SELECT id FROM data_table 
                    WHERE conflict_flag = 1 
                    ORDER BY timestamp DESC 
                    LIMIT 1
                ) as latest
            )
            """;
        
        try (Statement stmt = master.createStatement()) {
            int rowsAffected = stmt.executeUpdate(sql);
            System.out.println("Resolved " + rowsAffected + " conflicts");
        }
    }
}
```

## 12.7 Database Partitioning

Database partitioning divides large tables into smaller, more manageable pieces while maintaining logical unity, improving performance and manageability.

### Partitioning Types:
- **Range Partitioning**: Partition by value ranges
- **Hash Partitioning**: Partition using hash function
- **List Partitioning**: Partition by specific values
- **Composite Partitioning**: Combine multiple partitioning methods
- **Subpartitioning**: Partition within partitions

### Real-World Analogy:
Database partitioning is like organizing a large filing system:
- **Range Partitioning** = Files A-M in drawer 1, N-Z in drawer 2
- **Hash Partitioning** = Files distributed by hash of filename
- **List Partitioning** = Specific file types in specific drawers
- **Composite Partitioning** = Multiple organization methods
- **Subpartitioning** = Sub-drawers within main drawers

### Java Example - Database Partitioning:
```java
public class DatabasePartitioning {
    private Connection connection;
    
    public DatabasePartitioning(Connection connection) {
        this.connection = connection;
    }
    
    // Create range-partitioned table
    public void createRangePartitionedTable() throws SQLException {
        String sql = """
            CREATE TABLE students_partitioned (
                id INT,
                name VARCHAR(100),
                email VARCHAR(100),
                gpa DECIMAL(3,2),
                created_at DATE
            ) PARTITION BY RANGE (YEAR(created_at)) (
                PARTITION p2020 VALUES LESS THAN (2021),
                PARTITION p2021 VALUES LESS THAN (2022),
                PARTITION p2022 VALUES LESS THAN (2023),
                PARTITION p2023 VALUES LESS THAN (2024),
                PARTITION p_future VALUES LESS THAN MAXVALUE
            )
            """;
        
        try (Statement stmt = connection.createStatement()) {
            stmt.execute(sql);
            System.out.println("Range-partitioned table created");
        }
    }
    
    // Create hash-partitioned table
    public void createHashPartitionedTable() throws SQLException {
        String sql = """
            CREATE TABLE students_hash (
                id INT,
                name VARCHAR(100),
                email VARCHAR(100),
                gpa DECIMAL(3,2)
            ) PARTITION BY HASH(id) PARTITIONS 4
            """;
        
        try (Statement stmt = connection.createStatement()) {
            stmt.execute(sql);
            System.out.println("Hash-partitioned table created");
        }
    }
    
    // Query specific partition
    public void queryPartition(String partitionName) throws SQLException {
        String sql = "SELECT * FROM students_partitioned PARTITION (" + partitionName + ")";
        
        try (Statement stmt = connection.createStatement();
             ResultSet rs = stmt.executeQuery(sql)) {
            
            System.out.println("Data from partition " + partitionName + ":");
            while (rs.next()) {
                System.out.println("ID: " + rs.getInt("id") + 
                                 ", Name: " + rs.getString("name"));
            }
        }
    }
    
    // Get partition information
    public void getPartitionInfo() throws SQLException {
        String sql = """
            SELECT 
                table_name,
                partition_name,
                partition_expression,
                partition_description
            FROM information_schema.partitions
            WHERE table_name = 'students_partitioned'
            AND partition_name IS NOT NULL
            """;
        
        try (Statement stmt = connection.createStatement();
             ResultSet rs = stmt.executeQuery(sql)) {
            
            System.out.println("Partition Information:");
            while (rs.next()) {
                System.out.println("Partition: " + rs.getString("partition_name") + 
                                 ", Expression: " + rs.getString("partition_expression") + 
                                 ", Description: " + rs.getString("partition_description"));
            }
        }
    }
    
    // Add new partition
    public void addNewPartition(String partitionName, int year) throws SQLException {
        String sql = "ALTER TABLE students_partitioned ADD PARTITION (PARTITION " + 
                    partitionName + " VALUES LESS THAN (" + year + "))";
        
        try (Statement stmt = connection.createStatement()) {
            stmt.execute(sql);
            System.out.println("New partition added: " + partitionName);
        }
    }
    
    // Drop partition
    public void dropPartition(String partitionName) throws SQLException {
        String sql = "ALTER TABLE students_partitioned DROP PARTITION " + partitionName;
        
        try (Statement stmt = connection.createStatement()) {
            stmt.execute(sql);
            System.out.println("Partition dropped: " + partitionName);
        }
    }
}
```

## 12.8 Caching Strategies

Caching strategies store frequently accessed data in memory to improve performance and reduce database load.

### Caching Types:
- **Application-Level Caching**: Cache within application
- **Database Caching**: Cache within database system
- **Distributed Caching**: Cache across multiple servers
- **CDN Caching**: Cache at edge locations
- **Query Result Caching**: Cache query results

### Real-World Analogy:
Caching strategies are like having a personal assistant:
- **Application-Level Caching** = Personal notes and reminders
- **Database Caching** = Office filing system
- **Distributed Caching** = Shared knowledge base
- **CDN Caching** = Local branch offices
- **Query Result Caching** = Pre-computed answers

### Java Example - Caching Strategies:
```java
import java.util.concurrent.ConcurrentHashMap;
import java.util.Map;
import java.util.concurrent.TimeUnit;

public class CachingStrategies {
    private Map<String, CacheEntry> cache = new ConcurrentHashMap<>();
    private long defaultTtl = 300000; // 5 minutes
    
    // Cache entry with TTL
    private static class CacheEntry {
        private Object value;
        private long timestamp;
        private long ttl;
        
        public CacheEntry(Object value, long ttl) {
            this.value = value;
            this.timestamp = System.currentTimeMillis();
            this.ttl = ttl;
        }
        
        public boolean isExpired() {
            return System.currentTimeMillis() - timestamp > ttl;
        }
        
        public Object getValue() {
            return value;
        }
    }
    
    // Put data in cache
    public void put(String key, Object value) {
        put(key, value, defaultTtl);
    }
    
    public void put(String key, Object value, long ttl) {
        cache.put(key, new CacheEntry(value, ttl));
        System.out.println("Data cached: " + key);
    }
    
    // Get data from cache
    public Object get(String key) {
        CacheEntry entry = cache.get(key);
        if (entry != null && !entry.isExpired()) {
            System.out.println("Cache hit: " + key);
            return entry.getValue();
        }
        
        if (entry != null) {
            cache.remove(key);
            System.out.println("Cache expired: " + key);
        } else {
            System.out.println("Cache miss: " + key);
        }
        
        return null;
    }
    
    // Get or compute pattern
    public Object getOrCompute(String key, java.util.function.Supplier<Object> supplier) {
        Object value = get(key);
        if (value == null) {
            value = supplier.get();
            put(key, value);
        }
        return value;
    }
    
    // Cache statistics
    public void printCacheStats() {
        int totalEntries = cache.size();
        int expiredEntries = 0;
        
        for (CacheEntry entry : cache.values()) {
            if (entry.isExpired()) {
                expiredEntries++;
            }
        }
        
        System.out.println("Cache Statistics:");
        System.out.println("Total Entries: " + totalEntries);
        System.out.println("Expired Entries: " + expiredEntries);
        System.out.println("Valid Entries: " + (totalEntries - expiredEntries));
    }
    
    // Clear expired entries
    public void clearExpiredEntries() {
        cache.entrySet().removeIf(entry -> entry.getValue().isExpired());
        System.out.println("Expired entries cleared");
    }
    
    // Clear all cache
    public void clearAll() {
        cache.clear();
        System.out.println("All cache cleared");
    }
}
```