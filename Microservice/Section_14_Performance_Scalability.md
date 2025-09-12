# Section 14 – Performance & Scalability

## 14.1 Performance Optimization Strategies

Performance optimization ensures that microservices can handle high loads efficiently.

### Caching Strategies:

```java
// Redis Caching
@Service
public class UserService {
    @Autowired
    private UserRepository userRepository;
    @Autowired
    private RedisTemplate<String, User> redisTemplate;
    
    private static final String USER_CACHE_KEY = "user:";
    private static final Duration CACHE_TTL = Duration.ofMinutes(30);
    
    public User getUser(Long id) {
        String cacheKey = USER_CACHE_KEY + id;
        
        // Try to get from cache
        User cachedUser = redisTemplate.opsForValue().get(cacheKey);
        if (cachedUser != null) {
            return cachedUser;
        }
        
        // Get from database
        User user = userRepository.findById(id)
            .orElseThrow(() -> new UserNotFoundException("User not found: " + id));
        
        // Cache the result
        redisTemplate.opsForValue().set(cacheKey, user, CACHE_TTL);
        
        return user;
    }
    
    public void updateUser(Long id, UserRequest request) {
        User user = userRepository.findById(id)
            .orElseThrow(() -> new UserNotFoundException("User not found: " + id));
        
        user.setName(request.getName());
        user.setEmail(request.getEmail());
        
        User updatedUser = userRepository.save(user);
        
        // Update cache
        String cacheKey = USER_CACHE_KEY + id;
        redisTemplate.opsForValue().set(cacheKey, updatedUser, CACHE_TTL);
    }
}
```

### Database Optimization:

```java
// Database Optimization
@Repository
public class UserRepository extends JpaRepository<User, Long> {
    
    @Query("SELECT u FROM User u WHERE u.email = :email")
    Optional<User> findByEmail(@Param("email") String email);
    
    @Query("SELECT u FROM User u WHERE u.status = :status")
    List<User> findByStatus(@Param("status") UserStatus status);
    
    @Query(value = "SELECT * FROM users WHERE created_at >= :startDate", nativeQuery = true)
    List<User> findRecentUsers(@Param("startDate") LocalDateTime startDate);
    
    @Modifying
    @Query("UPDATE User u SET u.lastLoginAt = :lastLoginAt WHERE u.id = :id")
    void updateLastLogin(@Param("id") Long id, @Param("lastLoginAt") Instant lastLoginAt);
}
```

## 14.2 Caching Strategies

Caching improves performance by storing frequently accessed data in memory.

### Multi-Level Caching:

```java
// Multi-Level Caching
@Service
public class CachingService {
    @Autowired
    private RedisTemplate<String, Object> redisTemplate;
    
    private final Map<String, Object> localCache = new ConcurrentHashMap<>();
    private final Duration localCacheTtl = Duration.ofMinutes(5);
    
    public <T> T get(String key, Class<T> type, Supplier<T> loader) {
        // Level 1: Local cache
        T localValue = (T) localCache.get(key);
        if (localValue != null) {
            return localValue;
        }
        
        // Level 2: Redis cache
        T redisValue = (T) redisTemplate.opsForValue().get(key);
        if (redisValue != null) {
            localCache.put(key, redisValue);
            return redisValue;
        }
        
        // Level 3: Database
        T dbValue = loader.get();
        if (dbValue != null) {
            redisTemplate.opsForValue().set(key, dbValue, Duration.ofMinutes(30));
            localCache.put(key, dbValue);
        }
        
        return dbValue;
    }
}
```

### Cache Invalidation:

```java
// Cache Invalidation
@Service
public class CacheInvalidationService {
    @Autowired
    private RedisTemplate<String, Object> redisTemplate;
    
    public void invalidateUserCache(Long userId) {
        String userKey = "user:" + userId;
        redisTemplate.delete(userKey);
        
        // Invalidate related caches
        redisTemplate.delete("user:orders:" + userId);
        redisTemplate.delete("user:profile:" + userId);
    }
    
    public void invalidatePattern(String pattern) {
        Set<String> keys = redisTemplate.keys(pattern);
        if (!keys.isEmpty()) {
            redisTemplate.delete(keys);
        }
    }
}
```

## 14.3 Database Optimization

Database optimization improves query performance and reduces latency.

### Connection Pooling:

```java
// Connection Pool Configuration
@Configuration
public class DatabaseConfig {
    @Bean
    public DataSource dataSource() {
        HikariConfig config = new HikariConfig();
        config.setJdbcUrl("jdbc:mysql://localhost:3306/user_db");
        config.setUsername("user");
        config.setPassword("password");
        config.setMaximumPoolSize(20);
        config.setMinimumIdle(5);
        config.setConnectionTimeout(30000);
        config.setIdleTimeout(600000);
        config.setMaxLifetime(1800000);
        config.setLeakDetectionThreshold(60000);
        
        return new HikariDataSource(config);
    }
}
```

### Query Optimization:

```java
// Query Optimization
@Repository
public class OptimizedUserRepository {
    @Autowired
    private JdbcTemplate jdbcTemplate;
    
    public List<User> findUsersWithPagination(int offset, int limit) {
        String sql = "SELECT id, email, name, status, created_at FROM users " +
                    "WHERE status = 'ACTIVE' " +
                    "ORDER BY created_at DESC " +
                    "LIMIT ? OFFSET ?";
        
        return jdbcTemplate.query(sql, new Object[]{limit, offset}, (rs, rowNum) -> {
            User user = new User();
            user.setId(rs.getLong("id"));
            user.setEmail(rs.getString("email"));
            user.setName(rs.getString("name"));
            user.setStatus(UserStatus.valueOf(rs.getString("status")));
            user.setCreatedAt(rs.getTimestamp("created_at").toInstant());
            return user;
        });
    }
    
    public List<User> findUsersByStatus(UserStatus status) {
        String sql = "SELECT id, email, name, status, created_at FROM users " +
                    "WHERE status = ? " +
                    "ORDER BY created_at DESC";
        
        return jdbcTemplate.query(sql, new Object[]{status.name()}, (rs, rowNum) -> {
            User user = new User();
            user.setId(rs.getLong("id"));
            user.setEmail(rs.getString("email"));
            user.setName(rs.getString("name"));
            user.setStatus(UserStatus.valueOf(rs.getString("status")));
            user.setCreatedAt(rs.getTimestamp("created_at").toInstant());
            return user;
        });
    }
}
```

## 14.4 Asynchronous Processing

Asynchronous processing improves performance by handling time-consuming operations in the background.

### Async Service:

```java
// Async Service
@Service
public class AsyncUserService {
    @Autowired
    private UserRepository userRepository;
    @Autowired
    private EmailService emailService;
    @Autowired
    private AnalyticsService analyticsService;
    
    @Async
    public CompletableFuture<User> createUserAsync(UserRequest request) {
        User user = new User(request);
        User savedUser = userRepository.save(user);
        
        // Send welcome email asynchronously
        emailService.sendWelcomeEmailAsync(savedUser.getEmail(), savedUser.getName());
        
        // Track user registration asynchronously
        analyticsService.trackUserRegistrationAsync(savedUser.getId());
        
        return CompletableFuture.completedFuture(savedUser);
    }
    
    @Async
    public CompletableFuture<Void> processUserDataAsync(Long userId) {
        // Process user data in background
        User user = userRepository.findById(userId).orElse(null);
        if (user != null) {
            // Perform data processing
            processUserData(user);
        }
        return CompletableFuture.completedFuture(null);
    }
    
    private void processUserData(User user) {
        // Data processing logic
    }
}
```

### Message Queue Processing:

```java
// Message Queue Processing
@Component
public class UserEventProcessor {
    @Autowired
    private UserRepository userRepository;
    @Autowired
    private EmailService emailService;
    
    @RabbitListener(queues = "user.created.queue")
    public void handleUserCreated(UserCreatedEvent event) {
        // Process user created event
        User user = userRepository.findById(event.getUserId()).orElse(null);
        if (user != null) {
            emailService.sendWelcomeEmail(user.getEmail(), user.getName());
        }
    }
    
    @RabbitListener(queues = "user.updated.queue")
    public void handleUserUpdated(UserUpdatedEvent event) {
        // Process user updated event
        User user = userRepository.findById(event.getUserId()).orElse(null);
        if (user != null) {
            // Update user profile
            user.setName(event.getName());
            userRepository.save(user);
        }
    }
}
```

## 14.5 Resource Optimization

Resource optimization ensures efficient use of system resources.

### Memory Optimization:

```java
// Memory Optimization
@Service
public class MemoryOptimizedUserService {
    @Autowired
    private UserRepository userRepository;
    
    public List<User> getUsersOptimized(int page, int size) {
        Pageable pageable = PageRequest.of(page, size);
        Page<User> userPage = userRepository.findAll(pageable);
        
        // Process users in batches to avoid memory issues
        List<User> users = new ArrayList<>();
        for (User user : userPage.getContent()) {
            // Process user data
            User processedUser = processUser(user);
            users.add(processedUser);
        }
        
        return users;
    }
    
    private User processUser(User user) {
        // Process user data efficiently
        return user;
    }
}
```

### CPU Optimization:

```java
// CPU Optimization
@Service
public class CPUOptimizedService {
    @Autowired
    private UserRepository userRepository;
    
    public List<User> processUsersInParallel(List<Long> userIds) {
        return userIds.parallelStream()
            .map(this::processUser)
            .collect(Collectors.toList());
    }
    
    private User processUser(Long userId) {
        User user = userRepository.findById(userId).orElse(null);
        if (user != null) {
            // Process user data
            processUserData(user);
        }
        return user;
    }
    
    private void processUserData(User user) {
        // CPU-intensive processing
    }
}
```

## 14.6 Auto-scaling Strategies

Auto-scaling automatically adjusts resources based on demand.

### Kubernetes HPA:

```yaml
# hpa.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: user-service-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: user-service
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

### Custom Metrics Scaling:

```yaml
# custom-hpa.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: user-service-custom-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: user-service
  minReplicas: 2
  maxReplicas: 20
  metrics:
  - type: Pods
    pods:
      metric:
        name: requests_per_second
      target:
        type: AverageValue
        averageValue: "100"
```

## 14.7 Load Balancing Techniques

Load balancing distributes traffic across multiple service instances.

### Round Robin Load Balancing:

```java
// Round Robin Load Balancer
@Component
public class RoundRobinLoadBalancer implements LoadBalancer {
    private final AtomicInteger counter = new AtomicInteger(0);
    
    @Override
    public ServiceInstance choose(List<ServiceInstance> instances) {
        if (instances.isEmpty()) {
            return null;
        }
        
        int index = counter.getAndIncrement() % instances.size();
        return instances.get(index);
    }
}
```

### Weighted Load Balancing:

```java
// Weighted Load Balancer
@Component
public class WeightedLoadBalancer implements LoadBalancer {
    private final AtomicInteger counter = new AtomicInteger(0);
    
    @Override
    public ServiceInstance choose(List<ServiceInstance> instances) {
        if (instances.isEmpty()) {
            return null;
        }
        
        int totalWeight = instances.stream()
            .mapToInt(this::getWeight)
            .sum();
        
        if (totalWeight == 0) {
            return instances.get(counter.getAndIncrement() % instances.size());
        }
        
        int randomWeight = counter.getAndIncrement() % totalWeight;
        int currentWeight = 0;
        
        for (ServiceInstance instance : instances) {
            currentWeight += getWeight(instance);
            if (randomWeight < currentWeight) {
                return instance;
            }
        }
        
        return instances.get(instances.size() - 1);
    }
    
    private int getWeight(ServiceInstance instance) {
        String weightStr = instance.getMetadata().get("weight");
        return weightStr != null ? Integer.parseInt(weightStr) : 1;
    }
}
```

## 14.8 Performance Monitoring and Tuning

Performance monitoring helps identify bottlenecks and optimize performance.

### Performance Metrics:

```java
// Performance Metrics
@Component
public class PerformanceMetrics {
    private final MeterRegistry meterRegistry;
    private final Timer requestTimer;
    private final Counter requestCounter;
    private final Gauge activeConnectionsGauge;
    
    public PerformanceMetrics(MeterRegistry meterRegistry) {
        this.meterRegistry = meterRegistry;
        this.requestTimer = Timer.builder("http.requests")
            .description("HTTP request duration")
            .register(meterRegistry);
        this.requestCounter = Counter.builder("http.requests")
            .description("HTTP request count")
            .register(meterRegistry);
        this.activeConnectionsGauge = Gauge.builder("http.active.connections")
            .description("Active HTTP connections")
            .register(meterRegistry, this, PerformanceMetrics::getActiveConnections);
    }
    
    public void recordRequest(String method, String path, int statusCode, long duration) {
        requestTimer.record(duration, TimeUnit.MILLISECONDS);
        requestCounter.increment(
            Tags.of(
                "method", method,
                "path", path,
                "status", String.valueOf(statusCode)
            )
        );
    }
    
    private double getActiveConnections() {
        // Return actual active connections count
        return 50; // This would be calculated from actual data
    }
}
```

### Performance Tuning:

```java
// Performance Tuning
@Configuration
public class PerformanceTuningConfig {
    @Bean
    public ThreadPoolTaskExecutor taskExecutor() {
        ThreadPoolTaskExecutor executor = new ThreadPoolTaskExecutor();
        executor.setCorePoolSize(10);
        executor.setMaxPoolSize(20);
        executor.setQueueCapacity(100);
        executor.setThreadNamePrefix("async-");
        executor.setRejectedExecutionHandler(new ThreadPoolExecutor.CallerRunsPolicy());
        executor.initialize();
        return executor;
    }
    
    @Bean
    public RestTemplate restTemplate() {
        HttpComponentsClientHttpRequestFactory factory = new HttpComponentsClientHttpRequestFactory();
        factory.setConnectTimeout(5000);
        factory.setReadTimeout(10000);
        factory.setConnectionRequestTimeout(5000);
        
        return new RestTemplate(factory);
    }
}
```

This comprehensive guide covers all aspects of performance and scalability in microservices, providing both theoretical understanding and practical implementation examples.