# Section 24 – Microservices Best Practices

## 24.1 Design Principles

Design principles guide the creation of effective microservices architectures.

### Single Responsibility Principle:

```java
// Single Responsibility Principle
@Service
public class UserService {
    @Autowired
    private UserRepository userRepository;
    
    public User createUser(CreateUserRequest request) {
        // Only handles user creation
        User user = User.builder()
            .email(request.getEmail())
            .name(request.getName())
            .createdAt(Instant.now())
            .build();
        
        return userRepository.save(user);
    }
    
    public User getUser(Long id) {
        // Only handles user retrieval
        return userRepository.findById(id)
            .orElseThrow(() -> new UserNotFoundException("User not found"));
    }
}

// Separate service for user authentication
@Service
public class AuthenticationService {
    @Autowired
    private PasswordEncoder passwordEncoder;
    @Autowired
    private JwtTokenProvider tokenProvider;
    
    public String authenticate(String email, String password) {
        // Only handles authentication
        User user = userService.getUserByEmail(email);
        if (passwordEncoder.matches(password, user.getPassword())) {
            return tokenProvider.generateToken(user);
        }
        throw new AuthenticationException("Invalid credentials");
    }
}
```

### Domain-Driven Design:

```java
// Domain-Driven Design
@Entity
public class Order {
    @Id
    private Long id;
    private String orderNumber;
    private OrderStatus status;
    private List<OrderItem> items;
    private Money totalAmount;
    private CustomerId customerId;
    private Instant createdAt;
    
    // Domain methods
    public void addItem(ProductId productId, Quantity quantity, Money unitPrice) {
        OrderItem item = new OrderItem(productId, quantity, unitPrice);
        items.add(item);
        recalculateTotal();
    }
    
    public void confirm() {
        if (status != OrderStatus.PENDING) {
            throw new IllegalStateException("Order cannot be confirmed");
        }
        status = OrderStatus.CONFIRMED;
    }
    
    public void cancel() {
        if (status == OrderStatus.SHIPPED) {
            throw new IllegalStateException("Shipped orders cannot be cancelled");
        }
        status = OrderStatus.CANCELLED;
    }
    
    private void recalculateTotal() {
        totalAmount = items.stream()
            .map(OrderItem::getSubtotal)
            .reduce(Money.ZERO, Money::add);
    }
}
```

## 24.2 Service Design Guidelines

Guidelines for designing well-structured microservices.

### Service Interface Design:

```java
// Service Interface Design
@RestController
@RequestMapping("/api/v1/orders")
public class OrderController {
    @Autowired
    private OrderService orderService;
    
    @PostMapping
    public ResponseEntity<OrderResponse> createOrder(@RequestBody CreateOrderRequest request) {
        try {
            Order order = orderService.createOrder(request);
            OrderResponse response = OrderResponse.from(order);
            return ResponseEntity.status(HttpStatus.CREATED).body(response);
        } catch (ValidationException e) {
            return ResponseEntity.badRequest().build();
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).build();
        }
    }
    
    @GetMapping("/{id}")
    public ResponseEntity<OrderResponse> getOrder(@PathVariable Long id) {
        try {
            Order order = orderService.getOrder(id);
            OrderResponse response = OrderResponse.from(order);
            return ResponseEntity.ok(response);
        } catch (OrderNotFoundException e) {
            return ResponseEntity.notFound().build();
        }
    }
    
    @PutMapping("/{id}/status")
    public ResponseEntity<Void> updateOrderStatus(@PathVariable Long id, 
                                                @RequestBody UpdateOrderStatusRequest request) {
        try {
            orderService.updateOrderStatus(id, request.getStatus());
            return ResponseEntity.ok().build();
        } catch (OrderNotFoundException e) {
            return ResponseEntity.notFound().build();
        } catch (IllegalStateException e) {
            return ResponseEntity.badRequest().build();
        }
    }
}
```

### Data Transfer Objects:

```java
// Data Transfer Objects
public class CreateOrderRequest {
    @NotNull
    @Email
    private String customerEmail;
    
    @NotNull
    @NotEmpty
    private List<OrderItemRequest> items;
    
    @NotNull
    private AddressRequest shippingAddress;
    
    // Getters and setters
}

public class OrderResponse {
    private Long id;
    private String orderNumber;
    private String status;
    private Money totalAmount;
    private String customerEmail;
    private List<OrderItemResponse> items;
    private AddressResponse shippingAddress;
    private Instant createdAt;
    
    public static OrderResponse from(Order order) {
        return OrderResponse.builder()
            .id(order.getId())
            .orderNumber(order.getOrderNumber())
            .status(order.getStatus().toString())
            .totalAmount(order.getTotalAmount())
            .customerEmail(order.getCustomerId().getEmail())
            .items(order.getItems().stream()
                .map(OrderItemResponse::from)
                .collect(Collectors.toList()))
            .shippingAddress(AddressResponse.from(order.getShippingAddress()))
            .createdAt(order.getCreatedAt())
            .build();
    }
}
```

## 24.3 Error Handling Patterns

Consistent error handling across microservices.

### Global Exception Handler:

```java
// Global Exception Handler
@ControllerAdvice
public class GlobalExceptionHandler {
    
    @ExceptionHandler(ValidationException.class)
    public ResponseEntity<ErrorResponse> handleValidationException(ValidationException e) {
        ErrorResponse error = ErrorResponse.builder()
            .code("VALIDATION_ERROR")
            .message(e.getMessage())
            .timestamp(Instant.now())
            .build();
        
        return ResponseEntity.badRequest().body(error);
    }
    
    @ExceptionHandler(ResourceNotFoundException.class)
    public ResponseEntity<ErrorResponse> handleResourceNotFoundException(ResourceNotFoundException e) {
        ErrorResponse error = ErrorResponse.builder()
            .code("RESOURCE_NOT_FOUND")
            .message(e.getMessage())
            .timestamp(Instant.now())
            .build();
        
        return ResponseEntity.notFound().build();
    }
    
    @ExceptionHandler(ServiceUnavailableException.class)
    public ResponseEntity<ErrorResponse> handleServiceUnavailableException(ServiceUnavailableException e) {
        ErrorResponse error = ErrorResponse.builder()
            .code("SERVICE_UNAVAILABLE")
            .message("Service temporarily unavailable")
            .timestamp(Instant.now())
            .build();
        
        return ResponseEntity.status(HttpStatus.SERVICE_UNAVAILABLE).body(error);
    }
    
    @ExceptionHandler(Exception.class)
    public ResponseEntity<ErrorResponse> handleGenericException(Exception e) {
        ErrorResponse error = ErrorResponse.builder()
            .code("INTERNAL_ERROR")
            .message("An unexpected error occurred")
            .timestamp(Instant.now())
            .build();
        
        return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(error);
    }
}
```

### Circuit Breaker Pattern:

```java
// Circuit Breaker Pattern
@Service
public class PaymentService {
    @Autowired
    private PaymentClient paymentClient;
    @Autowired
    private CircuitBreakerRegistry circuitBreakerRegistry;
    
    private final CircuitBreaker circuitBreaker;
    
    public PaymentService() {
        this.circuitBreaker = circuitBreakerRegistry.circuitBreaker("payment-service");
    }
    
    public PaymentResult processPayment(PaymentRequest request) {
        return circuitBreaker.executeSupplier(() -> {
            try {
                return paymentClient.processPayment(request);
            } catch (Exception e) {
                throw new PaymentProcessingException("Payment processing failed", e);
            }
        });
    }
    
    @CircuitBreaker(name = "payment-service", fallbackMethod = "fallbackPayment")
    public PaymentResult processPaymentWithAnnotation(PaymentRequest request) {
        return paymentClient.processPayment(request);
    }
    
    public PaymentResult fallbackPayment(PaymentRequest request, Exception ex) {
        // Fallback logic
        return PaymentResult.builder()
            .status(PaymentStatus.PENDING)
            .message("Payment processing delayed due to service unavailability")
            .build();
    }
}
```

## 24.4 Logging and Monitoring

Comprehensive logging and monitoring for microservices.

### Structured Logging:

```java
// Structured Logging
@Service
public class OrderService {
    private static final Logger logger = LoggerFactory.getLogger(OrderService.class);
    
    @Autowired
    private OrderRepository orderRepository;
    @Autowired
    private EventPublisher eventPublisher;
    
    public Order createOrder(CreateOrderRequest request) {
        logger.info("Creating order for customer: {}", request.getCustomerEmail());
        
        try {
            Order order = Order.builder()
                .orderNumber(generateOrderNumber())
                .customerEmail(request.getCustomerEmail())
                .items(request.getItems())
                .status(OrderStatus.PENDING)
                .createdAt(Instant.now())
                .build();
            
            Order savedOrder = orderRepository.save(order);
            
            logger.info("Order created successfully with ID: {}", savedOrder.getId());
            
            // Publish event
            eventPublisher.publishEvent(new OrderCreatedEvent(savedOrder));
            
            return savedOrder;
            
        } catch (Exception e) {
            logger.error("Failed to create order for customer: {}", request.getCustomerEmail(), e);
            throw new OrderCreationException("Failed to create order", e);
        }
    }
    
    public Order getOrder(Long id) {
        logger.debug("Retrieving order with ID: {}", id);
        
        return orderRepository.findById(id)
            .orElseThrow(() -> {
                logger.warn("Order not found with ID: {}", id);
                return new OrderNotFoundException("Order not found");
            });
    }
}
```

### Metrics Collection:

```java
// Metrics Collection
@Component
public class OrderMetrics {
    private final MeterRegistry meterRegistry;
    private final Counter orderCreatedCounter;
    private final Timer orderProcessingTimer;
    private final Gauge activeOrdersGauge;
    
    public OrderMetrics(MeterRegistry meterRegistry) {
        this.meterRegistry = meterRegistry;
        this.orderCreatedCounter = Counter.builder("orders.created")
            .description("Number of orders created")
            .register(meterRegistry);
        this.orderProcessingTimer = Timer.builder("orders.processing.time")
            .description("Order processing time")
            .register(meterRegistry);
        this.activeOrdersGauge = Gauge.builder("orders.active")
            .description("Number of active orders")
            .register(meterRegistry, this, OrderMetrics::getActiveOrdersCount);
    }
    
    public void incrementOrderCreated() {
        orderCreatedCounter.increment();
    }
    
    public void recordOrderProcessingTime(Duration duration) {
        orderProcessingTimer.record(duration);
    }
    
    private double getActiveOrdersCount() {
        // Return current count of active orders
        return orderRepository.countByStatus(OrderStatus.PENDING);
    }
}
```

## 24.5 Security Best Practices

Security considerations for microservices.

### Authentication and Authorization:

```java
// Authentication and Authorization
@RestController
@RequestMapping("/api/v1/orders")
@PreAuthorize("hasRole('USER')")
public class OrderController {
    
    @PostMapping
    @PreAuthorize("hasPermission(#request.customerEmail, 'ORDER', 'CREATE')")
    public ResponseEntity<OrderResponse> createOrder(@RequestBody CreateOrderRequest request) {
        // Implementation
    }
    
    @GetMapping("/{id}")
    @PreAuthorize("hasPermission(#id, 'ORDER', 'READ')")
    public ResponseEntity<OrderResponse> getOrder(@PathVariable Long id) {
        // Implementation
    }
}

// JWT Token Provider
@Component
public class JwtTokenProvider {
    @Value("${jwt.secret}")
    private String secret;
    
    @Value("${jwt.expiration}")
    private Long expiration;
    
    public String generateToken(UserDetails userDetails) {
        Map<String, Object> claims = new HashMap<>();
        claims.put("sub", userDetails.getUsername());
        claims.put("roles", userDetails.getAuthorities());
        
        return createToken(claims, userDetails.getUsername());
    }
    
    private String createToken(Map<String, Object> claims, String subject) {
        return Jwts.builder()
            .setClaims(claims)
            .setSubject(subject)
            .setIssuedAt(new Date())
            .setExpiration(new Date(System.currentTimeMillis() + expiration))
            .signWith(SignatureAlgorithm.HS512, secret)
            .compact();
    }
    
    public Boolean validateToken(String token, UserDetails userDetails) {
        final String username = getUsernameFromToken(token);
        return (username.equals(userDetails.getUsername()) && !isTokenExpired(token));
    }
}
```

### Data Encryption:

```java
// Data Encryption
@Service
public class EncryptionService {
    @Value("${encryption.key}")
    private String encryptionKey;
    
    private final AESUtil aesUtil;
    
    public EncryptionService() {
        this.aesUtil = new AESUtil(encryptionKey);
    }
    
    public String encrypt(String plainText) {
        try {
            return aesUtil.encrypt(plainText);
        } catch (Exception e) {
            throw new EncryptionException("Failed to encrypt data", e);
        }
    }
    
    public String decrypt(String encryptedText) {
        try {
            return aesUtil.decrypt(encryptedText);
        } catch (Exception e) {
            throw new EncryptionException("Failed to decrypt data", e);
        }
    }
}

// Sensitive Data Entity
@Entity
public class Customer {
    @Id
    private Long id;
    
    @Convert(converter = EncryptedStringConverter.class)
    private String email;
    
    @Convert(converter = EncryptedStringConverter.class)
    private String phoneNumber;
    
    private String name; // Not encrypted
}
```

## 24.6 Performance Optimization

Performance optimization techniques for microservices.

### Caching Strategy:

```java
// Caching Strategy
@Service
public class ProductService {
    @Autowired
    private ProductRepository productRepository;
    @Autowired
    private RedisTemplate<String, Object> redisTemplate;
    
    @Cacheable(value = "products", key = "#id")
    public Product getProduct(Long id) {
        return productRepository.findById(id)
            .orElseThrow(() -> new ProductNotFoundException("Product not found"));
    }
    
    @CacheEvict(value = "products", key = "#product.id")
    public Product updateProduct(Product product) {
        return productRepository.save(product);
    }
    
    @CacheEvict(value = "products", allEntries = true)
    public void clearProductCache() {
        // Cache cleared
    }
    
    public List<Product> getProductsByCategory(String category) {
        String cacheKey = "products:category:" + category;
        
        List<Product> products = (List<Product>) redisTemplate.opsForValue().get(cacheKey);
        if (products == null) {
            products = productRepository.findByCategory(category);
            redisTemplate.opsForValue().set(cacheKey, products, Duration.ofMinutes(30));
        }
        
        return products;
    }
}
```

### Database Optimization:

```java
// Database Optimization
@Repository
public class OrderRepository extends JpaRepository<Order, Long> {
    
    @Query("SELECT o FROM Order o WHERE o.customerEmail = :email AND o.status = :status")
    List<Order> findByCustomerEmailAndStatus(@Param("email") String email, 
                                           @Param("status") OrderStatus status);
    
    @Query(value = "SELECT * FROM orders WHERE created_at >= :startDate AND created_at <= :endDate", 
           nativeQuery = true)
    List<Order> findOrdersByDateRange(@Param("startDate") LocalDateTime startDate, 
                                    @Param("endDate") LocalDateTime endDate);
    
    @Modifying
    @Query("UPDATE Order o SET o.status = :status WHERE o.id = :id")
    int updateOrderStatus(@Param("id") Long id, @Param("status") OrderStatus status);
    
    @Query("SELECT o FROM Order o JOIN FETCH o.items WHERE o.id = :id")
    Optional<Order> findByIdWithItems(@Param("id") Long id);
}
```

## 24.7 Testing Strategies

Comprehensive testing strategies for microservices.

### Unit Testing:

```java
// Unit Testing
@ExtendWith(MockitoExtension.class)
class OrderServiceTest {
    
    @Mock
    private OrderRepository orderRepository;
    
    @Mock
    private EventPublisher eventPublisher;
    
    @InjectMocks
    private OrderService orderService;
    
    @Test
    void shouldCreateOrderSuccessfully() {
        // Given
        CreateOrderRequest request = CreateOrderRequest.builder()
            .customerEmail("test@example.com")
            .items(Arrays.asList(new OrderItemRequest()))
            .build();
        
        Order savedOrder = Order.builder()
            .id(1L)
            .orderNumber("ORD-001")
            .customerEmail("test@example.com")
            .status(OrderStatus.PENDING)
            .build();
        
        when(orderRepository.save(any(Order.class))).thenReturn(savedOrder);
        
        // When
        Order result = orderService.createOrder(request);
        
        // Then
        assertThat(result).isNotNull();
        assertThat(result.getCustomerEmail()).isEqualTo("test@example.com");
        assertThat(result.getStatus()).isEqualTo(OrderStatus.PENDING);
        
        verify(orderRepository).save(any(Order.class));
        verify(eventPublisher).publishEvent(any(OrderCreatedEvent.class));
    }
    
    @Test
    void shouldThrowExceptionWhenOrderNotFound() {
        // Given
        Long orderId = 1L;
        when(orderRepository.findById(orderId)).thenReturn(Optional.empty());
        
        // When & Then
        assertThatThrownBy(() -> orderService.getOrder(orderId))
            .isInstanceOf(OrderNotFoundException.class)
            .hasMessage("Order not found");
    }
}
```

### Integration Testing:

```java
// Integration Testing
@SpringBootTest
@AutoConfigureTestDatabase
@Transactional
class OrderServiceIntegrationTest {
    
    @Autowired
    private OrderService orderService;
    
    @Autowired
    private OrderRepository orderRepository;
    
    @Test
    void shouldCreateAndRetrieveOrder() {
        // Given
        CreateOrderRequest request = CreateOrderRequest.builder()
            .customerEmail("test@example.com")
            .items(Arrays.asList(new OrderItemRequest()))
            .build();
        
        // When
        Order createdOrder = orderService.createOrder(request);
        Order retrievedOrder = orderService.getOrder(createdOrder.getId());
        
        // Then
        assertThat(retrievedOrder).isNotNull();
        assertThat(retrievedOrder.getId()).isEqualTo(createdOrder.getId());
        assertThat(retrievedOrder.getCustomerEmail()).isEqualTo("test@example.com");
    }
}
```

## 24.8 Deployment Best Practices

Best practices for deploying microservices.

### Blue-Green Deployment:

```yaml
# Blue-Green Deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: order-service-blue
spec:
  replicas: 3
  selector:
    matchLabels:
      app: order-service
      version: blue
  template:
    metadata:
      labels:
        app: order-service
        version: blue
    spec:
      containers:
      - name: order-service
        image: order-service:v1.0.0
        ports:
        - containerPort: 8080
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: order-service-green
spec:
  replicas: 3
  selector:
    matchLabels:
      app: order-service
      version: green
  template:
    metadata:
      labels:
        app: order-service
        version: green
    spec:
      containers:
      - name: order-service
        image: order-service:v1.1.0
        ports:
        - containerPort: 8080
---
apiVersion: v1
kind: Service
metadata:
  name: order-service
spec:
  selector:
    app: order-service
    version: blue  # Switch to green for deployment
  ports:
  - port: 80
    targetPort: 8080
```

### Health Checks:

```java
// Health Checks
@Component
public class OrderServiceHealthIndicator implements HealthIndicator {
    
    @Autowired
    private OrderRepository orderRepository;
    
    @Autowired
    private DatabaseHealthIndicator databaseHealthIndicator;
    
    @Override
    public Health health() {
        try {
            // Check database connectivity
            Health dbHealth = databaseHealthIndicator.health();
            if (dbHealth.getStatus() != Status.UP) {
                return Health.down()
                    .withDetail("database", "Database is down")
                    .build();
            }
            
            // Check if service can perform basic operations
            long orderCount = orderRepository.count();
            
            return Health.up()
                .withDetail("database", "Database is up")
                .withDetail("orderCount", orderCount)
                .build();
                
        } catch (Exception e) {
            return Health.down()
                .withDetail("error", e.getMessage())
                .build();
        }
    }
}
```

This comprehensive guide covers all aspects of microservices best practices, providing both theoretical understanding and practical implementation examples.