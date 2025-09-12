# Section 19 – Cloud Concurrency

## 19.1 Auto-scaling

Auto-scaling automatically adjusts computing resources based on demand, ensuring optimal performance and cost efficiency in cloud environments.

### Key Concepts
- **Horizontal Scaling**: Adding or removing instances
- **Vertical Scaling**: Increasing or decreasing instance capacity
- **Scaling Policies**: Rules that trigger scaling actions
- **Load Metrics**: CPU, memory, request rate, and custom metrics

### Real-World Analogy
Think of a restaurant that automatically adjusts its staff based on customer demand. During lunch rush, more chefs and waiters are called in. During slow periods, some staff go home. The restaurant maintains service quality while managing costs efficiently.

### Java Example
```java
// Auto-scaling service implementation
@Component
public class AutoScalingService {
    private final CloudProviderClient cloudClient;
    private final MetricsCollector metricsCollector;
    private final ScalingPolicy scalingPolicy;
    
    @Scheduled(fixedRate = 30000) // Check every 30 seconds
    public void evaluateScaling() {
        ScalingMetrics metrics = metricsCollector.getCurrentMetrics();
        ScalingDecision decision = scalingPolicy.evaluate(metrics);
        
        if (decision.shouldScale()) {
            executeScalingAction(decision);
        }
    }
    
    private void executeScalingAction(ScalingDecision decision) {
        switch (decision.getAction()) {
            case SCALE_OUT:
                scaleOut(decision.getTargetInstances());
                break;
            case SCALE_IN:
                scaleIn(decision.getTargetInstances());
                break;
            case SCALE_UP:
                scaleUp(decision.getTargetCapacity());
                break;
            case SCALE_DOWN:
                scaleDown(decision.getTargetCapacity());
                break;
        }
    }
    
    private void scaleOut(int targetInstances) {
        int currentInstances = cloudClient.getCurrentInstanceCount();
        int instancesToAdd = targetInstances - currentInstances;
        
        if (instancesToAdd > 0) {
            cloudClient.launchInstances(instancesToAdd);
            logScalingEvent("SCALE_OUT", currentInstances, targetInstances);
        }
    }
    
    private void scaleIn(int targetInstances) {
        int currentInstances = cloudClient.getCurrentInstanceCount();
        int instancesToRemove = currentInstances - targetInstances;
        
        if (instancesToRemove > 0) {
            List<String> instancesToTerminate = cloudClient.selectInstancesForTermination(instancesToRemove);
            cloudClient.terminateInstances(instancesToTerminate);
            logScalingEvent("SCALE_IN", currentInstances, targetInstances);
        }
    }
    
    // Scaling policy configuration
    public static class ScalingPolicy {
        private final double cpuThresholdHigh = 70.0;
        private final double cpuThresholdLow = 30.0;
        private final int minInstances = 2;
        private final int maxInstances = 10;
        
        public ScalingDecision evaluate(ScalingMetrics metrics) {
            double avgCpu = metrics.getAverageCpuUsage();
            int currentInstances = metrics.getCurrentInstanceCount();
            
            if (avgCpu > cpuThresholdHigh && currentInstances < maxInstances) {
                return new ScalingDecision(ScalingAction.SCALE_OUT, currentInstances + 1);
            } else if (avgCpu < cpuThresholdLow && currentInstances > minInstances) {
                return new ScalingDecision(ScalingAction.SCALE_IN, currentInstances - 1);
            }
            
            return new ScalingDecision(ScalingAction.NO_ACTION, currentInstances);
        }
    }
}
```

## 19.2 Load Balancing

Load balancing distributes incoming requests across multiple instances to ensure optimal resource utilization and high availability.

### Key Concepts
- **Load Distribution**: Evenly spreading requests across instances
- **Health Checks**: Monitoring instance health and availability
- **Session Affinity**: Sticky sessions for stateful applications
- **Algorithm Selection**: Round-robin, least connections, weighted, etc.

### Real-World Analogy
Think of a bank with multiple tellers. A load balancer is like a queue manager who directs customers to the teller with the shortest line or who is most appropriate for their type of transaction.

### Java Example
```java
// Load balancer implementation
@Component
public class LoadBalancer {
    private final List<ServiceInstance> instances = new CopyOnWriteArrayList<>();
    private final LoadBalancingStrategy strategy;
    private final HealthChecker healthChecker;
    
    public LoadBalancer(LoadBalancingStrategy strategy, HealthChecker healthChecker) {
        this.strategy = strategy;
        this.healthChecker = healthChecker;
    }
    
    public ServiceInstance selectInstance() {
        List<ServiceInstance> healthyInstances = getHealthyInstances();
        
        if (healthyInstances.isEmpty()) {
            throw new NoAvailableInstancesException("No healthy instances available");
        }
        
        return strategy.selectInstance(healthyInstances);
    }
    
    private List<ServiceInstance> getHealthyInstances() {
        return instances.stream()
            .filter(healthChecker::isHealthy)
            .collect(Collectors.toList());
    }
    
    public void addInstance(ServiceInstance instance) {
        instances.add(instance);
    }
    
    public void removeInstance(String instanceId) {
        instances.removeIf(instance -> instance.getId().equals(instanceId));
    }
    
    // Round-robin strategy
    public static class RoundRobinStrategy implements LoadBalancingStrategy {
        private final AtomicInteger counter = new AtomicInteger(0);
        
        @Override
        public ServiceInstance selectInstance(List<ServiceInstance> instances) {
            int index = counter.getAndIncrement() % instances.size();
            return instances.get(index);
        }
    }
    
    // Least connections strategy
    public static class LeastConnectionsStrategy implements LoadBalancingStrategy {
        @Override
        public ServiceInstance selectInstance(List<ServiceInstance> instances) {
            return instances.stream()
                .min(Comparator.comparing(ServiceInstance::getActiveConnections))
                .orElseThrow(() -> new NoAvailableInstancesException("No instances available"));
        }
    }
    
    // Weighted round-robin strategy
    public static class WeightedRoundRobinStrategy implements LoadBalancingStrategy {
        private final AtomicInteger counter = new AtomicInteger(0);
        
        @Override
        public ServiceInstance selectInstance(List<ServiceInstance> instances) {
            int totalWeight = instances.stream()
                .mapToInt(ServiceInstance::getWeight)
                .sum();
            
            int randomWeight = counter.getAndIncrement() % totalWeight;
            int currentWeight = 0;
            
            for (ServiceInstance instance : instances) {
                currentWeight += instance.getWeight();
                if (randomWeight < currentWeight) {
                    return instance;
                }
            }
            
            return instances.get(instances.size() - 1);
        }
    }
}
```

## 19.3 Serverless Concurrency

Serverless concurrency handles multiple concurrent requests in a serverless environment where functions are executed on-demand.

### Key Concepts
- **Function Invocation**: On-demand execution of code
- **Cold Starts**: Initialization overhead for new function instances
- **Concurrency Limits**: Maximum concurrent executions per function
- **Resource Allocation**: Dynamic resource assignment

### Real-World Analogy
Think of a food truck that only operates when customers arrive. When someone orders food, the truck starts up, prepares the meal, serves it, and then shuts down. Multiple customers can be served simultaneously by having multiple trucks (function instances).

### Java Example
```java
// Serverless function handler
@Component
public class ServerlessFunctionHandler {
    private final AtomicInteger concurrentExecutions = new AtomicInteger(0);
    private final int maxConcurrency = 1000;
    private final Map<String, Object> sharedState = new ConcurrentHashMap<>();
    
    @FunctionName("processOrder")
    public CompletableFuture<OrderResponse> processOrder(
            @HttpTrigger(name = "req", methods = {HttpMethod.POST}) HttpRequestMessage<OrderRequest> request,
            ExecutionContext context) {
        
        // Check concurrency limits
        if (concurrentExecutions.get() >= maxConcurrency) {
            throw new TooManyConcurrentExecutionsException("Concurrency limit exceeded");
        }
        
        int currentConcurrency = concurrentExecutions.incrementAndGet();
        context.getLogger().info("Current concurrency: " + currentConcurrency);
        
        try {
            OrderRequest orderRequest = request.getBody();
            
            // Process order asynchronously
            return processOrderAsync(orderRequest, context)
                .whenComplete((result, throwable) -> {
                    concurrentExecutions.decrementAndGet();
                    if (throwable != null) {
                        context.getLogger().severe("Error processing order: " + throwable.getMessage());
                    }
                });
                
        } catch (Exception e) {
            concurrentExecutions.decrementAndGet();
            throw e;
        }
    }
    
    private CompletableFuture<OrderResponse> processOrderAsync(OrderRequest request, ExecutionContext context) {
        return CompletableFuture.supplyAsync(() -> {
            // Simulate processing time
            try {
                Thread.sleep(1000);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                throw new RuntimeException("Processing interrupted", e);
            }
            
            // Process order
            OrderResponse response = new OrderResponse();
            response.setOrderId(UUID.randomUUID().toString());
            response.setStatus("PROCESSED");
            response.setProcessedAt(Instant.now());
            
            // Update shared state
            sharedState.put(response.getOrderId(), response);
            
            context.getLogger().info("Order processed: " + response.getOrderId());
            return response;
        });
    }
    
    // Batch processing function
    @FunctionName("processBatch")
    public CompletableFuture<BatchResponse> processBatch(
            @QueueTrigger(name = "batch", queueName = "order-batch") String batchData,
            ExecutionContext context) {
        
        return CompletableFuture.supplyAsync(() -> {
            List<OrderRequest> orders = parseBatchData(batchData);
            List<CompletableFuture<OrderResponse>> futures = orders.stream()
                .map(order -> processOrderAsync(order, context))
                .collect(Collectors.toList());
            
            // Wait for all orders to complete
            CompletableFuture<Void> allFutures = CompletableFuture.allOf(
                futures.toArray(new CompletableFuture[0])
            );
            
            return allFutures.thenApply(v -> {
                List<OrderResponse> responses = futures.stream()
                    .map(CompletableFuture::join)
                    .collect(Collectors.toList());
                
                BatchResponse batchResponse = new BatchResponse();
                batchResponse.setProcessedCount(responses.size());
                batchResponse.setResponses(responses);
                return batchResponse;
            }).join();
        });
    }
}
```

## 19.4 Container Orchestration

Container orchestration manages the deployment, scaling, and networking of containerized applications across multiple hosts.

### Key Concepts
- **Container Lifecycle**: Starting, stopping, and restarting containers
- **Service Discovery**: Finding and connecting to services
- **Load Balancing**: Distributing traffic across containers
- **Health Monitoring**: Ensuring container health and availability

### Real-World Analogy
Think of a shipping company managing a fleet of trucks (containers) across multiple warehouses (hosts). The orchestration system decides which truck to use, where to send it, when to refuel it, and how to coordinate multiple deliveries efficiently.

### Java Example
```java
// Container orchestration service
@Service
public class ContainerOrchestrationService {
    private final KubernetesClient kubernetesClient;
    private final ServiceDiscovery serviceDiscovery;
    private final LoadBalancer loadBalancer;
    
    public void deployService(ServiceSpec spec) {
        Deployment deployment = createDeployment(spec);
        Service service = createService(spec);
        Ingress ingress = createIngress(spec);
        
        // Deploy in order
        kubernetesClient.apps().deployments().create(deployment);
        kubernetesClient.services().create(service);
        kubernetesClient.networking().v1().ingresses().create(ingress);
        
        // Wait for deployment to be ready
        waitForDeploymentReady(spec.getName(), spec.getReplicas());
    }
    
    public void scaleService(String serviceName, int replicas) {
        Deployment deployment = kubernetesClient.apps().deployments()
            .inNamespace("default")
            .withName(serviceName)
            .get();
        
        if (deployment != null) {
            deployment.getSpec().setReplicas(replicas);
            kubernetesClient.apps().deployments()
                .inNamespace("default")
                .withName(serviceName)
                .replace(deployment);
        }
    }
    
    public void updateService(String serviceName, String newImage) {
        Deployment deployment = kubernetesClient.apps().deployments()
            .inNamespace("default")
            .withName(serviceName)
            .get();
        
        if (deployment != null) {
            deployment.getSpec().getTemplate().getSpec().getContainers()
                .forEach(container -> container.setImage(newImage));
            
            kubernetesClient.apps().deployments()
                .inNamespace("default")
                .withName(serviceName)
                .replace(deployment);
        }
    }
    
    public List<Pod> getServicePods(String serviceName) {
        return kubernetesClient.pods()
            .inNamespace("default")
            .withLabel("app", serviceName)
            .list()
            .getItems();
    }
    
    public void rollbackService(String serviceName) {
        RolloutConfig rolloutConfig = new RolloutConfig();
        rolloutConfig.setName(serviceName);
        rolloutConfig.setRollbackToRevision(0); // Rollback to previous version
        
        kubernetesClient.apps().deployments()
            .inNamespace("default")
            .withName(serviceName)
            .rollout()
            .undo(rolloutConfig);
    }
    
    private void waitForDeploymentReady(String serviceName, int expectedReplicas) {
        int maxWaitTime = 300; // 5 minutes
        int waitTime = 0;
        
        while (waitTime < maxWaitTime) {
            Deployment deployment = kubernetesClient.apps().deployments()
                .inNamespace("default")
                .withName(serviceName)
                .get();
            
            if (deployment != null && 
                deployment.getStatus().getReadyReplicas() != null &&
                deployment.getStatus().getReadyReplicas() == expectedReplicas) {
                return;
            }
            
            try {
                Thread.sleep(5000); // Wait 5 seconds
                waitTime += 5;
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                throw new RuntimeException("Wait interrupted", e);
            }
        }
        
        throw new DeploymentTimeoutException("Deployment did not become ready in time");
    }
}
```

## 19.5 Message Queues

Message queues enable asynchronous communication between services, providing reliable message delivery and decoupling of components.

### Key Concepts
- **Message Persistence**: Storing messages until they are processed
- **Delivery Guarantees**: At-least-once, at-most-once, exactly-once
- **Dead Letter Queues**: Handling failed messages
- **Message Ordering**: Ensuring messages are processed in order

### Real-World Analogy
Think of a postal system where letters are placed in mailboxes (queues) and postal workers (consumers) pick them up and deliver them. If a delivery fails, the letter goes to a dead letter office for manual handling.

### Java Example
```java
// Message queue service
@Service
public class MessageQueueService {
    private final AmazonSQS sqsClient;
    private final String queueUrl;
    private final ExecutorService messageProcessor;
    
    public MessageQueueService(AmazonSQS sqsClient, @Value("${queue.url}") String queueUrl) {
        this.sqsClient = sqsClient;
        this.queueUrl = queueUrl;
        this.messageProcessor = Executors.newFixedThreadPool(10);
    }
    
    public void sendMessage(String messageBody, Map<String, String> attributes) {
        SendMessageRequest request = new SendMessageRequest()
            .withQueueUrl(queueUrl)
            .withMessageBody(messageBody)
            .withMessageAttributes(attributes.entrySet().stream()
                .collect(Collectors.toMap(
                    Map.Entry::getKey,
                    entry -> new MessageAttributeValue()
                        .withStringValue(entry.getValue())
                        .withDataType("String")
                )));
        
        try {
            SendMessageResult result = sqsClient.sendMessage(request);
            System.out.println("Message sent: " + result.getMessageId());
        } catch (Exception e) {
            throw new MessageSendException("Failed to send message", e);
        }
    }
    
    public void startMessageProcessing() {
        messageProcessor.submit(() -> {
            while (!Thread.currentThread().isInterrupted()) {
                try {
                    ReceiveMessageRequest request = new ReceiveMessageRequest()
                        .withQueueUrl(queueUrl)
                        .withMaxNumberOfMessages(10)
                        .withWaitTimeSeconds(20);
                    
                    ReceiveMessageResult result = sqsClient.receiveMessage(request);
                    List<Message> messages = result.getMessages();
                    
                    for (Message message : messages) {
                        processMessage(message);
                    }
                    
                } catch (Exception e) {
                    System.err.println("Error processing messages: " + e.getMessage());
                    try {
                        Thread.sleep(5000); // Wait before retrying
                    } catch (InterruptedException ie) {
                        Thread.currentThread().interrupt();
                        break;
                    }
                }
            }
        });
    }
    
    private void processMessage(Message message) {
        try {
            // Process message
            String messageBody = message.getBody();
            System.out.println("Processing message: " + messageBody);
            
            // Simulate processing
            Thread.sleep(1000);
            
            // Delete message after successful processing
            DeleteMessageRequest deleteRequest = new DeleteMessageRequest()
                .withQueueUrl(queueUrl)
                .withReceiptHandle(message.getReceiptHandle());
            
            sqsClient.deleteMessage(deleteRequest);
            System.out.println("Message processed and deleted: " + message.getMessageId());
            
        } catch (Exception e) {
            System.err.println("Error processing message " + message.getMessageId() + ": " + e.getMessage());
            
            // Move to dead letter queue after max retries
            if (getRetryCount(message) >= 3) {
                moveToDeadLetterQueue(message);
            }
        }
    }
    
    private int getRetryCount(Message message) {
        String retryCount = message.getAttributes().get("ApproximateReceiveCount");
        return retryCount != null ? Integer.parseInt(retryCount) : 0;
    }
    
    private void moveToDeadLetterQueue(Message message) {
        // Implementation to move message to dead letter queue
        System.out.println("Moving message to dead letter queue: " + message.getMessageId());
    }
}
```

## 19.6 Event Streaming

Event streaming enables real-time data processing and analysis by continuously processing streams of events.

### Key Concepts
- **Stream Processing**: Real-time processing of event streams
- **Event Ordering**: Maintaining event sequence and timing
- **Backpressure**: Handling situations where producers are faster than consumers
- **Windowing**: Processing events within time or count windows

### Real-World Analogy
Think of a live sports broadcast where events (goals, fouls, substitutions) happen continuously. The broadcast system processes these events in real-time, updating scores, statistics, and commentary as they occur.

### Java Example
```java
// Event streaming service
@Service
public class EventStreamingService {
    private final KafkaTemplate<String, String> kafkaTemplate;
    private final KafkaListenerContainerFactory<?> kafkaListenerContainerFactory;
    
    public void publishEvent(String topic, String event) {
        kafkaTemplate.send(topic, event);
    }
    
    @KafkaListener(topics = "user-events", groupId = "user-processor")
    public void processUserEvent(String event) {
        try {
            UserEvent userEvent = parseUserEvent(event);
            
            // Process event based on type
            switch (userEvent.getType()) {
                case "LOGIN":
                    handleLoginEvent(userEvent);
                    break;
                case "PURCHASE":
                    handlePurchaseEvent(userEvent);
                    break;
                case "LOGOUT":
                    handleLogoutEvent(userEvent);
                    break;
                default:
                    System.out.println("Unknown event type: " + userEvent.getType());
            }
            
        } catch (Exception e) {
            System.err.println("Error processing user event: " + e.getMessage());
        }
    }
    
    @KafkaListener(topics = "order-events", groupId = "order-processor")
    public void processOrderEvent(String event) {
        try {
            OrderEvent orderEvent = parseOrderEvent(event);
            
            // Process order event
            switch (orderEvent.getType()) {
                case "CREATED":
                    handleOrderCreated(orderEvent);
                    break;
                case "PAID":
                    handleOrderPaid(orderEvent);
                    break;
                case "SHIPPED":
                    handleOrderShipped(orderEvent);
                    break;
                case "DELIVERED":
                    handleOrderDelivered(orderEvent);
                    break;
            }
            
        } catch (Exception e) {
            System.err.println("Error processing order event: " + e.getMessage());
        }
    }
    
    // Stream processing with windowing
    @KafkaListener(topics = "metrics-events", groupId = "metrics-processor")
    public void processMetricsEvent(String event) {
        try {
            MetricsEvent metricsEvent = parseMetricsEvent(event);
            
            // Process metrics in time windows
            processMetricsWindow(metricsEvent);
            
        } catch (Exception e) {
            System.err.println("Error processing metrics event: " + e.getMessage());
        }
    }
    
    private void processMetricsWindow(MetricsEvent event) {
        // Implementation for windowed processing
        long windowStart = event.getTimestamp() - (event.getTimestamp() % 60000); // 1-minute windows
        String windowKey = event.getMetricName() + "-" + windowStart;
        
        // Aggregate metrics within window
        // This would typically use a stream processing framework like Kafka Streams
    }
}
```

## 19.7 Caching Strategies

Caching strategies improve performance by storing frequently accessed data in fast storage layers.

### Key Concepts
- **Cache Levels**: L1, L2, L3 cache hierarchies
- **Cache Invalidation**: Removing stale data from cache
- **Cache Warming**: Preloading cache with frequently accessed data
- **Cache Consistency**: Ensuring data consistency across cache layers

### Real-World Analogy
Think of a library with multiple storage levels: a small desk drawer for frequently used books (L1 cache), a nearby shelf for less frequent books (L2 cache), and a large warehouse for rarely used books (L3 cache). The librarian knows where to find each book quickly.

### Java Example
```java
// Multi-level caching service
@Service
public class CachingService {
    private final RedisTemplate<String, Object> redisTemplate;
    private final Map<String, Object> localCache = new ConcurrentHashMap<>();
    private final CacheMetrics cacheMetrics;
    
    public <T> T get(String key, Class<T> type) {
        // L1 Cache: Local cache
        T value = (T) localCache.get(key);
        if (value != null) {
            cacheMetrics.recordHit("L1", key);
            return value;
        }
        
        // L2 Cache: Redis
        value = (T) redisTemplate.opsForValue().get(key);
        if (value != null) {
            localCache.put(key, value);
            cacheMetrics.recordHit("L2", key);
            return value;
        }
        
        cacheMetrics.recordMiss(key);
        return null;
    }
    
    public <T> T getOrCompute(String key, Supplier<T> supplier, Duration ttl) {
        T value = get(key, (Class<T>) Object.class);
        if (value != null) {
            return value;
        }
        
        // Compute value
        value = supplier.get();
        
        // Store in both caches
        put(key, value, ttl);
        
        return value;
    }
    
    public void put(String key, Object value, Duration ttl) {
        // Store in local cache
        localCache.put(key, value);
        
        // Store in Redis with TTL
        redisTemplate.opsForValue().set(key, value, ttl);
        
        cacheMetrics.recordPut(key);
    }
    
    public void evict(String key) {
        localCache.remove(key);
        redisTemplate.delete(key);
        cacheMetrics.recordEvict(key);
    }
    
    public void evictPattern(String pattern) {
        // Evict from local cache
        localCache.entrySet().removeIf(entry -> 
            entry.getKey().matches(pattern));
        
        // Evict from Redis
        Set<String> keys = redisTemplate.keys(pattern);
        if (!keys.isEmpty()) {
            redisTemplate.delete(keys);
        }
        
        cacheMetrics.recordEvictPattern(pattern);
    }
    
    // Cache warming
    @EventListener
    public void warmCache(ApplicationReadyEvent event) {
        // Warm cache with frequently accessed data
        List<String> frequentKeys = getFrequentKeys();
        
        for (String key : frequentKeys) {
            getOrCompute(key, () -> loadData(key), Duration.ofHours(1));
        }
    }
    
    // Cache consistency
    @EventListener
    public void handleDataUpdate(DataUpdateEvent event) {
        String key = event.getKey();
        
        // Invalidate cache
        evict(key);
        
        // Notify other instances
        publishCacheInvalidation(key);
    }
}
```

## 19.8 CDN Concurrency

Content Delivery Networks (CDN) provide global distribution of content with low latency and high availability.

### Key Concepts
- **Edge Locations**: Geographically distributed servers
- **Content Caching**: Storing content at edge locations
- **Load Balancing**: Distributing requests across edge servers
- **Cache Invalidation**: Updating cached content when it changes

### Real-World Analogy
Think of a chain of restaurants with the same menu. Instead of having one central kitchen, each restaurant has its own kitchen (edge server) that can prepare the same dishes. Customers get their food faster because they don't have to wait for it to be delivered from a distant central kitchen.

### Java Example
```java
// CDN service implementation
@Service
public class CDNService {
    private final CloudFrontClient cloudFrontClient;
    private final S3Client s3Client;
    private final Map<String, String> edgeLocations = new HashMap<>();
    
    public void uploadContent(String key, byte[] content, String contentType) {
        // Upload to S3
        PutObjectRequest request = PutObjectRequest.builder()
            .bucket("my-cdn-bucket")
            .key(key)
            .contentType(contentType)
            .build();
        
        s3Client.putObject(request, RequestBody.fromBytes(content));
        
        // Invalidate CDN cache
        invalidateCache(key);
    }
    
    public String getContentUrl(String key) {
        // Generate signed URL for CDN
        return cloudFrontClient.generatePresignedUrl(
            GetObjectRequest.builder()
                .bucket("my-cdn-bucket")
                .key(key)
                .build(),
            Duration.ofHours(1)
        ).toString();
    }
    
    public void invalidateCache(String key) {
        // Create invalidation request
        CreateInvalidationRequest request = CreateInvalidationRequest.builder()
            .distributionId("E1234567890")
            .invalidationBatch(InvalidationBatch.builder()
                .paths("/" + key)
                .callerReference(UUID.randomUUID().toString())
                .build())
            .build();
        
        cloudFrontClient.createInvalidation(request);
    }
    
    public void invalidateCachePattern(String pattern) {
        // Invalidate multiple paths matching pattern
        List<String> paths = getPathsMatchingPattern(pattern);
        
        CreateInvalidationRequest request = CreateInvalidationRequest.builder()
            .distributionId("E1234567890")
            .invalidationBatch(InvalidationBatch.builder()
                .paths(paths.toArray(new String[0]))
                .callerReference(UUID.randomUUID().toString())
                .build())
            .build();
        
        cloudFrontClient.createInvalidation(request);
    }
    
    public CDNStats getCDNStats() {
        // Get CDN statistics
        GetDistributionRequest request = GetDistributionRequest.builder()
            .id("E1234567890")
            .build();
        
        GetDistributionResponse response = cloudFrontClient.getDistribution(request);
        
        CDNStats stats = new CDNStats();
        stats.setDistributionId(response.distribution().id());
        stats.setStatus(response.distribution().status());
        stats.setDomainName(response.distribution().domainName());
        stats.setLastModified(response.distribution().lastModifiedTime());
        
        return stats;
    }
    
    // Edge location management
    public void updateEdgeLocation(String location, String status) {
        edgeLocations.put(location, status);
    }
    
    public String getOptimalEdgeLocation(String clientIp) {
        // Determine optimal edge location based on client IP
        // This would typically use GeoIP lookup
        return edgeLocations.entrySet().stream()
            .filter(entry -> "ACTIVE".equals(entry.getValue()))
            .min(Comparator.comparing(entry -> 
                calculateDistance(clientIp, entry.getKey())))
            .map(Map.Entry::getKey)
            .orElse("us-east-1");
    }
    
    private double calculateDistance(String clientIp, String edgeLocation) {
        // Simplified distance calculation
        // In practice, this would use GeoIP databases
        return Math.random() * 1000;
    }
}
```

This comprehensive explanation covers all aspects of cloud concurrency, providing both theoretical understanding and practical examples to illustrate each concept.