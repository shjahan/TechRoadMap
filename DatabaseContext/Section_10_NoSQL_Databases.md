# Section 10 – NoSQL Databases

## 10.1 NoSQL Database Types

NoSQL (Not Only SQL) databases provide flexible, scalable alternatives to traditional relational databases, designed to handle various data models and large-scale applications.

### NoSQL Categories:
- **Document Databases**: Store data as documents (JSON, BSON)
- **Key-Value Stores**: Simple key-value pairs
- **Column-Family Stores**: Column-oriented data storage
- **Graph Databases**: Node-edge relationship storage
- **Time-Series Databases**: Optimized for time-stamped data

### Real-World Analogy:
NoSQL databases are like different storage systems:
- **Document Databases** = Filing cabinets with complete documents
- **Key-Value Stores** = Simple address books
- **Column-Family Stores** = Spreadsheets with columns
- **Graph Databases** = Social network connections
- **Time-Series Databases** = Stock market tickers

### Java Example - NoSQL Types:
```java
// Document Database (MongoDB-style)
import org.bson.Document;
import java.util.Arrays;

public class DocumentDatabaseExample {
    public Document createUserDocument() {
        return new Document("_id", "user123")
            .append("name", "John Doe")
            .append("email", "john@example.com")
            .append("address", new Document()
                .append("street", "123 Main St")
                .append("city", "New York")
                .append("zip", "10001"))
            .append("hobbies", Arrays.asList("reading", "gaming", "cooking"));
    }
}

// Key-Value Store (Redis-style)
public class KeyValueStoreExample {
    private Map<String, String> keyValueStore = new HashMap<>();
    
    public void storeValue(String key, String value) {
        keyValueStore.put(key, value);
    }
    
    public String getValue(String key) {
        return keyValueStore.get(key);
    }
}

// Column-Family Store (Cassandra-style)
public class ColumnFamilyExample {
    private Map<String, Map<String, String>> columnFamily = new HashMap<>();
    
    public void insertRow(String rowKey, Map<String, String> columns) {
        columnFamily.put(rowKey, columns);
    }
    
    public Map<String, String> getRow(String rowKey) {
        return columnFamily.get(rowKey);
    }
}
```

## 10.2 Document Databases (MongoDB, CouchDB)

Document databases store data as documents, typically in JSON or BSON format, providing flexible schema and rich querying capabilities.

### Key Features:
- **Schema Flexibility**: No fixed schema required
- **Rich Queries**: Complex querying capabilities
- **Indexing**: Support for various index types
- **Replication**: Built-in replication support
- **Sharding**: Horizontal scaling through sharding

### Real-World Analogy:
Document databases are like digital filing systems:
- **Documents** = Individual files with complete information
- **Collections** = File folders containing related documents
- **Schema Flexibility** = No standard form required
- **Rich Queries** = Advanced search capabilities

### Java Example - MongoDB Operations:
```java
import com.mongodb.client.MongoClient;
import com.mongodb.client.MongoClients;
import com.mongodb.client.MongoCollection;
import com.mongodb.client.MongoDatabase;
import org.bson.Document;
import java.util.Arrays;

public class MongoDBExample {
    private MongoClient mongoClient;
    private MongoDatabase database;
    private MongoCollection<Document> collection;
    
    public MongoDBExample() {
        mongoClient = MongoClients.create("mongodb://localhost:27017");
        database = mongoClient.getDatabase("university");
        collection = database.getCollection("students");
    }
    
    // Insert document
    public void insertStudent(String name, String email, String major) {
        Document student = new Document("name", name)
            .append("email", email)
            .append("major", major)
            .append("enrolled", true)
            .append("courses", Arrays.asList("CS101", "MATH201"));
        
        collection.insertOne(student);
        System.out.println("Student inserted: " + name);
    }
    
    // Find documents
    public void findStudentsByMajor(String major) {
        Document query = new Document("major", major);
        
        for (Document student : collection.find(query)) {
            System.out.println("Student: " + student.getString("name") + 
                             ", Email: " + student.getString("email"));
        }
    }
    
    // Update document
    public void updateStudentEmail(String name, String newEmail) {
        Document filter = new Document("name", name);
        Document update = new Document("$set", new Document("email", newEmail));
        
        collection.updateOne(filter, update);
        System.out.println("Student email updated: " + name);
    }
    
    // Delete document
    public void deleteStudent(String name) {
        Document filter = new Document("name", name);
        collection.deleteOne(filter);
        System.out.println("Student deleted: " + name);
    }
    
    // Complex query
    public void findStudentsWithGPA(double minGpa) {
        Document query = new Document("gpa", new Document("$gte", minGpa));
        Document sort = new Document("gpa", -1);
        
        for (Document student : collection.find(query).sort(sort)) {
            System.out.println("Student: " + student.getString("name") + 
                             ", GPA: " + student.getDouble("gpa"));
        }
    }
}
```

## 10.3 Key-Value Stores (Redis, DynamoDB)

Key-value stores provide simple, fast access to data using unique keys, making them ideal for caching and session storage.

### Key Features:
- **Simple Model**: Key-value pairs only
- **High Performance**: Very fast read/write operations
- **Scalability**: Easy horizontal scaling
- **Persistence**: Optional data persistence
- **Atomic Operations**: Support for atomic operations

### Real-World Analogy:
Key-value stores are like simple address books:
- **Keys** = Names or identifiers
- **Values** = Associated information
- **Fast Lookup** = Quick name-to-address lookup
- **Simple Structure** = No complex relationships

### Java Example - Redis Operations:
```java
import redis.clients.jedis.Jedis;
import java.util.Set;

public class RedisExample {
    private Jedis jedis;
    
    public RedisExample() {
        jedis = new Jedis("localhost", 6379);
    }
    
    // Basic key-value operations
    public void setValue(String key, String value) {
        jedis.set(key, value);
        System.out.println("Set " + key + " = " + value);
    }
    
    public String getValue(String key) {
        String value = jedis.get(key);
        System.out.println("Get " + key + " = " + value);
        return value;
    }
    
    // Expire key after specified time
    public void setValueWithExpiry(String key, String value, int seconds) {
        jedis.setex(key, seconds, value);
        System.out.println("Set " + key + " = " + value + " with expiry " + seconds + " seconds");
    }
    
    // Hash operations
    public void setHashField(String key, String field, String value) {
        jedis.hset(key, field, value);
        System.out.println("Set hash " + key + "." + field + " = " + value);
    }
    
    public String getHashField(String key, String field) {
        String value = jedis.hget(key, field);
        System.out.println("Get hash " + key + "." + field + " = " + value);
        return value;
    }
    
    // List operations
    public void addToList(String key, String... values) {
        for (String value : values) {
            jedis.lpush(key, value);
        }
        System.out.println("Added values to list " + key);
    }
    
    public void getListRange(String key, int start, int end) {
        java.util.List<String> values = jedis.lrange(key, start, end);
        System.out.println("List " + key + " range: " + values);
    }
    
    // Set operations
    public void addToSet(String key, String... values) {
        for (String value : values) {
            jedis.sadd(key, value);
        }
        System.out.println("Added values to set " + key);
    }
    
    public Set<String> getSetMembers(String key) {
        Set<String> members = jedis.smembers(key);
        System.out.println("Set " + key + " members: " + members);
        return members;
    }
    
    // Session management example
    public void createSession(String sessionId, String userId, int timeoutSeconds) {
        String sessionKey = "session:" + sessionId;
        jedis.hset(sessionKey, "userId", userId);
        jedis.hset(sessionKey, "createdAt", String.valueOf(System.currentTimeMillis()));
        jedis.expire(sessionKey, timeoutSeconds);
        System.out.println("Session created: " + sessionId);
    }
    
    public String getSessionUserId(String sessionId) {
        String sessionKey = "session:" + sessionId;
        return jedis.hget(sessionKey, "userId");
    }
}
```

## 10.4 Column-Family Stores (Cassandra, HBase)

Column-family stores organize data in columns rather than rows, providing efficient storage and retrieval for large-scale distributed systems.

### Key Features:
- **Column-Oriented**: Data stored by columns
- **Distributed**: Built for distributed environments
- **Scalable**: Linear scalability
- **Fault-Tolerant**: High availability
- **Flexible Schema**: Dynamic column addition

### Real-World Analogy:
Column-family stores are like spreadsheets:
- **Rows** = Individual records
- **Columns** = Attributes or properties
- **Column Families** = Related columns grouped together
- **Distributed** = Multiple spreadsheet copies

### Java Example - Cassandra Operations:
```java
import com.datastax.driver.core.*;
import com.datastax.driver.core.querybuilder.QueryBuilder;

public class CassandraExample {
    private Cluster cluster;
    private Session session;
    
    public CassandraExample() {
        cluster = Cluster.builder()
            .addContactPoint("localhost")
            .build();
        session = cluster.connect();
    }
    
    // Create keyspace and table
    public void createSchema() {
        // Create keyspace
        String createKeyspace = "CREATE KEYSPACE IF NOT EXISTS university " +
                               "WITH REPLICATION = {'class': 'SimpleStrategy', 'replication_factor': 1}";
        session.execute(createKeyspace);
        
        // Create table
        String createTable = "CREATE TABLE IF NOT EXISTS university.students (" +
                            "student_id UUID PRIMARY KEY, " +
                            "name TEXT, " +
                            "email TEXT, " +
                            "major TEXT, " +
                            "gpa DECIMAL)";
        session.execute(createTable);
        
        System.out.println("Schema created successfully");
    }
    
    // Insert data
    public void insertStudent(UUID studentId, String name, String email, String major, BigDecimal gpa) {
        String insertQuery = "INSERT INTO university.students (student_id, name, email, major, gpa) " +
                            "VALUES (?, ?, ?, ?, ?)";
        
        PreparedStatement prepared = session.prepare(insertQuery);
        BoundStatement bound = prepared.bind(studentId, name, email, major, gpa);
        
        session.execute(bound);
        System.out.println("Student inserted: " + name);
    }
    
    // Query data
    public void findStudentById(UUID studentId) {
        String selectQuery = "SELECT * FROM university.students WHERE student_id = ?";
        
        PreparedStatement prepared = session.prepare(selectQuery);
        BoundStatement bound = prepared.bind(studentId);
        
        ResultSet result = session.execute(bound);
        for (Row row : result) {
            System.out.println("Student: " + row.getString("name") + 
                             ", Email: " + row.getString("email") + 
                             ", Major: " + row.getString("major") + 
                             ", GPA: " + row.getDecimal("gpa"));
        }
    }
    
    // Query by major
    public void findStudentsByMajor(String major) {
        String selectQuery = "SELECT * FROM university.students WHERE major = ? ALLOW FILTERING";
        
        PreparedStatement prepared = session.prepare(selectQuery);
        BoundStatement bound = prepared.bind(major);
        
        ResultSet result = session.execute(bound);
        for (Row row : result) {
            System.out.println("Student: " + row.getString("name") + 
                             ", Major: " + row.getString("major"));
        }
    }
    
    // Update data
    public void updateStudentGPA(UUID studentId, BigDecimal newGPA) {
        String updateQuery = "UPDATE university.students SET gpa = ? WHERE student_id = ?";
        
        PreparedStatement prepared = session.prepare(updateQuery);
        BoundStatement bound = prepared.bind(newGPA, studentId);
        
        session.execute(bound);
        System.out.println("Student GPA updated");
    }
    
    // Delete data
    public void deleteStudent(UUID studentId) {
        String deleteQuery = "DELETE FROM university.students WHERE student_id = ?";
        
        PreparedStatement prepared = session.prepare(deleteQuery);
        BoundStatement bound = prepared.bind(studentId);
        
        session.execute(bound);
        System.out.println("Student deleted");
    }
}
```

## 10.5 Graph Databases (Neo4j, Amazon Neptune)

Graph databases store data as nodes and edges, making them ideal for representing and querying complex relationships.

### Key Features:
- **Nodes**: Entities or objects
- **Edges**: Relationships between nodes
- **Properties**: Attributes on nodes and edges
- **Traversals**: Efficient relationship navigation
- **Cypher Query Language**: Specialized query language

### Real-World Analogy:
Graph databases are like social networks:
- **Nodes** = People or entities
- **Edges** = Relationships (friends, follows, likes)
- **Properties** = Attributes (name, age, interests)
- **Traversals** = Finding connections between people

### Java Example - Neo4j Operations:
```java
import org.neo4j.driver.*;
import java.util.List;
import java.util.Map;

public class Neo4jExample {
    private Driver driver;
    private Session session;
    
    public Neo4jExample() {
        driver = GraphDatabase.driver("bolt://localhost:7687", 
                                    AuthTokens.basic("neo4j", "password"));
        session = driver.session();
    }
    
    // Create nodes
    public void createPerson(String name, int age, String occupation) {
        String cypher = "CREATE (p:Person {name: $name, age: $age, occupation: $occupation})";
        Map<String, Object> parameters = Map.of("name", name, "age", age, "occupation", occupation);
        
        session.run(cypher, parameters);
        System.out.println("Person created: " + name);
    }
    
    // Create relationships
    public void createFriendship(String person1, String person2) {
        String cypher = """
            MATCH (p1:Person {name: $person1})
            MATCH (p2:Person {name: $person2})
            CREATE (p1)-[:FRIENDS_WITH]->(p2)
            """;
        Map<String, Object> parameters = Map.of("person1", person1, "person2", person2);
        
        session.run(cypher, parameters);
        System.out.println("Friendship created: " + person1 + " -> " + person2);
    }
    
    // Find friends of a person
    public void findFriends(String personName) {
        String cypher = """
            MATCH (p:Person {name: $name})-[:FRIENDS_WITH]->(friend:Person)
            RETURN friend.name, friend.age, friend.occupation
            """;
        Map<String, Object> parameters = Map.of("name", personName);
        
        Result result = session.run(cypher, parameters);
        System.out.println("Friends of " + personName + ":");
        while (result.hasNext()) {
            Record record = result.next();
            System.out.println("- " + record.get("friend.name") + 
                             " (age: " + record.get("friend.age") + 
                             ", occupation: " + record.get("friend.occupation") + ")");
        }
    }
    
    // Find mutual friends
    public void findMutualFriends(String person1, String person2) {
        String cypher = """
            MATCH (p1:Person {name: $person1})-[:FRIENDS_WITH]->(mutual:Person)<-[:FRIENDS_WITH]-(p2:Person {name: $person2})
            RETURN mutual.name
            """;
        Map<String, Object> parameters = Map.of("person1", person1, "person2", person2);
        
        Result result = session.run(cypher, parameters);
        System.out.println("Mutual friends of " + person1 + " and " + person2 + ":");
        while (result.hasNext()) {
            Record record = result.next();
            System.out.println("- " + record.get("mutual.name"));
        }
    }
    
    // Find shortest path
    public void findShortestPath(String person1, String person2) {
        String cypher = """
            MATCH (p1:Person {name: $person1}), (p2:Person {name: $person2})
            MATCH path = shortestPath((p1)-[:FRIENDS_WITH*]-(p2))
            RETURN path
            """;
        Map<String, Object> parameters = Map.of("person1", person1, "person2", person2);
        
        Result result = session.run(cypher, parameters);
        if (result.hasNext()) {
            Record record = result.next();
            System.out.println("Shortest path found between " + person1 + " and " + person2);
        } else {
            System.out.println("No path found between " + person1 + " and " + person2);
        }
    }
    
    // Find people by occupation
    public void findPeopleByOccupation(String occupation) {
        String cypher = "MATCH (p:Person {occupation: $occupation}) RETURN p.name, p.age";
        Map<String, Object> parameters = Map.of("occupation", occupation);
        
        Result result = session.run(cypher, parameters);
        System.out.println("People with occupation " + occupation + ":");
        while (result.hasNext()) {
            Record record = result.next();
            System.out.println("- " + record.get("p.name") + " (age: " + record.get("p.age") + ")");
        }
    }
}
```

## 10.6 Time-Series Databases

Time-series databases are optimized for storing and querying time-stamped data, making them ideal for IoT, monitoring, and analytics applications.

### Key Features:
- **Time-Ordered Data**: Data sorted by timestamp
- **Efficient Compression**: Optimized storage for time-series data
- **Aggregation Functions**: Built-in time-based aggregations
- **Retention Policies**: Automatic data cleanup
- **High Write Throughput**: Optimized for frequent writes

### Real-World Analogy:
Time-series databases are like data loggers:
- **Timestamps** = When each measurement was taken
- **Values** = The actual measurements
- **Compression** = Efficient storage of repetitive data
- **Aggregation** = Summary statistics over time periods

### Java Example - Time-Series Database:
```java
import java.time.Instant;
import java.time.temporal.ChronoUnit;
import java.util.List;
import java.util.ArrayList;

public class TimeSeriesExample {
    private List<TimeSeriesPoint> dataPoints = new ArrayList<>();
    
    // Time series data point
    public static class TimeSeriesPoint {
        private Instant timestamp;
        private String metric;
        private double value;
        private Map<String, String> tags;
        
        public TimeSeriesPoint(Instant timestamp, String metric, double value, Map<String, String> tags) {
            this.timestamp = timestamp;
            this.metric = metric;
            this.value = value;
            this.tags = tags;
        }
        
        // Getters and setters
        public Instant getTimestamp() { return timestamp; }
        public String getMetric() { return metric; }
        public double getValue() { return value; }
        public Map<String, String> getTags() { return tags; }
    }
    
    // Insert time series data
    public void insertDataPoint(String metric, double value, Map<String, String> tags) {
        TimeSeriesPoint point = new TimeSeriesPoint(Instant.now(), metric, value, tags);
        dataPoints.add(point);
        System.out.println("Data point inserted: " + metric + " = " + value);
    }
    
    // Query data by time range
    public List<TimeSeriesPoint> queryByTimeRange(Instant startTime, Instant endTime) {
        return dataPoints.stream()
            .filter(point -> point.getTimestamp().isAfter(startTime) && 
                            point.getTimestamp().isBefore(endTime))
            .collect(Collectors.toList());
    }
    
    // Query data by metric
    public List<TimeSeriesPoint> queryByMetric(String metric) {
        return dataPoints.stream()
            .filter(point -> point.getMetric().equals(metric))
            .collect(Collectors.toList());
    }
    
    // Calculate average over time period
    public double calculateAverage(String metric, Instant startTime, Instant endTime) {
        List<TimeSeriesPoint> points = queryByTimeRange(startTime, endTime).stream()
            .filter(point -> point.getMetric().equals(metric))
            .collect(Collectors.toList());
        
        if (points.isEmpty()) {
            return 0.0;
        }
        
        double sum = points.stream().mapToDouble(TimeSeriesPoint::getValue).sum();
        return sum / points.size();
    }
    
    // Calculate moving average
    public List<Double> calculateMovingAverage(String metric, int windowSize) {
        List<TimeSeriesPoint> points = queryByMetric(metric);
        List<Double> movingAverages = new ArrayList<>();
        
        for (int i = windowSize - 1; i < points.size(); i++) {
            double sum = 0.0;
            for (int j = i - windowSize + 1; j <= i; j++) {
                sum += points.get(j).getValue();
            }
            movingAverages.add(sum / windowSize);
        }
        
        return movingAverages;
    }
    
    // Find anomalies (values outside normal range)
    public List<TimeSeriesPoint> findAnomalies(String metric, double threshold) {
        List<TimeSeriesPoint> points = queryByMetric(metric);
        if (points.size() < 2) {
            return new ArrayList<>();
        }
        
        // Calculate mean and standard deviation
        double mean = points.stream().mapToDouble(TimeSeriesPoint::getValue).average().orElse(0.0);
        double variance = points.stream()
            .mapToDouble(point -> Math.pow(point.getValue() - mean, 2))
            .average().orElse(0.0);
        double stdDev = Math.sqrt(variance);
        
        return points.stream()
            .filter(point -> Math.abs(point.getValue() - mean) > threshold * stdDev)
            .collect(Collectors.toList());
    }
}
```

## 10.7 Search Engines (Elasticsearch, Solr)

Search engines provide full-text search capabilities and are optimized for searching and analyzing large volumes of text data.

### Key Features:
- **Full-Text Search**: Search across all text content
- **Indexing**: Fast text indexing and retrieval
- **Scoring**: Relevance scoring for search results
- **Faceted Search**: Filter and categorize results
- **Real-Time Search**: Near real-time search capabilities

### Real-World Analogy:
Search engines are like digital libraries:
- **Indexing** = Cataloging all books and content
- **Search** = Finding relevant information quickly
- **Scoring** = Ranking results by relevance
- **Faceted Search** = Filtering by categories

### Java Example - Elasticsearch Operations:
```java
import org.elasticsearch.client.RestHighLevelClient;
import org.elasticsearch.client.RestClient;
import org.elasticsearch.action.index.IndexRequest;
import org.elasticsearch.action.search.SearchRequest;
import org.elasticsearch.action.search.SearchResponse;
import org.elasticsearch.search.builder.SearchSourceBuilder;
import org.elasticsearch.search.SearchHit;
import org.elasticsearch.common.xcontent.XContentType;

public class ElasticsearchExample {
    private RestHighLevelClient client;
    
    public ElasticsearchExample() {
        client = new RestHighLevelClient(
            RestClient.builder(new HttpHost("localhost", 9200, "http"))
        );
    }
    
    // Index document
    public void indexDocument(String indexName, String id, String jsonDocument) {
        IndexRequest request = new IndexRequest(indexName);
        request.id(id);
        request.source(jsonDocument, XContentType.JSON);
        
        try {
            client.index(request, RequestOptions.DEFAULT);
            System.out.println("Document indexed: " + id);
        } catch (IOException e) {
            System.err.println("Error indexing document: " + e.getMessage());
        }
    }
    
    // Search documents
    public void searchDocuments(String indexName, String query) {
        SearchRequest searchRequest = new SearchRequest(indexName);
        SearchSourceBuilder searchSourceBuilder = new SearchSourceBuilder();
        searchSourceBuilder.query(QueryBuilders.matchQuery("content", query));
        searchRequest.source(searchSourceBuilder);
        
        try {
            SearchResponse searchResponse = client.search(searchRequest, RequestOptions.DEFAULT);
            SearchHit[] hits = searchResponse.getHits().getHits();
            
            System.out.println("Search results for '" + query + "':");
            for (SearchHit hit : hits) {
                System.out.println("- " + hit.getSourceAsString());
            }
        } catch (IOException e) {
            System.err.println("Error searching documents: " + e.getMessage());
        }
    }
    
    // Faceted search
    public void facetedSearch(String indexName, String query, String facetField) {
        SearchRequest searchRequest = new SearchRequest(indexName);
        SearchSourceBuilder searchSourceBuilder = new SearchSourceBuilder();
        searchSourceBuilder.query(QueryBuilders.matchQuery("content", query));
        searchSourceBuilder.aggregation(AggregationBuilders.terms("facets").field(facetField));
        searchRequest.source(searchSourceBuilder);
        
        try {
            SearchResponse searchResponse = client.search(searchRequest, RequestOptions.DEFAULT);
            // Process faceted results
            System.out.println("Faceted search completed");
        } catch (IOException e) {
            System.err.println("Error in faceted search: " + e.getMessage());
        }
    }
}
```

## 10.8 NoSQL vs SQL Trade-offs

Understanding the trade-offs between NoSQL and SQL databases helps in choosing the right technology for specific use cases.

### NoSQL Advantages:
- **Scalability**: Better horizontal scaling
- **Flexibility**: Schema-less design
- **Performance**: Optimized for specific use cases
- **Cost**: Often more cost-effective for large scale
- **Development Speed**: Faster development cycles

### NoSQL Disadvantages:
- **Consistency**: Eventual consistency models
- **ACID Properties**: Limited ACID support
- **Query Complexity**: Limited query capabilities
- **Learning Curve**: New paradigms and tools
- **Maturity**: Less mature ecosystem

### Real-World Analogy:
NoSQL vs SQL is like choosing between different tools:
- **SQL** = Swiss Army knife (versatile, reliable)
- **NoSQL** = Specialized tools (optimized for specific tasks)
- **Trade-offs** = Versatility vs specialization

### Java Example - Technology Choice:
```java
public class DatabaseTechnologyChoice {
    
    // Choose database based on requirements
    public String chooseDatabase(Requirements requirements) {
        if (requirements.needsACID()) {
            return "SQL Database (PostgreSQL, MySQL)";
        }
        
        if (requirements.needsHorizontalScaling()) {
            return "NoSQL Database (MongoDB, Cassandra)";
        }
        
        if (requirements.needsComplexQueries()) {
            return "SQL Database (PostgreSQL, MySQL)";
        }
        
        if (requirements.needsHighPerformance()) {
            return "NoSQL Database (Redis, MongoDB)";
        }
        
        if (requirements.needsFlexibleSchema()) {
            return "NoSQL Database (MongoDB, CouchDB)";
        }
        
        return "SQL Database (default choice)";
    }
    
    // Requirements class
    public static class Requirements {
        private boolean needsACID;
        private boolean needsHorizontalScaling;
        private boolean needsComplexQueries;
        private boolean needsHighPerformance;
        private boolean needsFlexibleSchema;
        
        // Constructor and getters
        public Requirements(boolean needsACID, boolean needsHorizontalScaling, 
                          boolean needsComplexQueries, boolean needsHighPerformance, 
                          boolean needsFlexibleSchema) {
            this.needsACID = needsACID;
            this.needsHorizontalScaling = needsHorizontalScaling;
            this.needsComplexQueries = needsComplexQueries;
            this.needsHighPerformance = needsHighPerformance;
            this.needsFlexibleSchema = needsFlexibleSchema;
        }
        
        public boolean needsACID() { return needsACID; }
        public boolean needsHorizontalScaling() { return needsHorizontalScaling; }
        public boolean needsComplexQueries() { return needsComplexQueries; }
        public boolean needsHighPerformance() { return needsHighPerformance; }
        public boolean needsFlexibleSchema() { return needsFlexibleSchema; }
    }
}
```