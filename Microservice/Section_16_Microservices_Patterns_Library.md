# Section 16 – Microservices Patterns Library

## 16.1 Aggregator Pattern

The Aggregator pattern collects data from multiple microservices and returns an aggregated response.

### Aggregator Service:

```java
// Aggregator Service
@Service
public class OrderAggregatorService {
    @Autowired
    private UserServiceClient userServiceClient;
    @Autowired
    private ProductServiceClient productServiceClient;
    @Autowired
    private PaymentServiceClient paymentServiceClient;
    
    public OrderDetails getOrderDetails(Long orderId) {
        // Get order information
        Order order = orderService.getOrder(orderId);
        
        // Get user information
        User user = userServiceClient.getUser(order.getUserId());
        
        // Get product information for each order item
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
        
        // Get payment information
        Payment payment = paymentServiceClient.getPayment(order.getPaymentId());
        
        return OrderDetails.builder()
            .order(order)
            .user(user)
            .items(itemDetails)
            .payment(payment)
            .build();
    }
}
```

## 16.2 Proxy Pattern

The Proxy pattern provides a simplified interface to a complex microservices system.

### Proxy Service:

```java
// Proxy Service
@Service
public class MicroservicesProxy {
    @Autowired
    private UserServiceClient userServiceClient;
    @Autowired
    private OrderServiceClient orderServiceClient;
    @Autowired
    private ProductServiceClient productServiceClient;
    
    public UserProfile getUserProfile(Long userId) {
        // Get user information
        User user = userServiceClient.getUser(userId);
        
        // Get user's recent orders
        List<Order> recentOrders = orderServiceClient.getRecentOrders(userId, 5);
        
        // Get user's favorite products
        List<Product> favoriteProducts = productServiceClient.getFavoriteProducts(userId);
        
        return UserProfile.builder()
            .user(user)
            .recentOrders(recentOrders)
            .favoriteProducts(favoriteProducts)
            .build();
    }
    
    public ProductCatalog getProductCatalog(String category) {
        // Get products in category
        List<Product> products = productServiceClient.getProductsByCategory(category);
        
        // Get product availability
        List<ProductAvailability> availability = products.stream()
            .map(product -> {
                boolean available = productServiceClient.isProductAvailable(product.getId());
                return ProductAvailability.builder()
                    .productId(product.getId())
                    .available(available)
                    .build();
            })
            .collect(Collectors.toList());
        
        return ProductCatalog.builder()
            .products(products)
            .availability(availability)
            .build();
    }
}
```

## 16.3 Chained Microservice Pattern

The Chained Microservice pattern processes requests through a chain of microservices.

### Chain Service:

```java
// Chain Service
@Service
public class OrderProcessingChain {
    @Autowired
    private InventoryServiceClient inventoryServiceClient;
    @Autowired
    private PaymentServiceClient paymentServiceClient;
    @Autowired
    private ShippingServiceClient shippingServiceClient;
    @Autowired
    private NotificationServiceClient notificationServiceClient;
    
    public Order processOrder(OrderRequest request) {
        Order order = new Order(request);
        
        // Step 1: Reserve inventory
        InventoryReservation reservation = inventoryServiceClient.reserveInventory(
            request.getProductId(), request.getQuantity());
        order.setInventoryReservationId(reservation.getId());
        
        // Step 2: Process payment
        Payment payment = paymentServiceClient.processPayment(request.getPaymentInfo());
        order.setPaymentId(payment.getId());
        order.setStatus(OrderStatus.PAID);
        
        // Step 3: Create shipping label
        ShippingLabel shippingLabel = shippingServiceClient.createShippingLabel(
            order.getId(), request.getShippingAddress());
        order.setShippingLabelId(shippingLabel.getId());
        order.setStatus(OrderStatus.SHIPPED);
        
        // Step 4: Send notification
        notificationServiceClient.sendOrderConfirmation(order.getId(), request.getUserId());
        
        return order;
    }
}
```

## 16.4 Branch Microservice Pattern

The Branch Microservice pattern processes requests through different branches based on conditions.

### Branch Service:

```java
// Branch Service
@Service
public class OrderProcessingBranch {
    @Autowired
    private StandardOrderService standardOrderService;
    @Autowired
    private PremiumOrderService premiumOrderService;
    @Autowired
    private ExpressOrderService expressOrderService;
    
    public Order processOrder(OrderRequest request) {
        OrderType orderType = determineOrderType(request);
        
        switch (orderType) {
            case STANDARD:
                return standardOrderService.processOrder(request);
            case PREMIUM:
                return premiumOrderService.processOrder(request);
            case EXPRESS:
                return expressOrderService.processOrder(request);
            default:
                throw new UnsupportedOrderTypeException("Unsupported order type: " + orderType);
        }
    }
    
    private OrderType determineOrderType(OrderRequest request) {
        if (request.isExpress()) {
            return OrderType.EXPRESS;
        } else if (request.isPremium()) {
            return OrderType.PREMIUM;
        } else {
            return OrderType.STANDARD;
        }
    }
}
```

## 16.5 Shared Data Pattern

The Shared Data pattern shares data between microservices through a shared database.

### Shared Data Service:

```java
// Shared Data Service
@Service
public class SharedDataService {
    @Autowired
    private SharedDataRepository sharedDataRepository;
    
    public void shareUserData(User user) {
        SharedUserData sharedData = SharedUserData.builder()
            .userId(user.getId())
            .email(user.getEmail())
            .name(user.getName())
            .status(user.getStatus())
            .lastUpdated(Instant.now())
            .build();
        
        sharedDataRepository.save(sharedData);
    }
    
    public SharedUserData getUserData(Long userId) {
        return sharedDataRepository.findByUserId(userId)
            .orElseThrow(() -> new UserDataNotFoundException("User data not found: " + userId));
    }
    
    public void updateUserData(Long userId, String name, String email) {
        SharedUserData sharedData = sharedDataRepository.findByUserId(userId)
            .orElseThrow(() -> new UserDataNotFoundException("User data not found: " + userId));
        
        sharedData.setName(name);
        sharedData.setEmail(email);
        sharedData.setLastUpdated(Instant.now());
        
        sharedDataRepository.save(sharedData);
    }
}
```

## 16.6 Saga Pattern Variations

The Saga pattern manages distributed transactions through a series of local transactions.

### Orchestration-based Saga:

```java
// Orchestration-based Saga
@Service
public class OrderSagaOrchestrator {
    @Autowired
    private InventoryServiceClient inventoryServiceClient;
    @Autowired
    private PaymentServiceClient paymentServiceClient;
    @Autowired
    private ShippingServiceClient shippingServiceClient;
    
    public void executeOrderSaga(OrderRequest request) {
        String sagaId = UUID.randomUUID().toString();
        List<SagaStep> steps = new ArrayList<>();
        
        try {
            // Step 1: Reserve inventory
            steps.add(new SagaStep("RESERVE_INVENTORY", () -> {
                inventoryServiceClient.reserveInventory(request.getProductId(), request.getQuantity());
            }, () -> {
                inventoryServiceClient.releaseInventory(request.getProductId(), request.getQuantity());
            }));
            
            // Step 2: Process payment
            steps.add(new SagaStep("PROCESS_PAYMENT", () -> {
                paymentServiceClient.processPayment(request.getPaymentInfo());
            }, () -> {
                paymentServiceClient.refundPayment(request.getPaymentInfo());
            }));
            
            // Step 3: Create shipping label
            steps.add(new SagaStep("CREATE_SHIPPING_LABEL", () -> {
                shippingServiceClient.createShippingLabel(request.getOrderId(), request.getShippingAddress());
            }, () -> {
                shippingServiceClient.cancelShippingLabel(request.getOrderId());
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
```

### Choreography-based Saga:

```java
// Choreography-based Saga
@Service
public class OrderSagaChoreography {
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
        // Create shipping label
        eventPublisher.publishEvent(new OrderSagaEvent(
            event.getSagaId(), 
            "SHIPPING_LABEL_CREATE_REQUESTED", 
            event.getPayload()
        ));
    }
    
    @EventListener
    public void handleShippingLabelCreated(OrderSagaEvent event) {
        // Complete order
        eventPublisher.publishEvent(new OrderSagaEvent(
            event.getSagaId(), 
            "ORDER_COMPLETED", 
            event.getPayload()
        ));
    }
}
```

## 16.7 Event Sourcing Patterns

Event Sourcing stores the state of an application as a sequence of events.

### Event Store:

```java
// Event Store
@Service
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
}
```

### Aggregate with Event Sourcing:

```java
// Aggregate with Event Sourcing
public class Order {
    private Long id;
    private Long userId;
    private List<OrderItem> items;
    private OrderStatus status;
    private List<DomainEvent> uncommittedEvents = new ArrayList<>();
    
    public Order(Long id, Long userId, List<OrderItem> items) {
        this.id = id;
        this.userId = userId;
        this.items = items;
        this.status = OrderStatus.PENDING;
        
        addEvent(new OrderCreatedEvent(id, userId, items));
    }
    
    public void addItem(Product product, int quantity) {
        OrderItem item = new OrderItem(product.getId(), quantity, product.getPrice());
        items.add(item);
        addEvent(new OrderItemAddedEvent(id, item));
    }
    
    public void confirm() {
        this.status = OrderStatus.CONFIRMED;
        addEvent(new OrderConfirmedEvent(id));
    }
    
    public void cancel() {
        this.status = OrderStatus.CANCELLED;
        addEvent(new OrderCancelledEvent(id));
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
```

## 16.8 CQRS Patterns

CQRS separates read and write operations, allowing different models for commands and queries.

### Command Side:

```java
// Command Handler
@Component
public class CreateOrderCommandHandler {
    @Autowired
    private OrderRepository orderRepository;
    @Autowired
    private EventPublisher eventPublisher;
    
    public void handle(CreateOrderCommand command) {
        Order order = new Order(command.getUserId(), command.getItems());
        orderRepository.save(order);
        
        eventPublisher.publishOrderCreated(order);
    }
}

// Command Controller
@RestController
@RequestMapping("/api/commands")
public class OrderCommandController {
    @Autowired
    private CreateOrderCommandHandler createOrderCommandHandler;
    
    @PostMapping("/orders")
    public ResponseEntity<Void> createOrder(@RequestBody CreateOrderCommand command) {
        createOrderCommandHandler.handle(command);
        return ResponseEntity.ok().build();
    }
}
```

### Query Side:

```java
// Query Handler
@Component
public class GetOrderQueryHandler {
    @Autowired
    private OrderReadModelRepository orderReadModelRepository;
    
    public OrderReadModel handle(GetOrderQuery query) {
        return orderReadModelRepository.findById(query.getOrderId());
    }
}

// Query Controller
@RestController
@RequestMapping("/api/queries")
public class OrderQueryController {
    @Autowired
    private GetOrderQueryHandler getOrderQueryHandler;
    
    @GetMapping("/orders/{id}")
    public ResponseEntity<OrderReadModel> getOrder(@PathVariable Long id) {
        GetOrderQuery query = new GetOrderQuery(id);
        OrderReadModel order = getOrderQueryHandler.handle(query);
        return ResponseEntity.ok(order);
    }
}
```

### Read Model Projection:

```java
// Read Model Projection
@Component
public class OrderProjectionHandler {
    @Autowired
    private OrderReadModelRepository orderReadModelRepository;
    
    @EventListener
    public void handleOrderCreated(OrderCreatedEvent event) {
        OrderReadModel readModel = OrderReadModel.builder()
            .orderId(event.getOrderId())
            .userId(event.getUserId())
            .status("PENDING")
            .createdAt(event.getTimestamp())
            .build();
        
        orderReadModelRepository.save(readModel);
    }
    
    @EventListener
    public void handleOrderConfirmed(OrderConfirmedEvent event) {
        OrderReadModel readModel = orderReadModelRepository.findById(event.getOrderId());
        if (readModel != null) {
            readModel.setStatus("CONFIRMED");
            orderReadModelRepository.save(readModel);
        }
    }
}
```

This comprehensive guide covers all aspects of microservices patterns, providing both theoretical understanding and practical implementation examples.