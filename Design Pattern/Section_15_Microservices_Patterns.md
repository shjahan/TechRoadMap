# Section 15 - Microservices Patterns

## 15.1 Service Decomposition Patterns

Service decomposition patterns help break down monolithic applications into smaller, focused microservices.

### When to Use:
- When you want to break down a monolithic application
- When you need to scale different parts of your system independently
- When you want to improve maintainability and deployment

### Real-World Analogy:
Think of a large department store that decides to split into specialized shops (electronics, clothing, books) - each shop can operate independently and focus on its specific domain.

### Implementation:
```java
// Monolithic approach
public class MonolithicOrderService {
    public void processOrder(Order order) {
        // User management
        User user = userRepository.findById(order.getUserId());
        
        // Inventory management
        for (OrderItem item : order.getItems()) {
            Product product = productRepository.findById(item.getProductId());
            if (product.getStock() < item.getQuantity()) {
                throw new InsufficientStockException();
            }
            product.setStock(product.getStock() - item.getQuantity());
        }
        
        // Payment processing
        PaymentResult result = paymentService.processPayment(order.getPaymentInfo());
        
        // Shipping
        ShippingInfo shipping = shippingService.createShipping(order);
        
        // Notification
        notificationService.sendOrderConfirmation(order);
    }
}

// Microservices approach
public class OrderService {
    private UserServiceClient userService;
    private InventoryServiceClient inventoryService;
    private PaymentServiceClient paymentService;
    private ShippingServiceClient shippingService;
    private NotificationServiceClient notificationService;
    
    public void processOrder(Order order) {
        // Delegate to specialized services
        userService.validateUser(order.getUserId());
        inventoryService.reserveItems(order.getItems());
        paymentService.processPayment(order.getPaymentInfo());
        shippingService.createShipping(order);
        notificationService.sendOrderConfirmation(order);
    }
}
```

## 15.2 Database per Service Pattern

Each microservice has its own database, ensuring data isolation and independence.

### When to Use:
- When you want to ensure data isolation between services
- When you need to use different database technologies
- When you want to scale databases independently

### Real-World Analogy:
Think of different departments in a company having their own filing systems - HR has employee records, Finance has financial data, and IT has technical documentation.

### Implementation:
```java
// User Service with its own database
@Service
public class UserService {
    @Autowired
    private UserRepository userRepository; // User database
    
    public User createUser(CreateUserRequest request) {
        User user = new User(request.getName(), request.getEmail());
        return userRepository.save(user);
    }
}

// Order Service with its own database
@Service
public class OrderService {
    @Autowired
    private OrderRepository orderRepository; // Order database
    
    public Order createOrder(CreateOrderRequest request) {
        Order order = new Order(request.getUserId(), request.getItems());
        return orderRepository.save(order);
    }
}

// Product Service with its own database
@Service
public class ProductService {
    @Autowired
    private ProductRepository productRepository; // Product database
    
    public Product createProduct(CreateProductRequest request) {
        Product product = new Product(request.getName(), request.getPrice());
        return productRepository.save(product);
    }
}
```

## 15.3 API Gateway Pattern

The API Gateway acts as a single entry point for all client requests, routing them to appropriate microservices.

### When to Use:
- When you need a single entry point for multiple microservices
- When you want to implement cross-cutting concerns (authentication, logging, rate limiting)
- When you need to hide the complexity of your microservices architecture

### Real-World Analogy:
Think of a hotel concierge who handles all guest requests and routes them to the appropriate department (housekeeping, room service, maintenance).

### Implementation:
```java
@RestController
@RequestMapping("/api")
public class ApiGatewayController {
    @Autowired
    private UserServiceClient userService;
    @Autowired
    private OrderServiceClient orderService;
    @Autowired
    private ProductServiceClient productService;
    
    @GetMapping("/users/{id}")
    public ResponseEntity<User> getUser(@PathVariable Long id) {
        return userService.getUser(id);
    }
    
    @PostMapping("/orders")
    public ResponseEntity<Order> createOrder(@RequestBody CreateOrderRequest request) {
        return orderService.createOrder(request);
    }
    
    @GetMapping("/products")
    public ResponseEntity<List<Product>> getProducts() {
        return productService.getProducts();
    }
}

// Gateway with cross-cutting concerns
@Component
public class ApiGatewayFilter implements Filter {
    @Override
    public void doFilter(ServletRequest request, ServletResponse response, FilterChain chain) {
        HttpServletRequest httpRequest = (HttpServletRequest) request;
        
        // Authentication
        if (!isAuthenticated(httpRequest)) {
            throw new UnauthorizedException();
        }
        
        // Rate limiting
        if (!isWithinRateLimit(httpRequest)) {
            throw new RateLimitExceededException();
        }
        
        // Logging
        logRequest(httpRequest);
        
        chain.doFilter(request, response);
    }
}
```

## 15.4 Backend for Frontend (BFF) Pattern

The BFF pattern creates separate backend services tailored to specific frontend applications.

### When to Use:
- When you have multiple frontend applications with different needs
- When you want to optimize data transfer for specific clients
- When you need to aggregate data from multiple microservices

### Real-World Analogy:
Think of a restaurant that has different menus for different types of customers (dine-in, takeout, delivery) - each menu is optimized for that specific service.

### Implementation:
```java
// Mobile BFF
@RestController
@RequestMapping("/mobile/api")
public class MobileBffController {
    @Autowired
    private UserServiceClient userService;
    @Autowired
    private OrderServiceClient orderService;
    
    @GetMapping("/user/{id}/summary")
    public ResponseEntity<UserSummary> getUserSummary(@PathVariable Long id) {
        User user = userService.getUser(id);
        List<Order> recentOrders = orderService.getRecentOrders(id, 5);
        
        // Aggregate data for mobile
        UserSummary summary = new UserSummary();
        summary.setName(user.getName());
        summary.setEmail(user.getEmail());
        summary.setRecentOrderCount(recentOrders.size());
        summary.setTotalSpent(recentOrders.stream()
                .mapToDouble(Order::getTotal)
                .sum());
        
        return ResponseEntity.ok(summary);
    }
}

// Web BFF
@RestController
@RequestMapping("/web/api")
public class WebBffController {
    @Autowired
    private UserServiceClient userService;
    @Autowired
    private OrderServiceClient orderService;
    @Autowired
    private ProductServiceClient productService;
    
    @GetMapping("/dashboard")
    public ResponseEntity<DashboardData> getDashboard() {
        // More detailed data for web
        DashboardData dashboard = new DashboardData();
        dashboard.setUsers(userService.getAllUsers());
        dashboard.setOrders(orderService.getAllOrders());
        dashboard.setProducts(productService.getAllProducts());
        
        return ResponseEntity.ok(dashboard);
    }
}
```

## 15.5 Strangler Fig Pattern

The Strangler Fig pattern gradually replaces a monolithic application by creating new microservices around it.

### When to Use:
- When you want to gradually migrate from a monolith to microservices
- When you need to minimize risk during migration
- When you want to maintain system stability during transition

### Real-World Analogy:
Think of renovating a house room by room while still living in it - you can continue using the house while gradually improving each room.

### Implementation:
```java
// Legacy monolith
@RestController
public class LegacyOrderController {
    @PostMapping("/legacy/orders")
    public ResponseEntity<Order> createOrder(@RequestBody OrderRequest request) {
        // Legacy implementation
        return legacyOrderService.createOrder(request);
    }
}

// New microservice
@RestController
public class NewOrderController {
    @PostMapping("/api/orders")
    public ResponseEntity<Order> createOrder(@RequestBody OrderRequest request) {
        // New implementation
        return newOrderService.createOrder(request);
    }
}

// Strangler Fig - gradually redirecting traffic
@RestController
public class OrderController {
    @Autowired
    private LegacyOrderController legacyController;
    @Autowired
    private NewOrderController newController;
    
    @PostMapping("/orders")
    public ResponseEntity<Order> createOrder(@RequestBody OrderRequest request) {
        // Feature flag to control routing
        if (isNewServiceEnabled(request.getType())) {
            return newController.createOrder(request);
        } else {
            return legacyController.createOrder(request);
        }
    }
    
    private boolean isNewServiceEnabled(String orderType) {
        // Logic to determine which service to use
        return "premium".equals(orderType);
    }
}
```

## 15.6 Anti-Corruption Layer Pattern

The Anti-Corruption Layer pattern translates between different domain models to prevent corruption.

### When to Use:
- When integrating with legacy systems
- When you need to protect your domain model from external influences
- When you want to gradually modernize without breaking existing systems

### Real-World Analogy:
Think of a translator who helps two people who speak different languages communicate without either person having to learn the other's language.

### Implementation:
```java
// Legacy system model
public class LegacyUser {
    private String user_id;
    private String full_name;
    private String email_address;
    // Legacy fields and methods
}

// Modern domain model
public class User {
    private Long id;
    private String name;
    private String email;
    // Modern fields and methods
}

// Anti-Corruption Layer
@Component
public class UserAntiCorruptionLayer {
    public User toModernUser(LegacyUser legacyUser) {
        User user = new User();
        user.setId(Long.parseLong(legacyUser.getUser_id()));
        user.setName(legacyUser.getFull_name());
        user.setEmail(legacyUser.getEmail_address());
        return user;
    }
    
    public LegacyUser toLegacyUser(User user) {
        LegacyUser legacyUser = new LegacyUser();
        legacyUser.setUser_id(user.getId().toString());
        legacyUser.setFull_name(user.getName());
        legacyUser.setEmail_address(user.getEmail());
        return legacyUser;
    }
}

// Service using the anti-corruption layer
@Service
public class UserService {
    @Autowired
    private UserAntiCorruptionLayer acl;
    @Autowired
    private LegacyUserRepository legacyRepository;
    @Autowired
    private UserRepository modernRepository;
    
    public User getUser(Long id) {
        LegacyUser legacyUser = legacyRepository.findById(id);
        return acl.toModernUser(legacyUser);
    }
    
    public User createUser(User user) {
        LegacyUser legacyUser = acl.toLegacyUser(user);
        legacyUser = legacyRepository.save(legacyUser);
        return acl.toModernUser(legacyUser);
    }
}
```

## 15.7 Bulkhead Pattern

The Bulkhead pattern isolates critical resources to prevent cascading failures.

### When to Use:
- When you want to prevent cascading failures
- When you need to isolate critical resources
- When you want to improve system resilience

### Real-World Analogy:
Think of a ship with watertight compartments - if one compartment floods, the water doesn't spread to other compartments, keeping the ship afloat.

### Implementation:
```java
// Bulkhead configuration
@Configuration
public class BulkheadConfig {
    @Bean
    public ThreadPoolTaskExecutor userServiceExecutor() {
        ThreadPoolTaskExecutor executor = new ThreadPoolTaskExecutor();
        executor.setCorePoolSize(5);
        executor.setMaxPoolSize(10);
        executor.setQueueCapacity(100);
        executor.setThreadNamePrefix("user-service-");
        return executor;
    }
    
    @Bean
    public ThreadPoolTaskExecutor orderServiceExecutor() {
        ThreadPoolTaskExecutor executor = new ThreadPoolTaskExecutor();
        executor.setCorePoolSize(3);
        executor.setMaxPoolSize(8);
        executor.setQueueCapacity(50);
        executor.setThreadNamePrefix("order-service-");
        return executor;
    }
}

// Service with bulkhead
@Service
public class UserService {
    @Autowired
    @Qualifier("userServiceExecutor")
    private ThreadPoolTaskExecutor executor;
    
    public CompletableFuture<User> getUserAsync(Long id) {
        return CompletableFuture.supplyAsync(() -> {
            // User service logic
            return userRepository.findById(id);
        }, executor);
    }
}

@Service
public class OrderService {
    @Autowired
    @Qualifier("orderServiceExecutor")
    private ThreadPoolTaskExecutor executor;
    
    public CompletableFuture<Order> getOrderAsync(Long id) {
        return CompletableFuture.supplyAsync(() -> {
            // Order service logic
            return orderRepository.findById(id);
        }, executor);
    }
}
```

## 15.8 Circuit Breaker Pattern

The Circuit Breaker pattern prevents cascading failures by stopping calls to failing services.

### When to Use:
- When you want to prevent cascading failures
- When you need to handle service failures gracefully
- When you want to improve system resilience

### Real-World Analogy:
Think of an electrical circuit breaker that trips when there's too much current, preventing damage to the electrical system.

### Implementation:
```java
@Component
public class CircuitBreaker {
    private enum State { CLOSED, OPEN, HALF_OPEN }
    
    private State state = State.CLOSED;
    private int failureCount = 0;
    private long lastFailureTime = 0;
    private final int failureThreshold = 5;
    private final long timeout = 60000; // 1 minute
    
    public <T> T execute(Supplier<T> operation) {
        if (state == State.OPEN) {
            if (System.currentTimeMillis() - lastFailureTime > timeout) {
                state = State.HALF_OPEN;
            } else {
                throw new CircuitBreakerOpenException();
            }
        }
        
        try {
            T result = operation.get();
            onSuccess();
            return result;
        } catch (Exception e) {
            onFailure();
            throw e;
        }
    }
    
    private void onSuccess() {
        failureCount = 0;
        state = State.CLOSED;
    }
    
    private void onFailure() {
        failureCount++;
        lastFailureTime = System.currentTimeMillis();
        
        if (failureCount >= failureThreshold) {
            state = State.OPEN;
        }
    }
}

// Service using circuit breaker
@Service
public class ExternalServiceClient {
    @Autowired
    private CircuitBreaker circuitBreaker;
    
    public String callExternalService(String request) {
        return circuitBreaker.execute(() -> {
            // External service call
            return externalApiClient.call(request);
        });
    }
}
```

## 15.9 Saga Pattern

The Saga pattern manages distributed transactions by breaking them into local transactions with compensating actions.

### When to Use:
- When you need to maintain data consistency across microservices
- When you want to avoid distributed transactions
- When you need to handle long-running business processes

### Real-World Analogy:
Think of booking a trip that involves flights, hotels, and car rentals - if any part fails, you need to cancel the previous bookings to maintain consistency.

### Implementation:
```java
// Saga orchestrator
@Component
public class OrderSaga {
    @Autowired
    private UserServiceClient userService;
    @Autowired
    private InventoryServiceClient inventoryService;
    @Autowired
    private PaymentServiceClient paymentService;
    @Autowired
    private ShippingServiceClient shippingService;
    
    public void processOrder(Order order) {
        List<SagaStep> steps = Arrays.asList(
            new ValidateUserStep(userService, order.getUserId()),
            new ReserveInventoryStep(inventoryService, order.getItems()),
            new ProcessPaymentStep(paymentService, order.getPaymentInfo()),
            new CreateShippingStep(shippingService, order)
        );
        
        List<SagaStep> completedSteps = new ArrayList<>();
        
        try {
            for (SagaStep step : steps) {
                step.execute();
                completedSteps.add(step);
            }
        } catch (Exception e) {
            // Compensate in reverse order
            Collections.reverse(completedSteps);
            for (SagaStep step : completedSteps) {
                step.compensate();
            }
            throw new SagaExecutionException("Order processing failed", e);
        }
    }
}

// Saga step interface
public interface SagaStep {
    void execute();
    void compensate();
}

// Concrete saga step
public class ReserveInventoryStep implements SagaStep {
    private InventoryServiceClient inventoryService;
    private List<OrderItem> items;
    
    public ReserveInventoryStep(InventoryServiceClient inventoryService, List<OrderItem> items) {
        this.inventoryService = inventoryService;
        this.items = items;
    }
    
    public void execute() {
        inventoryService.reserveItems(items);
    }
    
    public void compensate() {
        inventoryService.releaseItems(items);
    }
}
```

## 15.10 Event Sourcing Pattern

The Event Sourcing pattern stores changes as a sequence of events rather than storing the current state.

### When to Use:
- When you need to maintain a complete audit trail
- When you want to replay events to reconstruct state
- When you need to support temporal queries

### Real-World Analogy:
Think of a bank account statement that shows every transaction (deposit, withdrawal, transfer) rather than just the current balance.

### Implementation:
```java
// Event interface
public interface DomainEvent {
    String getEventId();
    LocalDateTime getTimestamp();
    String getEventType();
}

// Concrete events
public class UserCreatedEvent implements DomainEvent {
    private String eventId;
    private LocalDateTime timestamp;
    private String userId;
    private String name;
    private String email;
    
    // Constructor, getters, setters
}

public class UserUpdatedEvent implements DomainEvent {
    private String eventId;
    private LocalDateTime timestamp;
    private String userId;
    private String name;
    private String email;
    
    // Constructor, getters, setters
}

// Event store
@Component
public class EventStore {
    @Autowired
    private EventRepository eventRepository;
    
    public void saveEvent(DomainEvent event) {
        eventRepository.save(event);
    }
    
    public List<DomainEvent> getEvents(String aggregateId) {
        return eventRepository.findByAggregateId(aggregateId);
    }
}

// Aggregate root
public class User {
    private String id;
    private String name;
    private String email;
    private List<DomainEvent> uncommittedEvents;
    
    public User(String id, String name, String email) {
        this.id = id;
        this.name = name;
        this.email = email;
        this.uncommittedEvents = new ArrayList<>();
        
        // Add event
        uncommittedEvents.add(new UserCreatedEvent(id, name, email));
    }
    
    public void updateName(String newName) {
        this.name = newName;
        uncommittedEvents.add(new UserUpdatedEvent(id, newName, email));
    }
    
    public List<DomainEvent> getUncommittedEvents() {
        return uncommittedEvents;
    }
    
    public void markEventsAsCommitted() {
        uncommittedEvents.clear();
    }
}
```

This section covers the essential microservices patterns that help build scalable, resilient, and maintainable distributed systems.