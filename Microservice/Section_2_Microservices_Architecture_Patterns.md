# Section 2 – Microservices Architecture Patterns

## 2.1 Service Decomposition Patterns

Service decomposition is the process of breaking down a monolithic application into smaller, focused microservices. The goal is to identify natural boundaries and create services that are cohesive and loosely coupled.

### Decomposition Strategies:

#### 1. **Business Capability Decomposition**
Organize services around business capabilities rather than technical layers.

```java
// Good: Business capability decomposition
@Service
public class CustomerService {
    // Customer management, profiles, preferences
    public Customer createCustomer(CustomerRequest request) {
        // Customer-specific business logic
    }
}

@Service
public class OrderService {
    // Order processing, fulfillment, tracking
    public Order createOrder(OrderRequest request) {
        // Order-specific business logic
    }
}

@Service
public class PaymentService {
    // Payment processing, billing, invoicing
    public Payment processPayment(PaymentRequest request) {
        // Payment-specific business logic
    }
}
```

#### 2. **Domain-Driven Design Decomposition**
Use DDD concepts to identify bounded contexts and create services around them.

```java
// User Management Domain
@Entity
public class User {
    @Id
    private Long id;
    private String email;
    private String name;
    private UserProfile profile;
}

// Order Management Domain
@Entity
public class Order {
    @Id
    private Long id;
    private Long userId;
    private List<OrderItem> items;
    private OrderStatus status;
}

// Product Catalog Domain
@Entity
public class Product {
    @Id
    private Long id;
    private String name;
    private BigDecimal price;
    private ProductCategory category;
}
```

#### 3. **Data Decomposition**
Identify data ownership and create services around data boundaries.

```java
// User Data Service
@Repository
public class UserRepository {
    public User findById(Long id) {
        // User data access
    }
}

// Order Data Service
@Repository
public class OrderRepository {
    public Order findById(Long id) {
        // Order data access
    }
}

// Product Data Service
@Repository
public class ProductRepository {
    public Product findById(Long id) {
        // Product data access
    }
}
```

### Decomposition Guidelines:

#### 1. **Single Responsibility**
Each service should have one reason to change.

```java
// Good: Single responsibility
@Service
public class UserAuthenticationService {
    public boolean authenticateUser(String email, String password) {
        // Only handles authentication
    }
}

// Bad: Multiple responsibilities
@Service
public class UserManagementService {
    public boolean authenticateUser(String email, String password) {
        // Authentication
    }
    
    public void sendEmail(String to, String subject, String body) {
        // Email sending - should be separate service
    }
}
```

#### 2. **High Cohesion**
Related functionality should be grouped together.

```java
// Good: High cohesion
@Service
public class OrderService {
    public Order createOrder(OrderRequest request) {
        // Order creation
    }
    
    public Order updateOrder(Long id, OrderRequest request) {
        // Order updates
    }
    
    public Order cancelOrder(Long id) {
        // Order cancellation
    }
}
```

#### 3. **Loose Coupling**
Services should have minimal dependencies on each other.

```java
// Good: Loose coupling
@Service
public class OrderService {
    @Autowired
    private UserServiceClient userServiceClient;
    
    public Order createOrder(OrderRequest request) {
        // Only depends on user service for validation
        User user = userServiceClient.getUser(request.getUserId());
        // Process order
    }
}
```

## 2.2 Database per Service Pattern

The Database per Service pattern ensures that each microservice has its own database, providing data independence and preventing tight coupling between services.

### Benefits:

#### 1. **Data Independence**
Each service owns and controls its data.

#### 2. **Technology Diversity**
Different services can use different database technologies.

#### 3. **Scalability**
Each service can scale its database independently.

#### 4. **Fault Isolation**
Database failures are isolated to specific services.

### Implementation:

```java
// User Service - MySQL Database
@SpringBootApplication
public class UserServiceApplication {
    @Bean
    public DataSource userDataSource() {
        return DataSourceBuilder.create()
            .url("jdbc:mysql://localhost:3306/user_db")
            .username("user")
            .password("password")
            .build();
    }
}

// Order Service - PostgreSQL Database
@SpringBootApplication
public class OrderServiceApplication {
    @Bean
    public DataSource orderDataSource() {
        return DataSourceBuilder.create()
            .url("jdbc:postgresql://localhost:5432/order_db")
            .username("order")
            .password("password")
            .build();
    }
}

// Analytics Service - MongoDB Database
@SpringBootApplication
public class AnalyticsServiceApplication {
    @Bean
    public MongoTemplate mongoTemplate() {
        return new MongoTemplate(new MongoClient("localhost", 27017), "analytics_db");
    }
}
```

### Data Synchronization:

```java
// Event-driven data synchronization
@Service
public class UserService {
    @Autowired
    private UserRepository userRepository;
    
    @Autowired
    private EventPublisher eventPublisher;
    
    public User createUser(UserRequest request) {
        User user = userRepository.save(new User(request));
        
        // Publish event for other services
        eventPublisher.publishEvent(new UserCreatedEvent(user.getId(), user.getEmail()));
        
        return user;
    }
}

// Order Service listening to user events
@EventListener
public class OrderService {
    @Autowired
    private OrderRepository orderRepository;
    
    public void handleUserCreated(UserCreatedEvent event) {
        // Update local user cache or create user reference
        // No direct database access to user service
    }
}
```

### Challenges and Solutions:

#### 1. **Data Consistency**
Use eventual consistency and event-driven architecture.

```java
// Saga pattern for distributed transactions
@Service
public class OrderSaga {
    public void processOrder(OrderRequest request) {
        try {
            // Step 1: Reserve inventory
            inventoryService.reserveInventory(request.getProductId(), request.getQuantity());
            
            // Step 2: Process payment
            paymentService.processPayment(request.getPaymentInfo());
            
            // Step 3: Create order
            orderService.createOrder(request);
            
        } catch (Exception e) {
            // Compensate for completed steps
            compensateOrder(request);
        }
    }
}
```

#### 2. **Data Duplication**
Accept some data duplication for performance and independence.

```java
// User data in Order Service (denormalized)
@Entity
public class Order {
    @Id
    private Long id;
    private Long userId;
    private String userEmail; // Denormalized for performance
    private String userName;  // Denormalized for performance
    private List<OrderItem> items;
}
```

## 2.3 API Gateway Pattern

An API Gateway is a single entry point for all client requests to microservices. It handles cross-cutting concerns like authentication, routing, rate limiting, and monitoring.

### Benefits:

#### 1. **Single Entry Point**
Clients only need to know about one endpoint.

#### 2. **Cross-Cutting Concerns**
Centralized handling of authentication, logging, monitoring.

#### 3. **Protocol Translation**
Convert between different protocols (HTTP, gRPC, WebSocket).

#### 4. **Load Balancing**
Distribute requests across multiple service instances.

### Implementation with Spring Cloud Gateway:

```java
@SpringBootApplication
public class ApiGatewayApplication {
    public static void main(String[] args) {
        SpringApplication.run(ApiGatewayApplication.class, args);
    }
}

// Gateway configuration
@Configuration
public class GatewayConfig {
    @Bean
    public RouteLocator customRouteLocator(RouteLocatorBuilder builder) {
        return builder.routes()
            .route("user-service", r -> r.path("/api/users/**")
                .uri("lb://user-service"))
            .route("order-service", r -> r.path("/api/orders/**")
                .uri("lb://order-service"))
            .route("product-service", r -> r.path("/api/products/**")
                .uri("lb://product-service"))
            .build();
    }
}
```

### Authentication and Authorization:

```java
// JWT Authentication Filter
@Component
public class JwtAuthenticationFilter implements GatewayFilter {
    @Override
    public Mono<Void> filter(ServerWebExchange exchange, GatewayFilterChain chain) {
        String token = extractToken(exchange.getRequest());
        
        if (token != null && validateToken(token)) {
            // Add user info to headers
            exchange.getRequest().mutate()
                .header("X-User-Id", getUserIdFromToken(token))
                .build();
        }
        
        return chain.filter(exchange);
    }
}
```

### Rate Limiting:

```java
// Rate limiting configuration
@Configuration
public class RateLimitConfig {
    @Bean
    public RedisRateLimiter redisRateLimiter() {
        return new RedisRateLimiter(10, 20); // 10 requests per second, burst of 20
    }
}

// Apply rate limiting to routes
@Bean
public RouteLocator rateLimitedRoutes(RouteLocatorBuilder builder) {
    return builder.routes()
        .route("user-service", r -> r.path("/api/users/**")
            .filters(f -> f.requestRateLimiter(c -> c.setRateLimiter(redisRateLimiter())))
            .uri("lb://user-service"))
        .build();
}
```

### Monitoring and Logging:

```java
// Custom logging filter
@Component
public class LoggingFilter implements GatewayFilter {
    private static final Logger logger = LoggerFactory.getLogger(LoggingFilter.class);
    
    @Override
    public Mono<Void> filter(ServerWebExchange exchange, GatewayFilterChain chain) {
        ServerHttpRequest request = exchange.getRequest();
        
        logger.info("Request: {} {}", request.getMethod(), request.getURI());
        
        return chain.filter(exchange).then(Mono.fromRunnable(() -> {
            ServerHttpResponse response = exchange.getResponse();
            logger.info("Response: {}", response.getStatusCode());
        }));
    }
}
```

## 2.4 Backend for Frontend (BFF) Pattern

The Backend for Frontend pattern creates separate backend services tailored to specific client applications (web, mobile, desktop).

### Benefits:

#### 1. **Client-Specific Optimization**
Each BFF is optimized for its specific client needs.

#### 2. **Reduced Client Complexity**
Clients don't need to orchestrate multiple service calls.

#### 3. **Flexible Data Formatting**
Different clients can receive data in their preferred format.

#### 4. **Independent Evolution**
BFFs can evolve independently of the underlying services.

### Implementation:

```java
// Web BFF Service
@RestController
@RequestMapping("/api/web")
public class WebBffController {
    @Autowired
    private UserServiceClient userServiceClient;
    @Autowired
    private OrderServiceClient orderServiceClient;
    @Autowired
    private ProductServiceClient productServiceClient;
    
    @GetMapping("/dashboard")
    public WebDashboard getDashboard(@RequestParam Long userId) {
        // Aggregate data for web dashboard
        User user = userServiceClient.getUser(userId);
        List<Order> recentOrders = orderServiceClient.getRecentOrders(userId);
        List<Product> recommendedProducts = productServiceClient.getRecommendedProducts(userId);
        
        return WebDashboard.builder()
            .user(user)
            .recentOrders(recentOrders)
            .recommendedProducts(recommendedProducts)
            .build();
    }
}

// Mobile BFF Service
@RestController
@RequestMapping("/api/mobile")
public class MobileBffController {
    @Autowired
    private UserServiceClient userServiceClient;
    @Autowired
    private OrderServiceClient orderServiceClient;
    
    @GetMapping("/dashboard")
    public MobileDashboard getDashboard(@RequestParam Long userId) {
        // Simplified data for mobile
        User user = userServiceClient.getUser(userId);
        List<Order> recentOrders = orderServiceClient.getRecentOrders(userId);
        
        return MobileDashboard.builder()
            .user(user)
            .recentOrders(recentOrders)
            .build();
    }
}
```

### Data Aggregation:

```java
// BFF Service for complex data aggregation
@Service
public class OrderBffService {
    @Autowired
    private OrderServiceClient orderServiceClient;
    @Autowired
    private ProductServiceClient productServiceClient;
    @Autowired
    private UserServiceClient userServiceClient;
    
    public OrderDetails getOrderDetails(Long orderId) {
        Order order = orderServiceClient.getOrder(orderId);
        User user = userServiceClient.getUser(order.getUserId());
        
        List<OrderItemDetails> itemDetails = order.getItems().stream()
            .map(item -> {
                Product product = productServiceClient.getProduct(item.getProductId());
                return OrderItemDetails.builder()
                    .product(product)
                    .quantity(item.getQuantity())
                    .price(item.getPrice())
                    .build();
            })
            .collect(Collectors.toList());
        
        return OrderDetails.builder()
            .order(order)
            .user(user)
            .items(itemDetails)
            .build();
    }
}
```

## 2.5 Strangler Fig Pattern

The Strangler Fig pattern is used to gradually migrate from a monolithic application to microservices by gradually replacing functionality.

### Implementation Strategy:

#### 1. **Identify Extractable Functionality**
Find self-contained modules that can be extracted.

```java
// Original monolith
@RestController
public class MonolithController {
    @Autowired
    private UserService userService;
    @Autowired
    private OrderService orderService;
    @Autowired
    private ProductService productService;
    
    // Gradually extract services
}

// Step 1: Extract User Service
@RestController
public class UserController {
    @Autowired
    private UserService userService;
    
    // User-specific endpoints
}

// Step 2: Extract Order Service
@RestController
public class OrderController {
    @Autowired
    private OrderService orderService;
    
    // Order-specific endpoints
}
```

#### 2. **Create Facade**
Create a facade that routes requests to either the monolith or new services.

```java
// Strangler Fig Facade
@RestController
public class StranglerFigController {
    @Autowired
    private MonolithClient monolithClient;
    @Autowired
    private UserServiceClient userServiceClient;
    @Autowired
    private OrderServiceClient orderServiceClient;
    
    @GetMapping("/users/{id}")
    public ResponseEntity<User> getUser(@PathVariable Long id) {
        // Route to new user service
        return ResponseEntity.ok(userServiceClient.getUser(id));
    }
    
    @GetMapping("/orders/{id}")
    public ResponseEntity<Order> getOrder(@PathVariable Long id) {
        // Route to new order service
        return ResponseEntity.ok(orderServiceClient.getOrder(id));
    }
    
    @GetMapping("/products/{id}")
    public ResponseEntity<Product> getProduct(@PathVariable Long id) {
        // Still route to monolith
        return ResponseEntity.ok(monolithClient.getProduct(id));
    }
}
```

#### 3. **Gradual Migration**
Move functionality piece by piece.

```java
// Migration configuration
@Configuration
public class MigrationConfig {
    @Value("${migration.user-service.enabled:false}")
    private boolean userServiceEnabled;
    
    @Value("${migration.order-service.enabled:false}")
    private boolean orderServiceEnabled;
    
    @Bean
    public RoutingService routingService() {
        return new RoutingService(userServiceEnabled, orderServiceEnabled);
    }
}

// Routing service
@Service
public class RoutingService {
    private final boolean userServiceEnabled;
    private final boolean orderServiceEnabled;
    
    public boolean shouldRouteToUserService() {
        return userServiceEnabled;
    }
    
    public boolean shouldRouteToOrderService() {
        return orderServiceEnabled;
    }
}
```

## 2.6 Anti-Corruption Layer Pattern

The Anti-Corruption Layer pattern protects a new system from the complexities and inconsistencies of a legacy system by translating between the two systems.

### Implementation:

```java
// Legacy system interface
public interface LegacyUserService {
    LegacyUser getLegacyUser(String legacyId);
    void updateLegacyUser(String legacyId, LegacyUser user);
}

// New system interface
public interface UserService {
    User getUser(Long id);
    void updateUser(Long id, User user);
}

// Anti-corruption layer
@Service
public class UserAntiCorruptionLayer {
    @Autowired
    private LegacyUserService legacyUserService;
    @Autowired
    private UserService userService;
    
    public User getUser(Long id) {
        // Translate new system ID to legacy ID
        String legacyId = translateToLegacyId(id);
        
        // Call legacy system
        LegacyUser legacyUser = legacyUserService.getLegacyUser(legacyId);
        
        // Translate legacy response to new system format
        return translateToNewUser(legacyUser);
    }
    
    private String translateToLegacyId(Long id) {
        // Translation logic
        return "LEGACY_" + id;
    }
    
    private User translateToNewUser(LegacyUser legacyUser) {
        return User.builder()
            .id(translateFromLegacyId(legacyUser.getId()))
            .email(legacyUser.getEmailAddress())
            .name(legacyUser.getFullName())
            .build();
    }
}
```

### Data Translation:

```java
// Data translation service
@Service
public class DataTranslationService {
    public User translateLegacyUser(LegacyUser legacyUser) {
        return User.builder()
            .id(legacyUser.getId())
            .email(legacyUser.getEmailAddress())
            .name(legacyUser.getFullName())
            .profile(translateProfile(legacyUser.getProfile()))
            .build();
    }
    
    public Order translateLegacyOrder(LegacyOrder legacyOrder) {
        return Order.builder()
            .id(legacyOrder.getId())
            .userId(legacyOrder.getCustomerId())
            .items(translateOrderItems(legacyOrder.getItems()))
            .status(translateOrderStatus(legacyOrder.getStatus()))
            .build();
    }
}
```

## 2.7 Bulkhead Pattern

The Bulkhead pattern isolates critical resources to prevent cascading failures. It's named after the watertight compartments in ships.

### Implementation:

```java
// Thread pool isolation
@Configuration
public class ThreadPoolConfig {
    @Bean("userServiceExecutor")
    public Executor userServiceExecutor() {
        return new ThreadPoolTaskExecutor() {{
            setCorePoolSize(10);
            setMaxPoolSize(20);
            setQueueCapacity(100);
            setThreadNamePrefix("user-service-");
        }};
    }
    
    @Bean("orderServiceExecutor")
    public Executor orderServiceExecutor() {
        return new ThreadPoolTaskExecutor() {{
            setCorePoolSize(5);
            setMaxPoolSize(10);
            setQueueCapacity(50);
            setThreadNamePrefix("order-service-");
        }};
    }
}

// Service with isolated thread pool
@Service
public class UserService {
    @Autowired
    @Qualifier("userServiceExecutor")
    private Executor executor;
    
    public CompletableFuture<User> getUserAsync(Long id) {
        return CompletableFuture.supplyAsync(() -> {
            // User service logic
            return userRepository.findById(id);
        }, executor);
    }
}
```

### Database Connection Isolation:

```java
// Database connection pools
@Configuration
public class DatabaseConfig {
    @Bean("userDataSource")
    public DataSource userDataSource() {
        return DataSourceBuilder.create()
            .url("jdbc:mysql://localhost:3306/user_db")
            .username("user")
            .password("password")
            .build();
    }
    
    @Bean("orderDataSource")
    public DataSource orderDataSource() {
        return DataSourceBuilder.create()
            .url("jdbc:postgresql://localhost:5432/order_db")
            .username("order")
            .password("password")
            .build();
    }
}

// Service with isolated database
@Service
public class UserService {
    @Autowired
    @Qualifier("userDataSource")
    private DataSource dataSource;
    
    public User getUser(Long id) {
        // Use isolated database connection
        return userRepository.findById(id);
    }
}
```

## 2.8 Circuit Breaker Pattern

The Circuit Breaker pattern prevents cascading failures by monitoring service calls and opening the circuit when failures exceed a threshold.

### Implementation with Hystrix:

```java
// Circuit breaker configuration
@Configuration
public class CircuitBreakerConfig {
    @Bean
    public HystrixCommandProperties hystrixCommandProperties() {
        return HystrixCommandProperties.Setter()
            .withCircuitBreakerRequestVolumeThreshold(10)
            .withCircuitBreakerErrorThresholdPercentage(50)
            .withCircuitBreakerSleepWindowInMilliseconds(5000)
            .withExecutionTimeoutInMilliseconds(3000);
    }
}

// Service with circuit breaker
@Service
public class UserService {
    @Autowired
    private UserRepository userRepository;
    
    @HystrixCommand(fallbackMethod = "getUserFallback")
    public User getUser(Long id) {
        // Simulate potential failure
        if (Math.random() < 0.3) {
            throw new RuntimeException("Service temporarily unavailable");
        }
        return userRepository.findById(id);
    }
    
    public User getUserFallback(Long id) {
        // Fallback response
        return User.builder()
            .id(id)
            .name("Unknown User")
            .email("unknown@example.com")
            .build();
    }
}
```

### Circuit Breaker States:

```java
// Circuit breaker state management
@Component
public class CircuitBreakerService {
    private final CircuitBreaker circuitBreaker;
    
    public CircuitBreakerService() {
        this.circuitBreaker = CircuitBreaker.ofDefaults("userService");
    }
    
    public User getUser(Long id) {
        return circuitBreaker.executeSupplier(() -> {
            // Service call
            return userRepository.findById(id);
        });
    }
    
    public User getUserWithFallback(Long id) {
        return circuitBreaker.executeSupplier(() -> {
            // Service call
            return userRepository.findById(id);
        }).recover(throwable -> {
            // Fallback logic
            return User.builder()
                .id(id)
                .name("Fallback User")
                .build();
        });
    }
}
```

### Monitoring Circuit Breaker:

```java
// Circuit breaker metrics
@Component
public class CircuitBreakerMetrics {
    private final MeterRegistry meterRegistry;
    
    public CircuitBreakerMetrics(MeterRegistry meterRegistry) {
        this.meterRegistry = meterRegistry;
    }
    
    @EventListener
    public void handleCircuitBreakerStateChange(CircuitBreakerStateChangeEvent event) {
        Gauge.builder("circuit.breaker.state")
            .tag("name", event.getCircuitBreakerName())
            .register(meterRegistry, () -> event.getState().ordinal());
    }
}
```

This comprehensive guide covers all the essential microservices architecture patterns, providing both theoretical understanding and practical implementation examples. Each pattern is explained with real-world analogies and Java code examples to make the concepts clear and actionable.