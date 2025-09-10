# Section 14 - Enterprise Java Development

## 14.1 Spring Framework Ecosystem

Spring Framework یکی از محبوب‌ترین frameworks برای Enterprise Java Development است که مجموعه‌ای از ابزارها و libraries را فراهم می‌کند.

### مفاهیم کلیدی:

**1. Core Spring:**
- Dependency Injection (DI)
- Inversion of Control (IoC)
- Aspect-Oriented Programming (AOP)
- Spring Container

**2. Spring Modules:**
- Spring Boot
- Spring MVC
- Spring Data
- Spring Security
- Spring Cloud

**3. Enterprise Features:**
- Transaction Management
- Caching
- Messaging
- Web Services

### مثال عملی:

```java
// Spring Boot Application
@SpringBootApplication
public class SpringFrameworkExample {
    public static void main(String[] args) {
        SpringApplication.run(SpringFrameworkExample.class, args);
    }
}

// Service Layer
@Service
public class UserService {
    @Autowired
    private UserRepository userRepository;
    
    public User createUser(String name, String email) {
        User user = new User(name, email);
        return userRepository.save(user);
    }
    
    public User findUserById(Long id) {
        return userRepository.findById(id).orElse(null);
    }
}

// Repository Layer
@Repository
public interface UserRepository extends JpaRepository<User, Long> {
    List<User> findByName(String name);
    List<User> findByEmailContaining(String email);
}

// Entity
@Entity
@Table(name = "users")
public class User {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @Column(name = "name")
    private String name;
    
    @Column(name = "email")
    private String email;
    
    // Constructors, getters, setters
    public User() {}
    
    public User(String name, String email) {
        this.name = name;
        this.email = email;
    }
    
    // Getters and setters
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
    public String getEmail() { return email; }
    public void setEmail(String email) { this.email = email; }
}

// REST Controller
@RestController
@RequestMapping("/api/users")
public class UserController {
    @Autowired
    private UserService userService;
    
    @PostMapping
    public ResponseEntity<User> createUser(@RequestBody UserRequest request) {
        User user = userService.createUser(request.getName(), request.getEmail());
        return ResponseEntity.ok(user);
    }
    
    @GetMapping("/{id}")
    public ResponseEntity<User> getUser(@PathVariable Long id) {
        User user = userService.findUserById(id);
        if (user != null) {
            return ResponseEntity.ok(user);
        } else {
            return ResponseEntity.notFound().build();
        }
    }
}

// Configuration
@Configuration
@EnableJpaRepositories
public class DatabaseConfig {
    @Bean
    public DataSource dataSource() {
        HikariConfig config = new HikariConfig();
        config.setJdbcUrl("jdbc:mysql://localhost:3306/myapp");
        config.setUsername("root");
        config.setPassword("password");
        return new HikariDataSource(config);
    }
}
```

### آنالوژی دنیای واقعی:
Spring Framework مانند داشتن یک کارخانه تولیدی کامل است که:
- **Dependency Injection:** مانند سیستم تامین مواد اولیه خودکار
- **Spring Container:** مانند مدیریت مرکزی کارخانه
- **Modules:** مانند بخش‌های مختلف کارخانه (تولید، انبار، حمل و نقل)

## 14.2 Jakarta EE (formerly Java EE)

Jakarta EE (formerly Java EE) مجموعه‌ای از specifications برای Enterprise Java Development است.

### مفاهیم کلیدی:

**1. Core Specifications:**
- Servlets
- JSP (JavaServer Pages)
- JPA (Java Persistence API)
- EJB (Enterprise JavaBeans)
- JMS (Java Message Service)

**2. Web Technologies:**
- JSF (JavaServer Faces)
- JAX-RS (RESTful Web Services)
- JAX-WS (SOAP Web Services)
- WebSocket

**3. Enterprise Features:**
- Security
- Transactions
- Caching
- Validation

### مثال عملی:

```java
// JAX-RS REST Service
@Path("/users")
@Produces(MediaType.APPLICATION_JSON)
@Consumes(MediaType.APPLICATION_JSON)
public class UserResource {
    @Inject
    private UserService userService;
    
    @GET
    @Path("/{id}")
    public Response getUser(@PathParam("id") Long id) {
        User user = userService.findById(id);
        if (user != null) {
            return Response.ok(user).build();
        } else {
            return Response.status(Response.Status.NOT_FOUND).build();
        }
    }
    
    @POST
    public Response createUser(User user) {
        User createdUser = userService.create(user);
        return Response.status(Response.Status.CREATED)
                      .entity(createdUser)
                      .build();
    }
}

// EJB Service
@Stateless
@TransactionManagement(TransactionManagementType.CONTAINER)
public class UserService {
    @PersistenceContext
    private EntityManager entityManager;
    
    public User findById(Long id) {
        return entityManager.find(User.class, id);
    }
    
    @TransactionAttribute(TransactionAttributeType.REQUIRED)
    public User create(User user) {
        entityManager.persist(user);
        return user;
    }
}

// JPA Entity
@Entity
@Table(name = "users")
@NamedQuery(name = "User.findByEmail", 
           query = "SELECT u FROM User u WHERE u.email = :email")
public class User {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @Column(name = "name", nullable = false)
    private String name;
    
    @Column(name = "email", unique = true)
    private String email;
    
    // Constructors, getters, setters
}

// Servlet
@WebServlet("/hello")
public class HelloServlet extends HttpServlet {
    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response) 
            throws ServletException, IOException {
        response.setContentType("text/html");
        PrintWriter out = response.getWriter();
        out.println("<html><body>");
        out.println("<h1>Hello from Jakarta EE!</h1>");
        out.println("</body></html>");
    }
}
```

### آنالوژی دنیای واقعی:
Jakarta EE مانند داشتن یک مجموعه استانداردهای صنعتی است که:
- **Specifications:** مانند استانداردهای کیفیت محصولات
- **Implementations:** مانند کارخانه‌هایی که این استانداردها را پیاده‌سازی می‌کنند
- **Enterprise Features:** مانند امکانات پیشرفته برای سازمان‌های بزرگ

## 14.3 Microservices Architecture

Microservices Architecture یک الگوی معماری است که applications را به سرویس‌های کوچک و مستقل تقسیم می‌کند.

### مفاهیم کلیدی:

**1. Service Decomposition:**
- Single Responsibility Principle
- Domain-driven design
- Loose coupling
- High cohesion

**2. Communication:**
- HTTP/REST
- Message queues
- Event-driven architecture
- API Gateway

**3. Data Management:**
- Database per service
- Event sourcing
- CQRS (Command Query Responsibility Segregation)
- Saga pattern

### مثال عملی:

```java
// User Service
@SpringBootApplication
@EnableEurekaClient
public class UserServiceApplication {
    public static void main(String[] args) {
        SpringApplication.run(UserServiceApplication.class, args);
    }
}

@RestController
@RequestMapping("/api/users")
public class UserController {
    @Autowired
    private UserService userService;
    
    @GetMapping("/{id}")
    public ResponseEntity<User> getUser(@PathVariable Long id) {
        User user = userService.findById(id);
        return ResponseEntity.ok(user);
    }
    
    @PostMapping
    public ResponseEntity<User> createUser(@RequestBody User user) {
        User createdUser = userService.create(user);
        return ResponseEntity.ok(createdUser);
    }
}

@Service
public class UserService {
    @Autowired
    private UserRepository userRepository;
    
    @Autowired
    private NotificationServiceClient notificationService;
    
    public User create(User user) {
        User savedUser = userRepository.save(user);
        
        // Send notification to notification service
        notificationService.sendWelcomeEmail(savedUser.getEmail());
        
        return savedUser;
    }
}

// Order Service
@SpringBootApplication
@EnableEurekaClient
public class OrderServiceApplication {
    public static void main(String[] args) {
        SpringApplication.run(OrderServiceApplication.class, args);
    }
}

@RestController
@RequestMapping("/api/orders")
public class OrderController {
    @Autowired
    private OrderService orderService;
    
    @PostMapping
    public ResponseEntity<Order> createOrder(@RequestBody OrderRequest request) {
        Order order = orderService.createOrder(request);
        return ResponseEntity.ok(order);
    }
}

@Service
public class OrderService {
    @Autowired
    private OrderRepository orderRepository;
    
    @Autowired
    private UserServiceClient userService;
    
    @Autowired
    private PaymentServiceClient paymentService;
    
    public Order createOrder(OrderRequest request) {
        // Validate user exists
        User user = userService.getUser(request.getUserId());
        if (user == null) {
            throw new UserNotFoundException("User not found");
        }
        
        // Create order
        Order order = new Order(request.getUserId(), request.getItems());
        order = orderRepository.save(order);
        
        // Process payment
        PaymentResult paymentResult = paymentService.processPayment(
            order.getId(), request.getPaymentInfo());
        
        if (paymentResult.isSuccess()) {
            order.setStatus(OrderStatus.CONFIRMED);
        } else {
            order.setStatus(OrderStatus.PAYMENT_FAILED);
        }
        
        return orderRepository.save(order);
    }
}

// API Gateway
@SpringBootApplication
@EnableZuulProxy
public class ApiGatewayApplication {
    public static void main(String[] args) {
        SpringApplication.run(ApiGatewayApplication.class, args);
    }
}

@Configuration
public class GatewayConfig {
    @Bean
    public RouteLocator customRouteLocator(RouteLocatorBuilder builder) {
        return builder.routes()
            .route("user-service", r -> r.path("/api/users/**")
                .uri("http://user-service:8080"))
            .route("order-service", r -> r.path("/api/orders/**")
                .uri("http://order-service:8080"))
            .build();
    }
}
```

### آنالوژی دنیای واقعی:
Microservices Architecture مانند داشتن یک مجموعه رستوران‌های زنجیره‌ای است که:
- **Each Service:** مانند هر رستوران که مستقل عمل می‌کند
- **Communication:** مانند سیستم ارتباطی بین رستوران‌ها
- **API Gateway:** مانند مرکز تماس مرکزی که مشتریان را به رستوران مناسب هدایت می‌کند

## 14.4 RESTful Web Services

RESTful Web Services یک الگوی معماری برای طراحی web services است که از HTTP protocol استفاده می‌کند.

### مفاهیم کلیدی:

**1. REST Principles:**
- Stateless
- Client-Server
- Cacheable
- Uniform Interface
- Layered System

**2. HTTP Methods:**
- GET (Read)
- POST (Create)
- PUT (Update)
- DELETE (Delete)
- PATCH (Partial Update)

**3. Resource Design:**
- Resource identification
- Resource representation
- Self-descriptive messages
- Hypermedia as the Engine of Application State (HATEOAS)

### مثال عملی:

```java
// REST Controller
@RestController
@RequestMapping("/api/users")
@Validated
public class UserController {
    @Autowired
    private UserService userService;
    
    @GetMapping
    public ResponseEntity<List<User>> getAllUsers(
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "10") int size) {
        List<User> users = userService.findAll(page, size);
        return ResponseEntity.ok(users);
    }
    
    @GetMapping("/{id}")
    public ResponseEntity<User> getUser(@PathVariable @Min(1) Long id) {
        User user = userService.findById(id);
        if (user != null) {
            return ResponseEntity.ok(user);
        } else {
            return ResponseEntity.notFound().build();
        }
    }
    
    @PostMapping
    public ResponseEntity<User> createUser(@Valid @RequestBody UserRequest request) {
        User user = userService.create(request);
        return ResponseEntity.status(HttpStatus.CREATED).body(user);
    }
    
    @PutMapping("/{id}")
    public ResponseEntity<User> updateUser(@PathVariable Long id, 
                                         @Valid @RequestBody UserRequest request) {
        User user = userService.update(id, request);
        if (user != null) {
            return ResponseEntity.ok(user);
        } else {
            return ResponseEntity.notFound().build();
        }
    }
    
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteUser(@PathVariable Long id) {
        boolean deleted = userService.delete(id);
        if (deleted) {
            return ResponseEntity.noContent().build();
        } else {
            return ResponseEntity.notFound().build();
        }
    }
}

// Service Layer
@Service
@Transactional
public class UserService {
    @Autowired
    private UserRepository userRepository;
    
    public List<User> findAll(int page, int size) {
        Pageable pageable = PageRequest.of(page, size);
        return userRepository.findAll(pageable).getContent();
    }
    
    public User findById(Long id) {
        return userRepository.findById(id).orElse(null);
    }
    
    public User create(UserRequest request) {
        User user = new User();
        user.setName(request.getName());
        user.setEmail(request.getEmail());
        return userRepository.save(user);
    }
    
    public User update(Long id, UserRequest request) {
        User user = userRepository.findById(id).orElse(null);
        if (user != null) {
            user.setName(request.getName());
            user.setEmail(request.getEmail());
            return userRepository.save(user);
        }
        return null;
    }
    
    public boolean delete(Long id) {
        if (userRepository.existsById(id)) {
            userRepository.deleteById(id);
            return true;
        }
        return false;
    }
}

// DTOs
public class UserRequest {
    @NotBlank(message = "Name is required")
    private String name;
    
    @Email(message = "Invalid email format")
    private String email;
    
    // Constructors, getters, setters
}

public class User {
    private Long id;
    private String name;
    private String email;
    private LocalDateTime createdAt;
    
    // Constructors, getters, setters
}

// Exception Handling
@ControllerAdvice
public class GlobalExceptionHandler {
    @ExceptionHandler(ValidationException.class)
    public ResponseEntity<ErrorResponse> handleValidationException(ValidationException e) {
        ErrorResponse error = new ErrorResponse("VALIDATION_ERROR", e.getMessage());
        return ResponseEntity.badRequest().body(error);
    }
    
    @ExceptionHandler(ResourceNotFoundException.class)
    public ResponseEntity<ErrorResponse> handleResourceNotFoundException(ResourceNotFoundException e) {
        ErrorResponse error = new ErrorResponse("RESOURCE_NOT_FOUND", e.getMessage());
        return ResponseEntity.notFound().build();
    }
}
```

### آنالوژی دنیای واقعی:
RESTful Web Services مانند داشتن یک سیستم سفارش آنلاین است که:
- **Resources:** مانند محصولات مختلف در فروشگاه
- **HTTP Methods:** مانند عملیات مختلف (مشاهده، سفارش، تغییر، حذف)
- **Stateless:** مانند اینکه هر سفارش مستقل است و نیازی به حفظ وضعیت قبلی نیست

## 14.5 Message Queues & Event-Driven Architecture

Message Queues & Event-Driven Architecture الگوهای مهمی برای طراحی سیستم‌های توزیع‌شده هستند.

### مفاهیم کلیدی:

**1. Message Queues:**
- Asynchronous communication
- Decoupling
- Reliability
- Scalability

**2. Event-Driven Architecture:**
- Event sourcing
- CQRS
- Event streaming
- Reactive programming

**3. Popular Technologies:**
- Apache Kafka
- RabbitMQ
- Amazon SQS
- Redis

### مثال عملی:

```java
// Event Publisher
@Component
public class EventPublisher {
    @Autowired
    private RabbitTemplate rabbitTemplate;
    
    public void publishUserCreatedEvent(User user) {
        UserCreatedEvent event = new UserCreatedEvent(user.getId(), user.getName(), user.getEmail());
        rabbitTemplate.convertAndSend("user.exchange", "user.created", event);
    }
    
    public void publishOrderCreatedEvent(Order order) {
        OrderCreatedEvent event = new OrderCreatedEvent(order.getId(), order.getUserId(), order.getTotal());
        rabbitTemplate.convertAndSend("order.exchange", "order.created", event);
    }
}

// Event Listeners
@Component
public class UserEventListener {
    @Autowired
    private EmailService emailService;
    
    @RabbitListener(queues = "user.created.queue")
    public void handleUserCreated(UserCreatedEvent event) {
        System.out.println("User created: " + event.getName());
        emailService.sendWelcomeEmail(event.getEmail());
    }
}

@Component
public class OrderEventListener {
    @Autowired
    private InventoryService inventoryService;
    
    @RabbitListener(queues = "order.created.queue")
    public void handleOrderCreated(OrderCreatedEvent event) {
        System.out.println("Order created: " + event.getOrderId());
        inventoryService.reserveItems(event.getOrderId());
    }
}

// Event Classes
public class UserCreatedEvent {
    private Long userId;
    private String name;
    private String email;
    private LocalDateTime timestamp;
    
    // Constructors, getters, setters
}

public class OrderCreatedEvent {
    private Long orderId;
    private Long userId;
    private BigDecimal total;
    private LocalDateTime timestamp;
    
    // Constructors, getters, setters
}

// Configuration
@Configuration
@EnableRabbit
public class RabbitMQConfig {
    @Bean
    public TopicExchange userExchange() {
        return new TopicExchange("user.exchange");
    }
    
    @Bean
    public Queue userCreatedQueue() {
        return new Queue("user.created.queue");
    }
    
    @Bean
    public Binding userCreatedBinding() {
        return BindingBuilder.bind(userCreatedQueue())
                            .to(userExchange())
                            .with("user.created");
    }
}
```

### آنالوژی دنیای واقعی:
Message Queues & Event-Driven Architecture مانند داشتن یک سیستم پست هوشمند است که:
- **Message Queues:** مانند صندوق‌های پستی که پیام‌ها را ذخیره می‌کنند
- **Event-Driven:** مانند سیستم اطلاع‌رسانی که در صورت وقوع رویداد، پیام ارسال می‌کند
- **Asynchronous:** مانند ارسال نامه که نیازی به انتظار پاسخ فوری نیست

## 14.6 Database Integration & ORM

Database Integration & ORM یکی از مهم‌ترین جنبه‌های Enterprise Java Development است.

### مفاهیم کلیدی:

**1. ORM (Object-Relational Mapping):**
- JPA (Java Persistence API)
- Hibernate
- Entity mapping
- Relationship mapping

**2. Database Technologies:**
- SQL databases
- NoSQL databases
- Database migrations
- Connection pooling

**3. Data Access Patterns:**
- Repository pattern
- Unit of Work
- Active Record
- Data Mapper

### مثال عملی:

```java
// JPA Entity
@Entity
@Table(name = "users")
@NamedQueries({
    @NamedQuery(name = "User.findByEmail", 
               query = "SELECT u FROM User u WHERE u.email = :email"),
    @NamedQuery(name = "User.findActiveUsers", 
               query = "SELECT u FROM User u WHERE u.active = true")
})
public class User {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @Column(name = "name", nullable = false, length = 100)
    private String name;
    
    @Column(name = "email", unique = true, nullable = false)
    private String email;
    
    @Column(name = "active", nullable = false)
    private Boolean active = true;
    
    @OneToMany(mappedBy = "user", cascade = CascadeType.ALL, fetch = FetchType.LAZY)
    private List<Order> orders = new ArrayList<>();
    
    @CreationTimestamp
    @Column(name = "created_at", updatable = false)
    private LocalDateTime createdAt;
    
    @UpdateTimestamp
    @Column(name = "updated_at")
    private LocalDateTime updatedAt;
    
    // Constructors, getters, setters
}

// Repository
@Repository
public interface UserRepository extends JpaRepository<User, Long> {
    List<User> findByNameContainingIgnoreCase(String name);
    List<User> findByEmailContaining(String email);
    List<User> findByActiveTrue();
    
    @Query("SELECT u FROM User u WHERE u.createdAt >= :date")
    List<User> findUsersCreatedAfter(@Param("date") LocalDateTime date);
    
    @Modifying
    @Query("UPDATE User u SET u.active = false WHERE u.id = :id")
    int deactivateUser(@Param("id") Long id);
}

// Service Layer
@Service
@Transactional
public class UserService {
    @Autowired
    private UserRepository userRepository;
    
    public List<User> findAll() {
        return userRepository.findAll();
    }
    
    public User findById(Long id) {
        return userRepository.findById(id)
                           .orElseThrow(() -> new UserNotFoundException("User not found"));
    }
    
    public User create(User user) {
        return userRepository.save(user);
    }
    
    public User update(Long id, User user) {
        User existingUser = findById(id);
        existingUser.setName(user.getName());
        existingUser.setEmail(user.getEmail());
        return userRepository.save(existingUser);
    }
    
    public void delete(Long id) {
        userRepository.deleteById(id);
    }
    
    public List<User> searchUsers(String searchTerm) {
        return userRepository.findByNameContainingIgnoreCase(searchTerm);
    }
}

// Database Configuration
@Configuration
@EnableJpaRepositories
@EnableTransactionManagement
public class DatabaseConfig {
    @Bean
    public DataSource dataSource() {
        HikariConfig config = new HikariConfig();
        config.setJdbcUrl("jdbc:mysql://localhost:3306/myapp");
        config.setUsername("root");
        config.setPassword("password");
        config.setMaximumPoolSize(20);
        config.setMinimumIdle(5);
        return new HikariDataSource(config);
    }
    
    @Bean
    public LocalContainerEntityManagerFactoryBean entityManagerFactory() {
        LocalContainerEntityManagerFactoryBean em = new LocalContainerEntityManagerFactoryBean();
        em.setDataSource(dataSource());
        em.setPackagesToScan("com.example.entity");
        em.setJpaVendorAdapter(new HibernateJpaVendorAdapter());
        return em;
    }
    
    @Bean
    public PlatformTransactionManager transactionManager() {
        JpaTransactionManager transactionManager = new JpaTransactionManager();
        transactionManager.setEntityManagerFactory(entityManagerFactory().getObject());
        return transactionManager;
    }
}
```

### آنالوژی دنیای واقعی:
Database Integration & ORM مانند داشتن یک سیستم مدیریت انبار هوشمند است که:
- **ORM:** مانند سیستم ترجمه خودکار بین زبان‌های مختلف
- **Repository Pattern:** مانند سیستم طبقه‌بندی و بازیابی کالاها
- **Transactions:** مانند سیستم کنترل کیفیت که اطمینان می‌دهد همه عملیات به درستی انجام شوند