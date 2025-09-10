# Section 16 - Event-Driven Patterns

## 16.1 Event Sourcing Pattern

The Event Sourcing pattern stores changes as a sequence of events rather than storing the current state, providing a complete audit trail and enabling event replay.

### When to Use:
- When you need a complete audit trail
- When you want to replay events to reconstruct state
- When you need to support temporal queries
- When you want to enable event-driven architecture

### Real-World Analogy:
Think of a bank account statement that shows every transaction (deposit, withdrawal, transfer) rather than just the current balance. You can see the complete history and reconstruct the balance at any point in time.

### Basic Implementation:
```java
// Event interface
public interface DomainEvent {
    String getEventId();
    LocalDateTime getTimestamp();
    String getEventType();
    String getAggregateId();
}

// User events
public class UserCreatedEvent implements DomainEvent {
    private String eventId;
    private LocalDateTime timestamp;
    private String aggregateId;
    private String name;
    private String email;
    
    public UserCreatedEvent(String aggregateId, String name, String email) {
        this.eventId = UUID.randomUUID().toString();
        this.timestamp = LocalDateTime.now();
        this.aggregateId = aggregateId;
        this.name = name;
        this.email = email;
    }
    
    // Getters
    public String getEventId() { return eventId; }
    public LocalDateTime getTimestamp() { return timestamp; }
    public String getEventType() { return "UserCreated"; }
    public String getAggregateId() { return aggregateId; }
    public String getName() { return name; }
    public String getEmail() { return email; }
}

public class UserUpdatedEvent implements DomainEvent {
    private String eventId;
    private LocalDateTime timestamp;
    private String aggregateId;
    private String name;
    private String email;
    
    public UserUpdatedEvent(String aggregateId, String name, String email) {
        this.eventId = UUID.randomUUID().toString();
        this.timestamp = LocalDateTime.now();
        this.aggregateId = aggregateId;
        this.name = name;
        this.email = email;
    }
    
    // Getters
    public String getEventId() { return eventId; }
    public LocalDateTime getTimestamp() { return timestamp; }
    public String getEventType() { return "UserUpdated"; }
    public String getAggregateId() { return aggregateId; }
    public String getName() { return name; }
    public String getEmail() { return email; }
}

// Event store
public class EventStore {
    private List<DomainEvent> events = new ArrayList<>();
    
    public void saveEvent(DomainEvent event) {
        events.add(event);
    }
    
    public List<DomainEvent> getEvents(String aggregateId) {
        return events.stream()
            .filter(event -> event.getAggregateId().equals(aggregateId))
            .sorted(Comparator.comparing(DomainEvent::getTimestamp))
            .collect(Collectors.toList());
    }
    
    public List<DomainEvent> getAllEvents() {
        return new ArrayList<>(events);
    }
}

// Aggregate root
public class User {
    private String id;
    private String name;
    private String email;
    private List<DomainEvent> uncommittedEvents = new ArrayList<>();
    
    public User(String id, String name, String email) {
        this.id = id;
        this.name = name;
        this.email = email;
        this.uncommittedEvents.add(new UserCreatedEvent(id, name, email));
    }
    
    public void updateName(String newName) {
        this.name = newName;
        this.uncommittedEvents.add(new UserUpdatedEvent(id, newName, email));
    }
    
    public void updateEmail(String newEmail) {
        this.email = newEmail;
        this.uncommittedEvents.add(new UserUpdatedEvent(id, name, newEmail));
    }
    
    public List<DomainEvent> getUncommittedEvents() {
        return new ArrayList<>(uncommittedEvents);
    }
    
    public void markEventsAsCommitted() {
        uncommittedEvents.clear();
    }
    
    // Reconstruct from events
    public static User fromEvents(List<DomainEvent> events) {
        User user = null;
        for (DomainEvent event : events) {
            if (event instanceof UserCreatedEvent) {
                UserCreatedEvent createdEvent = (UserCreatedEvent) event;
                user = new User(createdEvent.getAggregateId(), 
                              createdEvent.getName(), 
                              createdEvent.getEmail());
            } else if (event instanceof UserUpdatedEvent) {
                UserUpdatedEvent updatedEvent = (UserUpdatedEvent) event;
                if (user != null) {
                    user.name = updatedEvent.getName();
                    user.email = updatedEvent.getEmail();
                }
            }
        }
        return user;
    }
}
```

## 16.2 CQRS Pattern

The CQRS (Command Query Responsibility Segregation) pattern separates read and write operations, allowing different models for commands and queries.

### When to Use:
- When you have different read and write requirements
- When you want to optimize for different use cases
- When you need to scale reads and writes independently

### Real-World Analogy:
Think of a library system where the process of checking out books (commands) is completely separate from searching for books (queries). The checkout system needs to be fast and reliable, while the search system needs to be flexible and comprehensive.

### Basic Implementation:
```java
// Command interface
public interface Command {
    String getCommandId();
    LocalDateTime getTimestamp();
}

// Query interface
public interface Query<T> {
    T execute();
}

// User commands
public class CreateUserCommand implements Command {
    private String commandId;
    private LocalDateTime timestamp;
    private String name;
    private String email;
    
    public CreateUserCommand(String name, String email) {
        this.commandId = UUID.randomUUID().toString();
        this.timestamp = LocalDateTime.now();
        this.name = name;
        this.email = email;
    }
    
    // Getters
    public String getCommandId() { return commandId; }
    public LocalDateTime getTimestamp() { return timestamp; }
    public String getName() { return name; }
    public String getEmail() { return email; }
}

public class UpdateUserCommand implements Command {
    private String commandId;
    private LocalDateTime timestamp;
    private String userId;
    private String name;
    private String email;
    
    public UpdateUserCommand(String userId, String name, String email) {
        this.commandId = UUID.randomUUID().toString();
        this.timestamp = LocalDateTime.now();
        this.userId = userId;
        this.name = name;
        this.email = email;
    }
    
    // Getters
    public String getCommandId() { return commandId; }
    public LocalDateTime getTimestamp() { return timestamp; }
    public String getUserId() { return userId; }
    public String getName() { return name; }
    public String getEmail() { return email; }
}

// Command handler
public class UserCommandHandler {
    private EventStore eventStore;
    
    public UserCommandHandler(EventStore eventStore) {
        this.eventStore = eventStore;
    }
    
    public void handle(CreateUserCommand command) {
        User user = new User(UUID.randomUUID().toString(), command.getName(), command.getEmail());
        List<DomainEvent> events = user.getUncommittedEvents();
        for (DomainEvent event : events) {
            eventStore.saveEvent(event);
        }
        user.markEventsAsCommitted();
    }
    
    public void handle(UpdateUserCommand command) {
        List<DomainEvent> events = eventStore.getEvents(command.getUserId());
        User user = User.fromEvents(events);
        
        if (user != null) {
            user.updateName(command.getName());
            user.updateEmail(command.getEmail());
            
            List<DomainEvent> newEvents = user.getUncommittedEvents();
            for (DomainEvent event : newEvents) {
                eventStore.saveEvent(event);
            }
            user.markEventsAsCommitted();
        }
    }
}

// Query models
public class UserReadModel {
    private String id;
    private String name;
    private String email;
    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;
    
    public UserReadModel(String id, String name, String email, LocalDateTime createdAt, LocalDateTime updatedAt) {
        this.id = id;
        this.name = name;
        this.email = email;
        this.createdAt = createdAt;
        this.updatedAt = updatedAt;
    }
    
    // Getters
    public String getId() { return id; }
    public String getName() { return name; }
    public String getEmail() { return email; }
    public LocalDateTime getCreatedAt() { return createdAt; }
    public LocalDateTime getUpdatedAt() { return updatedAt; }
}

// Query handlers
public class UserQueryHandler {
    private Map<String, UserReadModel> readModels = new HashMap<>();
    
    public UserReadModel handle(GetUserByIdQuery query) {
        return readModels.get(query.getUserId());
    }
    
    public List<UserReadModel> handle(GetAllUsersQuery query) {
        return new ArrayList<>(readModels.values());
    }
    
    public void updateReadModel(DomainEvent event) {
        if (event instanceof UserCreatedEvent) {
            UserCreatedEvent createdEvent = (UserCreatedEvent) event;
            UserReadModel readModel = new UserReadModel(
                createdEvent.getAggregateId(),
                createdEvent.getName(),
                createdEvent.getEmail(),
                createdEvent.getTimestamp(),
                createdEvent.getTimestamp()
            );
            readModels.put(createdEvent.getAggregateId(), readModel);
        } else if (event instanceof UserUpdatedEvent) {
            UserUpdatedEvent updatedEvent = (UserUpdatedEvent) event;
            UserReadModel readModel = readModels.get(updatedEvent.getAggregateId());
            if (readModel != null) {
                readModel = new UserReadModel(
                    readModel.getId(),
                    updatedEvent.getName(),
                    updatedEvent.getEmail(),
                    readModel.getCreatedAt(),
                    updatedEvent.getTimestamp()
                );
                readModels.put(updatedEvent.getAggregateId(), readModel);
            }
        }
    }
}

// Queries
public class GetUserByIdQuery implements Query<UserReadModel> {
    private String userId;
    
    public GetUserByIdQuery(String userId) {
        this.userId = userId;
    }
    
    public String getUserId() { return userId; }
    
    public UserReadModel execute() {
        // Implementation would use query handler
        return null;
    }
}

public class GetAllUsersQuery implements Query<List<UserReadModel>> {
    public List<UserReadModel> execute() {
        // Implementation would use query handler
        return null;
    }
}
```

## 16.3 Event Store Pattern

The Event Store pattern provides a dedicated storage system for events, enabling event sourcing and event replay.

### When to Use:
- When you need to store events persistently
- When you want to enable event replay
- When you need to support event sourcing

### Real-World Analogy:
Think of a video recording system that stores every frame of a movie. You can play back the movie from any point, fast forward, rewind, or even edit specific scenes.

### Basic Implementation:
```java
// Event store interface
public interface EventStore {
    void saveEvent(DomainEvent event);
    List<DomainEvent> getEvents(String aggregateId);
    List<DomainEvent> getEvents(String aggregateId, long fromVersion);
    List<DomainEvent> getAllEvents();
    List<DomainEvent> getEventsByType(String eventType);
}

// In-memory event store
public class InMemoryEventStore implements EventStore {
    private List<DomainEvent> events = new ArrayList<>();
    private Map<String, Long> aggregateVersions = new HashMap<>();
    
    public void saveEvent(DomainEvent event) {
        events.add(event);
        String aggregateId = event.getAggregateId();
        aggregateVersions.put(aggregateId, aggregateVersions.getOrDefault(aggregateId, 0L) + 1);
    }
    
    public List<DomainEvent> getEvents(String aggregateId) {
        return events.stream()
            .filter(event -> event.getAggregateId().equals(aggregateId))
            .sorted(Comparator.comparing(DomainEvent::getTimestamp))
            .collect(Collectors.toList());
    }
    
    public List<DomainEvent> getEvents(String aggregateId, long fromVersion) {
        return events.stream()
            .filter(event -> event.getAggregateId().equals(aggregateId))
            .filter(event -> getEventVersion(event) >= fromVersion)
            .sorted(Comparator.comparing(DomainEvent::getTimestamp))
            .collect(Collectors.toList());
    }
    
    public List<DomainEvent> getAllEvents() {
        return new ArrayList<>(events);
    }
    
    public List<DomainEvent> getEventsByType(String eventType) {
        return events.stream()
            .filter(event -> event.getEventType().equals(eventType))
            .sorted(Comparator.comparing(DomainEvent::getTimestamp))
            .collect(Collectors.toList());
    }
    
    private long getEventVersion(DomainEvent event) {
        return aggregateVersions.getOrDefault(event.getAggregateId(), 0L);
    }
}

// Persistent event store
public class PersistentEventStore implements EventStore {
    private EventRepository eventRepository;
    
    public PersistentEventStore(EventRepository eventRepository) {
        this.eventRepository = eventRepository;
    }
    
    public void saveEvent(DomainEvent event) {
        EventEntity entity = new EventEntity(
            event.getEventId(),
            event.getAggregateId(),
            event.getEventType(),
            event.getTimestamp(),
            serializeEvent(event)
        );
        eventRepository.save(entity);
    }
    
    public List<DomainEvent> getEvents(String aggregateId) {
        List<EventEntity> entities = eventRepository.findByAggregateId(aggregateId);
        return entities.stream()
            .map(this::deserializeEvent)
            .collect(Collectors.toList());
    }
    
    public List<DomainEvent> getEvents(String aggregateId, long fromVersion) {
        List<EventEntity> entities = eventRepository.findByAggregateIdAndVersionGreaterThanEqual(aggregateId, fromVersion);
        return entities.stream()
            .map(this::deserializeEvent)
            .collect(Collectors.toList());
    }
    
    public List<DomainEvent> getAllEvents() {
        List<EventEntity> entities = eventRepository.findAll();
        return entities.stream()
            .map(this::deserializeEvent)
            .collect(Collectors.toList());
    }
    
    public List<DomainEvent> getEventsByType(String eventType) {
        List<EventEntity> entities = eventRepository.findByEventType(eventType);
        return entities.stream()
            .map(this::deserializeEvent)
            .collect(Collectors.toList());
    }
    
    private String serializeEvent(DomainEvent event) {
        // Implementation to serialize event to JSON
        return "{}";
    }
    
    private DomainEvent deserializeEvent(EventEntity entity) {
        // Implementation to deserialize event from JSON
        return null;
    }
}

// Event entity for persistence
public class EventEntity {
    private String eventId;
    private String aggregateId;
    private String eventType;
    private LocalDateTime timestamp;
    private String eventData;
    
    public EventEntity(String eventId, String aggregateId, String eventType, LocalDateTime timestamp, String eventData) {
        this.eventId = eventId;
        this.aggregateId = aggregateId;
        this.eventType = eventType;
        this.timestamp = timestamp;
        this.eventData = eventData;
    }
    
    // Getters and setters
    public String getEventId() { return eventId; }
    public String getAggregateId() { return aggregateId; }
    public String getEventType() { return eventType; }
    public LocalDateTime getTimestamp() { return timestamp; }
    public String getEventData() { return eventData; }
}
```

## 16.4 Event Bus Pattern

The Event Bus pattern provides a centralized communication mechanism for events, enabling loose coupling between components.

### When to Use:
- When you need to decouple event publishers and subscribers
- When you want to enable dynamic event routing
- When you need to support multiple event types

### Real-World Analogy:
Think of a radio station that broadcasts news to multiple listeners. The station doesn't need to know who's listening, and listeners can tune in or out as they please.

### Basic Implementation:
```java
// Event bus interface
public interface EventBus {
    void publish(DomainEvent event);
    void subscribe(String eventType, EventHandler handler);
    void unsubscribe(String eventType, EventHandler handler);
}

// Event handler interface
public interface EventHandler {
    void handle(DomainEvent event);
    String getEventType();
}

// Simple event bus
public class SimpleEventBus implements EventBus {
    private Map<String, List<EventHandler>> handlers = new HashMap<>();
    
    public void publish(DomainEvent event) {
        String eventType = event.getEventType();
        List<EventHandler> eventHandlers = handlers.get(eventType);
        
        if (eventHandlers != null) {
            for (EventHandler handler : eventHandlers) {
                try {
                    handler.handle(event);
                } catch (Exception e) {
                    // Log error but continue processing other handlers
                    System.err.println("Error handling event: " + e.getMessage());
                }
            }
        }
    }
    
    public void subscribe(String eventType, EventHandler handler) {
        handlers.computeIfAbsent(eventType, k -> new ArrayList<>()).add(handler);
    }
    
    public void unsubscribe(String eventType, EventHandler handler) {
        List<EventHandler> eventHandlers = handlers.get(eventType);
        if (eventHandlers != null) {
            eventHandlers.remove(handler);
        }
    }
}

// Asynchronous event bus
public class AsyncEventBus implements EventBus {
    private Map<String, List<EventHandler>> handlers = new HashMap<>();
    private ExecutorService executor;
    
    public AsyncEventBus() {
        this.executor = Executors.newCachedThreadPool();
    }
    
    public void publish(DomainEvent event) {
        String eventType = event.getEventType();
        List<EventHandler> eventHandlers = handlers.get(eventType);
        
        if (eventHandlers != null) {
            for (EventHandler handler : eventHandlers) {
                executor.submit(() -> {
                    try {
                        handler.handle(event);
                    } catch (Exception e) {
                        System.err.println("Error handling event: " + e.getMessage());
                    }
                });
            }
        }
    }
    
    public void subscribe(String eventType, EventHandler handler) {
        handlers.computeIfAbsent(eventType, k -> new ArrayList<>()).add(handler);
    }
    
    public void unsubscribe(String eventType, EventHandler handler) {
        List<EventHandler> eventHandlers = handlers.get(eventType);
        if (eventHandlers != null) {
            eventHandlers.remove(handler);
        }
    }
    
    public void shutdown() {
        executor.shutdown();
    }
}

// Event handlers
public class UserCreatedEventHandler implements EventHandler {
    private UserQueryHandler queryHandler;
    
    public UserCreatedEventHandler(UserQueryHandler queryHandler) {
        this.queryHandler = queryHandler;
    }
    
    public void handle(DomainEvent event) {
        if (event instanceof UserCreatedEvent) {
            UserCreatedEvent userCreatedEvent = (UserCreatedEvent) event;
            queryHandler.updateReadModel(userCreatedEvent);
        }
    }
    
    public String getEventType() {
        return "UserCreated";
    }
}

public class UserUpdatedEventHandler implements EventHandler {
    private UserQueryHandler queryHandler;
    
    public UserUpdatedEventHandler(UserQueryHandler queryHandler) {
        this.queryHandler = queryHandler;
    }
    
    public void handle(DomainEvent event) {
        if (event instanceof UserUpdatedEvent) {
            UserUpdatedEvent userUpdatedEvent = (UserUpdatedEvent) event;
            queryHandler.updateReadModel(userUpdatedEvent);
        }
    }
    
    public String getEventType() {
        return "UserUpdated";
    }
}
```

## 16.5 Publish-Subscribe Pattern

The Publish-Subscribe pattern enables one-to-many communication where publishers send messages to topics, and subscribers receive messages from topics they're interested in.

### When to Use:
- When you need to broadcast information to multiple consumers
- When consumers have different interests
- When you want to decouple publishers from subscribers

### Real-World Analogy:
Think of a newspaper subscription system. The newspaper (publisher) publishes articles (messages) to different sections (topics). Subscribers (consumers) can subscribe to specific sections they're interested in, and they'll receive all articles published to those sections.

### Basic Implementation:
```java
// Publisher interface
public interface Publisher {
    void publish(String topic, Object message);
}

// Subscriber interface
public interface Subscriber {
    void onMessage(String topic, Object message);
}

// Topic-based publish-subscribe system
public class TopicBasedPubSub implements Publisher {
    private Map<String, List<Subscriber>> topicSubscribers = new HashMap<>();
    
    public void subscribe(String topic, Subscriber subscriber) {
        topicSubscribers.computeIfAbsent(topic, k -> new ArrayList<>()).add(subscriber);
    }
    
    public void unsubscribe(String topic, Subscriber subscriber) {
        List<Subscriber> subscribers = topicSubscribers.get(topic);
        if (subscribers != null) {
            subscribers.remove(subscriber);
        }
    }
    
    public void publish(String topic, Object message) {
        List<Subscriber> subscribers = topicSubscribers.get(topic);
        if (subscribers != null) {
            for (Subscriber subscriber : subscribers) {
                try {
                    subscriber.onMessage(topic, message);
                } catch (Exception e) {
                    System.err.println("Error notifying subscriber: " + e.getMessage());
                }
            }
        }
    }
}

// Example usage
public class NewsPublisher implements Publisher {
    private TopicBasedPubSub pubSub;
    
    public NewsPublisher(TopicBasedPubSub pubSub) {
        this.pubSub = pubSub;
    }
    
    public void publishNews(String category, String headline, String content) {
        NewsMessage message = new NewsMessage(headline, content);
        pubSub.publish(category, message);
    }
}

public class NewsSubscriber implements Subscriber {
    private String name;
    private Set<String> subscribedTopics;
    
    public NewsSubscriber(String name) {
        this.name = name;
        this.subscribedTopics = new HashSet<>();
    }
    
    public void subscribeTo(String topic) {
        subscribedTopics.add(topic);
    }
    
    public void onMessage(String topic, Object message) {
        if (subscribedTopics.contains(topic)) {
            System.out.println(name + " received " + topic + " news: " + message);
        }
    }
}
```

## 16.6 Event Streaming Pattern

The Event Streaming pattern processes continuous streams of events in real-time, enabling real-time analytics and processing.

### When to Use:
- When you need to process events in real-time
- When you want to enable real-time analytics
- When you need to handle high-volume event streams

### Real-World Analogy:
Think of a live sports broadcast where events (goals, fouls, substitutions) are streamed in real-time to viewers, who can see the action as it happens.

### Basic Implementation:
```java
// Event stream interface
public interface EventStream<T> {
    void subscribe(StreamSubscriber<T> subscriber);
    void unsubscribe(StreamSubscriber<T> subscriber);
    void publish(T event);
}

// Stream subscriber interface
public interface StreamSubscriber<T> {
    void onEvent(T event);
    void onError(Throwable error);
    void onComplete();
}

// Simple event stream
public class SimpleEventStream<T> implements EventStream<T> {
    private List<StreamSubscriber<T>> subscribers = new ArrayList<>();
    
    public void subscribe(StreamSubscriber<T> subscriber) {
        subscribers.add(subscriber);
    }
    
    public void unsubscribe(StreamSubscriber<T> subscriber) {
        subscribers.remove(subscriber);
    }
    
    public void publish(T event) {
        for (StreamSubscriber<T> subscriber : subscribers) {
            try {
                subscriber.onEvent(event);
            } catch (Exception e) {
                subscriber.onError(e);
            }
        }
    }
}

// Event processor
public class EventProcessor<T> {
    private EventStream<T> inputStream;
    private EventStream<T> outputStream;
    private Function<T, T> processor;
    
    public EventProcessor(EventStream<T> inputStream, EventStream<T> outputStream, Function<T, T> processor) {
        this.inputStream = inputStream;
        this.outputStream = outputStream;
        this.processor = processor;
        
        inputStream.subscribe(new StreamSubscriber<T>() {
            public void onEvent(T event) {
                try {
                    T processedEvent = processor.apply(event);
                    outputStream.publish(processedEvent);
                } catch (Exception e) {
                    onError(e);
                }
            }
            
            public void onError(Throwable error) {
                System.err.println("Error processing event: " + error.getMessage());
            }
            
            public void onComplete() {
                // Handle completion
            }
        });
    }
}

// Usage example
public class UserEventProcessor {
    public static void main(String[] args) {
        SimpleEventStream<UserEvent> inputStream = new SimpleEventStream<>();
        SimpleEventStream<UserEvent> outputStream = new SimpleEventStream<>();
        
        // Process user events
        EventProcessor<UserEvent> processor = new EventProcessor<>(
            inputStream,
            outputStream,
            event -> {
                // Add processing timestamp
                event.setProcessedAt(LocalDateTime.now());
                return event;
            }
        );
        
        // Subscribe to processed events
        outputStream.subscribe(new StreamSubscriber<UserEvent>() {
            public void onEvent(UserEvent event) {
                System.out.println("Processed event: " + event);
            }
            
            public void onError(Throwable error) {
                System.err.println("Error: " + error.getMessage());
            }
            
            public void onComplete() {
                System.out.println("Stream completed");
            }
        });
        
        // Publish events
        inputStream.publish(new UserEvent("user1", "created"));
        inputStream.publish(new UserEvent("user2", "updated"));
    }
}
```

## 16.7 Event Choreography Pattern

The Event Choreography pattern uses events to coordinate between services without a central orchestrator.

### When to Use:
- When you want to avoid central orchestration
- When you need to enable service autonomy
- When you want to reduce coupling between services

### Real-World Analogy:
Think of a dance where each dancer knows their part and responds to the music (events) without a choreographer telling them what to do. The dancers coordinate through the rhythm and flow of the music.

### Basic Implementation:
```java
// Order events
public class OrderCreatedEvent implements DomainEvent {
    private String eventId;
    private LocalDateTime timestamp;
    private String orderId;
    private String customerId;
    private List<OrderItem> items;
    
    public OrderCreatedEvent(String orderId, String customerId, List<OrderItem> items) {
        this.eventId = UUID.randomUUID().toString();
        this.timestamp = LocalDateTime.now();
        this.orderId = orderId;
        this.customerId = customerId;
        this.items = items;
    }
    
    // Getters
    public String getEventId() { return eventId; }
    public LocalDateTime getTimestamp() { return timestamp; }
    public String getEventType() { return "OrderCreated"; }
    public String getAggregateId() { return orderId; }
    public String getOrderId() { return orderId; }
    public String getCustomerId() { return customerId; }
    public List<OrderItem> getItems() { return items; }
}

public class InventoryReservedEvent implements DomainEvent {
    private String eventId;
    private LocalDateTime timestamp;
    private String orderId;
    private boolean success;
    
    public InventoryReservedEvent(String orderId, boolean success) {
        this.eventId = UUID.randomUUID().toString();
        this.timestamp = LocalDateTime.now();
        this.orderId = orderId;
        this.success = success;
    }
    
    // Getters
    public String getEventId() { return eventId; }
    public LocalDateTime getTimestamp() { return timestamp; }
    public String getEventType() { return "InventoryReserved"; }
    public String getAggregateId() { return orderId; }
    public String getOrderId() { return orderId; }
    public boolean isSuccess() { return success; }
}

// Service that handles order creation
public class OrderService {
    private EventBus eventBus;
    
    public OrderService(EventBus eventBus) {
        this.eventBus = eventBus;
    }
    
    public void createOrder(String customerId, List<OrderItem> items) {
        String orderId = UUID.randomUUID().toString();
        OrderCreatedEvent event = new OrderCreatedEvent(orderId, customerId, items);
        eventBus.publish(event);
    }
}

// Service that handles inventory
public class InventoryService {
    private EventBus eventBus;
    
    public InventoryService(EventBus eventBus) {
        this.eventBus = eventBus;
    }
    
    public void handleOrderCreated(OrderCreatedEvent event) {
        // Reserve inventory
        boolean success = reserveInventory(event.getItems());
        InventoryReservedEvent reservedEvent = new InventoryReservedEvent(event.getOrderId(), success);
        eventBus.publish(reservedEvent);
    }
    
    private boolean reserveInventory(List<OrderItem> items) {
        // Implementation to reserve inventory
        return true;
    }
}

// Service that handles payment
public class PaymentService {
    private EventBus eventBus;
    
    public PaymentService(EventBus eventBus) {
        this.eventBus = eventBus;
    }
    
    public void handleInventoryReserved(InventoryReservedEvent event) {
        if (event.isSuccess()) {
            // Process payment
            processPayment(event.getOrderId());
        } else {
            // Cancel order
            cancelOrder(event.getOrderId());
        }
    }
    
    private void processPayment(String orderId) {
        // Implementation to process payment
    }
    
    private void cancelOrder(String orderId) {
        // Implementation to cancel order
    }
}
```

## 16.8 Event Orchestration Pattern

The Event Orchestration pattern uses a central orchestrator to coordinate events between services.

### When to Use:
- When you need central control over the process
- When you want to implement complex business logic
- When you need to handle error scenarios centrally

### Real-World Analogy:
Think of a conductor leading an orchestra. The conductor (orchestrator) coordinates all the musicians (services) to play in harmony, ensuring the right timing and sequence.

### Basic Implementation:
```java
// Event orchestrator
public class EventOrchestrator {
    private EventBus eventBus;
    private Map<String, OrchestrationContext> contexts = new HashMap<>();
    
    public EventOrchestrator(EventBus eventBus) {
        this.eventBus = eventBus;
        setupEventHandlers();
    }
    
    private void setupEventHandlers() {
        eventBus.subscribe("OrderCreated", this::handleOrderCreated);
        eventBus.subscribe("InventoryReserved", this::handleInventoryReserved);
        eventBus.subscribe("PaymentProcessed", this::handlePaymentProcessed);
    }
    
    private void handleOrderCreated(DomainEvent event) {
        if (event instanceof OrderCreatedEvent) {
            OrderCreatedEvent orderEvent = (OrderCreatedEvent) event;
            OrchestrationContext context = new OrchestrationContext(orderEvent.getOrderId());
            contexts.put(orderEvent.getOrderId(), context);
            
            // Start orchestration
            context.addStep("inventory", "reserve");
            eventBus.publish(new ReserveInventoryCommand(orderEvent.getOrderId(), orderEvent.getItems()));
        }
    }
    
    private void handleInventoryReserved(DomainEvent event) {
        if (event instanceof InventoryReservedEvent) {
            InventoryReservedEvent reservedEvent = (InventoryReservedEvent) event;
            OrchestrationContext context = contexts.get(reservedEvent.getOrderId());
            
            if (context != null) {
                context.completeStep("inventory");
                
                if (reservedEvent.isSuccess()) {
                    context.addStep("payment", "process");
                    eventBus.publish(new ProcessPaymentCommand(reservedEvent.getOrderId()));
                } else {
                    context.addStep("order", "cancel");
                    eventBus.publish(new CancelOrderCommand(reservedEvent.getOrderId()));
                }
            }
        }
    }
    
    private void handlePaymentProcessed(DomainEvent event) {
        if (event instanceof PaymentProcessedEvent) {
            PaymentProcessedEvent paymentEvent = (PaymentProcessedEvent) event;
            OrchestrationContext context = contexts.get(paymentEvent.getOrderId());
            
            if (context != null) {
                context.completeStep("payment");
                
                if (paymentEvent.isSuccess()) {
                    context.addStep("order", "confirm");
                    eventBus.publish(new ConfirmOrderCommand(paymentEvent.getOrderId()));
                } else {
                    context.addStep("order", "cancel");
                    eventBus.publish(new CancelOrderCommand(paymentEvent.getOrderId()));
                }
            }
        }
    }
}

// Orchestration context
public class OrchestrationContext {
    private String orderId;
    private Map<String, String> steps = new HashMap<>();
    private Set<String> completedSteps = new HashSet<>();
    
    public OrchestrationContext(String orderId) {
        this.orderId = orderId;
    }
    
    public void addStep(String service, String action) {
        steps.put(service, action);
    }
    
    public void completeStep(String service) {
        completedSteps.add(service);
    }
    
    public boolean isStepCompleted(String service) {
        return completedSteps.contains(service);
    }
    
    public boolean areAllStepsCompleted() {
        return completedSteps.size() == steps.size();
    }
    
    // Getters
    public String getOrderId() { return orderId; }
    public Map<String, String> getSteps() { return steps; }
    public Set<String> getCompletedSteps() { return completedSteps; }
}
```

## 16.9 Event Collaboration Pattern

The Event Collaboration pattern enables services to collaborate through events while maintaining their autonomy.

### When to Use:
- When you need service autonomy
- When you want to enable loose coupling
- When you need to support dynamic collaboration

### Real-World Analogy:
Think of a team of experts working on a project. Each expert (service) knows their specialty and can contribute to the project by sharing their expertise (events) with others, without needing to know all the details of what others are doing.

### Basic Implementation:
```java
// Collaboration event
public class CollaborationEvent implements DomainEvent {
    private String eventId;
    private LocalDateTime timestamp;
    private String sourceService;
    private String targetService;
    private String eventType;
    private Map<String, Object> data;
    
    public CollaborationEvent(String sourceService, String targetService, String eventType, Map<String, Object> data) {
        this.eventId = UUID.randomUUID().toString();
        this.timestamp = LocalDateTime.now();
        this.sourceService = sourceService;
        this.targetService = targetService;
        this.eventType = eventType;
        this.data = data;
    }
    
    // Getters
    public String getEventId() { return eventId; }
    public LocalDateTime getTimestamp() { return timestamp; }
    public String getEventType() { return eventType; }
    public String getAggregateId() { return sourceService + ":" + targetService; }
    public String getSourceService() { return sourceService; }
    public String getTargetService() { return targetService; }
    public Map<String, Object> getData() { return data; }
}

// Service collaborator
public class ServiceCollaborator {
    private String serviceName;
    private EventBus eventBus;
    private Map<String, List<CollaborationHandler>> handlers = new HashMap<>();
    
    public ServiceCollaborator(String serviceName, EventBus eventBus) {
        this.serviceName = serviceName;
        this.eventBus = eventBus;
    }
    
    public void sendEvent(String targetService, String eventType, Map<String, Object> data) {
        CollaborationEvent event = new CollaborationEvent(serviceName, targetService, eventType, data);
        eventBus.publish(event);
    }
    
    public void onEvent(String eventType, CollaborationHandler handler) {
        handlers.computeIfAbsent(eventType, k -> new ArrayList<>()).add(handler);
    }
    
    public void handleCollaborationEvent(CollaborationEvent event) {
        if (event.getTargetService().equals(serviceName)) {
            List<CollaborationHandler> eventHandlers = handlers.get(event.getEventType());
            if (eventHandlers != null) {
                for (CollaborationHandler handler : eventHandlers) {
                    handler.handle(event);
                }
            }
        }
    }
}

// Collaboration handler interface
public interface CollaborationHandler {
    void handle(CollaborationEvent event);
}

// Example service collaboration
public class UserService {
    private ServiceCollaborator collaborator;
    
    public UserService(ServiceCollaborator collaborator) {
        this.collaborator = collaborator;
        setupCollaboration();
    }
    
    private void setupCollaboration() {
        collaborator.onEvent("UserCreated", event -> {
            Map<String, Object> data = event.getData();
            String userId = (String) data.get("userId");
            String email = (String) data.get("email");
            
            // Send welcome email
            Map<String, Object> emailData = new HashMap<>();
            emailData.put("userId", userId);
            emailData.put("email", email);
            emailData.put("template", "welcome");
            
            collaborator.sendEvent("EmailService", "SendWelcomeEmail", emailData);
        });
    }
    
    public void createUser(String name, String email) {
        String userId = UUID.randomUUID().toString();
        
        // Create user
        // ... user creation logic ...
        
        // Notify other services
        Map<String, Object> data = new HashMap<>();
        data.put("userId", userId);
        data.put("name", name);
        data.put("email", email);
        
        collaborator.sendEvent("EmailService", "UserCreated", data);
        collaborator.sendEvent("AnalyticsService", "UserCreated", data);
    }
}
```

## 16.10 Event Notification Pattern

The Event Notification pattern provides a way to notify interested parties about events without them needing to know the details of the event source.

### When to Use:
- When you need to notify multiple parties about events
- When you want to decouple event sources from consumers
- When you need to support different notification channels

### Real-World Analogy:
Think of a school's announcement system. When there's an important announcement, it's broadcast to all classrooms, and each classroom can decide how to respond (ignore, take action, etc.).

### Basic Implementation:
```java
// Event notification interface
public interface EventNotification {
    void notify(String eventType, Object event);
    void subscribe(String eventType, NotificationHandler handler);
    void unsubscribe(String eventType, NotificationHandler handler);
}

// Notification handler interface
public interface NotificationHandler {
    void handle(Object event);
    String getEventType();
}

// Simple event notification
public class SimpleEventNotification implements EventNotification {
    private Map<String, List<NotificationHandler>> handlers = new HashMap<>();
    
    public void notify(String eventType, Object event) {
        List<NotificationHandler> eventHandlers = handlers.get(eventType);
        if (eventHandlers != null) {
            for (NotificationHandler handler : eventHandlers) {
                try {
                    handler.handle(event);
                } catch (Exception e) {
                    System.err.println("Error notifying handler: " + e.getMessage());
                }
            }
        }
    }
    
    public void subscribe(String eventType, NotificationHandler handler) {
        handlers.computeIfAbsent(eventType, k -> new ArrayList<>()).add(handler);
    }
    
    public void unsubscribe(String eventType, NotificationHandler handler) {
        List<NotificationHandler> eventHandlers = handlers.get(eventType);
        if (eventHandlers != null) {
            eventHandlers.remove(handler);
        }
    }
}

// Email notification handler
public class EmailNotificationHandler implements NotificationHandler {
    private EmailService emailService;
    
    public EmailNotificationHandler(EmailService emailService) {
        this.emailService = emailService;
    }
    
    public void handle(Object event) {
        if (event instanceof UserCreatedEvent) {
            UserCreatedEvent userEvent = (UserCreatedEvent) event;
            sendWelcomeEmail(userEvent.getEmail(), userEvent.getName());
        }
    }
    
    public String getEventType() {
        return "UserCreated";
    }
    
    private void sendWelcomeEmail(String email, String name) {
        // Implementation to send welcome email
        System.out.println("Sending welcome email to: " + email);
    }
}

// SMS notification handler
public class SmsNotificationHandler implements NotificationHandler {
    private SmsService smsService;
    
    public SmsNotificationHandler(SmsService smsService) {
        this.smsService = smsService;
    }
    
    public void handle(Object event) {
        if (event instanceof OrderCreatedEvent) {
            OrderCreatedEvent orderEvent = (OrderCreatedEvent) event;
            sendOrderConfirmationSms(orderEvent.getCustomerId());
        }
    }
    
    public String getEventType() {
        return "OrderCreated";
    }
    
    private void sendOrderConfirmationSms(String customerId) {
        // Implementation to send SMS
        System.out.println("Sending order confirmation SMS to customer: " + customerId);
    }
}

// Usage example
public class EventNotificationExample {
    public static void main(String[] args) {
        EventNotification notification = new SimpleEventNotification();
        
        // Set up handlers
        notification.subscribe("UserCreated", new EmailNotificationHandler(new EmailService()));
        notification.subscribe("OrderCreated", new SmsNotificationHandler(new SmsService()));
        
        // Publish events
        notification.notify("UserCreated", new UserCreatedEvent("user1", "John Doe", "john@example.com"));
        notification.notify("OrderCreated", new OrderCreatedEvent("order1", "customer1", new ArrayList<>()));
    }
}
```

This comprehensive coverage of event-driven patterns provides the foundation for building reactive, scalable, and maintainable systems. Each pattern addresses specific event-driven architecture challenges and offers different approaches to handling events and enabling loose coupling between components.