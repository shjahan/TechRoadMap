# Section 3 – Communication Patterns

## 3.1 Synchronous Communication

Synchronous communication is a request-response pattern where the client sends a request and waits for a response before continuing execution. This is the most common communication pattern in microservices.

### Characteristics:

#### 1. **Blocking Nature**
The client blocks until it receives a response.

#### 2. **Immediate Response**
The client gets an immediate response or timeout.

#### 3. **Error Handling**
Errors are immediately visible to the client.

#### 4. **Performance Impact**
Network latency affects response time.

### Implementation with REST:

```java
// User Service
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
}

// Order Service calling User Service
@Service
public class OrderService {
    @Autowired
    private UserServiceClient userServiceClient;
    
    public Order createOrder(OrderRequest request) {
        // Synchronous call to user service
        User user = userServiceClient.getUser(request.getUserId());
        
        if (user == null) {
            throw new UserNotFoundException("User not found: " + request.getUserId());
        }
        
        // Process order with user information
        return processOrder(request, user);
    }
}

// User Service Client
@Component
public class UserServiceClient {
    @Autowired
    private RestTemplate restTemplate;
    
    private static final String USER_SERVICE_URL = "http://user-service/api/users";
    
    public User getUser(Long id) {
        try {
            ResponseEntity<User> response = restTemplate.getForEntity(
                USER_SERVICE_URL + "/" + id, User.class);
            return response.getBody();
        } catch (HttpClientErrorException e) {
            if (e.getStatusCode() == HttpStatus.NOT_FOUND) {
                return null;
            }
            throw new UserServiceException("Error calling user service", e);
        }
    }
}
```

### Implementation with gRPC:

```java
// gRPC Service Definition
service UserService {
    rpc GetUser(GetUserRequest) returns (GetUserResponse);
}

// gRPC Service Implementation
@Service
public class UserServiceImpl extends UserServiceGrpc.UserServiceImplBase {
    @Autowired
    private UserRepository userRepository;
    
    @Override
    public void getUser(GetUserRequest request, StreamObserver<GetUserResponse> responseObserver) {
        User user = userRepository.findById(request.getId());
        
        GetUserResponse response = GetUserResponse.newBuilder()
            .setId(user.getId())
            .setEmail(user.getEmail())
            .setName(user.getName())
            .build();
        
        responseObserver.onNext(response);
        responseObserver.onCompleted();
    }
}

// gRPC Client
@Component
public class UserServiceGrpcClient {
    private final UserServiceGrpc.UserServiceBlockingStub userServiceStub;
    
    public UserServiceGrpcClient() {
        ManagedChannel channel = ManagedChannelBuilder.forAddress("localhost", 9090)
            .usePlaintext()
            .build();
        this.userServiceStub = UserServiceGrpc.newBlockingStub(channel);
    }
    
    public User getUser(Long id) {
        GetUserRequest request = GetUserRequest.newBuilder()
            .setId(id)
            .build();
        
        GetUserResponse response = userServiceStub.getUser(request);
        
        return User.builder()
            .id(response.getId())
            .email(response.getEmail())
            .name(response.getName())
            .build();
    }
}
```

### Timeout and Retry Configuration:

```java
// RestTemplate with timeout configuration
@Configuration
public class RestTemplateConfig {
    @Bean
    public RestTemplate restTemplate() {
        HttpComponentsClientHttpRequestFactory factory = new HttpComponentsClientHttpRequestFactory();
        factory.setConnectTimeout(5000); // 5 seconds
        factory.setReadTimeout(10000);   // 10 seconds
        
        return new RestTemplate(factory);
    }
}

// Retry configuration with Spring Retry
@Service
public class UserServiceClient {
    @Autowired
    private RestTemplate restTemplate;
    
    @Retryable(value = {Exception.class}, maxAttempts = 3, backoff = @Backoff(delay = 1000))
    public User getUser(Long id) {
        ResponseEntity<User> response = restTemplate.getForEntity(
            "http://user-service/api/users/" + id, User.class);
        return response.getBody();
    }
    
    @Recover
    public User getUserFallback(Exception ex, Long id) {
        // Fallback logic
        return User.builder()
            .id(id)
            .name("Unknown User")
            .email("unknown@example.com")
            .build();
    }
}
```

## 3.2 Asynchronous Communication

Asynchronous communication allows services to send messages without waiting for immediate responses. This pattern is useful for decoupling services and improving system resilience.

### Characteristics:

#### 1. **Non-blocking**
The sender doesn't wait for a response.

#### 2. **Decoupling**
Services are loosely coupled through message queues.

#### 3. **Resilience**
System can handle temporary failures gracefully.

#### 4. **Scalability**
Services can process messages at their own pace.

### Implementation with Message Queues:

```java
// Message Publisher
@Service
public class OrderEventPublisher {
    @Autowired
    private RabbitTemplate rabbitTemplate;
    
    public void publishOrderCreated(Order order) {
        OrderCreatedEvent event = OrderCreatedEvent.builder()
            .orderId(order.getId())
            .userId(order.getUserId())
            .totalAmount(order.getTotalAmount())
            .createdAt(order.getCreatedAt())
            .build();
        
        rabbitTemplate.convertAndSend("order.exchange", "order.created", event);
    }
}

// Message Consumer
@Component
public class OrderEventConsumer {
    @Autowired
    private EmailService emailService;
    @Autowired
    private InventoryService inventoryService;
    
    @RabbitListener(queues = "order.created.queue")
    public void handleOrderCreated(OrderCreatedEvent event) {
        // Send confirmation email
        emailService.sendOrderConfirmation(event.getUserId(), event.getOrderId());
        
        // Update inventory
        inventoryService.reserveItems(event.getOrderId());
    }
}
```

### Implementation with Apache Kafka:

```java
// Kafka Producer
@Service
public class OrderEventProducer {
    @Autowired
    private KafkaTemplate<String, Object> kafkaTemplate;
    
    public void publishOrderCreated(Order order) {
        OrderCreatedEvent event = OrderCreatedEvent.builder()
            .orderId(order.getId())
            .userId(order.getUserId())
            .totalAmount(order.getTotalAmount())
            .createdAt(order.getCreatedAt())
            .build();
        
        kafkaTemplate.send("order-created", event);
    }
}

// Kafka Consumer
@Component
public class OrderEventConsumer {
    @Autowired
    private EmailService emailService;
    
    @KafkaListener(topics = "order-created", groupId = "email-service")
    public void handleOrderCreated(OrderCreatedEvent event) {
        emailService.sendOrderConfirmation(event.getUserId(), event.getOrderId());
    }
}
```

## 3.3 Request-Response Pattern

The Request-Response pattern is a fundamental communication pattern where one service sends a request and expects a response from another service.

### Implementation:

```java
// Request DTO
public class GetUserRequest {
    private Long userId;
    private boolean includeProfile;
    private boolean includeOrders;
    
    // Constructors, getters, setters
}

// Response DTO
public class GetUserResponse {
    private Long userId;
    private String email;
    private String name;
    private UserProfile profile;
    private List<Order> orders;
    
    // Constructors, getters, setters
}

// Service Implementation
@RestController
@RequestMapping("/api/users")
public class UserController {
    @Autowired
    private UserService userService;
    
    @PostMapping("/get")
    public ResponseEntity<GetUserResponse> getUser(@RequestBody GetUserRequest request) {
        User user = userService.getUser(request.getUserId());
        
        GetUserResponse response = GetUserResponse.builder()
            .userId(user.getId())
            .email(user.getEmail())
            .name(user.getName())
            .profile(request.isIncludeProfile() ? user.getProfile() : null)
            .orders(request.isIncludeOrders() ? user.getOrders() : null)
            .build();
        
        return ResponseEntity.ok(response);
    }
}
```

### Error Handling:

```java
// Error Response DTO
public class ErrorResponse {
    private String error;
    private String message;
    private String timestamp;
    
    // Constructors, getters, setters
}

// Service with error handling
@RestController
@RequestMapping("/api/users")
public class UserController {
    @Autowired
    private UserService userService;
    
    @GetMapping("/{id}")
    public ResponseEntity<?> getUser(@PathVariable Long id) {
        try {
            User user = userService.findById(id);
            return ResponseEntity.ok(user);
        } catch (UserNotFoundException e) {
            ErrorResponse error = ErrorResponse.builder()
                .error("USER_NOT_FOUND")
                .message("User with id " + id + " not found")
                .timestamp(Instant.now().toString())
                .build();
            return ResponseEntity.status(HttpStatus.NOT_FOUND).body(error);
        } catch (Exception e) {
            ErrorResponse error = ErrorResponse.builder()
                .error("INTERNAL_SERVER_ERROR")
                .message("An unexpected error occurred")
                .timestamp(Instant.now().toString())
                .build();
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(error);
        }
    }
}
```

## 3.4 Event-Driven Communication

Event-driven communication allows services to communicate through events, enabling loose coupling and better scalability.

### Event Definition:

```java
// Base Event
public abstract class DomainEvent {
    private String eventId;
    private Instant timestamp;
    private String eventType;
    
    // Constructors, getters, setters
}

// Specific Events
public class UserCreatedEvent extends DomainEvent {
    private Long userId;
    private String email;
    private String name;
    
    // Constructors, getters, setters
}

public class OrderCreatedEvent extends DomainEvent {
    private Long orderId;
    private Long userId;
    private BigDecimal totalAmount;
    private List<OrderItem> items;
    
    // Constructors, getters, setters
}
```

### Event Publisher:

```java
// Event Publisher Service
@Service
public class EventPublisher {
    @Autowired
    private ApplicationEventPublisher eventPublisher;
    
    public void publishUserCreated(User user) {
        UserCreatedEvent event = UserCreatedEvent.builder()
            .eventId(UUID.randomUUID().toString())
            .timestamp(Instant.now())
            .eventType("USER_CREATED")
            .userId(user.getId())
            .email(user.getEmail())
            .name(user.getName())
            .build();
        
        eventPublisher.publishEvent(event);
    }
    
    public void publishOrderCreated(Order order) {
        OrderCreatedEvent event = OrderCreatedEvent.builder()
            .eventId(UUID.randomUUID().toString())
            .timestamp(Instant.now())
            .eventType("ORDER_CREATED")
            .orderId(order.getId())
            .userId(order.getUserId())
            .totalAmount(order.getTotalAmount())
            .items(order.getItems())
            .build();
        
        eventPublisher.publishEvent(event);
    }
}
```

### Event Handlers:

```java
// Event Handler for User Created
@Component
public class UserCreatedEventHandler {
    @Autowired
    private EmailService emailService;
    @Autowired
    private AnalyticsService analyticsService;
    
    @EventListener
    public void handleUserCreated(UserCreatedEvent event) {
        // Send welcome email
        emailService.sendWelcomeEmail(event.getEmail(), event.getName());
        
        // Track user registration
        analyticsService.trackUserRegistration(event.getUserId());
    }
}

// Event Handler for Order Created
@Component
public class OrderCreatedEventHandler {
    @Autowired
    private InventoryService inventoryService;
    @Autowired
    private PaymentService paymentService;
    @Autowired
    private NotificationService notificationService;
    
    @EventListener
    public void handleOrderCreated(OrderCreatedEvent event) {
        // Reserve inventory
        inventoryService.reserveItems(event.getOrderId(), event.getItems());
        
        // Process payment
        paymentService.processPayment(event.getOrderId(), event.getTotalAmount());
        
        // Send notification
        notificationService.sendOrderConfirmation(event.getUserId(), event.getOrderId());
    }
}
```

## 3.5 Message Queues and Brokers

Message queues provide reliable, asynchronous communication between services. They ensure message delivery and handle failures gracefully.

### RabbitMQ Implementation:

```java
// RabbitMQ Configuration
@Configuration
public class RabbitMQConfig {
    @Bean
    public Queue userCreatedQueue() {
        return QueueBuilder.durable("user.created.queue").build();
    }
    
    @Bean
    public Queue orderCreatedQueue() {
        return QueueBuilder.durable("order.created.queue").build();
    }
    
    @Bean
    public TopicExchange userExchange() {
        return new TopicExchange("user.exchange");
    }
    
    @Bean
    public TopicExchange orderExchange() {
        return new TopicExchange("order.exchange");
    }
    
    @Bean
    public Binding userCreatedBinding() {
        return BindingBuilder.bind(userCreatedQueue())
            .to(userExchange())
            .with("user.created");
    }
    
    @Bean
    public Binding orderCreatedBinding() {
        return BindingBuilder.bind(orderCreatedQueue())
            .to(orderExchange())
            .with("order.created");
    }
}

// Message Producer
@Service
public class MessageProducer {
    @Autowired
    private RabbitTemplate rabbitTemplate;
    
    public void sendUserCreated(UserCreatedEvent event) {
        rabbitTemplate.convertAndSend("user.exchange", "user.created", event);
    }
    
    public void sendOrderCreated(OrderCreatedEvent event) {
        rabbitTemplate.convertAndSend("order.exchange", "order.created", event);
    }
}

// Message Consumer
@Component
public class MessageConsumer {
    @Autowired
    private EmailService emailService;
    
    @RabbitListener(queues = "user.created.queue")
    public void handleUserCreated(UserCreatedEvent event) {
        emailService.sendWelcomeEmail(event.getEmail(), event.getName());
    }
    
    @RabbitListener(queues = "order.created.queue")
    public void handleOrderCreated(OrderCreatedEvent event) {
        // Process order created event
    }
}
```

### Apache Kafka Implementation:

```java
// Kafka Configuration
@Configuration
public class KafkaConfig {
    @Bean
    public ProducerFactory<String, Object> producerFactory() {
        Map<String, Object> configProps = new HashMap<>();
        configProps.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, "localhost:9092");
        configProps.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, StringSerializer.class);
        configProps.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, JsonSerializer.class);
        return new DefaultKafkaProducerFactory<>(configProps);
    }
    
    @Bean
    public KafkaTemplate<String, Object> kafkaTemplate() {
        return new KafkaTemplate<>(producerFactory());
    }
    
    @Bean
    public ConsumerFactory<String, Object> consumerFactory() {
        Map<String, Object> configProps = new HashMap<>();
        configProps.put(ConsumerConfig.BOOTSTRAP_SERVERS_CONFIG, "localhost:9092");
        configProps.put(ConsumerConfig.GROUP_ID_CONFIG, "microservices-group");
        configProps.put(ConsumerConfig.KEY_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class);
        configProps.put(ConsumerConfig.VALUE_DESERIALIZER_CLASS_CONFIG, JsonDeserializer.class);
        return new DefaultKafkaConsumerFactory<>(configProps);
    }
    
    @Bean
    public ConcurrentKafkaListenerContainerFactory<String, Object> kafkaListenerContainerFactory() {
        ConcurrentKafkaListenerContainerFactory<String, Object> factory = new ConcurrentKafkaListenerContainerFactory<>();
        factory.setConsumerFactory(consumerFactory());
        return factory;
    }
}

// Kafka Producer
@Service
public class KafkaProducer {
    @Autowired
    private KafkaTemplate<String, Object> kafkaTemplate;
    
    public void sendUserCreated(UserCreatedEvent event) {
        kafkaTemplate.send("user-created", event);
    }
    
    public void sendOrderCreated(OrderCreatedEvent event) {
        kafkaTemplate.send("order-created", event);
    }
}

// Kafka Consumer
@Component
public class KafkaConsumer {
    @Autowired
    private EmailService emailService;
    
    @KafkaListener(topics = "user-created", groupId = "email-service")
    public void handleUserCreated(UserCreatedEvent event) {
        emailService.sendWelcomeEmail(event.getEmail(), event.getName());
    }
    
    @KafkaListener(topics = "order-created", groupId = "notification-service")
    public void handleOrderCreated(OrderCreatedEvent event) {
        // Process order created event
    }
}
```

## 3.6 Publish-Subscribe Pattern

The Publish-Subscribe pattern allows multiple subscribers to receive messages from a single publisher, enabling one-to-many communication.

### Implementation:

```java
// Event Publisher
@Service
public class EventPublisher {
    @Autowired
    private ApplicationEventPublisher eventPublisher;
    
    public void publishUserRegistered(User user) {
        UserRegisteredEvent event = UserRegisteredEvent.builder()
            .userId(user.getId())
            .email(user.getEmail())
            .name(user.getName())
            .registrationDate(user.getCreatedAt())
            .build();
        
        eventPublisher.publishEvent(event);
    }
}

// Multiple Subscribers
@Component
public class EmailNotificationSubscriber {
    @Autowired
    private EmailService emailService;
    
    @EventListener
    public void handleUserRegistered(UserRegisteredEvent event) {
        emailService.sendWelcomeEmail(event.getEmail(), event.getName());
    }
}

@Component
public class AnalyticsSubscriber {
    @Autowired
    private AnalyticsService analyticsService;
    
    @EventListener
    public void handleUserRegistered(UserRegisteredEvent event) {
        analyticsService.trackUserRegistration(event.getUserId());
    }
}

@Component
public class MarketingSubscriber {
    @Autowired
    private MarketingService marketingService;
    
    @EventListener
    public void handleUserRegistered(UserRegisteredEvent event) {
        marketingService.addToNewsletter(event.getEmail());
    }
}
```

### Topic-based Publish-Subscribe:

```java
// Topic-based Publisher
@Service
public class TopicPublisher {
    @Autowired
    private RabbitTemplate rabbitTemplate;
    
    public void publishUserEvent(String topic, UserEvent event) {
        rabbitTemplate.convertAndSend("user.topic", topic, event);
    }
    
    public void publishOrderEvent(String topic, OrderEvent event) {
        rabbitTemplate.convertAndSend("order.topic", topic, event);
    }
}

// Topic-based Subscribers
@Component
public class UserEventSubscriber {
    @RabbitListener(queues = "user.created.queue")
    public void handleUserCreated(UserCreatedEvent event) {
        // Handle user created
    }
    
    @RabbitListener(queues = "user.updated.queue")
    public void handleUserUpdated(UserUpdatedEvent event) {
        // Handle user updated
    }
    
    @RabbitListener(queues = "user.deleted.queue")
    public void handleUserDeleted(UserDeletedEvent event) {
        // Handle user deleted
    }
}
```

## 3.7 Event Sourcing

Event Sourcing stores the state of an application as a sequence of events, allowing you to reconstruct the current state by replaying events.

### Event Store:

```java
// Event Store Interface
public interface EventStore {
    void saveEvents(String aggregateId, List<DomainEvent> events, int expectedVersion);
    List<DomainEvent> getEvents(String aggregateId);
    List<DomainEvent> getEvents(String aggregateId, int fromVersion);
}

// Event Store Implementation
@Component
public class EventStoreImpl implements EventStore {
    @Autowired
    private EventRepository eventRepository;
    
    @Override
    public void saveEvents(String aggregateId, List<DomainEvent> events, int expectedVersion) {
        List<StoredEvent> storedEvents = eventRepository.findByAggregateId(aggregateId);
        
        if (storedEvents.size() != expectedVersion) {
            throw new ConcurrencyException("Expected version " + expectedVersion + 
                " but found " + storedEvents.size());
        }
        
        for (DomainEvent event : events) {
            StoredEvent storedEvent = StoredEvent.builder()
                .aggregateId(aggregateId)
                .eventType(event.getClass().getSimpleName())
                .eventData(serializeEvent(event))
                .version(storedEvents.size() + 1)
                .timestamp(Instant.now())
                .build();
            
            eventRepository.save(storedEvent);
        }
    }
    
    @Override
    public List<DomainEvent> getEvents(String aggregateId) {
        List<StoredEvent> storedEvents = eventRepository.findByAggregateId(aggregateId);
        return storedEvents.stream()
            .map(this::deserializeEvent)
            .collect(Collectors.toList());
    }
}
```

### Aggregate with Event Sourcing:

```java
// User Aggregate
public class User {
    private Long id;
    private String email;
    private String name;
    private UserStatus status;
    private List<DomainEvent> uncommittedEvents = new ArrayList<>();
    
    public User(Long id, String email, String name) {
        this.id = id;
        this.email = email;
        this.name = name;
        this.status = UserStatus.ACTIVE;
        
        // Add event
        addEvent(new UserCreatedEvent(id, email, name));
    }
    
    public void updateProfile(String name) {
        this.name = name;
        addEvent(new UserProfileUpdatedEvent(id, name));
    }
    
    public void deactivate() {
        this.status = UserStatus.INACTIVE;
        addEvent(new UserDeactivatedEvent(id));
    }
    
    private void addEvent(DomainEvent event) {
        uncommittedEvents.add(event);
    }
    
    public List<DomainEvent> getUncommittedEvents() {
        return new ArrayList<>(uncommittedEvents);
    }
    
    public void markEventsAsCommitted() {
        uncommittedEvents.clear();
    }
}

// User Repository with Event Sourcing
@Repository
public class UserRepository {
    @Autowired
    private EventStore eventStore;
    
    public User findById(Long id) {
        List<DomainEvent> events = eventStore.getEvents(id.toString());
        return User.fromEvents(events);
    }
    
    public void save(User user) {
        List<DomainEvent> events = user.getUncommittedEvents();
        eventStore.saveEvents(user.getId().toString(), events, 0);
        user.markEventsAsCommitted();
    }
}
```

## 3.8 CQRS (Command Query Responsibility Segregation)

CQRS separates read and write operations, allowing different models for commands (writes) and queries (reads).

### Command Side:

```java
// Command
public class CreateUserCommand {
    private String email;
    private String name;
    private String password;
    
    // Constructors, getters, setters
}

// Command Handler
@Component
public class CreateUserCommandHandler {
    @Autowired
    private UserRepository userRepository;
    @Autowired
    private EventPublisher eventPublisher;
    
    public void handle(CreateUserCommand command) {
        User user = new User(command.getEmail(), command.getName(), command.getPassword());
        userRepository.save(user);
        
        eventPublisher.publishUserCreated(user);
    }
}

// Command Controller
@RestController
@RequestMapping("/api/commands")
public class UserCommandController {
    @Autowired
    private CreateUserCommandHandler createUserCommandHandler;
    
    @PostMapping("/users")
    public ResponseEntity<Void> createUser(@RequestBody CreateUserCommand command) {
        createUserCommandHandler.handle(command);
        return ResponseEntity.ok().build();
    }
}
```

### Query Side:

```java
// Query
public class GetUserQuery {
    private Long userId;
    private boolean includeProfile;
    private boolean includeOrders;
    
    // Constructors, getters, setters
}

// Query Handler
@Component
public class GetUserQueryHandler {
    @Autowired
    private UserReadModelRepository userReadModelRepository;
    
    public UserReadModel handle(GetUserQuery query) {
        return userReadModelRepository.findById(query.getUserId());
    }
}

// Query Controller
@RestController
@RequestMapping("/api/queries")
public class UserQueryController {
    @Autowired
    private GetUserQueryHandler getUserQueryHandler;
    
    @GetMapping("/users/{id}")
    public ResponseEntity<UserReadModel> getUser(@PathVariable Long id, 
                                               @RequestParam(defaultValue = "false") boolean includeProfile,
                                               @RequestParam(defaultValue = "false") boolean includeOrders) {
        GetUserQuery query = new GetUserQuery(id, includeProfile, includeOrders);
        UserReadModel user = getUserQueryHandler.handle(query);
        return ResponseEntity.ok(user);
    }
}
```

### Read Model Projection:

```java
// Read Model
@Entity
@Table(name = "user_read_model")
public class UserReadModel {
    @Id
    private Long id;
    private String email;
    private String name;
    private String status;
    private Instant createdAt;
    private Instant lastLoginAt;
    private int totalOrders;
    private BigDecimal totalSpent;
    
    // Constructors, getters, setters
}

// Projection Handler
@Component
public class UserProjectionHandler {
    @Autowired
    private UserReadModelRepository userReadModelRepository;
    
    @EventListener
    public void handleUserCreated(UserCreatedEvent event) {
        UserReadModel readModel = UserReadModel.builder()
            .id(event.getUserId())
            .email(event.getEmail())
            .name(event.getName())
            .status("ACTIVE")
            .createdAt(event.getTimestamp())
            .totalOrders(0)
            .totalSpent(BigDecimal.ZERO)
            .build();
        
        userReadModelRepository.save(readModel);
    }
    
    @EventListener
    public void handleUserProfileUpdated(UserProfileUpdatedEvent event) {
        UserReadModel readModel = userReadModelRepository.findById(event.getUserId());
        if (readModel != null) {
            readModel.setName(event.getName());
            userReadModelRepository.save(readModel);
        }
    }
}
```

This comprehensive guide covers all the essential communication patterns in microservices, providing both theoretical understanding and practical implementation examples. Each pattern is explained with real-world scenarios and Java code examples to make the concepts clear and actionable.