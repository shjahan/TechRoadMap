# Section 5 – Database Services

## 5.1 Cloud SQL (Managed MySQL, PostgreSQL, SQL Server)

Cloud SQL is a fully managed relational database service.

### Key Features:
- Fully Managed
- Automatic Backups
- High Availability
- Automatic Scaling

### Supported Databases:
- MySQL
- PostgreSQL
- SQL Server

### Java Example:
```java
import com.google.cloud.sql.connector.ConnectorConfig;
import com.google.cloud.sql.connector.ConnectorRegistry;

public class CloudSQLManager {
    public void createDatabase(String projectId, String instanceName) {
        System.out.println("Cloud SQL instance created: " + instanceName);
    }
    
    public void connectToDatabase(String connectionName) {
        System.out.println("Connected to database: " + connectionName);
    }
}
```

## 5.2 Cloud Spanner (Global Relational Database)

Cloud Spanner is a globally distributed relational database.

### Key Features:
- Global Distribution
- ACID Transactions
- Horizontal Scaling
- 99.999% Availability

### Java Example:
```java
import com.google.cloud.spanner.*;

public class CloudSpannerManager {
    private DatabaseClient dbClient;
    
    public void createTable(String tableName) {
        System.out.println("Table created: " + tableName);
    }
    
    public void insertData(String tableName, String data) {
        System.out.println("Data inserted into: " + tableName);
    }
}
```

## 5.3 Firestore (NoSQL Document Database)

Firestore is a NoSQL document database for mobile and web applications.

### Key Features:
- Real-time Updates
- Offline Support
- Automatic Scaling
- Multi-region Replication

### Java Example:
```java
import com.google.cloud.firestore.*;

public class FirestoreManager {
    private Firestore db;
    
    public void createDocument(String collection, String documentId, Map<String, Object> data) {
        DocumentReference docRef = db.collection(collection).document(documentId);
        docRef.set(data);
        System.out.println("Document created: " + documentId);
    }
    
    public void getDocument(String collection, String documentId) {
        DocumentReference docRef = db.collection(collection).document(documentId);
        System.out.println("Document retrieved: " + documentId);
    }
}
```

## 5.4 Cloud Bigtable (NoSQL Wide-Column Database)

Cloud Bigtable is a NoSQL wide-column database for large-scale applications.

### Key Features:
- High Performance
- Massive Scale
- Low Latency
- Integration with BigQuery

### Java Example:
```java
import com.google.cloud.bigtable.data.v2.*;

public class BigtableManager {
    private BigtableDataClient dataClient;
    
    public void createTable(String tableId) {
        System.out.println("Bigtable created: " + tableId);
    }
    
    public void insertRow(String tableId, String rowKey, Map<String, String> data) {
        System.out.println("Row inserted into: " + tableId);
    }
}
```

## 5.5 Cloud Memorystore (Managed Redis)

Cloud Memorystore is a fully managed Redis service.

### Key Features:
- Fully Managed Redis
- High Availability
- Automatic Failover
- Monitoring and Alerting

### Java Example:
```java
import redis.clients.jedis.Jedis;

public class MemorystoreManager {
    private Jedis jedis;
    
    public void connect(String host, int port) {
        jedis = new Jedis(host, port);
        System.out.println("Connected to Redis");
    }
    
    public void setValue(String key, String value) {
        jedis.set(key, value);
        System.out.println("Value set: " + key);
    }
    
    public String getValue(String key) {
        return jedis.get(key);
    }
}
```

## 5.6 Cloud Datastore (NoSQL Document Database)

Cloud Datastore is a NoSQL document database for web and mobile applications.

### Key Features:
- ACID Transactions
- Automatic Scaling
- Multi-region Replication
- Free Tier Available

### Java Example:
```java
import com.google.cloud.datastore.*;

public class DatastoreManager {
    private Datastore datastore;
    
    public void createEntity(String kind, String name, String value) {
        KeyFactory keyFactory = datastore.newKeyFactory().setKind(kind);
        Key key = datastore.allocateId(keyFactory.newKey());
        
        Entity entity = Entity.newBuilder(key)
            .set("name", name)
            .set("value", value)
            .build();
        
        datastore.put(entity);
        System.out.println("Entity created: " + key);
    }
}
```

## 5.7 Database Migration Service

Database Migration Service helps migrate databases to GCP.

### Key Features:
- Minimal Downtime
- Continuous Replication
- Schema Conversion
- Data Validation

### Java Example:
```java
public class DatabaseMigrationManager {
    public void createMigrationJob(String sourceDb, String targetDb) {
        System.out.println("Migration job created: " + sourceDb + " -> " + targetDb);
    }
    
    public void startMigration(String jobId) {
        System.out.println("Migration started: " + jobId);
    }
}
```

## 5.8 Database Security

Database security includes encryption, access control, and monitoring.

### Security Features:
- Encryption at Rest
- Encryption in Transit
- IAM Integration
- Audit Logging

### Java Example:
```java
public class DatabaseSecurityManager {
    public void enableEncryption(String databaseId) {
        System.out.println("Encryption enabled for: " + databaseId);
    }
    
    public void setAccessControl(String databaseId, String user, String role) {
        System.out.println("Access control set for: " + databaseId);
    }
}
```

## 5.9 Database Backup and Recovery

Database backup and recovery ensures data protection and business continuity.

### Backup Features:
- Automated Backups
- Point-in-time Recovery
- Cross-region Replication
- Backup Retention

### Java Example:
```java
public class DatabaseBackupManager {
    public void createBackup(String databaseId, String backupName) {
        System.out.println("Backup created: " + backupName);
    }
    
    public void restoreFromBackup(String backupName, String targetDatabase) {
        System.out.println("Restored from backup: " + backupName);
    }
}
```

## 5.10 Database Performance Tuning

Database performance tuning optimizes query performance and resource utilization.

### Tuning Areas:
- Query Optimization
- Index Management
- Connection Pooling
- Resource Allocation

### Java Example:
```java
public class DatabasePerformanceManager {
    public void optimizeQuery(String query) {
        System.out.println("Query optimized: " + query);
    }
    
    public void createIndex(String tableName, String columnName) {
        System.out.println("Index created on: " + tableName + "." + columnName);
    }
}
```