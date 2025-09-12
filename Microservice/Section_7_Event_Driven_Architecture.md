# Section 7 – Event-Driven Architecture

## 7.1 Event-Driven Microservices Design

Event-driven architecture is a design pattern where microservices communicate through events, enabling loose coupling and better scalability. Events represent something that has happened in the system and can trigger reactions in other services.

### Key Concepts:

#### 1. **Events**
Something that has happened in the system that other services might be interested in.

#### 2. **Event Publishers**
Services that publish events when something significant happens.

#### 3. **Event Subscribers**
Services that listen for and react to events.

#### 4. **Event Store**
A persistent store for events that can be replayed and queried.

### Event Definition:

```java
// Base Event Interface
public interface DomainEvent {
    String getEventId();
    Instant getTimestamp();
    String getEventType();
}

// Specific Events
public class UserCreatedEvent implements DomainEvent {
    private String eventId;
    private Instant timestamp;
    private Long userId;
    private String email;
    private String name;
    
    public UserCreatedEvent(Long userId, String email, String name) {
        this.eventId = UUID.randomUUID().toString();
        this.timestamp = Instant.now();
        this.userId = userId;
        this.email = email;
        this.name = name;
    }
    
    // Getters
    @Override
    public String getEventId() { return eventId; }
    
    @Override
    public Instant getTimestamp() { return timestamp; }
    
    @Override
    public String getEventType() { return "USER_CREATED"; }
}

public class OrderCreatedEvent implements DomainEvent {
    private String eventId;
    private Instant timestamp;
    private Long orderId;
    private Long userId;
    private BigDecimal totalAmount;
    private List<OrderItem> items;
    
    public OrderCreatedEvent(Long orderId, Long userId, BigDecimal totalAmount, List<OrderItem> items) {
        this.eventId = UUID.randomUUID().toString();
        this.timestamp = Instant.now();
        this.orderId = orderId;
        this.userId = userId;
        this.totalAmount = totalAmount;
        this.items = items;
    }
    
    // Getters
    @Override
    public String getEventId() { return eventId; }
    
    @Override
    public Instant getTimestamp() { return timestamp; }
    
    @Override
    public String getEventType() { return "ORDER_CREATED"; }
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
        UserCreatedEvent event = new UserCreatedEvent(
            user.getId(), 
            user.getEmail(), 
            user.getName()
        );
        
        eventPublisher.publishEvent(event);
        log.info("Published UserCreatedEvent for user: {}", user.getId());
    }
    
    public void publishOrderCreated(Order order) {
        OrderCreatedEvent event = new OrderCreatedEvent(
            order.getId(),
            order.getUserId(),
            order.getTotalAmount(),
            order.getItems()
        );
        
        eventPublisher.publishEvent(event);
        log.info("Published OrderCreatedEvent for order: {}", order.getId());
    }
    
    public void publishUserUpdated(User user) {
        UserUpdatedEvent event = new UserUpdatedEvent(
            user.getId(),
            user.getEmail(),
            user.getName()
        );
        
        eventPublisher.publishEvent(event);
        log.info("Published UserUpdatedEvent for user: {}", user.getId());
    }
}
```

### Event Handlers:

```java
// User Event Handlers
@Component
public class UserEventHandler {
    @Autowired
    private EmailService emailService;
    @Autowired
    private AnalyticsService analyticsService;
    @Autowired
    private NotificationService notificationService;
    
    @EventListener
    public void handleUserCreated(UserCreatedEvent event) {
        log.info("Handling UserCreatedEvent for user: {}", event.getUserId());
        
        // Send welcome email
        emailService.sendWelcomeEmail(event.getEmail(), event.getName());
        
        // Track user registration
        analyticsService.trackUserRegistration(event.getUserId());
        
        // Send push notification
        notificationService.sendWelcomeNotification(event.getUserId());
    }
    
    @EventListener
    public void handleUserUpdated(UserUpdatedEvent event) {
        log.info("Handling UserUpdatedEvent for user: {}", event.getUserId());
        
        // Update user profile in other services
        analyticsService.updateUserProfile(event.getUserId(), event.getName());
        
        // Send profile update notification
        notificationService.sendProfileUpdateNotification(event.getUserId());
    }
}

// Order Event Handlers
@Component
public class OrderEventHandler {
    @Autowired
    private InventoryService inventoryService;
    @Autowired
    private PaymentService paymentService;
    @Autowired
    private ShippingService shippingService;
    @Autowired
    private NotificationService notificationService;
    
    @EventListener
    public void handleOrderCreated(OrderCreatedEvent event) {
        log.info("Handling OrderCreatedEvent for order: {}", event.getOrderId());
        
        // Reserve inventory
        inventoryService.reserveInventory(event.getOrderId(), event.getItems());
        
        // Process payment
        paymentService.processPayment(event.getOrderId(), event.getTotalAmount());
        
        // Send order confirmation
        notificationService.sendOrderConfirmation(event.getUserId(), event.getOrderId());
    }
    
    @EventListener
    public void handleOrderCancelled(OrderCancelledEvent event) {
        log.info("Handling OrderCancelledEvent for order: {}", event.getOrderId());
        
        // Release inventory
        inventoryService.releaseInventory(event.getOrderId());
        
        // Process refund
        paymentService.processRefund(event.getOrderId());
        
        // Send cancellation notification
        notificationService.sendOrderCancellationNotification(event.getUserId(), event.getOrderId());
    }
}
```

## 7.2 Event Streaming Platforms

Event streaming platforms provide the infrastructure for publishing, storing, and consuming events at scale.

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
        configProps.put(ProducerConfig.ACKS_CONFIG, "all");
        configProps.put(ProducerConfig.RETRIES_CONFIG, 3);
        configProps.put(ProducerConfig.ENABLE_IDEMPOTENCE_CONFIG, true);
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
        configProps.put(ConsumerConfig.AUTO_OFFSET_RESET_CONFIG, "earliest");
        configProps.put(ConsumerConfig.ENABLE_AUTO_COMMIT_CONFIG, false);
        return new DefaultKafkaConsumerFactory<>(configProps);
    }
    
    @Bean
    public ConcurrentKafkaListenerContainerFactory<String, Object> kafkaListenerContainerFactory() {
        ConcurrentKafkaListenerContainerFactory<String, Object> factory = new ConcurrentKafkaListenerContainerFactory<>();
        factory.setConsumerFactory(consumerFactory());
        factory.setConcurrency(3);
        return factory;
    }
}

// Kafka Producer
@Service
public class KafkaEventProducer {
    @Autowired
    private KafkaTemplate<String, Object> kafkaTemplate;
    
    public void publishUserCreated(UserCreatedEvent event) {
        kafkaTemplate.send("user-created", event.getUserId().toString(), event);
        log.info("Published UserCreatedEvent to Kafka: {}", event.getUserId());
    }
    
    public void publishOrderCreated(OrderCreatedEvent event) {
        kafkaTemplate.send("order-created", event.getOrderId().toString(), event);
        log.info("Published OrderCreatedEvent to Kafka: {}", event.getOrderId());
    }
    
    public void publishUserUpdated(UserUpdatedEvent event) {
        kafkaTemplate.send("user-updated", event.getUserId().toString(), event);
        log.info("Published UserUpdatedEvent to Kafka: {}", event.getUserId());
    }
}

// Kafka Consumer
@Component
public class KafkaEventConsumer {
    @Autowired
    private EmailService emailService;
    @Autowired
    private AnalyticsService analyticsService;
    
    @KafkaListener(topics = "user-created", groupId = "email-service")
    public void handleUserCreated(UserCreatedEvent event) {
        log.info("Received UserCreatedEvent from Kafka: {}", event.getUserId());
        emailService.sendWelcomeEmail(event.getEmail(), event.getName());
    }
    
    @KafkaListener(topics = "user-created", groupId = "analytics-service")
    public void handleUserCreatedForAnalytics(UserCreatedEvent event) {
        log.info("Received UserCreatedEvent from Kafka for analytics: {}", event.getUserId());
        analyticsService.trackUserRegistration(event.getUserId());
    }
    
    @KafkaListener(topics = "order-created", groupId = "notification-service")
    public void handleOrderCreated(OrderCreatedEvent event) {
        log.info("Received OrderCreatedEvent from Kafka: {}", event.getOrderId());
        // Handle order created event
    }
}
```

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

// RabbitMQ Producer
@Service
public class RabbitMQEventProducer {
    @Autowired
    private RabbitTemplate rabbitTemplate;
    
    public void publishUserCreated(UserCreatedEvent event) {
        rabbitTemplate.convertAndSend("user.exchange", "user.created", event);
        log.info("Published UserCreatedEvent to RabbitMQ: {}", event.getUserId());
    }
    
    public void publishOrderCreated(OrderCreatedEvent event) {
        rabbitTemplate.convertAndSend("order.exchange", "order.created", event);
        log.info("Published OrderCreatedEvent to RabbitMQ: {}", event.getOrderId());
    }
}

// RabbitMQ Consumer
@Component
public class RabbitMQEventConsumer {
    @Autowired
    private EmailService emailService;
    
    @RabbitListener(queues = "user.created.queue")
    public void handleUserCreated(UserCreatedEvent event) {
        log.info("Received UserCreatedEvent from RabbitMQ: {}", event.getUserId());
        emailService.sendWelcomeEmail(event.getEmail(), event.getName());
    }
    
    @RabbitListener(queues = "order.created.queue")
    public void handleOrderCreated(OrderCreatedEvent event) {
        log.info("Received OrderCreatedEvent from RabbitMQ: {}", event.getOrderId());
        // Handle order created event
    }
}
```

## 7.3 Apache Kafka for Microservices

Apache Kafka is a distributed streaming platform that is particularly well-suited for microservices event-driven architecture.

### Kafka Topics and Partitions:

```java
// Kafka Topic Configuration
@Configuration
public class KafkaTopicConfig {
    @Bean
    public NewTopic userCreatedTopic() {
        return TopicBuilder.name("user-created")
            .partitions(3)
            .replicas(1)
            .config(TopicConfig.RETENTION_MS_CONFIG, "604800000") // 7 days
            .build();
    }
    
    @Bean
    public NewTopic orderCreatedTopic() {
        return TopicBuilder.name("order-created")
            .partitions(6)
            .replicas(1)
            .config(TopicConfig.RETENTION_MS_CONFIG, "2592000000") // 30 days
            .build();
    }
    
    @Bean
    public NewTopic userUpdatedTopic() {
        return TopicBuilder.name("user-updated")
            .partitions(3)
            .replicas(1)
            .config(TopicConfig.RETENTION_MS_CONFIG, "604800000") // 7 days
            .build();
    }
}

// Kafka Producer with Partitioning
@Service
public class KafkaEventProducer {
    @Autowired
    private KafkaTemplate<String, Object> kafkaTemplate;
    
    public void publishUserCreated(UserCreatedEvent event) {
        // Use user ID as key for partitioning
        kafkaTemplate.send("user-created", event.getUserId().toString(), event);
        log.info("Published UserCreatedEvent to Kafka: {}", event.getUserId());
    }
    
    public void publishOrderCreated(OrderCreatedEvent event) {
        // Use order ID as key for partitioning
        kafkaTemplate.send("order-created", event.getOrderId().toString(), event);
        log.info("Published OrderCreatedEvent to Kafka: {}", event.getOrderId());
    }
}
```

### Kafka Consumer Groups:

```java
// Consumer Group Configuration
@Configuration
public class KafkaConsumerConfig {
    @Bean
    public ConsumerFactory<String, Object> emailServiceConsumerFactory() {
        Map<String, Object> configProps = new HashMap<>();
        configProps.put(ConsumerConfig.BOOTSTRAP_SERVERS_CONFIG, "localhost:9092");
        configProps.put(ConsumerConfig.GROUP_ID_CONFIG, "email-service");
        configProps.put(ConsumerConfig.KEY_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class);
        configProps.put(ConsumerConfig.VALUE_DESERIALIZER_CLASS_CONFIG, JsonDeserializer.class);
        configProps.put(ConsumerConfig.AUTO_OFFSET_RESET_CONFIG, "earliest");
        configProps.put(ConsumerConfig.ENABLE_AUTO_COMMIT_CONFIG, false);
        return new DefaultKafkaConsumerFactory<>(configProps);
    }
    
    @Bean
    public ConcurrentKafkaListenerContainerFactory<String, Object> emailServiceKafkaListenerContainerFactory() {
        ConcurrentKafkaListenerContainerFactory<String, Object> factory = new ConcurrentKafkaListenerContainerFactory<>();
        factory.setConsumerFactory(emailServiceConsumerFactory());
        factory.setConcurrency(3);
        return factory;
    }
}

// Email Service Consumer
@Component
public class EmailServiceConsumer {
    @Autowired
    private EmailService emailService;
    
    @KafkaListener(topics = "user-created", groupId = "email-service")
    public void handleUserCreated(UserCreatedEvent event) {
        log.info("Email service received UserCreatedEvent: {}", event.getUserId());
        emailService.sendWelcomeEmail(event.getEmail(), event.getName());
    }
    
    @KafkaListener(topics = "user-updated", groupId = "email-service")
    public void handleUserUpdated(UserUpdatedEvent event) {
        log.info("Email service received UserUpdatedEvent: {}", event.getUserId());
        emailService.sendProfileUpdateEmail(event.getEmail(), event.getName());
    }
}

// Analytics Service Consumer
@Component
public class AnalyticsServiceConsumer {
    @Autowired
    private AnalyticsService analyticsService;
    
    @KafkaListener(topics = "user-created", groupId = "analytics-service")
    public void handleUserCreated(UserCreatedEvent event) {
        log.info("Analytics service received UserCreatedEvent: {}", event.getUserId());
        analyticsService.trackUserRegistration(event.getUserId());
    }
    
    @KafkaListener(topics = "order-created", groupId = "analytics-service")
    public void handleOrderCreated(OrderCreatedEvent event) {
        log.info("Analytics service received OrderCreatedEvent: {}", event.getOrderId());
        analyticsService.trackOrderCreation(event.getOrderId(), event.getUserId());
    }
}
```

## 7.4 Event Schema Evolution

Event schema evolution allows you to modify event schemas over time while maintaining backward compatibility.

### Schema Registry Integration:

```java
// Schema Registry Configuration
@Configuration
public class SchemaRegistryConfig {
    @Bean
    public SchemaRegistryClient schemaRegistryClient() {
        return new CachedSchemaRegistryClient("http://localhost:8081", 100);
    }
    
    @Bean
    public KafkaAvroSerializer kafkaAvroSerializer() {
        return new KafkaAvroSerializer(schemaRegistryClient());
    }
    
    @Bean
    public KafkaAvroDeserializer kafkaAvroDeserializer() {
        return new KafkaAvroDeserializer(schemaRegistryClient());
    }
}

// Avro Schema Definition
@AvroSchema("""
    {
        "type": "record",
        "name": "UserCreatedEvent",
        "namespace": "com.example.events",
        "fields": [
            {"name": "eventId", "type": "string"},
            {"name": "timestamp", "type": "long", "logicalType": "timestamp-millis"},
            {"name": "userId", "type": "long"},
            {"name": "email", "type": "string"},
            {"name": "name", "type": "string"}
        ]
    }
    """)
public class UserCreatedEventAvro {
    private String eventId;
    private long timestamp;
    private long userId;
    private String email;
    private String name;
    
    // Constructors, getters, setters
}

// Schema Evolution Example
@AvroSchema("""
    {
        "type": "record",
        "name": "UserCreatedEvent",
        "namespace": "com.example.events",
        "fields": [
            {"name": "eventId", "type": "string"},
            {"name": "timestamp", "type": "long", "logicalType": "timestamp-millis"},
            {"name": "userId", "type": "long"},
            {"name": "email", "type": "string"},
            {"name": "name", "type": "string"},
            {"name": "phoneNumber", "type": ["null", "string"], "default": null}
        ]
    }
    """)
public class UserCreatedEventAvroV2 {
    private String eventId;
    private long timestamp;
    private long userId;
    private String email;
    private String name;
    private String phoneNumber; // New optional field
    
    // Constructors, getters, setters
}
```

### Backward Compatibility:

```java
// Event Versioning
public class UserCreatedEvent {
    private String eventId;
    private Instant timestamp;
    private Long userId;
    private String email;
    private String name;
    private String phoneNumber; // New field with default value
    
    public UserCreatedEvent(Long userId, String email, String name) {
        this.eventId = UUID.randomUUID().toString();
        this.timestamp = Instant.now();
        this.userId = userId;
        this.email = email;
        this.name = name;
        this.phoneNumber = null; // Default value for backward compatibility
    }
    
    public UserCreatedEvent(Long userId, String email, String name, String phoneNumber) {
        this.eventId = UUID.randomUUID().toString();
        this.timestamp = Instant.now();
        this.userId = userId;
        this.email = email;
        this.name = name;
        this.phoneNumber = phoneNumber;
    }
    
    // Getters and setters
}

// Event Deserializer with Version Handling
@Component
public class EventDeserializer {
    public DomainEvent deserializeEvent(String eventType, byte[] eventData) {
        switch (eventType) {
            case "USER_CREATED":
                return deserializeUserCreatedEvent(eventData);
            case "USER_CREATED_V2":
                return deserializeUserCreatedEventV2(eventData);
            default:
                throw new UnsupportedEventTypeException("Unknown event type: " + eventType);
        }
    }
    
    private UserCreatedEvent deserializeUserCreatedEvent(byte[] eventData) {
        // Deserialize V1 event
        return objectMapper.readValue(eventData, UserCreatedEvent.class);
    }
    
    private UserCreatedEvent deserializeUserCreatedEventV2(byte[] eventData) {
        // Deserialize V2 event
        return objectMapper.readValue(eventData, UserCreatedEvent.class);
    }
}
```

## 7.5 Event Ordering and Partitioning

Event ordering and partitioning ensure that related events are processed in the correct order.

### Partitioning Strategy:

```java
// Custom Partitioner
@Component
public class EventPartitioner implements Partitioner {
    @Override
    public int partition(String topic, Object key, byte[] keyBytes, Object value, byte[] valueBytes, Cluster cluster) {
        if (key == null) {
            return 0; // Default partition for null keys
        }
        
        // Use key hash for partitioning
        return Math.abs(key.hashCode()) % cluster.partitionCountForTopic(topic);
    }
    
    @Override
    public void close() {
        // Cleanup resources
    }
    
    @Override
    public void configure(Map<String, ?> configs) {
        // Configure partitioner
    }
}

// Event Producer with Partitioning
@Service
public class EventProducer {
    @Autowired
    private KafkaTemplate<String, Object> kafkaTemplate;
    
    public void publishUserEvent(UserEvent event) {
        // Use user ID as key to ensure events for same user go to same partition
        String key = event.getUserId().toString();
        kafkaTemplate.send("user-events", key, event);
    }
    
    public void publishOrderEvent(OrderEvent event) {
        // Use order ID as key to ensure events for same order go to same partition
        String key = event.getOrderId().toString();
        kafkaTemplate.send("order-events", key, event);
    }
}
```

### Event Ordering:

```java
// Event Ordering Service
@Service
public class EventOrderingService {
    private final Map<String, Long> eventSequences = new ConcurrentHashMap<>();
    
    public void processEvent(String partitionKey, DomainEvent event) {
        // Get current sequence number for partition
        Long currentSequence = eventSequences.getOrDefault(partitionKey, 0L);
        
        // Check if event is in order
        if (event.getSequenceNumber() > currentSequence) {
            // Process event
            processEventInOrder(event);
            
            // Update sequence number
            eventSequences.put(partitionKey, event.getSequenceNumber());
        } else {
            // Event is out of order, queue for later processing
            queueOutOfOrderEvent(partitionKey, event);
        }
    }
    
    private void processEventInOrder(DomainEvent event) {
        // Process event
        log.info("Processing event in order: {}", event.getEventId());
    }
    
    private void queueOutOfOrderEvent(String partitionKey, DomainEvent event) {
        // Queue event for later processing
        log.warn("Event out of order, queuing: {}", event.getEventId());
    }
}
```

## 7.6 Event Sourcing Patterns

Event sourcing stores the state of an application as a sequence of events, allowing you to reconstruct the current state by replaying events.

### Event Store Implementation:

```java
// Event Store
@Component
public class EventStore {
    @Autowired
    private EventRepository eventRepository;
    
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
    
    public List<DomainEvent> getEvents(String aggregateId) {
        List<StoredEvent> storedEvents = eventRepository.findByAggregateId(aggregateId);
        return storedEvents.stream()
            .map(this::deserializeEvent)
            .collect(Collectors.toList());
    }
    
    public List<DomainEvent> getEvents(String aggregateId, int fromVersion) {
        List<StoredEvent> storedEvents = eventRepository.findByAggregateIdAndVersionGreaterThan(aggregateId, fromVersion);
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

## 7.7 Event Store Implementation

Event store is a specialized database for storing events in an event-sourced system.

### Event Store Database Schema:

```sql
-- Event Store Table
CREATE TABLE event_store (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    aggregate_id VARCHAR(255) NOT NULL,
    event_type VARCHAR(255) NOT NULL,
    event_data TEXT NOT NULL,
    version INT NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    INDEX idx_aggregate_id (aggregate_id),
    INDEX idx_timestamp (timestamp)
);

-- Event Store Repository
@Repository
public class EventRepository {
    @Autowired
    private JdbcTemplate jdbcTemplate;
    
    public void save(StoredEvent event) {
        String sql = "INSERT INTO event_store (aggregate_id, event_type, event_data, version, timestamp) VALUES (?, ?, ?, ?, ?)";
        jdbcTemplate.update(sql, 
            event.getAggregateId(), 
            event.getEventType(), 
            event.getEventData(), 
            event.getVersion(), 
            event.getTimestamp());
    }
    
    public List<StoredEvent> findByAggregateId(String aggregateId) {
        String sql = "SELECT * FROM event_store WHERE aggregate_id = ? ORDER BY version";
        return jdbcTemplate.query(sql, new Object[]{aggregateId}, new StoredEventRowMapper());
    }
    
    public List<StoredEvent> findByAggregateIdAndVersionGreaterThan(String aggregateId, int version) {
        String sql = "SELECT * FROM event_store WHERE aggregate_id = ? AND version > ? ORDER BY version";
        return jdbcTemplate.query(sql, new Object[]{aggregateId, version}, new StoredEventRowMapper());
    }
}
```

### Event Store Service:

```java
// Event Store Service
@Service
public class EventStoreService {
    @Autowired
    private EventRepository eventRepository;
    @Autowired
    private ObjectMapper objectMapper;
    
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
    
    public List<DomainEvent> getEvents(String aggregateId) {
        List<StoredEvent> storedEvents = eventRepository.findByAggregateId(aggregateId);
        return storedEvents.stream()
            .map(this::deserializeEvent)
            .collect(Collectors.toList());
    }
    
    private String serializeEvent(DomainEvent event) {
        try {
            return objectMapper.writeValueAsString(event);
        } catch (Exception e) {
            throw new EventSerializationException("Failed to serialize event", e);
        }
    }
    
    private DomainEvent deserializeEvent(StoredEvent storedEvent) {
        try {
            Class<?> eventClass = Class.forName(storedEvent.getEventType());
            return (DomainEvent) objectMapper.readValue(storedEvent.getEventData(), eventClass);
        } catch (Exception e) {
            throw new EventDeserializationException("Failed to deserialize event", e);
        }
    }
}
```

## 7.8 Event Replay and Recovery

Event replay allows you to reconstruct the state of an application by replaying events from the event store.

### Event Replay Service:

```java
// Event Replay Service
@Service
public class EventReplayService {
    @Autowired
    private EventStoreService eventStoreService;
    @Autowired
    private EventHandlerRegistry eventHandlerRegistry;
    
    public void replayEvents(String aggregateId) {
        List<DomainEvent> events = eventStoreService.getEvents(aggregateId);
        
        for (DomainEvent event : events) {
            replayEvent(event);
        }
    }
    
    public void replayEventsFromVersion(String aggregateId, int fromVersion) {
        List<DomainEvent> events = eventStoreService.getEventsFromVersion(aggregateId, fromVersion);
        
        for (DomainEvent event : events) {
            replayEvent(event);
        }
    }
    
    public void replayAllEvents() {
        List<StoredEvent> allEvents = eventStoreService.getAllEvents();
        
        for (StoredEvent storedEvent : allEvents) {
            DomainEvent event = eventStoreService.deserializeEvent(storedEvent);
            replayEvent(event);
        }
    }
    
    private void replayEvent(DomainEvent event) {
        List<EventHandler> handlers = eventHandlerRegistry.getHandlers(event.getClass());
        
        for (EventHandler handler : handlers) {
            try {
                handler.handle(event);
            } catch (Exception e) {
                log.error("Failed to replay event: {}", event.getEventId(), e);
            }
        }
    }
}

// Event Handler Registry
@Component
public class EventHandlerRegistry {
    private final Map<Class<?>, List<EventHandler>> handlers = new HashMap<>();
    
    public void registerHandler(Class<?> eventType, EventHandler handler) {
        handlers.computeIfAbsent(eventType, k -> new ArrayList<>()).add(handler);
    }
    
    public List<EventHandler> getHandlers(Class<?> eventType) {
        return handlers.getOrDefault(eventType, Collections.emptyList());
    }
}
```

### Snapshot Service:

```java
// Snapshot Service
@Service
public class SnapshotService {
    @Autowired
    private SnapshotRepository snapshotRepository;
    @Autowired
    private EventStoreService eventStoreService;
    
    public void createSnapshot(String aggregateId) {
        List<DomainEvent> events = eventStoreService.getEvents(aggregateId);
        Object aggregate = reconstructAggregate(events);
        
        Snapshot snapshot = Snapshot.builder()
            .aggregateId(aggregateId)
            .version(events.size())
            .data(serializeAggregate(aggregate))
            .timestamp(Instant.now())
            .build();
        
        snapshotRepository.save(snapshot);
    }
    
    public Object getSnapshot(String aggregateId) {
        Snapshot snapshot = snapshotRepository.findByAggregateId(aggregateId);
        if (snapshot != null) {
            return deserializeAggregate(snapshot.getData());
        }
        return null;
    }
    
    public Object getAggregateWithSnapshot(String aggregateId) {
        Snapshot snapshot = snapshotRepository.findByAggregateId(aggregateId);
        
        if (snapshot != null) {
            // Start from snapshot
            Object aggregate = deserializeAggregate(snapshot.getData());
            List<DomainEvent> events = eventStoreService.getEventsFromVersion(aggregateId, snapshot.getVersion());
            
            // Apply events since snapshot
            for (DomainEvent event : events) {
                applyEventToAggregate(aggregate, event);
            }
            
            return aggregate;
        } else {
            // No snapshot, replay all events
            List<DomainEvent> events = eventStoreService.getEvents(aggregateId);
            return reconstructAggregate(events);
        }
    }
}
```

This comprehensive guide covers all aspects of event-driven architecture in microservices, providing both theoretical understanding and practical implementation examples. Each concept is explained with real-world scenarios and Java code examples to make the concepts clear and actionable.