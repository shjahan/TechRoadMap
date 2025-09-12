# Section 20 – Microservices Anti-Patterns

## 20.1 Distributed Monolith

A distributed monolith is a microservices architecture that behaves like a monolith due to tight coupling.

### Symptoms:

- Services are tightly coupled
- Changes require coordination across multiple services
- Shared database across services
- Synchronous communication only
- Single deployment unit

### Example of Distributed Monolith:

```java
// Bad: Distributed Monolith
@Service
public class UserService {
    @Autowired
    private OrderServiceClient orderServiceClient;
    @Autowired
    private PaymentServiceClient paymentServiceClient;
    @Autowired
    private NotificationServiceClient notificationServiceClient;
    
    public User createUser(UserRequest request) {
        // Tight coupling - user service knows about all other services
        User user = new User(request);
        userRepository.save(user);
        
        // Synchronous calls to all services
        Order order = orderServiceClient.createOrder(request.getOrderRequest());
        Payment payment = paymentServiceClient.processPayment(request.getPaymentRequest());
        notificationServiceClient.sendWelcomeEmail(user.getEmail());
        
        return user;
    }
}
```

### Solution:

```java
// Good: Properly Decoupled Microservices
@Service
public class UserService {
    @Autowired
    private UserRepository userRepository;
    @Autowired
    private EventPublisher eventPublisher;
    
    public User createUser(UserRequest request) {
        User user = new User(request);
        User savedUser = userRepository.save(user);
        
        // Publish event for other services to handle
        eventPublisher.publishEvent(new UserCreatedEvent(savedUser));
        
        return savedUser;
    }
}

// Other services handle the event asynchronously
@EventListener
public class OrderService {
    public void handleUserCreated(UserCreatedEvent event) {
        // Handle user creation in order service
    }
}
```

## 20.2 Shared Database Anti-Pattern

Sharing a database across multiple microservices breaks data independence.

### Symptoms:

- Multiple services access the same database
- Database schema changes affect multiple services
- Data consistency issues
- Tight coupling between services

### Example of Shared Database:

```java
// Bad: Shared Database
@Service
public class UserService {
    @Autowired
    private JdbcTemplate jdbcTemplate;
    
    public User getUser(Long id) {
        // Direct access to shared database
        String sql = "SELECT * FROM users WHERE id = ?";
        return jdbcTemplate.queryForObject(sql, new Object[]{id}, User.class);
    }
}

@Service
public class OrderService {
    @Autowired
    private JdbcTemplate jdbcTemplate;
    
    public Order getOrder(Long id) {
        // Same database, different service
        String sql = "SELECT * FROM orders WHERE id = ?";
        return jdbcTemplate.queryForObject(sql, new Object[]{id}, Order.class);
    }
}
```

### Solution:

```java
// Good: Database per Service
@Service
public class UserService {
    @Autowired
    private UserRepository userRepository; // User database
    
    public User getUser(Long id) {
        return userRepository.findById(id);
    }
}

@Service
public class OrderService {
    @Autowired
    private OrderRepository orderRepository; // Order database
    
    public Order getOrder(Long id) {
        return orderRepository.findById(id);
    }
}
```

## 20.3 Chatty Services

Chatty services make too many small requests, causing performance issues.

### Symptoms:

- Multiple small API calls
- High network latency
- Poor performance
- Increased complexity

### Example of Chatty Services:

```java
// Bad: Chatty Services
@Service
public class OrderService {
    @Autowired
    private UserServiceClient userServiceClient;
    @Autowired
    private ProductServiceClient productServiceClient;
    
    public OrderDetails getOrderDetails(Long orderId) {
        Order order = getOrder(orderId);
        
        // Multiple small calls
        User user = userServiceClient.getUser(order.getUserId());
        List<Product> products = new ArrayList<>();
        for (OrderItem item : order.getItems()) {
            Product product = productServiceClient.getProduct(item.getProductId());
            products.add(product);
        }
        
        return OrderDetails.builder()
            .order(order)
            .user(user)
            .products(products)
            .build();
    }
}
```

### Solution:

```java
// Good: Batch Operations
@Service
public class OrderService {
    @Autowired
    private UserServiceClient userServiceClient;
    @Autowired
    private ProductServiceClient productServiceClient;
    
    public OrderDetails getOrderDetails(Long orderId) {
        Order order = getOrder(orderId);
        
        // Single batch call
        List<Long> productIds = order.getItems().stream()
            .map(OrderItem::getProductId)
            .collect(Collectors.toList());
        
        User user = userServiceClient.getUser(order.getUserId());
        List<Product> products = productServiceClient.getProducts(productIds);
        
        return OrderDetails.builder()
            .order(order)
            .user(user)
            .products(products)
            .build();
    }
}
```

## 20.4 God Service Anti-Pattern

A God service handles too many responsibilities, becoming a monolith.

### Symptoms:

- Single service with many responsibilities
- Large codebase
- Difficult to maintain
- Violates single responsibility principle

### Example of God Service:

```java
// Bad: God Service
@Service
public class UserManagementService {
    // User management
    public User createUser(UserRequest request) { }
    public User updateUser(Long id, UserRequest request) { }
    public void deleteUser(Long id) { }
    
    // Order management
    public Order createOrder(OrderRequest request) { }
    public Order updateOrder(Long id, OrderRequest request) { }
    public void cancelOrder(Long id) { }
    
    // Payment management
    public Payment processPayment(PaymentRequest request) { }
    public Payment refundPayment(Long paymentId) { }
    
    // Notification management
    public void sendEmail(String to, String subject, String body) { }
    public void sendSMS(String phone, String message) { }
    
    // Analytics
    public void trackUserAction(String action, Long userId) { }
    public AnalyticsReport generateReport() { }
}
```

### Solution:

```java
// Good: Separate Services
@Service
public class UserService {
    public User createUser(UserRequest request) { }
    public User updateUser(Long id, UserRequest request) { }
    public void deleteUser(Long id) { }
}

@Service
public class OrderService {
    public Order createOrder(OrderRequest request) { }
    public Order updateOrder(Long id, OrderRequest request) { }
    public void cancelOrder(Long id) { }
}

@Service
public class PaymentService {
    public Payment processPayment(PaymentRequest request) { }
    public Payment refundPayment(Long paymentId) { }
}

@Service
public class NotificationService {
    public void sendEmail(String to, String subject, String body) { }
    public void sendSMS(String phone, String message) { }
}

@Service
public class AnalyticsService {
    public void trackUserAction(String action, Long userId) { }
    public AnalyticsReport generateReport() { }
}
```

## 20.5 Anemic Domain Model

Anemic domain models have no business logic, only data.

### Symptoms:

- Domain objects with only getters and setters
- Business logic in service classes
- No encapsulation
- Poor object-oriented design

### Example of Anemic Domain Model:

```java
// Bad: Anemic Domain Model
public class User {
    private Long id;
    private String email;
    private String name;
    private String status;
    
    // Only getters and setters
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    public String getEmail() { return email; }
    public void setEmail(String email) { this.email = email; }
    // ... more getters and setters
}

@Service
public class UserService {
    public void activateUser(Long userId) {
        User user = userRepository.findById(userId);
        user.setStatus("ACTIVE"); // Business logic in service
        userRepository.save(user);
    }
    
    public void deactivateUser(Long userId) {
        User user = userRepository.findById(userId);
        user.setStatus("INACTIVE"); // Business logic in service
        userRepository.save(user);
    }
}
```

### Solution:

```java
// Good: Rich Domain Model
public class User {
    private Long id;
    private String email;
    private String name;
    private UserStatus status;
    
    public User(String email, String name) {
        this.email = email;
        this.name = name;
        this.status = UserStatus.ACTIVE;
    }
    
    // Business logic in domain object
    public void activate() {
        if (this.status == UserStatus.SUSPENDED) {
            throw new IllegalStateException("Cannot activate suspended user");
        }
        this.status = UserStatus.ACTIVE;
    }
    
    public void deactivate() {
        this.status = UserStatus.INACTIVE;
    }
    
    public void suspend() {
        this.status = UserStatus.SUSPENDED;
    }
    
    public boolean isActive() {
        return this.status == UserStatus.ACTIVE;
    }
}

@Service
public class UserService {
    public void activateUser(Long userId) {
        User user = userRepository.findById(userId);
        user.activate(); // Business logic in domain object
        userRepository.save(user);
    }
}
```

## 20.6 Data Duplication Issues

Data duplication across services can lead to consistency problems.

### Symptoms:

- Same data stored in multiple services
- Data inconsistency
- Synchronization issues
- Storage waste

### Example of Data Duplication:

```java
// Bad: Data Duplication
@Service
public class UserService {
    public User getUser(Long id) {
        return userRepository.findById(id);
    }
}

@Service
public class OrderService {
    @Autowired
    private UserServiceClient userServiceClient;
    
    public Order createOrder(OrderRequest request) {
        // Duplicate user data in order
        User user = userServiceClient.getUser(request.getUserId());
        Order order = new Order();
        order.setUserId(user.getId());
        order.setUserEmail(user.getEmail()); // Duplicated data
        order.setUserName(user.getName());   // Duplicated data
        return orderRepository.save(order);
    }
}
```

### Solution:

```java
// Good: Reference Data
@Service
public class OrderService {
    @Autowired
    private UserServiceClient userServiceClient;
    
    public Order createOrder(OrderRequest request) {
        // Only store reference to user
        Order order = new Order();
        order.setUserId(request.getUserId());
        return orderRepository.save(order);
    }
    
    public OrderDetails getOrderDetails(Long orderId) {
        Order order = orderRepository.findById(orderId);
        
        // Get user data when needed
        User user = userServiceClient.getUser(order.getUserId());
        
        return OrderDetails.builder()
            .order(order)
            .user(user)
            .build();
    }
}
```

## 20.7 Inappropriate Service Boundaries

Service boundaries that don't align with business capabilities.

### Symptoms:

- Services based on technical layers
- Services that don't match business domains
- Difficult to understand service responsibilities
- Poor team organization

### Example of Inappropriate Boundaries:

```java
// Bad: Technical Layer Boundaries
@Service
public class DatabaseService {
    public void saveUser(User user) { }
    public void saveOrder(Order order) { }
    public void saveProduct(Product product) { }
}

@Service
public class ValidationService {
    public void validateUser(User user) { }
    public void validateOrder(Order order) { }
    public void validateProduct(Product product) { }
}

@Service
public class NotificationService {
    public void sendUserNotification(User user) { }
    public void sendOrderNotification(Order order) { }
    public void sendProductNotification(Product product) { }
}
```

### Solution:

```java
// Good: Business Capability Boundaries
@Service
public class UserService {
    public User createUser(UserRequest request) { }
    public User updateUser(Long id, UserRequest request) { }
    public void deleteUser(Long id) { }
    public void sendUserNotification(User user) { }
}

@Service
public class OrderService {
    public Order createOrder(OrderRequest request) { }
    public Order updateOrder(Long id, OrderRequest request) { }
    public void cancelOrder(Long id) { }
    public void sendOrderNotification(Order order) { }
}

@Service
public class ProductService {
    public Product createProduct(ProductRequest request) { }
    public Product updateProduct(Long id, ProductRequest request) { }
    public void deleteProduct(Long id) { }
    public void sendProductNotification(Product product) { }
}
```

## 20.8 Over-Engineering

Over-engineering adds unnecessary complexity to microservices.

### Symptoms:

- Complex architecture for simple problems
- Unnecessary abstractions
- Over-designed solutions
- High maintenance cost

### Example of Over-Engineering:

```java
// Bad: Over-Engineering
@Service
public class UserService {
    @Autowired
    private UserRepository userRepository;
    @Autowired
    private UserValidationService userValidationService;
    @Autowired
    private UserTransformationService userTransformationService;
    @Autowired
    private UserAuditService userAuditService;
    @Autowired
    private UserCacheService userCacheService;
    @Autowired
    private UserEventService userEventService;
    
    public User createUser(UserRequest request) {
        // Over-engineered with too many services
        UserValidationResult validation = userValidationService.validate(request);
        if (!validation.isValid()) {
            throw new ValidationException(validation.getErrors());
        }
        
        User user = userTransformationService.transform(request);
        User savedUser = userRepository.save(user);
        
        userAuditService.audit(savedUser);
        userCacheService.cache(savedUser);
        userEventService.publishEvent(savedUser);
        
        return savedUser;
    }
}
```

### Solution:

```java
// Good: Simple and Effective
@Service
public class UserService {
    @Autowired
    private UserRepository userRepository;
    
    public User createUser(UserRequest request) {
        // Simple and direct
        User user = new User(request);
        return userRepository.save(user);
    }
}
```

This comprehensive guide covers all aspects of microservices anti-patterns, providing both theoretical understanding and practical examples of what to avoid.