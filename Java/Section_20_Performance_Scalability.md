# Section 20 - Performance & Scalability

## 20.1 JVM Tuning & Optimization

JVM tuning involves configuring the Java Virtual Machine for optimal performance based on application requirements.

### Core Concepts:

**1. Memory Management:**
- Heap size configuration
- Garbage collection tuning
- Memory allocation patterns
- Memory leak prevention

**2. GC Algorithms:**
- Serial GC
- Parallel GC
- G1 GC
- ZGC
- Shenandoah GC

**3. Performance Tuning:**
- JIT compilation
- HotSpot optimization
- Profiling and monitoring

### Example:

```java
// JVM Tuning Example
public class JVMTuningExample {
    
    public static void main(String[] args) {
        // Display JVM information
        displayJVMInfo();
        
        // Memory allocation test
        testMemoryAllocation();
        
        // GC performance test
        testGCPerformance();
    }
    
    public static void displayJVMInfo() {
        Runtime runtime = Runtime.getRuntime();
        
        System.out.println("=== JVM Information ===");
        System.out.println("Max Memory: " + runtime.maxMemory() / 1024 / 1024 + " MB");
        System.out.println("Total Memory: " + runtime.totalMemory() / 1024 / 1024 + " MB");
        System.out.println("Free Memory: " + runtime.freeMemory() / 1024 / 1024 + " MB");
        System.out.println("Available Processors: " + runtime.availableProcessors());
        
        // GC information
        List<GarbageCollectorMXBean> gcBeans = ManagementFactory.getGarbageCollectorMXBeans();
        for (GarbageCollectorMXBean gcBean : gcBeans) {
            System.out.println("GC: " + gcBean.getName() + 
                             " - Collections: " + gcBean.getCollectionCount() + 
                             " - Time: " + gcBean.getCollectionTime() + " ms");
        }
    }
    
    public static void testMemoryAllocation() {
        System.out.println("\n=== Memory Allocation Test ===");
        
        long startTime = System.currentTimeMillis();
        
        // Allocate large objects
        List<String> strings = new ArrayList<>();
        for (int i = 0; i < 100000; i++) {
            strings.add("String " + i + " " + "x".repeat(100));
        }
        
        long endTime = System.currentTimeMillis();
        System.out.println("Allocated 100,000 strings in " + (endTime - startTime) + " ms");
        
        // Force GC
        System.gc();
        
        // Check memory after GC
        Runtime runtime = Runtime.getRuntime();
        System.out.println("Memory after GC: " + 
                          (runtime.totalMemory() - runtime.freeMemory()) / 1024 / 1024 + " MB");
    }
    
    public static void testGCPerformance() {
        System.out.println("\n=== GC Performance Test ===");
        
        // Create objects to trigger GC
        for (int i = 0; i < 10; i++) {
            List<byte[]> data = new ArrayList<>();
            for (int j = 0; j < 1000; j++) {
                data.add(new byte[1024 * 1024]); // 1MB each
            }
            // Objects become eligible for GC
        }
        
        // Force GC and measure time
        long startTime = System.currentTimeMillis();
        System.gc();
        long endTime = System.currentTimeMillis();
        
        System.out.println("GC took " + (endTime - startTime) + " ms");
    }
}
```

### JVM Tuning Parameters:

```bash
# Basic JVM tuning
java -Xms512m -Xmx2g -XX:+UseG1GC MyApplication

# Advanced G1 GC tuning
java -Xms1g -Xmx4g \
     -XX:+UseG1GC \
     -XX:MaxGCPauseMillis=200 \
     -XX:G1HeapRegionSize=16m \
     -XX:G1NewSizePercent=30 \
     -XX:G1MaxNewSizePercent=40 \
     MyApplication

# ZGC tuning
java -Xms2g -Xmx8g \
     -XX:+UnlockExperimentalVMOptions \
     -XX:+UseZGC \
     -XX:+UnlockDiagnosticVMOptions \
     -XX:+LogVMOutput \
     MyApplication

# JIT compilation tuning
java -XX:+TieredCompilation \
     -XX:CompileThreshold=1000 \
     -XX:+PrintCompilation \
     MyApplication
```

### Real-world Analogy:
JVM tuning is like tuning a car engine - you adjust various parameters to get the best performance for your specific driving conditions.

## 20.2 Memory Profiling & Analysis

Memory profiling helps identify memory leaks, excessive memory usage, and optimization opportunities.

### Core Concepts:

**1. Memory Profiling Tools:**
- JVisualVM
- JProfiler
- Eclipse MAT
- YourKit
- Flight Recorder

**2. Common Memory Issues:**
- Memory leaks
- OutOfMemoryError
- Excessive object creation
- Inefficient data structures

### Example:

```java
// Memory profiling example
public class MemoryProfilingExample {
    
    private static final int OBJECT_COUNT = 1000000;
    
    public static void main(String[] args) {
        System.out.println("=== Memory Profiling Example ===");
        
        // Test 1: Object creation patterns
        testObjectCreation();
        
        // Test 2: Memory leak simulation
        testMemoryLeak();
        
        // Test 3: String concatenation
        testStringConcatenation();
        
        // Test 4: Collection usage
        testCollectionUsage();
    }
    
    public static void testObjectCreation() {
        System.out.println("\n=== Object Creation Test ===");
        
        long startTime = System.currentTimeMillis();
        List<String> strings = new ArrayList<>();
        
        for (int i = 0; i < OBJECT_COUNT; i++) {
            strings.add("String " + i);
        }
        
        long endTime = System.currentTimeMillis();
        System.out.println("Created " + OBJECT_COUNT + " strings in " + (endTime - startTime) + " ms");
        
        // Check memory usage
        Runtime runtime = Runtime.getRuntime();
        long usedMemory = runtime.totalMemory() - runtime.freeMemory();
        System.out.println("Memory used: " + usedMemory / 1024 / 1024 + " MB");
    }
    
    public static void testMemoryLeak() {
        System.out.println("\n=== Memory Leak Test ===");
        
        // Simulate memory leak with static collection
        List<byte[]> leakyList = new ArrayList<>();
        
        for (int i = 0; i < 1000; i++) {
            leakyList.add(new byte[1024 * 1024]); // 1MB each
        }
        
        System.out.println("Created 1000 1MB objects (potential memory leak)");
        
        // These objects won't be garbage collected because they're referenced by static list
        // In real applications, this would cause OutOfMemoryError
    }
    
    public static void testStringConcatenation() {
        System.out.println("\n=== String Concatenation Test ===");
        
        // Bad: String concatenation in loop
        long startTime = System.currentTimeMillis();
        String badResult = "";
        for (int i = 0; i < 10000; i++) {
            badResult += "item" + i; // Creates many temporary String objects
        }
        long endTime = System.currentTimeMillis();
        System.out.println("Bad concatenation time: " + (endTime - startTime) + " ms");
        
        // Good: StringBuilder
        startTime = System.currentTimeMillis();
        StringBuilder goodResult = new StringBuilder();
        for (int i = 0; i < 10000; i++) {
            goodResult.append("item").append(i);
        }
        endTime = System.currentTimeMillis();
        System.out.println("Good concatenation time: " + (endTime - startTime) + " ms");
    }
    
    public static void testCollectionUsage() {
        System.out.println("\n=== Collection Usage Test ===");
        
        // Test ArrayList vs LinkedList
        int size = 100000;
        
        // ArrayList test
        long startTime = System.currentTimeMillis();
        List<Integer> arrayList = new ArrayList<>();
        for (int i = 0; i < size; i++) {
            arrayList.add(i);
        }
        long endTime = System.currentTimeMillis();
        System.out.println("ArrayList add time: " + (endTime - startTime) + " ms");
        
        // LinkedList test
        startTime = System.currentTimeMillis();
        List<Integer> linkedList = new LinkedList<>();
        for (int i = 0; i < size; i++) {
            linkedList.add(i);
        }
        endTime = System.currentTimeMillis();
        System.out.println("LinkedList add time: " + (endTime - startTime) + " ms");
        
        // Random access test
        startTime = System.currentTimeMillis();
        for (int i = 0; i < 1000; i++) {
            arrayList.get(i * 100);
        }
        endTime = System.currentTimeMillis();
        System.out.println("ArrayList random access time: " + (endTime - startTime) + " ms");
        
        startTime = System.currentTimeMillis();
        for (int i = 0; i < 1000; i++) {
            linkedList.get(i * 100);
        }
        endTime = System.currentTimeMillis();
        System.out.println("LinkedList random access time: " + (endTime - startTime) + " ms");
    }
}

// Memory leak detection utility
public class MemoryLeakDetector {
    
    private static final Map<String, List<Object>> objectTracker = new HashMap<>();
    
    public static void trackObject(String category, Object obj) {
        objectTracker.computeIfAbsent(category, k -> new ArrayList<>()).add(obj);
    }
    
    public static void printMemoryStats() {
        Runtime runtime = Runtime.getRuntime();
        long totalMemory = runtime.totalMemory();
        long freeMemory = runtime.freeMemory();
        long usedMemory = totalMemory - freeMemory;
        
        System.out.println("=== Memory Stats ===");
        System.out.println("Total Memory: " + totalMemory / 1024 / 1024 + " MB");
        System.out.println("Used Memory: " + usedMemory / 1024 / 1024 + " MB");
        System.out.println("Free Memory: " + freeMemory / 1024 / 1024 + " MB");
        
        System.out.println("\n=== Object Tracking ===");
        for (Map.Entry<String, List<Object>> entry : objectTracker.entrySet()) {
            System.out.println(entry.getKey() + ": " + entry.getValue().size() + " objects");
        }
    }
}
```

### Real-world Analogy:
Memory profiling is like having a detailed energy audit of your house - it shows you exactly where energy (memory) is being used and wasted.

## 20.3 Caching Strategies

Caching improves application performance by storing frequently accessed data in fast storage.

### Core Concepts:

**1. Cache Types:**
- In-memory caches
- Distributed caches
- Database caches
- CDN caches

**2. Caching Patterns:**
- Cache-aside
- Write-through
- Write-behind
- Refresh-ahead

**3. Cache Eviction:**
- LRU (Least Recently Used)
- LFU (Least Frequently Used)
- TTL (Time To Live)
- Size-based eviction

### Example:

```java
// Spring Cache Example
@Service
public class UserService {
    
    @Autowired
    private UserRepository userRepository;
    
    @Cacheable(value = "users", key = "#id")
    public User findById(Long id) {
        System.out.println("Fetching user from database: " + id);
        return userRepository.findById(id).orElse(null);
    }
    
    @CacheEvict(value = "users", key = "#user.id")
    public User updateUser(User user) {
        System.out.println("Updating user: " + user.getId());
        return userRepository.save(user);
    }
    
    @CacheEvict(value = "users", allEntries = true)
    public void clearCache() {
        System.out.println("Clearing all user cache");
    }
}

// Redis Cache Example
@Service
public class ProductService {
    
    @Autowired
    private RedisTemplate<String, Object> redisTemplate;
    
    @Autowired
    private ProductRepository productRepository;
    
    public Product findById(Long id) {
        String cacheKey = "product:" + id;
        
        // Try to get from cache
        Product product = (Product) redisTemplate.opsForValue().get(cacheKey);
        
        if (product == null) {
            // Cache miss - fetch from database
            product = productRepository.findById(id).orElse(null);
            if (product != null) {
                // Store in cache with TTL
                redisTemplate.opsForValue().set(cacheKey, product, Duration.ofMinutes(30));
            }
        }
        
        return product;
    }
    
    public void updateProduct(Product product) {
        // Update database
        productRepository.save(product);
        
        // Update cache
        String cacheKey = "product:" + product.getId();
        redisTemplate.opsForValue().set(cacheKey, product, Duration.ofMinutes(30));
    }
    
    public void deleteProduct(Long id) {
        // Delete from database
        productRepository.deleteById(id);
        
        // Remove from cache
        String cacheKey = "product:" + id;
        redisTemplate.delete(cacheKey);
    }
}

// Custom Cache Implementation
public class LRUCache<K, V> {
    
    private final int capacity;
    private final Map<K, Node<K, V>> cache;
    private final Node<K, V> head;
    private final Node<K, V> tail;
    
    public LRUCache(int capacity) {
        this.capacity = capacity;
        this.cache = new HashMap<>();
        this.head = new Node<>(null, null);
        this.tail = new Node<>(null, null);
        head.next = tail;
        tail.prev = head;
    }
    
    public V get(K key) {
        Node<K, V> node = cache.get(key);
        if (node == null) {
            return null;
        }
        
        // Move to head
        moveToHead(node);
        return node.value;
    }
    
    public void put(K key, V value) {
        Node<K, V> node = cache.get(key);
        
        if (node != null) {
            // Update existing node
            node.value = value;
            moveToHead(node);
        } else {
            // Add new node
            Node<K, V> newNode = new Node<>(key, value);
            cache.put(key, newNode);
            addToHead(newNode);
            
            if (cache.size() > capacity) {
                // Remove least recently used
                Node<K, V> tail = removeTail();
                cache.remove(tail.key);
            }
        }
    }
    
    private void moveToHead(Node<K, V> node) {
        removeNode(node);
        addToHead(node);
    }
    
    private void addToHead(Node<K, V> node) {
        node.prev = head;
        node.next = head.next;
        head.next.prev = node;
        head.next = node;
    }
    
    private void removeNode(Node<K, V> node) {
        node.prev.next = node.next;
        node.next.prev = node.prev;
    }
    
    private Node<K, V> removeTail() {
        Node<K, V> lastNode = tail.prev;
        removeNode(lastNode);
        return lastNode;
    }
    
    private static class Node<K, V> {
        K key;
        V value;
        Node<K, V> prev;
        Node<K, V> next;
        
        Node(K key, V value) {
            this.key = key;
            this.value = value;
        }
    }
}
```

### Real-world Analogy:
Caching is like having a well-organized pantry - you keep frequently used items close at hand so you don't have to go to the store every time you need them.

## 20.4 Database Optimization

Database optimization improves query performance and reduces resource usage.

### Core Concepts:

**1. Query Optimization:**
- Index usage
- Query plan analysis
- Join optimization
- Subquery optimization

**2. Database Design:**
- Normalization
- Denormalization
- Partitioning
- Sharding

**3. Connection Management:**
- Connection pooling
- Connection timeout
- Transaction management

### Example:

```java
// Database optimization example
@Entity
@Table(name = "users", indexes = {
    @Index(name = "idx_email", columnList = "email"),
    @Index(name = "idx_name", columnList = "name"),
    @Index(name = "idx_created_at", columnList = "created_at")
})
public class User {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @Column(name = "email", unique = true, nullable = false)
    private String email;
    
    @Column(name = "name", nullable = false)
    private String name;
    
    @Column(name = "created_at")
    private LocalDateTime createdAt;
    
    // Getters and setters
}

@Repository
public class OptimizedUserRepository {
    
    @PersistenceContext
    private EntityManager entityManager;
    
    // Optimized query with proper indexing
    @Query("SELECT u FROM User u WHERE u.email = :email")
    public User findByEmail(@Param("email") String email) {
        return entityManager.createQuery(
            "SELECT u FROM User u WHERE u.email = :email", User.class)
            .setParameter("email", email)
            .getSingleResult();
    }
    
    // Pagination for large datasets
    @Query("SELECT u FROM User u ORDER BY u.createdAt DESC")
    public Page<User> findUsersWithPagination(Pageable pageable) {
        Query query = entityManager.createQuery(
            "SELECT u FROM User u ORDER BY u.createdAt DESC", User.class);
        
        query.setFirstResult(pageable.getPageNumber() * pageable.getPageSize());
        query.setMaxResults(pageable.getPageSize());
        
        List<User> users = query.getResultList();
        return new PageImpl<>(users, pageable, users.size());
    }
    
    // Batch operations
    @Modifying
    @Query("UPDATE User u SET u.name = :name WHERE u.id IN :ids")
    public int updateUsersInBatch(@Param("name") String name, @Param("ids") List<Long> ids) {
        return entityManager.createQuery(
            "UPDATE User u SET u.name = :name WHERE u.id IN :ids")
            .setParameter("name", name)
            .setParameter("ids", ids)
            .executeUpdate();
    }
}

// Connection pooling configuration
@Configuration
public class DatabaseConfig {
    
    @Bean
    public DataSource dataSource() {
        HikariConfig config = new HikariConfig();
        config.setJdbcUrl("jdbc:mysql://localhost:3306/myapp");
        config.setUsername("root");
        config.setPassword("password");
        
        // Connection pool settings
        config.setMaximumPoolSize(20);
        config.setMinimumIdle(5);
        config.setConnectionTimeout(30000);
        config.setIdleTimeout(600000);
        config.setMaxLifetime(1800000);
        config.setLeakDetectionThreshold(60000);
        
        return new HikariDataSource(config);
    }
    
    @Bean
    public JdbcTemplate jdbcTemplate(DataSource dataSource) {
        return new JdbcTemplate(dataSource);
    }
}
```

### Real-world Analogy:
Database optimization is like organizing a library - you create indexes (catalogs), arrange books efficiently, and use efficient search methods to find information quickly.

## 20.5 Load Balancing & Clustering

Load balancing distributes traffic across multiple servers to improve performance and availability.

### Core Concepts:

**1. Load Balancing Algorithms:**
- Round Robin
- Weighted Round Robin
- Least Connections
- IP Hash
- Least Response Time

**2. Clustering Types:**
- Horizontal scaling
- Vertical scaling
- Session clustering
- Data clustering

### Example:

```java
// Load balancer configuration
@Configuration
public class LoadBalancerConfig {
    
    @Bean
    @LoadBalanced
    public RestTemplate restTemplate() {
        return new RestTemplate();
    }
    
    @Bean
    public IRule loadBalancerRule() {
        return new RoundRobinRule();
    }
}

// Service discovery
@SpringBootApplication
@EnableEurekaClient
public class LoadBalancedApp {
    public static void main(String[] args) {
        SpringApplication.run(LoadBalancedApp.class, args);
    }
}

// Health check endpoint
@RestController
public class HealthController {
    
    @Value("${server.port}")
    private String port;
    
    @GetMapping("/health")
    public ResponseEntity<Map<String, String>> health() {
        Map<String, String> status = new HashMap<>();
        status.put("status", "UP");
        status.put("port", port);
        status.put("timestamp", LocalDateTime.now().toString());
        return ResponseEntity.ok(status);
    }
}

// Session clustering
@Configuration
@EnableRedisHttpSession
public class SessionConfig {
    
    @Bean
    public LettuceConnectionFactory connectionFactory() {
        return new LettuceConnectionFactory(
            new RedisStandaloneConfiguration("localhost", 6379));
    }
}
```

### Real-world Analogy:
Load balancing is like having multiple checkout lanes at a store - customers are distributed evenly to prevent any single lane from becoming overwhelmed.

## 20.6 Horizontal vs Vertical Scaling

Scaling strategies determine how to handle increased load and demand.

### Core Concepts:

**1. Vertical Scaling (Scale Up):**
- Increase server resources
- More CPU, RAM, storage
- Easier to implement
- Limited by hardware

**2. Horizontal Scaling (Scale Out):**
- Add more servers
- Distribute load across servers
- More complex to implement
- Virtually unlimited capacity

### Example:

```java
// Auto-scaling configuration
@Configuration
public class AutoScalingConfig {
    
    @Bean
    public MeterRegistry meterRegistry() {
        return new SimpleMeterRegistry();
    }
    
    @Bean
    public TimedAspect timedAspect(MeterRegistry registry) {
        return new TimedAspect(registry);
    }
}

// Performance monitoring
@Component
public class PerformanceMonitor {
    
    private final MeterRegistry meterRegistry;
    private final Counter requestCounter;
    private final Timer requestTimer;
    
    public PerformanceMonitor(MeterRegistry meterRegistry) {
        this.meterRegistry = meterRegistry;
        this.requestCounter = Counter.builder("http_requests_total")
            .description("Total HTTP requests")
            .register(meterRegistry);
        this.requestTimer = Timer.builder("http_request_duration")
            .description("HTTP request duration")
            .register(meterRegistry);
    }
    
    public void recordRequest(String endpoint) {
        requestCounter.increment(Tags.of("endpoint", endpoint));
    }
    
    public Timer.Sample startTimer() {
        return Timer.start(meterRegistry);
    }
    
    public void recordTimer(Timer.Sample sample, String endpoint) {
        sample.stop(Timer.builder("http_request_duration")
            .tag("endpoint", endpoint)
            .register(meterRegistry));
    }
}
```

### Real-world Analogy:
- **Vertical Scaling:** Like upgrading your car's engine to make it faster
- **Horizontal Scaling:** Like adding more lanes to a highway to handle more traffic

## 20.7 Performance Testing & Benchmarking

Performance testing ensures applications meet performance requirements under various conditions.

### Core Concepts:

**1. Performance Testing Types:**
- Load testing
- Stress testing
- Volume testing
- Spike testing
- Endurance testing

**2. Key Metrics:**
- Response time
- Throughput
- Resource utilization
- Error rate
- Concurrent users

### Example:

```java
// JMH Benchmarking example
@BenchmarkMode(Mode.AverageTime)
@OutputTimeUnit(TimeUnit.MICROSECONDS)
@State(Scope.Benchmark)
public class PerformanceBenchmark {
    
    private List<String> testData;
    
    @Setup
    public void setup() {
        testData = new ArrayList<>();
        for (int i = 0; i < 10000; i++) {
            testData.add("String " + i);
        }
    }
    
    @Benchmark
    public String stringConcatenation() {
        String result = "";
        for (String str : testData) {
            result += str;
        }
        return result;
    }
    
    @Benchmark
    public String stringBuilder() {
        StringBuilder result = new StringBuilder();
        for (String str : testData) {
            result.append(str);
        }
        return result.toString();
    }
    
    @Benchmark
    public String stringJoiner() {
        StringJoiner result = new StringJoiner("");
        for (String str : testData) {
            result.add(str);
        }
        return result.toString();
    }
}

// Load testing with JUnit
@SpringBootTest
public class LoadTest {
    
    @Autowired
    private TestRestTemplate restTemplate;
    
    @Test
    public void loadTest() throws InterruptedException {
        int numberOfThreads = 100;
        int requestsPerThread = 100;
        ExecutorService executor = Executors.newFixedThreadPool(numberOfThreads);
        CountDownLatch latch = new CountDownLatch(numberOfThreads);
        
        long startTime = System.currentTimeMillis();
        
        for (int i = 0; i < numberOfThreads; i++) {
            executor.submit(() -> {
                try {
                    for (int j = 0; j < requestsPerThread; j++) {
                        ResponseEntity<String> response = restTemplate.getForEntity(
                            "/api/users/1", String.class);
                        assertThat(response.getStatusCode()).isEqualTo(HttpStatus.OK);
                    }
                } finally {
                    latch.countDown();
                }
            });
        }
        
        latch.await();
        long endTime = System.currentTimeMillis();
        
        System.out.println("Total requests: " + (numberOfThreads * requestsPerThread));
        System.out.println("Total time: " + (endTime - startTime) + " ms");
        System.out.println("Requests per second: " + 
                          (numberOfThreads * requestsPerThread * 1000) / (endTime - startTime));
        
        executor.shutdown();
    }
}
```

### Real-world Analogy:
Performance testing is like stress-testing a bridge - you gradually increase the load to see how much it can handle before it breaks, ensuring it's safe for normal use.