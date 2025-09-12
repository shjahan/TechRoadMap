# Section 18 – Microservices Concurrency

## 18.1 Service-to-Service Communication

Service-to-service communication in microservices architecture involves multiple services communicating concurrently while maintaining reliability and performance.

### Key Concepts
- **Asynchronous Communication**: Services don't wait for immediate responses
- **Service Discovery**: Finding and connecting to available services
- **Load Balancing**: Distributing requests across multiple service instances
- **Circuit Breaking**: Preventing cascading failures

### Real-World Analogy
Think of a large corporation with different departments (microservices). When the sales department needs information from the inventory department, they send a request. The inventory department processes it and responds. Multiple departments can work simultaneously, and if one department is overloaded, requests can be routed to other available departments.

### Java Example
```java
// Service client with circuit breaker pattern
@Service
public class OrderServiceClient {
    private final RestTemplate restTemplate;
    private final CircuitBreaker circuitBreaker;
    private final String inventoryServiceUrl;
    
    public OrderServiceClient(RestTemplate restTemplate, 
                            CircuitBreaker circuitBreaker,
                            @Value("${inventory.service.url}") String inventoryServiceUrl) {
        this.restTemplate = restTemplate;
        this.circuitBreaker = circuitBreaker;
        this.inventoryServiceUrl = inventoryServiceUrl;
    }
    
    public CompletableFuture<InventoryResponse> checkInventory(String productId, int quantity) {
        return CompletableFuture.supplyAsync(() -> {
            try {
                return circuitBreaker.executeSupplier(() -> {
                    String url = inventoryServiceUrl + "/inventory/" + productId + "/check";
                    InventoryRequest request = new InventoryRequest(productId, quantity);
                    
                    ResponseEntity<InventoryResponse> response = restTemplate.postForEntity(
                        url, request, InventoryResponse.class
                    );
                    
                    return response.getBody();
                });
            } catch (Exception e) {
                // Fallback to default response
                return new InventoryResponse(productId, false, 0);
            }
        });
    }
    
    public CompletableFuture<PaymentResponse> processPayment(String orderId, BigDecimal amount) {
        return CompletableFuture.supplyAsync(() -> {
            try {
                return circuitBreaker.executeSupplier(() -> {
                    String url = inventoryServiceUrl + "/payment/process";
                    PaymentRequest request = new PaymentRequest(orderId, amount);
                    
                    ResponseEntity<PaymentResponse> response = restTemplate.postForEntity(
                        url, request, PaymentResponse.class
                    );
                    
                    return response.getBody();
                });
            } catch (Exception e) {
                throw new PaymentProcessingException("Payment service unavailable", e);
            }
        });
    }
}
```

## 18.2 Event-Driven Architecture

Event-driven architecture enables loose coupling between microservices through asynchronous event processing and message passing.

### Key Concepts
- **Event Sourcing**: Storing state changes as events
- **Event Streaming**: Continuous flow of events between services
- **Event Handlers**: Services that react to specific events
- **Event Ordering**: Ensuring events are processed in correct sequence

### Real-World Analogy
Think of a news agency where different departments (services) publish news events. The sports department publishes a "game finished" event, which triggers the statistics department to calculate player stats, the marketing department to update social media, and the finance department to process betting results. Each department works independently but reacts to relevant events.

### Java Example
```java
// Event-driven order processing
@Component
public class OrderEventHandler {
    private final ApplicationEventPublisher eventPublisher;
    private final OrderService orderService;
    private final InventoryService inventoryService;
    private final PaymentService paymentService;
    
    @EventListener
    @Async
    public void handleOrderCreated(OrderCreatedEvent event) {
        Order order = event.getOrder();
        
        // Process inventory check
        CompletableFuture<Boolean> inventoryCheck = inventoryService
            .checkAvailability(order.getProductId(), order.getQuantity())
            .thenApply(available -> {
                if (available) {
                    eventPublisher.publishEvent(new InventoryReservedEvent(order));
                } else {
                    eventPublisher.publishEvent(new InventoryUnavailableEvent(order));
                }
                return available;
            });
        
        // Process payment
        CompletableFuture<Boolean> paymentProcess = paymentService
            .processPayment(order.getOrderId(), order.getAmount())
            .thenApply(success -> {
                if (success) {
                    eventPublisher.publishEvent(new PaymentProcessedEvent(order));
                } else {
                    eventPublisher.publishEvent(new PaymentFailedEvent(order));
                }
                return success;
            });
        
        // Wait for both to complete
        CompletableFuture.allOf(inventoryCheck, paymentProcess)
            .thenRun(() -> {
                if (inventoryCheck.join() && paymentProcess.join()) {
                    eventPublisher.publishEvent(new OrderConfirmedEvent(order));
                } else {
                    eventPublisher.publishEvent(new OrderCancelledEvent(order));
                }
            });
    }
    
    @EventListener
    @Async
    public void handleInventoryReserved(InventoryReservedEvent event) {
        // Update order status
        orderService.updateOrderStatus(event.getOrder().getOrderId(), "INVENTORY_RESERVED");
    }
    
    @EventListener
    @Async
    public void handlePaymentProcessed(PaymentProcessedEvent event) {
        // Update order status
        orderService.updateOrderStatus(event.getOrder().getOrderId(), "PAYMENT_PROCESSED");
    }
}
```

## 18.3 Saga Pattern

The Saga pattern manages distributed transactions across multiple microservices by breaking them into a sequence of local transactions with compensating actions.

### Key Concepts
- **Local Transactions**: Each service manages its own transaction
- **Compensating Actions**: Undo operations when failures occur
- **Orchestration**: Central coordinator manages the saga
- **Choreography**: Services coordinate through events

### Real-World Analogy
Think of planning a wedding where you need to book a venue, hire a caterer, and order flowers. If the venue booking fails, you need to cancel the caterer and flower orders. Each booking is a local transaction, and cancellations are compensating actions.

### Java Example
```java
// Saga orchestrator for order processing
@Component
public class OrderSagaOrchestrator {
    private final OrderService orderService;
    private final InventoryService inventoryService;
    private final PaymentService paymentService;
    private final ShippingService shippingService;
    
    @SagaOrchestrationStart
    public void startOrderSaga(OrderCreatedEvent event) {
        Order order = event.getOrder();
        
        // Step 1: Reserve inventory
        inventoryService.reserveInventory(order.getProductId(), order.getQuantity())
            .thenCompose(inventoryResult -> {
                if (inventoryResult.isSuccess()) {
                    return paymentService.processPayment(order.getOrderId(), order.getAmount());
                } else {
                    return CompletableFuture.completedFuture(
                        new PaymentResult(false, "Inventory not available")
                    );
                }
            })
            .thenCompose(paymentResult -> {
                if (paymentResult.isSuccess()) {
                    return shippingService.createShipment(order.getOrderId(), order.getAddress());
                } else {
                    // Compensate: release inventory
                    return inventoryService.releaseInventory(order.getProductId(), order.getQuantity())
                        .thenApply(v -> new ShippingResult(false, "Payment failed"));
                }
            })
            .thenAccept(shippingResult -> {
                if (shippingResult.isSuccess()) {
                    orderService.updateOrderStatus(order.getOrderId(), "COMPLETED");
                } else {
                    // Compensate: refund payment and release inventory
                    compensateOrder(order);
                }
            });
    }
    
    private void compensateOrder(Order order) {
        // Compensating actions
        CompletableFuture.allOf(
            paymentService.refundPayment(order.getOrderId()),
            inventoryService.releaseInventory(order.getProductId(), order.getQuantity())
        ).thenRun(() -> {
            orderService.updateOrderStatus(order.getOrderId(), "CANCELLED");
        });
    }
}
```

## 18.4 Circuit Breaker Pattern

The Circuit Breaker pattern prevents cascading failures by monitoring service calls and opening the circuit when failure rates exceed thresholds.

### Key Concepts
- **Circuit States**: Closed, Open, Half-Open
- **Failure Thresholds**: Configurable failure rates
- **Timeout Handling**: Automatic circuit opening
- **Fallback Mechanisms**: Alternative responses when circuit is open

### Real-World Analogy
Think of a home's electrical circuit breaker. When there's too much current (too many failures), the breaker trips (opens) to prevent damage. After a while, you can try to reset it (half-open) to see if the problem is fixed, and if it works, it closes again.

### Java Example
```java
// Circuit breaker implementation
@Component
public class ServiceCircuitBreaker {
    private final AtomicInteger failureCount = new AtomicInteger(0);
    private final AtomicInteger successCount = new AtomicInteger(0);
    private final AtomicReference<CircuitState> state = new AtomicReference<>(CircuitState.CLOSED);
    private final long timeoutMs;
    private final int failureThreshold;
    private final long retryTimeoutMs;
    private volatile long lastFailureTime = 0;
    
    public enum CircuitState {
        CLOSED, OPEN, HALF_OPEN
    }
    
    public <T> T execute(Supplier<T> operation, Supplier<T> fallback) {
        if (state.get() == CircuitState.OPEN) {
            if (System.currentTimeMillis() - lastFailureTime > retryTimeoutMs) {
                state.set(CircuitState.HALF_OPEN);
                successCount.set(0);
            } else {
                return fallback.get();
            }
        }
        
        try {
            T result = operation.get();
            onSuccess();
            return result;
        } catch (Exception e) {
            onFailure();
            return fallback.get();
        }
    }
    
    private void onSuccess() {
        successCount.incrementAndGet();
        if (state.get() == CircuitState.HALF_OPEN) {
            if (successCount.get() >= 3) {
                state.set(CircuitState.CLOSED);
                failureCount.set(0);
            }
        }
    }
    
    private void onFailure() {
        lastFailureTime = System.currentTimeMillis();
        int failures = failureCount.incrementAndGet();
        
        if (failures >= failureThreshold) {
            state.set(CircuitState.OPEN);
        }
    }
    
    public CircuitState getState() {
        return state.get();
    }
}

// Usage in service
@Service
public class ExternalServiceClient {
    private final ServiceCircuitBreaker circuitBreaker;
    private final RestTemplate restTemplate;
    
    public String callExternalService(String data) {
        return circuitBreaker.execute(
            () -> {
                ResponseEntity<String> response = restTemplate.postForEntity(
                    "/external-service", data, String.class
                );
                return response.getBody();
            },
            () -> "Service temporarily unavailable - using cached data"
        );
    }
}
```

## 18.5 Bulkhead Pattern

The Bulkhead pattern isolates critical resources to prevent failures in one area from affecting the entire system.

### Key Concepts
- **Resource Isolation**: Separate pools for different operations
- **Failure Containment**: Limit impact of failures
- **Independent Scaling**: Scale resources independently
- **Priority Management**: Ensure critical operations continue

### Real-World Analogy
Think of a ship with watertight compartments (bulkheads). If one compartment floods, the water doesn't spread to other compartments, keeping the ship afloat. Similarly, if one service fails, it doesn't bring down the entire system.

### Java Example
```java
// Bulkhead pattern implementation
@Component
public class BulkheadServiceManager {
    private final ExecutorService criticalOperationsPool;
    private final ExecutorService standardOperationsPool;
    private final ExecutorService backgroundTasksPool;
    
    public BulkheadServiceManager() {
        // Separate thread pools for different operation types
        this.criticalOperationsPool = Executors.newFixedThreadPool(5);
        this.standardOperationsPool = Executors.newFixedThreadPool(10);
        this.backgroundTasksPool = Executors.newFixedThreadPool(3);
    }
    
    public CompletableFuture<String> processCriticalOperation(String data) {
        return CompletableFuture.supplyAsync(() -> {
            try {
                // Critical operation - uses dedicated pool
                Thread.sleep(1000); // Simulate processing
                return "Critical operation completed: " + data;
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                throw new RuntimeException("Critical operation interrupted", e);
            }
        }, criticalOperationsPool);
    }
    
    public CompletableFuture<String> processStandardOperation(String data) {
        return CompletableFuture.supplyAsync(() -> {
            try {
                // Standard operation - uses separate pool
                Thread.sleep(500); // Simulate processing
                return "Standard operation completed: " + data;
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                throw new RuntimeException("Standard operation interrupted", e);
            }
        }, standardOperationsPool);
    }
    
    public CompletableFuture<Void> processBackgroundTask(String data) {
        return CompletableFuture.runAsync(() -> {
            try {
                // Background task - uses separate pool
                Thread.sleep(2000); // Simulate processing
                System.out.println("Background task completed: " + data);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                throw new RuntimeException("Background task interrupted", e);
            }
        }, backgroundTasksPool);
    }
    
    // Health check for each bulkhead
    public Map<String, String> getBulkheadHealth() {
        Map<String, String> health = new HashMap<>();
        health.put("critical", isPoolHealthy(criticalOperationsPool) ? "HEALTHY" : "UNHEALTHY");
        health.put("standard", isPoolHealthy(standardOperationsPool) ? "HEALTHY" : "UNHEALTHY");
        health.put("background", isPoolHealthy(backgroundTasksPool) ? "HEALTHY" : "UNHEALTHY");
        return health;
    }
    
    private boolean isPoolHealthy(ExecutorService pool) {
        return !pool.isShutdown() && !pool.isTerminated();
    }
}
```

## 18.6 Timeout and Retry Patterns

Timeout and retry patterns handle transient failures by implementing configurable timeouts and automatic retry mechanisms.

### Key Concepts
- **Exponential Backoff**: Increasing delays between retries
- **Jitter**: Random variation in retry delays
- **Maximum Retries**: Limiting retry attempts
- **Timeout Configuration**: Setting appropriate timeouts

### Real-World Analogy
Think of calling a busy restaurant. If no one answers, you wait a bit and try again. If still busy, you wait longer before the next attempt. Eventually, you either get through or give up after several attempts.

### Java Example
```java
// Retry and timeout service
@Component
public class RetryableService {
    private final Random random = new Random();
    
    public <T> T executeWithRetry(Supplier<T> operation, RetryConfig config) {
        int attempts = 0;
        Exception lastException = null;
        
        while (attempts < config.getMaxRetries()) {
            try {
                return operation.get();
            } catch (Exception e) {
                lastException = e;
                attempts++;
                
                if (attempts >= config.getMaxRetries()) {
                    break;
                }
                
                // Calculate delay with exponential backoff and jitter
                long delay = calculateDelay(attempts, config);
                try {
                    Thread.sleep(delay);
                } catch (InterruptedException ie) {
                    Thread.currentThread().interrupt();
                    throw new RuntimeException("Retry interrupted", ie);
                }
            }
        }
        
        throw new RetryExhaustedException("Max retries exceeded", lastException);
    }
    
    private long calculateDelay(int attempt, RetryConfig config) {
        // Exponential backoff: baseDelay * 2^(attempt-1)
        long baseDelay = config.getBaseDelayMs();
        long exponentialDelay = baseDelay * (1L << (attempt - 1));
        
        // Add jitter: ±25% random variation
        long jitter = (long) (exponentialDelay * 0.25 * (random.nextDouble() - 0.5));
        
        return Math.min(exponentialDelay + jitter, config.getMaxDelayMs());
    }
    
    // Configuration class
    public static class RetryConfig {
        private final int maxRetries;
        private final long baseDelayMs;
        private final long maxDelayMs;
        
        public RetryConfig(int maxRetries, long baseDelayMs, long maxDelayMs) {
            this.maxRetries = maxRetries;
            this.baseDelayMs = baseDelayMs;
            this.maxDelayMs = maxDelayMs;
        }
        
        // Getters
        public int getMaxRetries() { return maxRetries; }
        public long getBaseDelayMs() { return baseDelayMs; }
        public long getMaxDelayMs() { return maxDelayMs; }
    }
}

// Usage example
@Service
public class ExternalApiClient {
    private final RetryableService retryableService;
    private final RestTemplate restTemplate;
    
    public String callExternalApi(String endpoint, String data) {
        RetryConfig config = new RetryConfig(3, 1000, 10000); // 3 retries, 1s base delay, 10s max
        
        return retryableService.executeWithRetry(() -> {
            ResponseEntity<String> response = restTemplate.postForEntity(
                endpoint, data, String.class
            );
            return response.getBody();
        }, config);
    }
}
```

## 18.7 Idempotency

Idempotency ensures that operations can be safely repeated without causing unintended side effects, crucial for reliable microservices communication.

### Key Concepts
- **Idempotent Operations**: Same result regardless of execution count
- **Idempotency Keys**: Unique identifiers for operations
- **Duplicate Detection**: Identifying and handling duplicate requests
- **State Management**: Maintaining operation state

### Real-World Analogy
Think of a light switch. Pressing it once turns the light on, pressing it again turns it off, and pressing it a third time turns it on again. The result depends only on the current state, not how many times you've pressed it.

### Java Example
```java
// Idempotent service implementation
@Service
public class IdempotentOrderService {
    private final Map<String, OrderOperation> operationCache = new ConcurrentHashMap<>();
    private final OrderRepository orderRepository;
    
    public CompletableFuture<OrderResult> createOrder(String idempotencyKey, OrderRequest request) {
        // Check if operation already exists
        OrderOperation existingOperation = operationCache.get(idempotencyKey);
        if (existingOperation != null) {
            return CompletableFuture.completedFuture(existingOperation.getResult());
        }
        
        // Create new operation
        OrderOperation operation = new OrderOperation(idempotencyKey, request);
        operationCache.put(idempotencyKey, operation);
        
        return CompletableFuture.supplyAsync(() -> {
            try {
                // Check if order already exists in database
                Optional<Order> existingOrder = orderRepository.findByIdempotencyKey(idempotencyKey);
                if (existingOrder.isPresent()) {
                    OrderResult result = new OrderResult(existingOrder.get().getId(), "EXISTING");
                    operation.setResult(result);
                    return result;
                }
                
                // Create new order
                Order order = new Order();
                order.setIdempotencyKey(idempotencyKey);
                order.setCustomerId(request.getCustomerId());
                order.setAmount(request.getAmount());
                order.setStatus("PENDING");
                
                Order savedOrder = orderRepository.save(order);
                OrderResult result = new OrderResult(savedOrder.getId(), "CREATED");
                operation.setResult(result);
                
                return result;
                
            } catch (Exception e) {
                // Remove failed operation from cache
                operationCache.remove(idempotencyKey);
                throw new OrderCreationException("Failed to create order", e);
            }
        });
    }
    
    // Operation tracking class
    private static class OrderOperation {
        private final String idempotencyKey;
        private final OrderRequest request;
        private volatile OrderResult result;
        private final long timestamp;
        
        public OrderOperation(String idempotencyKey, OrderRequest request) {
            this.idempotencyKey = idempotencyKey;
            this.request = request;
            this.timestamp = System.currentTimeMillis();
        }
        
        // Getters and setters
        public String getIdempotencyKey() { return idempotencyKey; }
        public OrderRequest getRequest() { return request; }
        public OrderResult getResult() { return result; }
        public void setResult(OrderResult result) { this.result = result; }
        public long getTimestamp() { return timestamp; }
    }
}
```

## 18.8 Distributed Tracing

Distributed tracing tracks requests across multiple microservices to provide visibility into system behavior and performance.

### Key Concepts
- **Trace**: Complete request journey across services
- **Span**: Individual operation within a trace
- **Context Propagation**: Passing trace information between services
- **Sampling**: Selecting which requests to trace

### Real-World Analogy
Think of tracking a package through a delivery network. Each stop (service) logs when the package arrives and leaves, creating a complete journey map. If there's a delay, you can see exactly where it occurred.

### Java Example
```java
// Distributed tracing implementation
@Component
public class TracingService {
    private final Tracer tracer;
    
    public <T> T traceOperation(String operationName, Supplier<T> operation) {
        Span span = tracer.nextSpan()
            .name(operationName)
            .start();
        
        try (Tracer.SpanInScope ws = tracer.withSpanInScope(span)) {
            return operation.get();
        } catch (Exception e) {
            span.tag("error", true);
            span.tag("error.message", e.getMessage());
            throw e;
        } finally {
            span.end();
        }
    }
    
    public <T> CompletableFuture<T> traceAsyncOperation(String operationName, Supplier<T> operation) {
        Span parentSpan = tracer.currentSpan();
        
        return CompletableFuture.supplyAsync(() -> {
            Span span = tracer.nextSpan()
                .name(operationName)
                .start();
            
            if (parentSpan != null) {
                span.tag("parent.traceId", parentSpan.context().traceId());
            }
            
            try (Tracer.SpanInScope ws = tracer.withSpanInScope(span)) {
                return operation.get();
            } catch (Exception e) {
                span.tag("error", true);
                span.tag("error.message", e.getMessage());
                throw e;
            } finally {
                span.end();
            }
        });
    }
}

// Service with tracing
@RestController
public class OrderController {
    private final TracingService tracingService;
    private final OrderService orderService;
    private final InventoryService inventoryService;
    
    @PostMapping("/orders")
    public CompletableFuture<ResponseEntity<OrderResponse>> createOrder(@RequestBody OrderRequest request) {
        return tracingService.traceAsyncOperation("create-order", () -> {
            // Trace inventory check
            return tracingService.traceAsyncOperation("check-inventory", () -> {
                return inventoryService.checkAvailability(request.getProductId(), request.getQuantity());
            }).thenCompose(inventoryAvailable -> {
                if (inventoryAvailable) {
                    // Trace order creation
                    return tracingService.traceAsyncOperation("create-order-entity", () -> {
                        return orderService.createOrder(request);
                    });
                } else {
                    throw new InventoryUnavailableException("Product not available");
                }
            });
        }).thenApply(order -> ResponseEntity.ok(new OrderResponse(order)));
    }
}
```

This comprehensive explanation covers all aspects of microservices concurrency, providing both theoretical understanding and practical examples to illustrate each concept.