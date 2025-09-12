# Section 15 – Error Handling & Resilience

## 15.1 Circuit Breaker Pattern

The Circuit Breaker pattern prevents cascading failures by monitoring service calls and opening the circuit when failures exceed a threshold.

### Circuit Breaker Implementation:

```java
// Circuit Breaker Service
@Service
public class CircuitBreakerService {
    private final Map<String, CircuitBreaker> circuitBreakers = new ConcurrentHashMap<>();
    
    public <T> T execute(String serviceName, Supplier<T> operation, Supplier<T> fallback) {
        CircuitBreaker circuitBreaker = getOrCreateCircuitBreaker(serviceName);
        
        return circuitBreaker.executeSupplier(() -> {
            try {
                return operation.get();
            } catch (Exception e) {
                throw new ServiceException("Service call failed", e);
            }
        }).recover(throwable -> {
            log.warn("Circuit breaker fallback triggered for service: {}", serviceName);
            return fallback.get();
        });
    }
    
    private CircuitBreaker getOrCreateCircuitBreaker(String serviceName) {
        return circuitBreakers.computeIfAbsent(serviceName, name -> 
            CircuitBreaker.ofDefaults(name)
                .toBuilder()
                .failureRateThreshold(50)
                .waitDurationInOpenState(Duration.ofSeconds(30))
                .slidingWindowSize(10)
                .minimumNumberOfCalls(5)
                .build()
        );
    }
}

// Usage
@Service
public class UserService {
    @Autowired
    private CircuitBreakerService circuitBreakerService;
    @Autowired
    private UserServiceClient userServiceClient;
    
    public User getUser(Long id) {
        return circuitBreakerService.execute("user-service", 
            () -> userServiceClient.getUser(id),
            () -> User.builder()
                .id(id)
                .name("Unknown User")
                .email("unknown@example.com")
                .build()
        );
    }
}
```

## 15.2 Retry Patterns

Retry patterns handle transient failures by automatically retrying failed operations.

### Exponential Backoff Retry:

```java
// Retry Service
@Service
public class RetryService {
    private final Map<String, Retry> retries = new ConcurrentHashMap<>();
    
    public <T> T executeWithRetry(String operationName, Supplier<T> operation) {
        Retry retry = getOrCreateRetry(operationName);
        
        return retry.executeSupplier(() -> {
            try {
                return operation.get();
            } catch (Exception e) {
                throw new RetryableException("Operation failed", e);
            }
        });
    }
    
    private Retry getOrCreateRetry(String operationName) {
        return retries.computeIfAbsent(operationName, name -> 
            Retry.of(name)
                .toBuilder()
                .maxAttempts(3)
                .waitDuration(Duration.ofSeconds(1))
                .exponentialBackoff(2.0, Duration.ofSeconds(1), Duration.ofSeconds(10))
                .retryOnException(throwable -> throwable instanceof RetryableException)
                .build()
        );
    }
}

// Usage
@Service
public class OrderService {
    @Autowired
    private RetryService retryService;
    @Autowired
    private PaymentServiceClient paymentServiceClient;
    
    public Payment processPayment(PaymentRequest request) {
        return retryService.executeWithRetry("process-payment", 
            () -> paymentServiceClient.processPayment(request)
        );
    }
}
```

## 15.3 Timeout Patterns

Timeout patterns prevent operations from hanging indefinitely.

### Timeout Service:

```java
// Timeout Service
@Service
public class TimeoutService {
    private final ExecutorService executorService = Executors.newCachedThreadPool();
    
    public <T> T executeWithTimeout(String operationName, Supplier<T> operation, Duration timeout) {
        CompletableFuture<T> future = CompletableFuture.supplyAsync(operation, executorService);
        
        try {
            return future.get(timeout.toMillis(), TimeUnit.MILLISECONDS);
        } catch (TimeoutException e) {
            future.cancel(true);
            throw new TimeoutException("Operation timed out: " + operationName);
        } catch (Exception e) {
            throw new RuntimeException("Operation failed: " + operationName, e);
        }
    }
    
    public <T> T executeWithTimeoutAndFallback(String operationName, Supplier<T> operation, 
                                             Supplier<T> fallback, Duration timeout) {
        try {
            return executeWithTimeout(operationName, operation, timeout);
        } catch (TimeoutException e) {
            log.warn("Operation timed out, using fallback: {}", operationName);
            return fallback.get();
        }
    }
}

// Usage
@Service
public class UserService {
    @Autowired
    private TimeoutService timeoutService;
    @Autowired
    private UserServiceClient userServiceClient;
    
    public User getUser(Long id) {
        return timeoutService.executeWithTimeoutAndFallback(
            "get-user",
            () -> userServiceClient.getUser(id),
            () -> User.builder()
                .id(id)
                .name("Unknown User")
                .email("unknown@example.com")
                .build(),
            Duration.ofSeconds(5)
        );
    }
}
```

## 15.4 Bulkhead Pattern

The Bulkhead pattern isolates critical resources to prevent cascading failures.

### Thread Pool Isolation:

```java
// Bulkhead Service
@Service
public class BulkheadService {
    private final ExecutorService userServiceExecutor;
    private final ExecutorService orderServiceExecutor;
    private final ExecutorService paymentServiceExecutor;
    
    public BulkheadService() {
        this.userServiceExecutor = createExecutor("user-service", 10, 20);
        this.orderServiceExecutor = createExecutor("order-service", 5, 10);
        this.paymentServiceExecutor = createExecutor("payment-service", 3, 5);
    }
    
    private ExecutorService createExecutor(String name, int corePoolSize, int maxPoolSize) {
        ThreadPoolTaskExecutor executor = new ThreadPoolTaskExecutor();
        executor.setCorePoolSize(corePoolSize);
        executor.setMaxPoolSize(maxPoolSize);
        executor.setQueueCapacity(100);
        executor.setThreadNamePrefix(name + "-");
        executor.setRejectedExecutionHandler(new ThreadPoolExecutor.CallerRunsPolicy());
        executor.initialize();
        return executor;
    }
    
    public CompletableFuture<User> executeUserOperation(Supplier<User> operation) {
        return CompletableFuture.supplyAsync(operation, userServiceExecutor);
    }
    
    public CompletableFuture<Order> executeOrderOperation(Supplier<Order> operation) {
        return CompletableFuture.supplyAsync(operation, orderServiceExecutor);
    }
    
    public CompletableFuture<Payment> executePaymentOperation(Supplier<Payment> operation) {
        return CompletableFuture.supplyAsync(operation, paymentServiceExecutor);
    }
}
```

### Database Connection Isolation:

```java
// Database Bulkhead
@Configuration
public class DatabaseBulkheadConfig {
    @Bean("userDataSource")
    public DataSource userDataSource() {
        HikariConfig config = new HikariConfig();
        config.setJdbcUrl("jdbc:mysql://localhost:3306/user_db");
        config.setUsername("user");
        config.setPassword("password");
        config.setMaximumPoolSize(10);
        config.setMinimumIdle(2);
        return new HikariDataSource(config);
    }
    
    @Bean("orderDataSource")
    public DataSource orderDataSource() {
        HikariConfig config = new HikariConfig();
        config.setJdbcUrl("jdbc:postgresql://localhost:5432/order_db");
        config.setUsername("order");
        config.setPassword("password");
        config.setMaximumPoolSize(5);
        config.setMinimumIdle(1);
        return new HikariDataSource(config);
    }
}
```

## 15.5 Graceful Degradation

Graceful degradation ensures that the system continues to function even when some services are unavailable.

### Graceful Degradation Service:

```java
// Graceful Degradation Service
@Service
public class GracefulDegradationService {
    @Autowired
    private UserServiceClient userServiceClient;
    @Autowired
    private OrderServiceClient orderServiceClient;
    @Autowired
    private PaymentServiceClient paymentServiceClient;
    
    public Order createOrder(OrderRequest request) {
        Order order = new Order(request);
        
        // Try to get user information, but don't fail if unavailable
        try {
            User user = userServiceClient.getUser(request.getUserId());
            order.setUserName(user.getName());
            order.setUserEmail(user.getEmail());
        } catch (Exception e) {
            log.warn("Failed to get user information, using fallback", e);
            order.setUserName("Unknown User");
            order.setUserEmail("unknown@example.com");
        }
        
        // Try to process payment, but don't fail if unavailable
        try {
            Payment payment = paymentServiceClient.processPayment(request.getPaymentInfo());
            order.setPaymentId(payment.getId());
            order.setStatus(OrderStatus.CONFIRMED);
        } catch (Exception e) {
            log.warn("Failed to process payment, marking order as pending", e);
            order.setStatus(OrderStatus.PENDING);
        }
        
        return order;
    }
}
```

## 15.6 Fallback Mechanisms

Fallback mechanisms provide alternative behavior when primary services are unavailable.

### Fallback Service:

```java
// Fallback Service
@Service
public class FallbackService {
    @Autowired
    private UserRepository userRepository;
    @Autowired
    private CacheService cacheService;
    
    public User getUserFallback(Long id) {
        // Try cache first
        User cachedUser = cacheService.get("user:" + id, User.class);
        if (cachedUser != null) {
            return cachedUser;
        }
        
        // Try database
        try {
            User user = userRepository.findById(id).orElse(null);
            if (user != null) {
                cacheService.put("user:" + id, user, Duration.ofMinutes(30));
                return user;
            }
        } catch (Exception e) {
            log.warn("Database unavailable, using default user", e);
        }
        
        // Return default user
        return User.builder()
            .id(id)
            .name("Unknown User")
            .email("unknown@example.com")
            .status(UserStatus.ACTIVE)
            .build();
    }
    
    public List<Order> getOrdersFallback(Long userId) {
        // Try cache first
        List<Order> cachedOrders = cacheService.get("orders:" + userId, List.class);
        if (cachedOrders != null) {
            return cachedOrders;
        }
        
        // Return empty list as fallback
        return Collections.emptyList();
    }
}
```

## 15.7 Error Propagation

Error propagation ensures that errors are properly handled and propagated through the system.

### Error Propagation Service:

```java
// Error Propagation Service
@Service
public class ErrorPropagationService {
    @Autowired
    private ErrorRepository errorRepository;
    @Autowired
    private NotificationService notificationService;
    
    public <T> T handleError(String operation, Supplier<T> operation, Supplier<T> fallback) {
        try {
            return operation.get();
        } catch (Exception e) {
            Error error = Error.builder()
                .operation(operation)
                .errorType(e.getClass().getSimpleName())
                .errorMessage(e.getMessage())
                .stackTrace(getStackTrace(e))
                .timestamp(Instant.now())
                .build();
            
            errorRepository.save(error);
            
            // Notify administrators
            notificationService.notifyError(error);
            
            // Return fallback if available
            if (fallback != null) {
                return fallback.get();
            }
            
            throw new ServiceException("Operation failed: " + operation, e);
        }
    }
    
    private String getStackTrace(Exception e) {
        StringWriter sw = new StringWriter();
        PrintWriter pw = new PrintWriter(sw);
        e.printStackTrace(pw);
        return sw.toString();
    }
}
```

## 15.8 Resilience Testing

Resilience testing verifies that the system can handle failures gracefully.

### Chaos Engineering Test:

```java
// Chaos Engineering Test
@SpringBootTest
class ResilienceTest {
    @Autowired
    private TestRestTemplate restTemplate;
    
    @Test
    void shouldHandleServiceFailure() {
        // Simulate service failure
        mockServer.when(requestTo("/api/users/1"))
            .respond(withStatus(HttpStatus.SERVICE_UNAVAILABLE));
        
        // Make request
        ResponseEntity<String> response = restTemplate.getForEntity("/api/users/1", String.class);
        
        // Verify fallback behavior
        assertThat(response.getStatusCode()).isEqualTo(HttpStatus.OK);
        assertThat(response.getBody()).contains("Unknown User");
    }
    
    @Test
    void shouldHandleTimeout() {
        // Simulate slow response
        mockServer.when(requestTo("/api/users/1"))
            .respond(withStatus(HttpStatus.OK)
                .withFixedDelay(10000)); // 10 second delay
        
        // Make request with timeout
        ResponseEntity<String> response = restTemplate.getForEntity("/api/users/1", String.class);
        
        // Verify timeout handling
        assertThat(response.getStatusCode()).isEqualTo(HttpStatus.OK);
        assertThat(response.getBody()).contains("Unknown User");
    }
}
```

### Resilience Metrics:

```java
// Resilience Metrics
@Component
public class ResilienceMetrics {
    private final MeterRegistry meterRegistry;
    private final Counter circuitBreakerOpens;
    private final Counter retryAttempts;
    private final Counter timeoutCount;
    private final Counter fallbackExecutions;
    
    public ResilienceMetrics(MeterRegistry meterRegistry) {
        this.meterRegistry = meterRegistry;
        this.circuitBreakerOpens = Counter.builder("resilience.circuit.breaker.opens")
            .description("Number of circuit breaker opens")
            .register(meterRegistry);
        this.retryAttempts = Counter.builder("resilience.retry.attempts")
            .description("Number of retry attempts")
            .register(meterRegistry);
        this.timeoutCount = Counter.builder("resilience.timeout.count")
            .description("Number of timeouts")
            .register(meterRegistry);
        this.fallbackExecutions = Counter.builder("resilience.fallback.executions")
            .description("Number of fallback executions")
            .register(meterRegistry);
    }
    
    public void recordCircuitBreakerOpen(String serviceName) {
        circuitBreakerOpens.increment(Tags.of("service", serviceName));
    }
    
    public void recordRetryAttempt(String operationName) {
        retryAttempts.increment(Tags.of("operation", operationName));
    }
    
    public void recordTimeout(String operationName) {
        timeoutCount.increment(Tags.of("operation", operationName));
    }
    
    public void recordFallbackExecution(String operationName) {
        fallbackExecutions.increment(Tags.of("operation", operationName));
    }
}
```

This comprehensive guide covers all aspects of error handling and resilience in microservices, providing both theoretical understanding and practical implementation examples.