# Section 6 – Data Management in Microservices

## 6.1 Database per Service Pattern

The Database per Service pattern ensures that each microservice has its own database, providing data independence and preventing tight coupling between services.

### Benefits:

#### 1. **Data Independence**
Each service owns and controls its data without interference from other services.

#### 2. **Technology Diversity**
Different services can use different database technologies based on their specific needs.

#### 3. **Scalability**
Each service can scale its database independently based on demand.

#### 4. **Fault Isolation**
Database failures are isolated to specific services, preventing cascading failures.

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
            .driverClassName("com.mysql.cj.jdbc.Driver")
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
            .driverClassName("org.postgresql.Driver")
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
        eventPublisher.publishEvent(new UserCreatedEvent(
            user.getId(), 
            user.getEmail(), 
            user.getName()
        ));
        
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
        UserReference userRef = new UserReference(
            event.getUserId(), 
            event.getEmail(), 
            event.getName()
        );
        // Store user reference locally
    }
}
```

## 6.2 Data Consistency Challenges

Data consistency in microservices is challenging due to the distributed nature of the system and the lack of shared databases.

### Consistency Levels:

#### 1. **Strong Consistency**
All nodes see the same data at the same time.

#### 2. **Eventual Consistency**
Data will eventually be consistent across all nodes.

#### 3. **Weak Consistency**
No guarantee about when data will be consistent.

### Implementation Strategies:

```java
// Strong Consistency with Distributed Transactions
@Service
@Transactional
public class OrderService {
    @Autowired
    private OrderRepository orderRepository;
    @Autowired
    private InventoryService inventoryService;
    @Autowired
    private PaymentService paymentService;
    
    public Order createOrder(OrderRequest request) {
        // Start distributed transaction
        try {
            // Reserve inventory
            inventoryService.reserveInventory(request.getProductId(), request.getQuantity());
            
            // Process payment
            paymentService.processPayment(request.getPaymentInfo());
            
            // Create order
            Order order = orderRepository.save(new Order(request));
            
            // Commit transaction
            return order;
        } catch (Exception e) {
            // Rollback transaction
            throw new OrderCreationException("Failed to create order", e);
        }
    }
}

// Eventual Consistency with Event Sourcing
@Service
public class OrderService {
    @Autowired
    private EventStore eventStore;
    
    public Order createOrder(OrderRequest request) {
        // Create events instead of direct database updates
        List<DomainEvent> events = Arrays.asList(
            new OrderCreatedEvent(request.getOrderId(), request.getUserId()),
            new InventoryReservedEvent(request.getProductId(), request.getQuantity()),
            new PaymentProcessedEvent(request.getPaymentInfo())
        );
        
        // Store events
        eventStore.saveEvents(request.getOrderId().toString(), events);
        
        // Events will be processed asynchronously
        return new Order(request);
    }
}
```

## 6.3 Eventual Consistency

Eventual consistency is a consistency model where the system will eventually become consistent, but there's no guarantee about when.

### Implementation:

```java
// Event-driven eventual consistency
@Service
public class UserService {
    @Autowired
    private UserRepository userRepository;
    @Autowired
    private EventPublisher eventPublisher;
    
    public User updateUser(Long id, UserRequest request) {
        User user = userRepository.findById(id);
        user.setName(request.getName());
        user.setEmail(request.getEmail());
        
        User updatedUser = userRepository.save(user);
        
        // Publish event for eventual consistency
        eventPublisher.publishEvent(new UserUpdatedEvent(
            user.getId(), 
            user.getName(), 
            user.getEmail()
        ));
        
        return updatedUser;
    }
}

// Order Service - Eventually consistent with User Service
@EventListener
public class OrderService {
    @Autowired
    private OrderRepository orderRepository;
    
    public void handleUserUpdated(UserUpdatedEvent event) {
        // Update user information in order service
        List<Order> orders = orderRepository.findByUserId(event.getUserId());
        for (Order order : orders) {
            order.setUserName(event.getName());
            order.setUserEmail(event.getEmail());
        }
        orderRepository.saveAll(orders);
    }
}
```

### Conflict Resolution:

```java
// Conflict resolution for eventual consistency
@Service
public class ConflictResolver {
    public User resolveUserConflict(User localUser, User remoteUser) {
        // Use timestamp-based conflict resolution
        if (localUser.getLastModified().isAfter(remoteUser.getLastModified())) {
            return localUser;
        } else if (remoteUser.getLastModified().isAfter(localUser.getLastModified())) {
            return remoteUser;
        } else {
            // Use business rules for conflict resolution
            return resolveByBusinessRules(localUser, remoteUser);
        }
    }
    
    private User resolveByBusinessRules(User localUser, User remoteUser) {
        // Business-specific conflict resolution logic
        if (localUser.getVersion() > remoteUser.getVersion()) {
            return localUser;
        } else {
            return remoteUser;
        }
    }
}
```

## 6.4 Saga Pattern for Distributed Transactions

The Saga pattern manages distributed transactions by breaking them into a series of local transactions with compensating actions.

### Choreography-based Saga:

```java
// Saga Events
public class OrderSagaEvent {
    private String sagaId;
    private String eventType;
    private Object payload;
    private Instant timestamp;
    
    // Constructors, getters, setters
}

// Order Saga
@Service
public class OrderSaga {
    @Autowired
    private EventPublisher eventPublisher;
    
    public void startOrderSaga(OrderRequest request) {
        String sagaId = UUID.randomUUID().toString();
        
        // Start saga
        eventPublisher.publishEvent(new OrderSagaEvent(
            sagaId, 
            "ORDER_CREATED", 
            request
        ));
    }
    
    @EventListener
    public void handleOrderCreated(OrderSagaEvent event) {
        // Reserve inventory
        eventPublisher.publishEvent(new OrderSagaEvent(
            event.getSagaId(), 
            "INVENTORY_RESERVE_REQUESTED", 
            event.getPayload()
        ));
    }
    
    @EventListener
    public void handleInventoryReserved(OrderSagaEvent event) {
        // Process payment
        eventPublisher.publishEvent(new OrderSagaEvent(
            event.getSagaId(), 
            "PAYMENT_PROCESS_REQUESTED", 
            event.getPayload()
        ));
    }
    
    @EventListener
    public void handlePaymentProcessed(OrderSagaEvent event) {
        // Complete order
        eventPublisher.publishEvent(new OrderSagaEvent(
            event.getSagaId(), 
            "ORDER_COMPLETED", 
            event.getPayload()
        ));
    }
    
    @EventListener
    public void handleInventoryReservationFailed(OrderSagaEvent event) {
        // Compensate - cancel order
        eventPublisher.publishEvent(new OrderSagaEvent(
            event.getSagaId(), 
            "ORDER_CANCELLED", 
            event.getPayload()
        ));
    }
}
```

### Orchestration-based Saga:

```java
// Saga Orchestrator
@Service
public class OrderSagaOrchestrator {
    @Autowired
    private InventoryService inventoryService;
    @Autowired
    private PaymentService paymentService;
    @Autowired
    private OrderService orderService;
    
    public void executeOrderSaga(OrderRequest request) {
        String sagaId = UUID.randomUUID().toString();
        List<SagaStep> steps = new ArrayList<>();
        
        try {
            // Step 1: Reserve inventory
            steps.add(new SagaStep("RESERVE_INVENTORY", () -> {
                inventoryService.reserveInventory(request.getProductId(), request.getQuantity());
            }, () -> {
                inventoryService.releaseInventory(request.getProductId(), request.getQuantity());
            }));
            
            // Step 2: Process payment
            steps.add(new SagaStep("PROCESS_PAYMENT", () -> {
                paymentService.processPayment(request.getPaymentInfo());
            }, () -> {
                paymentService.refundPayment(request.getPaymentInfo());
            }));
            
            // Step 3: Create order
            steps.add(new SagaStep("CREATE_ORDER", () -> {
                orderService.createOrder(request);
            }, () -> {
                orderService.cancelOrder(request.getOrderId());
            }));
            
            // Execute saga steps
            executeSagaSteps(steps);
            
        } catch (Exception e) {
            // Compensate for completed steps
            compensateSagaSteps(steps);
            throw new OrderSagaException("Order saga failed", e);
        }
    }
    
    private void executeSagaSteps(List<SagaStep> steps) {
        for (SagaStep step : steps) {
            step.execute();
        }
    }
    
    private void compensateSagaSteps(List<SagaStep> steps) {
        // Execute compensation in reverse order
        Collections.reverse(steps);
        for (SagaStep step : steps) {
            try {
                step.compensate();
            } catch (Exception e) {
                log.error("Compensation failed for step: {}", step.getName(), e);
            }
        }
    }
}

// Saga Step
public class SagaStep {
    private String name;
    private Runnable action;
    private Runnable compensation;
    
    public SagaStep(String name, Runnable action, Runnable compensation) {
        this.name = name;
        this.action = action;
        this.compensation = compensation;
    }
    
    public void execute() {
        action.run();
    }
    
    public void compensate() {
        compensation.run();
    }
    
    // Getters
}
```

## 6.5 Two-Phase Commit (2PC) vs Saga

### Two-Phase Commit (2PC):

```java
// 2PC Coordinator
@Service
public class TwoPhaseCommitCoordinator {
    @Autowired
    private List<Participant> participants;
    
    public void executeTransaction(TransactionRequest request) {
        String transactionId = UUID.randomUUID().toString();
        
        try {
            // Phase 1: Prepare
            List<Boolean> prepareResults = new ArrayList<>();
            for (Participant participant : participants) {
                boolean prepared = participant.prepare(transactionId, request);
                prepareResults.add(prepared);
            }
            
            // Phase 2: Commit or Abort
            if (prepareResults.stream().allMatch(Boolean::booleanValue)) {
                // All participants prepared successfully - commit
                for (Participant participant : participants) {
                    participant.commit(transactionId);
                }
            } else {
                // Some participants failed to prepare - abort
                for (Participant participant : participants) {
                    participant.abort(transactionId);
                }
            }
        } catch (Exception e) {
            // Abort on any exception
            for (Participant participant : participants) {
                participant.abort(transactionId);
            }
            throw new TransactionException("Transaction failed", e);
        }
    }
}

// Participant Interface
public interface Participant {
    boolean prepare(String transactionId, TransactionRequest request);
    void commit(String transactionId);
    void abort(String transactionId);
}
```

### Comparison:

| Aspect | 2PC | Saga |
|--------|-----|------|
| **Consistency** | Strong | Eventual |
| **Performance** | Slow (blocking) | Fast (non-blocking) |
| **Scalability** | Poor | Good |
| **Complexity** | Low | High |
| **Failure Handling** | Automatic rollback | Manual compensation |

## 6.6 Event Sourcing for Data Management

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
    
    // Reconstruct from events
    public static User fromEvents(List<DomainEvent> events) {
        User user = new User();
        for (DomainEvent event : events) {
            user.apply(event);
        }
        return user;
    }
    
    private void apply(DomainEvent event) {
        if (event instanceof UserCreatedEvent) {
            UserCreatedEvent e = (UserCreatedEvent) event;
            this.id = e.getUserId();
            this.email = e.getEmail();
            this.name = e.getName();
            this.status = UserStatus.ACTIVE;
        } else if (event instanceof UserProfileUpdatedEvent) {
            UserProfileUpdatedEvent e = (UserProfileUpdatedEvent) event;
            this.name = e.getName();
        } else if (event instanceof UserDeactivatedEvent) {
            this.status = UserStatus.INACTIVE;
        }
    }
}
```

## 6.7 CQRS Implementation

CQRS (Command Query Responsibility Segregation) separates read and write operations, allowing different models for commands and queries.

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

## 6.8 Data Replication Strategies

Data replication ensures data availability and improves performance by maintaining copies of data across multiple locations.

### Master-Slave Replication:

```java
// Master-Slave Configuration
@Configuration
public class MasterSlaveConfig {
    @Bean
    @Primary
    public DataSource masterDataSource() {
        return DataSourceBuilder.create()
            .url("jdbc:mysql://master-db:3306/user_db")
            .username("master")
            .password("password")
            .build();
    }
    
    @Bean
    public DataSource slaveDataSource() {
        return DataSourceBuilder.create()
            .url("jdbc:mysql://slave-db:3306/user_db")
            .username("slave")
            .password("password")
            .build();
    }
}

// Read-Write Splitting
@Service
public class UserService {
    @Autowired
    @Qualifier("masterDataSource")
    private DataSource masterDataSource;
    
    @Autowired
    @Qualifier("slaveDataSource")
    private DataSource slaveDataSource;
    
    public User createUser(UserRequest request) {
        // Write to master
        JdbcTemplate masterTemplate = new JdbcTemplate(masterDataSource);
        // Create user logic
        return user;
    }
    
    public User getUser(Long id) {
        // Read from slave
        JdbcTemplate slaveTemplate = new JdbcTemplate(slaveDataSource);
        // Get user logic
        return user;
    }
}
```

### Event-Driven Replication:

```java
// Event-Driven Replication
@Service
public class DataReplicationService {
    @Autowired
    private EventPublisher eventPublisher;
    
    public void replicateUserData(User user) {
        UserReplicationEvent event = UserReplicationEvent.builder()
            .userId(user.getId())
            .email(user.getEmail())
            .name(user.getName())
            .status(user.getStatus())
            .timestamp(Instant.now())
            .build();
        
        eventPublisher.publishEvent(event);
    }
}

// Replication Event Handler
@EventListener
public class UserReplicationHandler {
    @Autowired
    private UserReplicationRepository replicationRepository;
    
    public void handleUserReplication(UserReplicationEvent event) {
        UserReplication replication = UserReplication.builder()
            .userId(event.getUserId())
            .email(event.getEmail())
            .name(event.getName())
            .status(event.getStatus())
            .replicatedAt(event.getTimestamp())
            .build();
        
        replicationRepository.save(replication);
    }
}
```

This comprehensive guide covers all aspects of data management in microservices, providing both theoretical understanding and practical implementation examples. Each concept is explained with real-world scenarios and Java code examples to make the concepts clear and actionable.